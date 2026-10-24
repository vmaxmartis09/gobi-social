"""
=============================================================================
CLI SUBCOMMAND: GOBI CONTENT REMIX WORKFLOW
Dựa vào nội dung (kịch bản/nhịp độ) của 1 video tham khảo, viết kịch bản MỚI
qua Gemini và dựng video review sản phẩm bằng ảnh + giọng clone của Gô Bi —
KHÔNG swap mặt lên video tham khảo (khác với `gobi mimic`).
=============================================================================
"""

from pathlib import Path

from gobi.domain.scene_models import ContentRemixInput
from gobi.domain.motion_mimic_models import MimicLayoutMode, AudioStrategy
from gobi.services.workflows.content_remix_workflow import ContentRemixWorkflow
from gobi.services.workflows.simple_edit_workflow import SimpleEditWorkflow
from gobi.services.media import video_ingest
from gobi.services.media.video_classifier import classify_reference_video


def register_remix_parser(subparsers):
    """Đăng ký parser cho lệnh `python -m gobi remix`."""
    remix_parser = subparsers.add_parser(
        "remix",
        help="Dựa vào nội dung 1 video tham khảo, viết kịch bản mới (Gemini) và dựng video Gô Bi review sản phẩm (không swap mặt)"
    )
    remix_parser.add_argument(
        "--ref",
        required=True,
        help="Đường dẫn video mẫu nội bộ hoặc URL TikTok/YouTube để tham khảo nội dung/nhịp độ"
    )
    remix_parser.add_argument(
        "--product",
        default=None,
        help="Mã sản phẩm trong configs/products/catalog/ (ví dụ: SP-CD-005). Bắt buộc nếu không dùng --product-json."
    )
    remix_parser.add_argument(
        "--product-json",
        default=None,
        help="Đường dẫn file JSON chứa product_info trực tiếp (dùng khi sản phẩm không có trong catalog, vd: job từ Dashboard)"
    )
    remix_parser.add_argument(
        "--character",
        default="gobi_lyly",
        help="Preset tên nhân vật (gobi_lyly, gobi_neau) hoặc đường dẫn file ảnh chân dung"
    )
    remix_parser.add_argument(
        "--layout",
        choices=["solo", "split_3_tier", "side_by_side"],
        default="solo",
        help="Bố cục video HyperFrames (mặc định: solo)"
    )
    remix_parser.add_argument(
        "--title",
        default="GOBI AI REVIEW",
        help="Tiêu đề hiển thị trên header TikTok Safe Zone"
    )
    remix_parser.add_argument(
        "--out",
        default=None,
        help="Tên file video MP4 đầu ra mong muốn"
    )
    remix_parser.add_argument(
        "--force-type",
        choices=["talking_head", "product_only"],
        default=None,
        help="Ghi đè kết quả tự động phát hiện loại video (bỏ qua classifier)"
    )
    remix_parser.set_defaults(func=cmd_remix_run)
    return remix_parser


def cmd_remix_run(args):
    """Handler thực thi lệnh `python -m gobi remix`."""
    if not args.product and not args.product_json:
        print("❌ Lỗi: cần truyền --product <mã_sp> hoặc --product-json <đường_dẫn>")
        return 1

    print("=" * 60)
    print("🎭 GOBI CONTENT REMIX PIPELINE ACTIVATED")
    print(f"[*] Video tham khảo   : {args.ref}")
    print(f"[*] Sản phẩm          : {args.product or args.product_json}")
    print(f"[*] Nhân vật AI KOC   : {args.character}")
    print(f"[*] Bố cục HyperFrames: {args.layout}")
    print("=" * 60)

    content_wf = ContentRemixWorkflow()

    # Nạp dữ liệu sản phẩm thật (dùng chung cho cả 2 pipeline)
    try:
        if args.product_json:
            product_data = content_wf.load_product_data_from_json(args.product_json)
        else:
            product_data = content_wf.load_product_data(args.product)
    except Exception as e:
        print(f"❌ Lỗi nạp dữ liệu sản phẩm: {e}")
        return 1

    # Tải video tham khảo 1 lần (file local thì chỉ copy, không tải lại ở bước sau)
    import tempfile
    classify_dir = Path(tempfile.mkdtemp(prefix="gobi_remix_classify_"))
    try:
        local_ref_path = video_ingest.ingest_reference_video(args.ref, classify_dir, content_wf.workspace_root)
    except Exception as e:
        print(f"❌ Lỗi tải video tham khảo: {e}")
        return 1

    if args.force_type:
        video_type = args.force_type
        print(f"[*] Loại video: ÉP BUỘC = {video_type} (--force-type)")
    else:
        video_ingest.extract_audio(local_ref_path, classify_dir / "classify_audio.mp3")
        transcript = ""
        try:
            transcript = content_wf.preprocessor.transcribe_audio(str(classify_dir / "classify_audio.mp3"))
        except Exception:
            pass
        classification = classify_reference_video(local_ref_path, transcript)
        video_type = classification["video_type"]
        print(
            f"[*] Phát hiện: video dạng '{video_type}' "
            f"(face_ratio={classification['face_presence_ratio']}, "
            f"face_area={classification['avg_face_area_ratio']}, "
            f"has_speech={classification['has_speech']})"
        )

    if video_type == "product_only":
        simple_wf = SimpleEditWorkflow()
        result = simple_wf.execute(
            reference_video_path_or_url=args.ref,
            product_data=product_data,
            title_badge=args.title,
            output_filename=args.out,
            pre_ingested_ref_path=local_ref_path
        )
    else:
        remix_input = ContentRemixInput(
            reference_video_path_or_url=str(local_ref_path),
            product_code=args.product,
            product_info_path=args.product_json,
            character_avatar_path=args.character,
            layout_mode=MimicLayoutMode(args.layout),
            audio_strategy=AudioStrategy.OMNIVOICE_CLONE,
            title_badge=args.title,
            output_filename=args.out
        )
        result = content_wf.execute(remix_input)

    if result.is_success:
        print("\n" + "=" * 60)
        print("🎉 QUY TRÌNH HOÀN TẤT THÀNH CÔNG!")
        print(f"[+] Video Master hoàn chỉnh: {result.output_video_path}")
        print(f"[+] HyperFrames Project     : {result.hyperframes_project_dir}")
        print(f"[+] Thời lượng video        : {result.duration_seconds:.1f}s")
        if result.remix_script:
            print(f"[+] Hook kịch bản           : {result.remix_script.hook}")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ QUY TRÌNH THẤT BẠI:")
        print(f"[!] Lỗi: {result.metadata.get('error')}")
        print("=" * 60)
        return 1
