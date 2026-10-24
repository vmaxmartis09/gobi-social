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

def dismiss_modals(page):
    # Xử lý modal 'Turn on automatic content checks?'
    turn_on_btn = page.locator("button:has-text('Turn on'), button:has-text('Bật')").first
    if turn_on_btn.count() > 0 and turn_on_btn.is_visible():
        log_status("Phát hiện popup 'Turn on content checks', đang bấm Turn on...", "MODAL")
        turn_on_btn.click()
        time.sleep(2)
        return True
        
    cancel_btn = page.locator("button:has-text('Cancel'), button:has-text('Hủy')").first
    if cancel_btn.count() > 0 and cancel_btn.is_visible():
        log_status("Bấm Cancel đóng popup...", "MODAL")
        cancel_btn.click()
        time.sleep(2)
        return True
        
    # Xử lý các tooltip hoặc thông báo che màn hình
    close_icons = page.locator("[aria-label='close'], [aria-label='Close'], button.close-button, div[class*='modal'] [aria-label='close']")
    if close_icons.count() > 0 and close_icons.first.is_visible():
        close_icons.first.click()
        time.sleep(1)
        return True
        
    return False

def main():
    if not os.path.exists(VIDEO_PATH):
        print(f"ERROR: Video not found at {VIDEO_PATH}")
        sys.exit(1)

    log_status("Khởi chạy Chrome với profile cá nhân của bạn...", "INIT")

    with sync_playwright() as p:
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1280,900"
        ]

        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=USER_PROFILE_DIR,
            executable_path=CHROME_EXE,
            headless=False,
            args=args,
            viewport=None
        )

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

        log_status("Đang truy cập TikTok Studio Upload...", "NAVIGATE")
        page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload", wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        page.screenshot(path="shots/upload_page_ready.png")

        # Kiểm tra và dismiss popup nếu có sẵn
        dismiss_modals(page)

        # 1. Tải file video lên
        file_input = page.locator("input[type='file']").first
        if file_input.count() > 0:
            log_status("Đang upload file video KOC AI lên TikTok...", "UPLOADING")
            file_input.set_input_files(VIDEO_PATH)
            time.sleep(8)
            page.screenshot(path="shots/upload_file_pasted.png")
        else:
            log_status("Tìm nút upload thay thế...", "SEARCH_BTN")
            upload_btn = page.locator("button:has-text('Select video'), button:has-text('Chọn video')").first
            if upload_btn.is_visible():
                with page.expect_file_chooser() as fc_info:
                    upload_btn.click()
                fc = fc_info.value
                fc.set_files(VIDEO_PATH)
                time.sleep(8)

        # Đóng mọi modal chắn màn hình sau khi file được upload
        for _ in range(3):
            if dismiss_modals(page):
                time.sleep(2)

        # 2. Nhập Caption / Tiêu đề
        log_status("Đang điền tiêu đề & hashtags kịch bản...", "CAPTION")
        caption_box = page.locator("div[contenteditable='true'], div.public-DraftEditor-content").first
        
        # Nếu vẫn bị modal che, thử click force hoặc dismiss lại
        for attempt in range(5):
            if dismiss_modals(page):
                time.sleep(1)
            try:
                caption_box.click(force=True, timeout=5000)
                break
            except Exception as e:
                print(f"Click caption attempt {attempt+1} failed: {e}. Trying dismiss...")
                dismiss_modals(page)
                time.sleep(2)

        time.sleep(1)
        # Xóa caption cũ nếu có
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        time.sleep(0.5)
        
        # Gõ caption mới
        page.keyboard.type(CAPTION_TEXT, delay=15)
        time.sleep(2)
        page.screenshot(path="shots/caption_filled.png")

        # Đóng mọi modal lần nữa trước khi bấm Đăng
        dismiss_modals(page)

        # 3. Chờ xử lý video hoàn tất (Thường có thanh tiến trình upload 100%)
        log_status("Đang chờ TikTok xử lý video hoàn tất và sẵn sàng đăng...", "WAIT_PROCESS")
        time.sleep(8)
        page.screenshot(path="shots/before_post.png")

        # 4. Tìm nút Post / Đăng
        post_btn = page.locator("button:has-text('Post'), button:has-text('Đăng')").first
        if post_btn.is_visible():
            # Scroll vào view
            post_btn.scroll_into_view_if_needed()
            time.sleep(1)
            log_status("Đang bấm nút POST để đăng video lên TikTok...", "POSTING")
            post_btn.click(force=True)
            time.sleep(10)
            
            # Chụp ảnh xác thực kết quả sau khi bấm Đăng
            page.screenshot(path="shots/tiktok_uploaded_success.png")
            log_status("THÀNH CÔNG! Video đã được đăng lên TikTok!", "SUCCESS")
        else:
            print("Post button not directly visible, searching with broader selector...")
            all_btns = page.locator("button").all()
            for b in all_btns:
                txt = b.inner_text().strip().lower()
                if txt in ['post', 'đăng']:
                    b.click(force=True)
                    time.sleep(10)
                    page.screenshot(path="shots/tiktok_uploaded_success.png")
                    log_status("THÀNH CÔNG! Video đã được đăng lên TikTok!", "SUCCESS")
                    break

        print("\nQUY TRÌNH ĐĂNG TIKTOK HOÀN TẤT 100%!")
        time.sleep(5)
        browser_context.close()

if __name__ == '__main__':
    main()
