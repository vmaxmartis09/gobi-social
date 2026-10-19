"""
Vmax Live Agent Monitor - Powered by Ego Lite
Chạy tác vụ trình duyệt thông qua Ego Lite Browser,
đồng thời xuất luồng hình ảnh trực tiếp (Live Viewport) lên Dashboard để quan sát.
"""

import os
import sys
import time
import json
import subprocess
import webbrowser

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")
STATUS_FILE = os.path.join(SHOTS_DIR, "status.json")
VIEWER_HTML = os.path.join(PROJECT_ROOT, "live_viewer.html")

def update_status(msg: str):
    os.makedirs(SHOTS_DIR, exist_ok=True)
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump({"status": msg, "timestamp": time.time()}, f, ensure_ascii=False)
    print(f"[*] {msg}")

def execute_task(task_url: str):
    print("\n" + "="*70)
    print("      VMAX AI AGENT - EGO LITE BROWSER AUTOMATION")
    print("="*70)
    
    if os.path.exists(VIEWER_HTML):
        print("[+] Đang mở Live Viewer dashboard...")
        webbrowser.open(f"file:///{VIEWER_HTML}")
        time.sleep(1)

    update_status(f"Ego Lite: Đang truy cập {task_url}...")
    
    temp_mjs = os.path.join(SHOTS_DIR, "temp_ego_monitor.mjs")
    clean_live_img = LIVE_IMG.replace("\\", "/")
    
    script_content = f"""
    const task = await taskSpace("Vmax Live Monitor");
    const page = task.page("p1");
    await page.goto("{task_url}");
    await page.waitForLoadState();
    await page.screenshot({{ path: "{clean_live_img}" }});
    const snapshot = await page.snapshot();
    console.log(JSON.stringify(snapshot));
    await task.finish({{ keep: [] }});
    """
    with open(temp_mjs, "w", encoding="utf-8") as f:
        f.write(script_content)

    update_status("Ego Lite: Đang quét nội dung và phân tích giao diện...")
    
    mjs_url = f"file:///{temp_mjs.replace(os.sep, '/')}"
    cmd = f'cmd.exe /c "ego-browser nodejs -e ""await import(\'{mjs_url}\')"" < nul"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    
    update_status(f"Hoàn thành xử lý trang: {task_url}!")
    if res.stdout:
        print("[+] Kết quả từ Ego Lite:")
        print(res.stdout[:500] + "..." if len(res.stdout) > 500 else res.stdout)
    
    if os.path.exists(temp_mjs):
        try:
            os.remove(temp_mjs)
        except Exception:
            pass

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://news.ycombinator.com"
    execute_task(url)
