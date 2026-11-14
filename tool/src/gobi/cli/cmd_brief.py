"""
=============================================================================
CLI SUBCOMMAND: GOBI BRIEF (chỉ phân tích, KHÔNG render)
Dựa vào 1 video tham khảo + dữ liệu sản phẩm thật, phân loại loại video và
viết kịch bản mới qua Gemini — in ra JSON để Dashboard/Claude đọc và tự vận
hành EGO Lite/Google Flow tạo video AI thật (không chạy pipeline render ở đây).
=============================================================================
"""

import json
import sys
import tempfile
from pathlib import Path

from gobi.services.media import video_ingest
from gobi.services.media.video_classifier import classify_reference_video
from gobi.services.workflows.content_remix_workflow import ContentRemixWorkflow


def register_brief_parser(subparsers):
    """Đăng ký parser cho lệnh `python -m gobi brief`."""
    brief_parser = subparsers.add_parser(
        "brief",
        help="Phân tích video tham khảo + sản phẩm, in ra JSON kịch bản (không render video)"
    )
    brief_parser.add_argument("--ref", required=True, help="Video mẫu nội bộ hoặc URL TikTok/YouTube")
    brief_parser.add_argument("--product", default=None, help="Mã sản phẩm trong configs/products/catalog/")
    brief_parser.add_argument("--product-json", default=None, help="Đường dẫn file JSON product_info trực tiếp")
    brief_parser.add_argument("--character", default="gobi_lyly", help="Preset nhân vật (gobi_lyly, gobi_neau)")
    brief_parser.set_defaults(func=cmd_brief_run)
    return brief_parser


def cmd_brief_run(args):
    """Handler thực thi lệnh `python -m gobi brief`. In 1 dòng JSON duy nhất ra stdout."""
    if not args.product and not args.product_json:
        print(json.dumps({"success": False, "error": "Cần --product hoặc --product-json"}))
        return 1

    wf = ContentRemixWorkflow()

    try:
        if args.product_json:
            product_data = wf.load_product_data_from_json(args.product_json)
        else:
            product_data = wf.load_product_data(args.product)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Lỗi nạp dữ liệu sản phẩm: {e}"}))
        return 1

    tmp_dir = Path(tempfile.mkdtemp(prefix="gobi_brief_"))
    try:
        ref_path = video_ingest.ingest_reference_video(args.ref, tmp_dir, wf.workspace_root)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Lỗi tải video tham khảo: {e}"}))
        return 1

    video_ingest.extract_audio(ref_path, tmp_dir / "audio.mp3")
    transcript = ""
    try:
        transcript = wf.preprocessor.transcribe_audio(str(tmp_dir / "audio.mp3"))
    except Exception:
        pass

    classification = classify_reference_video(ref_path, transcript)

    try:
        from gobi.adapters.integrations.gemini_text_adapter import GeminiTextAdapter
        gemini = GeminiTextAdapter()
        script = gemini.generate_remix_script(
            reference_transcript=transcript,
            product_info=product_data["product_info"],
            existing_koc_script=product_data.get("existing_koc_script"),
        )
    except Exception as gemini_error:
        # Gemini hết quota/lỗi -> tự động fallback sang Ollama cục bộ (deepseek-r1),
        # không chặn cả pipeline chỉ vì hết quota free-tier Gemini.
        try:
            from gobi.adapters.integrations.ollama_text_adapter import OllamaTextAdapter
            print(f"[cmd_brief] Gemini lỗi ({gemini_error}) — fallback sang Ollama local...", file=sys.stderr)
            ollama = OllamaTextAdapter()
            script = ollama.generate_remix_script(
                reference_transcript=transcript,
                product_info=product_data["product_info"],
                existing_koc_script=product_data.get("existing_koc_script"),
            )
        except Exception as ollama_error:
            print(json.dumps({
                "success": False,
                "error": f"Lỗi gọi Gemini ({gemini_error}) và Ollama fallback ({ollama_error})",
            }))
            return 1

    voice_profile_id = wf.resolve_voice_profile_id(args.character) or "voice-fm-lyly"
    character_avatar = str(wf.resolve_character_avatar(args.character))

    result = {
        "success": True,
        "video_type": classification["video_type"],
        "classification": classification,
        "reference_transcript": transcript,
        "product_info": product_data["product_info"],
        "character": args.character,
        "character_avatar_path": character_avatar,
        "voice_profile_id": voice_profile_id,
        "hook": script.hook,
        "beats": [{"beat_name": b.beat_name, "voiceover_line": b.voiceover_line} for b in script.beats],
        "cta": script.cta,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0
