import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs("shots", exist_ok=True)

with sync_playwright() as p:
    args = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1280,900"
    ]
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=USER_PROFILE_DIR,
        executable_path=CHROME_EXE,
        headless=False,
        args=args,
        viewport=None
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    # Handle OAuth popups automatically
    def handle_popup(popup):
        print(f"[POPUP] New popup opened: {popup.url}")
        try:
            popup.wait_for_load_state("domcontentloaded", timeout=15000)
            time.sleep(2)
            popup.screenshot(path="shots/everai_oauth_popup.png")
            # Click account dinhthienthoai@gmail.com or first account
            acc = popup.locator("text=dinhthienthoai@gmail.com, [data-identifier*='gmail.com'], div[data-email]").first
            if acc.count() > 0:
                print("[POPUP] Clicking Google account...")
                acc.click()
                time.sleep(3)
            # Click Continue / Tiếp tục / Cho phép if present
            cont = popup.locator("button:has-text('Continue'), button:has-text('Tiếp tục'), button:has-text('Allow'), button:has-text('Cho phép')").first
            if cont.count() > 0 and cont.is_visible():
                print("[POPUP] Clicking Continue...")
                cont.click()
                time.sleep(3)
        except Exception as e:
            print(f"[POPUP] Info: {e}")

    ctx.on("page", handle_popup)

    print("[1] Navigating to https://everai.vn ...")
    page.goto("https://everai.vn", wait_until="domcontentloaded", timeout=45000)
    time.sleep(4)
    page.screenshot(path="shots/everai_01_home.png")
    print("Current URL:", page.url)

    # Check if login button exists
    login_btn = page.locator("a:has-text('Đăng nhập'), button:has-text('Đăng nhập'), a:has-text('Bắt đầu ngay'), button:has-text('Bắt đầu ngay')").first
    if login_btn.count() > 0 and login_btn.is_visible():
        print("[2] Clicking Đăng nhập / Bắt đầu ngay...")
        login_btn.click()
        time.sleep(4)
        page.screenshot(path="shots/everai_02_login_page.png")
        print("URL after click:", page.url)

    # Check if Google login button is on page
    google_btn = page.locator("button:has-text('Google'), a:has-text('Google'), [class*='google'], button:has(svg)").first
    # Let's print all buttons and links on current page
    els = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a, button, input, [role="button"]')).map(el => ({
            tag: el.tagName,
            text: (el.innerText || el.value || '').trim().slice(0, 80),
            href: el.href || '',
            id: el.id || '',
            cls: (el.className || '').toString().slice(0, 80)
        }));
    }""")
    print("Elements on page:")
    for e in els:
        if e['text'] or e['href']:
            print(" ", e)

    ctx.close()
