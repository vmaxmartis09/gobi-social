"""
=============================================================================
🎬 GOBI MOTION MIMIC WORKFLOW ENGINE (TẦNG 2: SERVICES - WORKFLOWS)
Pipeline độc lập: Nạp 1 video bất kỳ -> KOC AI bắt chước chuyển động ->
Dựng và xuất bản video chuẩn 9:16 bằng HeyGen HyperFrames.
=============================================================================
"""

import os
import sys
import json
import time
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List

from gobi.domain.motion_mimic_models import (
    MotionMimicInput,
    MotionMimicResult,
    MotionMimicExecutionStep,
    MimicLayoutMode,
    MotionEngineType,
    AudioStrategy,
    LipSyncMode
)
from gobi.services.media.hyperframes_engine import HyperFramesEngine
from gobi.services.media import video_ingest

FACESWAP_PROVIDERS = ["CoreMLExecutionProvider", "CPUExecutionProvider"]

PROJECT_ROOT = Path("/Volumes/Data/gobi-social")
CONFIG_PATH = PROJECT_ROOT / "configs" / "workflows" / "motion_mimic_config.json"


class MotionMimicWorkflow:
    """
    Quy trình độc lập thực thi việc bắt chước video mẫu nạp vào cho Gobi Social.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or PROJECT_ROOT
        self.hyperframes_engine = HyperFramesEngine(self.workspace_root)
        self.config = self._load_config()
        self.output_base = self.workspace_root / "output" / "mimic_workflow"
        self.output_base.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Đọc cấu hình workflow từ json."""
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Warning: Lỗi đọc {CONFIG_PATH}: {e}")
        return {}

    def get_video_metadata(self, video_path: str | Path) -> Dict[str, Any]:
        """Lấy thông tin duration, fps, resolution của video bằng ffprobe."""
        return video_ingest.get_video_metadata(video_path)

    def ingest_reference_video(self, source: str, job_dir: Path) -> Path:
        """Tiếp nhận video mẫu: Có thể là đường dẫn file nội bộ hoặc URL TikTok / YouTube."""
        return video_ingest.ingest_reference_video(source, job_dir, self.workspace_root)

    def extract_audio(self, video_path: Path, output_audio_path: Path) -> Path:
        """Trích xuất file audio từ video phục vụ ghép nhạc và đồng bộ khẩu hình."""
        return video_ingest.extract_audio(video_path, output_audio_path)

    def resolve_character_avatar(self, char_input: str) -> Path:
        """Giải quyết đường dẫn ảnh phôi của nhân vật AI."""
        # Kiểm tra presets
        presets = self.config.get("character_dna_presets", {})
        if char_input in presets:
            rel = presets[char_input].get("avatar_path")
            if rel:
                p = self.workspace_root / rel
                if p.exists():
                    return p

        # Kiểm tra đường dẫn trực tiếp
        direct = Path(char_input)
        if direct.exists():
            return direct.resolve()

        # Fallback ảnh mặc định nếu chưa có
        default_avatar = self.workspace_root / "assets" / "characters" / "lyly_master_portrait.png"
        return default_avatar

    def run_motion_transfer(
        self,
        ref_video_path: Path,
        avatar_path: Path,
        engine_type: MotionEngineType,
        job_dir: Path
    ) -> Path:
        """
        Thực thi chuyển động: Swap mặt nhân vật AI vào từng frame video mẫu,
        giữ nguyên chuyển động/dáng điệu/sản phẩm gốc.
        """
        reenacted_output = job_dir / "reenacted_raw.mp4"
        print(f"[*] Khởi chạy Motion Transfer Engine: {engine_type.value}")

        if engine_type == MotionEngineType.MOCK:
            # Passthrough thuần: không swap gì, chỉ re-encode để test nhanh pipeline không tốn GPU
            cmd = [
                "ffmpeg", "-y",
                "-i", str(ref_video_path),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                str(reenacted_output)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return reenacted_output

        if engine_type == MotionEngineType.KLING_MOTION_CONTROL:
            raise NotImplementedError(
                "Engine 'kling_motion' là Cloud API (trả phí) và chưa có adapter thật trong repo này. "
                "Dùng --engine local_faceswap (local, miễn phí) hoặc --engine mock để test."
            )

        # LOCAL_FACESWAP: InsightFace (buffalo_l) + inswapper_128.onnx, qua CoreML EP (fallback CPU)
        import cv2
        import insightface
        from insightface.app import FaceAnalysis

        swapper_model_path = str(self.workspace_root / "models" / "weights" / "inswapper_128.onnx")
        if not Path(swapper_model_path).exists():
            raise FileNotFoundError(f"Không tìm thấy model face-swap tại: {swapper_model_path}")

        print("[*] Nạp InsightFace Buffalo_L + Inswapper (providers: %s)..." % FACESWAP_PROVIDERS)
        app = FaceAnalysis(name="buffalo_l", providers=FACESWAP_PROVIDERS)
        app.prepare(ctx_id=0, det_size=(512, 512))
        swapper = insightface.model_zoo.get_model(swapper_model_path, providers=FACESWAP_PROVIDERS)

        source_img = cv2.imread(str(avatar_path))
        if source_img is None:
            raise FileNotFoundError(f"Không đọc được ảnh nhân vật AI tại: {avatar_path}")
        source_faces = app.get(source_img)
        if not source_faces:
            raise ValueError(f"Không tìm thấy khuôn mặt trong ảnh nhân vật AI: {avatar_path}")
        source_face = source_faces[0]
        print(f"[+] Đã trích xuất DNA khuôn mặt từ {avatar_path.name}")

        cap = cv2.VideoCapture(str(ref_video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"[*] Video mẫu: {width}x{height} @ {fps}fps, ~{total_frames} frame")

        temp_video = job_dir / "_reenacted_noaudio.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(temp_video), fourcc, fps, (width, height))

        frame_idx = 0
        swapped_count = 0
        t0 = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            faces = app.get(frame)
            if faces:
                primary_face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
                frame = swapper.get(frame, primary_face, source_face, paste_back=True)
                swapped_count += 1
            writer.write(frame)
        cap.release()
        writer.release()
        elapsed = time.time() - t0
        fps_processed = frame_idx / elapsed if elapsed > 0 else 0.0
        print(f"[+] Face swap xong: {swapped_count}/{frame_idx} frame có mặt, {elapsed:.1f}s ({fps_processed:.1f} fps xử lý)")

        # Mux lại audio gốc của video mẫu vào clip đã swap (bước audio ở execute() có thể thay thế sau)
        cmd_mux = [
            "ffmpeg", "-y",
            "-i", str(temp_video),
            "-i", str(ref_video_path),
            "-map", "0:v:0", "-map", "1:a:0?",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(reenacted_output)
        ]
        subprocess.run(cmd_mux, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return reenacted_output

    def resolve_voice_profile_id(self, char_input: str) -> Optional[str]:
        """Map tên preset nhân vật (hoặc đường dẫn ảnh trực tiếp) -> profile_id trong Voice Vault."""
        presets = self.config.get("character_dna_presets", {})
        if char_input in presets:
            return presets[char_input].get("voice_id")
        return None

    def generate_hyperframes_html(
        self,
        ref_video_path: Path,
        reenacted_video_path: Path,
        audio_path: Optional[Path],
        duration: float,
        layout: MimicLayoutMode,
        title_badge: str = "GOBI AI MIMIC SOTA",
        subtitle_text: Optional[str] = None
    ) -> str:
        """
        Tạo mã nguồn HTML5 cho HyperFrames Composition theo chuẩn 9:16 (1080x1920)
        hỗ trợ cả 3 dạng bố cục: Solo, Split 3 Tầng (What's up AI), Side-by-Side.
        """
        abs_ref = ref_video_path.resolve()
        abs_reenact = reenacted_video_path.resolve()
        abs_audio = audio_path.resolve() if audio_path and audio_path.exists() else None

        audio_markup = ""
        if abs_audio:
            audio_markup = f"""
    <audio id="main-audio" class="clip audio-track"
           src="{abs_audio}"
           data-start="0.000"
           data-duration="{duration:.3f}"
           data-track-index="0"
           data-volume="1.0"></audio>"""

        # Layout-specific CSS và HTML Structure
        if layout == MimicLayoutMode.SPLIT_3_TIER:
            # Chuẩn 3 tầng của What's up AI
            content_markup = f"""
    <!-- TẦNG 1: TOP PANEL (SLIDE / PROOF / STATS) -->
    <div class="tier top-tier">
      <div class="top-badge">{title_badge}</div>
      <div class="stats-card">
        <div class="stat-pill">🔥 1.3M VIEWS</div>
        <div class="stat-pill">+15.6K FOLLOWERS</div>
      </div>
    </div>

    <!-- TẦNG 2: MIDDLE PANEL (NHÂN VẬT GOBI AI BẮT CHƯỚC) -->
    <div class="tier mid-tier">
      <div class="tier-label">GOBI AI VIRTUAL IDOL</div>
      <video id="vid-reenact" class="clip tier-video"
             src="{abs_reenact}"
             playsinline muted loop
             data-start="0.000"
             data-duration="{duration:.3f}"
             data-track-index="1"></video>
    </div>

    <!-- TẦNG 3: BOTTOM PANEL (VIDEO MẪU / DRIVING SPEAKER) -->
    <div class="tier bot-tier">
      <div class="tier-label">REFERENCE MOTION GỐC</div>
      <video id="vid-ref" class="clip tier-video"
             src="{abs_ref}"
             playsinline muted loop
             data-start="0.000"
             data-duration="{duration:.3f}"
             data-track-index="2"></video>
    </div>
"""
            custom_layout_css = """
      .tier {
        width: 100%;
        height: 33.333%;
        position: relative;
        overflow: hidden;
        border-bottom: 3px solid rgba(255, 255, 255, 0.15);
      }
      .top-tier {
        background: radial-gradient(circle at center, #1e1e24 0%, #0d0d11 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 20px;
      }
      .top-badge {
        background: #ffe600;
        color: #000;
        font-weight: 900;
        font-size: 38px;
        padding: 12px 36px;
        border-radius: 16px;
        letter-spacing: 2px;
      }
      .stats-card {
        display: flex;
        gap: 20px;
      }
      .stat-pill {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        color: #fff;
        font-size: 28px;
        font-weight: 800;
        padding: 10px 24px;
        border-radius: 50px;
      }
      .tier-label {
        position: absolute;
        top: 20px;
        left: 30px;
        z-index: 10;
        background: rgba(0, 0, 0, 0.7);
        color: #ffe600;
        font-size: 22px;
        font-weight: 800;
        padding: 6px 16px;
        border-radius: 8px;
      }
      .tier-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
"""
        elif layout == MimicLayoutMode.SIDE_BY_SIDE:
            # Chia đôi so sánh: Trái (Gốc) | Phải (AI)
            content_markup = f"""
    <div class="duet-container">
      <div class="duet-pane left-pane">
        <div class="duet-label">VIDEO MẪU GỐC</div>
        <video id="vid-ref" class="clip duet-video"
               src="{abs_ref}"
               playsinline muted loop
               data-start="0.000"
               data-duration="{duration:.3f}"
               data-track-index="1"></video>
      </div>
      <div class="duet-pane right-pane">
        <div class="duet-label">GOBI AI BẮT CHƯỚC</div>
        <video id="vid-reenact" class="clip duet-video"
               src="{abs_reenact}"
               playsinline muted loop
               data-start="0.000"
               data-duration="{duration:.3f}"
               data-track-index="2"></video>
      </div>
    </div>
"""
            custom_layout_css = """
      .duet-container {
        display: flex;
        width: 100%;
        height: 100%;
      }
      .duet-pane {
        flex: 1;
        position: relative;
        height: 100%;
        overflow: hidden;
      }
      .left-pane { border-right: 4px solid #ffe600; }
      .duet-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .duet-label {
        position: absolute;
        top: 140px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
        background: rgba(0, 0, 0, 0.75);
        color: #fff;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 22px;
        white-space: nowrap;
      }
"""
        else:
            # SOLO: 100% Khung hình dọc là nhân vật AI
            content_markup = f"""
    <div class="solo-container">
      <video id="vid-reenact" class="clip solo-video"
             src="{abs_reenact}"
             playsinline muted loop
             data-start="0.000"
             data-duration="{duration:.3f}"
             data-track-index="1"></video>
    </div>
"""
            custom_layout_css = """
      .solo-container {
        width: 100%;
        height: 100%;
        position: relative;
      }
      .solo-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
"""

        # Phụ đề Kinetic Subtitles
        subtitle_markup = ""
        if subtitle_text:
            subtitle_markup = f"""
    <div class="kinetic-caption-container">
      <div class="caption-pill">{subtitle_text}</div>
    </div>
"""

        html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920" />
  <title>{title_badge}</title>
  <!-- GSAP for seekable deterministic animations -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body, html {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #000;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    #root, .stage {{
      position: relative;
      width: 1080px;
      height: 1920px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    /* TIKTOK SAFE ZONE OVERLAYS */
    .tiktok-safe-header {{
      position: absolute;
      top: 60px;
      left: 60px;
      z-index: 99;
      background: rgba(0,0,0,0.6);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 50px;
      padding: 12px 30px;
      color: #ffe600;
      font-weight: 900;
      font-size: 26px;
      letter-spacing: 1px;
    }}
    .kinetic-caption-container {{
      position: absolute;
      bottom: 260px;
      width: 100%;
      display: flex;
      justify-content: center;
      z-index: 100;
      padding: 0 40px;
    }}
    .caption-pill {{
      background: rgba(0, 0, 0, 0.85);
      border: 3px solid #ffe600;
      color: #ffffff;
      padding: 16px 36px;
      border-radius: 24px;
      font-size: 38px;
      font-weight: 900;
      text-align: center;
      box-shadow: 0 10px 40px rgba(0,0,0,0.8);
    }}
    {custom_layout_css}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{duration:.3f}" class="stage">
    <div class="tiktok-safe-header">{title_badge}</div>
    {content_markup}
    {subtitle_markup}
    {audio_markup}
  </div>

  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo(".tiktok-safe-header", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }}, 0.1);
    window.__timelines["main"] = tl;
    tl.seek(0);
  </script>
</body>
</html>
"""
        return html_template

    def execute(self, params: MotionMimicInput) -> MotionMimicResult:
        """
        Thực thi toàn bộ workflow bắt chước video nạp vào:
        1. Ingest Video mẫu (URL/Local).
        2. Resolve Avatar AI KOC.
        3. Motion Transfer (Lái chuyển động).
        4. Tách/Chuẩn bị Audio.
        5. HyperFrames Composition HTML5.
        6. Render MP4 Master.
        """
        job_id = f"mimic_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        job_dir = self.output_base / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        steps: List[MotionMimicExecutionStep] = []

        print(f"\n=======================================================")
        print(f"🎬 BẮT ĐẦU GOBI MOTION MIMIC WORKFLOW [{job_id}]")
        print(f"=======================================================")

        try:
            # BƯỚC 1: TIẾP NHẬN VIDEO MẪU
            s1 = MotionMimicExecutionStep(name="Ingest Reference Video", started_at=time.time())
            ref_path = self.ingest_reference_video(params.reference_video_path_or_url, job_dir)
            meta = self.get_video_metadata(ref_path)
            s1.status = "completed"
            s1.finished_at = time.time()
            s1.details = meta
            steps.append(s1)
            print(f"[✓] Bước 1 hoàn tất: Reference video {meta['width']}x{meta['height']}, {meta['duration']}s")

            # BƯỚC 2: GIẢI QUYẾT AVATAR NHÂN VẬT AI
            s2 = MotionMimicExecutionStep(name="Resolve Character Avatar", started_at=time.time())
            avatar_path = self.resolve_character_avatar(params.character_avatar_path)
            s2.status = "completed"
            s2.finished_at = time.time()
            s2.details = {"avatar_path": str(avatar_path)}
            steps.append(s2)
            print(f"[✓] Bước 2 hoàn tất: Nhân vật AI = {avatar_path.name}")

            # BƯỚC 3: TRUYỀN CHUYỂN ĐỘNG (MOTION TRANSFER)
            s3 = MotionMimicExecutionStep(name="Run Motion Transfer", started_at=time.time())
            reenacted_path = self.run_motion_transfer(
                ref_video_path=ref_path,
                avatar_path=avatar_path,
                engine_type=params.engine_type,
                job_dir=job_dir
            )
            s3.status = "completed"
            s3.finished_at = time.time()
            s3.details = {"reenacted_path": str(reenacted_path)}
            steps.append(s3)
            print(f"[✓] Bước 3 hoàn tất: Đã tạo video reenact")

            # BƯỚC 4: XỬ LÝ ÂM THANH
            s4 = MotionMimicExecutionStep(name="Process Audio", started_at=time.time())
            audio_out = job_dir / "audio_track.mp3"
            if params.audio_strategy == AudioStrategy.KEEP_ORIGINAL:
                audio_path = self.extract_audio(ref_path, audio_out)
            elif params.audio_strategy == AudioStrategy.OMNIVOICE_CLONE:
                if not params.spoken_script:
                    raise ValueError(
                        "--audio omnivoice cần kịch bản lời đọc mới: truyền --script \"...\" (hoặc --sub)."
                    )
                voice_profile_id = self.resolve_voice_profile_id(params.character_avatar_path) or "voice-fm-lyly"
                print(f"[*] Clone giọng qua Voice Vault profile: {voice_profile_id}")
                from gobi.services.voice.voice_cloner import VoiceCloner
                cloner = VoiceCloner()
                cloner.speak(
                    profile_id=voice_profile_id,
                    new_script=params.spoken_script,
                    output_path=str(audio_out),
                    engine="omnivoice"
                )
                audio_path = audio_out
            elif params.custom_bgm_path and Path(params.custom_bgm_path).exists():
                audio_path = Path(params.custom_bgm_path)
            else:
                audio_path = None
            s4.status = "completed"
            s4.finished_at = time.time()
            s4.details = {"audio_path": str(audio_path) if audio_path else None}
            steps.append(s4)
            print(f"[✓] Bước 4 hoàn tất: Audio Strategy = {params.audio_strategy.value}")

            # BƯỚC 5: LIP SYNC (chỉ chạy khi audio bị thay bằng giọng clone mới)
            s5 = MotionMimicExecutionStep(name="Lip Sync", started_at=time.time())
            video_for_compose = reenacted_path
            should_lipsync = (
                params.lipsync_mode == LipSyncMode.ON
                or (params.lipsync_mode == LipSyncMode.AUTO and params.audio_strategy == AudioStrategy.OMNIVOICE_CLONE)
            )
            if should_lipsync and audio_path and Path(audio_path).exists():
                try:
                    from gobi.adapters.integrations.wav2lip_adapter import Wav2LipAdapter
                    lipsynced_path = job_dir / "reenacted_lipsynced.mp4"
                    Wav2LipAdapter().run(
                        video_path=reenacted_path,
                        audio_path=Path(audio_path),
                        output_path=lipsynced_path
                    )
                    video_for_compose = lipsynced_path
                    s5.status = "completed"
                    s5.details = {"lipsynced_path": str(lipsynced_path)}
                    print(f"[✓] Bước 5 hoàn tất: Lip-sync xong -> {lipsynced_path.name}")
                except Exception as e_lip:
                    print(f"[!] Lip-sync lỗi ({e_lip}) — dùng video chưa lip-sync (khẩu hình theo audio gốc).")
                    s5.status = "skipped"
                    s5.error_message = str(e_lip)
                    s5.finished_at = time.time()
            else:
                s5.status = "skipped"
                print("[~] Bước 5 bỏ qua: không cần lip-sync (audio giữ nguyên gốc hoặc --lipsync off)")
            if s5.finished_at is None:
                s5.finished_at = time.time()
            steps.append(s5)

            # BƯỚC 6: TẠO DỰNG HYPERFRAMES COMPOSITION
            s6 = MotionMimicExecutionStep(name="Generate HyperFrames Project", started_at=time.time())
            hf_proj_dir = job_dir / "hyperframes_proj"
            hf_proj_dir.mkdir(parents=True, exist_ok=True)

            html_content = self.generate_hyperframes_html(
                ref_video_path=ref_path,
                reenacted_video_path=video_for_compose,
                audio_path=audio_path,
                duration=meta["duration"],
                layout=params.layout_mode,
                title_badge=params.title_badge,
                subtitle_text=params.subtitles_text
            )

            index_html_file = hf_proj_dir / "index.html"
            with open(index_html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Tạo file hyperframes.json hợp lệ
            hf_config = {
                "id": job_id,
                "fps": 30,
                "width": 1080,
                "height": 1920,
                "duration": meta["duration"],
                "entry": "index.html"
            }
            with open(hf_proj_dir / "hyperframes.json", "w", encoding="utf-8") as f:
                json.dump(hf_config, f, indent=2)

            s6.status = "completed"
            s6.finished_at = time.time()
            steps.append(s6)
            print(f"[✓] Bước 6 hoàn tất: Đã khởi tạo HyperFrames Project tại {hf_proj_dir}")

            # BƯỚC 7: RENDER MASTER VIDEO
            s7 = MotionMimicExecutionStep(name="Render Final Video", started_at=time.time())
            final_mp4_name = params.output_filename or f"{job_id}_master.mp4"
            final_mp4_path = self.output_base / final_mp4_name

            # Thực thi render qua HyperFramesEngine
            render_res = self.hyperframes_engine.render_project(
                project_dir=hf_proj_dir,
                output_file=final_mp4_path
            )
            s7.status = "completed"
            s7.finished_at = time.time()
            steps.append(s7)
            print(f"[✓] Bước 7 hoàn tất: Xuất bản video thành công tại {render_res}")

            return MotionMimicResult(
                job_id=job_id,
                is_success=True,
                output_video_path=str(render_res),
                hyperframes_project_dir=str(hf_proj_dir),
                duration_seconds=meta["duration"],
                steps=steps,
                metadata={
                    "layout": params.layout_mode.value,
                    "engine": params.engine_type.value,
                    "audio_strategy": params.audio_strategy.value,
                    "lipsync_mode": params.lipsync_mode.value
                }
            )

        except Exception as e:
            print(f"[!] Lỗi trong quy trình Motion Mimic: {e}")
            return MotionMimicResult(
                job_id=job_id,
                is_success=False,
                steps=steps,
                metadata={"error": str(e)}
            )
