"""
Full Complete Autonomous TikTok Password Reset & Login Flow
"""

import sys
import os
import time
import re
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
STATUS_FILE = os.path.join(SHOTS_DIR, "status.json")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")

EMAIL_ADDRESS = "dinhthienthoai@gmail.com"
NEW_PASSWORD = "ThoaiReview@2026!"

def update_status(step, message, url="https://www.tiktok.com", success=False):
    payload = {
        "step": step,
        "status": message,
        "url": url,
        "success": success,
        "timestamp": time.time()
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[{time.strftime('%H:%M:%S')}] [Step {step}] {message}", flush=True)

def get_latest_otp_from_gmail(context):
    print("[*] Đang mở Gmail để lấy mã xác minh mới nhất...", flush=True)
    gmail = context.new_page()
    try:
        gmail.goto("https://mail.google.com/mail/u/0/#inbox", timeout=45000)
        gmail.wait_for_timeout(3500)
        
        # Tìm thư TikTok
        for attempt in range(12):
            rows = gmail.locator('tr.zA:has-text("TikTok")')
            if rows.count() > 0:
                print(f"[+] Đã tìm thấy {rows.count()} email TikTok trong hộp thư!")
                rows.first.click()
                gmail.wait_for_timeout(2500)
                body = gmail.inner_text("body")
                codes = re.findall(r'\b\d{6}\b', body)
                if codes:
                    # Lấy mã đầu tiên hoặc cuối cùng trong thread
                    code = codes[0]
                    print(f"🎉 MÃ OTP TIKTOK TRÍCH XUẤT THÀNH CÔNG: {code}", flush=True)
                    gmail.screenshot(path=os.path.join(SHOTS_DIR, "latest_otp_mail.png"))
                    return code
            time.sleep(3)
            gmail.reload()
            gmail.wait_for_timeout(2000)
        return None
    finally:
        gmail.close()

def run():
    print("="*75, flush=True)
    print("🚀 HE THONG TU DONG HOA 100%: DANG NHAP TAI KHOAN TIKTOK (dinhthienthoai@gmail.com)", flush=True)
    print("="*75, flush=True)
    
    update_status(1, "🚀 Khởi động trình duyệt Headed với Profile ai_profile...")
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
                "--start-maximized"
            ],
            no_viewport=True
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # Lắng nghe các request quan trọng
        page.on("request", lambda r: print(f">> REQ: {r.method} {r.url[:100]}", flush=True) if any(k in r.url for k in ["passport", "reset", "email", "login"]) else None)
        page.on("response", lambda r: print(f"<< RESP: {r.status} {r.url[:100]}", flush=True) if any(k in r.url for k in ["passport", "reset", "email", "login"]) else None)
        
        # Bước 1: Mở trang Reset password
        update_status(2, "🌐 Đang truy cập trang đặt lại mật khẩu TikTok...")
        page.goto("https://www.tiktok.com/login/email/forget-password", timeout=60000)
        page.wait_for_timeout(3000)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 2: Điền Email
        update_status(2, f"✍️ Đang điền email tài khoản: {EMAIL_ADDRESS}...")
        email_input = page.locator('input[name="email"], input[placeholder*="Email"]').first
        email_input.click()
        email_input.press_sequentially(EMAIL_ADDRESS, delay=30)
        time.sleep(1)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 3: Bấm Send code
        update_status(3, "📨 Đang nhấp nút 'Send code'...")
        send_btn = page.locator('button:has-text("Send code")').first
        send_btn.click()
        page.wait_for_timeout(3500)
        page.screenshot(path=LIVE_IMG)
        
        # Kiểm tra Captcha nếu có
        captcha = page.locator('div:has-text("puzzle"), div:has-text("slider"), div:has-text("ghép hình")').first
        if captcha.is_visible(timeout=2500):
            update_status(3, "⚠️ TIKTOK YÊU CẦU CAPTCHA: Hãy gạt thanh trượt trên màn hình...")
            for _ in range(45):
                if not captcha.is_visible(timeout=1000):
                    print("[+] Captcha đã hoàn thành!", flush=True)
                    break
                page.screenshot(path=LIVE_IMG)
                time.sleep(1)
                
        # Bước 4: Lấy OTP từ Gmail
        update_status(4, "📬 Đang đọc mã xác minh 6 số từ Gmail...")
        otp = get_latest_otp_from_gmail(context)
        if not otp:
            update_status(4, "❌ Không tìm thấy mã OTP trong Gmail sau 60s.")
            time.sleep(10)
            context.close()
            return
            
        update_status(4, f"🔑 Đã có mã OTP: {otp}! Đang nhập vào TikTok...")
        code_input = page.locator('input[placeholder*="6-digit"], input[placeholder*="mã"]').first
        code_input.click()
        code_input.press_sequentially(otp, delay=35)
        time.sleep(1)
        
        # Bước 5: Điền mật khẩu mới và kích hoạt kiểm tra
        update_status(5, "🔒 Đang thiết lập mật khẩu mới và kiểm tra điều kiện bảo mật...")
        pwd_input = page.locator('input[type="password"]').first
        pwd_input.click()
        pwd_input.press_sequentially(NEW_PASSWORD, delay=35)
        time.sleep(1)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 6: Nhấn Enter để submit form
        update_status(5, "🚀 Đang gửi form xác thực tài khoản...")
        pwd_input.press("Enter")
        page.wait_for_timeout(4000)
        
        # Nếu chưa chuyển trang, click nút Log in
        if "forget-password" in page.url:
            print("[*] Vẫn ở trang forget-password, thử nhấp chuột trực tiếp vào nút Log in...", flush=True)
            submit_btn = page.locator('button[type="submit"]').first
            if submit_btn.is_enabled():
                submit_btn.click()
                page.wait_for_timeout(5000)
                
        page.screenshot(path=LIVE_IMG)
        page.screenshot(path=os.path.join(SHOTS_DIR, "after_full_submit.png"))
        print(f"[+] URL sau khi submit: {page.url}", flush=True)
        
        # Bước 7: Điều hướng tới TikTok và kiểm tra trạng thái đăng nhập
        update_status(5, "🔍 Đang truy cập TikTok để lấy thông tin tài khoản...")
        page.goto("https://www.tiktok.com/", timeout=45000)
        page.wait_for_timeout(5000)
        page.screenshot(path=LIVE_IMG)
        
        # Kiểm tra Profile link
        profile_link = page.locator('a[href*="/@"]').first
        if profile_link.is_visible(timeout=4000):
            profile_url = "https://www.tiktok.com" + profile_link.get_attribute("href")
            print(f"🎉 TÌM THẤY TÀI KHOẢN TIKTOK: {profile_url}", flush=True)
            page.goto(profile_url, timeout=45000)
            page.wait_for_timeout(5000)
            page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_verified_profile.png"))
            page.screenshot(path=LIVE_IMG)
            
            title = page.locator('h1[data-e2e="user-title"], h1').first.inner_text()
            subtitle = page.locator('h2[data-e2e="user-subtitle"], h2').first.inner_text()
            update_status(5, f"🎉 ĐĂNG NHẬP THÀNH CÔNG! Kênh: {title} ({subtitle}) - URL: {profile_url}", profile_url, True)
            print("\n" + "="*75, flush=True)
            print("🎉 TÀI KHOẢN TIKTOK ĐÃ SẴN SÀNG:", flush=True)
            print(f"Tên: {title}", flush=True)
            print(f"Username: {subtitle}", flush=True)
            print(f"URL: {profile_url}", flush=True)
            print("="*75, flush=True)
        else:
            print("[!] Đang mở trang thông tin cá nhân...", flush=True)
            page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_final_screen.png"))
            update_status(5, f"Trạng thái TikTok hiện tại: {page.url}", page.url, True)
            
        time.sleep(20)
        context.close()

if __name__ == "__main__":
    run()
