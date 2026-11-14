"""Gobi Product Warehouse Domain Models - Data schemas for KOC product repository."""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ProductStatus(str, Enum):
    """Trạng thái tiến độ sản xuất video của sản phẩm."""
    CHUA_LAM = "chua_lam"          # Chưa triển khai kịch bản / video
    DANG_LAM = "dang_lam"          # Đang viết script, render KOC AI hoặc dựng video
    DA_DANG_VIDEO = "da_dang_video" # Đã render xong và xuất bản video lên TikTok


class ProductCategory(str, Enum):
    """Phân loại ngành hàng thời trang & phụ kiện."""
    AO_THUN = "ao_thun"
    QUAN_TAY = "quan_tay"
    QUAN_JEAN = "quan_jean"
    QUAN_SHORT = "quan_short"
    AO_KHOAC = "ao_khoac"
    VAY_DAM = "vay_dam"
    TUI_XACH = "tui_xach"
    MY_PHAM_SET = "my_pham_set"
    PHU_KIEN = "phu_kien"


class ProductPricing(BaseModel):
    """Thông tin giá bán & hoa hồng affiliate."""
    price_vnd: int = Field(..., description="Giá niêm yết bán lẻ VND")
    original_price_vnd: Optional[int] = Field(None, description="Giá gốc trước giảm VND")
    commission_rate_percent: float = Field(..., description="Tỷ lệ hoa hồng (%)")
    commission_per_order_vnd: int = Field(..., description="Hoa hồng nhận được trên mỗi đơn VND")


class ProductSpecs(BaseModel):
    """Thông số kỹ thuật, chất liệu, xuất xứ của sản phẩm."""
    material: str = Field(..., description="Chất liệu vải hoặc thành phần chính")
    colors: List[str] = Field(default_factory=list, description="Bảng màu sắc")
    sizes: List[str] = Field(default_factory=list, description="Dải kích cỡ")
    origin_shop: str = Field(..., description="Tên gian hàng / Thương hiệu cung ứng")
    usp_features: List[str] = Field(default_factory=list, description="Điểm bán hàng độc nhất (Unique Selling Points)")


class ProductVideoProduction(BaseModel):
    """Theo dõi quá trình sản xuất video KOC AI."""
    status: ProductStatus = Field(default=ProductStatus.CHUA_LAM, description="Trạng thái sản xuất")
    assigned_koc: str = Field(..., description="Handle hoặc tên KOC AI được phân công (ví dụ: @gobiboutique)")
    winning_format: str = Field(..., description="Định dạng video chủ đạo (Fast-Cut, 1 Item N Outfits...)")
    vmax_panels: List[str] = Field(default_factory=list, description="Các góc máy neo trong Ma trận 36 Panels")
    benchmark_video_url: Optional[str] = Field(None, description="Link video TikTok đối thủ triệu view")
    benchmark_views: Optional[int] = Field(None, description="Lượt view video đối thủ")
    published_video_url: Optional[str] = Field(None, description="Link video TikTok sau khi đăng")
    published_at: Optional[str] = Field(None, description="Thời điểm xuất bản video")


class ProductSEOMetadata(BaseModel):
    """Dữ liệu tối ưu SEO TikTok khép kín."""
    primary_keywords: List[str] = Field(default_factory=list, description="Từ khóa chính")
    secondary_keywords: List[str] = Field(default_factory=list, description="Từ khóa phụ & ngữ nghĩa LSI")
    search_intents: List[str] = Field(default_factory=list, description="Ý định tìm kiếm trên thanh search")
    hashtags: List[str] = Field(default_factory=list, description="Bộ hashtag 3 tầng")
    caption_template: str = Field(..., description="Mẫu caption chuẩn SEO")


class ProductItem(BaseModel):
    """Mô hình dữ liệu hoàn chỉnh của một sản phẩm trong kho."""
    product_code: str = Field(..., description="Mã định danh sản phẩm duy nhất (ví dụ: SP-BJ-001)")
    product_name: str = Field(..., description="Tên đầy đủ của sản phẩm")
    category: ProductCategory = Field(..., description="Ngành hàng")
    pricing: ProductPricing
    specs: ProductSpecs
    production: ProductVideoProduction
    seo: ProductSEOMetadata
    folder_path: Optional[str] = Field(None, description="Đường dẫn tương đối tới folder sản phẩm")


class WarehouseIndex(BaseModel):
    """File chỉ mục tổng kho sản phẩm."""
    system_name: str = "VMAX Gobi Product Warehouse"
    version: str = "1.0.0"
    last_updated: str
    total_products: int
    status_summary: Dict[str, int]
    koc_assignments_summary: Dict[str, int]
    products: List[Dict[str, Any]]
