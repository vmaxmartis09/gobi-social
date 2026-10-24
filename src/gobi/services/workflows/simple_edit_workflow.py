"""
=============================================================================
🎬 GOBI SIMPLE EDIT WORKFLOW (TẦNG 2: SERVICES - WORKFLOWS)
Pipeline tối giản cho video "product_only" (lookbook/outfit, không nói trực
diện): GIỮ NGUYÊN hình ảnh + âm thanh gốc của video tham khảo, chỉ thêm 1 tag
sản phẩm nhỏ góc dưới — không Gemini, không ghép ảnh Gô Bi, không voice clone.
=============================================================================
"""

import json
import shutil
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from gobi.domain.scene_models import ContentRemixResult, ContentRemixExecutionStep
from gobi.services.media import video_ingest
from gobi.services.media.hyperframes_engine import HyperFramesEngine

PROJECT_ROOT = Path("/Volumes/Data/gobi-social")


class SimpleEditWorkflow:
    """Edit tối giản, chill — giữ nguyên video gốc, chỉ thêm tag sản phẩm nhỏ."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or PROJECT_ROOT
        self.hyperframes_engine = HyperFramesEngine(self.workspace_root)
        self.output_base = self.workspace_root / "output" / "simple_edit_workflow"
        self.output_base.mkdir(parents=True, exist_ok=True)

    def generate_chill_html(self, video_relpath: str, duration: float, product_name: str) -> str:
        """HTML tối giản: 1 video full khung hình + 1 tag nhỏ góc dưới-trái, không pill to/CTA chớp nháy."""
        return f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Gobi Social - Simple Chill Edit</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; position: relative; overflow: hidden; }}
      .main-clip {{
        position: absolute; top: 0; left: 0;
        width: 1080px; height: 1920px; object-fit: cover;
      }}
      .product-tag {{
        position: absolute;
        bottom: 260px;
        left: 50px;
        z-index: 10;
        background: rgba(20, 20, 20, 0.55);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 14px;
        padding: 10px 20px;
        color: #f5f5f5;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 28px;
        font-weight: 500;
        letter-spacing: 0.01em;
        max-width: 700px;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.3f}" data-width="1080" data-height="1920">
      <video id="main-video" class="clip main-clip"
             src="{video_relpath}"
             playsinline
             data-start="0.000"
             data-duration="{duration:.3f}"
             data-track-index="1"></video>
      <div id="product-tag" class="product-tag">{product_name}</div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#product-tag", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }}, 0.3);
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>"""

    def execute(
        self,
        reference_video_path_or_url: str,
        product_data: Dict[str, Any],
        title_badge: str = "GOBI AI REVIEW",
        output_filename: Optional[str] = None,
        pre_ingested_ref_path: Optional[Path] = None,
    ) -> ContentRemixResult:
        job_id = f"simple_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        job_dir = self.output_base / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        steps = []

        print(f"\n=======================================================")
        print(f"🎬 BẮT ĐẦU GOBI SIMPLE EDIT WORKFLOW [{job_id}]")
        print(f"=======================================================")

        try:
            s1 = ContentRemixExecutionStep(name="Ingest Reference Video", started_at=time.time())
            if pre_ingested_ref_path and Path(pre_ingested_ref_path).exists():
                ref_path = Path(pre_ingested_ref_path)
            else:
                ref_path = video_ingest.ingest_reference_video(
                    reference_video_path_or_url, job_dir, self.workspace_root
                )
            meta = video_ingest.get_video_metadata(ref_path)
            s1.status = "completed"
            s1.finished_at = time.time()
            steps.append(s1)
            print(f"[✓] Bước 1 hoàn tất: {ref_path.name} ({meta['duration']}s)")

            s2 = ContentRemixExecutionStep(name="Build Chill Composition", started_at=time.time())
            proj_dir = self.output_base / job_id / "hyperframes_proj"
            assets_dir = proj_dir / "assets"
            assets_dir.mkdir(parents=True, exist_ok=True)

            dest_video = assets_dir / f"ref{ref_path.suffix}"
            shutil.copy2(ref_path, dest_video)

            product_name = product_data.get("product_info", {}).get("product_name", title_badge)
            html_content = self.generate_chill_html(
                video_relpath=f"assets/{dest_video.name}",
                duration=meta["duration"],
                product_name=product_name
            )
            (proj_dir / "index.html").write_text(html_content, encoding="utf-8")
            hf_config = {
                "id": job_id, "fps": 30, "width": 1080, "height": 1920,
                "duration": meta["duration"], "entry": "index.html"
            }
            (proj_dir / "hyperframes.json").write_text(json.dumps(hf_config, indent=2), encoding="utf-8")
            s2.status = "completed"
            s2.finished_at = time.time()
            steps.append(s2)
            print(f"[✓] Bước 2 hoàn tất: Composition chill đã khởi tạo tại {proj_dir}")

            s3 = ContentRemixExecutionStep(name="Render Final Video", started_at=time.time())
            final_mp4_name = output_filename or f"{job_id}_master.mp4"
            final_mp4_path = self.output_base / final_mp4_name
            render_res = self.hyperframes_engine.render_project(
                project_dir=proj_dir,
                output_file=final_mp4_path
            )
            s3.status = "completed"
            s3.finished_at = time.time()
            steps.append(s3)
            print(f"[✓] Bước 3 hoàn tất: Xuất bản video thành công tại {render_res}")

            return ContentRemixResult(
                job_id=job_id,
                is_success=True,
                output_video_path=str(render_res),
                hyperframes_project_dir=str(proj_dir),
                duration_seconds=meta["duration"],
                steps=steps,
                metadata={"workflow": "simple_edit", "product_name": product_name}
            )

        except Exception as e:
            print(f"[!] Lỗi trong quy trình Simple Edit: {e}")
            return ContentRemixResult(
                job_id=job_id,
                is_success=False,
                steps=steps,
                metadata={"error": str(e)}
            )
