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
        r'C:\Users\HAI\.agent-browser\profiles\ai_profile',
        channel='chrome',
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized"
        ],
        no_viewport=True
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    log("Navigating to https://www.tiktok.com/ ...")
    page.goto("https://www.tiktok.com/", timeout=45000)
    page.wait_for_timeout(4000)
    
    # Query account info directly from browser context
    account_info = page.evaluate('''async () => {
        try {
            const resp = await fetch("/passport/web/account/info/?aid=1459&app_language=en");
            const data = await resp.json();
            return data;
        } catch(e) {
            return { error: e.message };
        }
    }''')
    log(f"Account Info from Passport API:\n{json.dumps(account_info, indent=2, ensure_ascii=False)}")
    
    # Also check user settings
    user_settings = page.evaluate('''async () => {
        try {
            const resp = await fetch("/api/user/settings/?aid=1988&app_language=en");
            const data = await resp.json();
            return data;
        } catch(e) {
            return { error: e.message };
        }
    }''')
    log(f"User Settings API:\n{json.dumps(user_settings, indent=2, ensure_ascii=False)}")
    
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\tiktok_current_state.png")
    page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png")
    
    # If logged in, navigate to profile
    user_id = account_info.get("data", {}).get("user_id") or account_info.get("data", {}).get("user_id_str")
    username = account_info.get("data", {}).get("username") or account_info.get("data", {}).get("screen_name")
    
    if username:
        profile_url = f"https://www.tiktok.com/@{username}"
        log(f"Navigating to user profile: {profile_url}")
        page.goto(profile_url, timeout=30000)
        page.wait_for_timeout(4000)
        page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\my_exact_tiktok_profile.png")
        page.screenshot(path=r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png")
        log(f"Profile Title: {page.title()}")
        
    time.sleep(10)
    browser.close()
