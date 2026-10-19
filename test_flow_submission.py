import os
import sys
import asyncio
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
PROFILE_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\AI_Agent_Profile")
PROJECT_URL = "https://flow.google.com/project/905a28b7-ceb4-4cf9-b92d-443050bd2d43"

async def main():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled", "--no-first-run"]
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        page.on("response", lambda resp: print(f"API: {resp.status} {resp.url[:120]}") if any(k in resp.url for k in ["generate", "predict", "flow", "session", "batch", "run"]) else None)

        await page.goto(PROJECT_URL, wait_until="networkidle", timeout=60000)
        
        textbox = page.locator(".ProseMirror, [contenteditable='true']").first
        await textbox.click()
        await textbox.fill("A cinematic video of a cute cat playing with a yarn ball, photorealistic")
        await page.wait_for_timeout(1000)

        # Click the arrow_forward button
        gen_btn = page.locator("button[aria-label='Bắt đầu tạo'], button.generate-icon-button").first
        print("[*] Clicking arrow_forward submit button...")
        await gen_btn.click()
        
        # Wait 15s to capture API responses
        await page.wait_for_timeout(15000)
        await page.screenshot(path="shots/flow_api_test.png")

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(main())
