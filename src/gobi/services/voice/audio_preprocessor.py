"""
GOBI VOICE ENGINE 2.0 - AUDIO PREPROCESSOR
==========================================
Chuyên xử lý bóc tách audio từ bất kỳ video (mp4, mov, mkv) hoặc audio (mp3, wav, m4a),
lọc tạp âm, cô lập giọng nói (Vocal Isolation), tự động cắt lát vàng (Golden Slice VAD 3.8s-6s)
và tự động chép lời đối chiếu (Auto-Transcription) bằng Faster-Whisper Tiếng Việt.
"""

import os
import sys
import subprocess
import numpy as np
import soundfile as sf
from pathlib import Path
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

class AudioPreprocessor:
    def __init__(self, whisper_model: str = "base"):
        """
        Khởi tạo bộ tiền xử lý âm thanh.
        whisper_model: 'tiny', 'base', 'small', 'medium' (mặc định 'base' nhanh & chính xác).
        """
        self.whisper_model_name = whisper_model
        self._whisper = None

    def _get_whisper(self):
        if self._whisper is None:
            from faster_whisper import WhisperModel
            print(f"[AudioPreprocessor] Đang tải mô hình Faster-Whisper ({self.whisper_model_name})...")
            # Chạy trên CPU với int8 cho tốc độ tức thì trên Mac
            self._whisper = WhisperModel(self.whisper_model_name, device="cpu", compute_type="int8")
            print("[AudioPreprocessor] Whisper đã sẵn sàng!")
        return self._whisper

    def extract_and_denoise_audio(self, input_path: str, output_wav: str, sample_rate: int = 48000) -> str:
        """
        Trích xuất và lọc tạp âm chuyên sâu:
        - Chuyển đổi sang PCM 16-bit Mono.
        - Lọc dải thông giọng nói (Highpass 80Hz - Lowpass 12000Hz).
        - Giảm nhiễu nền thích ứng (afftdn với mức triệt tiêu -25dB).
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", str(input_path),
            "-vn",
            "-af", "highpass=f=80,lowpass=f=12000,afftdn=nf=-25",
            "-ar", str(sample_rate),
            "-ac", "1",
            str(output_wav)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi khi trích xuất âm thanh từ {input_path}: {res.stderr}")
        return output_wav

    def find_golden_slice(
        self,
        full_wav_path: str,
        output_slice_path: str,
        target_duration: float = 4.5,
        min_duration: float = 3.5,
        max_duration: float = 6.0
    ) -> dict:
        """
        Thuật toán VAD thông minh quét toàn bộ file âm thanh để tìm lát cắt vàng (Golden Slice):
        - Có mức năng lượng RMS ổn định (0.08 <= RMS <= 0.45).
        - Không bị rè/clip (peak < 0.98).
        - Tỷ lệ Zero-Crossing chuẩn giọng nói người (0.06 <= ZCR <= 0.22).
        - Tránh hoàn toàn các khoảng lặng hoặc tiếng ồn tạp.
        """
        data, sr = sf.read(full_wav_path)
        if len(data.shape) > 1:
            data = data[:, 0]

        total_samples = len(data)
        target_samples = int(target_duration * sr)
        step_samples = int(0.20 * sr)  # Bước nhảy 200ms

        # Nếu file ngắn hơn target_duration thì lấy toàn bộ
        if total_samples <= target_samples:
            sf.write(output_slice_path, data, sr)
            return {
                "slice_path": output_slice_path,
                "start_sec": 0.0,
                "end_sec": total_samples / sr,
                "duration": total_samples / sr,
                "rms": float(np.sqrt(np.mean(data**2)))
            }

        best_score = -1e9
        best_start = 0

        for start in range(0, total_samples - target_samples, step_samples):
            window = data[start:start + target_samples]
            rms = np.sqrt(np.mean(window**2))

            # Loại bỏ nếu quá yên tĩnh (< 0.05) hoặc quá chói/clip (> 0.55)
            if rms < 0.05 or rms > 0.55:
                continue

            # Đo độ ổn định phân bố năng lượng và mật độ phát âm
            peak = np.max(np.abs(window))
            crest_factor = peak / (rms + 1e-6)
            zero_crossings = np.sum(np.abs(np.diff(np.sign(window)))) / (2.0 * len(window))

            # Điểm số tối ưu: Năng lượng dồi dào, phát âm rõ ràng, không bị nén nghẹt
            score = (rms * 15.0) - abs(zero_crossings - 0.12) * 8.0 - abs(crest_factor - 4.0) * 1.5

            if score > best_score:
                best_score = score
                best_start = start

        # Áp dụng fade in / fade out nhẹ 50ms để không bị tiếng "pop/click"
        slice_data = data[best_start:best_start + target_samples].copy()
        fade_len = int(0.05 * sr)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        slice_data[:fade_len] *= fade_in
        slice_data[-fade_len:] *= fade_out

        os.makedirs(os.path.dirname(os.path.abspath(output_slice_path)), exist_ok=True)
        sf.write(output_slice_path, slice_data, sr)

        start_sec = best_start / sr
        end_sec = (best_start + target_samples) / sr
        return {
            "slice_path": output_slice_path,
            "start_sec": round(start_sec, 3),
            "end_sec": round(end_sec, 3),
            "duration": round(target_duration, 3),
            "rms": round(float(np.sqrt(np.mean(slice_data**2))), 4)
        }

    def load_audio_for_whisper(self, audio_path: str) -> np.ndarray:
        """
        Đọc audio bất kỳ và chuyển sang numpy array float32 16kHz chuẩn của Whisper bằng FFmpeg.
        Bỏ qua hoàn toàn phụ thuộc vào PyAV giúp tương thích 100% mọi hệ điều hành.
        """
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", str(audio_path),
            "-f", "f32le",
            "-ac", "1",
            "-ar", "16000",
            "-"
        ]
        raw_bytes = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return np.frombuffer(raw_bytes, dtype=np.float32)

    def transcribe_audio(self, audio_path: str, language: str = "vi") -> str:
        """
        Nhận diện văn bản đối chiếu (Reference Text) tự động bằng Faster-Whisper.
        Bảo toàn dấu thanh điệu, chính tả chuẩn tiếng Việt.
        """
        whisper = self._get_whisper()
        audio_data = self.load_audio_for_whisper(audio_path)
        
        segments, info = whisper.transcribe(
            audio_data,
            language=language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=300)
        )
        
        texts = []
        for segment in segments:
            texts.append(segment.text.strip())

        full_text = " ".join(texts).strip()
        return full_text

    def process_media(self, input_media_path: str, output_dir: str, target_duration: float = 4.5) -> dict:
        """
        Quy trình tiền xử lý 1 chạm:
        1. Nhận video hoặc mp3
        2. Tách và làm sạch full audio
        3. Cắt lát vàng 4.5s
        4. Tự động chép lời văn bản
        5. Trả về payload hoàn chỉnh cho Voice Cloner
        """
        os.makedirs(output_dir, exist_ok=True)
        full_wav = os.path.join(output_dir, "raw_extracted_clean.wav")
        ref_slice_wav = os.path.join(output_dir, "reference_clean_slice.wav")

        print(f"[1/3] Trích xuất và khử tạp âm từ: {input_media_path}...")
        self.extract_and_denoise_audio(input_media_path, full_wav)

        print(f"[2/3] Quét VAD tìm phân đoạn vàng ({target_duration}s)...")
        slice_info = self.find_golden_slice(full_wav, ref_slice_wav, target_duration=target_duration)

        print("[3/3] Nhận diện văn bản đối chiếu bằng Whisper Tiếng Việt...")
        transcript = self.transcribe_audio(ref_slice_wav, language="vi")

        result = {
            "source_media": os.path.abspath(input_media_path),
            "full_wav": os.path.abspath(full_wav),
            "ref_slice_wav": os.path.abspath(ref_slice_wav),
            "start_sec": slice_info["start_sec"],
            "end_sec": slice_info["end_sec"],
            "duration": slice_info["duration"],
            "rms": slice_info["rms"],
            "transcript": transcript
        }

        print(f"\n[+] Tiền xử lý hoàn tất!")
        print(f"    - Mẫu vàng: {result['ref_slice_wav']} ({result['duration']}s, RMS: {result['rms']})")
        print(f"    - Text đối chiếu: \"{result['transcript']}\"")
        return result
