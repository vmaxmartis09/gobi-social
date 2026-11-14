import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-first-run", "--no-default-browser-check"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    print("[1] Dang truy cap trang dang ky TikTok (Phone or Email)...")
    page.goto("https://www.tiktok.com/signup/phone-or-email/email", timeout=45000)
    page.wait_for_timeout(3000)
    page.screenshot(path=LIVE_IMG)
    page.screenshot(path=os.path.join(SHOTS_DIR, "email_signup_page.png"))
    
    print("URL hien tai:", page.url)
    print("Tieu de:", page.title())
    
    # Kiem tra cac truong tren form
    inputs = page.query_selector_all('input, div[class*="select"], div[aria-haspopup="listbox"]')
    print(f"Tim thay {len(inputs)} input / selector:")
    for i in inputs:
        tag = i.evaluate("e => e.tagName")
        ph = i.get_attribute("placeholder")
        name = i.get_attribute("name")
        txt = i.inner_text().strip()
        print(f"  TAG: {tag} | NAME: {name} | PH: {ph} | TEXT: {repr(txt[:30])}")
        
    browser.close()
