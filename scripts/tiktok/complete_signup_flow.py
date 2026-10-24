import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/signup")
    page.wait_for_timeout(3000)
    
    google_btn = page.locator('div:has-text("Continue with Google"), a:has-text("Continue with Google")').last
    
    print("[1] Bấm nút Continue with Google...")
    with browser.expect_page() as popup_info:
        google_btn.click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded")
    print("[2] Popup opened:", popup.url[:60])
    popup.wait_for_timeout(2000)
    
    print("[3] Bấm vào dòng tài khoản Thiên Thoại Đinh...")
    acc = popup.locator('div:has-text("dinhthienthoai@gmail.com")').last
    acc.click()
    
    # Chờ xem popup có đóng không hoặc có nút Tiếp tục / Continue không
    print("[4] Đang chờ Google xử lý token...")
    for _ in range(8):
        time.sleep(1)
        if popup.is_closed():
            print("[+] Popup Google đã đóng thành công!")
            break
        # Nếu có nút Continue hoặc Tiếp tục thì bấm
        for b_text in ["Continue", "Tiếp tục", "Xác nhận"]:
            b = popup.locator(f'button:has-text("{b_text}"), div[role="button"]:has-text("{b_text}")').first
            try:
                if b.is_visible(timeout=500):
                    print(f"Bấm nút {b_text} trên Google...")
                    b.click()
            except Exception:
                pass
                
    print("[5] Đang kiểm tra trang TikTok sau khi xác thực...")
    page.wait_for_timeout(5000)
    print("TikTok Current URL:", page.url)
    page.screenshot(path=LIVE_IMG)
    page.screenshot(path=os.path.join(SHOTS_DIR, "after_complete_oauth.png"))
    
    # Kiểm tra xem có trường ngày sinh (Birthday) hoặc Username không
    content = page.content()
    print("Page content length:", len(content))
    if "birthday" in content.lower() or "ngày sinh" in content.lower():
        print("[!] TIKTOK ĐANG YÊU CẦU NHẬP NGÀY SINH (BIRTHDAY)!")
    if "username" in content.lower() or "tên người dùng" in content.lower():
        print("[!] TIKTOK ĐANG YÊU CẦU ĐẶT TÊN NGƯỜI DÙNG (USERNAME)!")
    if "puzzle" in content.lower() or "slider" in content.lower():
        print("[!] TIKTOK ĐANG YÊU CẦU GIẢI CAPTCHA!")
        
    browser.close()
