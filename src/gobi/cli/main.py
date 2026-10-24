"""Gobi Social Unified CLI - Entrypoint for video, voice, prompt, policy, and learning pipelines."""
import argparse
import sys

def cmd_policy(args):
    from gobi.domain.policy_compliance_checker import scan_text_compliance
    res = scan_text_compliance(args.script)
    status = "HOÀN HẢO" if res["is_compliant"] else "CẢNH BÁO VI PHẠM"
    print(f"[*] Trạng thái tuân thủ: {status} ({res['total_violations']} vi phạm)")
    for v in res["details"]:
        print(f"  - [{v['category']}] {v['detected']} -> {v['fix_suggestion']}")
    return 0 if res["is_compliant"] else 1

def cmd_prompt(args):
    from gobi.services.prompt.koc_prompt_generator import generate_kling_video_prompt, generate_tiktok_affiliate_package
    prompt = generate_kling_video_prompt(
        subject_action=f"Vietnamese female KOC smiling naturally, showcasing {args.product}",
        camera_move="push_in"
    )
    pkg = generate_tiktok_affiliate_package(
        product_name=args.product,
        price_sale="139.000đ",
        pain_point="mặc đồ đi làm bị đơn điệu"
    )
    print("\n[+] 4K CINEMATIC PROMPT:\n", prompt)
    print("\n[+] TIKTOK HOOK (0:00-0:03):\n", pkg["video_structure"][0]["voiceover"])
    print("\n[+] CTA GIỎ HÀNG (0:25-0:30):\n", pkg["video_structure"][-1]["voiceover"])
    return 0



def cmd_voice(args):
    import asyncio
    from gobi.services.voice.generate_gobi_voice import generate_voiceover
    asyncio.run(generate_voiceover(args.text, args.output, voice=args.voice))
    print(f"[+] Audio voiceover saved to: {args.output}")
    return 0

def cmd_learn(args):
    from gobi.services.intelligence.continuous_learning_engine import ContinuousLearningEngine
    engine = ContinuousLearningEngine()
    engine.run_interactive_cycle()
    return 0

def cmd_video(args):
    action = getattr(args, "action", "render")
    engine_choice = getattr(args, "engine", "hyperframes")

    if action == "preview":
        from gobi.services.media.hyperframes_engine import HyperFramesEngine
        engine = HyperFramesEngine()
        proj_dir = getattr(args, "project", None) or "output/hyperframes_projects/demo"
        print(f"[*] Mở Studio Live Preview HyperFrames tại: {proj_dir}...")
        proc = engine.preview(proj_dir)
        proc.wait()
        return 0

    if engine_choice == "hyperframes":
        from gobi.services.media.hyperframes_engine import HyperFramesEngine
        engine = HyperFramesEngine()
        proj_dir = getattr(args, "project", None)
        out_file = getattr(args, "output", None)
        quality = getattr(args, "quality", "looks")

        if proj_dir and os.path.exists(proj_dir):
            print(f"[*] Đang render project HyperFrames: {proj_dir}...")
            res = engine.render_project(proj_dir, out_file, quality=quality)
            print(f"[+] Video đã hoàn thành: {res}")
            return 0
        else:
            print("[*] Render video mẫu Gobi Flow + LyLy voice với HyperFrames Engine...")
            from gobi.services.media.render_gobi_flow_real_video import FLOW_V1, FLOW_V2, VOICEOVER, BGM, OUTPUT_DIR
            scenes = [
                {"video": str(FLOW_V2), "sub": "Chất thun Nunu bodyfit co giãn 4 chiều cực đỉnh!", "duration": 4.5},
                {"video": str(FLOW_V1), "sub": "Tôn dáng chuẩn từng đường nét, thoáng mát cả ngày.", "duration": 5.5}
            ]
            res = engine.create_and_render_video(
                scenes=scenes,
                audio_voiceover_path=str(VOICEOVER) if os.path.exists(VOICEOVER) else "output/lyly_neau_review.mp3",
                output_mp4=out_file or str(OUTPUT_DIR / "gobi_hyperframes_official_master.mp4"),
                title_badge="ÁO THUN NUNU BODYFIT GÔ BI",
                bgm_path=str(BGM) if os.path.exists(BGM) else None,
                temp_project_name="gobi_hyperframes_nunu_master",
                quality=quality
            )
            print(f"[+] Video Master hoàn thành với HyperFrames: {res}")
            return 0
    else:
        # Legacy fallback
        if action == "render":
            from gobi.services.media.render_gobi_boutique_v1 import main as render_main
            render_main()
        elif action == "concat":
            from gobi.services.media.ai_concat_auto_editor import main as concat_main
            concat_main()
    return 0

def cmd_product(args):
    from gobi.services.product.ingestion import ingest_tiktok_product, get_product_catalog
    import json
    
    if args.action == "list":
        catalog = get_product_catalog()
        products = catalog.get("products", {})
        if not products:
            print("[i] Chưa có sản phẩm nào trong data/products/catalog.json.")
            return 0
        print(f"[+] Danh sách {len(products)} sản phẩm đã chuẩn hóa trong data/products/:")
        for pid, p in products.items():
            print(f"  * [{pid}] {p.get('title')} (Creator: @{p.get('author')})")
            print(f"    - Link Shop: {p.get('pdp_url')}")
            print(f"    - Folder   : {p.get('folder')}")
        return 0
        
    elif args.action == "ingest":
        if not getattr(args, "url", None):
            print("[!] Thiếu URL video TikTok để nạp sản phẩm.")
            return 1
        url = args.url
        if not args.json:
            print(f"[*] Đang chuẩn hoá và nạp dữ liệu từ video: {url}...")
        ingest_res = ingest_tiktok_product(
            video_url=url,
            base_dir=getattr(args, "dir", "data/products"),
            download_cover=True,
            download_video=getattr(args, "video", False)
        )
        if args.json:
            print(json.dumps(ingest_res, indent=2, ensure_ascii=False))
            return 0 if ingest_res.get("success") else 1
            
        if not ingest_res.get("success"):
            print(f"[!] Thất bại: {ingest_res.get('error')}")
            return 1
            
        print(f"\n[+] ĐÃ CHUẨN HOÁ & NẠP THÀNH CÔNG {ingest_res['total_ingested']} SẢN PHẨM VÀO DATA:")
        for idx, p in enumerate(ingest_res["products"], 1):
            print(f"\n--- [SẢN PHẨM {idx}] ---")
            print(f"  * Tên sản phẩm   : {p['title']}")
            print(f"  * Product ID     : {p['product_id']}")
            print(f"  * Link Shop chuẩn : {p['pdp_url']}")
            print(f"  * Link Affiliate  : {p['affiliate_pdp_url']}")
            print(f"  * Folder lưu trữ : {p['folder']}")
            print(f"  * File metadata  : {p['metadata_file']}")
            print(f"  * Đã tải ảnh bìa : {'Có (cover.jpg)' if p['cover_downloaded'] else 'Không'}")
        print(f"\n[*] Sổ cái Catalog: {ingest_res['catalog_file']}")
        return 0
    return 0

def cmd_tiktok(args):
    from gobi.adapters.platforms.tiktok.product_extractor import extract_tiktok_shop_products
    from gobi.services.product.ingestion import ingest_tiktok_product
    import json
    
    url = args.url
    
    # Nếu có cờ --ingest (tự động nạp vào data có folder chứa)
    if getattr(args, "ingest", False):
        if not args.json:
            print(f"[*] Đang chuẩn hoá và nạp dữ liệu từ video: {url}...")
        ingest_res = ingest_tiktok_product(
            video_url=url,
            base_dir=getattr(args, "dir", "data/products"),
            download_cover=True,
            download_video=getattr(args, "download_video", False)
        )
        if args.json:
            print(json.dumps(ingest_res, indent=2, ensure_ascii=False))
            return 0 if ingest_res.get("success") else 1
            
        if not ingest_res.get("success"):
            print(f"[!] Thất bại: {ingest_res.get('error')}")
            return 1
            
        print(f"\n[+] ĐÃ CHUẨN HOÁ & NẠP THÀNH CÔNG {ingest_res['total_ingested']} SẢN PHẨM VÀO DATA:")
        for idx, p in enumerate(ingest_res["products"], 1):
            print(f"\n--- [SẢN PHẨM {idx}] ---")
            print(f"  * Tên sản phẩm   : {p['title']}")
            print(f"  * Product ID     : {p['product_id']}")
            print(f"  * Link Shop chuẩn : {p['pdp_url']}")
            print(f"  * Folder lưu trữ : {p['folder']}")
            print(f"  * File metadata  : {p['metadata_file']}")
            print(f"  * Đã tải ảnh bìa : {'Có (cover.jpg)' if p['cover_downloaded'] else 'Không'}")
        print(f"\n[*] Sổ cái Catalog: {ingest_res['catalog_file']}")
        return 0

    if not args.json:
        print(f"[*] Đang trích xuất link TikTok Shop từ video: {url}...")
    res = extract_tiktok_shop_products(url)
    
    if not res.get("success"):
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"[!] Thất bại: {res.get('error')}")
        return 1
        
    if not res.get("has_shop_anchor"):
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"[i] Video không gắn giỏ hàng TikTok Shop.")
        return 0
        
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
        
    print(f"[+] Tìm thấy {res['total_products']} sản phẩm gắn trong video @{res['author']}:")
    for idx, p in enumerate(res["products"], 1):
        print(f"\n--- [SẢN PHẨM {idx}] ---")
        print(f"  * Tên sản phẩm   : {p['title']}")
        print(f"  * Nhãn giỏ hàng  : {p['keyword']}")
        print(f"  * Product ID     : {p['product_id']}")
        print(f"  * Link Shop chuẩn : {p['pdp_url']}")
        if p.get('affiliate_pdp_url'):
            print(f"  * Link Affiliate  : {p['affiliate_pdp_url']}")
        print(f"  * Ảnh sản phẩm   : {p['cover_url']}")
    return 0

def main():
    parser = argparse.ArgumentParser(prog="gobi", description="Gobi Social Autonomous AI KOC Pipeline CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # gobi policy check --script "..."
    p_policy = subparsers.add_parser("policy", help="Quét vi phạm chính sách & Safe Zone TikTok Shop")
    p_policy.add_argument("action", choices=["check"], default="check", nargs="?")
    p_policy.add_argument("--script", required=True, help="Nội dung kịch bản cần kiểm tra")
    p_policy.set_defaults(func=cmd_policy)

    # gobi prompt [generate]
    p_prompt = subparsers.add_parser("prompt", help="Sinh prompt ma trận 36 góc quay camera")
    p_prompt.add_argument("--angle", type=int, default=1, help="Góc máy (1-36)")
    p_prompt.add_argument("--product", default="Áo cardigan len tăm thắt nơ kiểu Pháp", help="Tên sản phẩm")
    p_prompt.set_defaults(func=cmd_prompt)

    # gobi voice synth --text "..."
    p_voice = subparsers.add_parser("voice", help="Tổng hợp giọng nói KOC tiếng Việt chuẩn")
    p_voice.add_argument("action", choices=["synth"], default="synth", nargs="?")
    p_voice.add_argument("--text", required=True, help="Văn bản cần đọc")
    p_voice.add_argument("--output", default="output/voice_output.mp3", help="Đường dẫn file đầu ra")
    p_voice.add_argument("--voice", default="vi-VN-HoaiMyNeural", help="Giọng đọc Edge-TTS")
    p_voice.set_defaults(func=cmd_voice)

    # gobi learn [run]
    p_learn = subparsers.add_parser("learn", help="Chạy chu trình tự học và tối ưu trọng số prompt")
    p_learn.set_defaults(func=cmd_learn)

    # gobi video [render|preview|concat]
    p_video = subparsers.add_parser("video", help="Render video hoặc xem trước timeline tự động với HyperFrames")
    p_video.add_argument("action", choices=["render", "preview", "concat"], default="render", nargs="?")
    p_video.add_argument("--engine", choices=["hyperframes", "legacy"], default="hyperframes", help="Engine dựng video (mặc định: hyperframes)")
    p_video.add_argument("--project", "-p", help="Đường dẫn thư mục project HyperFrames (nếu render/preview project có sẵn)")
    p_video.add_argument("--output", "-o", help="Đường dẫn file MP4 xuất bản (mặc định: output/videos/...)")
    p_video.add_argument("--quality", "-q", choices=["draft", "looks", "delivery"], default="looks", help="Chất lượng render HyperFrames")
    p_video.set_defaults(func=cmd_video)

    # gobi account [list|emails|apply-domain|export|warmup|set-status]
    p_acc = subparsers.add_parser("account", help="Quản lý ma trận 12 tài khoản KOC 12 Chòm Sao")
    p_acc.add_argument("action", choices=["list", "emails", "apply-domain", "export", "warmup", "set-status"], default="list", nargs="?")
    p_acc.add_argument("--domain", default="shopgobi.com", help="Domain email của bạn (ví dụ: yourbrand.com)")
    p_acc.add_argument("--id", help="Mã tài khoản (ví dụ: gobi-aries)")
    p_acc.add_argument("--status", help="Trạng thái (PLANNED, WARMING_UP, ACTIVE, REVIEW, SUSPENDED)")
    p_acc.add_argument("--day", type=int, default=0, help="Ngày làm ấm tài khoản (0-5)")
    p_acc.add_argument("--format", choices=["csv", "json"], default="csv", help="Định dạng xuất file")
    p_acc.add_argument("--output", help="Đường dẫn lưu file xuất")
    from gobi.cli.cmd_account import handle_account_command
    p_acc.set_defaults(func=handle_account_command)

    # gobi snaptik [url]
    p_snaptik = subparsers.add_parser("snaptik", help="Tải source video TikTok không logo (SnapTik) vào project")
    p_snaptik.add_argument("url", nargs="?", help="Link video TikTok (ví dụ: https://www.tiktok.com/@user/video/...)")
    p_snaptik.add_argument("-o", "--output", help="Thư mục hoặc đường dẫn file lưu video (mặc định: output/videos/)")
    p_snaptik.add_argument("-p", "--to-product", "--product", dest="to_product", action="store_true", help="Trích xuất link sản phẩm TikTok Shop & đóng gói thành folder sản phẩm trong data/products/")
    p_snaptik.add_argument("--product-dir", default="data/products", help="Thư mục gốc lưu trữ kho sản phẩm (mặc định: data/products)")
    p_snaptik.add_argument("-i", "--info", action="store_true", help="Chỉ xem thông tin & thống kê video, không tải")
    p_snaptik.add_argument("-a", "--audio", action="store_true", help="Tải kèm file âm thanh MP3")
    p_snaptik.add_argument("-c", "--cover", action="store_true", help="Tải kèm ảnh bìa video (Cover)")
    p_snaptik.add_argument("-wm", "--watermark", action="store_true", help="Tải video có logo watermark")
    p_snaptik.add_argument("--no-hd", action="store_true", help="Không ưu tiên định dạng HD")
    p_snaptik.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON")
    p_snaptik.add_argument("-b", "--batch", help="File txt chứa danh sách link TikTok tải hàng loạt")
    p_snaptik.add_argument("--web", action="store_true", help="Khởi chạy giao diện SnapTik Web UI trên trình duyệt")
    p_snaptik.add_argument("--port", type=int, default=8088, help="Cổng mạng cho Web UI (mặc định: 8088)")
    from gobi.cli.cmd_snaptik import handle_snaptik_command
    p_snaptik.set_defaults(func=handle_snaptik_command)

    # gobi tiktok product <url> [--ingest] [--dir DIR] [--video]
    p_tiktok = subparsers.add_parser("tiktok", help="Công cụ TikTok (Lấy link sản phẩm TikTok Shop từ video)")
    p_tiktok.add_argument("action", choices=["product"], default="product", nargs="?", help="Hành động (mặc định: product)")
    p_tiktok.add_argument("url", help="Link video TikTok (ví dụ: https://www.tiktok.com/@user/video/...)")
    p_tiktok.add_argument("--ingest", action="store_true", help="Tự động chuẩn hóa và nạp vào folder data/products")
    p_tiktok.add_argument("--dir", default="data/products", help="Thư mục đích lưu trữ sản phẩm (mặc định: data/products)")
    p_tiktok.add_argument("--download-video", action="store_true", help="Tải kèm video gốc không logo vào thư mục sản phẩm")
    p_tiktok.add_argument("--json", action="store_true", help="Xuất định dạng JSON chi tiết")
    p_tiktok.set_defaults(func=cmd_tiktok)

    # gobi product [ingest|list]
    p_prod = subparsers.add_parser("product", help="Quản lý và nạp dữ liệu sản phẩm TikTok Shop vào data")
    p_prod.add_argument("action", choices=["ingest", "list"], default="ingest", nargs="?", help="Hành động: ingest (nạp link) hoặc list (xem danh sách)")
    p_prod.add_argument("url", nargs="?", help="Link video TikTok cần nạp sản phẩm")
    p_prod.add_argument("--dir", default="data/products", help="Thư mục đích lưu trữ sản phẩm (mặc định: data/products)")
    p_prod.add_argument("--video", action="store_true", help="Tải kèm video không logo vào thư mục sản phẩm")
    p_prod.add_argument("--json", action="store_true", help="Xuất định dạng JSON chi tiết")
    p_prod.set_defaults(func=cmd_product)

    # gobi warehouse [list|get|update-status|assign|rebuild]
    from gobi.cli.cmd_product import handle_product_cli
    p_wh = subparsers.add_parser("warehouse", help="Quản trị kho sản phẩm KOC AI (Mã SP, Status, Assigned KOC)")
    wh_sub = p_wh.add_subparsers(dest="product_action", help="Thao tác kho")
    
    list_p = wh_sub.add_parser("list", help="Xem danh sách sản phẩm trong kho")
    list_p.add_argument("--status", choices=["chua_lam", "dang_lam", "da_dang_video"], help="Lọc theo trạng thái")
    list_p.add_argument("--koc", help="Lọc theo KOC AI phụ trách")

    get_p = wh_sub.add_parser("get", help="Xem chi tiết một sản phẩm theo mã")
    get_p.add_argument("code", help="Mã sản phẩm (ví dụ: SP-BJ-001)")

    up_p = wh_sub.add_parser("update-status", help="Cập nhật trạng thái sản xuất")
    up_p.add_argument("code", help="Mã sản phẩm")
    up_p.add_argument("status", choices=["chua_lam", "dang_lam", "da_dang_video"], help="Trạng thái mới")
    up_p.add_argument("--video-url", help="Link video TikTok sau khi đăng")

    assign_p = wh_sub.add_parser("assign", help="Phân công KOC phụ trách sản phẩm")
    assign_p.add_argument("code", help="Mã sản phẩm")
    assign_p.add_argument("koc", help="Handle KOC AI (ví dụ: @gobiboutique)")

    wh_sub.add_parser("rebuild", help="Tái tạo chỉ mục warehouse_index.json")
    p_wh.set_defaults(func=handle_product_cli)

    # gobi mimic --ref <url_or_path> [--character <name>] [--layout <solo|split_3_tier|side_by_side>]
    from gobi.cli.cmd_mimic import register_mimic_parser
    register_mimic_parser(subparsers)

    # gobi remix --ref <url_or_path> --product <code> [--character <name>] [--layout <...>]
    from gobi.cli.cmd_remix import register_remix_parser
    register_remix_parser(subparsers)

    # gobi brief --ref <url_or_path> --product <code> [--character <name>]
    from gobi.cli.cmd_brief import register_brief_parser
    register_brief_parser(subparsers)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
