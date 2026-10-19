from playwright.sync_api import sync_playwright
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        executable_path=CHROME_BIN,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://www.facebook.com/tuongvi.kocai', wait_until='domcontentloaded')
    time.sleep(3)
    
    graphql_reqs = []
    page.on('request', lambda r: graphql_reqs.append(r.url) if 'graphql' in r.url else None)
    
    # Observer script to remove modals continuously
    js_observer = """
    (() => {
        function cleanup() {
            document.querySelectorAll('div[role="dialog"]').forEach(d => d.remove());
            document.querySelectorAll('div[data-pagelet="root"] ~ div').forEach(d => {
                const style = window.getComputedStyle(d);
                if (style.position === 'fixed' || style.zIndex > 100) {
                    d.remove();
                }
            });
            document.body.style.overflow = 'auto';
            document.documentElement.style.overflow = 'auto';
        }
        cleanup();
        setInterval(cleanup, 500);
    })();
    """
    page.evaluate(js_observer)
    
    for i in range(1, 10):
        page.evaluate("window.scrollBy(0, 2000)")
        time.sleep(3)
        print(f"Scroll {i}: GraphQL requests intercepted: {len(graphql_reqs)}")
        
    page.screenshot(path=r"shots\fb_scroll_test.png")
    context.close()
