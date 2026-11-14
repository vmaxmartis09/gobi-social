import sys
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
    page.goto("https://www.tiktok.com/signup/phone-or-email/email")
    page.wait_for_timeout(3000)
    
    age_selectors = page.locator('div.tiktok-psovae-de495bb3--DivAgeSelector > div')
    print("Found age selectors:", age_selectors.count())
    
    # Month
    print("Selecting Month (July)...")
    age_selectors.nth(0).click()
    page.wait_for_timeout(500)
    page.locator('div[id*="Month-options-item-"]:has-text("July")').first.click()
    page.wait_for_timeout(500)
    
    # Day
    print("Selecting Day (8)...")
    age_selectors.nth(1).click()
    page.wait_for_timeout(500)
    page.locator('div[id*="Day-options-item-"]:has-text("8")').first.click()
    page.wait_for_timeout(500)
    
    # Year
    print("Selecting Year (2000)...")
    age_selectors.nth(2).click()
    page.wait_for_timeout(500)
    year_target = page.locator('div[id*="Year-options-item-"]:has-text("2000")').first
    year_target.scroll_into_view_if_needed()
    year_target.click()
    page.wait_for_timeout(1000)
    
    # Print current values
    print("Selected Birthday values:")
    print("  Month:", age_selectors.nth(0).inner_text().strip())
    print("  Day:", age_selectors.nth(1).inner_text().strip())
    print("  Year:", age_selectors.nth(2).inner_text().strip())
    
    # Fill email and check if Send code becomes enabled!
    page.fill('input[name="email"]', 'dinhthienthoai@gmail.com')
    page.fill('input[type="password"]', 'ThoaiReview@2026!')
    page.wait_for_timeout(1000)
    
    send_btn = page.locator('button[data-e2e="send-code-button"]').first
    print("Send code button is enabled?:", send_btn.is_enabled())
    
    page.screenshot(path=r"shots/bday_and_send_code_ready.png")
    page.screenshot(path=r"shots/live.png")
    browser.close()
