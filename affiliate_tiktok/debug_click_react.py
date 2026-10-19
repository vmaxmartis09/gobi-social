import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    page.goto("https://www.tiktok.com/signup/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    # Track ALL POST requests and console
    page.on("request", lambda r: print(">> REQ:", r.method, r.url) if "send_code" in r.url or "passport" in r.url or r.method == "POST" else None)
    page.on("response", lambda r: print("<< RESP:", r.status, r.url) if "send_code" in r.url or "passport" in r.url or r.request.method == "POST" else None)
    page.on("console", lambda msg: print("CONSOLE:", msg.text) if "error" in msg.text.lower() or "passport" in msg.text.lower() else None)
    
    # Birthday
    age_selectors = page.locator('div.tiktok-psovae-de495bb3--DivAgeSelector > div')
    age_selectors.nth(0).click()
    page.locator('div[id*="Month-options-item-"]:has-text("July")').first.click()
    age_selectors.nth(1).click()
    page.locator('div[id*="Day-options-item-"]:has-text("8")').first.click()
    age_selectors.nth(2).click()
    page.locator('div[id*="Year-options-item-"]:has-text("2000")').first.scroll_into_view_if_needed()
    page.locator('div[id*="Year-options-item-"]:has-text("2000")').first.click()
    
    # Type email naturally
    email_input = page.locator('input[name="email"]').first
    email_input.click()
    email_input.press_sequentially('dinhthienthoai@gmail.com', delay=50)
    
    # Type password naturally
    pwd_input = page.locator('input[type="password"]').first
    pwd_input.click()
    pwd_input.press_sequentially('ThoaiReview@2026!', delay=50)
    
    page.wait_for_timeout(1000)
    
    # Mouse click on Send code button
    send_btn = page.locator('button[data-e2e="send-code-button"]').first
    box = send_btn.bounding_box()
    print("Mouse clicking at:", box)
    page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    time.sleep(0.2)
    page.mouse.down()
    time.sleep(0.1)
    page.mouse.up()
    
    print("Waiting 5s after click...")
    page.wait_for_timeout(5000)
    
    page.screenshot(path=r"shots/after_mouse_click.png")
    page.screenshot(path=r"shots/live.png")
    
    # Check if captcha appeared or button changed
    print("Button text now:", repr(send_btn.inner_text().strip()))
    captcha = page.locator('div[class*="captcha"], div:has-text("puzzle"), div:has-text("slider")').count()
    print("Captcha elements detected:", captcha)
    
    browser.close()
