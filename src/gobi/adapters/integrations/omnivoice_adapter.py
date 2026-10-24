"""
GOBI SOCIAL - OMNIVOICE ADAPTER
===============================
Adapter kết nối động cơ Zero-Shot Voice Cloning OmniVoice (k2-fsa/OmniVoice).
Chạy trên môi trường ảo chuyên biệt tại integrations/OmniVoice/.venv.
Hỗ trợ Apple Silicon Metal (MPS), CUDA và CPU.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
OMNIVOICE_DIR = PROJECT_ROOT / "integrations" / "OmniVoice"
OMNIVOICE_PYTHON = OMNIVOICE_DIR / ".venv" / "bin" / "python"


class OmniVoiceAdapter:
    def __init__(self, python_exe: Optional[str] = None):
        self.python_exe = Path(python_exe) if python_exe else OMNIVOICE_PYTHON
        if not self.python_exe.exists():
            raise FileNotFoundError(f"Không tìm thấy Python môi trường OmniVoice tại: {self.python_exe}")

    def create_prompt(
        self,
        profile_dir: str,
        ref_slice: Optional[str] = None,
        ref_text: Optional[str] = None
    ) -> str:
        """
        Trích xuất và mã hóa Audio Codes + Transcript thành OmniVoice Prompt (.pt).
        Lưu trữ vĩnh viễn vào profile_dir/omnivoice_prompt.pt.
        """
        p_dir = Path(profile_dir)
        prompt_file = p_dir / "omnivoice_prompt.pt"
        slice_file = Path(ref_slice) if ref_slice else p_dir / "reference_clean_slice.wav"
        
        if not ref_text:
            txt_file = p_dir / "reference_transcript.txt"
            if txt_file.exists():
                ref_text = txt_file.read_text(encoding="utf-8").strip()

        if not slice_file.exists():
            raise FileNotFoundError(f"Không tìm thấy file audio tham chiếu: {slice_file}")

        worker_script = f"""
import sys
from pathlib import Path
import torch

sys.path.insert(0, "{str(OMNIVOICE_DIR)}")
from omnivoice import OmniVoice

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="mps" if torch.backends.mps.is_available() else ("cuda:0" if torch.cuda.is_available() else "cpu"),
    dtype=torch.float16 if (torch.backends.mps.is_available() or torch.cuda.is_available()) else torch.float32,
    asr_model_name="openai/whisper-small",
    asr_device="cpu"
)

prompt = model.create_voice_clone_prompt(
    ref_audio=r"{str(slice_file)}",
    ref_text={repr(ref_text)}
)
prompt.save(r"{str(prompt_file)}")
print("PROMPT_SAVED:" + str(prompt_file))
"""
        cmd = [str(self.python_exe), "-c", worker_script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"OmniVoice prompt creation failed: {result.stderr}\nStdout: {result.stdout}")

        return str(prompt_file)

    def synthesize_from_profile(
        self,
        profile_dir: str,
        text: str,
        output_wav: str,
        speed: float = 1.0,
        num_step: int = 32,
        denoise: bool = True
    ) -> str:
        """
        Sinh âm thanh clone từ hồ sơ Sound Profile đã được tạo trong Voice Vault.
        Tự động sử dụng prompt đã cache (omnivoice_prompt.pt) hoặc tạo mới từ reference_clean_slice.wav.
        """
        p_dir = Path(profile_dir)
        prompt_file = p_dir / "omnivoice_prompt.pt"
        ref_slice = p_dir / "reference_clean_slice.wav"
        ref_txt_file = p_dir / "reference_transcript.txt"
        ref_text = ref_txt_file.read_text(encoding="utf-8").strip() if ref_txt_file.exists() else None

        output_path = Path(output_wav).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        worker_script = f"""
import sys
from pathlib import Path
import soundfile as sf
import torch

sys.path.insert(0, "{str(OMNIVOICE_DIR)}")
from omnivoice import OmniVoice, VoiceClonePrompt

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="mps" if torch.backends.mps.is_available() else ("cuda:0" if torch.cuda.is_available() else "cpu"),
    dtype=torch.float16 if (torch.backends.mps.is_available() or torch.cuda.is_available()) else torch.float32,
    asr_model_name="openai/whisper-small",
    asr_device="cpu"
)

prompt_path = Path(r"{str(prompt_file)}")
if prompt_path.exists():
    prompt = VoiceClonePrompt.load(str(prompt_path))
else:
    prompt = model.create_voice_clone_prompt(
        ref_audio=r"{str(ref_slice)}",
        ref_text={repr(ref_text)}
    )
    prompt.save(str(prompt_path))

audio = model.generate(
    text={repr(text)},
    language="vi",
    voice_clone_prompt=prompt,
    speed={speed},
    denoise={denoise},
    num_step={num_step}
)

sf.write(r"{str(output_path)}", audio[0], 24000)
"""
        cmd = [str(self.python_exe), "-c", worker_script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"OmniVoice synthesis failed: {result.stderr}\nStdout: {result.stdout}")

        return str(output_path)
