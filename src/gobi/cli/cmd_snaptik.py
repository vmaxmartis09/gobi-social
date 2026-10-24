"""CLI handler for SnapTik TikTok video downloader."""

import argparse
import json
import os
import sys
from pathlib import Path

from gobi.services.media.snaptik_service import SnaptikService


def format_number(num: int) -> str:
    """Format large numbers with readable suffixes (K, M)."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def print_progress(downloaded: int, total: int):
    """Simple terminal progress indicator."""
    if total > 0:
        pct = (downloaded / total) * 100
        mb_down = downloaded / (1024 * 1024)
        mb_total = total / (1024 * 1024)
        bar_len = 30
        filled = int(bar_len * downloaded // total)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(f"\r  [{bar}] {pct:5.1f}% ({mb_down:.2f}/{mb_total:.2f} MB)")
        sys.stdout.flush()
        if downloaded >= total:
            sys.stdout.write("\n")


def handle_snaptik_command(args: argparse.Namespace) -> int:
    """Entry point for `gobi snaptik ...` subcommand."""
    # Web UI mode
    if getattr(args, "web", False):
        from gobi.services.media.snaptik_web import run_web_server
        port = getattr(args, "port", 8088)
        run_web_server(host="0.0.0.0", port=port)
        return 0

    service = SnaptikService()

    # Batch mode
    batch_file = getattr(args, "batch", None)
    if batch_file:
        b_path = Path(batch_file)
        if not b_path.exists():
            print(f"[!] File không tồn tại: {batch_file}", file=sys.stderr)
            return 1
        with open(b_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"[*] Bắt đầu tải hàng loạt {len(urls)} video TikTok...")
        results = service.download_batch(
            urls,
            output_dir=args.output or "output/videos",
            download_audio=args.audio,
            download_cover=args.cover,
            watermark=args.watermark,
        )
        success_count = sum(1 for r in results if r.success)
        print(f"\n[+] Hoàn thành: {success_count}/{len(urls)} video tải thành công!")
        return 0 if success_count == len(urls) else 1

    # Single URL mode
    url = getattr(args, "url", None)
    if not url:
        print("[!] Vui lòng cung cấp link TikTok hoặc chạy `gobi snaptik --web` để mở giao diện web.", file=sys.stderr)
        return 1

    # Product Ingestion Integration mode (-p / --to-product)
    if getattr(args, "to_product", False):
        print(f"[*] Đang trích xuất giỏ hàng TikTok Shop & tải video đóng gói vào folder sản phẩm...")
        from gobi.services.product.ingestion import ingest_tiktok_product
        base_dir = getattr(args, "product_dir", None) or "data/products"
        ingest_res = ingest_tiktok_product(
            video_url=url,
            base_dir=base_dir,
            download_cover=True,
            download_video=True,
            download_audio=getattr(args, "audio", True)
        )
        if getattr(args, "json", False):
            import json
            print(json.dumps(ingest_res, indent=2, ensure_ascii=False))
            return 0 if ingest_res.get("success") else 1

        if not ingest_res.get("success"):
            print(f"[!] {ingest_res.get('error')}", file=sys.stderr)
            print("[*] Video không có giỏ hàng TikTok Shop. Chuyển sang tải source video thông thường vào output/videos/...")
        else:
            print("\n" + "🎉 " + "=" * 65)
            print("ĐÃ TRÍCH XUẤT THÀNH CÔNG SẢN PHẨM & ĐÓNG GÓI VÀO HỆ THỐNG FOLDER")
            print("=" * 68)
            for idx, p in enumerate(ingest_res["products"], 1):
                print(f"📦 [SẢN PHẨM {idx}]: {p['title']}")
                print(f"   ├─ Product ID      : {p['product_id']}")
                print(f"   ├─ Link TikTok Shop: {p['pdp_url']}")
                print(f"   ├─ Link Affiliate  : {p['affiliate_pdp_url']}")
                print(f"   ├─ Thư mục lưu trữ : {p['folder']}")
                print(f"   ├─ Source video MP4: {p['folder']}/video_clean.mp4")
                print(f"   ├─ File audio MP3  : {p['folder']}/video_clean_audio.mp3")
                print(f"   ├─ Ảnh bìa sản phẩm: {p['folder']}/cover.jpg")
                print(f"   └─ File metadata   : {p['metadata_file']} & README.md")
            print(f"\n📚 Sổ cái Warehouse Catalog: {ingest_res['catalog_file']}")
            print("=" * 68 + "\n")
            return 0

    # Info-only mode
    if getattr(args, "info", False):
        print(f"[*] Đang lấy thông tin video từ: {url}")
        try:
            info = service.get_info(url)
            if getattr(args, "json", False):
                print(info.model_dump_json(indent=2))
                return 0

            print("\n" + "=" * 60)
            print(f"🎬 TIÊU ĐỀ: {info.title or '(Không có tiêu đề)'}")
            print(f"👤 TÁC GIẢ: {info.author.nickname or 'N/A'} (@{info.author.unique_id or 'unknown'})")
            print(f"⏱️ THỜI LƯỢNG: {info.duration} giây")
            print(f"📊 THỐNG KÊ: {format_number(info.stats.plays)} lượt xem | {format_number(info.stats.likes)} tim | {format_number(info.stats.comments)} bình luận | {format_number(info.stats.shares)} chia sẻ")
            print(f"⚙️ ENGINE NGUỒN: {info.source_engine}")
            print("-" * 60)
            print(f"🔗 LINK TẢI VIDEO (KHÔNG LOGO): {info.media.video_url or 'N/A'}")
            if info.media.video_hd_url:
                print(f"🔗 LINK TẢI HD: {info.media.video_hd_url}")
            if info.media.audio_url:
                print(f"🎵 LINK NHẠC/AUDIO MP3: {info.media.audio_url}")
            if info.media.cover_url:
                print(f"🖼️ LINK ẢNH BÌA: {info.media.cover_url}")
            if info.is_slideshow:
                print(f"📸 ẢNH SLIDESHOW: {len(info.media.images)} ảnh")
            print("=" * 60 + "\n")
            return 0
        except Exception as e:
            print(f"[!] Lỗi khi lấy thông tin video: {e}", file=sys.stderr)
            return 1

    # Download mode
    print(f"[*] Đang phân tích và tải video từ: {url}")
    target_out = args.output or "output/videos"
    hd = not getattr(args, "no_hd", False)

    res = service.download(
        url=url,
        output_dir=target_out if not target_out.endswith(".mp4") else "output/videos",
        filename=target_out if target_out.endswith(".mp4") else None,
        watermark=getattr(args, "watermark", False),
        hd=hd,
        download_audio=getattr(args, "audio", False),
        download_cover=getattr(args, "cover", False),
        save_metadata=True,
        on_progress=print_progress if not getattr(args, "json", False) else None,
    )

    if getattr(args, "json", False):
        print(res.model_dump_json(indent=2))
        return 0 if res.success else 1

    if res.success:
        print("\n" + "🎉 " + "=" * 55)
        print("TẢI SOURCE VIDEO TIKTOK THÀNH CÔNG (CHUẨN SNAPTIK)")
        print("=" * 58)
        if res.info:
            print(f"📌 Tiêu đề: {res.info.title[:65]}")
            print(f"👤 Kênh: {res.info.author.nickname} (@{res.info.author.unique_id})")
            print(f"📈 Tương tác: {format_number(res.info.stats.plays)} views | {format_number(res.info.stats.likes)} likes")
        if res.video_path:
            size_mb = os.path.getsize(res.video_path) / (1024 * 1024)
            print(f"🎥 Video (Sạch Không Logo): {res.video_path} ({size_mb:.2f} MB)")
        if res.audio_path:
            print(f"🎵 Audio MP3: {res.audio_path}")
        if res.cover_path:
            print(f"🖼️ Ảnh bìa: {res.cover_path}")
        if res.metadata_path:
            print(f"📋 Metadata JSON: {res.metadata_path}")
        if res.image_paths:
            print(f"📸 Ảnh slides: {len(res.image_paths)} ảnh")
        print("=" * 58 + "\n")
        return 0
    else:
        print(f"[!] Tải thất bại: {res.error}", file=sys.stderr)
        return 1
