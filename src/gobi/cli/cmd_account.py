"""Gobi CLI Subcommand - Account Management for Zodiac KOC TikTok Matrix."""
import sys
from pathlib import Path
from gobi.services.account_manager import ZodiacAccountManager, WARMUP_PROTOCOLS
from gobi.domain.account_models import AccountStatus

def handle_account_command(args):
    mgr = ZodiacAccountManager()

    if args.action == "list":
        accounts = mgr.list_accounts()
        print("\n" + "=" * 88)
        print(f"🌟 BẢNG QUẢN TRỊ MA TRẬN 12 TÀI KHOẢN KOC GÔ BI - 12 CHÒM SAO")
        print("=" * 88)
        header = f"{'STT':<4} | {'MÃ PROFILE':<18} | {'CHÒM SAO':<14} | {'HANDLE TIKTOK':<16} | {'TRẠNG THÁI':<12} | {'NGÀY'}"
        print(header)
        print("-" * 88)
        for i, acc in enumerate(accounts, 1):
            email = acc.assigned_email or f"{acc.email_prefix}@<chưa gán domain>"
            zodiac_str = f"{acc.symbol} {acc.zodiac_name_vi}"
            status_str = f"{acc.status.value}"
            print(f"{i:<4} | {acc.account_id:<18} | {zodiac_str:<14} | {acc.handle:<16} | {status_str:<12} | Day {acc.warmup_day}")
            print(f"     └── Email: {email} | Niche: {acc.niche_fashion[:45]}...")
        print("=" * 88)
        print("💡 Gợi ý lệnh: python -m gobi account emails --domain shopgobi.com")
        print("=" * 88 + "\n")
        return 0

    elif args.action == "emails":
        domain = getattr(args, "domain", "shopgobi.com")
        matrix = mgr.generate_email_list(domain)
        print(f"\n[+] DANH SÁCH 12 ĐỊA CHỈ EMAIL THEO CHÒM SAO (Domain: @{domain.lstrip('@')}):")
        print("-" * 75)
        for item in matrix:
            print(f"  • {item['zodiac']:<22} ->  {item['email']:<30} (Handle: {item['handle']})")
        print("-" * 75)
        print("👉 Bạn chỉ cần copy danh sách email này vào Cloudflare Email Routing hoặc form đăng ký TikTok.\n")
        return 0

    elif args.action == "apply-domain":
        domain = getattr(args, "domain", None)
        if not domain:
            print("[!] Lỗi: Vui lòng cung cấp --domain (ví dụ: --domain yourbrand.com)")
            return 1
        updated = mgr.apply_domain_to_all(domain)
        print(f"[✓] Đã gán domain @{domain.lstrip('@')} cho toàn bộ 12 tài khoản thành công!")
        return 0

    elif args.action == "export":
        out_fmt = getattr(args, "format", "csv") or "csv"
        raw_output = getattr(args, "output", None) or f"output/accounts/gobi_zodiac_profiles.{out_fmt}"
        out_path = Path(raw_output)
        domain = getattr(args, "domain", "shopgobi.com") or "shopgobi.com"
        
        if out_fmt == "csv":
            saved_path = mgr.export_antidetect_csv(out_path, domain=domain)
            print(f"[✓] Đã xuất file CSV cấu hình Antidetect Browser tại: {saved_path}")
            print("👉 Định dạng tương thích 100% với: AdsPower, GoLogin, Hidemyacc, MoreLogin.")
        else:
            accounts = mgr.list_accounts()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            import json
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump([acc.to_dict() for acc in accounts], f, ensure_ascii=False, indent=2)
            print(f"[✓] Đã xuất file JSON tại: {out_path}")
        return 0

    elif args.action == "warmup":
        day = getattr(args, "day", 0)
        proto = mgr.get_warmup_protocol(day)
        print(f"\n📋 [QUY TRÌNH LÀM ẤM TÀI KHOẢN TIKTOK] - {proto['title'].upper()}")
        print("-" * 70)
        for step, task in enumerate(proto["tasks"], 1):
            print(f"  {step}. {task}")
        print("-" * 70 + "\n")
        return 0

    elif args.action == "set-status":
        acc_id = getattr(args, "id", None)
        status_str = getattr(args, "status", None)
        warmup_day = getattr(args, "day", None)
        if not acc_id or not status_str:
            print("[!] Thiếu tham số: --id <account_id> --status <PLANNED|WARMING_UP|ACTIVE|REVIEW|SUSPENDED>")
            return 1
        try:
            status = AccountStatus(status_str.upper())
            res = mgr.update_account_status(acc_id, status, warmup_day=warmup_day)
            if res:
                print(f"[✓] Cập nhật thành công tài khoản {acc_id} -> Status: {status.value}")
            else:
                print(f"[!] Không tìm thấy tài khoản {acc_id}")
        except ValueError:
            print(f"[!] Trạng thái không hợp lệ: {status_str}")
            return 1
        return 0

    else:
        print("[!] Lệnh không hợp lệ. Sử dụng: list, emails, apply-domain, export, warmup, set-status")
        return 1
