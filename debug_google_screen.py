import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_PROFILE_DIR = os.environ.get("USER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", "ai_profile"))
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=USER_PROFILE_DIR,
        executable_path=CHROME_EXE,
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = ctx.new_page()
    page.goto("https://everai.vn/login?next=/", wait_until="domcontentloaded")
    time.sleep(2)
    google_btn = page.locator("button:has-text('Đăng nhập với Google')").first
    if google_btn.is_visible():
        google_btn.click()
        time.sleep(5)
    print("URL:", page.url)
    try:
        page.screenshot(path="shots/google_login_debug.png", timeout=5000)
    except Exception as e:
        print("Screenshot error:", e)
    text = page.evaluate("() => document.body.innerText")
    print("PAGE BODY TEXT:\n", text[:1000])
    ctx.close()
