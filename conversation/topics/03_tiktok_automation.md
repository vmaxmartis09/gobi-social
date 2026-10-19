# 🤖 TOPIC 03: TIKTOK SHOP AUTOMATION & STEALTH BROWSER BOT
> **Tổng hợp chuyên đề:** Trình duyệt tự động hóa tàng hình (Playwright + CDP), cơ chế vượt Anti-Bot, xử lý Google OAuth Popup, giải Captcha và đăng video lên kênh.

---

## 1. MỤC ĐÍCH & Ý NGHĨA TRONG BỨC TRANH VMAX
* Loại bỏ thao tác thủ công khi đăng tải video hàng ngày, giúp phân phối nội dung đều đặn vào các khung giờ vàng.
* Duy trì session đăng nhập vĩnh viễn trên profile trình duyệt thực tế, không bị checkpoint hoặc văng tài khoản.
* Tự động phản hồi hoặc hỗ trợ giải Captcha trượt mà không làm đứt gãy luồng xử lý của hệ thống.

---

## 2. KIẾN TRÚC TỰ ĐỘNG HÓA TRÌNH DUYỆT (BROWSER ARCHITECTURE)

### 2.1. Quản lý Profile & Kết nối CDP
* **Chrome Profile thực:** Được cấu hình tại ` hoặc qua cổng **Chrome DevTools Protocol (CDP)** tại `http://localhost:9222`.
* **Cờ khởi chạy chống phát hiện bot (Stealth Flags):**
  * `--disable-blink-features=AutomationControlled`
  * `--no-first-run`
  * `--no-default-browser-check`
* **Quy chuẩn Headed Mode:** Luôn ưu tiên chạy giao diện trực tiếp trên màn hình đối với TikTok/Google để giảm thiểu tỷ lệ kích hoạt hệ thống bảo mật Cloudflare / TikTok Shield.

### 2.2. Xử lý Google OAuth & Đa cửa sổ Popup
* Khi click vào nút "Continue with Google":
  * Lắng nghe sự kiện mở popup bằng `context.expect_page()`.
  * Tự động định vị tài khoản `dinhthienthoai@gmail.com` và nhấn tiếp tục.
  * Tự động chuyển ngữ cảnh về lại tab TikTok chính sau khi popup hoàn tất.

### 2.3. Giải Captcha & Theo dõi trực quan qua Live Viewer
* **Xử lý Captcha:** [`affiliate_tiktok/handle_tiktok_captcha.py`](../../affiliate_tiktok/handle_tiktok_captcha.py).
  * Chụp ảnh toàn cảnh và ảnh mảnh ghép puzzle.
  * Tự động tính toán khoảng cách offset x để kéo thanh trượt mô phỏng gia tốc tay người thật (human-like mouse drag).
* **Giao diện giám sát Live Viewer:**
  * File HTML: [`live_viewer.html`](../../live_viewer.html)
  * File dữ liệu trạng thái: [`shots/status.json`](../../shots/status.json)
  * Giúp người dùng quan sát từng bước bot đang click, đang upload hoặc đang chờ lệnh mà không cần nhìn vào terminal.

---

## 3. CÁC FILE LIÊN QUAN CHÍNH
* [`upload_to_tiktok.py`](../../upload_to_tiktok.py) & [`publish_tiktok.py`](../../publish_tiktok.py)
* [`affiliate_tiktok/full_verified_login.py`](../../affiliate_tiktok/full_verified_login.py)
* [`affiliate_tiktok/execute_tiktok_flow.py`](../../affiliate_tiktok/execute_tiktok_flow.py)
* [`core/stealth_monitor.py`](../../core/stealth_monitor.py)
