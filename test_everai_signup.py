import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_PROFILE_DIR = os.environ.get("USER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", "ai_profile"))
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

    print("[1] Navigating to https://everai.vn/sign-up ...")
    page.goto("https://everai.vn/sign-up", wait_until="domcontentloaded", timeout=45000)
    time.sleep(3)
    page.screenshot(path="shots/everai_signup_page.png")

    email = f"vmax.voice.{int(time.time())}@gmail.com"
    pwd = "VmaxVoiceAI@2026!"
    print(f"[2] Filling signup form: {email} ...")
    page.fill("#id_email", email)
    page.fill("#id_password1", pwd)
    page.fill("#id_password2", pwd)
    time.sleep(1)

    print("[3] Clicking Đăng ký ...")
    signup_btn = page.locator("button:has-text('Đăng ký'), input[type='submit']").first
    signup_btn.click()
    time.sleep(5)
    page.screenshot(path="shots/everai_signup_result.png")
    print("Post-signup URL:", page.url)

    # Print page message / text
    msg = page.evaluate("() => document.body.innerText.slice(0, 500)")
    print("Page text snippet:\n", msg)

    ctx.close()
