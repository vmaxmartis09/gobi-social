import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/signup/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    # Click Month
    month_div = page.locator('div:has-text("Month")').last
    print("Clicking Month...")
    month_div.click()
    page.wait_for_timeout(1000)
    
    # List options
    opts = page.query_selector_all('li, div[role="option"], div[class*="option"]')
    print(f"Options found: {len(opts)}")
    for o in opts[:15]:
        print("  Option:", repr(o.inner_text().strip()))
        
    browser.close()
