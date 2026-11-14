import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    # Listen to console and network
    console_logs = []
    page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
    
    network_errors = []
    page.on("response", lambda resp: network_errors.append(f"{resp.status} {resp.url}") if resp.status >= 400 else None)
    
    page.goto("https://www.tiktok.com/signup")
    page.wait_for_timeout(2000)
    
    google_btn = page.get_by_text("Continue with Google")
    with browser.expect_page() as p_info:
        google_btn.click()
    popup = p_info.value
    popup.wait_for_load_state("domcontentloaded")
    popup.wait_for_timeout(2000)
    
    # Click account
    popup.get_by_text("Thiên Thoại Đinh").click()
    
    # Wait for popup to close and network to settle
    for _ in range(10):
        time.sleep(1)
        if popup.is_closed():
            break
            
    page.wait_for_timeout(4000)
    
    print("\n--- NETWORK RESPONSES >= 400 ---")
    for ne in network_errors[-10:]:
        print("  ", ne)
        
    print("\n--- CONSOLE ERRORS / WARNINGS ---")
    for cl in [c for c in console_logs if "error" in c.lower() or "warn" in c.lower()][-10:]:
        print("  ", cl)
        
    browser.close()
