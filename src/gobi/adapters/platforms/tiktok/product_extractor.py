"""TikTok Video to TikTok Shop Product Link Extractor.

Trích xuất thông tin sản phẩm và link TikTok Shop PDP (Product Detail Page)
trực tiếp từ link video TikTok có gắn giỏ hàng.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def extract_tiktok_shop_products(video_url: str) -> Dict[str, Any]:
    """Trích xuất danh sách sản phẩm TikTok Shop được gắn trong video TikTok.

    Args:
        video_url: URL của video TikTok (ví dụ: https://www.tiktok.com/@user/video/12345...
                   hoặc link rút gọn vt.tiktok.com).

    Returns:
        Dict chứa trạng thái, thông tin video, và danh sách sản phẩm (PDP links, title, cover, seller).
    """
    video_url = video_url.strip()
    if not video_url:
        return {"success": False, "error": "URL video không được để trống"}

    # Chuẩn bị file cấu hình tạm
    tmp_config = "/tmp/gobi_tiktok_req.json"
    with open(tmp_config, "w", encoding="utf-8") as f:
        json.dump({"url": video_url}, f)

    script_path = Path(__file__).parent / "extract_product.mjs"

    cmd = [
        "ego-browser",
        "nodejs",
        "-e",
        f"await import('file://{script_path.resolve()}')"
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=35
        )
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Quá thời gian tải trang TikTok (Timeout sau 35s)."
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Không tìm thấy trình duyệt ego-browser. Hãy đảm bảo ego-browser đã được cài đặt."
        }

    combined_output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    
    # Tìm dòng chứa JSON kết quả
    result = None
    for line in combined_output.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                candidate = json.loads(line)
                if "success" in candidate or "products" in candidate:
                    result = candidate
                    break
            except json.JSONDecodeError:
                continue

    if not result:
        return {
            "success": False,
            "error": f"Không thể phân tích dữ liệu trả về từ trình duyệt. Output: {combined_output[:300]}",
            "raw_output": combined_output
        }

    return result
