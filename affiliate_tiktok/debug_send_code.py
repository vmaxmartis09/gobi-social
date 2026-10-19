import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        r'C:\Users\HAI\.agent-browser\profiles\ai_profile',
        channel='chrome',
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/signup/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    # Listen to network
    page.on("request", lambda req: print(">> REQ:", req.method, req.url) if "send_code" in req.url or "passport" in req.url or "code" in req.url else None)
    page.on("response", lambda resp: print("<< RESP:", resp.status, resp.url) if "send_code" in resp.url or "passport" in resp.url or "code" in resp.url else None)
    
    # Birthday
    age_selectors = page.locator('div.tiktok-psovae-de495bb3--DivAgeSelector > div')
    age_selectors.nth(0).click()
    page.locator('div[id*="Month-options-item-"]:has-text("July")').first.click()
    age_selectors.nth(1).click()
    page.locator('div[id*="Day-options-item-"]:has-text("8")').first.click()
    age_selectors.nth(2).click()
    year_target = page.locator('div[id*="Year-options-item-"]:has-text("2000")').first
    year_target.scroll_into_view_if_needed()
    year_target.click()
    
    # Fill email and pass
    page.fill('input[name="email"]', 'dinhthienthoai@gmail.com')
    page.fill('input[type="password"]', 'ThoaiReview@2026!')
    page.wait_for_timeout(1000)
    
    send_btn = page.locator('button[data-e2e="send-code-button"]').first
    print("Send code button box:", send_btn.bounding_box())
    print("Is enabled:", send_btn.is_enabled())
    
    # Click Send code
    print("Clicking Send code...")
    send_btn.click()
    page.wait_for_timeout(4000)
    
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\debug_send_code.png")
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png")
    
    # Print button text now
    print("Button text now:", repr(send_btn.inner_text().strip()))
    
    # Check if any toast or error message appeared
    errors = page.eval_on_selector_all('div[class*="error"], span[class*="error"], div[role="status"]', 'els => els.map(e => e.innerText)')
    print("Error / status messages:", errors)
    
    browser.close()
