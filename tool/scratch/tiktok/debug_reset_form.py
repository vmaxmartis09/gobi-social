import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def log(msg):
    print(msg, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"),
        channel='chrome',
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check"
        ]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/login/email/forget-password")
    page.wait_for_timeout(3000)
    
    email_input = page.locator('input[name="email"], input[placeholder*="Email"]').first
    email_input.click()
    email_input.press_sequentially("dinhthienthoai@gmail.com", delay=30)
    
    code_input = page.locator('input[placeholder*="6-digit"], input[placeholder*="mã"]').first
    code_input.click()
    code_input.press_sequentially("123456", delay=30)
    
    pwd_input = page.locator('input[type="password"]').first
    pwd_input.click()
    pwd_input.press_sequentially("ThoaiReview@2026!", delay=30)
    
    page.wait_for_timeout(1000)
    
    submit_btn = page.locator('button[type="submit"]').first
    log(f"Submit btn HTML: {submit_btn.evaluate('el => el.outerHTML')}")
    log(f"Submit btn disabled: {submit_btn.evaluate('el => el.disabled')}")
    log(f"Submit btn is_enabled(): {submit_btn.is_enabled()}")
    
    page.screenshot(path=r"shots/debug_reset_form.png")
    page.screenshot(path=r"shots/live.png")
    
    browser.close()
