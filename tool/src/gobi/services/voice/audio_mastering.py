"""
GOBI VOICE ENGINE 2.0 - TIKTOK AUDIO MASTERING
==============================================
Bộ xử lý âm thanh hậu kỳ chuyên nghiệp cho TikTok / Reels / Shorts:
- De-Esser: Khử chói và rít ở các phụ âm x, s, tr, ch (tần số 5.5kHz - 7kHz).
- Parametric EQ: Boost dải Presence (+3.5dB tại 3.2kHz - 4.5kHz) giúp giọng KOC nổi bật trên nhạc nền BGM.
- Warmth EQ: Boost nhẹ (+2.0dB tại 120Hz) tạo độ ấm và nội lực cho giọng nói.
- Dynamic Compressor: Tỷ lệ nén 4:1 ép phẳng dải động, tạo độ nảy dồn dập (TikTok Action Hype).
- EBU R128 Loudness Normalizer: Đạt chuẩn -14 LUFS (chuẩn phát thanh thương mại TikTok / YouTube).
- Pacing Shifter: Tăng tốc nhẹ 3% - 5% duy trì nhịp điệu cuốn hút, giữ chân người xem 3s đầu.
"""

import os
import sys
import subprocess
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

class AudioMastering:
    def __init__(self):
        self.ffmpeg = FFMPEG_EXE

    def master_tiktok_koc(
        self,
        input_audio_path: str,
        output_audio_path: str,
        target_lufs: float = -14.0,
        presence_boost_db: float = 1.2,
        tempo_factor: float = 1.22,
        bitrate: str = "192k"
    ) -> str:
        """
        Thực thi chuỗi Mastering TikTok Broadcast 6 bước liên hoàn qua FFmpeg.
        Được tinh chỉnh bảo toàn âm sắc tự nhiên (Warmth, Sweetness) và tăng tốc nhịp nói KOC Action.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)

        filter_chain = (
            # 1. De-Esser khử chói tần số cao
            "deesser=i=0.4:m=0.4:f=6500:s=o,"
            # 2. Parametric EQ: Giữ độ ấm tự nhiên (160Hz) và presence vừa vặn
            f"equalizer=f=3500:t=q:w=2.0:g={presence_boost_db},"
            "equalizer=f=160:t=q:w=1.2:g=1.2,"
            # 3. Dynamic Compressor nén nhẹ nhàng 2.5:1 không làm bẹt giọng
            "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120:makeup=2.0dB,"
            # 4. Chuẩn hóa âm lượng EBU R128 (-14 LUFS)
            f"loudnorm=I={target_lufs}:LRA=8:TP=-1.5,"
            # 5. Tăng tốc nhịp nói KOC TikTok
            f"atempo={tempo_factor}"
        )

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(input_audio_path),
            "-af", filter_chain,
            "-ar", "48000",
            "-ac", "1",
            "-b:a", bitrate,
            str(output_audio_path)
        ]

        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            # Fallback đơn giản nếu filter quá phức tạp
            cmd_fallback = [
                self.ffmpeg, "-y",
                "-i", str(input_audio_path),
                "-af", f"loudnorm=I={target_lufs}:TP=-1.5,atempo={tempo_factor}",
                "-ar", "48000",
                "-ac", "1",
                "-b:a", bitrate,
                str(output_audio_path)
            ]
            subprocess.run(cmd_fallback, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return os.path.abspath(output_audio_path)
