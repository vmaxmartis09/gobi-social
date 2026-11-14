"""
=============================================================================
🎬 CONTENT REMIX DOMAIN MODELS (TẦNG 1: DOMAIN)
Quy chuẩn dữ liệu cho quy trình: Video tham khảo -> Kịch bản mới (Gemini) ->
Danh sách cảnh Ken Burns -> HyperFrames Composition.
=============================================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from gobi.domain.motion_mimic_models import MimicLayoutMode, AudioStrategy


class SceneMotion(str, Enum):
    """Kiểu chuyển động Ken Burns áp dụng cho ảnh tĩnh."""
    ZOOM_IN = "zoom_in"
    PAN_DOWN = "pan_down"
    PAN_HORIZONTAL = "pan_horizontal"


@dataclass
class VideoScene:
    """Một cảnh trong video: ảnh tĩnh + thời lượng + caption, dùng cho HyperFramesEngine."""
    image_path: str
    duration: float
    caption: str = ""
    motion: SceneMotion = SceneMotion.ZOOM_IN
    track_index: int = 0


@dataclass
class RemixScriptBeat:
    """Một nhịp (beat) trong kịch bản: hook / chi tiết / trải nghiệm / CTA..."""
    beat_name: str
    voiceover_line: str
    duration_hint: float = 4.0


@dataclass
class RemixScript:
    """Kịch bản hoàn chỉnh do Gemini sinh ra, dựa trên transcript tham khảo + info sản phẩm thật."""
    hook: str
    beats: List[RemixScriptBeat] = field(default_factory=list)
    cta: str = ""


@dataclass
class ContentRemixInput:
    """Đầu vào cho ContentRemixWorkflow."""
    reference_video_path_or_url: str
    product_code: Optional[str] = None
    product_info_path: Optional[str] = None  # Dùng khi sản phẩm không có trong catalog (vd: job từ dashboard)
    character_avatar_path: str = "gobi_lyly"
    layout_mode: MimicLayoutMode = MimicLayoutMode.SOLO
    audio_strategy: AudioStrategy = AudioStrategy.OMNIVOICE_CLONE
    title_badge: str = "GOBI AI REVIEW"
    output_filename: Optional[str] = None
    # Ghép Gô Bi mặc đúng trang phục sản phẩm bằng GeminiImageAdapter thay vì chỉ
    # Ken Burns ảnh sản phẩm thô. Tắt nếu muốn quay lại hành vi cũ (ảnh gốc).
    use_ai_outfit_compositing: bool = True


@dataclass
class ContentRemixExecutionStep:
    """Từng bước thực thi độc lập trong workflow."""
    name: str
    status: str = "pending"
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None


@dataclass
class ContentRemixResult:
    """Kết quả hoàn tất sau khi workflow xử lý xong."""
    job_id: str
    is_success: bool
    output_video_path: Optional[str] = None
    hyperframes_project_dir: Optional[str] = None
    duration_seconds: float = 0.0
    remix_script: Optional[RemixScript] = None
    steps: List[ContentRemixExecutionStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
