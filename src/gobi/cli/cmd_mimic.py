"""
=============================================================================
CLI SUBCOMMAND: GOBI MOTION MIMIC WORKFLOW
Cho phép nạp một video bất kỳ để KOC AI bắt chước chuyển động và dựng bằng HyperFrames.
=============================================================================
"""

import sys
import argparse
from pathlib import Path

from gobi.domain.motion_mimic_models import (
    MotionMimicInput,
    MimicLayoutMode,
    MotionEngineType,
    AudioStrategy,
    LipSyncMode
)
from gobi.services.workflows.motion_mimic_workflow import MotionMimicWorkflow


def register_mimic_parser(subparsers):
    """Đăng ký parser cho lệnh `python -m gobi mimic`."""
    mimic_parser = subparsers.add_parser(
        "mimic",
        help="Chạy quy trình AI KOC bắt chước một video nạp vào và dựng qua HyperFrames"
    )
    mimic_parser.add_argument(
        "--ref",
        required=True,
        help="Đường dẫn file video mẫu nội bộ hoặc URL TikTok/YouTube/Reels"
    )
    mimic_parser.add_argument(
        "--character",
        default="gobi_lyly",
        help="Preset tên nhân vật (gobi_lyly, gobi_neau) hoặc đường dẫn file ảnh chân dung"
    )
    mimic_parser.add_argument(
        "--layout",
        choices=["solo", "split_3_tier", "side_by_side"],
        default="solo",
        help="Bố cục video HyperFrames: solo (toàn màn hình 9:16), split_3_tier (chuẩn 3 tầng What's up AI), side_by_side (chia đôi)"
    )
    mimic_parser.add_argument(
        "--engine",
        choices=["local_faceswap", "kling_motion", "mock"],
        default="local_faceswap",
        help="Engine truyền chuyển động (mặc định: local_faceswap — InsightFace + CoreML, local trên M4)"
    )
    mimic_parser.add_argument(
        "--audio",
        choices=["keep_original", "omnivoice", "replace_bgm"],
        default="keep_original",
        help="Chiến lược âm thanh (mặc định: keep_original)"
    )
    mimic_parser.add_argument(
        "--title",
        default="GOBI AI MIMIC SOTA",
        help="Tiêu đề hiển thị trên header TikTok Safe Zone"
    )
    mimic_parser.add_argument(
        "--sub",
        default=None,
        help="Nội dung phụ đề động (Kinetic caption) gắn vào video"
    )
    mimic_parser.add_argument(
        "--script",
        default=None,
        help="Kịch bản lời đọc mới để clone giọng (chỉ dùng khi --audio omnivoice). Nếu bỏ trống sẽ dùng --sub."
    )
    mimic_parser.add_argument(
        "--lipsync",
        choices=["auto", "on", "off"],
        default="auto",
        help="Khớp khẩu hình theo audio mới (mặc định: auto — tự chạy khi --audio omnivoice)"
    )
    mimic_parser.add_argument(
        "--out",
        default=None,
        help="Tên file video MP4 đầu ra mong muốn"
    )
    mimic_parser.set_defaults(func=cmd_mimic_run)
    return mimic_parser


def cmd_mimic_run(args):
    """Handler thực thi lệnh `python -m gobi mimic`."""
    print("=" * 60)
    print("🎭 GOBI MOTION MIMIC PIPELINE ACTIVATED")
    print(f"[*] Video mẫu nạp vào : {args.ref}")
    print(f"[*] Nhân vật AI KOC   : {args.character}")
    print(f"[*] Bố cục HyperFrames: {args.layout}")
    print(f"[*] Engine chuyển động: {args.engine}")
    print(f"[*] Xử lý Audio       : {args.audio}")
    print("=" * 60)

    mimic_input = MotionMimicInput(
        reference_video_path_or_url=args.ref,
        character_avatar_path=args.character,
        layout_mode=MimicLayoutMode(args.layout),
        engine_type=MotionEngineType(args.engine),
        audio_strategy=AudioStrategy(args.audio),
        title_badge=args.title,
        subtitles_text=args.sub,
        output_filename=args.out,
        spoken_script=args.script or args.sub,
        lipsync_mode=LipSyncMode(args.lipsync)
    )

    workflow = MotionMimicWorkflow()
    result = workflow.execute(mimic_input)

    if result.is_success:
        print("\n" + "=" * 60)
        print("🎉 QUY TRÌNH HOÀN TẤT THÀNH CÔNG!")
        print(f"[+] Video Master hoàn chỉnh: {result.output_video_path}")
        print(f"[+] HyperFrames Project     : {result.hyperframes_project_dir}")
        print(f"[+] Thời lượng video        : {result.duration_seconds}s")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ QUY TRÌNH THẤT BẠI:")
        print(f"[!] Lỗi: {result.metadata.get('error')}")
        print("=" * 60)
        return 1
