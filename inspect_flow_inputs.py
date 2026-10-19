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
        await page.goto(PROJECT_URL, wait_until="networkidle", timeout=60000)

        # Check all file inputs on the page
        inputs = await page.locator("input[type='file']").count()
        print(f"Total file inputs on page: {inputs}")

        # Check button icons near prompt box
        btn_info = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                classes: b.className
            })).filter(b => b.text || b.aria);
        }""")
        print("Buttons on page:", btn_info[-15:])

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(main())
