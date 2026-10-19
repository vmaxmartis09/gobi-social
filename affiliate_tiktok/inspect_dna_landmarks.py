import numpy as np
from PIL import Image, ImageDraw

g2_path = r"./affiliate_tiktok\dataset_koc\cinematic_koc_36_storyboard_v2.jpg"
g2 = Image.open(g2_path).convert("RGB")

# Upscale g2 by 2x to 2048x2048 so we can read local cell coordinates (0..512 in each 512x512 cell)
canvas = Image.new("RGB", (6 * 256, 6 * 256))
w, h = g2.size
cw, ch = w / 6.0, h / 6.0

for r in range(6):
    for c in range(6):
        x1 = int(round(c * cw)) + 5
        y1 = int(round(r * ch)) + 5
        x2 = int(round((c + 1) * cw)) - 5
        y2 = int(round((r + 1) * ch)) - 21
        cell = g2.crop((x1, y1, x2, y2)).resize((256, 256), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(cell)
        for gx in range(32, 256, 32):
            draw.line([(gx, 0), (gx, 256)], fill=(255, 0, 0), width=1)
        for gy in range(32, 256, 32):
            draw.line([(0, gy), (256, gy)], fill=(0, 255, 0), width=1)
        idx = r * 6 + c + 1
        draw.text((4, 4), f"G2[{idx}]", fill=(255, 255, 0))
        canvas.paste(cell, (c * 256, r * 256))

canvas.save(r"./affiliate_tiktok\dataset_koc\debug_g2_grid.jpg", quality=90)
print("Saved debug_g2_grid.jpg")
