"""Domain models for SnapTik video extractor & media ingestion."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SnaptikAuthor(BaseModel):
    id: Optional[str] = None
    unique_id: Optional[str] = None  # e.g. "benaithucchien"
    nickname: Optional[str] = None   # e.g. "Ben AI Studio"
    avatar: Optional[str] = None


class SnaptikMusic(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    play_url: Optional[str] = None
    duration: Optional[int] = 0


class SnaptikStats(BaseModel):
    plays: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    downloads: int = 0


class SnaptikMedia(BaseModel):
    video_url: Optional[str] = None            # Clean video without watermark
    video_hd_url: Optional[str] = None         # HD clean video
    watermark_video_url: Optional[str] = None  # Original video with watermark
    audio_url: Optional[str] = None            # Direct MP3 audio track
    cover_url: Optional[str] = None            # Thumbnail cover image
    dynamic_cover_url: Optional[str] = None    # Animated cover
    images: List[str] = Field(default_factory=list)  # Images if photo slide post


class SnaptikVideoItem(BaseModel):
    id: str
    original_url: str
    title: str = ""
    duration: int = 0
    is_slideshow: bool = False
    author: SnaptikAuthor = Field(default_factory=SnaptikAuthor)
    stats: SnaptikStats = Field(default_factory=SnaptikStats)
    media: SnaptikMedia = Field(default_factory=SnaptikMedia)
    music: Optional[SnaptikMusic] = None
    source_engine: str = "tikwm_snaptik"  # "tikwm_snaptik" | "ytdlp" | "web" | "playwright"


class SnaptikDownloadResult(BaseModel):
    success: bool
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    cover_path: Optional[str] = None
    metadata_path: Optional[str] = None
    image_paths: List[str] = Field(default_factory=list)
    info: Optional[SnaptikVideoItem] = None
    error: Optional[str] = None
