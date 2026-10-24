import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const PRODUCTS_DIR = path.join(PROJECT_ROOT, 'data/products');
const PYTHON_PATH = path.join(PROJECT_ROOT, '.venv/bin/python');

// Next.js chỉ tự đọc .env trong thư mục app của chính nó (tools/dashboard/), KHÔNG đọc
// .env ở root dự án — nên phải tự nạp thủ công (GEMINI_API_KEY, v.v.) để truyền cho tiến trình Python con.
function loadRootEnv(): Record<string, string> {
  const envPath = path.join(PROJECT_ROOT, '.env');
  const vars: Record<string, string> = {};
  if (!fs.existsSync(envPath)) return vars;
  const content = fs.readFileSync(envPath, 'utf-8');
  for (const rawLine of content.split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const eqIdx = line.indexOf('=');
    if (eqIdx === -1) continue;
    const key = line.slice(0, eqIdx).trim();
    let value = line.slice(eqIdx + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    vars[key] = value;
  }
  return vars;
}

function findJobFolder(id: string): string | null {
  const productId = id.replace(/^JOB-/, '');
  if (!fs.existsSync(PRODUCTS_DIR)) return null;
  const entries = fs.readdirSync(PRODUCTS_DIR, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && entry.name.startsWith(productId)) {
      return path.join(PRODUCTS_DIR, entry.name);
    }
  }
  return null;
}

function buildProductInfo(prodData: any) {
  return {
    product_name: prodData.title || 'Sản phẩm chưa đặt tên',
    pricing: {
      price_vnd: prodData.price || 0,
      currency: prodData.currency || 'VND',
    },
    specs: {
      categories: prodData.categories || [],
    },
    source: {
      pdp_url: prodData.pdp_url || '',
      keyword: prodData.keyword || '',
    },
  };
}

export async function POST(req: NextRequest) {
  let id: string;
  try {
    const body = await req.json();
    id = body.id;
  } catch {
    return NextResponse.json({ error: 'Body JSON không hợp lệ' }, { status: 400 });
  }

  if (!id || typeof id !== 'string') {
    return NextResponse.json({ error: 'Thiếu id job' }, { status: 400 });
  }

  const jobFolder = findJobFolder(id);
  if (!jobFolder) {
    return NextResponse.json({ error: `Không tìm thấy job '${id}'` }, { status: 404 });
  }

  const videoPath = path.join(jobFolder, 'video_clean.mp4');
  if (!fs.existsSync(videoPath)) {
    return NextResponse.json(
      { error: 'Job chưa có video_clean.mp4 — hãy Nạp Job lại để tải video nguồn trước.' },
      { status: 400 }
    );
  }

  const productJsonPath = path.join(jobFolder, 'product.json');
  let prodData: any = {};
  if (fs.existsSync(productJsonPath)) {
    try {
      prodData = JSON.parse(fs.readFileSync(productJsonPath, 'utf-8'));
    } catch {}
  }

  const productInfoPath = path.join(jobFolder, '_remix_product_info.json');
  fs.writeFileSync(productInfoPath, JSON.stringify(buildProductInfo(prodData), null, 2), 'utf-8');

  const outputPath = path.join(jobFolder, 'generated_video.mp4');
  const scriptArgs = [
    '-m', 'gobi', 'remix',
    '--ref', videoPath,
    '--product-json', productInfoPath,
    '--character', 'gobi_lyly',
    '--out', outputPath,
  ];

  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      let isClosed = false;
      const safeEnqueue = (data: string) => {
        if (isClosed) return;
        try {
          controller.enqueue(encoder.encode(data));
        } catch {
          isClosed = true;
        }
      };

      const child = spawn(PYTHON_PATH, scriptArgs, {
        cwd: PROJECT_ROOT,
        env: {
          ...process.env,
          ...loadRootEnv(),
          PYTHONPATH: `${PROJECT_ROOT}:${PROJECT_ROOT}/src`,
        },
      });

      let detectedVideoType: string | null = null;
      let hyperframesProjectDir: string | null = null;

      const sendLog = (line: string) => {
        const typeMatch = line.match(/Phát hiện: video dạng '(\w+)'/);
        if (typeMatch) detectedVideoType = typeMatch[1];

        const projMatch = line.match(/HyperFrames Project\s*:\s*(.+)$/);
        if (projMatch) hyperframesProjectDir = projMatch[1].trim();

        safeEnqueue(`data: ${JSON.stringify({ type: 'LOG', line })}\n\n`);
      };

      child.stdout.on('data', (chunk) => {
        chunk.toString().split('\n').filter(Boolean).forEach(sendLog);
      });
      child.stderr.on('data', (chunk) => {
        chunk.toString().split('\n').filter(Boolean).forEach(sendLog);
      });

      child.on('close', (code) => {
        const success = code === 0 && fs.existsSync(outputPath);

        if (success) {
          try {
            prodData.status = 'DA_LAM_VIDEO';
            prodData.generated_video_at = new Date().toISOString();
            if (detectedVideoType) prodData.video_type = detectedVideoType;
            if (hyperframesProjectDir) prodData.hyperframes_project_dir = hyperframesProjectDir;
            fs.writeFileSync(productJsonPath, JSON.stringify(prodData, null, 2), 'utf-8');
          } catch (e) {
            console.error('[render] Failed to update product.json status:', e);
          }
        }

        safeEnqueue(`data: ${JSON.stringify({ type: 'DONE', success, exitCode: code })}\n\n`);
        isClosed = true;
        try {
          controller.close();
        } catch {}
      });

      req.signal.addEventListener('abort', () => {
        isClosed = true;
        if (!child.killed) child.kill('SIGTERM');
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  });
}
