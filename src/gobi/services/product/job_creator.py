"""Job Creator Service - Unified Orchestrator for Ingesting any TikTok Link as a Job."""

import datetime
import json
import logging
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path("/Volumes/Data/gobi-social")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from gobi.services.product.ingestion import ingest_tiktok_product, update_product_catalog, slugify_vietnamese, download_asset
from gobi.services.media.snaptik_service import SnaptikService

logger = logging.getLogger(__name__)


def create_job_from_url(url: str, base_dir: str = "data/products") -> Dict[str, Any]:
    """Unified handler: Ingests any TikTok video as a Job.
    1. Tries to ingest TikTok Shop product anchor.
    2. Fallback to Snaptik clean video & metadata ingestion if no shop anchor.
    """
    url = url.strip()
    if not url:
        return {"success": False, "error": "URL không được để trống"}

    base_path = PROJECT_ROOT / base_dir
    base_path.mkdir(parents=True, exist_ok=True)

    # Strategy 1: Try full TikTok Shop product ingestion
    try:
        res = ingest_tiktok_product(
            video_url=url,
            base_dir=str(base_path),
            download_cover=True,
            download_video=True,
            download_audio=True,
        )
        if res.get("success") and res.get("products"):
            return {
                "success": True,
                "strategy": "tiktok_shop_anchor",
                "product": res["products"][0],
                "total_ingested": res.get("total_ingested", 1),
                "message": f"Đã nạp thành công sản phẩm TikTok Shop: {res['products'][0]['title']}"
            }
    except Exception as e:
        logger.warning(f"TikTok Shop ingestion fallback trigger: {e}")

    # Strategy 2: Fallback to SnapTik universal media ingestion
    try:
        snaptik = SnaptikService()
        meta = snaptik.get_info(url)
        video_id = meta.id or ""
        if not video_id:
            m = re.search(r"/video/(\d+)", url)
            if m:
                video_id = m.group(1)
        video_id = str(video_id or int(datetime.datetime.now().timestamp()))

        title = meta.title or "TikTok Fashion Review"
        slug = slugify_vietnamese(title, max_length=45)
        folder_name = f"{video_id}_{slug}"
        job_dir = base_path / folder_name
        job_dir.mkdir(parents=True, exist_ok=True)

        # Download clean video + audio + cover
        download_res = snaptik.download(
            url=url,
            output_dir=str(job_dir),
            filename="video_clean",
            download_audio=True,
            download_cover=True,
            hd=True,
        )

        now_iso = datetime.datetime.now().isoformat()

        # Resolve cover image URL safely from SnaptikMedia
        cover_remote_url = ""
        if meta.media:
            cover_remote_url = meta.media.cover_url or meta.media.dynamic_cover_url or ""

        # Ensure cover.jpg exists locally
        local_cover = job_dir / "cover.jpg"
        if download_res.cover_path and Path(download_res.cover_path).exists():
            if str(Path(download_res.cover_path).resolve()) != str(local_cover.resolve()):
                try:
                    shutil.copy2(download_res.cover_path, local_cover)
                except Exception:
                    pass
        elif cover_remote_url:
            download_asset(cover_remote_url, local_cover)

        final_cover_path = str(local_cover.resolve()) if local_cover.exists() else (download_res.cover_path or "")
        final_video_path = str(Path(download_res.video_path).resolve()) if (download_res.video_path and Path(download_res.video_path).exists()) else ""
        final_audio_path = str(Path(download_res.audio_path).resolve()) if (download_res.audio_path and Path(download_res.audio_path).exists()) else ""

        # Product schema
        product_data = {
            "product_id": video_id,
            "title": title,
            "keyword": (meta.author.nickname if meta.author and meta.author.nickname else "TikTok Fashion"),
            "pdp_url": url,
            "affiliate_pdp_url": url,
            "seo_url": url,
            "cover_url": cover_remote_url,
            "seller_id": "",
            "price": 0,
            "currency": "VND",
            "categories": ["Thời trang nữ", "KOC Review"],
            "source_video": {
                "video_id": video_id,
                "author": (meta.author.unique_id if meta.author and meta.author.unique_id else "creator"),
                "nickname": (meta.author.nickname if meta.author and meta.author.nickname else "Creator"),
                "desc": title,
                "video_url": url,
            },
            "downloaded_assets": {
                "cover": final_cover_path,
                "video": final_video_path,
                "audio": final_audio_path,
            },
            "status": "CHUA_LAM",
            "ingested_at": now_iso,
        }

        # Write product.json
        (job_dir / "product.json").write_text(json.dumps(product_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Write video_clean.json
        video_clean_data = {
            "id": video_id,
            "original_url": url,
            "title": title,
            "duration": meta.duration or 60,
            "author": {
                "unique_id": (meta.author.unique_id if meta.author and meta.author.unique_id else "creator"),
                "nickname": (meta.author.nickname if meta.author and meta.author.nickname else "Creator"),
                "avatar": (meta.author.avatar if meta.author and meta.author.avatar else ""),
            },
            "stats": {
                "plays": (meta.stats.plays if meta.stats else 0),
                "likes": (meta.stats.likes if meta.stats else 0),
                "comments": (meta.stats.comments if meta.stats else 0),
                "shares": (meta.stats.shares if meta.stats else 0),
            },
            "saved_files": {
                "video": final_video_path,
                "audio": final_audio_path,
                "cover": final_cover_path,
            },
        }
        (job_dir / "video_clean.json").write_text(json.dumps(video_clean_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Update catalog.json
        catalog_entry = {
            "product_id": video_id,
            "title": title,
            "keyword": product_data["keyword"],
            "pdp_url": url,
            "affiliate_pdp_url": url,
            "folder": f"data/products/{folder_name}",
            "cover_image": f"data/products/{folder_name}/cover.jpg" if local_cover.exists() else cover_remote_url,
            "video_path": final_video_path,
            "audio_path": final_audio_path,
            "author": product_data["source_video"]["author"],
            "video_id": video_id,
            "ingested_at": now_iso,
            "status": "CHUA_LAM",
        }
        update_product_catalog(catalog_entry)

        return {
            "success": True,
            "strategy": "snaptik_media_fallback",
            "product": catalog_entry,
            "total_ingested": 1,
            "message": f"Đã nạp thành công video và trích xuất tài nguyên: {title}"
        }

    except Exception as e:
        logger.error(f"Error creating job from {url}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python job_creator.py <tiktok_url>")
        sys.exit(1)
    url_arg = sys.argv[1]
    res = create_job_from_url(url_arg)
    print(json.dumps(res, indent=2, ensure_ascii=False))
