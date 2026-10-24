"""Domain models for Zodiac KOC TikTok Accounts and Profile Governance."""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from enum import Enum

class AccountStatus(str, Enum):
    PLANNED = "PLANNED"                  # Chưa đăng ký
    WARMING_UP = "WARMING_UP"            # Đang trong chu kỳ làm ấm (Day 1 - Day 5)
    ACTIVE = "ACTIVE"                    # Đã hoạt động, sẵn sàng lên video
    REVIEW = "REVIEW"                    # Đang kiểm tra tương tác / cần tối ưu
    SUSPENDED = "SUSPENDED"              # Bị tạm ngưng hoặc quét

@dataclass
class ZodiacAccount:
    account_id: str                      # Ví dụ: gobi-aries
    zodiac_name_vi: str                  # Bạch Dương
    zodiac_name_en: str                  # Aries
    symbol: str                          # ♈
    handle: str                          # @gobi.aries
    niche_fashion: str                   # Phong cách thời trang
    persona_vibe: str                    # Tính cách & năng lượng KOC
    content_theme: str                   # Chủ đề nội dung chính
    email_prefix: str                    # gobi-aries
    target_audience: str                 # Đối tượng người xem mục tiêu
    status: AccountStatus = AccountStatus.PLANNED
    warmup_day: int = 0                  # Ngày làm ấm hiện tại (0 - 5)
    proxy_assigned: Optional[str] = None # Proxy 4G/Residential gán cho nick
    assigned_email: Optional[str] = None # Email đầy đủ khi đã có domain
    metrics: Dict[str, int] = field(default_factory=lambda: {
        "followers": 0,
        "total_views": 0,
        "videos_posted": 0
    })

    def get_full_email(self, domain: str = "example.com") -> str:
        clean_domain = domain.lstrip("@")
        return f"{self.email_prefix}@{clean_domain}"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "ZodiacAccount":
        status_val = data.get("status", AccountStatus.PLANNED.value)
        data_copy = dict(data)
        data_copy["status"] = AccountStatus(status_val)
        return cls(**data_copy)
