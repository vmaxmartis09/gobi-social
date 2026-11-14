import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"),
        channel='chrome',
        headless=True
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto('https://www.tiktok.com/signup')
    page.wait_for_timeout(3000)
    
    # Check elements matching Google
    els = page.query_selector_all('//*[contains(text(), "Google")]')
    print(f"Found {len(els)} elements matching 'Google'")
    for idx, el in enumerate(els):
        tag = el.evaluate('e => e.tagName')
        text = el.evaluate('e => e.innerText')
        parent_tag = el.evaluate('e => e.parentElement ? e.parentElement.tagName : ""')
        parent_class = el.evaluate('e => e.parentElement ? e.parentElement.className : ""')
        parent_href = el.evaluate('e => e.parentElement ? e.parentElement.getAttribute("href") : ""')
        print(f"[{idx}] TAG: {tag} | TEXT: {repr(text)} | PARENT: {parent_tag} | CLASS: {parent_class} | HREF: {parent_href}")
    browser.close()
