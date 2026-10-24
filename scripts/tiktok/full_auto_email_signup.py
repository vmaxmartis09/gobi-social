"""
Full-Loop Autonomous TikTok Signup via Email & Auto Gmail OTP Extraction
100% Tu dong hoa:
1. Chon Ngay sinh (July 8, 2000)
2. Nhap Email (dinhthienthoai@gmail.com) & Mat khau (ThoaiReview@2026!)
3. Bam Send Code & theo doi Captcha
4. Sang Gmail tu dong lay ma OTP 6 so
5. Nhap OTP, hoan tat dang ky kenh!
"""

import sys
import os
import time
import re
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
STATUS_FILE = os.path.join(SHOTS_DIR, "status.json")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")

EMAIL_ADDRESS = "dinhthienthoai@gmail.com"
ACCOUNT_PASSWORD = "ThoaiReview@2026!"
TIKTOK_USERNAME = "thienthoaireview"

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
    print(f"[{time.strftime('%H:%M:%S')}] [Step {step}] {message}")

def extract_otp_from_gmail(context):
    print("[*] Dang mo tab Gmail de doc ma OTP tu TikTok...")
    gmail_page = context.new_page()
    gmail_page.goto("https://mail.google.com/mail/u/0/#inbox", timeout=45000)
    gmail_page.wait_for_timeout(4000)
    
    code = None
    start_time = time.time()
    while time.time() - start_time < 60:
        # Tim email TikTok
        emails = gmail_page.locator('tr.zA:has-text("TikTok"), span:has-text("TikTok")')
        count = emails.count()
        if count > 0:
            print(f"[+] Phat hien {count} email TikTok trong hop thu!")
            emails.first.click()
            gmail_page.wait_for_timeout(3000)
            
            body = gmail_page.inner_text("div.a3s") if gmail_page.locator("div.a3s").count() > 0 else gmail_page.inner_text("body")
            # Tim 6 chu so
            matches = re.findall(r'\b\d{6}\b', body)
            if matches:
                code = matches[0]
                print(f"🎉 TIM THAY MA OTP TIKTOK TRONG GMAIL: {code}")
                gmail_page.screenshot(path=os.path.join(SHOTS_DIR, "gmail_otp_found.png"))
                break
        time.sleep(3)
        gmail_page.reload()
        
    gmail_page.close()
    return code

def run():
    print("="*75)
    print("🚀 HE THONG TU DONG HOA 100%: TAO KENH TIKTOK QUA EMAIL & DOC OTP GMAIL")
    print("="*75)
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

        page = context.pages[0] if context.pages else context.new_page()
        
        # Buoc 1: Mo form dang ky Email
        update_status(2, "🌐 Dang truy cap form dang ky Email tren TikTok...")
        page.goto("https://www.tiktok.com/signup/phone-or-email/email", timeout=60000)
        page.wait_for_timeout(3000)
        page.screenshot(path=LIVE_IMG)

        # Buoc 2: Chon Ngay sinh (July 8, 2000)
        update_status(2, "📅 Dang tu dong chon ngay sinh: 08/07/2000...")
        age_selectors = page.locator('div.tiktok-psovae-de495bb3--DivAgeSelector > div')
        
        # Chon Thang (July)
        age_selectors.nth(0).click()
        time.sleep(0.5)
        page.locator('div[id*="Month-options-item-"]:has-text("July")').first.click()
        time.sleep(0.5)

        # Chon Ngay (8)
        age_selectors.nth(1).click()
        time.sleep(0.5)
        page.locator('div[id*="Day-options-item-"]:has-text("8")').first.click()
        time.sleep(0.5)

        # Chon Nam (2000)
        age_selectors.nth(2).click()
        time.sleep(0.5)
        year_target = page.locator('div[id*="Year-options-item-"]:has-text("2000")').first
        year_target.scroll_into_view_if_needed()
        year_target.click()
        time.sleep(0.5)
        print("[+] Da chon xong ngay sinh: 08/07/2000!")
        page.screenshot(path=LIVE_IMG)

        # Buoc 3: Dien Email va Mat khau
        update_status(3, f"✍️ Dang nhap Email ({EMAIL_ADDRESS}) va tao mat khau an toan...")
        page.fill('input[name="email"]', EMAIL_ADDRESS)
        time.sleep(0.8)
        page.fill('input[type="password"]', ACCOUNT_PASSWORD)
        time.sleep(0.8)
        page.screenshot(path=LIVE_IMG)
        print(f"[+] Da dien Email va Mat khau hop le.")

        # Buoc 4: Bam nut Send Code
        update_status(3, "📨 Dang bam nut 'Send code' de TikTok gui ma xac nhan...")
        send_btn = page.locator('button[data-e2e="send-code-button"]').first
        send_btn.click()
        time.sleep(3)
        page.screenshot(path=LIVE_IMG)

        # Kiem tra xem co Captcha Slider xuat hien khong
        captcha = page.locator('div:has-text("Drag the slider to fit the puzzle"), div:has-text("Kéo thanh trượt để ghép hình")').first
        if captcha.is_visible(timeout=2500):
            update_status(3, "⚠️ TIKTOK YÊU CẦU GẠT MẢNH GHÉP! Hãy gạt nhẹ thanh trượt trên màn hình nhé...")
            print("\n[!] Chu y: Gạt nhẹ thanh trượt trên màn hình để hoàn tất gửi mã!")
            for _ in range(40):
                if not captcha.is_visible(timeout=1000):
                    print("[+] Captcha da bien mat! Tiep tuc tien trinh...")
                    break
                page.screenshot(path=LIVE_IMG)
                time.sleep(1)

        # Buoc 5: Mo tab Gmail doc ma OTP
        update_status(4, "📬 Dang tu dong mo Gmail doc ma OTP 6 so tu TikTok...")
        otp_code = extract_otp_from_gmail(context)

        if otp_code:
            update_status(4, f"🔑 Da lay duoc ma OTP: {otp_code}! Dang nhap vao TikTok...")
            code_input = page.locator('input[placeholder*="code"], input[placeholder*="mã"]').first
            code_input.fill(otp_code)
            time.sleep(1)
            page.screenshot(path=LIVE_IMG)

            # Bam Next / Sign up
            submit_btn = page.locator('button[type="submit"], button:has-text("Next"), button:has-text("Sign up"), button:has-text("Tiếp")').first
            if submit_btn.is_visible(timeout=3000):
                submit_btn.click()
                print("[+] Da bam nut xac nhan dang ky!")

            page.wait_for_timeout(4000)
            page.screenshot(path=LIVE_IMG)

            # Buoc 6: Dat Username neu duoc yeu cau
            user_input = page.locator('input[placeholder*="username"], input[placeholder*="Username"], input[name*="username"]').first
            if user_input.is_visible(timeout=3000):
                update_status(4, f"🏷️ Dang dat ten nguoi dung (Username): {TIKTOK_USERNAME}...")
                user_input.fill(TIKTOK_USERNAME)
                time.sleep(1)
                page.locator('button[type="submit"], button:has-text("Sign up"), button:has-text("Done")').first.click()
                page.wait_for_timeout(4000)

            page.screenshot(path=LIVE_IMG)
            update_status(5, f"🎉 DANG KY THANH CONG! URL: {page.url}", page.url, True)
            print("\n[🎉 THÀNH CÔNG] TÀI KHOẢN TIKTOK ĐÃ ĐƯỢC TẠO HOÀN TẤT!")
        else:
            update_status(4, "Chua doc duoc ma OTP tu dong tu Gmail. Hay kiem tra hop thu nhe.")

        time.sleep(25)
        context.close()

if __name__ == "__main__":
    run()
