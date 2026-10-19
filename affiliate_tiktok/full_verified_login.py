"""
Full Verified TikTok Password Reset & Login Pipeline
1. Xoa / danh dau da doc cac mail TikTok cu trong Gmail de chi lay duy nhat ma OTP moi nhat.
2. Gui ma OTP tu trang Reset password TikTok.
3. Lay ma OTP moi (vua gui trong vong vai giay).
4. Dien OTP va mat khau ThoaiReview@2026!.
5. Submit, cho TikTok xu ly thanh cong.
6. Kiem tra cookie session, truy cap trang chu TikTok & lay username chinh xac.
7. Chup anh va cap nhat live_viewer.
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

def cleanup_old_tiktok_emails(context):
    print("[*] Don dep / kiem tra cac email TikTok cu trong Gmail...", flush=True)
    gmail = context.new_page()
    try:
        gmail.goto("https://mail.google.com/mail/u/0/#search/from%3Atiktok", timeout=45000)
        gmail.wait_for_timeout(3000)
        # Neu co email cu, chon tat ca va danh dau da doc
        select_all = gmail.locator('div[role="button"][aria-label*="Select"], div[role="checkbox"]').first
        if select_all.is_visible(timeout=3000):
            select_all.click()
            time.sleep(1)
            mark_read = gmail.locator('div[aria-label*="Mark as read"], div[aria-label*="Đánh dấu là đã đọc"]').first
            if mark_read.is_visible(timeout=2000):
                mark_read.click()
                print("[+] Da danh dau doc tat ca email TikTok cu.", flush=True)
        gmail.wait_for_timeout(1000)
    except Exception as e:
        print(f"[!] Warning khi don mail: {e}", flush=True)
    finally:
        gmail.close()

def wait_for_new_otp(context, request_timestamp):
    print(f"[*] Dang cho ma OTP moi tu TikTok (gui sau {time.strftime('%H:%M:%S', time.localtime(request_timestamp))})...", flush=True)
    gmail = context.new_page()
    try:
        gmail.goto("https://mail.google.com/mail/u/0/#inbox", timeout=45000)
        gmail.wait_for_timeout(3000)
        
        start_wait = time.time()
        while time.time() - start_wait < 75:
            # Tim email TikTok
            rows = gmail.locator('tr.zA:has-text("TikTok")')
            count = rows.count()
            if count > 0:
                print(f"[+] Phat hien {count} email TikTok moi! Dang mo email dau tien...", flush=True)
                rows.first.click()
                gmail.wait_for_timeout(2500)
                
                body = gmail.inner_text("div.a3s") if gmail.locator("div.a3s").count() > 0 else gmail.inner_text("body")
                matches = re.findall(r'\b\d{6}\b', body)
                if matches:
                    code = matches[0]
                    print(f"🎉 TIM THAY MA OTP MOI: {code}", flush=True)
                    gmail.screenshot(path=os.path.join(SHOTS_DIR, "fresh_otp.png"))
                    return code
            time.sleep(3)
            gmail.reload()
            gmail.wait_for_timeout(2000)
            
        return None
    finally:
        gmail.close()

def run():
    print("="*75, flush=True)
    print("🚀 HE THONG TU DONG HOA: RESET MAT KHAU & DANG NHAP TAI KHOAN TIKTOK", flush=True)
    print("="*75, flush=True)
    
    update_status(1, "🚀 Dang khoi dong trinh duyet voi Profile dinhthienthoai...")
    
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
        
        # Don mail cu truoc
        cleanup_old_tiktok_emails(context)
        
        page = context.pages[0] if context.pages else context.new_page()
        
        page.on("response", lambda r: print(f"<< RESP: {r.status} {r.url[:110]}", flush=True) if "passport" in r.url or "code" in r.url or "login" in r.url else None)
        
        # Buoc 1: Mo form quen mat khau
        update_status(2, "🌐 Dang mo trang Reset password TikTok...")
        page.goto("https://www.tiktok.com/login/email/forget-password", timeout=60000)
        page.wait_for_timeout(3000)
        page.screenshot(path=LIVE_IMG)
        
        # Buoc 2: Nhap Email
        update_status(2, f"✍️ Dang nhap email: {EMAIL_ADDRESS}...")
        email_input = page.locator('input[name="email"], input[placeholder*="Email"]').first
        email_input.click()
        email_input.press_sequentially(EMAIL_ADDRESS, delay=30)
        time.sleep(1)
        page.screenshot(path=LIVE_IMG)
        
        # Buoc 3: Bam Send code
        update_status(3, "📨 Dang nhap Send code de nhan ma OTP moi...")
        send_btn = page.locator('button:has-text("Send code")').first
        send_time = time.time()
        send_btn.click()
        time.sleep(3)
        page.screenshot(path=LIVE_IMG)
        
        # Kiem tra Captcha
        captcha = page.locator('div:has-text("puzzle"), div:has-text("slider"), div:has-text("ghép hình")').first
        if captcha.is_visible(timeout=2500):
            update_status(3, "⚠️ TIKTOK HIEN CAPTCHA: Hay gat thanh truot tren man hinh nhe...")
            print("[!] Gat thanh truot tren man hinh neu co Captcha...", flush=True)
            for _ in range(40):
                if not captcha.is_visible(timeout=1000):
                    print("[+] Captcha da bien mat!", flush=True)
                    break
                page.screenshot(path=LIVE_IMG)
                time.sleep(1)
                
        # Buoc 4: Lay OTP moi tu Gmail
        update_status(4, "📬 Dang tu dong trich xuat ma OTP vua gui tu Gmail...")
        new_otp = wait_for_new_otp(context, send_time)
        
        if not new_otp:
            update_status(4, "❌ Khong tim thay ma OTP moi trong Gmail. Ket thuc.")
            time.sleep(10)
            context.close()
            return
            
        update_status(4, f"🔑 Da lay duoc OTP moi: {new_otp}! Dang dien vao form...")
        code_input = page.locator('input[placeholder*="6-digit"], input[placeholder*="mã"]').first
        code_input.click()
        code_input.press_sequentially(new_otp, delay=35)
        time.sleep(0.5)
        
        # Nhap mat khau moi
        pwd_input = page.locator('input[type="password"]').first
        pwd_input.click()
        pwd_input.press_sequentially(NEW_PASSWORD, delay=35)
        time.sleep(1)
        page.screenshot(path=LIVE_IMG)
        
        # Buoc 5: Bam nut Log in (submit form)
        update_status(5, "🚀 Dang nhap nut Log in de hoan tat xac thuc...")
        submit_btn = page.locator('button[type="submit"]').first
        print(f"Submit btn is enabled: {submit_btn.is_enabled()}", flush=True)
        submit_btn.click()
        
        print("[*] Cho 10 giay de TikTok hoan tat cap nhat va thiet lap cookie session...", flush=True)
        page.wait_for_timeout(10000)
        page.screenshot(path=LIVE_IMG)
        page.screenshot(path=os.path.join(SHOTS_DIR, "after_submit_login.png"))
        
        # Buoc 6: Kiem tra trang chu va cookie
        update_status(5, "🔍 Dang truy cap trang chu TikTok de xac minh session dang nhap...")
        page.goto("https://www.tiktok.com/", timeout=45000)
        page.wait_for_timeout(5000)
        page.screenshot(path=LIVE_IMG)
        
        # Kiem tra xem co avatar hoac nut Profile khong
        is_logged_in = page.evaluate('''() => {
            const avatar = document.querySelector('img[class*="Avatar"], div[class*="avatar"], header img');
            const profileLink = document.querySelector('a[href*="/@"]');
            const loginBtn = document.querySelector('#header-login-button, button:has-text("Log in")');
            return {
                hasAvatar: !!avatar,
                profileHref: profileLink ? profileLink.getAttribute('href') : null,
                hasLoginBtn: !!loginBtn,
                cookies: document.cookie.substring(0, 200)
            };
        }''')
        print(f"[*] Ket qua kiem tra session tren TikTok: {json.dumps(is_logged_in, ensure_ascii=False)}", flush=True)
        
        if is_logged_in.get("profileHref"):
            user_url = "https://www.tiktok.com" + is_logged_in["profileHref"]
            print(f"🎉 TIM THAY URL TRANG CA NHAN CHINH XAC: {user_url}", flush=True)
            page.goto(user_url, timeout=45000)
            page.wait_for_timeout(5000)
            page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_my_real_profile.png"))
            page.screenshot(path=LIVE_IMG)
            
            acc_name = page.locator('h1[data-e2e="user-title"], h1').first.inner_text()
            acc_user = page.locator('h2[data-e2e="user-subtitle"], h2').first.inner_text()
            print("\n" + "="*75, flush=True)
            print(f"🎉 TÀI KHOẢN TIKTOK HIỆN TẠI CỦA BẠN:", flush=True)
            print(f"Tên hiển thị: {acc_name}", flush=True)
            print(f"Username TikTok: {acc_user}", flush=True)
            print(f"URL: {user_url}", flush=True)
            print("="*75, flush=True)
            update_status(5, f"🎉 ĐÃ VÀO TÀI KHOẢN TIKTOK! Tên: {acc_name} ({acc_user}) - URL: {user_url}", user_url, True)
        else:
            print("[!] Chua thay profileHref tren header, luu anh de kiem tra...", flush=True)
            page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_home_state.png"))
            
        time.sleep(20)
        context.close()

if __name__ == "__main__":
    run()
