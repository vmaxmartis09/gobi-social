"""
Test HyperFrames Engine Integration with Gobi Social Real Assets.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gobi.services.media.hyperframes_engine import HyperFramesEngine

def main():
    engine = HyperFramesEngine()

    video1 = Path("output/flow_videos/flow_video_2.mp4").resolve()
    video2 = Path("output/flow_videos/flow_video_1.mp4").resolve()
    voice = Path("output/lyly_neau_review.mp3").resolve()
    bgm = Path("assets/audio/bgm.mp3").resolve()

    print("[*] Testing HyperFramesEngine creation & render...")

    scenes = [
        {"video": str(video1), "sub": "Chất thun Nunu bodyfit co giãn 4 chiều cực đỉnh!", "duration": 4.5},
        {"video": str(video2), "sub": "Tôn dáng chuẩn từng đường nét, thoáng mát cả ngày.", "duration": 5.5}
    ]

    out_mp4 = Path("output/videos/test_hyperframes_real_flow.mp4").resolve()

    res = engine.create_and_render_video(
        scenes=scenes,
        audio_voiceover_path=str(voice),
        output_mp4=str(out_mp4),
        title_badge="ÁO THUN NUNU BODYFIT GÔ BI",
        bgm_path=str(bgm),
        temp_project_name="test_gobi_hyperframes",
        quality="draft",
        fps=30
    )

    print(f"[+] SUCCESS! Rendered video output: {res}")
    print(f"[+] File size: {os.path.getsize(res) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
