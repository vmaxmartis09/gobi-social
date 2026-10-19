import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        r'C:\Users\HAI\.agent-browser\profiles\ai_profile',
        channel='chrome',
        headless=True
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto('https://www.tiktok.com', timeout=45000)
    page.wait_for_timeout(3000)
    
    # Kiem tra avatar hoac nut Profile
    user_links = page.query_selector_all('a[href*="/@"]')
    print(f"Tim thay {len(user_links)} link user:")
    for l in user_links[:5]:
        href = l.get_attribute("href")
        print("  -> Link:", href)
        
    page.screenshot(path=r'c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png')
    page.screenshot(path=r'c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\current_tiktok.png')
    print("Screenshot saved to shots/current_tiktok.png")
    browser.close()
