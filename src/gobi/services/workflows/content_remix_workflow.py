"""
=============================================================================
🎬 GOBI CONTENT REMIX WORKFLOW ENGINE (TẦNG 2: SERVICES - WORKFLOWS)
Pipeline: Video tham khảo (học nội dung/nhịp độ, KHÔNG dùng hình ảnh) ->
Kịch bản mới (Gemini) -> Ảnh sản phẩm/Gô Bi + giọng clone -> HyperFrames.
Không swap mặt lên video người khác — khác với MotionMimicWorkflow.
=============================================================================
"""

import glob
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from gobi.domain.scene_models import (
    ContentRemixInput,
    ContentRemixResult,
    ContentRemixExecutionStep,
    RemixScript,
    SceneMotion,
)
from gobi.domain.motion_mimic_models import AudioStrategy
from gobi.domain.policy_compliance_checker import PolicyComplianceChecker
from gobi.services.media import video_ingest
from gobi.services.media.hyperframes_engine import HyperFramesEngine
from gobi.services.voice.audio_preprocessor import AudioPreprocessor
from gobi.adapters.integrations.gemini_text_adapter import GeminiTextAdapter

PROJECT_ROOT = Path("/Volumes/Data/gobi-social")
MIMIC_CONFIG_PATH = PROJECT_ROOT / "configs" / "workflows" / "motion_mimic_config.json"
PRODUCT_CATALOG_DIR = PROJECT_ROOT / "configs" / "products" / "catalog"

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")
MOTION_CYCLE = [SceneMotion.ZOOM_IN, SceneMotion.PAN_DOWN, SceneMotion.PAN_HORIZONTAL]


class ContentRemixWorkflow:
    """Quy trình độc lập: video tham khảo -> kịch bản mới -> video Gô Bi (không swap mặt)."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or PROJECT_ROOT
        self.hyperframes_engine = HyperFramesEngine(self.workspace_root)
        self.preprocessor = AudioPreprocessor()
        self.config = self._load_character_config()
        self.output_base = self.workspace_root / "output" / "remix_workflow"
        self.output_base.mkdir(parents=True, exist_ok=True)

    def _load_character_config(self) -> Dict[str, Any]:
        """Tái dùng character_dna_presets từ motion_mimic_config.json (tránh định nghĩa lại preset nhân vật)."""
        if MIMIC_CONFIG_PATH.exists():
            try:
                with open(MIMIC_CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Warning: Lỗi đọc {MIMIC_CONFIG_PATH}: {e}")
        return {}

    def resolve_character_avatar(self, char_input: str) -> Path:
        presets = self.config.get("character_dna_presets", {})
        if char_input in presets:
            rel = presets[char_input].get("avatar_path")
            if rel:
                p = self.workspace_root / rel
                if p.exists():
                    return p
        direct = Path(char_input)
        if direct.exists():
            return direct.resolve()
        return self.workspace_root / "assets" / "characters" / "lyly_master_portrait.png"

    def resolve_voice_profile_id(self, char_input: str) -> Optional[str]:
        presets = self.config.get("character_dna_presets", {})
        if char_input in presets:
            return presets[char_input].get("voice_id")
        return None

    def load_product_data(self, product_code: str) -> Dict[str, Any]:
        """Đọc product_info.json + koc_script.md thật từ configs/products/catalog/<mã_sp>/."""
        product_dir = PRODUCT_CATALOG_DIR / product_code
        info_path = product_dir / "product_info.json"
        if not info_path.exists():
            raise FileNotFoundError(f"Không tìm thấy sản phẩm '{product_code}' tại: {info_path}")

        with open(info_path, "r", encoding="utf-8") as f:
            product_info = json.load(f)

        script_path = product_dir / "koc_script.md"
        existing_script = script_path.read_text(encoding="utf-8") if script_path.exists() else None

        return {"product_info": product_info, "existing_koc_script": existing_script, "product_dir": product_dir}

    def load_product_data_from_json(self, product_info_path: str) -> Dict[str, Any]:
        """
        Đọc product_info trực tiếp từ 1 file JSON cho trước (dùng khi sản phẩm không có
        trong catalog — vd: job được nạp qua Dashboard tại data/products/<folder>/).
        product_dir = thư mục cha của file này (để resolve_scene_images tìm ảnh cover.jpg cùng chỗ).
        """
        info_path = Path(product_info_path)
        if not info_path.exists():
            raise FileNotFoundError(f"Không tìm thấy product_info_path tại: {info_path}")

        with open(info_path, "r", encoding="utf-8") as f:
            product_info = json.load(f)

        return {"product_info": product_info, "existing_koc_script": None, "product_dir": info_path.parent}

    def resolve_scene_images(self, product_dir: Path, character_avatar: Path, count: int) -> List[Path]:
        """
        Lấy ảnh sản phẩm thật: ưu tiên product_dir/assets/ (catalog chuẩn), sau đó ảnh rời ngay
        trong product_dir (vd: cover.jpg của job dashboard). Nếu không có gì, dùng ảnh chân dung Gô Bi.
        """
        search_dirs = [product_dir / "assets", product_dir]
        images: List[Path] = []
        for d in search_dirs:
            if not d.exists():
                continue
            for ext in IMAGE_EXTS:
                images.extend(sorted(Path(p) for p in glob.glob(str(d / f"*{ext}"))))
            if images:
                break

        if not images:
            print(f"[!] Sản phẩm chưa có ảnh trong {product_dir} — dùng ảnh chân dung Gô Bi cho mọi cảnh.")
            return [character_avatar] * count

        # Lặp vòng ảnh sản phẩm nếu số cảnh nhiều hơn số ảnh có sẵn
        return [images[i % len(images)] for i in range(count)]

    def compose_outfit_scene_images(
        self, character_avatar: Path, raw_scene_images: List[Path], job_dir: Path
    ) -> List[Path]:
        """
        Ghép Gô Bi (character_avatar) mặc từng trang phục trong raw_scene_images bằng
        GeminiImageAdapter — giữ nguyên mặt/dáng người, chỉ đổi outfit — thay vì chỉ
        Ken Burns ảnh sản phẩm thô. Ảnh nào ghép lỗi thì fallback về ảnh gốc, không
        chặn cứng cả pipeline (cùng tinh thần fallback với Bước 4: Gemini -> Ollama).
        """
        try:
            from gobi.adapters.integrations.gemini_image_adapter import GeminiImageAdapter
            composer = GeminiImageAdapter()
        except Exception as e:
            print(f"[!] GeminiImageAdapter không khởi tạo được ({e}) — dùng ảnh sản phẩm gốc.")
            return raw_scene_images

        composited: List[Path] = []
        for idx, product_img in enumerate(raw_scene_images):
            if Path(product_img) == Path(character_avatar):
                composited.append(Path(product_img))  # không có ảnh sản phẩm riêng để ghép
                continue
            out_path = job_dir / f"outfit_composite_{idx:02d}.png"
            try:
                composited.append(
                    composer.compose_outfit_image(
                        character_image_path=character_avatar,
                        clothing_image_path=product_img,
                        output_path=out_path,
                    )
                )
            except Exception as e:
                print(f"[!] Ghép trang phục AI lỗi ở cảnh {idx} ({e}) — dùng ảnh sản phẩm gốc.")
                composited.append(Path(product_img))
        return composited

    def execute(self, params: ContentRemixInput) -> ContentRemixResult:
        job_id = f"remix_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        job_dir = self.output_base / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        steps: List[ContentRemixExecutionStep] = []

        print(f"\n=======================================================")
        print(f"🎬 BẮT ĐẦU GOBI CONTENT REMIX WORKFLOW [{job_id}]")
        print(f"=======================================================")

        try:
            # BƯỚC 1: INGEST VIDEO THAM KHẢO
            s1 = ContentRemixExecutionStep(name="Ingest Reference Video", started_at=time.time())
            ref_path = video_ingest.ingest_reference_video(
                params.reference_video_path_or_url, job_dir, self.workspace_root
            )
            s1.status = "completed"
            s1.finished_at = time.time()
            steps.append(s1)
            print(f"[✓] Bước 1 hoàn tất: {ref_path.name}")

            # BƯỚC 2: TRANSCRIBE AUDIO THAM KHẢO (Whisper local)
            s2 = ContentRemixExecutionStep(name="Transcribe Reference Audio", started_at=time.time())
            ref_audio_path = job_dir / "ref_audio.wav"
            video_ingest.extract_audio(ref_path, job_dir / "ref_audio.mp3")
            try:
                reference_transcript = self.preprocessor.transcribe_audio(str(job_dir / "ref_audio.mp3"))
            except Exception as e_tr:
                print(f"[!] Transcribe lỗi ({e_tr}) — tiếp tục không có transcript tham khảo.")
                reference_transcript = ""
            s2.status = "completed"
            s2.finished_at = time.time()
            s2.details = {"transcript_preview": reference_transcript[:200]}
            steps.append(s2)
            print(f"[✓] Bước 2 hoàn tất: transcript ~{len(reference_transcript)} ký tự")

            # BƯỚC 3: NẠP DỮ LIỆU SẢN PHẨM THẬT
            s3 = ContentRemixExecutionStep(name="Load Product Data", started_at=time.time())
            if params.product_info_path:
                product_data = self.load_product_data_from_json(params.product_info_path)
            elif params.product_code:
                product_data = self.load_product_data(params.product_code)
            else:
                raise ValueError("Cần truyền product_code (catalog) hoặc product_info_path (JSON trực tiếp).")
            s3.status = "completed"
            s3.finished_at = time.time()
            steps.append(s3)
            print(f"[✓] Bước 3 hoàn tất: {product_data['product_info'].get('product_name')}")

            # BƯỚC 4: VIẾT KỊCH BẢN MỚI (GEMINI, FALLBACK SANG OLLAMA CỤC BỘ NẾU HẾT QUOTA)
            s4 = ContentRemixExecutionStep(name="Generate Remix Script (Gemini)", started_at=time.time())
            script_engine = "gemini"
            try:
                gemini = GeminiTextAdapter()
                remix_script: RemixScript = gemini.generate_remix_script(
                    reference_transcript=reference_transcript,
                    product_info=product_data["product_info"],
                    existing_koc_script=product_data["existing_koc_script"]
                )
            except Exception as gemini_error:
                print(f"[!] Gemini lỗi ({gemini_error}) — fallback sang Ollama cục bộ (deepseek-r1)...")
                from gobi.adapters.integrations.ollama_text_adapter import OllamaTextAdapter
                script_engine = "ollama"
                ollama = OllamaTextAdapter()
                remix_script = ollama.generate_remix_script(
                    reference_transcript=reference_transcript,
                    product_info=product_data["product_info"],
                    existing_koc_script=product_data["existing_koc_script"]
                )
            s4.status = "completed"
            s4.finished_at = time.time()
            s4.details = {"num_beats": len(remix_script.beats), "engine": script_engine}
            steps.append(s4)
            print(f"[✓] Bước 4 hoàn tất ({script_engine}): hook=\"{remix_script.hook[:60]}...\", {len(remix_script.beats)} beats")

            # BƯỚC 5: QUÉT COMPLIANCE KỊCH BẢN (cảnh báo, không chặn cứng)
            s5 = ContentRemixExecutionStep(name="Policy Compliance Scan", started_at=time.time())
            full_script_text = " ".join(
                [remix_script.hook] + [b.voiceover_line for b in remix_script.beats] + [remix_script.cta]
            )
            compliance = PolicyComplianceChecker.scan(full_script_text)
            if not compliance["is_compliant"]:
                print(f"[!] CẢNH BÁO compliance: {compliance['total_violations']} vi phạm tiềm ẩn — {compliance['details']}")
            s5.status = "completed"
            s5.finished_at = time.time()
            s5.details = compliance
            steps.append(s5)
            print(f"[✓] Bước 5 hoàn tất: compliant={compliance['is_compliant']}")

            # BƯỚC 6: SINH GIỌNG CLONE TỪNG BEAT + ĐO DURATION THẬT
            s6 = ContentRemixExecutionStep(name="Synthesize Voice Per Beat", started_at=time.time())
            voice_profile_id = self.resolve_voice_profile_id(params.character_avatar_path) or "voice-fm-lyly"
            character_avatar = self.resolve_character_avatar(params.character_avatar_path)

            all_lines = [remix_script.hook] + [b.voiceover_line for b in remix_script.beats] + [remix_script.cta]
            beat_audio_paths: List[Path] = []

            if params.audio_strategy == AudioStrategy.OMNIVOICE_CLONE:
                from gobi.services.voice.voice_cloner import VoiceCloner
                cloner = VoiceCloner()
                for i, line in enumerate(all_lines):
                    beat_audio = job_dir / f"beat_{i:02d}.mp3"
                    cloner.speak(
                        profile_id=voice_profile_id,
                        new_script=line,
                        output_path=str(beat_audio),
                        engine="omnivoice"
                    )
                    beat_audio_paths.append(beat_audio)
            else:
                raise NotImplementedError(
                    "ContentRemixWorkflow hiện chỉ hỗ trợ --audio omnivoice "
                    "(kịch bản là nội dung MỚI, không có audio gốc để giữ nguyên)."
                )

            beat_durations = [self.hyperframes_engine.get_audio_duration(p) for p in beat_audio_paths]
            s6.status = "completed"
            s6.finished_at = time.time()
            steps.append(s6)
            print(f"[✓] Bước 6 hoàn tất: {len(beat_audio_paths)} audio clip, tổng {sum(beat_durations):.1f}s")

            # Nối các audio clip thành 1 track hoàn chỉnh
            final_audio_path = job_dir / "voiceover_full.mp3"
            self._concat_audio(beat_audio_paths, final_audio_path)

            # BƯỚC 7: CHỌN ẢNH CẢNH CHO TỪNG BEAT (+ GHÉP TRANG PHỤC BẰNG AI NẾU BẬT)
            s7 = ContentRemixExecutionStep(name="Resolve Scene Images", started_at=time.time())
            product_dir = product_data["product_dir"]
            raw_scene_images = self.resolve_scene_images(product_dir, character_avatar, len(all_lines))
            if params.use_ai_outfit_compositing:
                scene_images = self.compose_outfit_scene_images(character_avatar, raw_scene_images, job_dir)
            else:
                scene_images = raw_scene_images
            s7.status = "completed"
            s7.finished_at = time.time()
            steps.append(s7)
            print(f"[✓] Bước 7 hoàn tất: {len(scene_images)} ảnh cảnh")

            # BƯỚC 8: DỰNG KEN BURNS QUA HYPERFRAMES
            s8 = ContentRemixExecutionStep(name="Render via HyperFrames", started_at=time.time())
            beat_names = ["HOOK"] + [b.beat_name for b in remix_script.beats] + ["CTA"]
            scenes = [
                {
                    "img": str(scene_images[i]),
                    "duration": beat_durations[i],
                    "sub": (all_lines[i][:80] + "...") if len(all_lines[i]) > 80 else all_lines[i],
                }
                for i in range(len(all_lines))
            ]

            final_mp4_name = params.output_filename or f"{job_id}_master.mp4"
            final_mp4_path = self.output_base / final_mp4_name

            render_res = self.hyperframes_engine.create_and_render_video(
                scenes=scenes,
                audio_voiceover_path=final_audio_path,
                output_mp4=final_mp4_path,
                title_badge=params.title_badge,
                temp_project_name=job_id
            )
            s8.status = "completed"
            s8.finished_at = time.time()
            steps.append(s8)
            print(f"[✓] Bước 8 hoàn tất: Xuất bản video thành công tại {render_res}")

            hf_proj_dir = self.workspace_root / "output" / "hyperframes_projects" / job_id

            return ContentRemixResult(
                job_id=job_id,
                is_success=True,
                output_video_path=str(render_res),
                hyperframes_project_dir=str(hf_proj_dir),
                duration_seconds=sum(beat_durations),
                remix_script=remix_script,
                steps=steps,
                metadata={
                    "product_code": params.product_code,
                    "character": params.character_avatar_path,
                    "compliance_ok": compliance["is_compliant"],
                }
            )

        except Exception as e:
            print(f"[!] Lỗi trong quy trình Content Remix: {e}")
            return ContentRemixResult(
                job_id=job_id,
                is_success=False,
                steps=steps,
                metadata={"error": str(e)}
            )

    @staticmethod
    def _concat_audio(audio_paths: List[Path], output_path: Path) -> Path:
        """Nối nhiều file audio thành 1 track bằng ffmpeg concat demuxer."""
        import subprocess
        concat_list = output_path.parent / "concat_list.txt"
        with open(concat_list, "w", encoding="utf-8") as f:
            for p in audio_paths:
                f.write(f"file '{p.resolve()}'\n")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c:a", "libmp3lame", "-q:a", "2",
            str(output_path)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return output_path
