import asyncio
import os
import requests
from playwright.async_api import async_playwright

async def main():
    url = "https://www.tiktok.com/@benaithucchien/video/7649853202522967304"
    profile_dir = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
    video_out = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_video.mp4"
    
    media_urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check"
            ]
        )
        page = await browser.new_page()

        async def on_resp(resp):
            u = resp.url
            if ("video/tos" in u or "mime_type=video" in u) and (".mp4" in u or "tos-alisg" in u):
                if u not in media_urls:
                    media_urls.append(u)
                    print("Found video URL:", u[:100])

        page.on("response", on_resp)
        print("Navigating to TikTok...")
        await page.goto(url, wait_until="domcontentloaded", timeout=40000)
        await page.wait_for_timeout(4000)

        # Unmute & play video by clicking inside video
        try:
            await page.click("video", timeout=3000)
        except Exception:
            pass

        # Capture key frames from the live DOM
        for i in range(1, 6):
            await page.wait_for_timeout(4000)
            f_path = rf"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_f{i}.png"
            await page.screenshot(path=f_path)
            print(f"Captured frame {i} -> {f_path}")

        # Check video src directly in DOM
        try:
            dom_src = await page.eval_on_selector("video", "v => v.currentSrc || v.src")
            if dom_src:
                print("DOM video currentSrc:", dom_src[:100])
                media_urls.insert(0, dom_src)
        except Exception as e:
            print("DOM src error:", e)

        # Try to extract any text/captions
        texts = await page.eval_on_selector_all("span, h1, p", "els => els.map(e => e.innerText).filter(t => t.length > 20)")
        print("Page texts:", texts[:5])

        await browser.close()

    print("Media URLs count:", len(media_urls))
    if media_urls:
        best_url = media_urls[0]
        print("Downloading best video stream...")
        try:
            r = requests.get(best_url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.tiktok.com/"}, timeout=20)
            if r.status_code == 200 and len(r.content) > 100000:
                with open(video_out, "wb") as f:
                    f.write(r.content)
                print(f"Downloaded {len(r.content)} bytes to {video_out}")
            else:
                print(f"Download failed with status {r.status_code}, length {len(r.content)}")
        except Exception as e:
            print("Download err:", e)

if __name__ == "__main__":
    asyncio.run(main())
