import asyncio
import json
import os
import re
import requests
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import imageio_ffmpeg

load_dotenv()

TARGET_URL = "https://www.tiktok.com/@ainativelab/video/7693210848747113748"
PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
SHOTS_DIR = r"C:\Users\HAI\OneDrive\Tài liệu\vmax\shots"
VIDEO_OUT = os.path.join(SHOTS_DIR, "ainative_video.mp4")
AUDIO_OUT = os.path.join(SHOTS_DIR, "ainative_audio.mp3")
INFO_OUT = os.path.join(SHOTS_DIR, "ainative_info.json")

async def main():
    os.makedirs(SHOTS_DIR, exist_ok=True)
    media_urls = []
    api_responses = []

    print(f"Target URL: {TARGET_URL}")
    print("Launching Chromium persistent context...")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=True,
            viewport={"width": 1280, "height": 900},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check"
            ]
        )
        page = await browser.new_page()

        async def on_response(response):
            try:
                url = response.url
                # Video media check
                if any(k in url for k in ["video/tos", "mime_type=video", "playAddr", ".mp4"]) and not any(k in url for k in ["favicon", ".png", ".jpg"]):
                    if url not in media_urls:
                        print(f"-> Captured video stream: {url[:100]}...")
                        media_urls.append(url)
                
                # Check for captions / vtt / transcript or api data
                if any(k in url for k in ["item/detail", "item_info", "subtitle", ".vtt", "transcript"]):
                    try:
                        ct = response.headers.get("content-type", "")
                        if "json" in ct or "text" in ct:
                            text = await response.text()
                            api_responses.append({"url": url, "data": text[:2000]})
                            print(f"-> Captured relevant API/Subtitle response: {url[:80]}")
                    except Exception:
                        pass
            except Exception:
                pass

        page.on("response", on_response)

        print("Navigating to TikTok...")
        await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(5000)

        # Extract title and description
        page_title = await page.title()
        print(f"Page Title: {page_title}")

        # Check for CAPTCHA or Login modal overlay
        try:
            close_btn = page.locator("[data-e2e='modal-close-inner-button'], button:has-text('Không phải bây giờ'), button:has-text('Not now')")
            if await close_btn.count() > 0:
                print("Closing login modal...")
                await close_btn.first.click()
                await page.wait_for_timeout(1000)
        except Exception as e:
            print("Modal close error (ignored):", e)

        # Unmute & play video if possible
        try:
            await page.click("video", timeout=3000)
            print("Clicked video element to trigger playback.")
        except Exception:
            pass

        # Capture initial screenshot
        await page.screenshot(path=os.path.join(SHOTS_DIR, "ainative_page.png"))
        print("Captured full page screenshot.")

        # Extract DOM details
        extracted_info = {
            "title": page_title,
            "descriptions": [],
            "transcripts": [],
            "hashtags": [],
            "author": ""
        }

        try:
            author_el = page.locator("[data-e2e='browser-nickname'], [data-e2e='user-title']")
            if await author_el.count() > 0:
                extracted_info["author"] = await author_el.first.inner_text()
        except Exception:
            pass

        try:
            desc_els = page.locator("[data-e2e='browse-video-desc'], h1, [data-e2e='video-desc']")
            for i in range(await desc_els.count()):
                t = await desc_els.nth(i).inner_text()
                if t and t not in extracted_info["descriptions"]:
                    extracted_info["descriptions"].append(t)
        except Exception as e:
            print("Desc extraction error:", e)

        # Check for TikTok transcript
        try:
            transcript_els = page.locator("[data-e2e='transcript-text'], [class*='DivTranscriptText']")
            for i in range(await transcript_els.count()):
                t = await transcript_els.nth(i).inner_text()
                if t:
                    extracted_info["transcripts"].append(t)
        except Exception as e:
            print("Transcript extraction error:", e)

        # Capture video frames across 25 seconds
        frame_paths = []
        for f_idx in range(1, 9):
            await page.wait_for_timeout(3000)
            f_path = os.path.join(SHOTS_DIR, f"ainative_f{f_idx}.png")
            try:
                video_el = page.locator("video")
                if await video_el.count() > 0:
                    await video_el.first.screenshot(path=f_path)
                else:
                    await page.screenshot(path=f_path)
                frame_paths.append(f_path)
                print(f"Captured frame {f_idx}: {f_path}")
            except Exception as e:
                print(f"Frame {f_idx} screenshot err:", e)

        # Check currentSrc from video tag
        try:
            dom_src = await page.eval_on_selector("video", "v => v.currentSrc || v.src")
            if dom_src and dom_src not in media_urls:
                print(f"Captured DOM currentSrc: {dom_src[:100]}...")
                media_urls.insert(0, dom_src)
        except Exception as e:
            print("DOM src error:", e)

        # Extract browser cookies for download
        cookies = await browser.cookies()
        cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies if 'tiktok' in c['domain']])

        await browser.close()

    # Save extracted info
    extracted_info["media_urls"] = media_urls
    extracted_info["frame_paths"] = frame_paths
    with open(INFO_OUT, "w", encoding="utf-8") as f:
        json.dump(extracted_info, f, ensure_ascii=False, indent=2)
    print(f"Saved metadata to {INFO_OUT}")

    # Attempt video download
    download_success = False
    if media_urls:
        print(f"Found {len(media_urls)} media candidates. Attempting download...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
            "Cookie": cookie_header
        }
        for u in media_urls[:3]:
            try:
                print(f"Downloading stream: {u[:100]}...")
                r = requests.get(u, headers=headers, stream=True, timeout=30)
                if r.status_code == 200:
                    total_bytes = 0
                    with open(VIDEO_OUT, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024*64):
                            if chunk:
                                f.write(chunk)
                                total_bytes += len(chunk)
                    if total_bytes > 50000:
                        print(f"Downloaded video successfully: {total_bytes} bytes -> {VIDEO_OUT}")
                        download_success = True
                        break
                    else:
                        print(f"File too small ({total_bytes} bytes), skipping.")
                else:
                    print(f"HTTP {r.status_code} for {u[:60]}")
            except Exception as e:
                print(f"Download stream error: {e}")

    # Extract audio if video downloaded
    if download_success and os.path.exists(VIDEO_OUT):
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"Extracting audio using FFmpeg ({ffmpeg_exe})...")
        cmd = f'"{ffmpeg_exe}" -y -i "{VIDEO_OUT}" -vn -ar 16000 -ac 1 -ab 128k -f mp3 "{AUDIO_OUT}"'
        res = os.system(cmd)
        print(f"FFmpeg audio extraction result code: {res}")
        if os.path.exists(AUDIO_OUT):
            print(f"Audio extracted successfully: {os.path.getsize(AUDIO_OUT)} bytes -> {AUDIO_OUT}")

if __name__ == "__main__":
    asyncio.run(main())
