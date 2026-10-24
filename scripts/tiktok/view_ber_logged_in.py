import sys
import os
import json
import time
import base64
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
TARGET_URL = "https://www.tiktok.com/@ber.review/video/7680784467144887573"

def run():
    print("="*75)
    print("🎬 ĐANG PHÂN TÍCH VIDEO @ber.review...")
    print(f"[*] URL: {TARGET_URL}")
    print("="*75)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
                "--start-maximized"
            ],
            no_viewport=True
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(TARGET_URL, timeout=45000)
        
        # Wait up to 15s for video element to be attached and playing
        print("[*] Đang chờ video load dữ liệu...")
        time.sleep(8)

        # Wait for video to have readyState >= 2
        try:
            page.wait_for_function('''() => {
                const v = document.querySelector('video');
                return v && (v.readyState >= 2 || v.currentTime > 0);
            }''', timeout=15000)
            print("[+] Video đã sẵn sàng phát!")
        except Exception as e:
            print("[!] Timeout chờ video:", e)

        time.sleep(3)

        # Full page screenshot
        shot_path = os.path.join(SHOTS_DIR, "ber_review_page.png")
        page.screenshot(path=shot_path)
        print(f"[+] Full page screenshot: {shot_path}")

        # Capture video element screenshot
        video_shot = os.path.join(SHOTS_DIR, "ber_review_video_element.png")
        try:
            v_el = page.query_selector('video')
            if v_el:
                v_el.screenshot(path=video_shot)
                print(f"[+] Video element screenshot: {video_shot}")
        except Exception as e:
            print("Video screenshot error:", e)

        # Extract frames via canvas
        try:
            frames = page.evaluate('''() => {
                const v = document.querySelector('video');
                if (!v) return null;
                const canvas = document.createElement('canvas');
                canvas.width = v.videoWidth || 720;
                canvas.height = v.videoHeight || 1280;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
                return canvas.toDataURL('image/jpeg', 0.85);
            }''')
            if frames and frames.startswith("data:image/jpeg;base64,"):
                b64 = frames.split(",")[1]
                frame_path = os.path.join(SHOTS_DIR, "ber_review_canvas_frame.jpg")
                with open(frame_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"[+] Video frame canvas captured: {frame_path}")
        except Exception as e:
            print("Canvas frame error:", e)

        # Extract all metadata & text
        info = page.evaluate('''() => {
            const h1 = document.querySelector('h1[data-e2e="browse-video-desc"], div[data-e2e="browse-video-desc"], [data-e2e="video-desc"]');
            const author = document.querySelector('span[data-e2e="browser-nickname"], [data-e2e="user-title"], h2');
            const music = document.querySelector('h4[data-e2e="browse-music"], [data-e2e="video-music"]');
            const product = document.querySelector('[data-e2e="video-anchor"], [class*="Anchor"], a[href*="shop"]');
            const captions = Array.from(document.querySelectorAll('[class*="caption"], [class*="subtitle"], [class*="Caption"]')).map(e => e.innerText);
            const visibleTexts = Array.from(document.querySelectorAll('span, p, div, a'))
                .map(e => e.innerText ? e.innerText.trim() : '')
                .filter(t => t.length > 5 && t.length < 150);
            
            return {
                title: document.title,
                desc: h1 ? h1.innerText : '',
                author: author ? author.innerText : '',
                music: music ? music.innerText : '',
                product: product ? product.innerText : '',
                captions: captions,
                visibleTexts: Array.from(new Set(visibleTexts)).slice(0, 30)
            };
        }''')

        print("\n" + "="*50)
        print("KẾT QUẢ TRÍCH XUẤT:")
        print(json.dumps(info, ensure_ascii=False, indent=2))
        print("="*50 + "\n")

        with open(os.path.join(SHOTS_DIR, "ber_analysis.json"), "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

        # Giữ màn hình mở để người dùng xem trực tiếp
        print("[*] Đang giữ trình duyệt mở trên màn hình cho bạn quan sát...")
        for _ in range(120):
            time.sleep(1)

if __name__ == "__main__":
    run()
