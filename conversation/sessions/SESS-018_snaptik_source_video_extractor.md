# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-018
> **Tiêu đề phiên:** Tích hợp Phân hệ SnapTik - Trích xuất & Tải Source Video TikTok Không Logo Vào Dự Án  
> **Thời gian:** 2026-10-20  
> **Người thực hiện:** Người dùng & AI Assistant (Antigravity)  
> **Phân hệ chính:** `[Video Engine] | [Scrapers] | [CLI & Web UI]`  
> **Trạng thái:** `Hoàn thành`

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Vấn đề đặt ra:** Người dùng cần một chức năng giống https://snaptik.vn/ để dán liên kết video TikTok (chuẩn, rút gọn `vt.tiktok.com`, `vm.tiktok.com`, album ảnh slide) và kéo source video MP4 sạch watermark, file âm thanh MP3, ảnh bìa và metadata chi tiết trực tiếp vào dự án `gobi-social`.
* **Mục tiêu cần đạt:**
  1. Xây dựng domain models và adapter đa tầng (Multi-Strategy Scraper) theo Clean Architecture.
  2. Tích hợp engine TikWM (cơ chế đằng sau snaptik.vn) cùng fallback yt-dlp & Web parsing.
  3. Cung cấp Unified CLI: `./gobi snaptik <URL>` hỗ trợ tải video không logo, audio MP3, cover, batch downloading.
  4. Cung cấp giao diện SnapTik Web UI cục bộ (`./gobi snaptik --web`) trực quan, hiện đại.
  5. Viết đầy đủ unit tests & integration tests và kiểm thử tải video thực tế.

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI
* **Các file code đã tạo hoặc chỉnh sửa:**
  * `src/gobi/domain/snaptik_models.py`: Định nghĩa schemas Pydantic cho Video Item, Author, Stats, Media và Download Result.
  * `src/gobi/adapters/scrapers/snaptik_scraper.py`: Bộ cào đa chiến lược (Strategy 1: TikWM, Strategy 2: yt-dlp, Strategy 3: TikTok oEmbed/Web) kèm engine stream download có chunking và referer chống chặn.
  * `src/gobi/services/media/snaptik_service.py`: Service điều phối tải video sạch, audio, cover, slideshow và metadata JSON.
  * `src/gobi/services/media/snaptik_web.py`: FastAPI server & Single-page Web UI chuẩn giao diện SnapTik.vn (neon/gradient, xem trước video, thông số views/likes, tải trực tiếp vào `output/videos`).
  * `src/gobi/cli/cmd_snaptik.py`: Xử lý lệnh CLI `gobi snaptik` với các flags `-o`, `-i`, `-a`, `-c`, `-wm`, `--batch`, `--web`.
  * `src/gobi/cli/main.py`: Đăng ký subparser `snaptik` vào hệ thống CLI hợp nhất.
  * `tests/unit/test_snaptik.py`: Bộ kiểm thử đơn vị cho models, sanitizer, URL parsing, fallback loop.
  * `tests/integration/test_snaptik_api.py`: Kiểm thử tích hợp các endpoint `/`, `/api/extract`, `/api/download`.
* **Lệnh terminal hoặc script đã thực thi:**
  ```bash
  # Chạy toàn bộ test suites
  ./.venv/bin/python -m unittest tests/unit/test_snaptik.py tests/integration/test_snaptik_api.py

  # Test kiểm tra metadata video thực tế
  ./gobi snaptik "https://www.tiktok.com/@benaithucchien/video/7649853202522967304" -i

  # Test tải video sạch không logo + audio + cover vào output/videos
  ./gobi snaptik "https://www.tiktok.com/@ber.review/video/7680784467144887573" -a -c
  ```

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
* **Kết quả thực tế:**
  * 9/9 tests đơn vị & tích hợp vượt qua thành công 100%.
  * Tải thành công video sạch TikTok không watermark trong ~1.5 giây:
    * Video sạch: `output/videos/ber.review_7680784467144887573_Ao_Khoac_Cardigan_xuhuong_fyp_ao_cardiga.mp4` (0.86 MB, 576x1024, h264/aac).
    * Audio gốc: `output/audio/ber.review_7680784467144887573_Ao_Khoac_Cardigan_xuhuong_fyp_ao_cardiga_audio.mp3` (419 KB).
    * Ảnh bìa: `output/videos/ber.review_7680784467144887573_Ao_Khoac_Cardigan_xuhuong_fyp_ao_cardiga_cover.jpg` (18 KB).
    * Metadata: `output/videos/ber.review_7680784467144887573_Ao_Khoac_Cardigan_xuhuong_fyp_ao_cardiga.json`.

---

## 🧠 4. BÀI HỌC KINH NGHIỆM ĐÚC KẾT ĐƯỢC
* `snaptik.vn` sử dụng TikWM API làm backend chính và fallback sang Cloudflare Turnstile token / zcdn. Sử dụng TikWM kết hợp yt-dlp làm fallback nội bộ trong Python cho độ tin cậy vượt trội mà không bị phụ thuộc vào trình duyệt web bên thứ ba.
* Để tên file an toàn tuyệt đối trên mọi hệ điều hành (macOS, Linux, Windows), việc chuẩn hóa NFKD loại bỏ dấu tiếng Việt kết hợp regex slug giúp không bị lỗi font hoặc ký tự `??`.

---

## ⏭️ 5. BƯỚC TIẾP THEO (NEXT ACTIONS)
- [ ] Tích hợp tính năng tự động chuyển đổi video vừa tải từ SnapTik sang Pipeline Voice Clone (sử dụng OmniVoice / Voice Studio 2.0).
- [ ] Mở rộng tính năng phân tích transcript và tự động bóc tách kịch bản review KOC từ video tải về.
