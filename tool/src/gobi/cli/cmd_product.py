"""CLI subcommand for managing KOC product warehouse."""

import argparse
from gobi.services.product_manager import ProductManager
from gobi.domain.product_models import ProductStatus


def add_product_subparser(subparsers):
    """Đăng ký subparser cho lệnh `gobi product`."""
    prod_parser = subparsers.add_parser("product", help="Quản trị kho sản phẩm KOC AI & tiến độ video")
    prod_subparsers = prod_parser.add_subparsers(dest="product_action", help="Hành động trên sản phẩm")

    # list
    list_p = prod_subparsers.add_parser("list", help="Liệt kê danh sách sản phẩm trong kho")
    list_p.add_argument("--status", choices=["chua_lam", "dang_lam", "da_dang_video"], help="Lọc theo trạng thái")
    list_p.add_argument("--koc", help="Lọc theo KOC AI phụ trách (ví dụ: @gobiboutique)")

    # get
    get_p = prod_subparsers.add_parser("get", help="Xem chi tiết một sản phẩm theo mã")
    get_p.add_argument("code", help="Mã sản phẩm (ví dụ: SP-BJ-001)")

    # update-status
    up_p = prod_subparsers.add_parser("update-status", help="Cập nhật trạng thái sản xuất")
    up_p.add_argument("code", help="Mã sản phẩm")
    up_p.add_argument("status", choices=["chua_lam", "dang_lam", "da_dang_video"], help="Trạng thái mới")
    up_p.add_argument("--video-url", help="Link video TikTok sau khi đăng")

    # assign
    assign_p = prod_subparsers.add_parser("assign", help="Phân công KOC phụ trách sản phẩm")
    assign_p.add_argument("code", help="Mã sản phẩm")
    assign_p.add_argument("koc", help="Handle KOC AI (ví dụ: @gobiboutique)")

    # rebuild
    prod_subparsers.add_parser("rebuild", help="Tái tạo lại file chỉ mục warehouse_index.json")


def handle_product_cli(args):
    """Xử lý thực thi lệnh product CLI."""
    manager = ProductManager()
    action = getattr(args, "product_action", "list")

    if action == "list":
        products = manager.load_all_products()
        if getattr(args, "status", None):
            products = [p for p in products if p.production.status.value == args.status]
        if getattr(args, "koc", None):
            products = [p for p in products if p.production.assigned_koc == args.koc]

        print("\n" + "=" * 80)
        print(f"📦 KHO SẢN PHẨM GOBI SOCIAL (Tổng số: {len(products)} sản phẩm)")
        print("=" * 80)
        for p in products:
            st = p.production.status.value
            st_badge = {
                "chua_lam": "⏳ CHƯA LÀM",
                "dang_lam": "🔄 ĐANG LÀM",
                "da_dang_video": "✅ ĐÃ ĐĂNG VIDEO",
            }.get(st, st)
            print(f"[{p.product_code}] {p.product_name}")
            print(f"  ├─ Trạng thái: {st_badge}")
            print(f"  ├─ Phân công KOC: {p.production.assigned_koc}")
            print(f"  ├─ Giá bán: {p.pricing.price_vnd:,}đ | Hoa hồng: {p.pricing.commission_rate_percent}% ({p.pricing.commission_per_order_vnd:,}đ/đơn)")
            print(f"  ├─ Folder: {p.folder_path}")
            if p.production.published_video_url:
                print(f"  └─ TikTok Video: {p.production.published_video_url}")
            else:
                print(f"  └─ Benchmark: {p.production.benchmark_video_url or 'N/A'}")
            print("-" * 80)
        return 0

    elif action == "get":
        p = manager.get_product(args.code)
        if not p:
            print(f"[!] Không tìm thấy sản phẩm có mã: {args.code}")
            return 1
        print("\n" + "=" * 80)
        print(f"📋 CHI TIẾT SẢN PHẨM: {p.product_code} - {p.product_name}")
        print("=" * 80)
        print(f"• Ngành hàng: {p.category.value}")
        print(f"• Shop cung ứng: {p.specs.origin_shop}")
        print(f"• Giá bán: {p.pricing.price_vnd:,}đ (Giá gốc: {p.pricing.original_price_vnd or 0:,}đ)")
        print(f"• Hoa hồng: {p.pricing.commission_rate_percent}% -> {p.pricing.commission_per_order_vnd:,}đ/đơn")
        print(f"• Chất liệu: {p.specs.material}")
        print(f"• Màu sắc: {', '.join(p.specs.colors)}")
        print(f"• Kích cỡ: {', '.join(p.specs.sizes)}")
        print(f"• Trạng thái sản xuất: {p.production.status.value.upper()}")
        print(f"• KOC phụ trách: {p.production.assigned_koc}")
        print(f"• Format video: {p.production.winning_format}")
        print(f"• VMAX Panels: {', '.join(p.production.vmax_panels)}")
        print(f"• Thư mục lưu trữ: {p.folder_path}")
        print("\n[🎯 TỐI ƯU SEO TIKTOK]")
        print(f"• Từ khóa chính: {', '.join(p.seo.primary_keywords)}")
        print(f"• Hashtags: {' '.join(p.seo.hashtags)}")
        print(f"• Caption mẫu:\n  {p.seo.caption_template}")
        print("=" * 80)
        return 0

    elif action == "update-status":
        st = ProductStatus(args.status)
        p = manager.update_status(args.code, st, video_url=getattr(args, "video_url", None))
        if not p:
            print(f"[!] Lỗi: Không tìm thấy sản phẩm {args.code}")
            return 1
        print(f"[+] Đã cập nhật trạng thái {args.code} -> {st.value.upper()}")
        if getattr(args, "video_url", None):
            print(f"    Link video: {args.video_url}")
        return 0

    elif action == "assign":
        p = manager.assign_koc(args.code, args.koc)
        if not p:
            print(f"[!] Lỗi: Không tìm thấy sản phẩm {args.code}")
            return 1
        print(f"[+] Đã phân công sản phẩm {args.code} cho KOC: {args.koc}")
        return 0

    elif action == "rebuild":
        manifest = manager.rebuild_warehouse_index()
        print(f"[+] Đã tái tạo chỉ mục kho: {manifest.total_products} sản phẩm.")
        print(f"    Thống kê: {manifest.status_summary}")
        return 0

    return 0
