import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shots")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    print("Checking Gmail access at https://mail.google.com ...")
    page.goto("https://mail.google.com", timeout=45000)
    page.wait_for_timeout(5000)
    print("Current URL:", page.url)
    print("Page Title:", page.title())
    page.screenshot(path=os.path.join(SHOTS_DIR, "gmail_check.png"))
    
    # Check if inbox is loaded
    if "inbox" in page.url or "mail" in page.url:
        print("[+] GMAIL DANG NHAP SAN THANH CONG!")
    browser.close()
