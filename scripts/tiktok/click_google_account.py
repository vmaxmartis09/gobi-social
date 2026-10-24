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
    
    # Bấm Continue with Google
    print("[1] Bấm nút Continue with Google...")
    google_btn = page.get_by_text("Continue with Google")
    with browser.expect_page() as p_info:
        google_btn.click()
    popup = p_info.value
    popup.wait_for_load_state("domcontentloaded")
    print("[2] Popup opened:", popup.url[:60])
    popup.wait_for_timeout(3000)
    
    # Bấm vào Thiên Thoại Đinh
    print("[3] Bấm vào tên 'Thiên Thoại Đinh'...")
    acc_target = popup.get_by_text("Thiên Thoại Đinh")
    box = acc_target.bounding_box()
    print("Bounding box of account:", box)
    if box:
        popup.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    else:
        acc_target.click()
        
    print("[4] Đang chờ Google xử lý và chuyển hướng...")
    for i in range(12):
        time.sleep(1)
        if popup.is_closed():
            print(f"[+] Popup đã đóng sau {i+1} giây!")
            break
        try:
            # Kiểm tra xem có yêu cầu nhập mật khẩu hay nút Tiếp tục không
            p_text = popup.inner_text("body")
            if "Nhập mật khẩu" in p_text or "Enter your password" in p_text:
                print("[!] GOOGLE ĐANG HỎI XÁC NHẬN MẬT KHẨU CỦA DINHTHIENTHOAI@GMAIL.COM!")
                popup.screenshot(path=os.path.join(SHOTS_DIR, "google_needs_password.png"))
                break
            # Nếu có nút Tiếp tục / Continue
            for btn_label in ["Tiếp tục", "Continue", "Cho phép", "Allow"]:
                b = popup.get_by_text(btn_label, exact=True)
                if b.is_visible(timeout=500):
                    print(f"Bấm nút {btn_label} trên popup Google...")
                    b.click()
        except Exception:
            pass
            
    page.wait_for_timeout(6000)
    print("\n[5] Trang TikTok hiện tại:")
    print("URL:", page.url)
    print("Title:", page.title())
    page.screenshot(path=LIVE_IMG)
    page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_after_oauth_click.png"))
    
    # Ghi lại nội dung text hiện tại trên TikTok
    body_lines = [l.strip() for l in page.inner_text("body").split("\n") if l.strip()]
    print("\nNội dung hiển thị trên trang TikTok:")
    for l in body_lines[:20]:
        print("  ->", l)
        
    browser.close()
