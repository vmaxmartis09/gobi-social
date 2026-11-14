import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")

def capture():
    print("Capturing @ber.review video with modal bypass...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        url = "https://www.tiktok.com/@ber.review/video/7680784467144887573"
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        # 1. Close or remove login modal
        try:
            # Try clicking close button
            btn = page.query_selector('div[role="dialog"] button, [data-e2e="modal-close-inner-button"], svg:has(path[d*="M19.707"])')
            if btn:
                print("Clicking close button...")
                btn.click()
            else:
                print("Removing modal via JS...")
                page.evaluate('''() => {
                    document.querySelectorAll('div[role="dialog"], #loginContainer, div[class*="DivLoginContainer"], div[class*="DivModalMask"]').forEach(el => el.remove());
                }''')
        except Exception as e:
            print("Modal handle error:", e)

        page.wait_for_timeout(2000)

        # 2. Check for warning button "Watch video" / "Xem video" / "Open TikTok"
        try:
            btns = page.query_selector_all('button')
            for b in btns:
                txt = b.inner_text().strip()
                if any(w in txt.lower() for w in ["watch", "xem", "continue", "tiếp tục"]):
                    print(f"Found warning button: '{txt}', clicking...")
                    b.click()
                    break
        except Exception as e:
            print("Warning button error:", e)

        page.wait_for_timeout(3000)

        # 3. Take screenshot
        shot_path = os.path.join(SHOTS_DIR, "ber_video_unmasked.png")
        page.screenshot(path=shot_path)
        print(f"Unmasked screenshot saved to {shot_path}")

        # 4. Extract video details
        details = page.evaluate('''() => {
            const video = document.querySelector('video');
            const h1 = document.querySelector('h1, [data-e2e="browse-video-desc"], [data-e2e="video-desc"]');
            const author = document.querySelector('[data-e2e="browser-nickname"], [data-e2e="user-title"], h2');
            const sound = document.querySelector('[data-e2e="browse-music"]');
            const textNodes = Array.from(document.querySelectorAll('span, p, h1, h2, h3, h4'))
                                  .map(el => el.innerText.trim())
                                  .filter(t => t.length > 5 && t.length < 200);
            return {
                videoSrc: video ? (video.currentSrc || video.src) : '',
                desc: h1 ? h1.innerText : '',
                author: author ? author.innerText : '',
                sound: sound ? sound.innerText : '',
                samples: textNodes.slice(0, 25)
            };
        }''')
        print("Details extracted:", details)

        browser.close()

if __name__ == "__main__":
    capture()
