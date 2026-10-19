# 🎙️ TOPIC 01: KOC AI & VOICE CLONING PIPELINE
> **Tổng hợp chuyên đề:** Nhân vật số KOC AI, quản lý DNA nhận dạng khuôn mặt, ma trận góc quay 36 angles, và công nghệ sao chép giọng nói tiếng Việt.

---

## 1. MỤC ĐÍCH & Ý NGHĨA TRONG BỨC TRANH VMAX
* Xóa bỏ hoàn toàn sự phụ thuộc vào KOL/KOC người thật, giảm chi phí sản xuất video review thời trang & đồ công nghệ xuống gần bằng 0.
* Đảm bảo tính nhất quán (Face Consistency) của nhân vật thương hiệu xuyên suốt hàng trăm video TikTok Affiliate.
* Tự động hóa việc chuyển đổi văn bản kịch bản (Script) thành giọng nói tự nhiên, có ngữ điệu cảm xúc, đúng phong cách review chân thực.

---

## 2. CÁC THÀNH PHẦN KỸ THUẬT CỐT LÕI

### 2.1. Quản lý DNA & Nhận diện nhân vật KOC
* **Master Profile:** Đinh Thiên Thoại - Kênh TikTok `@tis.decor`.
* **Concept:** Chàng trai có gu thẩm mỹ đánh giá đồ nữ / tư vấn trang phục tôn dáng và gợi ý quà tặng tinh tế.
* **Tài nguyên ảnh gốc (Ground Truth):**
  * [`affiliate_tiktok/dataset_koc/MASTER_KOC_DNA.jpg`](../../affiliate_tiktok/dataset_koc/MASTER_KOC_DNA.jpg)
  * [`affiliate_tiktok/dataset_koc/cinematic_koc_36_storyboard_v2.jpg`](../../affiliate_tiktok/dataset_koc/cinematic_koc_36_storyboard_v2.jpg)
* **Ma trận 36 góc quay camera:**
  * File cấu hình: [`affiliate_tiktok/prompts/koc_matrix_36_angles.json`](../../affiliate_tiktok/prompts/koc_matrix_36_angles.json)
  * Bao gồm đầy đủ các góc: Cận cảnh biểu cảm (Close-up), bán thân (Medium Shot), toàn thân xem form dáng đồ (Full Body), góc nghiêng 45 độ, góc trên cao (High Angle) và góc dưới chân (Low Angle).

### 2.2. Động cơ sinh Prompt kịch bản
* File mã nguồn: [`core/koc_prompt_generator.py`](../../core/koc_prompt_generator.py)
* Cơ chế: Kết hợp Master DNA + Mô tả sản phẩm thời trang + Yêu cầu góc máy + Phong cách ánh sáng studio thực tế để tạo prompt ảnh/video đạt chất lượng photorealistic chuẩn 8K.

### 2.3. Hệ thống sao chép giọng nói (Voice Cloning & TTS)
* **Phương án 1 (Fast TTS):** `edge-tts` (giọng tiếng Việt `vi-VN-HoaiMyNeural` hoặc `vi-VN-NamMinhNeural`) cho tốc độ sinh giọng tức thì.
* **Phương án 2 (Offline Neural Voice Clone - VieNeu-TTS v3 Turbo 48kHz ONNX):** 
  * Chạy trực tiếp qua CPU ONNX, không cần GPU nặng, không phụ thuộc cloud API.
  * Tự động trích xuất slice chuẩn 4.2s từ bất kỳ video review thật nào (`mau-voice.mp4`) để tạo Sound Profile vĩnh viễn trong [`assets/voice_profiles/`](../../assets/voice_profiles).
  * Chuỗi **TikTok Audio Mastering** tích hợp: Bộ nén `acompressor`, chuẩn hóa âm lượng `-14 LUFS`, boost tần số hiện diện `+3.5dB @ 3.2kHz`, tăng nhịp `1.05x` cho chất giọng Action KOC dồn dập.
* **Công cụ One-Click:** [`clone_voice_from_video.py`](../../clone_voice_from_video.py) và [`tools/voice/koc_voice_cloner.py`](../../tools/voice/koc_voice_cloner.py).
* **Đầu ra:** Các file audio và video thành phẩm tại [`output/`](../../output) (ví dụ: `koc_neil_girl_review_action.mp3`, `koc_neil_girl_review_demo.mp4`).

---

## 3. CÁC FILE LIÊN QUAN CHÍNH
* [`tools/voice/koc_voice_cloner.py`](../../tools/voice/koc_voice_cloner.py)
* [`clone_voice_from_video.py`](../../clone_voice_from_video.py)
* [`core/koc_ai_engine.py`](../../core/koc_ai_engine.py)
* [`affiliate_tiktok/rebuild_master_36_panels.py`](../../affiliate_tiktok/rebuild_master_36_panels.py)
* [`affiliate_tiktok/scripts/korean_fashion_review_scripts.py`](../../affiliate_tiktok/scripts/korean_fashion_review_scripts.py)
* [`affiliate_tiktok/TIKTOK_PROFILE.md`](../../affiliate_tiktok/TIKTOK_PROFILE.md)
