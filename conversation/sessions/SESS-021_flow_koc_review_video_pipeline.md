# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-021
> **Tiêu đề phiên:** Quy trình làm video review Gô Bi hoàn toàn thủ công qua EGO Lite + Google Flow + HyperFrames (job Áo len tiêu Miho House)
> **Thời gian:** 2026-10-21
> **Người thực hiện:** Người dùng & Claude (trực tiếp vận hành EGO Lite, không qua dashboard)
> **Phân hệ chính:** `[KOC AI] | [Video Engine] | [Browser Bot - EGO Lite] | [Flow AI]`
> **Trạng thái:** `Hoàn thành một phần — video đã xuất, pipeline tối ưu hơn đang chờ tài khoản Flow hết bị gắn cờ`

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Vấn đề đặt ra:** Dashboard chỉ nên thống kê, không tự render. Khi cần làm video cho 1 job cụ thể, Claude phải tự vào EGO Lite điều khiển Google Flow thật để Gô Bi "diễn" đúng sản phẩm, rồi ráp lại bằng HyperFrames — không dùng Ken-Burns ảnh tĩnh, không gọi Gemini (hết quota free-tier).
* **Job cụ thể:** JOB-7694350317697142037 "Áo len tiêu Miho House" (@vananhm68), yêu cầu làm hoàn toàn từ Claude, không qua dashboard.
* **Mục tiêu cần đạt:** Video review 9:16 có Gô Bi mặc **đúng** sản phẩm thật (màu, chất liệu, kiểu dáng), giọng Gô Bi lồng tiếng, phong cách edit tự nhiên giống video gốc, không watermark AI, không chữ overlay thừa.

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI

### Quy trình tổng (end-to-end đã chạy thành công ít nhất 1 lần)
1. **Kiểm tra & vá nguồn:** `video_clean.mp4` của job bị hỏng (chỉ có audio, không có video stream) → tải lại qua `SnaptikService.download()` → thay thế file nguồn.
2. **Trích & chọn frame tham chiếu sản phẩm thật:** dùng `ffmpeg -ss <t> -frames:v 1` lấy nhiều frame từ `video_clean.mp4`, chọn frame **ánh sáng đều, không cháy sáng, không có chữ burn-in** để không làm lệch màu khi AI diễn giải (bài học quan trọng — xem mục 4).
3. **Viết kịch bản tay** (bỏ qua Gemini) dựa trên transcript Whisper thật của video gốc, giữ đúng nội dung review (chất liệu, form, cách phối đồ).
4. **Vận hành EGO Lite → Google Flow:**
   * Resume task space đã có tên cố định `"Google Flow Production"` (không tạo task space mới).
   * Vào đúng dự án Flow đã có sẵn nhân vật **"Gô Bi KOC"** (characters không global, gắn theo từng project).
   * Cài đặt: chế độ Video, 9:16, 720p, 8 giây/clip, model **Omni 1.1 Flash**.
   * Mỗi cảnh: đính kèm ảnh tham chiếu sản phẩm + nhân vật "Gô Bi KOC" vào prompt, mô tả rõ màu/chất liệu/kiểu cổ áo, gửi tạo (5 cảnh: Hook, chất liệu, form dáng, phối đồ, CTA).
   * Tải video (720p) qua menu "Tuỳ chọn khác → Tải xuống" cho từng clip.
5. **Ráp video bằng `scripts/flow_ai/assemble_flow_scenes.py`** (script mới viết, không wire vào dashboard):
   * Sinh giọng Gô Bi (`VoiceCloner`, OmniVoice, profile `voice-fm-lyly`) cho từng câu thoại.
   * Xoá watermark AI (icon ✦ góc dưới-phải của Flow/Veo) bằng crop 82% khung hình từ góc trên-trái rồi scale lại full-frame.
   * Tách mỗi clip 8s gốc thành 2 sub-cut (45%/55%) để tăng nhịp cắt (10 cut/37s thay vì 5 cut) — gần với nhịp quay/dựng thật của video gốc.
   * Bỏ hoàn toàn text overlay (tên sản phẩm + tag giỏ hàng) theo yêu cầu — chỉ còn hình ảnh + giọng.
   * Nhúng `<audio id="voiceover-audio">` đúng pattern `data-track-index` đã dùng ở `hyperframes_engine.py` để adapter mux đúng audio vào video cuối (lúc đầu quên bước này → video câm tiếng, đã fix).
   * Render qua `HyperFramesEngine.render_project()` → `generated_video.mp4`, cập nhật `product.json` (`status=DA_LAM_VIDEO`, `video_type`, `generated_via=google_flow_ego_lite`) để dashboard tự hiện qua SSE.
6. **Nén bản xem trên mobile:** `ffmpeg -c:v libx264 -b:v 4000k ... ` xuống còn ~19MB (dưới giới hạn gửi file 30MB).

### File chính đã tạo/sửa
* `scripts/flow_ai/assemble_flow_scenes.py` — viết mới, sau đó sửa 3 lần: (1) thêm `<audio>` track, (2) thêm `_dewatermark_and_trim()` + tách sub-cut, (3) bỏ hẳn text overlay.
* Job folder `data/products/7694350317697142037_.../`: `_product_ref/` (ảnh tham chiếu + bản face-swap thử nghiệm), `_flow_clips/` (5 clip gốc tải từ Flow), `_flow_assembly/` (composition HyperFrames + audio).

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
* **Video đã xuất:** [`generated_video.mp4`](../../data/products/7694350317697142037_ao_len_tieu_miho_house_tiktokshop1010_chinhha/generated_video.mp4) (37.5s, 1080x1920, có audio, không watermark, không text overlay, 10 sub-cut) — đã gửi người dùng xem qua bản nén.
* **Validate kỹ thuật thành công:** pipeline "ảnh khởi đầu khoá pixel sản phẩm" (xem mục 4) đã test ra 1 clip (`Woman smiling and tucking hair`) giữ **chính xác 100%** màu/chất liệu/phụ kiện trang phục trong suốt 8 giây — chứng minh hướng đi đúng, nhưng chưa áp dụng được hết 5 cảnh do bị Flow chặn (xem mục 4).
* **Trạng thái job:** `product.json.status = DA_LAM_VIDEO`, dashboard tự nhận diện qua `generated_video_path`.

---

## 🧠 4. BÀI HỌC KINH NGHIỆM ĐÚC KẾT ĐƯỢC

1. **Chọn frame tham chiếu sai → AI lệch màu hoàn toàn.** Frame bị cháy sáng/backlight (`frame_04.jpg` ban đầu) khiến Flow diễn giải áo "olive-khaki" thành "trắng kem". Luôn chọn frame ánh sáng đều, không ngược sáng, không có text burn-in trước khi đưa vào prompt.
2. **Mô tả chữ (text + ảnh "ingredient") KHÔNG đủ để Flow tái tạo chính xác màu/chất liệu/form sản phẩm** — đây là giới hạn cấu trúc của model sinh video (ưu tiên giữ nhân vật nhất quán, diễn giải lỏng lẻo phần trang phục). Giải pháp đúng là **khoá pixel sản phẩm trước khi animate**:
   - Flow có chế độ **"Khung hình"** (Start/End frame, tương đương image-to-video) — upload 1 ảnh tĩnh đã đúng 100% sản phẩm, Flow chỉ cần animate chuyển động, không "tưởng tượng" lại trang phục.
   - Cách tạo ảnh tĩnh đó: ban đầu thử face-swap (InsightFace/inswapper, tái dùng từ `motion_mimic_workflow.py`) ghép mặt Gô Bi vào frame thật — **bị người dùng từ chối** (không muốn đổi mặt lên người mẫu thật). Hướng đúng hơn được yêu cầu: **giữ nguyên danh tính/thân hình Gô Bi, chỉ đổi trang phục** qua ảnh-sang-ảnh (Nano Banana trong Flow, chế độ Hình ảnh, đính cả nhân vật + ảnh sản phẩm, prompt chỉ rõ "giữ nguyên mặt/dáng, chỉ đổi áo") — **chưa kịp verify do bị chặn tài khoản (mục 5)**.
3. **Mỗi clip Flow 8s muốn giống nhịp cắt nhanh của video gốc** (video gốc ~14 cut/26s) cần chủ động tách clip thành nhiều sub-cut bằng ffmpeg, không trông chờ Flow tự cắt nhanh.
4. **Watermark AI (✦ góc dưới-phải)** xử lý được sạch bằng crop 82%+scale — không cần tool xoá watermark phức tạp.
5. **Audio voiceover phải nhúng rõ ràng `<audio data-track-index="N">` trong composition HyperFrames** — `render_project()` không tự mux audio ngoài nếu HTML không khai báo.

---

## 🚨 5. SỰ CỐ NGHIÊM TRỌNG — TÀI KHOẢN GOOGLE FLOW BỊ GẮN CỜ "HOẠT ĐỘNG BẤT THƯỜNG"

Sau khi gửi liên tiếp nhiều yêu cầu tạo video/ảnh qua EGO Lite (kể cả khi đã giãn cách thời gian), tài khoản Flow (`dinhthienthoai@gmail.com`) bắt đầu báo lỗi **"Không thành công — Chúng tôi nhận thấy có hoạt động bất thường... các tiện ích trình duyệt sửa đổi trang có thể gây ra vấn đề"** cho MỌI yêu cầu tạo mới (cả ảnh lẫn video), không tính phí nhưng cũng không ra kết quả.

* **Đã thử và đều thất bại:** gửi lại sau vài phút, gửi 1 yêu cầu đơn lẻ cách xa — tất cả đều bị chặn giống hệt nhau → xác nhận đây là chặn ở **cấp tài khoản/server**, không phải do tốc độ gửi.
* **Quyết định đã thực hiện theo đúng quy tắc an toàn:** KHÔNG mở task space EGO Lite mới để né chặn (vì vẫn cùng tài khoản Google, và cố né tránh hệ thống chống lạm dụng chỉ làm tăng rủi ro khoá tài khoản vĩnh viễn). Dừng hẳn thao tác Flow qua EGO Lite, bàn giao hướng dẫn thủ công cho người dùng tự thao tác bằng tay thật khi cần.
* **Khuyến nghị cho các phiên sau:** giãn cách đáng kể giữa các lượt tạo Flow qua EGO Lite trong cùng 1 phiên (không gửi 5 yêu cầu liên tiếp như lần đầu từng làm thành công — rất có thể chính đợt đó đã tích luỹ điểm "bất thường" dẫn đến bị chặn ở đợt sau), và luôn có phương án dự phòng "người dùng tự thao tác tay" khi bị chặn thay vì cố gắng vòng qua.

---

## 📂 Tài sản còn lại để dùng tiếp khi tài khoản Flow hết bị gắn cờ
* Ảnh tham chiếu màu chuẩn: `_product_ref/product_ref_v2.jpg`
* Prompt "giữ nguyên danh tính, chỉ đổi trang phục" đã soạn sẵn (xem log hội thoại).
* Script ráp video đã hoàn thiện, không cần sửa thêm: `scripts/flow_ai/assemble_flow_scenes.py`.
