"""
GOBI SOCIAL - GEMINI IMAGE ADAPTER
===================================
Adapter gọi Gemini (multi-image -> image) để ghép trang phục sản phẩm lên ảnh
nhân vật Gô Bi — giữ nguyên danh tính/dáng người, chỉ đổi outfit. Thay thế bước
dán tay vào Google Flow (chế độ Hình ảnh, Nano Banana) từng thử và bị chặn tài
khoản (xem conversation/sessions/SESS-021_flow_koc_review_video_pipeline.md),
gọi thẳng Gemini API nên tự động hoá được trong pipeline. Dùng chung
GEMINI_API_KEY trong .env như GeminiTextAdapter.
"""

import os
import time
from pathlib import Path
from typing import Optional

from PIL import Image

DEFAULT_PROMPT = (
    "The person in the first image wears the exact clothing item shown in the "
    "second image. Keep the person's face, hair, body shape and identity "
    "completely unchanged — only replace the outfit. Full body, front-facing "
    "view, studio lighting, photorealistic, high detail fabric texture."
)

# Thử lần lượt các model ảnh Gemini theo thứ tự ưu tiên — tên/preview có thể
# chưa bật cho mọi API key, nên fallback thay vì hardcode 1 model duy nhất.
# Danh sách đã xác nhận hoạt động trong scripts/dataset/generate_master_36_from_dna.py.
IMAGE_MODELS = [
    "gemini-3-pro-image",
    "gemini-3.1-flash-image-preview",
    "gemini-2.5-flash-image",
    "gemini-3.1-flash-lite-image",
    "gemini-3-pro-image-preview",
]


class GeminiImageAdapter:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Thiếu GEMINI_API_KEY (đặt trong file .env ở root dự án, xem .env.example)."
            )

    def _client(self):
        from google import genai
        return genai.Client(api_key=self.api_key)

    def compose_outfit_image(
        self,
        character_image_path: str | Path,
        clothing_image_path: str | Path,
        output_path: str | Path,
        instruction: str = DEFAULT_PROMPT,
    ) -> Path:
        """
        Ghép nhân vật ở character_image_path mặc trang phục ở clothing_image_path
        thành 1 ảnh mới, lưu tại output_path. Trả về Path ảnh kết quả.
        Raise RuntimeError nếu mọi model trong IMAGE_MODELS đều lỗi.
        """
        character_img = Image.open(character_image_path)
        clothing_img = Image.open(clothing_image_path)
        client = self._client()

        last_error: Optional[Exception] = None
        for model_name in IMAGE_MODELS:
            # [GOBI] Gemini thỉnh thoảng lỗi tạm thời (503/429) — thử lại 1 lần
            # trước khi bỏ qua model này và sang model kế tiếp trong danh sách.
            for attempt, delay in enumerate([0, 3], start=1):
                if delay:
                    time.sleep(delay)
                try:
                    from google.genai import types

                    response = client.models.generate_content(
                        model=model_name,
                        contents=[character_img, clothing_img, instruction],
                        config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
                    )
                    image_bytes = self._extract_image_bytes(response)
                    if image_bytes:
                        out = Path(output_path)
                        out.parent.mkdir(parents=True, exist_ok=True)
                        out.write_bytes(image_bytes)
                        return out
                    last_error = RuntimeError(f"{model_name} không trả về ảnh nào.")
                except Exception as e:
                    last_error = e
                    msg = str(e)
                    is_transient = any(code in msg for code in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"])
                    if not is_transient:
                        break  # lỗi không tạm thời -> bỏ model này, thử model kế tiếp

        raise RuntimeError(f"Ghép trang phục AI thất bại với mọi model: {last_error}") from last_error

    @staticmethod
    def _extract_image_bytes(response) -> Optional[bytes]:
        candidates = getattr(response, "candidates", None) or []
        if not candidates:
            return None
        parts = getattr(candidates[0].content, "parts", None) or []
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and inline_data.data:
                return inline_data.data
        return None
