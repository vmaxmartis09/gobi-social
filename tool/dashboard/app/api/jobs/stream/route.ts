import { NextRequest } from 'next/server';
import fs from 'fs';
import path from 'path';
import { getAllJobs } from '@/lib/getJobs';

export const dynamic = 'force-dynamic';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const PRODUCTS_DIR = path.join(PROJECT_ROOT, 'data/products');

export async function GET(req: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      let isClosed = false;

      const safeEnqueue = (data: string) => {
        if (isClosed) return;
        try {
          controller.enqueue(encoder.encode(data));
        } catch (e) {
          isClosed = true;
        }
      };

      // 1. Send initial jobs payload
      try {
        const initialJobs = getAllJobs();
        safeEnqueue(`data: ${JSON.stringify({ type: 'INITIAL', jobs: initialJobs })}\n\n`);
      } catch (err) {
        console.error('[SSE] Failed to send initial jobs:', err);
      }

      // 2. Setup debounced file watcher on data/products
      let debounceTimer: NodeJS.Timeout | null = null;
      let watcher: fs.FSWatcher | null = null;

      const broadcastUpdate = () => {
        try {
          const currentJobs = getAllJobs();
          safeEnqueue(
            `data: ${JSON.stringify({
              type: 'UPDATE',
              jobs: currentJobs,
              timestamp: new Date().toISOString(),
            })}\n\n`
          );
        } catch (err) {
          console.error('[SSE] Broadcast update error:', err);
        }
      };

      if (fs.existsSync(PRODUCTS_DIR)) {
        try {
          watcher = fs.watch(PRODUCTS_DIR, { recursive: true }, () => {
            if (debounceTimer) clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
              broadcastUpdate();
            }, 350);
          });
        } catch (err) {
          console.error('[SSE] FS Watcher error:', err);
        }
      }

      // 3. Heartbeat ping every 12 seconds
      const heartbeatTimer = setInterval(() => {
        safeEnqueue(`: ping\n\n`);
      }, 12000);

      // 4. Handle connection close
      req.signal.addEventListener('abort', () => {
        isClosed = true;
        if (debounceTimer) clearTimeout(debounceTimer);
        clearInterval(heartbeatTimer);
        if (watcher) watcher.close();
        try {
          controller.close();
        } catch (e) {}
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
