"""
Script thử nhanh GeminiImageAdapter.compose_outfit_image với 1 cặp ảnh thật có
sẵn trong repo. Chạy: PYTHONPATH=.:src .venv/bin/python scratch/test_gemini_outfit_compose.py
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

for line in (PROJECT_ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

from gobi.adapters.integrations.gemini_image_adapter import GeminiImageAdapter

character_image = PROJECT_ROOT / "assets/characters/lyly_master_portrait.png"
clothing_image = PROJECT_ROOT / "data/products/7694350317697142037_ao_len_tieu_miho_house_tiktokshop1010_chinhha/cover.jpg"
output_path = PROJECT_ROOT / "scratch/test_outfit_composite.png"

print(f"Character: {character_image} (exists={character_image.exists()})")
print(f"Clothing : {clothing_image} (exists={clothing_image.exists()})")

adapter = GeminiImageAdapter()
result = adapter.compose_outfit_image(
    character_image_path=character_image,
    clothing_image_path=clothing_image,
    output_path=output_path,
)
print(f"OK -> {result} ({result.stat().st_size} bytes)")
