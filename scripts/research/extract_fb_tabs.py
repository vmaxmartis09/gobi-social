import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SHOTS_DIR = r"shots/"
PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

tabs = [
    ("reels", "https://www.facebook.com/tuongvi.kocai/reels"),
    ("photos", "https://www.facebook.com/tuongvi.kocai/photos"),
    ("about", "https://www.facebook.com/tuongvi.kocai/about"),
]

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        executable_path=CHROME_BIN,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    for tab_name, url in tabs:
        print(f"\n[*] Navigating to {url}...")
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(4)
            # Dismiss modal
            page.evaluate("""() => {
                document.querySelectorAll('div[role="dialog"]').forEach(d => d.remove());
                document.querySelectorAll('div[data-pagelet="root"] ~ div').forEach(d => {
                    const style = window.getComputedStyle(d);
                    if (style.position === 'fixed' || style.zIndex > 100) d.remove();
                });
                document.body.style.overflow = 'auto';
            }""")
            time.sleep(1)
            
            shot_path = os.path.join(SHOTS_DIR, f"fb_tab_{tab_name}.png")
            page.screenshot(path=shot_path)
            print(f"[+] Screenshot saved to {shot_path}")
            
            # Extract links and texts
            texts = page.evaluate("""() => {
                const res = [];
                document.querySelectorAll('span, a, div[dir="auto"]').forEach(el => {
                    const t = el.innerText ? el.innerText.trim() : '';
                    if (t.length > 25 && !res.includes(t)) {
                        res.push(t);
                    }
                });
                return res;
            }""")
            
            print(f"[+] Extracted {len(texts)} text snippets from {tab_name}.")
            with open(f"fb_{tab_name}_extracted.txt", "w", encoding="utf-8") as out:
                for t in texts:
                    out.write(t + "\n---\n")
        except Exception as e:
            print(f"[!] Error on {tab_name}: {e}")

    context.close()
    print("\n[OK] Finished tab extraction.")
