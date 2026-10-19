import sys
import os
import json
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def log(msg):
    print(msg, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        r'C:\Users\HAI\.agent-browser\profiles\ai_profile',
        channel='chrome',
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check"
        ]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    # Catch all console logs & page errors
    page.on("console", lambda m: log(f"[BROWSER CONSOLE] {m.type}: {m.text}"))
    page.on("pageerror", lambda e: log(f"[BROWSER JS ERROR] {e}"))
    
    # Catch all network requests that contain passport or send_code or email
    page.on("request", lambda r: log(f">> REQ: {r.method} {r.url}") if any(k in r.url for k in ["send_code", "passport", "email", "check", "signup"]) else None)
    page.on("response", lambda r: log(f"<< RESP: {r.status} {r.url}") if any(k in r.url for k in ["send_code", "passport", "email", "check", "signup"]) else None)
    
    log("Navigating to TikTok signup email...")
    page.goto("https://www.tiktok.com/signup/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    # Select birthday
    log("Selecting birthday...")
    age_selectors = page.locator('div.tiktok-psovae-de495bb3--DivAgeSelector > div')
    age_selectors.nth(0).click()
    page.locator('div[id*="Month-options-item-"]:has-text("July")').first.click()
    age_selectors.nth(1).click()
    page.locator('div[id*="Day-options-item-"]:has-text("8")').first.click()
    age_selectors.nth(2).click()
    year_target = page.locator('div[id*="Year-options-item-"]:has-text("2000")').first
    year_target.scroll_into_view_if_needed()
    year_target.click()
    time.sleep(0.5)
    
    # Type email
    log("Typing email...")
    email_input = page.locator('input[name="email"]').first
    email_input.click()
    email_input.type("dinhthienthoai@gmail.com", delay=30)
    email_input.evaluate('el => el.dispatchEvent(new Event("change", { bubbles: true }))')
    time.sleep(0.5)
    
    # Type password
    log("Typing password...")
    pwd_input = page.locator('input[type="password"]').first
    pwd_input.click()
    pwd_input.type("ThoaiReview@2026!", delay=30)
    pwd_input.evaluate('el => el.dispatchEvent(new Event("change", { bubbles: true }))')
    time.sleep(1)
    
    send_btn = page.locator('button[data-e2e="send-code-button"]').first
    log(f"Send button disabled: {send_btn.evaluate('el => el.disabled')}")
    
    # Try clicking using page.evaluate to trigger real react click
    log("Triggering click via JavaScript...")
    res = page.evaluate('''() => {
        const btn = document.querySelector('button[data-e2e="send-code-button"]');
        if (!btn) return "Button not found";
        try {
            btn.click();
            return "Clicked directly";
        } catch(err) {
            return "Error: " + err.message;
        }
    }''')
    log(f"Evaluate click result: {res}")
    
    log("Waiting 6s...")
    page.wait_for_timeout(6000)
    
    # If still nothing, try Playwright click
    log("Now trying Playwright send_btn.click()...")
    send_btn.click()
    page.wait_for_timeout(6000)
    
    # Check button text and DOM status
    log(f"Button text: {repr(send_btn.inner_text().strip())}")
    
    # Check if any popup or modal is present
    modals = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('div[class*="modal"], div[class*="dialog"], div[role="dialog"]'))
            .map(m => m.innerText.substring(0, 100));
    }''')
    log(f"Modals detected: {modals}")
    
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\click_handler_test.png")
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png")
    
    browser.close()
