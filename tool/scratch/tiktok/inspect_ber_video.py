import sys
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")

def inspect_ber_video():
    with sync_playwright() as p:
        try:
            print("Connecting to existing Chrome via CDP (localhost:9222)...")
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.new_page()
            url = "https://www.tiktok.com/@ber.review/video/7680784467144887573"
            print(f"Navigating to {url}...")
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            
            # Check if there's any close button for modal
            close_btn = page.query_selector('div[data-e2e="modal-close-inner-button"], button[aria-label="Close"]')
            if close_btn:
                print("Closing modal...")
                close_btn.click()
                page.wait_for_timeout(2000)
                
            # If warning button ("Watch video" / "Xem video")
            warn_btn = page.query_selector('button:has-text("Watch video"), button:has-text("Xem video"), button:has-text("Tiếp tục xem")')
            if warn_btn:
                print("Clicking watch warning button...")
                warn_btn.click()
                page.wait_for_timeout(2000)

            shot_path = os.path.join(SHOTS_DIR, "ber_review_detail.png")
            page.screenshot(path=shot_path)
            print(f"Detail screenshot saved to {shot_path}")

            # Extract detailed video info
            info = page.evaluate('''() => {
                const desc = document.querySelector('h1[data-e2e="browse-video-desc"], div[data-e2e="browse-video-desc"], [data-e2e="video-desc"]');
                const author = document.querySelector('span[data-e2e="browser-nickname"], [data-e2e="user-title"]');
                const music = document.querySelector('h4[data-e2e="browse-music"]');
                const videoTag = document.querySelector('video');
                const videoSrc = videoTag ? (videoTag.src || videoTag.currentSrc) : '';
                return {
                    desc: desc ? desc.innerText : document.title,
                    author: author ? author.innerText : '',
                    music: music ? music.innerText : '',
                    videoSrc: videoSrc
                };
            }''')
            print("Video Info:", json.dumps(info, ensure_ascii=False, indent=2))
        except Exception as e:
            print("CDP Error:", e)

if __name__ == "__main__":
    inspect_ber_video()
