"""
Auto-Update TikTok Profile Name & Bio
Cập nhật tên kênh thành: Thiên Thoại Review
Bio: Chàng trai thẩm đồ nữ - Review có tâm, gu có tầm 👗✨
"""

import sys
import os
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_DIR = os.environ.get("BROWSER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"))
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")
LIVE_IMG = os.path.join(SHOTS_DIR, "live.png")

NEW_NAME = "Gobi Boutique | Gu Nàng Thơ 🌷"
NEW_BIO = "🌷 Gobi | 1m62-48kg ✨ Gobi Boutique 👗 Phối đồ hack dáng 👇 Săn deal ở giỏ hàng!"

def run():
    print("="*70)
    print("🚀 TU DONG CAP NHAT PROFILE TIKTOK: TIEU SU & TEN KENH")
    print("="*70)
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
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
        page = browser.pages[0] if browser.pages else browser.new_page()
        print("[*] Dang mo trang ca nhan https://www.tiktok.com/@tis.decor ...")
        page.goto("https://www.tiktok.com/@tis.decor", timeout=45000)
        page.wait_for_timeout(4000)
        page.screenshot(path=LIVE_IMG)
        
        # Bam nut Edit profile
        edit_btn = page.locator('button:has-text("Edit profile")').first
        if edit_btn.is_visible(timeout=5000):
            print("[+] Da tim thay nut 'Edit profile'! Dang nhap...")
            edit_btn.click()
            page.wait_for_timeout(2500)
            page.screenshot(path=LIVE_IMG)
            
            # Doi ten Name
            name_input = page.locator('input[placeholder*="Name"], div[class*="edit"] input').first
            if name_input.is_visible(timeout=3000):
                print(f"[+] Cap nhat ten hien thi: {NEW_NAME}")
                name_input.click()
                name_input.fill("")
                name_input.fill(NEW_NAME)
                time.sleep(1)
                
            # Doi Bio
            bio_area = page.locator('textarea[placeholder*="Bio"], div[class*="edit"] textarea').first
            if bio_area.is_visible(timeout=3000):
                print(f"[+] Cap nhat tieu su Bio: {NEW_BIO[:40]}...")
                bio_area.click()
                bio_area.fill("")
                bio_area.fill(NEW_BIO)
                time.sleep(1)
                
            page.screenshot(path=LIVE_IMG)
            
            # Bam nut Save
            save_btn = page.locator('button:has-text("Save"), button:has-text("Lưu")').first
            if save_btn.is_visible(timeout=3000):
                save_btn.click()
                print("[+] Da bam nut Save cap nhat profile!")
                page.wait_for_timeout(2000)
                
            # Bam Confirm neu co popup "Set nickname?"
            confirm_btn = page.locator('button:has-text("Confirm"), button:has-text("Xác nhận")').first
            if confirm_btn.is_visible(timeout=3000):
                confirm_btn.click()
                print("[+] Da bam nut Confirm xac nhan doi ten!")
                page.wait_for_timeout(4000)
                
            page.reload()
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(SHOTS_DIR, "tiktok_profile_updated.png"))
            page.screenshot(path=LIVE_IMG)
            print("🎉 CAP NHAT PROFILE TIKTOK THANH CONG!")
        else:
            print("[-] Khong tim thay nut Edit profile tren trang.")
            
        browser.close()

if __name__ == "__main__":
    run()
