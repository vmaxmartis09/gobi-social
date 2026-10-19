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
    log("Navigating to TikTok login email...")
    page.goto("https://www.tiktok.com/login/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    # Click Forgot password
    log("Clicking 'Forgot password?'...")
    forgot_link = page.locator('a:has-text("Forgot password"), span:has-text("Forgot password")').first
    forgot_link.click()
    page.wait_for_timeout(3000)
    
    log(f"Current URL: {page.url}")
    
    # Check elements on forgot password page
    options = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('input, button, a')).map(el => ({
            tag: el.tagName,
            type: el.type,
            name: el.name,
            placeholder: el.placeholder,
            text: el.innerText
        }));
    }''')
    log(f"Form elements: {json.dumps(options, indent=2)}")
    
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\forgot_password_page.png")
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png")
    
    browser.close()
