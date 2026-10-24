"""
=============================================================================
🎭 GOBI MOTION MIMIC WORKFLOW DOMAIN MODELS (TẦNG 1: DOMAIN)
Quy chuẩn dữ liệu độc lập cho quy trình: AI KOC bắt chước Video nạp vào
(Motion Reference / Driving Video -> AI Character -> HyperFrames Composition)
=============================================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List
import time


class MimicLayoutMode(str, Enum):
    """Bố cục dựng video đầu ra qua HyperFrames."""
    SOLO = "solo"                     # 100% Khung hình 9:16 là nhân vật AI bắt chước
    SPLIT_3_TIER = "split_3_tier"     # Chuẩn như What's up AI: Top (Slide/Proof) | Mid (AI KOC) | Bot (Người quay thật)
    SIDE_BY_SIDE = "side_by_side"     # So sánh song song: Trái (Video mẫu gốc) | Phải (AI KOC bắt chước)


class MotionEngineType(str, Enum):
    """Công cụ thực thi truyền chuyển động (Motion Transfer)."""
    LOCAL_FACESWAP = "local_faceswap"          # Local AI: InsightFace + inswapper_128.onnx (CoreML), swap mặt giữ chuyển động gốc
    KLING_MOTION_CONTROL = "kling_motion"      # Cloud AI: Kling AI Motion Control
    MOCK = "mock"                              # Giả lập / Test nhanh pipeline không tốn GPU/Credit


class LipSyncMode(str, Enum):
    """Chiến lược khớp khẩu hình theo audio mới."""
    AUTO = "auto"   # Tự chạy khi audio_strategy = omnivoice, tự bỏ qua khi keep_original/replace_bgm
    ON = "on"       # Luôn chạy Wav2Lip nếu có audio mới
    OFF = "off"     # Không bao giờ chạy


class AudioStrategy(str, Enum):
    """Chiến lược xử lý âm thanh."""
    KEEP_ORIGINAL = "keep_original"   # Giữ trọn âm thanh gốc (dành cho clip nhạc viral, nhảy, hát cover)
    OMNIVOICE_CLONE = "omnivoice"     # Tách tiếng gốc và thay bằng giọng đọc clone AI tiếng Việt
    REPLACE_BGM = "replace_bgm"       # Giữ giọng nói hoặc thay toàn bộ bằng nhạc nền mới


@dataclass
class MotionMimicInput:
    """Đầu vào cần thiết khi nạp một video cho Gobi bắt chước."""
    reference_video_path_or_url: str
    character_avatar_path: str        # Đường dẫn ảnh phôi nhân vật AI (hoặc ID KOC: gobi_lyly, neau...)
    layout_mode: MimicLayoutMode = MimicLayoutMode.SOLO
    engine_type: MotionEngineType = MotionEngineType.LOCAL_FACESWAP
    audio_strategy: AudioStrategy = AudioStrategy.KEEP_ORIGINAL
    title_badge: str = "GOBI AI MIMIC SOTA"
    subtitles_text: Optional[str] = None
    custom_bgm_path: Optional[str] = None
    output_filename: Optional[str] = None
    spoken_script: Optional[str] = None       # Kịch bản lời đọc mới, dùng khi audio_strategy = omnivoice
    lipsync_mode: LipSyncMode = LipSyncMode.AUTO


@dataclass
class MotionMimicExecutionStep:
    """Từng bước thực thi độc lập trong workflow."""
    name: str
    status: str = "pending"           # pending -> running -> completed -> failed
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None


@dataclass
class MotionMimicResult:
    """Kết quả hoàn tất sau khi workflow xử lý xong."""
    job_id: str
    is_success: bool
    output_video_path: Optional[str] = None
    preview_url: Optional[str] = None
    hyperframes_project_dir: Optional[str] = None
    duration_seconds: float = 0.0
    steps: List[MotionMimicExecutionStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
