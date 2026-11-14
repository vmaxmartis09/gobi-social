"""SnapTik Scraper Adapter - Multi-Strategy TikTok & Social Video Extractor."""

import json
import logging
import re
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable

import httpx

from gobi.domain.snaptik_models import (
    SnaptikAuthor,
    SnaptikMusic,
    SnaptikStats,
    SnaptikMedia,
    SnaptikVideoItem,
)

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}


class SnaptikScraper:
    """Multi-Strategy Scraper for extracting watermark-free TikTok videos & metadata."""

    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout

    @staticmethod
    def normalize_url(url: str) -> str:
        """Sanitize and normalize TikTok URL (handles short links, trims tracking params)."""
        clean = url.strip()
        # If url contains tracking parameters like ?is_from_webapp=1&sender_device=pc
        if "?" in clean and not ("vt.tiktok.com" in clean or "vm.tiktok.com" in clean):
            clean = clean.split("?")[0]
        return clean

    def resolve_redirects(self, url: str) -> str:
        """Resolve short redirect URLs such as vt.tiktok.com or vm.tiktok.com."""
        if any(domain in url for domain in ["vt.tiktok.com", "vm.tiktok.com", "v.douyin.com"]):
            try:
                with httpx.Client(
                    headers=DEFAULT_HEADERS,
                    follow_redirects=True,
                    timeout=self.timeout,
                ) as client:
                    resp = client.get(url)
                    return str(resp.url).split("?")[0]
            except Exception as e:
                logger.warning(f"Failed to resolve short URL {url}: {e}")
        return url

    def extract(self, url: str) -> SnaptikVideoItem:
        """Extract video metadata and media download links using Multi-Strategy Pivot Loop.

        Strategy 1: TikWM API (SnapTik.vn underlying engine)
        Strategy 2: yt-dlp native extractor
        Strategy 3: TikTok oEmbed & Web metadata
        """
        raw_url = self.normalize_url(url)
        resolved_url = self.resolve_redirects(raw_url)

        errors = []

        # --- STRATEGY 1: TikWM (SnapTik Engine) ---
        try:
            item = self._extract_via_tikwm(resolved_url)
            if item:
                return item
        except Exception as e:
            msg = f"[Strategy 1 - TikWM] Error: {e}"
            logger.warning(msg)
            errors.append(msg)

        # --- STRATEGY 2: yt-dlp Native Extractor ---
        try:
            item = self._extract_via_ytdlp(resolved_url)
            if item:
                return item
        except Exception as e:
            msg = f"[Strategy 2 - yt-dlp] Error: {e}"
            logger.warning(msg)
            errors.append(msg)

        # --- STRATEGY 3: TikTok oEmbed & Web Scraping ---
        try:
            item = self._extract_via_web(resolved_url)
            if item:
                return item
        except Exception as e:
            msg = f"[Strategy 3 - Web] Error: {e}"
            logger.warning(msg)
            errors.append(msg)

        raise RuntimeError(
            f"All extraction strategies exhausted for {url}. Details: {' | '.join(errors)}"
        )

    def _extract_via_tikwm(self, url: str) -> Optional[SnaptikVideoItem]:
        """Extract metadata & clean URLs via TikWM API (as used by snaptik.vn)."""
        api_endpoint = f"https://tikwm.com/api/?url={urllib.parse.quote(url)}"
        headers = {
            **DEFAULT_HEADERS,
            "Referer": "https://snaptik.vn/",
        }

        with httpx.Client(headers=headers, timeout=self.timeout) as client:
            resp = client.get(api_endpoint)
            resp.raise_for_status()
            data = resp.json()

        if data.get("code") != 0 or not data.get("data"):
            msg = data.get("msg", "Unknown TikWM API error")
            raise ValueError(f"TikWM API failed with message: {msg}")

        d = data["data"]
        video_id = str(d.get("id") or "")
        title = d.get("title") or ""
        duration = int(d.get("duration") or 0)

        # Media links
        play_url = d.get("play")
        # Ensure full URL if relative
        if play_url and play_url.startswith("/"):
            play_url = f"https://tikwm.com{play_url}"

        hd_url = d.get("hdplay")
        if hd_url and hd_url.startswith("/"):
            hd_url = f"https://tikwm.com{hd_url}"

        wm_url = d.get("wmplay")
        if wm_url and wm_url.startswith("/"):
            wm_url = f"https://tikwm.com{wm_url}"

        music_url = d.get("music")
        if music_url and music_url.startswith("/"):
            music_url = f"https://tikwm.com{music_url}"

        cover_url = d.get("cover")
        images = d.get("images") or []
        is_slideshow = len(images) > 0

        # Author info
        author_data = d.get("author") or {}
        author = SnaptikAuthor(
            id=str(author_data.get("id") or ""),
            unique_id=author_data.get("unique_id"),
            nickname=author_data.get("nickname"),
            avatar=author_data.get("avatar"),
        )

        # Music info
        music_data = d.get("music_info") or {}
        music = SnaptikMusic(
            id=str(music_data.get("id") or ""),
            title=music_data.get("title") or d.get("music_info", {}).get("title"),
            author=music_data.get("author"),
            play_url=music_url,
            duration=int(music_data.get("duration") or 0),
        )

        # Statistics
        stats = SnaptikStats(
            plays=int(d.get("play_count") or 0),
            likes=int(d.get("digg_count") or 0),
            comments=int(d.get("comment_count") or 0),
            shares=int(d.get("share_count") or 0),
            downloads=int(d.get("download_count") or 0),
        )

        media = SnaptikMedia(
            video_url=play_url,
            video_hd_url=hd_url,
            watermark_video_url=wm_url,
            audio_url=music_url,
            cover_url=cover_url,
            dynamic_cover_url=d.get("dynamic_cover"),
            images=images,
        )

        return SnaptikVideoItem(
            id=video_id,
            original_url=url,
            title=title,
            duration=duration,
            is_slideshow=is_slideshow,
            author=author,
            stats=stats,
            media=media,
            music=music,
            source_engine="tikwm_snaptik",
        )

    def _extract_via_ytdlp(self, url: str) -> Optional[SnaptikVideoItem]:
        """Extract metadata & direct stream via yt-dlp native TikTok extractor."""
        import yt_dlp

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if not info:
            return None

        video_id = str(info.get("id") or "")
        title = info.get("title") or info.get("description") or ""
        duration = int(info.get("duration") or 0)

        # Find best video stream URL
        formats = info.get("formats", [])
        best_video_url = None
        for fmt in reversed(formats):
            if fmt.get("url") and not fmt.get("url").startswith("blob:"):
                best_video_url = fmt.get("url")
                break

        author = SnaptikAuthor(
            id=str(info.get("uploader_id") or ""),
            unique_id=info.get("uploader_id") or info.get("uploader"),
            nickname=info.get("uploader"),
            avatar=None,
        )

        stats = SnaptikStats(
            plays=int(info.get("view_count") or 0),
            likes=int(info.get("like_count") or 0),
            comments=int(info.get("comment_count") or 0),
            shares=int(info.get("repost_count") or 0),
        )

        media = SnaptikMedia(
            video_url=best_video_url,
            video_hd_url=best_video_url,
            watermark_video_url=None,
            audio_url=None,
            cover_url=info.get("thumbnail"),
            images=[],
        )

        return SnaptikVideoItem(
            id=video_id,
            original_url=url,
            title=title,
            duration=duration,
            is_slideshow=False,
            author=author,
            stats=stats,
            media=media,
            music=None,
            source_engine="ytdlp",
        )

    def _extract_via_web(self, url: str) -> Optional[SnaptikVideoItem]:
        """Extract basic video details via TikTok oEmbed API."""
        oembed_url = f"https://www.tiktok.com/oembed?url={urllib.parse.quote(url)}"
        with httpx.Client(headers=DEFAULT_HEADERS, timeout=self.timeout) as client:
            resp = client.get(oembed_url)
            if resp.status_code != 200:
                return None
            data = resp.json()

        video_id = str(data.get("embed_product_id") or "")
        title = data.get("title") or ""
        author_name = data.get("author_name") or ""
        author_unique_id = data.get("author_unique_id") or ""
        thumbnail = data.get("thumbnail_url")

        author = SnaptikAuthor(
            unique_id=author_unique_id,
            nickname=author_name,
            avatar=None,
        )

        media = SnaptikMedia(
            cover_url=thumbnail,
        )

        return SnaptikVideoItem(
            id=video_id or "web_parsed",
            original_url=url,
            title=title,
            author=author,
            media=media,
            source_engine="tiktok_oembed",
        )

    def download_stream(
        self,
        media_url: str,
        dest_path: Path,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> Path:
        """Stream download media bytes directly to disk with proper referer and chunking."""
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Referer": "https://www.tiktok.com/",
            "Accept": "*/*",
        }

        with httpx.stream(
            "GET", media_url, headers=headers, follow_redirects=True, timeout=60.0
        ) as stream:
            stream.raise_for_status()
            total_size = int(stream.headers.get("content-length", 0))
            downloaded = 0

            with open(dest_path, "wb") as f:
                for chunk in stream.iter_bytes(chunk_size=65536):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if on_progress:
                        on_progress(downloaded, total_size)

        return dest_path
