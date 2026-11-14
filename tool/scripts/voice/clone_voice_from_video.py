"""
Convenient One-Click CLI to Clone Voice from Video & Synthesize Script
Usage:
    python scripts/voice/clone_voice_from_video.py --video mau-voice.mp4 --script "Mấy bà ơi, hôm nay em lên một mã..." --output output/voice.mp3
"""

import argparse
import sys
from pathlib import Path
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))  # repo src/ -> gobi.*
from gobi.services.voice.koc_voice_cloner import KOCVoiceCloner

def main():
    parser = argparse.ArgumentParser(description="VMAX KOC AI Voice Cloner")
    parser.add_argument("--video", "-v", default="mau-voice.mp4", help="Path to input video/audio")
    parser.add_argument("--profile", "-p", default="koc_neil_girl", help="Voice profile ID")
    parser.add_argument("--script", "-s", default="Mấy bà ơi, hôm nay em lên tiếp một mã áo thun chống nắng siêu đỉnh cho mùa hè này nhé! Nhanh tay bấm giỏ hàng kẻo hết size nha!", help="Script text to speak")
    parser.add_argument("--output", "-o", default="output/cloned_voice_speech.mp3", help="Output MP3 path")
    parser.add_argument("--render-video", "-rv", action="store_true", help="Render demo MP4 video")
    parser.add_argument("--speed", type=float, default=1.05, help="Speech playback speed")

    args = parser.parse_args()

    cloner = KOCVoiceCloner()
    
    # Check if profile exists, if not create it from video
    profile_dir = Path("assets/voice_profiles") / args.profile
    if not (profile_dir / "profile.json").exists():
        print(f"[*] Voice profile '{args.profile}' not found. Creating from '{args.video}'...")
        cloner.create_profile(args.video, args.profile)
    else:
        print(f"[*] Found existing voice profile '{args.profile}'.")

    # Synthesize audio
    cloner.synthesize(
        profile_id=args.profile,
        text=args.script,
        output_path=args.output,
        speed=args.speed,
        master_for_tiktok=True
    )

    if args.render_video:
        video_out = Path(args.output).with_suffix(".mp4")
        cloner.render_demo_video(
            video_source=args.video,
            audio_path=args.output,
            script_text=args.script,
            output_video=str(video_out)
        )

if __name__ == "__main__":
    main()
