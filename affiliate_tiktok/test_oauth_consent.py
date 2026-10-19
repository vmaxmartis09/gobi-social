import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shots")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/signup")
    page.wait_for_timeout(3000)
    
    google_btn = page.locator('div:has-text("Continue with Google"), a:has-text("Continue with Google")').last
    
    with browser.expect_page() as popup_info:
        google_btn.click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded")
    print("Google Popup URL:", popup.url)
    popup.wait_for_timeout(2000)
    
    # Click account
    acc = popup.locator('div:has-text("dinhthienthoai@gmail.com")').first
    if acc.is_visible(timeout=3000):
        print("Clicking dinhthienthoai@gmail.com...")
        acc.click()
        
    popup.wait_for_timeout(3000)
    popup.screenshot(path=os.path.join(SHOTS_DIR, "popup_after_account_click.png"))
    print("Popup text after account click:")
    print(popup.inner_text("body")[:500])
    
    # Check if there is a Continue button
    btns = popup.query_selector_all('button, div[role="button"]')
    print(f"Buttons on popup: {len(btns)}")
    for b in btns:
        t = b.inner_text().strip()
        if t:
            print("  Btn:", t)
            
    browser.close()
