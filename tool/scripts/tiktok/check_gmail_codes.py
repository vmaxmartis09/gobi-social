import sys
import re
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"),
        channel='chrome',
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://mail.google.com/mail/u/0/#search/from%3Atiktok", timeout=45000)
    page.wait_for_timeout(4000)
    
    rows = page.locator('tr.zA')
    print(f"Total TikTok rows found: {rows.count()}")
    for i in range(min(rows.count(), 5)):
        row = rows.nth(i)
        print(f"Row {i}: {repr(row.inner_text())}")
        
    # Open the very first row
    if rows.count() > 0:
        rows.first.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=r"shots/gmail_detail_test.png")
        body = page.inner_text("body")
        codes = re.findall(r'\b\d{6}\b', body)
        print("All 6-digit codes in email body:", codes)
        
    browser.close()
