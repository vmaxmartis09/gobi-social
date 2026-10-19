"""
Launch Headed Chrome Browser directly on the user's screen with the logged-in TikTok profile.
No .bat file needed - 100% managed by Antigravity AI Agent.
"""

import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
TARGET_URL = "https://www.tiktok.com/@tis.decor"

def run():
    print("="*75)
    print("🌐 ĐANG MỞ TRÌNH DUYỆT CHROME TRỰC TIẾP TRÊN MÀN HÌNH BẠN...")
    print(f"[*] Tài khoản: Tis Decor (@tis.decor)")
    print(f"[*] URL:       {TARGET_URL}")
    print("="*75, flush=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
                "--start-maximized"
            ],
            no_viewport=True
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(TARGET_URL, timeout=45000)
        print(f"[+] Trình duyệt đã mở thành công trên màn hình của bạn!", flush=True)
        print("[+] Bạn có thể tương tác trực tiếp hoặc quan sát kênh TikTok.", flush=True)
        print("[*] Phiên làm việc đang được giữ mở...", flush=True)

        # Giữ cửa sổ mở liên tục chừng nào user chưa đóng toàn bộ tab
        try:
            while len(context.pages) > 0:
                time.sleep(1)
        except Exception:
            pass
        print("[*] Trình duyệt đã được đóng.")

if __name__ == "__main__":
    run()
