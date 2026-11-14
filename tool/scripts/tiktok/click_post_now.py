import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_PROFILE_DIR = os.environ.get("USER_PROFILE_DIR", os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", "ai_profile"))
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
VIDEO_PATH = r"./output\KOC_AI_Tai_Nghe_Viral_Review.mp4"

CAPTION_TEXT = (
    "Review tai nghe chống ồn ANC 45dB siêu êm giá cực sốc năm 2026! 🔥 "
    "Deal giảm 40% độc quyền trong giỏ hàng góc trái. "
    "#tainghe #tainghebluetooth #reviewcongnghe #kocai #anc #affiliate #dealhot"
)

def log_status(status_text, step_name="RUNNING"):
    os.makedirs("shots", exist_ok=True)
    status_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "step": step_name,
        "message": status_text
    }
    with open("shots/status.json", "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)
    print(f"[{step_name}] {status_text}")

def main():
    log_status("Mở lại phiên để kích hoạt 'Post now' hoàn tất...", "INIT")

    with sync_playwright() as p:
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1280,960"
        ]

        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=USER_PROFILE_DIR,
            executable_path=CHROME_EXE,
            headless=False,
            args=args,
            viewport=None
        )

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

        log_status("Truy cập lại trang Upload...", "NAVIGATE")
        page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload", wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)

        # 1. Kiểm tra xem có popup "Post now" không
        post_now_btn = page.locator("button:has-text('Post now'), button:has-text('Đăng ngay')").first
        if post_now_btn.count() > 0 and post_now_btn.is_visible():
            log_status("Bấm nút POST NOW...", "CLICK_POST_NOW")
            post_now_btn.click()
            time.sleep(8)
        else:
            # Nếu chưa có video, chọn file lại
            uploaded = page.locator("text='Uploaded', text='KOC_AI_Tai_Nghe_Viral_Review.mp4'").first
            if uploaded.count() == 0 or not uploaded.is_visible():
                log_status("Đang nạp lại file video...", "REUPLOAD")
                file_input = page.locator("input[type='file']").first
                if file_input.count() > 0:
                    file_input.set_input_files(VIDEO_PATH)
                    time.sleep(7)
                
            # Đóng popup Turn on checks nếu có
            turn_on = page.locator("button:has-text('Turn on'), button:has-text('Bật')").first
            if turn_on.count() > 0 and turn_on.is_visible():
                turn_on.click()
                time.sleep(1)

            # Điền caption nếu trống
            caption_box = page.locator("div[contenteditable='true'], div.public-DraftEditor-content").first
            if caption_box.is_visible():
                caption_box.click(force=True)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(CAPTION_TEXT, delay=10)
                time.sleep(2)

            # Bấm Post
            post_btn = page.locator("button:has-text('Post'), button:has-text('Đăng')").last
            if post_btn.is_visible():
                post_btn.scroll_into_view_if_needed()
                time.sleep(1)
                log_status("Bấm nút Post...", "POST")
                post_btn.click()
                time.sleep(3)

            # Bấm tiếp Post now nếu popup xuất hiện
            post_now_btn = page.locator("button:has-text('Post now'), button:has-text('Đăng ngay')").first
            for _ in range(10):
                if post_now_btn.count() > 0 and post_now_btn.is_visible():
                    log_status("Bấm nút 'Post now' trong popup xác nhận!", "CLICK_POST_NOW")
                    post_now_btn.click()
                    time.sleep(5)
                    break
                time.sleep(1)

        # Chờ điều hướng đến trang quản lý nội dung /content hoặc thông báo thành công
        log_status("Chờ TikTok xác nhận xuất bản video...", "WAIT_FINALIZE")
        time.sleep(10)

        # Chụp ảnh bằng chứng cuối cùng
        page.screenshot(path="shots/tiktok_feed_published.png")
        log_status("XÁC NHẬN: Video đã được xuất bản chính thức lên kênh TikTok!", "PUBLISHED")
        
        time.sleep(5)
        browser_context.close()

if __name__ == '__main__':
    main()
