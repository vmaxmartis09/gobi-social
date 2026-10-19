import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.facebook.com/tuongvi.kocai', wait_until='domcontentloaded')
    
    links = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            href: a.href,
            text: a.innerText.trim()
        })).filter(l => l.href);
    }""")
    
    with open('fb_links.txt', 'w', encoding='utf-8') as f:
        for l in links:
            f.write(f"{l['text']} -> {l['href']}\n")
            
    print(f"Saved {len(links)} links to fb_links.txt")
    browser.close()
