"""Account Management Service for Gobi Social Zodiac KOC Multi-Account Matrix."""
import json
import csv
from pathlib import Path
from typing import List, Optional, Dict
from gobi.domain.account_models import ZodiacAccount, AccountStatus

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent.parent / "configs" / "koc_zodiac_accounts.json"

WARMUP_PROTOCOLS = {
    0: {
        "title": "Giai đoạn chuẩn bị (Pre-Registration)",
        "tasks": [
            "Chuẩn bị 1 domain riêng và kết nối Cloudflare Email Routing về Gmail chính.",
            "Chuẩn bị proxy di động 4G/5G hoặc Profile Antidetect sạch (1 profile = 1 tài khoản).",
            "Đăng ký tài khoản TikTok trên ứng dụng di động hoặc Antidetect Browser."
        ]
    },
    1: {
        "title": "Ngày 1: Khởi tạo & Định vị Hành vi Người dùng Thật",
        "tasks": [
            "Đăng nhập tài khoản, cập nhật Họ Tên & Bio phù hợp Niche chòm sao.",
            "Lướt feed TikTok (Dành cho bạn / For You) 15-20 phút.",
            "Tìm kiếm 2-3 hashtag thời trang liên quan đến Niche, xem hết video và thả tim 2-3 video.",
            "KHÔNG đổi avatar hay chèn link bio trong ngày đầu tiên."
        ]
    },
    2: {
        "title": "Ngày 2: Nuôi thuật toán đề xuất (Algorithm Feeding)",
        "tasks": [
            "Lướt feed 20 phút, follow 3-5 KOC cùng ngành thời trang.",
            "Để lại 1-2 comment tự nhiên, tích cực trên các video triệu view.",
            "Cập nhật Avatar KOC Gô Bi chính thức phù hợp phong cách chòm sao."
        ]
    },
    3: {
        "title": "Ngày 3: Tương tác sâu & Chuẩn bị nội dung",
        "tasks": [
            "Xem livestream thời trang/bán hàng 10-15 phút, thả tim màn hình.",
            "Hoàn thiện Profile: Link liên kết, mô tả chuẩn SEO TikTok.",
            "Chuẩn bị sẵn 3 video AI KOC đầu tiên được render từ Gobi Pipeline."
        ]
    },
    4: {
        "title": "Ngày 4: Xuất bản Video Đầu Tiên (Launch Video #1)",
        "tasks": [
            "Đăng video #1 vào khung giờ vàng (11h30 - 12h30 hoặc 19h30 - 20h30).",
            "Sử dụng âm thanh đang thịnh hành (Trending Sound) và gắn 3-5 hashtag chuẩn Niche.",
            "Sau khi đăng, xem lại 1 lần và tắt app, không cày view ảo."
        ]
    },
    5: {
        "title": "Ngày 5+: Bật chế độ Vận hành Tự động (Active KOC)",
        "tasks": [
            "Kiểm tra chỉ số video #1 (Retention rate, Completion rate, Views).",
            "Đăng video #2 và #3 theo lịch trình định kỳ.",
            "Khi đạt đủ điều kiện follower, kích hoạt tính năng TikTok Shop Creator / Affiliate."
        ]
    }
}

class ZodiacAccountManager:
    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config_path = config_path

    def _load_data(self) -> dict:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_data(self, data: dict):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def list_accounts(self) -> List[ZodiacAccount]:
        raw_data = self._load_data()
        return [ZodiacAccount.from_dict(acc) for acc in raw_data.get("accounts", [])]

    def get_account(self, account_id: str) -> Optional[ZodiacAccount]:
        accounts = self.list_accounts()
        for acc in accounts:
            if acc.account_id == account_id:
                return acc
        return None

    def generate_email_list(self, domain: str) -> List[Dict[str, str]]:
        """Sinh danh sách 12 email gán mã chòm sao dựa trên domain của người dùng."""
        clean_domain = domain.lstrip("@").strip()
        accounts = self.list_accounts()
        matrix = []
        for acc in accounts:
            full_email = f"{acc.email_prefix}@{clean_domain}"
            matrix.append({
                "account_id": acc.account_id,
                "zodiac": f"{acc.symbol} {acc.zodiac_name_vi} ({acc.zodiac_name_en})",
                "handle": acc.handle,
                "email": full_email,
                "niche": acc.niche_fashion
            })
        return matrix

    def apply_domain_to_all(self, domain: str) -> List[ZodiacAccount]:
        """Cập nhật email chính thức cho toàn bộ 12 tài khoản trong file config."""
        clean_domain = domain.lstrip("@").strip()
        raw_data = self._load_data()
        updated_accounts = []
        for acc in raw_data.get("accounts", []):
            acc["assigned_email"] = f"{acc['email_prefix']}@{clean_domain}"
            updated_accounts.append(ZodiacAccount.from_dict(acc))
        self._save_data(raw_data)
        return updated_accounts

    def update_account_status(self, account_id: str, status: AccountStatus, warmup_day: Optional[int] = None) -> bool:
        raw_data = self._load_data()
        found = False
        for acc in raw_data.get("accounts", []):
            if acc["account_id"] == account_id:
                acc["status"] = status.value
                if warmup_day is not None:
                    acc["warmup_day"] = warmup_day
                found = True
                break
        if found:
            self._save_data(raw_data)
        return found

    def export_antidetect_csv(self, output_path: Path, domain: str = "example.com") -> str:
        """Xuất file CSV chuẩn định dạng để import nhanh vào các Antidetect Browser (AdsPower, GoLogin, Hidemyacc)."""
        accounts = self.list_accounts()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "Profile Name", "Group", "Platform", "Username", "Email", 
                "Password", "2FA Key", "Proxy Type", "Proxy Host:Port", "Notes"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for acc in accounts:
                email = acc.assigned_email or acc.get_full_email(domain)
                writer.writerow({
                    "Profile Name": f"Gobi - {acc.zodiac_name_en} ({acc.symbol})",
                    "Group": "Gobi Zodiac KOC",
                    "Platform": "TikTok",
                    "Username": acc.handle,
                    "Email": email,
                    "Password": "",  # Để trống cho người dùng tự điền mật khẩu bí mật
                    "2FA Key": "",
                    "Proxy Type": "HTTP / SOCKS5",
                    "Proxy Host:Port": acc.proxy_assigned or "",
                    "Notes": f"Niche: {acc.niche_fashion} | Status: {acc.status.value} (Day {acc.warmup_day})"
                })
        return str(output_path)

    def get_warmup_protocol(self, day: int) -> dict:
        return WARMUP_PROTOCOLS.get(day, WARMUP_PROTOCOLS[0])
