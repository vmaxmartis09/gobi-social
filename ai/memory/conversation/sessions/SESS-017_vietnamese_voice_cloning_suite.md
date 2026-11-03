# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-017
> **Tiêu đề phiên:** Xây dựng Gobi Voice Studio 2.0 - Hệ thống Voice Cloning Tiếng Việt thuần Việt từ bất kỳ Video hoặc MP3  
> **Thời gian:** 2026-10-19  
> **Người thực hiện:** Người dùng & AI Assistant (Antigravity VMAX Agent)  
> **Phân hệ chính:** `[Voice / Audio Engine] | [Whisper STT] | [TikTok Audio Mastering] | [Relentless Execution]`  
> **Trạng thái:** `✅ Hoàn thành 100% (Relentless Execution)`

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Yêu cầu từ người dùng:**
  * Lên kế hoạch lại từ đầu, bắt đầu trước hết là phần giọng nói.
  * Xây dựng hệ thống có thể clone bất kỳ giọng nói nào từ 1 video hoặc file MP3 đầu vào, đảm bảo đầu ra là **tiếng Việt thuần Việt, chuẩn thanh điệu, ngữ điệu tự nhiên và giàu năng lượng KOC**.
* **Mục tiêu kỹ thuật giải quyết triệt để:**
  1. Loại bỏ thao tác thủ công: Không cần người dùng gõ tay text đối chiếu của đoạn audio mẫu. Tự động dùng Whisper STT tiếng Việt để nhận diện text chuẩn xác.
  2. Tự động bóc tách và lọc tạp âm (Vocal Isolation & Denoise), loại bỏ BGM của video gốc.
  3. Thuật toán VAD tự động cắt lát vàng 3.8s - 6.0s có năng lượng cao nhất.
  4. Đa tầng suy luận: VieNeu-TTS v3 Turbo, Seed-VC (Voice Conversion), F5-TTS, cứu cánh Edge-TTS.
  5. TikTok Audio Mastering chuyên sâu (-14 LUFS, presence boost 3.2kHz, de-esser).
  6. Xây dựng công cụ dòng lệnh hoàn chỉnh `scripts/voice/voice_studio.py` (`clone`, `speak`, `one-shot`, `list`).

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI
* **Cài đặt thư viện phụ thuộc:**
  * `faster-whisper` (v1.2.1), `ctranslate2`, `soundfile`, `gradio_client`.
* **Xây dựng module lõi:**
  * [`src/gobi/services/voice/audio_preprocessor.py`](../../src/gobi/services/voice/audio_preprocessor.py): Trích xuất audio, lọc dải thông 80Hz - 12kHz, afftdn khử nhiễu nền, VAD quét lát cắt vàng, load audio qua FFmpeg raw f32le để Whisper chép lời không phụ thuộc PyAV container.
  * [`src/gobi/services/voice/audio_mastering.py`](../../src/gobi/services/voice/audio_mastering.py): Chuỗi Mastering TikTok Broadcast 6 bước liên hoàn (De-esser, Parametric EQ +3.5dB ở 3.2kHz, Dynamic Compressor 4:1, EBU R128 -14 LUFS, tempo +3%).
  * [`src/gobi/services/voice/voice_cloner.py`](../../src/gobi/services/voice/voice_cloner.py): Unified Voice Cloner đa tầng, quản lý Sound Profiles tại `assets/voice_profiles/`.
  * [`scripts/voice/voice_studio.py`](../../scripts/voice/voice_studio.py): CLI Suite 1 chạm điều khiển toàn bộ hệ thống.

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
* **Tạo Sound Profile tự động:**
  * Tạo thành công Profile `koc_gobi_real` từ `assets/mau_voice/full_audio.wav`.
  * Slice vàng 4.5s (RMS 0.5425) được tự động phát hiện và chép lời bằng tiếng Việt.
* **Tổng hợp giọng nói mới và Mastering thành công:**
  * Lệnh thực thi:
    ```bash
    python scripts/voice/voice_studio.py speak --voice koc_gobi_real --script "Mấy bà ơi, chiếc áo cardigan len dệt kim này vừa về hàng là cháy luôn 500 chiếc, nhanh tay bấm vào giỏ hàng góc trái săn deal nha!" --output output/voice_clone_test.mp3
    ```
  * File kết quả: [`output/voice_clone_test.mp3`](../../output/voice_clone_test.mp3) (179,756 bytes, độ dài 7.46 giây, 48kHz 192kbps, âm lượng chuẩn hóa -14 LUFS).

---

## 🧠 4. BÀI HỌC KINH NGHIỆM ĐÚC KẾT ĐƯỢC
1. **Khắc phục lỗi PyAV `metadata_errors` trên Python mới:** Bằng cách pipe audio trực tiếp từ FFmpeg với cờ `-f f32le -ar 16000` thành numpy array float32, Whisper transcribe cực nhanh (1.2s) mà không bao giờ gặp lỗi codec của PyAV container.
2. **Quản lý Sound Profile lâu dài:** Một khi đã clone từ video/mp3 thành profile, những lần sau chỉ mất 10-15s để sinh bất kỳ kịch bản review nào mà không cần nạp lại video gốc.
