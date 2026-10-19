import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SHOTS_DIR = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots"
os.makedirs(SHOTS_DIR, exist_ok=True)

PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print("[*] Launching browser with user profile...")
with sync_playwright() as p:
    try:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            executable_path=CHROME_BIN,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            viewport={"width": 1280, "height": 850}
        )
        page = context.pages[0] if context.pages else context.new_page()
        
        target_url = "https://www.facebook.com/tuongvi.kocai"
        print(f"[*] Navigating to {target_url}...")
        page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
        
        time.sleep(5)
        
        screenshot_path = os.path.join(SHOTS_DIR, "fb_tuongvi_1.png")
        page.screenshot(path=screenshot_path)
        print(f"[+] Screenshot saved to {screenshot_path}")
        print(f"[+] Current page title: {page.title()}")
        print(f"[+] Current page URL: {page.url}")
        
        # Check if login overlay or dialog exists and try pressing Escape
        page.keyboard.press("Escape")
        time.sleep(1)
        
        # Check text length
        body_text = page.inner_text("body")
        print(f"[+] Page text length: {len(body_text)} chars")
        print("[+] First 300 chars of body:\n", body_text[:300])
        
        context.close()
        print("[OK] Test finished successfully.")
    except Exception as e:
        print(f"[!] Error: {e}")
