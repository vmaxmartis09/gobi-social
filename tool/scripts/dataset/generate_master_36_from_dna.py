import os
import sys
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

# Load .env
env_path = Path(r"./.env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: No GEMINI_API_KEY found")
    sys.exit(1)

client = genai.Client(api_key=api_key)

master_dna_path = Path(r"./assets/datasets/koc/MASTER_KOC_DNA.jpg")
master_img = Image.open(master_dna_path)

prompt = """Create an ultra-realistic 8K 36-panel camera angle and pose reference storyboard (strict 6x6 grid layout of 36 equal square panels with thin clean white borders) featuring the EXACT SAME young Vietnamese woman from the attached reference image (MASTER_KOC_DNA.jpg).

CRITICAL IDENTITY & WARDROBE LOCK (100% CONSISTENCY WITH ATTACHED REFERENCE IMAGE):
1. FACE & HAIR: Must be the exact same woman in the reference photo — sleek, natural straight jet-black hair with a soft off-center side part draped over her shoulders, soft natural Vietnamese eyebrows, clear expressive dark brown almond eyes with natural double eyelids, refined narrow straight high nose bridge with a petite feminine tip, lean sculpted cheeks with a delicate V-line jawline, and natural soft rose-pink lips. Fair luminous porcelain-warm skin.
2. WARDROBE: Keep the EXACT SAME outfit from the reference image across all 36 panels (NO glasses, NO brown shirt):
   - Ivory/cream silk satin cowl-neck camisole top
   - Soft cream cashmere cardigan draped/worn effortlessly over the shoulders
   - High-waisted tailored light beige trousers
   - Delicate thin gold chain necklace with a tiny pendant
3. STUDIO & NUMBERING:
   - Minimalist warm-gray studio background across all 36 panels.
   - Numbered sequentially 1 to 36 in the top-left corner of each panel, with short Vietnamese caption at the bottom:
   Row 1: 1. Chính diện toàn thân | 2. Chính diện trung cảnh | 3. Cận mặt chính diện | 4. Góc 3/4 toàn thân | 5. Góc 3/4 trung cảnh | 6. Cận mặt 3/4
   Row 2: 7. Góc nghiêng toàn thân | 8. Cận mặt góc nghiêng | 9. Góc chụp từ sau lưng | 10. Nhìn lại qua vai | 11. Góc cao toàn thân | 12. Góc cao cận mặt
   Row 3: 13. Góc thấp toàn thân | 14. Góc thấp cận mặt | 15. Góc 90 độ từ trên xuống | 16. Top-down trung cảnh | 17. Top-down nằm ngửa | 18. Top-down ngồi bệt
   Row 4: 19. Góc rộng toàn cảnh | 20. Cận cảnh góc rộng | 21. Góc nghiêng Hà Lan | 22. Góc ngang hông | 23. Khoanh tay trước ngực | 24. Chạm tay lên cổ áo
   Row 5: 25. Cận cảnh chất liệu | 26. Bước đi tự nhiên | 27. Ngồi ghế đẩu | 28. Dựa tường ảo | 29. Ngước nhìn lên | 30. Cúi nhìn xuống
   Row 6: 31. Cận cảnh đôi mắt | 32. Ánh sáng bóng đổ | 33. Góc chụp nửa mặt | 34. Cúi người về trước | 35. Chỉnh tóc | 36. Tạo dáng nghệ thuật"""

models_to_try = [
    "gemini-3-pro-image",
    "gemini-3.1-flash-image-preview",
    "gemini-2.5-flash-image",
    "gemini-3.1-flash-lite-image",
    "gemini-3-pro-image-preview",
    "imagen-3.0-generate-002",
]

out_path = Path(r"./assets/datasets/koc/ethereal_koc_36_storyboard_v3.jpg")

for model_name in models_to_try:
    print(f"Trying model: {model_name} ...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[master_img, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        saved = False
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"SUCCESS with {model_name}! Saved to {out_path}")
                saved = True
                break
        if saved:
            sys.exit(0)
    except Exception as e:
        print(f"Failed {model_name}: {e}")

print("All generate_content models failed.")
sys.exit(1)
