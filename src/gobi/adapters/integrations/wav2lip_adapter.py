"""
GOBI SOCIAL - WAV2LIP ADAPTER
=============================
Adapter kết nối động cơ khớp khẩu hình Wav2Lip (bản ONNX, dựa trên
instant-high/wav2lip-onnx-HQ). Chạy trên môi trường ảo chuyên biệt tại
integrations/Wav2Lip/.venv, dùng CoreMLExecutionProvider trên Apple Silicon
(onnxruntime tự fallback CPU nếu không khả dụng).
"""

import subprocess
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
WAV2LIP_DIR = PROJECT_ROOT / "integrations" / "Wav2Lip"
WAV2LIP_PYTHON = WAV2LIP_DIR / ".venv" / "bin" / "python"
WAV2LIP_CHECKPOINT = WAV2LIP_DIR / "checkpoints" / "wav2lip_gan.onnx"


class Wav2LipAdapter:
    def __init__(self, python_exe: Optional[str] = None, checkpoint_path: Optional[str] = None):
        self.python_exe = Path(python_exe) if python_exe else WAV2LIP_PYTHON
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path else WAV2LIP_CHECKPOINT
        if not self.python_exe.exists():
            raise FileNotFoundError(f"Không tìm thấy Python môi trường Wav2Lip tại: {self.python_exe}")
        if not self.checkpoint_path.exists():
            raise FileNotFoundError(f"Không tìm thấy checkpoint Wav2Lip tại: {self.checkpoint_path}")

    def run(self, video_path: Path, audio_path: Path, output_path: Path) -> Path:
        """
        Khớp khẩu hình trong video theo audio mới.
        video_path: video đầu vào (đã swap mặt, khẩu hình theo audio GỐC).
        audio_path: audio mới (giọng clone) cần khớp môi theo.
        Trả về output_path khi thành công, raise RuntimeError khi thất bại.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # inference_onnxModel.py viết file tạm vào ./temp (tương đối cwd) nhưng không tự tạo thư mục này
        (WAV2LIP_DIR / "temp").mkdir(parents=True, exist_ok=True)

        cmd = [
            str(self.python_exe),
            "inference_onnxModel.py",
            "--checkpoint_path", str(self.checkpoint_path),
            "--face", str(video_path.resolve()),
            "--audio", str(audio_path.resolve()),
            "--outfile", str(output_path.resolve()),
        ]

        result = subprocess.run(
            cmd,
            cwd=str(WAV2LIP_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if result.returncode != 0 or not output_path.exists():
            raise RuntimeError(
                f"Wav2Lip lip-sync thất bại (exit code {result.returncode}):\n"
                f"{result.stdout[-4000:] if result.stdout else '(không có output)'}"
            )

        return output_path
