"""Product Manager Service - Manages KOC product vault, assignments, and status lifecycles."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from gobi.domain.product_models import (
    ProductItem,
    ProductStatus,
    ProductCategory,
    WarehouseIndex,
)

CATALOG_DIR = Path("configs/products/catalog")
INDEX_FILE = Path("configs/products/warehouse_index.json")


class ProductManager:
    """Quản trị kho sản phẩm, vòng đời video và phân công KOC AI."""

    def __init__(self, catalog_dir: Path = CATALOG_DIR, index_file: Path = INDEX_FILE):
        self.catalog_dir = catalog_dir
        self.index_file = index_file
        self.catalog_dir.mkdir(parents=True, exist_ok=True)

    def load_all_products(self) -> List[ProductItem]:
        """Tải toàn bộ sản phẩm từ các thư mục con trong catalog/."""
        products = []
        if not self.catalog_dir.exists():
            return products

        for prod_folder in sorted(self.catalog_dir.iterdir()):
            if prod_folder.is_dir():
                info_path = prod_folder / "product_info.json"
                if info_path.exists():
                    try:
                        with open(info_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            prod = ProductItem(**data)
                            prod.folder_path = str(prod_folder)
                            products.append(prod)
                    except Exception as e:
                        print(f"[!] Lỗi khi đọc sản phẩm tại {prod_folder}: {e}")
        return products

    def get_product(self, product_code: str) -> Optional[ProductItem]:
        """Lấy thông tin chi tiết của một sản phẩm theo mã."""
        code_clean = product_code.strip().upper()
        prod_folder = self.catalog_dir / code_clean
        info_path = prod_folder / "product_info.json"
        if not info_path.exists():
            # Thử tìm kiếm nếu tên thư mục viết thường hoặc lệch
            for folder in self.catalog_dir.iterdir():
                if folder.is_dir() and folder.name.upper() == code_clean:
                    info_path = folder / "product_info.json"
                    break

        if info_path.exists():
            with open(info_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                prod = ProductItem(**data)
                prod.folder_path = str(info_path.parent)
                return prod
        return None

    def update_status(
        self, product_code: str, new_status: ProductStatus, video_url: Optional[str] = None
    ) -> Optional[ProductItem]:
        """Cập nhật trạng thái sản xuất (chua_lam, dang_lam, da_dang_video)."""
        prod = self.get_product(product_code)
        if not prod:
            return None

        prod.production.status = new_status
        if video_url:
            prod.production.published_video_url = video_url
        if new_status == ProductStatus.DA_DANG_VIDEO and not prod.production.published_at:
            prod.production.published_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_product(prod)
        self.rebuild_warehouse_index()
        return prod

    def assign_koc(self, product_code: str, koc_handle: str) -> Optional[ProductItem]:
        """Phân công KOC AI phụ trách sản phẩm."""
        prod = self.get_product(product_code)
        if not prod:
            return None

        prod.production.assigned_koc = koc_handle.strip()
        self.save_product(prod)
        self.rebuild_warehouse_index()
        return prod

    def save_product(self, prod: ProductItem) -> Path:
        """Lưu thông tin sản phẩm vào thư mục riêng."""
        folder = self.catalog_dir / prod.product_code.upper()
        folder.mkdir(parents=True, exist_ok=True)
        assets_dir = folder / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        info_path = folder / "product_info.json"
        prod.folder_path = str(folder)
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(prod.model_dump(), f, ensure_ascii=False, indent=2)
        return info_path

    def rebuild_warehouse_index(self) -> WarehouseIndex:
        """Tái tạo file chỉ mục tổng hợp warehouse_index.json."""
        products = self.load_all_products()
        status_counts = {
            ProductStatus.CHUA_LAM.value: 0,
            ProductStatus.DANG_LAM.value: 0,
            ProductStatus.DA_DANG_VIDEO.value: 0,
        }
        koc_counts: Dict[str, int] = {}
        items_summary = []

        for p in products:
            st = p.production.status.value
            status_counts[st] = status_counts.get(st, 0) + 1

            koc = p.production.assigned_koc
            koc_counts[koc] = koc_counts.get(koc, 0) + 1

            items_summary.append({
                "product_code": p.product_code,
                "product_name": p.product_name,
                "category": p.category.value,
                "price_vnd": p.pricing.price_vnd,
                "commission_rate_percent": p.pricing.commission_rate_percent,
                "commission_per_order_vnd": p.pricing.commission_per_order_vnd,
                "status": p.production.status.value,
                "assigned_koc": p.production.assigned_koc,
                "published_video_url": p.production.published_video_url,
                "folder_path": p.folder_path,
            })

        manifest = WarehouseIndex(
            system_name="VMAX Gobi Product Warehouse",
            version="1.0.0",
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_products=len(products),
            status_summary=status_counts,
            koc_assignments_summary=koc_counts,
            products=items_summary,
        )

        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(manifest.model_dump(), f, ensure_ascii=False, indent=2)

        return manifest
