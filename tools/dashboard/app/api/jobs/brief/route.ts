import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const PRODUCTS_DIR = path.join(PROJECT_ROOT, 'data/products');
const PYTHON_PATH = path.join(PROJECT_ROOT, '.venv/bin/python');

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

/** stdout có thể lẫn vài dòng log (vd Whisper model loading) trước dòng JSON cuối — quét ngược tìm dòng JSON hợp lệ. */
function parseJsonFromOutput(output: string): any {
  const lines = output.split('\n').map((l) => l.trim()).filter(Boolean);
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].startsWith('{') && lines[i].endsWith('}')) {
      try {
        return JSON.parse(lines[i]);
      } catch {
        continue;
      }
    }
  }
  return null;
}

function formatBrief(data: any, jobFolder: string): string {
  const p = data.product_info;
  const typeLabel = data.video_type === 'talking_head' ? 'Nói trực diện' : 'Chỉ sản phẩm (lookbook)';

  const beatsText = (data.beats || [])
    .map((b: any, i: number) => `${i + 1}. [${b.beat_name}]\n   Lời thoại: "${b.voiceover_line}"`)
    .join('\n\n');

  return `=== GOBI BRIEF — ${p.product_name} ===

[LOẠI VIDEO ĐÃ DETECT]: ${typeLabel}

[SẢN PHẨM THẬT]
- Tên: ${p.product_name}
- Giá: ${p.pricing?.price_vnd || 0} ${p.pricing?.currency || 'VND'}
- Danh mục: ${(p.specs?.categories || []).join(' > ')}
- Link PDP thật (vào đây lấy ảnh sản phẩm thật): ${p.source?.pdp_url || '(không có)'}

[NHÂN VẬT]
- Preset: ${data.character} (dùng nhân vật Flow đã tạo sẵn: "Gô Bi KOC")
- Giọng đọc (Voice Vault): ${data.voice_profile_id}
- Ảnh chân dung tham chiếu: ${data.character_avatar_path}

[KỊCH BẢN TỪNG CẢNH]
0. [HOOK]
   Lời thoại: "${data.hook}"

${beatsText}

${(data.beats?.length || 0) + 1}. [CTA]
   Lời thoại: "${data.cta}"

[GHI CHÚ]
- Gô Bi phải mặc/cầm ĐÚNG sản phẩm thật lấy từ link PDP ở trên, không bịa trang phục.
- Mỗi cảnh = 1 clip Flow (~8s), ráp lại bằng HyperFrames theo vibe tự nhiên/lookbook.
- Lưu kết quả vào: ${jobFolder}/generated_video.mp4
- Cập nhật ${jobFolder}/product.json: status=DA_LAM_VIDEO, video_type=${data.video_type}
`;
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

  return new Promise<NextResponse>((resolve) => {
    const child = spawn(
      PYTHON_PATH,
      ['-m', 'gobi', 'brief', '--ref', videoPath, '--product-json', productInfoPath, '--character', 'gobi_lyly'],
      {
        cwd: PROJECT_ROOT,
        env: {
          ...process.env,
          ...loadRootEnv(),
          PYTHONPATH: `${PROJECT_ROOT}:${PROJECT_ROOT}/src`,
        },
      }
    );

    let output = '';
    child.stdout.on('data', (chunk) => (output += chunk.toString()));
    child.stderr.on('data', (chunk) => (output += chunk.toString()));

    child.on('close', (code) => {
      const parsed = parseJsonFromOutput(output);
      if (!parsed || !parsed.success) {
        resolve(
          NextResponse.json(
            { error: parsed?.error || `gobi brief thất bại (exit code ${code}):\n${output.slice(-2000)}` },
            { status: 500 }
          )
        );
        return;
      }
      const brief = formatBrief(parsed, jobFolder);
      resolve(NextResponse.json({ success: true, brief }));
    });
  });
}
