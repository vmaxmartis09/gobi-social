"""
GOBI SOCIAL - OLLAMA TEXT ADAPTER
=================================
Adapter gọi LLM cục bộ qua Ollama (mặc định qwen2.5:7b) để viết kịch bản review
mới — thay thế GeminiTextAdapter khi hết quota free-tier hoặc muốn chạy hoàn
toàn offline, không tốn chi phí cloud. Cùng schema đầu ra (RemixScript) nên
có thể hoán đổi trực tiếp cho GeminiTextAdapter trong content_remix_workflow.py.

[Đã test thực tế] deepseek-r1:7b KHÔNG dùng được cho việc này — model hay lẫn
tiếng Trung/Anh vào output dù prompt yêu cầu rõ tiếng Việt (đặc tính distill
thiên về reasoning tiếng Anh/Trung), và từng bịa link sản phẩm không có thật.
qwen2.5:7b cho kết quả tiếng Việt tự nhiên, bám đúng dữ liệu sản phẩm, không
bịa thông tin — dùng model này làm mặc định.

Yêu cầu: Ollama server đang chạy (`ollama serve`, mặc định cổng 11434) và đã
`ollama pull qwen2.5:7b` (hoặc model khác truyền vào qua `model=`).
"""

import json
import re
from typing import Any, Dict, Optional

import requests

from gobi.domain.scene_models import RemixScript, RemixScriptBeat

DEFAULT_MODEL = "qwen2.5:7b"
DEFAULT_BASE_URL = "http://localhost:11434"

PROMPT_TEMPLATE = """QUAN TRỌNG: Toàn bộ câu trả lời PHẢI viết 100% bằng TIẾNG VIỆT.
TUYỆT ĐỐI KHÔNG được dùng tiếng Trung, tiếng Anh, hay bất kỳ ngôn ngữ nào khác
trong bất kỳ giá trị chuỗi nào của JSON trả về.

Bạn là biên kịch TikTok Shop chuyên nghiệp cho KOC ảo "Gô Bi", viết kịch bản
hoàn toàn bằng tiếng Việt tự nhiên, đời thường như người Việt Nam nói chuyện.

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

YÊU CẦU ĐẦU RA: CHỈ trả về một JSON object đúng schema sau, không thêm chữ nào khác,
không giải thích, không suy luận trong câu trả lời cuối cùng. NHẮC LẠI: mọi giá trị
chuỗi (hook, beat_name, voiceover_line, cta) PHẢI viết bằng tiếng Việt, không dùng
tiếng Trung hay tiếng Anh:
{{
  "hook": "câu hook 3 giây đầu, giật tít, dừng lại ngón tay lướt",
  "beats": [
    {{"beat_name": "chi tiết sản phẩm", "voiceover_line": "...", "duration_hint": 5.0}},
    {{"beat_name": "trải nghiệm/mix đồ", "voiceover_line": "...", "duration_hint": 5.0}}
  ],
  "cta": "câu kêu gọi hành động cuối video, nhắc giỏ hàng"
}}
"""


class OllamaTextAdapter:
    def __init__(self, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")

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

        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",  # ép Ollama constrain output đúng JSON (deepseek-r1 hay lờ hướng dẫn JSON trong prompt)
                    "options": {"temperature": 0.4},
                },
                timeout=180,
            )
            resp.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(
                f"Không kết nối được Ollama tại {self.base_url} — chạy `ollama serve` "
                f"và `ollama pull {self.model}` trước khi dùng adapter này."
            ) from e

        raw_text = resp.json().get("response", "")
        return self._parse_response(raw_text)

    @staticmethod
    def _parse_response(raw_text: str) -> RemixScript:
        if not raw_text:
            raise RuntimeError("Ollama trả về rỗng.")

        # deepseek-r1 là reasoning model, hay bọc suy luận trong <think>...</think>
        # trước câu trả lời cuối — bóc bỏ phần này trước khi tìm JSON.
        cleaned = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL)

        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise RuntimeError(f"Không tìm thấy JSON hợp lệ trong phản hồi Ollama:\n{raw_text[:500]}")

        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON từ Ollama không hợp lệ: {e}\n{match.group(0)[:500]}") from e

        beats = [
            RemixScriptBeat(
                beat_name=b.get("beat_name", f"beat_{i+1}"),
                voiceover_line=b.get("voiceover_line", ""),
                duration_hint=float(b.get("duration_hint", 4.0))
            )
            for i, b in enumerate(data.get("beats", []))
        ]
        if not beats:
            raise RuntimeError("Ollama trả về kịch bản không có beat nào.")

        return RemixScript(
            hook=data.get("hook", ""),
            beats=beats,
            cta=data.get("cta", "")
        )
