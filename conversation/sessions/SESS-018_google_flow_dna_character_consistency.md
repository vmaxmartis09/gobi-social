# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-018
> **Tiêu đề phiên:** Rà soát bức tranh Video Affiliate, kiểm tra Google Flow trên Ego Lite, chuẩn hóa DNA Master Gô Bi chống trôi khuôn mặt / dáng người / da tóc qua nhiều video  
> **Thời gian:** 2026-10-20  
> **Người thực hiện:** Người dùng & AI Assistant (Antigravity)  
> **Phân hệ chính:** `[KOC AI] | [Google Flow / Ego Lite] | [Video Engine] | [Master DNA]`  
> **Trạng thái:** Hoàn thành ✅  

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Yêu cầu người dùng:**
  1. Xem nhanh bức tranh dự án làm video affiliate KOC AI, tập trung vào pipeline Google Flow (`flow.google.com`).
  2. Đánh giá setup nhân vật hiện tại: Đã có nhân vật rồi thì cần bổ sung những gì để sau nhiều video khác nhau, nhân vật không bao giờ bị đổi khuôn mặt, dáng người, làn da và mái tóc.
  3. Mở trình duyệt Ego Lite, kiểm tra thực tế Studio Google Flow; nếu chưa chuẩn thì setup lại nhân vật với kho DNA Master có sẵn.

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI
1. **Kiểm tra hiện trạng hệ thống Ego Lite & Google Flow:**
   - Mở Ego Lite truy cập `https://flow.google.com` (Tài khoản Google: Đinh Thiên Thoại `dinhthienthoai@gmail.com`).
   - Rà soát các dự án đang hoạt động:
     - `97437688-2b73-4a07-9091-77969b802e73` (Dự án chính đang tạo nhân vật & video Gobi).
     - `3216ade9-8f46-4a7b-bf2a-695e49698f15`.
   - Phát hiện điểm nghẽn nghiêm trọng trong thiết lập nhân vật:
     - Trong mục **"Nhân vật" > Gobi KOC**, trường mô tả tính cách vĩnh viễn (`personality-textarea`) bị gán cứng trang phục và hành động của một video đơn lẻ:
       *Cũ:* `"Gobi, cô gái KOC thời trang Việt Nam 22 tuổi, mặc chiếc áo thun ôm dài tay màu xám tiêu NEAU NuNu NU221, mỉm cười rạng rỡ với camera, nhẹ nhàng dùng tay kéo nhẹ mép cổ áo..."*
     - **Hậu quả:** Khi sinh các video tiếp theo về Áo cardigan, Đầm lụa, Quần suông... Google Flow sẽ bị xung đột token giữa áo xám tiêu trong DNA và áo mới trong kịch bản, dẫn đến biến dạng trang phục và trôi dạt nhân vật (character drift).

2. **Khắc phục và Setup lại DNA Bất biến (Invariant Master DNA):**
   - Truy cập vào Character Editor của `Gobi KOC` trên Google Flow qua script Node.js Ego Lite (`scratch/update_gobi_dna_flow.mjs`).
   - Cập nhật trường mô tả vĩnh viễn thành bộ từ khóa giải phẫu hình thể & nhân trắc học bất biến từ kho Master DNA (`assets/datasets/koc/gobi_profile_36/`):
     *Mới:* `"Gobi, nữ KOC thời trang Việt Nam 22 tuổi. Gương mặt trái xoan thanh tú, mắt hạnh nhân hai mí tự nhiên sáng ngời, sống mũi cao thẳng thon gọn, môi cánh cung mềm mại rạng rỡ. Chiều cao 1m62, nặng 49kg, vóc dáng thon thả chuẩn người mẫu thời trang lookbook. Làn da trắng sứ mịn màng bắt sáng studio tự nhiên, mái tóc đen tuyền suôn mượt buông xõa vai. Thần thái thanh lịch, hiện đại phong cách Quiet Luxury, chi tiết chân thực chuẩn 8K điện ảnh."*
   - Lưu thành công bằng nút "Xong" và xác thực qua ảnh chụp màn hình `shots/ego_gobi_dna_updated_verified.png`.

3. **Kiểm tra tiến độ & Thu hoạch Video Render từ Google Flow:**
   - Kiểm tra media gallery trong Studio Google Flow: Video Cảnh 1 (8 giây) đã render hoàn tất 100%.
   - Tải video gốc về máy: `output/flow_gobi_test_8s.mp4` (dung lượng 3.5MB, chuẩn 720x1280 9:16 dọc, 24fps).
   - Trích xuất frame kiểm thử: `shots/flow_video_frame_2s.jpg`.

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
* **Video đầu ra từ Google Flow:** [`output/flow_gobi_test_8s.mp4`](../../output/flow_gobi_test_8s.mp4) (8s, 720x1280, 24fps).
* **Ảnh chụp màn hình Studio Google Flow:**
  - Trang chủ Flow: [`shots/ego_flow_home_review.png`](../../shots/ego_flow_home_review.png)
  - Chi tiết Character Editor trước khi sửa: [`shots/ego_gobi_char_editor_full.png`](../../shots/ego_gobi_char_editor_full.png)
  - Xác nhận đã cập nhật DNA chuẩn hóa: [`shots/ego_gobi_dna_updated_verified.png`](../../shots/ego_gobi_dna_updated_verified.png)
  - Trạng thái thư viện media hoàn tất: [`shots/ego_flow_media_gallery_status.png`](../../shots/ego_flow_media_gallery_status.png)
  - Frame video thực tế 2s: [`shots/flow_video_frame_2s.jpg`](../../shots/flow_video_frame_2s.jpg)

---

## 🧠 4. BÀI HỌC KINH NGHIỆM ĐÚC KẾT (CHỐNG TRÔI NHÂN VẬT 100%)
Để nhân vật giữ nguyên 100% khuôn mặt, dáng người, làn da, mái tóc qua hàng trăm video:
1. **Quy tắc 3 Tầng Prompt Độc lập (Prompt Separation):**
   - *Tầng 1 (Frozen Character DNA):* Khóa trong Personality (Mặt, mắt, mũi, môi, da, tóc, chiều cao, cân nặng). Không chứa quần áo hay động tác.
   - *Tầng 2 (Scene Prompt):* Quần áo theo video, hành động theo kịch bản (xoay người, đưa tay vuốt tóc, giới thiệu sản phẩm).
   - *Tầng 3 (Style & Safe Zone):* Tỷ lệ 9:16, ống kính 50mm, ánh sáng Lookbook, không giật hình.
2. **Khóa chặt Visual Anchor:** Luôn dùng ảnh chuẩn từ `assets/datasets/koc/gobi_profile_36/` (`00_MASTER_DNA_ANCHOR.jpg` và `gobi_angle_07_full_body_standing.jpg`) làm tham chiếu đầu vào.
3. **Chốt chặn hậu kỳ:** Kết hợp pipeline LivePortrait / ReActor Face-Sync làm fail-safe nếu có micro-drift ở các góc xoay khó.
