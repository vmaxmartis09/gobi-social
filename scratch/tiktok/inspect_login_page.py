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
    page.on("console", lambda m: log(f"[CONSOLE] {m.text}") if "passport" in m.text.lower() or "error" in m.text.lower() or "login" in m.text.lower() else None)
    
    log("Navigating to TikTok login page: https://www.tiktok.com/login/phone-or-email/email")
    page.goto("https://www.tiktok.com/login/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    # Check elements on login page
    log(f"Page title: {page.title()}")
    log(f"Page URL: {page.url}")
    
    # Look for options: Log in with code?
    login_options = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a, button, span')).map(el => el.innerText.trim()).filter(t => t.length > 0 && t.length < 50);
    }''')
    log(f"Login options visible: {login_options[:30]}")
    
    page.screenshot(path=r"shots/tiktok_login_form.png")
    page.screenshot(path=r"shots/live.png")
    
    browser.close()
