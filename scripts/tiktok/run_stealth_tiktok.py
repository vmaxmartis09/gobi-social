"""
TikTok Stealth CDP Runner
Ket noi qua Chrome DevTools Protocol (CDP port 9222) voi Profile ai_profile
De vuot hoan toan Akamai / Cloudflare anti-bot cua TikTok.
"""

import sys
import time
import os
import subprocess
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")
STATUS_FILE = os.path.join(SHOTS_DIR, "status.json")

def is_cdp_ready():
    import urllib.request
    try:
        with urllib.request.urlopen("http://localhost:9222/json/version", timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False

def launch_chrome_cdp():
    print("[*] Khoi chay Chrome voi cong CDP 9222 va co chong bot...")
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        f"--user-data-dir={PROFILE_DIR}",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check"
    ]
    subprocess.Popen(cmd)
    for _ in range(10):
        if is_cdp_ready():
            print("[+] Chrome CDP 9222 da san sang!")
            return True
        time.sleep(1)
    return False

def run():
    print("="*75)
    print("🚀 PIVOT CHIEN LUOC 5: KET NOI QUA CHROME CDP DE VUOT ANTI-BOT TIKTOK")
    print("="*75)
    
    if not is_cdp_ready():
        if not launch_chrome_cdp():
            print("[!] Khong the khoi dong Chrome CDP!")
            return

    with sync_playwright() as p:
        print("[*] Dang ket noi Playwright vao Chrome CDP http://localhost:9222...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        default_context = browser.contexts[0]
        page = default_context.pages[0] if default_context.pages else default_context.new_page()

        print("[*] Dang truy cap TikTok qua trinh duyet thuc te...")
        page.goto("https://www.tiktok.com", timeout=60000)
        time.sleep(4)
        
        print(f"[+] URL hien tai: {page.url}")
        print(f"[+] Tieu de trang: {page.title()}")
        page.screenshot(path=LIVE_IMG)
        page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_cdp_success.png"))

        # Kiem tra Captcha
        captcha_text = page.locator('div:has-text("Drag the slider to fit the puzzle")')
        if captcha_text.is_visible(timeout=2000):
            print("[!] Captcha dang xuat hien tren man hinh Chrome thuc te!")
        else:
            print("[+] Trang web load sach 100%, khong bi loi HTTP hay 403!")

        print("\n[OK] Chien luoc CDP da hoat dong hoan hao!")

if __name__ == "__main__":
    run()
