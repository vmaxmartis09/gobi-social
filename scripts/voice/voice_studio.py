#!/usr/bin/env python3
"""
=============================================================================
🌟 GOBI VOICE STUDIO 2.0 - CLI VIETNAMESE VOICE CLONING SUITE
=============================================================================
Hệ thống dòng lệnh chuyên biệt để nhân bản bất kỳ giọng nói nào từ Video hoặc MP3
và đọc kịch bản mới bằng giọng Tiếng Việt thuần Việt, đầy đủ ngữ điệu và năng lượng KOC.

CÁCH DÙNG:
  1. Tạo Profile mới từ Video/MP3:
     python scripts/voice/voice_studio.py clone --input video.mp4 --name koc_linh

  2. Đọc kịch bản mới bằng giọng đã clone:
     python scripts/voice/voice_studio.py speak --voice koc_linh --script "Kịch bản review..." --output output/review.mp3

  3. Chạy 1 chạm từ Video -> Kịch bản mới (One-shot):
     python scripts/voice/voice_studio.py one-shot --input video.mp4 --script "Kịch bản..." --output output/voice.mp3

  4. Liệt kê danh sách các giọng đã lưu:
     python scripts/voice/voice_studio.py list
=============================================================================
"""

import os
import sys
import argparse
from pathlib import Path

# Đảm bảo UTF-8 trên terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))  # repo src/ -> gobi.*
from gobi.services.voice import VoiceCloner

def main():
    parser = argparse.ArgumentParser(
        description="Gobi Voice Studio 2.0 - Clone bất kỳ giọng nói nào từ Video / MP3 sang Tiếng Việt chuẩn"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # SUBCOMMAND 1: clone
    p_clone = subparsers.add_parser("clone", help="Trích xuất audio, cắt lát vàng VAD, chép lời Whisper và tạo Sound Profile")
    p_clone.add_argument("--input", "-i", required=True, help="Đường dẫn file video (mp4, mov) hoặc audio (mp3, wav)")
    p_clone.add_argument("--name", "-n", required=True, help="Mã định danh cho giọng (vd: koc_neil, gô_bi, hoa_hậu)")
    p_clone.add_argument("--dialect", "-d", default="north", choices=["north", "south", "central"], help="Phương ngữ (north, south, central)")
    p_clone.add_argument("--text", "-t", default=None, help="Text đối chiếu mẫu (nếu để trống Whisper sẽ tự động nhận diện)")
    p_clone.add_argument("--duration", type=float, default=4.5, help="Độ dài mẫu âm thanh chuẩn (3.5s - 6.0s)")

    # SUBCOMMAND 2: speak
    p_speak = subparsers.add_parser("speak", help="Đọc kịch bản mới bằng Sound Profile đã lưu")
    p_speak.add_argument("--voice", "-v", required=True, help="Tên giọng (Sound Profile ID)")
    p_speak.add_argument("--script", "-s", required=True, help="Văn bản hoặc đường dẫn file .txt chứa kịch bản cần đọc")
    p_speak.add_argument("--output", "-o", default=None, help="Đường dẫn file mp3 đầu ra")
    p_speak.add_argument("--engine", "-e", default="omnivoice", choices=["omnivoice", "vieneu", "seed_vc", "f5_tts", "edge_tts"], help="Động cơ suy luận")
    p_speak.add_argument("--tempo", type=float, default=1.10, help="Tốc độ nhịp nói (1.00 - 1.30x, mặc định 1.10x đọc vừa phải)")
    p_speak.add_argument("--no-master", action="store_true", help="Bỏ qua bước Mastering TikTok -14 LUFS")

    # SUBCOMMAND 3: one-shot
    p_oneshot = subparsers.add_parser("one-shot", help="Quy trình 1 chạm: Nhận video/mp3 -> Clone -> Xuất audio kịch bản mới")
    p_oneshot.add_argument("--input", "-i", required=True, help="Đường dẫn file video hoặc mp3 mẫu")
    p_oneshot.add_argument("--script", "-s", required=True, help="Kịch bản mới cần đọc")
    p_oneshot.add_argument("--output", "-o", required=True, help="Đường dẫn file kết quả (.mp3 hoặc .wav)")
    p_oneshot.add_argument("--engine", "-e", default="omnivoice", choices=["omnivoice", "vieneu", "seed_vc", "f5_tts", "edge_tts"])
    p_oneshot.add_argument("--name", "-n", default=None, help="Tên profile lưu trữ")

    # SUBCOMMAND 4: list
    p_list = subparsers.add_parser("list", help="Xem danh sách các Sound Profile hiện có trong hệ thống")

    args = parser.parse_args()
    cloner = VoiceCloner()

    if args.command == "clone":
        meta = cloner.create_profile(
            media_path=args.input,
            profile_id=args.name,
            dialect=args.dialect,
            custom_transcript=args.text,
            target_duration=args.duration
        )
        print(f"\n[OK] Tạo Profile thành công cho: {meta['profile_id']}")

    elif args.command == "speak":
        script_text = args.script
        if os.path.isfile(args.script):
            with open(args.script, "r", encoding="utf-8") as f:
                script_text = f.read().strip()

        out_file = args.output or f"output/{args.voice}_script.mp3"
        res = cloner.speak(
            profile_id=args.voice,
            new_script=script_text,
            output_path=out_file,
            engine=args.engine,
            master=not args.no_master,
            tempo_factor=args.tempo
        )
        print(f"\n[OK] Đã xuất file giọng nói: {res}")

    elif args.command == "one-shot":
        script_text = args.script
        if os.path.isfile(args.script):
            with open(args.script, "r", encoding="utf-8") as f:
                script_text = f.read().strip()

        res = cloner.clone_and_speak(
            media_path=args.input,
            new_script=script_text,
            output_path=args.output,
            profile_id=args.name,
            engine=args.engine
        )
        print(f"\n[OK] One-shot hoàn tất: {res}")

    elif args.command == "list":
        vault_dir = Path("assets/voice_vault")
        print("\n=======================================================")
        print("📁 DANH SÁCH SOUND PROFILES TRONG KHO (VOICE VAULT):")
        print("=======================================================")
        count = 0
        if vault_dir.exists():
            for p in sorted(vault_dir.iterdir()):
                if p.is_dir() and (p / "profile.json").exists():
                    count += 1
                    import json
                    with open(p / "profile.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        dialect = data.get("dialect", "N/A")
                        dur = data.get("duration", "N/A")
                        print(f" • [{data.get('profile_id')}]: {data.get('speaker_name', data.get('profile_id'))} ({dialect}) - Mẫu: {dur}s")
                        print(f"   Thư mục: {p}")
                        print(f"   Text gốc: \"{data.get('transcript', '')[:65]}...\"")
                        if "source_preview_mp3" in data:
                            print(f"   🎧 Source gốc: {data['source_preview_mp3']}")
                        if "cloned_default_mp3" in data:
                            print(f"   🎤 Clone mẫu: {data['cloned_default_mp3']}")
        if count == 0:
            print("Chưa có profile nào trong kho.")
        print("=======================================================\n")

if __name__ == "__main__":
    main()
