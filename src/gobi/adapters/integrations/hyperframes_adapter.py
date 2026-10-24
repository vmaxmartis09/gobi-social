"""
=============================================================================
🎬 HYPERFRAMES ADAPTER (TẦNG 3: INTEGRATIONS ADAPTER)
Bộ chuyển đổi kết nối framework HyperFrames (HeyGen) với Gobi Social Python.
Cho phép AI Agent và hệ thống backend điều khiển toàn bộ pipeline dựng video:
- Render HTML/CSS/GSAP thành video MP4 chuẩn tất định (deterministic).
- Lint & Check tính hợp lệ của composition trước khi xuất bản.
- Mở Live Preview / Studio tương tác trên trình duyệt.
=============================================================================
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List


class HyperFramesAdapter:
    """Adapter mỏng đóng gói toàn bộ lệnh gọi CLI của HeyGen HyperFrames."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path("/Volumes/Data/gobi-social")
        self.integrations_dir = self.workspace_root / "integrations" / "hyperframes"

    def is_available(self) -> bool:
        """Kiểm tra môi trường có Node.js và npx để chạy HyperFrames không."""
        return shutil.which("npx") is not None

    def init_project(self, project_dir: str | Path, example: str = "blank") -> Path:
        """Khởi tạo một HyperFrames project mới."""
        target_path = Path(project_dir).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = ["npx", "--yes", "hyperframes", "init", target_path.name, f"--example={example}"]
        # Chạy trong thư mục cha, không chặn khi preview khởi động
        proc = subprocess.Popen(
            cmd,
            cwd=str(target_path.parent),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            # Cho phép tạo file ban đầu rồi ngắt nếu lệnh cố mở server preview vô tận
            proc.communicate(input="\n", timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()

        return target_path

    def lint(self, project_dir: str | Path) -> bool:
        """Kiểm tra cú pháp và cấu trúc timeline của project."""
        target_path = Path(project_dir).resolve()
        cmd = ["npx", "--yes", "hyperframes", "lint"]
        res = subprocess.run(
            cmd,
            cwd=str(target_path),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return res.returncode == 0

    def check(self, project_dir: str | Path) -> bool:
        """Chạy bộ kiểm tra toàn diện trước khi render (Lint + Headless browser probe)."""
        target_path = Path(project_dir).resolve()
        cmd = ["npx", "--yes", "hyperframes", "check"]
        res = subprocess.run(
            cmd,
            cwd=str(target_path),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return res.returncode == 0

    def get_timeline(self, project_dir: str | Path) -> Dict[str, Any]:
        """Trích xuất dữ liệu timeline chi tiết (tracks, clips, timing) dưới dạng JSON."""
        target_path = Path(project_dir).resolve()
        cmd = ["npx", "--yes", "hyperframes", "timeline", "--json"]
        res = subprocess.run(
            cmd,
            cwd=str(target_path),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode == 0 and res.stdout.strip():
            try:
                return json.loads(res.stdout)
            except json.JSONDecodeError:
                pass
        return {}

    def render(
        self,
        project_dir: str | Path,
        output_file: str | Path,
        quality: str = "looks",
        fps: int = 30,
        extra_args: Optional[List[str]] = None
    ) -> Path:
        """
        Render composition thành file MP4 chất lượng cao.
        - quality: draft | looks | delivery
        - fps: số khung hình/giây (mặc định 30fps)
        """
        target_path = Path(project_dir).resolve()
        out_path = Path(output_file).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "npx", "--yes", "hyperframes", "render",
            "--output", str(out_path),
            "--quality", quality,
            "--fps", str(fps)
        ]
        if extra_args:
            cmd.extend(extra_args)

        # Chạy render với stdin đóng để không bị treo bởi khảo sát NPS
        res = subprocess.run(
            cmd,
            cwd=str(target_path),
            input="\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if not out_path.exists() or out_path.stat().st_size == 0:
            raise RuntimeError(
                f"HyperFrames render thất bại (Exit code {res.returncode}):\n{res.stderr}\n{res.stdout}"
            )

        return out_path

    def preview(self, project_dir: str | Path, background: bool = True) -> subprocess.Popen:
        """Mở Live Preview Studio trên trình duyệt để kiểm tra timeline tương tác."""
        target_path = Path(project_dir).resolve()
        cmd = ["npx", "--yes", "hyperframes", "preview"]
        if background:
            cmd.append("--background")

        proc = subprocess.Popen(
            cmd,
            cwd=str(target_path),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return proc
