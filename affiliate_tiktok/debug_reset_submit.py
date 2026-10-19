import sys
import json
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
    
    # Catch all responses
    def on_resp(resp):
        if any(k in resp.url for k in ["passport", "reset", "change", "login", "password"]):
            try:
                body = resp.text()[:400]
            except Exception:
                body = "(binary or empty)"
            log(f"<< RESP {resp.status} {resp.url[:80]}\n   BODY: {body}")
            
    page.on("response", on_resp)
    
    log("Navigating to forget-password...")
    page.goto("https://www.tiktok.com/login/email/forget-password")
    page.wait_for_timeout(3000)
    
    email_input = page.locator('input[name="email"], input[placeholder*="Email"]').first
    email_input.click()
    email_input.press_sequentially("dinhthienthoai@gmail.com", delay=30)
    
    code_input = page.locator('input[placeholder*="6-digit"], input[placeholder*="mã"]').first
    code_input.click()
    code_input.press_sequentially("301507", delay=30)
    
    pwd_input = page.locator('input[type="password"]').first
    pwd_input.click()
    pwd_input.press_sequentially("ThoaiReview@2026!", delay=30)
    time.sleep(1)
    
    submit_btn = page.locator('button[type="submit"]').first
    log(f"Submitting form... is_enabled={submit_btn.is_enabled()}")
    submit_btn.click()
    
    log("Waiting 6s...")
    page.wait_for_timeout(6000)
    
    # Check page error or toast
    toasts = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('div[role="status"], div[class*="toast"], div[class*="error"], span[class*="error"]'))
            .map(e => e.innerText.trim()).filter(Boolean);
    }''')
    log(f"Toasts/Errors on page: {toasts}")
    log(f"Current URL: {page.url}")
    
    page.screenshot(path=r"shots/debug_reset_result.png")
    page.screenshot(path=r"shots/live.png")
    
    browser.close()
