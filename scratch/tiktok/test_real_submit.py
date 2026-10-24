import sys
import re
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
    
    # Catch ALL requests to see what is sent
    page.on("request", lambda r: log(f">> REQ: {r.method} {r.url[:100]}") if any(k in r.url for k in ["passport", "reset", "change", "email"]) else None)
    page.on("response", lambda r: log(f"<< RESP: {r.status} {r.url[:100]}") if any(k in r.url for k in ["passport", "reset", "change", "email"]) else None)
    
    log("Navigating to forget-password...")
    page.goto("https://www.tiktok.com/login/email/forget-password")
    page.wait_for_timeout(3000)
    
    email_input = page.locator('input[name="email"], input[placeholder*="Email"]').first
    email_input.click()
    email_input.press_sequentially("dinhthienthoai@gmail.com", delay=30)
    time.sleep(1)
    
    # Click Send code
    log("Clicking Send code...")
    send_btn = page.locator('button:has-text("Send code")').first
    send_btn.click()
    page.wait_for_timeout(4000)
    
    # Check Gmail for the new code
    log("Opening Gmail to get the fresh code...")
    gmail_page = browser.new_page()
    gmail_page.goto("https://mail.google.com/mail/u/0/#inbox")
    gmail_page.wait_for_timeout(4000)
    
    otp = None
    for _ in range(15):
        row = gmail_page.locator('tr.zA:has-text("TikTok")').first
        if row.is_visible():
            row.click()
            gmail_page.wait_for_timeout(2000)
            body = gmail_page.inner_text("body")
            codes = re.findall(r'\b\d{6}\b', body)
            if codes:
                otp = codes[0] # or latest
                log(f"Found OTP in Gmail: {otp}")
                break
        time.sleep(3)
        gmail_page.reload()
        
    gmail_page.close()
    
    if not otp:
        log("No OTP found!")
        browser.close()
        sys.exit(1)
        
    log(f"Entering OTP {otp} and new password...")
    code_input = page.locator('input[placeholder*="6-digit"], input[placeholder*="mã"]').first
    code_input.click()
    code_input.press_sequentially(otp, delay=35)
    time.sleep(0.5)
    
    pwd_input = page.locator('input[type="password"]').first
    pwd_input.click()
    pwd_input.press_sequentially("ThoaiReview@2026!", delay=35)
    time.sleep(1)
    
    submit_btn = page.locator('button[type="submit"]').first
    log(f"Submitting form... is_enabled={submit_btn.is_enabled()}")
    submit_btn.click()
    
    log("Waiting 10s after submit...")
    page.wait_for_timeout(10000)
    
    log(f"Current URL after submit: {page.url}")
    page.screenshot(path=r"shots/real_submit_result.png")
    page.screenshot(path=r"shots/live.png")
    
    browser.close()
