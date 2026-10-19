import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    url = "https://www.tiktok.com/@benaithucchien/video/7649853202522967304"
    profile_dir = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
    video_out = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_full.mp4"
    
    target_video_url = []

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
            if ("video/tos" in u or "tos-alisg-ve" in u) and not u.startswith("blob:"):
                target_video_url.append(u)

        page.on("response", on_resp)
        print("Navigating...")
        await page.goto(url, wait_until="domcontentloaded", timeout=40000)
        await page.wait_for_timeout(3000)

        # Let it play and capture frames every 5s across the 60s video
        for t in range(5, 55, 6):
            await page.wait_for_timeout(6000)
            shot_file = rf"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_t{t}.png"
            await page.screenshot(path=shot_file)
            print(f"Captured {shot_file}")

        print("Total video streams caught:", len(target_video_url))
        if target_video_url:
            v_url = target_video_url[0]
            print("Fetching video using browser context request...", v_url[:100])
            try:
                res = await page.request.get(v_url, headers={"Referer": "https://www.tiktok.com/"})
                if res.status == 200:
                    body = await res.body()
                    with open(video_out, "wb") as f:
                        f.write(body)
                    print(f"SUCCESS: Saved full video ({len(body)} bytes) to {video_out}")
            except Exception as e:
                print("Context get error:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
