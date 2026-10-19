import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-first-run", "--no-default-browser-check"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    print("[1] Dang truy cap https://www.tiktok.com/login...")
    page.goto("https://www.tiktok.com/login", timeout=60000)
    page.wait_for_timeout(3000)
    page.screenshot(path=LIVE_IMG)
    
    # Tim nut Google tren trang Login
    print("[2] Tim nut 'Continue with Google' tren trang Dang nhap...")
    google_btn = page.locator('div:has-text("Continue with Google"), a:has-text("Continue with Google"), button:has-text("Continue with Google")').last
    
    popup = None
    try:
        with browser.expect_page(timeout=8000) as popup_info:
            google_btn.click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        print("[3] Cua so Google OAuth mo:", popup.url[:60])
        popup.wait_for_timeout(2000)
        # Chon dinhthienthoai@gmail.com
        acc = popup.locator('div:has-text("dinhthienthoai@gmail.com")').first
        if acc.is_visible(timeout=3000):
            acc.click()
            print("[+] Da click tai khoan dinhthienthoai@gmail.com tren Google OAuth!")
    except Exception as e:
        print("[i] Popup info:", e)
        
    page.wait_for_timeout(5000)
    page.screenshot(path=LIVE_IMG)
    page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_login_result.png"))
    
    print("\n=== KET QUA HIEN TAI TREN TIKTOK ===")
    print("URL:", page.url)
    print("Title:", page.title())
    
    # Lay tat ca text hien thi de biet TikTok dang hoi gi
    body_text = page.inner_text("body")
    lines = [l.strip() for l in body_text.split("\n") if l.strip()]
    for l in lines[:25]:
        print("  ->", l)
        
    browser.close()
