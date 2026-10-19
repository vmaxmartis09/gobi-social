# 📝 TÓM TẮT PHIÊN LÀM VIỆC - SESS-011: CHUẨN HÓA KOC MASTER DNA & SẢN XUẤT VIDEO MẪU GOBI THÚI 9S
> **Thời gian:** 2026-10-18  
> **Người thực hiện:** Người dùng & Antigravity AI  
> **Phân hệ chính:** `[KOC AI] | [Video Engine] | [Voice & Audio]`  
> **Trạng thái:** ✅ Hoàn thành xuất sắc

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Vấn đề đặt ra:**
  1. Người dùng yêu cầu tinh chỉnh gương mặt người mẫu ban đầu (`Mauz`): mặt thanh tú hơn, mũi cao thon gọn hơn, kết hợp khí chất điện ảnh của Trương Bá Chi & Lưu Diệc Phi nhưng vẫn giữ trọn nhận diện người mẫu gốc.
  2. Đồng nhất tuyệt đối ma trận 36 góc chụp (`ethereal_koc_panels_v3/`) với ảnh gốc chuẩn đã duyệt [`MASTER_KOC_DNA.jpg`](../../affiliate_tiktok/dataset_koc/MASTER_KOC_DNA.jpg).
  3. Đọc hiểu và phân tích video TikTok hướng dẫn làm giọng nói AI từ kênh `@benaithucchien` để đánh giá giá trị ứng dụng.
  4. Sản xuất video mẫu chuẩn 9 giây: KOC Gobi Thúi nói câu *"hello ông kẹ em là Gobi thúi của anh đây!"* sử dụng hình ảnh KOC chuẩn và giọng đọc tiếng Việt đã được chuẩn hóa trong dự án.

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI
* **Các file code đã tạo hoặc chỉnh sửa:**
  * [`affiliate_tiktok/render_gobi_sample_video.py`](../../affiliate_tiktok/render_gobi_sample_video.py): Engine render video 9s chuẩn TikTok (1080x1920, 30fps), tích hợp Super-sampling 2x Lanczos (1536x2752), chuyển động camera điện ảnh 3 phân cảnh (Hook greeting -> OOTD showcase -> Emotional close-up), phụ đề Frosted Glass pill động chuẩn TikTok Safe Zone.
  * [`affiliate_tiktok/gen_gobi_voice.py`](../../affiliate_tiktok/gen_gobi_voice.py): Script tạo giọng đọc tiếng Việt tự nhiên `vi-VN-HoaiMyNeural` (-2% rate) độ dài 8.69s.
  * [`affiliate_tiktok/rebuild_master_36_panels.py`](../../affiliate_tiktok/rebuild_master_36_panels.py): Script điêu khắc tọa độ vi mô (Diffeomorphic Facial Sculpting) tái thiết kế toàn bộ 36 panel góc quay chuẩn 100% Master DNA.
  * [`affiliate_tiktok/download_tiktok_native.py`](../../affiliate_tiktok/download_tiktok_native.py): Tải video trực tiếp từ link TikTok `@benaithucchien`.
  * [`affiliate_tiktok/capture_benaithucchien_frames.py`](../../affiliate_tiktok/capture_benaithucchien_frames.py): Bóc tách âm thanh và 72 khung hình để phân tích giao diện công nghệ.
  * [`affiliate_tiktok/analyze_benaithucchien_video.py`](../../affiliate_tiktok/analyze_benaithucchien_video.py): Đọc hiểu toàn diện nền tảng giọng nói AI (EverAI v1.6).

* **Lệnh terminal thực thi chính:**
  ```powershell
  # 1. Tái dựng ma trận 36 góc
  & ".\.venv\Scripts\python.exe" affiliate_tiktok/rebuild_master_36_panels.py
  # 2. Sinh voiceover 9s
  & ".\.venv\Scripts\python.exe" affiliate_tiktok/gen_gobi_voice.py
  # 3. Render video TikTok 9s
  & ".\.venv\Scripts\python.exe" affiliate_tiktok/render_gobi_sample_video.py
  ```

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
1. **Video mẫu 9 giây hoàn chỉnh (Deliverable cốt lõi):**
   * File video thành phẩm: [`affiliate_tiktok/sample_video/output/gobi_thui_koc_9s.mp4`](../../affiliate_tiktok/sample_video/output/gobi_thui_koc_9s.mp4) (3.91 MB, 1080x1920, 30 FPS, đúng 9.0 giây).
   * File âm thanh hoàn chỉnh: [`affiliate_tiktok/sample_video/audio/gobi_thui_9s.mp3`](../../affiliate_tiktok/sample_video/audio/gobi_thui_9s.mp3) (8.69s, hòa âm với BGM nhẹ nhàng -18dB).
   * Ảnh trích xuất thực tế (Proof-of-work):
     * Cảnh 1 (Hook): [`shots/gobi_frames/v2_frame_intro.jpg`](../../shots/gobi_frames/v2_frame_intro.jpg)
     * Cảnh 2 (OOTD): [`shots/gobi_frames/v2_frame_ootd.jpg`](../../shots/gobi_frames/v2_frame_ootd.jpg)
     * Cảnh 3 (Outro): [`shots/gobi_frames/v2_frame_outro.jpg`](../../shots/gobi_frames/v2_frame_outro.jpg)
2. **Bộ dữ liệu 36 góc chụp đồng nhất 100%:**
   * 36 panel kích thước 512x512 tại thư mục [`affiliate_tiktok/dataset_koc/ethereal_koc_panels_v3/`](../../affiliate_tiktok/dataset_koc/ethereal_koc_panels_v3).
   * Storyboard tổng hợp 6x6 (3072x3072): [`affiliate_tiktok/dataset_koc/ethereal_koc_36_storyboard_v3.jpg`](../../affiliate_tiktok/dataset_koc/ethereal_koc_36_storyboard_v3.jpg).
   * File chỉ mục góc quay: [`manifest.json`](../../affiliate_tiktok/dataset_koc/ethereal_koc_panels_v3/manifest.json).
3. **Phân tích công nghệ video `@benaithucchien`:**
   * Video & âm thanh phân tích: [`shots/benaithucchien_full.mp4`](../../shots/benaithucchien_full.mp4).
   * Kết quả: Xác định nền tảng **EverAI** (`everai.vn` / model `Everai v1.6`) chuyên clone giọng tức thời 2-60s tiếng Việt, dùng để mở rộng thêm tùy chọn voice clone bên cạnh Edge-TTS.

---

## 🧠 4. BÀI HỌC KINH NGHIỆM ĐÚC KẾT ĐƯỢC
* **Khóa nhận diện KOC trong video (Super-sampling vs Face-cut):** Không nên cắt ghép nhiều ảnh khác thời điểm tạo gây cảm giác biến đổi mặt. Dùng ảnh chuẩn Master DNA kích thước lớn (1536x2752) kết hợp kỹ thuật camera motion (zoom, pan, tilt) giúp người mẫu giữ nguyên 100% đường nét sống mũi cao, cằm V-line và trang phục từ đầu đến cuối video.
* **Xử lý Typography & Safe Zone:** Khi render phụ đề dạng pill trong PIL, cần tính toán độ dài chuỗi ký tự động (`draw.textbbox`) để card tự căn chỉnh lề, và loại bỏ emoji thô khỏi font hệ thống để tránh lỗi ô vuông ký tự `[]`. Đặt phụ đề ở `y = 1380` nằm trọn trong TikTok Safe Zone phía trên nút Giỏ hàng.
* **Cân bằng hòa âm (Audio Ducking):** Giảm âm lượng nhạc nền BGM xuống `-18dB` khi có giọng thoại và tự động fade-out ở 1 giây cuối cùng mang lại trải nghiệm chuyên nghiệp, thu hút người xem trong 3 giây đầu tiên.

---

## ⏭️ 5. BƯỚC TIẾP THEO (NEXT ACTIONS)
- [ ] Tích hợp kịch bản video 9s vào quy trình tự động hóa sản xuất video Affiliate hàng loạt (`affiliate_tiktok/video_pipeline.py`).
- [ ] Thử nghiệm kết hợp API/Browser Automation với EverAI hoặc F5-TTS để nhân bản giọng đọc cá nhân hóa cho KOC Gobi Thúi.
- [ ] Đẩy video `gobi_thui_koc_9s.mp4` lên kênh TikTok thông qua quy trình tự động đăng bài đã xây dựng trong SESS-005.
