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
        await page.goto(PROJECT_URL, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(5000)

        # Dismiss "Bắt đầu" modal if visible
        for txt in ["Bắt đầu", "Got it", "Đóng", "Tiếp tục"]:
            btn = page.locator(f"button:has-text('{txt}')").first
            if await btn.count() > 0 and await btn.is_visible():
                print(f"[+] Clicking '{txt}'")
                await btn.click(force=True)
                await page.wait_for_timeout(2000)

        await page.screenshot(path="shots/flow_clean_studio.png")

        # Dump all visible buttons, inputs, textboxes
        elements = await page.evaluate("""() => {
            const items = [];
            document.querySelectorAll('button, [role="button"], textarea, input, [contenteditable="true"], mat-chip, [role="tab"]').forEach((el) => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    items.push({
                        tag: el.tagName,
                        text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('placeholder') || '').trim().replace(/\\n+/g, ' | ').slice(0, 100),
                        role: el.getAttribute('role'),
                        className: (el.className || '').toString().slice(0, 60),
                        x: Math.round(rect.x),
                        y: Math.round(rect.y),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height)
                    });
                }
            });
            return items;
        }""")
        print("=== CLEAN STUDIO ELEMENTS ===")
        for el in elements:
            print(el)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(main())
