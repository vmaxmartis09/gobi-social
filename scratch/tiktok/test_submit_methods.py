import sys
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
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/login/email/forget-password")
    page.wait_for_timeout(3000)
    
    # Fill email
    email = page.locator('input[name="email"]').first
    email.click()
    email.press_sequentially("dinhthienthoai@gmail.com", delay=30)
    
    # Fill code
    code = page.locator('input[placeholder*="6-digit"]').first
    code.click()
    code.press_sequentially("301507", delay=30)
    
    # Fill password
    pwd = page.locator('input[type="password"]').first
    pwd.click()
    pwd.press_sequentially("ThoaiReview@2026!", delay=30)
    
    # Check error text
    error_span = page.locator('span[role="status"]').first
    log(f"Status/error text before submit: {repr(error_span.inner_text())}")
    
    # Check button disabled
    btn = page.locator('button[type="submit"]').first
    log(f"Button disabled attr: {btn.evaluate('el => el.disabled')}")
    log(f"Button class: {btn.evaluate('el => el.className')}")
    
    # Try pressing Enter in the password field
    log("Pressing Enter in password field...")
    pwd.press("Enter")
    page.wait_for_timeout(3000)
    
    log(f"Status/error text after Enter: {repr(error_span.inner_text())}")
    log(f"URL after Enter: {page.url}")
    
    page.screenshot(path=r"shots/after_enter_press.png")
    page.screenshot(path=r"shots/live.png")
    
    browser.close()
