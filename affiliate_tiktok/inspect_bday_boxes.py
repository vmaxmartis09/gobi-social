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
    
    # Tim tat ca cac element duoi When's your birthday
    bday_container = page.locator('div:has-text("When\'s your birthday?")').last
    children = page.eval_on_selector_all('div[class*="DivAge"] > div, div[class*="Select"], div[role="combobox"]', 'els => els.map(e => ({text: e.innerText, class: e.className, id: e.id, tag: e.tagName}))')
    print(f"Tim thay {len(children)} dropdowns:")
    for c in children:
        print(" ", c)
        
    browser.close()
