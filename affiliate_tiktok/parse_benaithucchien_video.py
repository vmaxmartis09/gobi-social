import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    url = "https://www.tiktok.com/@benaithucchien/video/7649853202522967304"
    profile_dir = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
    
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
        print(f"Navigating to {url} ...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(5000)

        # Extract title, caption, hashtags, description
        title = await page.title()
        print("Page title:", title)

        # Take screenshot of the video page
        shot_path = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_video.png"
        await page.screenshot(path=shot_path)
        print("Saved screenshot to", shot_path)

        # Extract text content from description / caption
        desc = ""
        try:
            h1 = await page.locator("h1").all_text_contents()
            desc += "\n".join(h1)
        except Exception as e:
            print("h1 error:", e)

        try:
            spans = await page.locator("[data-e2e='browse-video-desc']").all_text_contents()
            desc += "\n" + "\n".join(spans)
        except Exception as e:
            print("desc error:", e)

        # Extract transcript if available
        transcripts = []
        try:
            t_elems = await page.locator("[data-e2e='transcript-text']").all_text_contents()
            transcripts = t_elems
        except Exception:
            pass

        # Try to find video src or audio src
        video_src = ""
        try:
            v_elem = page.locator("video")
            video_src = await v_elem.get_attribute("src") or ""
        except Exception:
            pass

        data = {
            "url": url,
            "title": title,
            "description": desc.strip(),
            "transcript": transcripts,
            "video_src": video_src
        }

        out_json = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_info.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved info to {out_json}")
        print("Description:", desc[:500])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
