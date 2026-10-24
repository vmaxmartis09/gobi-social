"""Automated Ingestion & Standardization for TikTok Shop Products."""

import datetime
import json
import logging
import os
import re
import unicodedata
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from gobi.adapters.platforms.tiktok.product_extractor import extract_tiktok_shop_products

logger = logging.getLogger(__name__)


def slugify_vietnamese(text: str, max_length: int = 50) -> str:
    """Chuyển chuỗi tiếng Việt thành slug an toàn cho tên folder trên mọi hệ điều hành."""
    if not text:
        return "product"
    # Chuẩn hóa unicode và bỏ dấu tiếng Việt
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = nfkd.encode("ASCII", "ignore").decode("utf-8").lower()
    # Loại bỏ ký tự đặc biệt, chỉ giữ chữ số và gạch dưới
    clean = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    clean = clean.strip("_")
    return clean[:max_length] if clean else "product"


def download_asset(url: str, dest_path: Path, timeout: int = 20) -> bool:
    """Tải một file tài nguyên từ URL về máy."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            dest_path.write_bytes(data)
        return True
    except Exception as e:
        logger.warning(f"Không thể tải file từ {url} về {dest_path}: {e}")
        return False


def get_product_catalog(catalog_file: Optional[Path] = None) -> Dict[str, Any]:
    """Đọc sổ cái catalog các sản phẩm đã nạp."""
    catalog_path = catalog_file or Path("data/products/catalog.json")
    if catalog_path.exists():
        try:
            return json.loads(catalog_path.read_text(encoding="utf-8"))
        except Exception:
            return {"products": {}, "last_updated": ""}
    return {"products": {}, "last_updated": ""}


def update_product_catalog(entry: Dict[str, Any], catalog_file: Optional[Path] = None) -> None:
    """Cập nhật sản phẩm vào sổ cái catalog.json."""
    catalog_path = catalog_file or Path("data/products/catalog.json")
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    
    catalog = get_product_catalog(catalog_path)
    products = catalog.get("products", {})
    
    pid = str(entry.get("product_id"))
    products[pid] = entry
    
    catalog["products"] = products
    catalog["total_products"] = len(products)
    catalog["last_updated"] = datetime.datetime.now().isoformat()
    
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")


def ingest_tiktok_product(
    video_url: str,
    base_dir: str = "data/products",
    download_cover: bool = True,
    download_video: bool = False,
    download_audio: bool = True
) -> Dict[str, Any]:
    """Chuẩn hóa và tự động nạp thông tin sản phẩm TikTok Shop từ video vào thư mục dữ liệu.

    Args:
        video_url: Link video TikTok chứa giỏ hàng sản phẩm.
        base_dir: Thư mục gốc chứa các folder sản phẩm (mặc định: 'data/products').
        download_cover: Có tải ảnh bìa sản phẩm về lưu trữ không (mặc định: True).
        download_video: Có tải video TikTok không watermark về kèm không (mặc định: False).
        download_audio: Có tải file âm thanh / nhạc nền MP3 về kèm không (mặc định: True).

    Returns:
        Dict chi tiết trạng thái, danh sách thư mục đã tạo và metadata sản phẩm.
    """
    logger.info(f"Bắt đầu nạp và chuẩn hóa video: {video_url}")
    
    # 1. Trích xuất thông tin sản phẩm từ video
    extraction = extract_tiktok_shop_products(video_url)
    if not extraction.get("success"):
        return {
            "success": False,
            "error": extraction.get("error", "Lỗi không xác định khi trích xuất dữ liệu.")
        }

    if not extraction.get("has_shop_anchor") or not extraction.get("products"):
        return {
            "success": False,
            "error": "Video này không có giỏ hàng TikTok Shop được gắn kèm (Không tìm thấy sản phẩm)."
        }

    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)
    
    video_info = {
        "video_id": extraction.get("video_id", ""),
        "author": extraction.get("author", ""),
        "nickname": extraction.get("nickname", ""),
        "desc": extraction.get("desc", ""),
        "video_url": video_url
    }

    ingested_products = []
    now_iso = datetime.datetime.now().isoformat()

    # 2. Xử lý từng sản phẩm được gắn vào video
    for p in extraction["products"]:
        pid = str(p.get("product_id"))
        title = p.get("title", "san_pham")
        slug = slugify_vietnamese(title, max_length=45)
        
        # Đặt tên folder chuẩn mực: <product_id>_<slug>
        folder_name = f"{pid}_{slug}" if slug else pid
        product_dir = base_path / folder_name
        product_dir.mkdir(parents=True, exist_ok=True)

        downloaded_assets = {}

        # 3. Tải ảnh bìa sản phẩm
        if download_cover and p.get("cover_url"):
            cover_file = product_dir / "cover.jpg"
            if download_asset(p["cover_url"], cover_file):
                downloaded_assets["cover"] = str(cover_file.resolve())

        # 4. Tải video không logo & audio nếu được yêu cầu
        if download_video:
            try:
                from gobi.services.media.snaptik_service import SnaptikService
                snaptik = SnaptikService()
                video_res = snaptik.download(
                    url=video_url,
                    output_dir=str(product_dir),
                    filename="video_clean",
                    download_audio=download_audio,
                    hd=True
                )
                if video_res.video_path:
                    downloaded_assets["video"] = str(Path(video_res.video_path).resolve())
                if video_res.audio_path:
                    downloaded_assets["audio"] = str(Path(video_res.audio_path).resolve())
            except Exception as e:
                logger.warning(f"Lỗi khi tải video không logo: {e}")

        # 5. Xây dựng metadata chuẩn hóa
        category_names = [c.get("category_name") for c in p.get("categories", []) if c.get("category_name")]
        metadata = {
            "product_id": pid,
            "title": title,
            "keyword": p.get("keyword", ""),
            "pdp_url": p.get("pdp_url", ""),
            "affiliate_pdp_url": p.get("affiliate_pdp_url", ""),
            "seo_url": p.get("seo_url", ""),
            "cover_url": p.get("cover_url", ""),
            "seller_id": p.get("seller_id", ""),
            "price": p.get("price", 0),
            "currency": p.get("currency", "VND"),
            "categories": category_names,
            "source_video": video_info,
            "downloaded_assets": downloaded_assets,
            "ingested_at": now_iso
        }

        # Lưu product.json vào chính thư mục sản phẩm
        meta_file = product_dir / "product.json"
        meta_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

        # 6. Tạo file README.md tóm tắt trực quan trong thư mục
        cat_str = " > ".join(category_names) if category_names else "Chưa phân loại"
        cover_md = "![Ảnh sản phẩm](cover.jpg)\n\n" if "cover" in downloaded_assets else ""
        readme_content = f"""# {title}

{cover_md}
## 📌 Thông tin sản phẩm
* **Product ID:** `{pid}`
* **Tên hiển thị giỏ hàng:** {p.get('keyword', 'N/A')}
* **Link TikTok Shop chuẩn:** [{p.get('pdp_url')}]({p.get('pdp_url')})
* **Link Affiliate (Gốc kèm chain_key):** [{p.get('affiliate_pdp_url')}]({p.get('affiliate_pdp_url')})
* **Shop Seller ID:** `{p.get('seller_id', 'N/A')}`
* **Danh mục:** {cat_str}
* **Thời gian nạp:** {now_iso}

## 🎬 Video nguồn
* **Kênh Creator:** [@{video_info['author']}](https://www.tiktok.com/@{video_info['author']}) ({video_info['nickname']})
* **Video ID:** `{video_info['video_id']}`
* **Mô tả video:** {video_info['desc']}
* **Link video:** [{video_url}]({video_url})
"""
        (product_dir / "README.md").write_text(readme_content, encoding="utf-8")

        # 7. Cập nhật vào sổ cái catalog.json
        catalog_entry = {
            "product_id": pid,
            "title": title,
            "keyword": p.get("keyword", ""),
            "pdp_url": p.get("pdp_url", ""),
            "affiliate_pdp_url": p.get("affiliate_pdp_url", ""),
            "folder": str(product_dir),
            "cover_image": str(product_dir / "cover.jpg") if "cover" in downloaded_assets else None,
            "video_path": downloaded_assets.get("video"),
            "audio_path": downloaded_assets.get("audio"),
            "author": video_info["author"],
            "video_id": video_info["video_id"],
            "ingested_at": now_iso
        }
        update_product_catalog(catalog_entry, base_path / "catalog.json")

        ingested_products.append({
            "product_id": pid,
            "title": title,
            "folder": str(product_dir),
            "pdp_url": p.get("pdp_url", ""),
            "affiliate_pdp_url": p.get("affiliate_pdp_url", ""),
            "metadata_file": str(meta_file),
            "cover_downloaded": "cover" in downloaded_assets
        })

    return {
        "success": True,
        "video_url": video_url,
        "author": video_info["author"],
        "total_ingested": len(ingested_products),
        "catalog_file": str((base_path / "catalog.json").resolve()),
        "products": ingested_products
    }
