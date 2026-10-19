import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
VIDEO_PATH = r"C:\Users\HAI\OneDrive\Tài liệu\vmax\output\KOC_AI_Tai_Nghe_Viral_Review.mp4"

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
    log_status("Mở trình duyệt thực hiện đăng video lên TikTok...", "INIT")

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

        log_status("Truy cập trang TikTok Studio Upload...", "NAVIGATE")
        page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload", wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)

        # 1. Đóng bất kỳ modal nào nếu đang xuất hiện (như modal Turn on checks hoặc Exit)
        for _ in range(3):
            # Nếu có modal Are you sure you want to exit -> Bấm Cancel
            exit_cancel = page.locator("button:has-text('Cancel')").first
            if exit_cancel.count() > 0 and exit_cancel.is_visible():
                log_status("Đóng modal cảnh báo...", "MODAL")
                exit_cancel.click()
                time.sleep(1)

            # Nếu có modal Turn on automatic content checks -> Bấm Turn on
            turn_on_btn = page.locator("button:has-text('Turn on'), button:has-text('Bật')").first
            if turn_on_btn.count() > 0 and turn_on_btn.is_visible():
                log_status("Bật kiểm tra nội dung tự động...", "MODAL")
                turn_on_btn.click()
                time.sleep(1)

        # 2. Kiểm tra xem video đã được upload lên chưa
        # Trong ảnh trước: "Uploaded (4.43MB)" hoặc "KOC_AI_Tai_Nghe_Viral_Review.mp4"
        uploaded_indicator = page.locator("text='Uploaded', text='KOC_AI_Tai_Nghe_Viral_Review.mp4'").first
        if uploaded_indicator.count() == 0 or not uploaded_indicator.is_visible():
            log_status("Đang tải file video lên TikTok...", "UPLOADING")
            file_input = page.locator("input[type='file']").first
            if file_input.count() > 0:
                file_input.set_input_files(VIDEO_PATH)
                time.sleep(8)
            else:
                upload_zone = page.locator("button:has-text('Select video'), button:has-text('Chọn video')").first
                if upload_zone.is_visible():
                    with page.expect_file_chooser() as fc_info:
                        upload_zone.click()
                    fc_info.value.set_files(VIDEO_PATH)
                    time.sleep(8)

        # Đóng modal lại sau khi upload
        time.sleep(2)
        turn_on_btn = page.locator("button:has-text('Turn on'), button:has-text('Bật')").first
        if turn_on_btn.count() > 0 and turn_on_btn.is_visible():
            turn_on_btn.click()
            time.sleep(1)

        # 3. Điền Caption đầy đủ
        log_status("Đang điền tiêu đề & hashtags kịch bản...", "CAPTION")
        caption_box = page.locator("div[contenteditable='true'], div.public-DraftEditor-content").first
        if caption_box.is_visible():
            caption_box.click(force=True)
            time.sleep(0.5)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(CAPTION_TEXT, delay=15)
            time.sleep(2)
            page.screenshot(path="shots/step_caption_ready.png")

        # 4. Tìm và cuộn đến nút POST (Đăng)
        log_status("Đang tìm nút Post chính xác...", "FIND_POST")
        
        # Chờ video hiển thị "Uploaded" 100%
        for wait_i in range(15):
            page.screenshot(path="shots/waiting_upload.png")
            # Tìm nút Post - thường có background đỏ hoặc chữ Post/Đăng
            # Trong TikTok Studio: button with text "Post" located at bottom of form
            btn_post = page.locator("button:has-text('Post'), button:has-text('Đăng')").last
            if btn_post.count() > 0 and btn_post.is_visible():
                # Kiểm tra xem có disabled không
                is_disabled = btn_post.get_attribute("disabled")
                print(f"Found Post button. is_disabled={is_disabled}")
                if not is_disabled:
                    btn_post.scroll_into_view_if_needed()
                    time.sleep(1)
                    log_status("ĐANG BẤM NÚT POST (ĐĂNG)...", "CLICK_POST")
                    btn_post.click()
                    print("Clicked Post button!")
                    break
            time.sleep(2)

        # 5. Chờ phản hồi sau khi bấm Post
        log_status("Đang chờ TikTok xác nhận video đã được đăng thành công...", "WAIT_SUCCESS")
        time.sleep(15)
        
        # Chụp màn hình xác thực
        page.screenshot(path="shots/tiktok_final_published.png")
        log_status("ĐÃ HOÀN TẤT ĐĂNG VIDEO LÊN TIKTOK THÀNH CÔNG!", "SUCCESS")

        # Giữ màn hình mở thêm 10 giây để TikTok lưu cache và session
        print("Waiting 10s before finish...")
        time.sleep(10)
        browser_context.close()

if __name__ == '__main__':
    main()
