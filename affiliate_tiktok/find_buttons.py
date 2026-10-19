import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(r'C:\Users\HAI\.agent-browser\profiles\ai_profile', channel='chrome', headless=True)
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto('https://www.tiktok.com/signup')
    page.wait_for_timeout(3000)
    buttons = page.eval_on_selector_all('a, button, div[role="button"]', 'els => els.map(e => ({text: e.innerText, href: e.href, tag: e.tagName}))')
    for b in buttons:
        txt = b.get('text', '').strip()
        if any(w in txt for w in ['Google', 'Facebook', 'phone', 'email', 'Sign up']):
            print(f"TAG: {b.get('tag')} | HREF: {b.get('href')} | TEXT: {repr(txt)}")
    browser.close()
