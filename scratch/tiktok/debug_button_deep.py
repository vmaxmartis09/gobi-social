import sys
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def log(msg):
    print(msg, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"),
        channel='chrome',
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    log("Navigating to TikTok signup email...")
    page.goto("https://www.tiktok.com/signup/phone-or-email/email", wait_until="networkidle")
    
    # Check initial send code button
    send_btn = page.locator('button[data-e2e="send-code-button"]').first
    log(f"Initial send button outerHTML:\n{send_btn.evaluate('el => el.outerHTML')}")
    log(f"Initial disabled property: {send_btn.evaluate('el => el.disabled')}")
    log(f"Initial class: {send_btn.evaluate('el => el.className')}")
    
    # Fill Birthday
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
    
    # Type email
    log("Typing email...")
    email_input = page.locator('input[name="email"]').first
    email_input.click()
    email_input.type("dinhthienthoai@gmail.com", delay=30)
    email_input.evaluate('el => el.dispatchEvent(new Event("change", { bubbles: true }))')
    
    log(f"After email - disabled property: {send_btn.evaluate('el => el.disabled')}")
    log(f"After email - class: {send_btn.evaluate('el => el.className')}")
    
    # Type password
    log("Typing password...")
    pwd_input = page.locator('input[type="password"]').first
    pwd_input.click()
    pwd_input.type("ThoaiReview@2026!", delay=30)
    pwd_input.evaluate('el => el.dispatchEvent(new Event("change", { bubbles: true }))')
    
    log(f"After password - disabled property: {send_btn.evaluate('el => el.disabled')}")
    log(f"After password - class: {send_btn.evaluate('el => el.className')}")
    
    # Check React fiber / props on button
    react_props = send_btn.evaluate('''el => {
        const key = Object.keys(el).find(k => k.startsWith("__reactFiber") || k.startsWith("__reactProps"));
        if (!key) return "No react key found";
        const props = el[key];
        return {
            hasOnClick: !!(props?.memoizedProps?.onClick || props?.onClick),
            disabled: props?.memoizedProps?.disabled ?? props?.disabled
        };
    }''')
    log(f"React props on send_btn: {json.dumps(react_props)}")
    
    browser.close()
