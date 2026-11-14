import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const PYTHON_PATH = path.join(PROJECT_ROOT, '.venv/bin/python');
const SCRIPT_PATH = path.join(PROJECT_ROOT, 'src/gobi/services/product/job_creator.py');

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();

    if (!url || typeof url !== 'string' || !url.trim()) {
      return NextResponse.json({ error: 'URL video TikTok không được để trống' }, { status: 400 });
    }

    const cleanUrl = url.trim();

    return new Promise<NextResponse>((resolve) => {
      const child = spawn(PYTHON_PATH, [SCRIPT_PATH, cleanUrl], {
        cwd: PROJECT_ROOT,
        env: {
          ...process.env,
          PYTHONPATH: `${PROJECT_ROOT}:${PROJECT_ROOT}/src`,
        },
      });

      let stdoutData = '';
      let stderrData = '';

      child.stdout.on('data', (chunk) => {
        stdoutData += chunk.toString();
      });

      child.stderr.on('data', (chunk) => {
        stderrData += chunk.toString();
      });

      child.on('close', (code) => {
        if (code !== 0 && !stdoutData.trim()) {
          console.error('[API Create Job] Error:', stderrData);
          return resolve(
            NextResponse.json(
              { error: stderrData || 'Lỗi xử lý khi nạp Job từ link' },
              { status: 500 }
            )
          );
        }

        try {
          // Parse JSON output from python script
          const parsed = JSON.parse(stdoutData.trim());
          if (!parsed.success) {
            return resolve(NextResponse.json({ error: parsed.error || 'Thất bại' }, { status: 400 }));
          }
          return resolve(NextResponse.json(parsed));
        } catch (e: any) {
          console.error('[API Create Job] JSON Parse Error:', stdoutData);
          return resolve(NextResponse.json({ error: 'Không thể phân tích dữ liệu trả về từ engine' }, { status: 500 }));
        }
      });
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
