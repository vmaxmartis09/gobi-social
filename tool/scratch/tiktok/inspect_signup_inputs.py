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
    page.goto("https://www.tiktok.com/signup")
    page.wait_for_timeout(3000)
    
    google_btn = page.locator('div:has-text("Continue with Google"), a:has-text("Continue with Google")').last
    with browser.expect_page() as popup_info:
        google_btn.click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded")
    acc = popup.locator('div:has-text("dinhthienthoai@gmail.com")').last
    acc.click()
    
    for _ in range(8):
        time.sleep(1)
        if popup.is_closed():
            break
            
    page.wait_for_timeout(4000)
    
    # Inspect inputs
    inputs = page.query_selector_all('input, select, div[class*="select"]')
    print(f"Total inputs on signup: {len(inputs)}")
    for i in inputs:
        name = i.get_attribute("name")
        placeholder = i.get_attribute("placeholder")
        tag = i.evaluate("e => e.tagName")
        text = i.inner_text().strip()
        print(f"TAG: {tag} | NAME: {name} | PLACEHOLDER: {placeholder} | TEXT: {text[:40]}")
        
    browser.close()
