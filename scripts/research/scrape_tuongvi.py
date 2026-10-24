import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SHOTS_DIR = r"shots/"
os.makedirs(SHOTS_DIR, exist_ok=True)

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        executable_path=CHROME_BIN,
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
        ],
        viewport={"width": 1280, "height": 900}
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    target_url = "https://www.facebook.com/tuongvi.kocai"
    print(f"[*] Navigating to {target_url}...")
    page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    
    # Try closing the modal
    print("[*] Checking for Close button...")
    try:
        # Check aria-label="Close" or aria-label="Đóng"
        close_btn = page.locator('div[aria-label="Close"], div[aria-label="Đóng"], [role="button"][aria-label="Close"], [role="button"][aria-label="Đóng"]')
        if close_btn.count() > 0:
            print(f"[+] Found {close_btn.count()} close button(s). Clicking first one...")
            close_btn.first.click()
            time.sleep(2)
        else:
            print("[*] No direct aria-label Close button found. Trying JS search for modal close...")
            page.evaluate("""() => {
                const buttons = Array.from(document.querySelectorAll('div[role="dialog"] div[role="button"], div[role="dialog"] [tabindex="0"]'));
                for (let b of buttons) {
                    if (b.querySelector('svg')) {
                        b.click();
                        break;
                    }
                }
            }""")
            time.sleep(2)
    except Exception as e:
        print(f"[!] Close modal attempt: {e}")

    # Remove any blocking backdrop if still present
    page.evaluate("""() => {
        document.querySelectorAll('div[role="dialog"]').forEach(d => d.remove());
        document.body.style.overflow = 'auto';
        document.documentElement.style.overflow = 'auto';
    }""")
    time.sleep(1)
    
    page.screenshot(path=os.path.join(SHOTS_DIR, "fb_modal_closed.png"))
    print("[+] Saved fb_modal_closed.png")
    
    # Let's inspect what posts are visible right now
    print("\n[*] Scrolling and expanding posts...")
    
    # Function to click all "See more" / "Xem thêm"
    def click_see_more():
        try:
            see_mores = page.locator('div[role="button"]:has-text("See more"), div[role="button"]:has-text("Xem thêm")')
            cnt = see_mores.count()
            for i in range(cnt):
                try:
                    see_mores.nth(i).click(timeout=1000)
                except:
                    pass
        except:
            pass

    posts_content = []
    
    # Scroll multiple times to collect posts
    for scroll_idx in range(1, 15):
        click_see_more()
        time.sleep(1)
        
        # Extract post text blocks
        # On Facebook, posts are often in div[data-ad-preview="message"] or div[dir="auto"]
        extracted = page.evaluate("""() => {
            const results = [];
            // find feed post containers
            const postElements = document.querySelectorAll('div[data-ad-preview="message"], div[data-ad-rendering-role="story_message"], div[dir="auto"]');
            postElements.forEach(el => {
                const txt = el.innerText.trim();
                // Filter meaningful post text (not UI nav buttons)
                if (txt.length > 40 && !results.includes(txt)) {
                    results.push(txt);
                }
            });
            return results;
        }""")
        
        for item in extracted:
            if item not in posts_content:
                posts_content.append(item)
                print(f"[+] Found Post/Content snippet ({len(item)} chars): {item[:80]}...")
                
        # Scroll down
        page.evaluate("window.scrollBy(0, 1000);")
        time.sleep(2.5)
        
        # Take periodic screenshot
        if scroll_idx in [3, 7, 12]:
            page.screenshot(path=os.path.join(SHOTS_DIR, f"fb_scroll_{scroll_idx}.png"))
            
    # Save all extracted content to file
    with open("data/raw/facebook/fb_tuongvi_knowledge.txt", "w", encoding="utf-8") as f:
        for idx, post in enumerate(posts_content, 1):
            f.write(f"==================== POST #{idx} ====================\n")
            f.write(post + "\n\n")
            
    print(f"\n[OK] Extracted {len(posts_content)} unique content blocks to data/raw/facebook/fb_tuongvi_knowledge.txt")
    context.close()
