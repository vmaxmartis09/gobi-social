import { NextRequest, NextResponse } from 'next/server';
import { execFile } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const HF_PROJECTS_DIR = path.join(PROJECT_ROOT, 'output/hyperframes_projects');

const execFileAsync = promisify(execFile);

// Chỉ cho phép project id dạng job_id của content_remix_workflow (remix_<ts>_<hash>)
// hoặc tên thư mục an toàn tương tự — chặn path traversal ("../").
function resolveProjectDir(projectId: string): string | null {
  if (!/^[a-zA-Z0-9_-]+$/.test(projectId)) return null;
  return path.join(HF_PROJECTS_DIR, projectId);
}

function parseJsonLine(stdout: string): any {
  const lastLine = stdout.trim().split('\n').pop() || '{}';
  return JSON.parse(lastLine);
}

// Khởi động (hoặc tái sử dụng nếu đã chạy) HyperFrames Studio preview nền cho 1 project,
// để dashboard nhúng iframe xem trực tiếp quá trình dựng/edit video.
export async function POST(req: NextRequest) {
  let projectId: string;
  try {
    const body = await req.json();
    projectId = body.projectId;
  } catch {
    return NextResponse.json({ error: 'Body JSON không hợp lệ' }, { status: 400 });
  }

  if (!projectId || typeof projectId !== 'string') {
    return NextResponse.json({ error: 'Thiếu projectId' }, { status: 400 });
  }

  const dir = resolveProjectDir(projectId);
  if (!dir) {
    return NextResponse.json({ error: 'projectId không hợp lệ' }, { status: 400 });
  }

  const indexFile = path.join(dir, 'index.html');
  if (!fs.existsSync(indexFile)) {
    // Project HyperFrames chưa được tạo xong (workflow đang ở bước trước đó) — client nên poll lại.
    return NextResponse.json({ ready: false });
  }

  try {
    const { stdout } = await execFileAsync(
      'npx',
      ['hyperframes', 'preview', dir, '--no-open', '--background', '--json'],
      { cwd: PROJECT_ROOT, timeout: 25000 }
    );
    const parsed = parseJsonLine(stdout);
    if (!parsed.ok) {
      return NextResponse.json({ ready: false, error: 'Không khởi động được HyperFrames Studio preview' });
    }
    return NextResponse.json({
      ready: true,
      studioUrl: parsed.result.studioUrl,
      serverUrl: parsed.result.serverUrl,
      port: parsed.result.port,
    });
  } catch (err: any) {
    return NextResponse.json(
      { ready: false, error: err.message || 'Lỗi khởi động HyperFrames Studio preview' },
      { status: 500 }
    );
  }
}

// Dừng preview nền của 1 project (gọi khi đóng modal hoặc bắt đầu render job khác).
export async function DELETE(req: NextRequest) {
  const projectId = req.nextUrl.searchParams.get('projectId');
  if (!projectId) {
    return NextResponse.json({ error: 'Thiếu projectId' }, { status: 400 });
  }

  const dir = resolveProjectDir(projectId);
  if (!dir) {
    return NextResponse.json({ error: 'projectId không hợp lệ' }, { status: 400 });
  }

  try {
    await execFileAsync('npx', ['hyperframes', 'preview', dir, '--stop', '--json'], {
      cwd: PROJECT_ROOT,
      timeout: 10000,
    });
  } catch {
    // Có thể preview đã dừng từ trước — bỏ qua.
  }
  return NextResponse.json({ stopped: true });
}
