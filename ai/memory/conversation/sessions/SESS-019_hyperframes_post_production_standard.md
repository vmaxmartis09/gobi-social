# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-019
> **Tiêu đề phiên:** Thiết Lập Chuẩn Hóa Tài Liệu & Chỉ Dẫn Hệ Thống: HeyGen HyperFrames Là Công Cụ Hậu Kỳ Mặc Định  
> **Thời gian:** 2026-10-20  
> **Người thực hiện:** Người dùng & AI Assistant (Antigravity)  
> **Phân hệ chính:** `[Video Engine] | [System Rules] | [Architecture & Docs]`  
> **Trạng thái:** `Hoàn thành`

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Vấn đề đặt ra:** Hệ thống cần một bộ tài liệu và quy chuẩn chỉ dẫn tối cao để toàn bộ AI Agents (Gemini, Claude, Cursor, Antigravity) và các kỹ sư tiếp quản luôn tự động hiểu và bắt buộc sử dụng **HeyGen HyperFrames** làm công cụ biên tập, hậu kỳ video mặc định của dự án `gobi-social`.
* **Mục tiêu cần đạt:**
  1. Ban hành tài liệu tiêu chuẩn kỹ thuật hậu kỳ: [`docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md`](docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md).
  2. Khóa cứng quy tắc hoạt động bắt buộc trong các file chỉ dẫn agent: [`AGENTS.md`](AGENTS.md), [`GEMINI.md`](GEMINI.md), [`CLAUDE.md`](CLAUDE.md), [`.cursorrules`](.cursorrules), và [`.agent/rules/hyperframes-post-production.md`](.agent/rules/hyperframes-post-production.md).
  3. Đồng bộ hóa pipeline CLI: `python -m gobi video render --engine hyperframes` và `python -m gobi video preview`.
  4. Chuẩn hóa TikTok Safe Zone 9:16 (Top 180px, Bottom 320px) và cơ chế phụ đề động (Kinetic / Karaoke Pill).

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI
* **Các file code và tài liệu đã ban hành:**
  * [`docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md`](docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md): Tài liệu tiêu chuẩn kỹ thuật đầy đủ: Safe Zone 9:16, Composition Contract HTML5/CSS, đa luồng âm thanh ducking, mẫu kịch bản review KOC, hướng dẫn dòng lệnh & Python SDK.
  * [`.agent/rules/hyperframes-post-production.md`](.agent/rules/hyperframes-post-production.md) & [`.agents/rules/hyperframes-post-production.md`](.agents/rules/hyperframes-post-production.md): Chỉ dẫn bắt buộc cho mọi AI Agent.
  * [`CLAUDE.md`](CLAUDE.md) & [`.cursorrules`](.cursorrules): Cập nhật quy tắc bắt buộc và câu lệnh phím tắt.
  * [`src/gobi/adapters/integrations/hyperframes_adapter.py`](src/gobi/adapters/integrations/hyperframes_adapter.py): Adapter kết nối Node CLI `npx hyperframes` (lint, check, render, preview).
  * [`src/gobi/services/media/hyperframes_engine.py`](src/gobi/services/media/hyperframes_engine.py): Service điều phối dựng video KOC review 9:16.
* **Cập nhật đồ thị tri thức:**
  * Chạy `graphify update .` để đồng bộ hóa mã nguồn vào `graphify-out/`.

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
* Toàn bộ hệ thống AI Agents và tooling khi tiếp nhận yêu cầu dựng/hậu kỳ video sẽ tự động định tuyến sang HyperFrames.
* Tài liệu tiêu chuẩn hoàn chỉnh đã lưu tại [`docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md`](docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md).
* Môi trường thực thi đáp ứng 100%: Node 26.8, FFmpeg 8.1.1, Chrome Headless Shell, 11 HyperFrames AI skills đã cài đặt.

---

## 🧠 4. BÀI HỌC KINH NGHIỆM ĐÚC KẾT ĐƯỢC
* Việc định nghĩa quy chuẩn ở cả 3 cấp độ (File Rule hệ thống như `AGENTS.md`, File Rule của từng công cụ như `.cursorrules`/`CLAUDE.md`, và File Tài liệu kiến trúc `docs/`) đảm bảo không có bất kỳ agent nào bị sót hoặc quay lại thói quen cũ dùng FFmpeg thô.

---

## ⏭️ 5. BƯỚC TIẾP THEO (NEXT ACTIONS)
- [ ] Thực hiện 1 video mẫu hoàn chỉnh: Lấy source video từ SnapTik -> Ghép giọng LyLy -> Hậu kỳ chèn phụ đề kinetic và nhãn giá 139K bằng HyperFrames.
- [ ] Xây dựng thư viện component mẫu (blocks) độc quyền cho thương hiệu Gobi Boutique (nơ, tag giá, badge rating 5 sao).
