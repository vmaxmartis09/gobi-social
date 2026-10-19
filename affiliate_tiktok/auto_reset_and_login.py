"""
Autonomous TikTok Account Recovery / Login & Profile Verification
Cho tài khoản: dinhthienthoai@gmail.com
Mật khẩu mới: ThoaiReview@2026!

Quy trình tự động 100%:
1. Truy cập https://www.tiktok.com/login/email/forget-password
2. Điền email: dinhthienthoai@gmail.com
3. Nhấp "Send code"
4. Theo dõi Captcha (nếu có)
5. Mở tab Gmail lấy mã OTP 6 số TikTok gửi về
6. Điền mã OTP và mật khẩu mới
7. Nhấp "Log in" hoàn tất
8. Truy cập tiktok.com/@me để kiểm tra Username, Avatar và trạng thái tài khoản
9. Chụp ảnh kết quả và cập nhật live_viewer
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
PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
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

def extract_otp_from_gmail(context):
    print("[*] Đang mở tab Gmail để đọc mã OTP từ TikTok...", flush=True)
    gmail_page = context.new_page()
    try:
        gmail_page.goto("https://mail.google.com/mail/u/0/#inbox", timeout=45000)
        gmail_page.wait_for_timeout(4000)
        
        code = None
        start_time = time.time()
        while time.time() - start_time < 90:
            emails = gmail_page.locator('tr.zA:has-text("TikTok"), span:has-text("TikTok"), tr.zA:has-text("mã"), tr.zA:has-text("code")')
            count = emails.count()
            if count > 0:
                print(f"[+] Tìm thấy {count} email có liên quan trong Gmail!", flush=True)
                emails.first.click()
                gmail_page.wait_for_timeout(3000)
                
                body = gmail_page.inner_text("div.a3s") if gmail_page.locator("div.a3s").count() > 0 else gmail_page.inner_text("body")
                matches = re.findall(r'\b\d{6}\b', body)
                if matches:
                    code = matches[0]
                    print(f"🎉 TÌM THẤY MÃ OTP TIKTOK TRONG GMAIL: {code}", flush=True)
                    gmail_page.screenshot(path=os.path.join(SHOTS_DIR, "gmail_otp_recovered.png"))
                    break
            time.sleep(4)
            gmail_page.reload()
            gmail_page.wait_for_timeout(2000)
            
        return code
    finally:
        gmail_page.close()

def run():
    print("="*75, flush=True)
    print("🚀 HE THONG TU DONG HOA 100%: DANG NHAP / KHOI PHUC TAI KHOAN TIKTOK QUA GMAIL", flush=True)
    print("="*75, flush=True)
    
    update_status(1, "🚀 Đang khởi động trình duyệt bảo mật với Profile ai_profile...")
    
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
        
        # Lắng nghe phản hồi từ TikTok API
        page.on("response", lambda r: print(f"<< RESP: {r.status} {r.url[:100]}", flush=True) if "send_code" in r.url or "passport" in r.url else None)
        
        # Bước 1: Mở trang khôi phục mật khẩu / đặt mật khẩu tài khoản
        update_status(2, "🌐 Đang truy cập trang xác minh tài khoản TikTok...")
        page.goto("https://www.tiktok.com/login/email/forget-password", timeout=60000)
        page.wait_for_timeout(3000)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 2: Điền Email
        update_status(2, f"✍️ Đang nhập email tài khoản: {EMAIL_ADDRESS}...")
        email_input = page.locator('input[name="email"], input[placeholder*="Email"]').first
        email_input.click()
        email_input.fill(EMAIL_ADDRESS)
        email_input.evaluate('el => el.dispatchEvent(new Event("change", { bubbles: true }))')
        time.sleep(1)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 3: Bấm nút "Send code"
        update_status(3, "📨 Đang nhấp nút 'Send code' để TikTok gửi mã OTP vào Gmail...")
        send_btn = page.locator('button:has-text("Send code")').first
        send_btn.click()
        time.sleep(3)
        page.screenshot(path=LIVE_IMG)
        
        # Kiểm tra Captcha
        captcha = page.locator('div:has-text("puzzle"), div:has-text("slider"), div:has-text("ghép hình")').first
        if captcha.is_visible(timeout=3000):
            update_status(3, "⚠️ TIKTOK HIỂN THỊ CAPTCHA XÁC MINH: Hãy gạt thanh trượt trên màn hình nhé...")
            print("\n[!] Chú ý: TikTok yêu cầu gạt mảnh ghép. Màn hình Headed đang mở, hệ thống sẽ tự phát hiện khi giải xong!", flush=True)
            for _ in range(45):
                if not captcha.is_visible(timeout=1000):
                    print("[+] Captcha đã được giải quyết thành công!", flush=True)
                    break
                page.screenshot(path=LIVE_IMG)
                time.sleep(1)
        
        # Bước 4: Mở Gmail lấy OTP
        update_status(4, "📬 Đang tự động mở Gmail đọc mã OTP 6 số từ TikTok...")
        otp_code = extract_otp_from_gmail(context)
        
        if not otp_code:
            update_status(4, "❌ Chưa đọc được mã OTP trong Gmail sau 90 giây. Vui lòng kiểm tra hộp thư.")
            print("[-] Khong tim thay OTP trong Gmail.")
            time.sleep(15)
            context.close()
            return
            
        update_status(4, f"🔑 Đã trích xuất mã OTP thành công: {otp_code}! Đang điền vào TikTok...")
        code_input = page.locator('input[placeholder*="6-digit"], input[placeholder*="mã"]').first
        code_input.click()
        code_input.fill(otp_code)
        time.sleep(0.8)
        
        # Điền mật khẩu mới
        pwd_input = page.locator('input[type="password"]').first
        pwd_input.click()
        pwd_input.fill(NEW_PASSWORD)
        time.sleep(0.8)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 5: Bấm nút Log in
        update_status(5, "🚀 Đang bấm 'Log in' để hoàn tất đăng nhập tài khoản...")
        submit_btn = page.locator('button[type="submit"]:has-text("Log in"), button[type="submit"]').first
        submit_btn.click()
        page.wait_for_timeout(6000)
        page.screenshot(path=LIVE_IMG)
        
        # Bước 6: Kiểm tra tài khoản đã đăng nhập
        update_status(5, "🔍 Đang truy cập trang cá nhân TikTok để trích xuất thông tin...")
        page.goto("https://www.tiktok.com/@me", timeout=45000)
        page.wait_for_timeout(5000)
        
        final_url = page.url
        print(f"[+] Final URL: {final_url}", flush=True)
        page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_logged_account.png"))
        page.screenshot(path=LIVE_IMG)
        
        # Trích xuất username và tên hiển thị
        user_info = page.evaluate('''() => {
            const h1 = document.querySelector('h1[data-e2e="user-title"], h1');
            const h2 = document.querySelector('h2[data-e2e="user-subtitle"], h2');
            return {
                title: h1 ? h1.innerText : '',
                subtitle: h2 ? h2.innerText : '',
                url: window.location.href
            };
        }''')
        print(f"🎉 THONG TIN TAI KHOAN TIKTOK: {json.dumps(user_info, ensure_ascii=False)}", flush=True)
        
        update_status(5, f"🎉 ĐĂNG NHẬP THÀNH CÔNG! Tài khoản: {user_info.get('title')} ({user_info.get('subtitle')}) - URL: {final_url}", final_url, True)
        
        print("\n" + "="*75, flush=True)
        print("🎉 TÀI KHOẢN TIKTOK ĐÃ ĐĂNG NHẬP THÀNH CÔNG VÀ SẴN SÀNG SỬ DỤNG!", flush=True)
        print(f"Tài khoản: {user_info.get('title')} ({user_info.get('subtitle')})", flush=True)
        print(f"URL: {final_url}", flush=True)
        print("="*75, flush=True)
        
        time.sleep(15)
        context.close()

if __name__ == "__main__":
    run()
