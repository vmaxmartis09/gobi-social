import os
import sys
import time
import json
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")
STATUS_FILE = os.path.join(SHOTS_DIR, "status.json")

def log_progress(step_num, message, current_url="https://www.tiktok.com/signup", is_success=False):
    os.makedirs(SHOTS_DIR, exist_ok=True)
    payload = {
        "step": step_num,
        "status": message,
        "url": current_url,
        "success": is_success,
        "timestamp": time.time()
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[Step {step_num}] {message}")

def run():
    log_progress(1, "🚀 Khởi động không gian Ego Task Space trên Ego Lite...")
    clean_live_img = LIVE_IMG.replace("\\", "/")
    
    script_mjs = os.path.join(SHOTS_DIR, "tiktok_ego_flow.mjs")
    mjs_code = f"""
    const task = await taskSpace("TikTok Google OAuth Flow");
    const page = task.page("p1");
    
    console.log("[Ego] Đang điều hướng đến https://www.tiktok.com/signup...");
    await page.goto("https://www.tiktok.com/signup");
    await page.waitForLoadState();
    await page.screenshot({{ path: "{clean_live_img}" }});
    
    console.log("[Ego] Đang tìm nút Continue with Google...");
    try {{
      const popupPromise = page.waitForEvent("popup", {{ timeout: 15000 }});
      await page.click('div:has-text("Continue with Google"), button:has-text("Continue with Google"), a:has-text("Continue with Google")');
      const popup = await popupPromise;
      await popup.waitForLoadState();
      console.log("[Ego] Popup Google OAuth đã mở:", popup.url());
      await popup.screenshot({{ path: "{clean_live_img}" }});
      
      console.log("[Ego] Chọn tài khoản dinhthienthoai@gmail.com...");
      await popup.click('text="dinhthienthoai@gmail.com"');
      await popup.waitForTimeout(3000);
      await popup.screenshot({{ path: "{clean_live_img}" }});
    }} catch (err) {{
      console.log("[Ego] Lưu ý popup hoặc selector:", err.message);
    }}
    
    await page.waitForTimeout(4000);
    await page.screenshot({{ path: "{clean_live_img}" }});
    console.log("[Ego] Hoàn tất luồng xử lý!");
    await task.finish({{ keep: [] }});
    """
    
    with open(script_mjs, "w", encoding="utf-8") as f:
        f.write(mjs_code)
        
    log_progress(2, "⚡ Chạy Ego Lite automation flow qua ego-browser nodejs...")
    mjs_url = f"file:///{script_mjs.replace(os.sep, '/')}"
    cmd = f'cmd.exe /c "ego-browser nodejs -e ""await import(\'{mjs_url}\')"" < nul"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print(res.stderr)
        
    log_progress(5, "🎉 Quá trình đăng nhập/xử lý TikTok trên Ego Lite hoàn tất!", is_success=True)
    
    if os.path.exists(script_mjs):
        try:
            os.remove(script_mjs)
        except Exception:
            pass

if __name__ == "__main__":
    run()
