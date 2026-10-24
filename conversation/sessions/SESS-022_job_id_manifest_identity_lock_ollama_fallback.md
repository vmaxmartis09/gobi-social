# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-022
> **Tiêu đề phiên:** Thêm ID/manifest theo job, face-consistency cho Gô Bi, và Ollama fallback thay Gemini
> **Thời gian:** 2026-10-22
> **Người thực hiện:** Người dùng & Claude
> **Phân hệ chính:** `[KOC AI] | [Video Engine] | [Intelligence / Local LLM]`
> **Trạng thái:** `Hoàn thành`

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU
Sau SESS-021 (video review Miho House), người dùng nêu 3 vấn đề cần cải thiện mà **không phụ thuộc Google Flow** (đang bị gắn cờ "hoạt động bất thường"):
1. Mỗi job cần ID/thư viện đồng nhất để không lẫn clip giữa các job.
2. Khuôn mặt "Gô Bi" bị trôi nhẹ giữa các lần Flow generate (khác với vấn đề trang phục đã biết).
3. Có Ollama + DeepSeek cục bộ thì giúp được công đoạn nào trong pipeline?

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI

### A. Manifest + job_id (`scripts/flow_ai/assemble_flow_scenes.py`)
* `assemble()` nhận thêm `job_id` (mặc định tự tách từ tên folder job, vd `7694350317697142037_...` → `7694350317697142037`).
* Sau khi render xong, ghi `_flow_manifest.json` ngay trong job folder: liệt kê từng cảnh (clip nguồn, voiceover, có bị face-lock hay không, thời lượng) + `job_id`, `generated_at`, `output_video`. Dùng để tra cứu clip nào thuộc job nào khi nhiều job cùng xử lý trong 1 phiên.
* **Chưa làm:** phần "Google Drive folder/project riêng cho mỗi job" người dùng từng chọn — phụ thuộc thao tác Flow trực tiếp, đang tạm hoãn vì tài khoản Flow bị chặn.

### B. Face-consistency lock cho Gô Bi (`_enforce_gobi_identity()` trong cùng file)
* **Phân biệt rõ với lần trước:** đây là face-swap **TỪ CHÍNH** `assets/characters/lyly_master_portrait.png` (ảnh gốc của Gô Bi) **LÊN** clip Flow đã tạo ra (đã là "Gô Bi" nhưng mặt trôi nhẹ) — không phải ghép mặt Gô Bi lên người mẫu thật (đã bị từ chối ở job trước).
* Tái dùng pattern InsightFace/inswapper per-frame từ `motion_mimic_workflow.py`, áp cho từng clip trước bước xoá watermark/cắt sub-cut.
* Mặc định bật (`enforce_identity=True`); chạy xong với job Miho House, kiểm tra 3 frame rải rác trong video: 2/3 rất sạch, 1/3 có vệt blend nhẹ ở má — chấp nhận được, cải thiện rõ so với không lock.
* **Hạn chế đã biết:** mỗi lần gọi `_enforce_gobi_identity()` tự load lại InsightFace+inswapper từ đầu (không cache qua các cảnh) — chạy đúng nhưng chậm hơn cần thiết (~2 phút cho 5 clip). Có thể tối ưu sau bằng cách load model 1 lần dùng chung.

### C. Ollama local LLM thay Gemini khi hết quota
* **Model đã thử và loại:** `deepseek-r1:7b` — distill reasoning, dù prompt yêu cầu rõ tiếng Việt vẫn lẫn tiếng Trung/Anh, thậm chí bịa link sản phẩm không có thật trong dữ liệu đầu vào. **Không dùng cho tác vụ này.**
* **Model đã chọn làm mặc định:** `qwen2.5:7b` — output tiếng Việt tự nhiên, bám đúng giá/thông tin sản phẩm thật, không bịa. (16GB RAM máy hiện tại không tải nổi DeepSeek-V3/V3.1 bản đầy đủ — ~400GB; "DeepSeek V4" người dùng nhắc tới chưa tồn tại tại thời điểm này).
* File mới: `src/gobi/adapters/integrations/ollama_text_adapter.py` — cùng method `generate_remix_script()` và schema `RemixScript` như `GeminiTextAdapter`, hoán đổi được trực tiếp. Dùng `format: "json"` của Ollama API để ép constraint JSON (prompt chữ không đủ để deepseek-r1 tuân theo, dù qwen2.5 tuân theo khá tốt ngay cả không có flag này).
* **Tự động fallback Gemini → Ollama** khi Gemini lỗi/hết quota, đã nối vào cả `src/gobi/cli/cmd_brief.py` và `src/gobi/services/workflows/content_remix_workflow.py` (bước "Generate Remix Script") — không cần người dùng tự chuyển tay.
* **Giới hạn phạm vi đã nêu rõ với người dùng:** Ollama/DeepSeek là model NGÔN NGỮ — không sửa được 2 vấn đề thị giác (trang phục sai, mặt trôi); chỉ hợp với các bước xử lý CHỮ (viết kịch bản, parse brief). Muốn tự động hoá bước "chọn frame chuẩn" (phát hiện cháy sáng/chữ burn-in) cần model vision cục bộ riêng (LLaVA/DeepSeek-VL qua Ollama), chưa làm.

---

## 🏆 3. KẾT QUẢ & BẰNG CHỨNG
* [`_flow_manifest.json`](../../data/products/7694350317697142037_ao_len_tieu_miho_house_tiktokshop1010_chinhha/_flow_manifest.json) của job Miho House — mẫu thực tế đầu tiên.
* Video đã render lại với face-lock: [`generated_video.mp4`](../../data/products/7694350317697142037_ao_len_tieu_miho_house_tiktokshop1010_chinhha/generated_video.mp4), đã gửi người dùng xem bản nén.
* `src/gobi/adapters/integrations/ollama_text_adapter.py` — test độc lập thành công với `qwen2.5:7b`.

---

## 🧠 4. BÀI HỌC KINH NGHIỆM
1. **Face-swap có 2 hướng dùng hoàn toàn khác nhau** — ghép mặt AI lên người thật (rủi ro đạo đức, đã bị từ chối) vs. ép đồng nhất chính nhân vật AI với ảnh gốc của nó (hợp lý, giải quyết đúng vấn đề "trôi" identity). Luôn hỏi rõ hướng nào trước khi code, đừng gộp chung là "face-swap" rồi đoán.
2. **Local LLM 7B không đồng đều giữa các họ model cho cùng 1 ngôn ngữ** — distill reasoning (deepseek-r1) tối ưu cho math/code tiếng Anh/Trung, không đáng tin cho copywriting tiếng Việt tự nhiên; model multilingual-first (qwen2.5) vượt trội hẳn dù cùng kích thước 7B. Luôn test thực tế bằng tiếng Việt trước khi chọn làm mặc định, không giả định theo tên/độ nổi tiếng model.
3. **Ollama `format: "json"` chỉ ép đúng cú pháp, không ép đúng ngôn ngữ nội dung** — phải tự viết prompt nhấn mạnh ngôn ngữ ở cả đầu và cuối prompt.
