"""
GOBI SOCIAL - GEMINI TEXT ADAPTER
=================================
Adapter gọi Gemini (text) để viết kịch bản review mới, dựa trên transcript
của 1 video tham khảo (học cấu trúc/nhịp độ, KHÔNG copy nguyên văn) + thông
tin sản phẩm thật (không bịa). Dùng chung GEMINI_API_KEY đã có trong .env
cho các tác vụ khác của dự án (os_kernel.py, generate_master_36_from_dna.py).
"""

import json
import os
import re
import time
from typing import Any, Dict, Optional

from gobi.domain.scene_models import RemixScript, RemixScriptBeat

DEFAULT_MODEL = "gemini-3.8-flash"

PROMPT_TEMPLATE = """Bạn là biên kịch TikTok Shop chuyên nghiệp cho KOC ảo "Gô Bi".

NHIỆM VỤ: Viết kịch bản review sản phẩm MỚI cho Gô Bi, lấy cảm hứng về CẤU TRÚC,
NHỊP ĐỘ và GIỌNG ĐIỆU bán hàng từ video tham khảo dưới đây — TUYỆT ĐỐI KHÔNG chép
nguyên văn lời thoại của video tham khảo. Mọi thông tin sản phẩm (giá, chất liệu,
USP) PHẢI lấy đúng từ dữ liệu sản phẩm thật được cung cấp, không được bịa thêm.

--- TRANSCRIPT VIDEO THAM KHẢO (chỉ để học văn phong/nhịp độ) ---
{reference_transcript}

--- THÔNG TIN SẢN PHẨM THẬT (bắt buộc dùng đúng, không bịa) ---
{product_info_json}

--- KỊCH BẢN MẪU CÓ SẴN CHO SẢN PHẨM NÀY (nếu có, tham khảo thêm) ---
{existing_koc_script}

--- PHONG CÁCH NHÂN VẬT ---
{persona_style}

YÊU CẦU ĐẦU RA: CHỈ trả về một JSON object đúng schema sau, không thêm chữ nào khác:
{{
  "hook": "câu hook 3 giây đầu, giật tít, dừng lại ngón tay lướt",
  "beats": [
    {{"beat_name": "chi tiết sản phẩm", "voiceover_line": "...", "duration_hint": 5.0}},
    {{"beat_name": "trải nghiệm/mix đồ", "voiceover_line": "...", "duration_hint": 5.0}}
  ],
  "cta": "câu kêu gọi hành động cuối video, nhắc giỏ hàng"
}}
"""


class GeminiTextAdapter:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Thiếu GEMINI_API_KEY (đặt trong file .env ở root dự án, xem .env.example)."
            )
        self.model = model

    def _client(self):
        from google import genai
        return genai.Client(api_key=self.api_key)

    def generate_remix_script(
        self,
        reference_transcript: str,
        product_info: Dict[str, Any],
        existing_koc_script: Optional[str] = None,
        persona_style: str = "GenZ thời trang, thân thiện, nụ cười sáng, nói chuyện tự nhiên như bạn gái thân"
    ) -> RemixScript:
        prompt = PROMPT_TEMPLATE.format(
            reference_transcript=reference_transcript.strip() or "(không có lời thoại / video không tiếng)",
            product_info_json=json.dumps(product_info, ensure_ascii=False, indent=2),
            existing_koc_script=existing_koc_script.strip() if existing_koc_script else "(không có)",
            persona_style=persona_style
        )

        client = self._client()
        raw_text = None
        last_error: Optional[Exception] = None

        # [GOBI] Gemini thỉnh thoảng trả lỗi tạm thời (503 UNAVAILABLE/quá tải, 429 rate limit)
        # — thử lại vài lần với backoff tăng dần trước khi báo lỗi thật sự.
        for attempt, delay in enumerate([0, 3, 8], start=1):
            if delay:
                print(f"[GeminiTextAdapter] Lỗi tạm thời, thử lại lần {attempt} sau {delay}s...")
                time.sleep(delay)
            try:
                response = client.models.generate_content(model=self.model, contents=prompt)
                raw_text = response.text
                last_error = None
                break
            except Exception as e:
                last_error = e
                msg = str(e)
                is_transient = any(code in msg for code in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"])
                if not is_transient:
                    break

        if last_error is not None:
            raise RuntimeError(f"Gọi Gemini thất bại sau nhiều lần thử: {last_error}") from last_error

        return self._parse_response(raw_text)

    @staticmethod
    def _parse_response(raw_text: str) -> RemixScript:
        if not raw_text:
            raise RuntimeError("Gemini trả về rỗng.")

        # Gemini đôi khi bọc JSON trong ```json ... ``` — bóc ra trước khi parse
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise RuntimeError(f"Không tìm thấy JSON hợp lệ trong phản hồi Gemini:\n{raw_text[:500]}")

        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON từ Gemini không hợp lệ: {e}\n{match.group(0)[:500]}") from e

        beats = [
            RemixScriptBeat(
                beat_name=b.get("beat_name", f"beat_{i+1}"),
                voiceover_line=b.get("voiceover_line", ""),
                duration_hint=float(b.get("duration_hint", 4.0))
            )
            for i, b in enumerate(data.get("beats", []))
        ]
        if not beats:
            raise RuntimeError("Gemini trả về kịch bản không có beat nào.")

        return RemixScript(
            hook=data.get("hook", ""),
            beats=beats,
            cta=data.get("cta", "")
        )
