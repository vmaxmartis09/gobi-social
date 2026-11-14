import os
import sys
import re
import json
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROMPTS_FILE = os.path.join(PROJECT_ROOT, "configs", "prompts", "koc_matrix_36_angles.json")
OUTPUT_PANELS_DIR = os.path.join(PROJECT_ROOT, "assets", "samples", "sample_video", "koc_matrix_panels")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
    text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
    text = re.sub(r'[ìíịỉĩ]', 'i', text)
    text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
    text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
    text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
    text = re.sub(r'[đ]', 'd', text)
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text

def crop_36_grid(grid_image_path, out_dir=None):
    if out_dir is None:
        out_dir = OUTPUT_PANELS_DIR
    os.makedirs(out_dir, exist_ok=True)

    print("="*65)
    print("✂️ VMAX AUTOMATED SLICER: CẮT BẢNG MA TRẬN 36 GÓC KOC AI...")
    print(f"[*] File ảnh gốc: {grid_image_path}")
    print(f"[*] Thư mục đích: {out_dir}")
    print("="*65)

    if not os.path.exists(grid_image_path):
        print(f"[!] Lỗi: Không tìm thấy file {grid_image_path}")
        return False

    # Load danh mục 36 góc từ JSON prompt
    panels_meta = {}
    if os.path.exists(PROMPTS_FILE):
        try:
            with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                panels_meta = data.get("image_generation_prompt", {}).get("panels_sequence", {})
        except Exception as e:
            print("[!] Không đọc được metadata prompt:", e)

    with Image.open(grid_image_path) as im:
        im = im.convert("RGB")
        w, h = im.size
        print(f"[+] Kích thước ảnh gốc: {w} x {h} px")

        rows, cols = 6, 6
        cell_w = w / cols
        cell_h = h / rows
        print(f"[+] Kích thước mỗi ô (Panel): {cell_w:.1f} x {cell_h:.1f} px\n")

        manifest = []

        for r in range(rows):
            for c in range(cols):
                panel_num = r * cols + c + 1
                key = f"panel_{panel_num}"
                info = panels_meta.get(key, {})
                vn_title = info.get("text", f"Góc {panel_num}")
                action = info.get("action", "")
                slug = slugify(vn_title)

                left = int(c * cell_w)
                top = int(r * cell_h)
                right = int((c + 1) * cell_w) if c < cols - 1 else w
                bottom = int((r + 1) * cell_h) if r < rows - 1 else h

                panel_img = im.crop((left, top, right, bottom))
                
                filename = f"panel_{panel_num:02d}_{slug}.jpg"
                save_path = os.path.join(out_dir, filename)
                panel_img.save(save_path, quality=95)

                manifest.append({
                    "panel_number": panel_num,
                    "row": r + 1,
                    "col": c + 1,
                    "vn_title": vn_title,
                    "action_description": action,
                    "file_name": filename,
                    "file_path": save_path
                })
                print(f"  [✓] Panel {panel_num:02d}: {vn_title} -> {filename}")

        manifest_path = os.path.join(out_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print("\n" + "="*65)
        print(f"🎉 ĐÃ CẮT THÀNH CÔNG 36/36 PHÂN CẢNH KOC AI!")
        print(f"[*] Thư mục lưu: {out_dir}")
        print(f"[*] File danh mục: {manifest_path}")
        print("="*65)
        return manifest

if __name__ == "__main__":
    if len(sys.argv) > 2:
        crop_36_grid(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        crop_36_grid(sys.argv[1])
    else:
        # Tự tìm ảnh ma trận trong artifact hoặc sample_video
        candidate_dirs = [
            os.path.join(PROJECT_ROOT, "assets", "character_dna"), PROJECT_ROOT,
            os.path.join(PROJECT_ROOT, "assets", "samples", "sample_video")
        ]
        found = None
        for d in candidate_dirs:
            if os.path.exists(d):
                for f in os.listdir(d):
                    if ("36" in f or "matrix" in f or "grid" in f or "storyboard" in f) and f.lower().endswith((".jpg", ".png")):
                        found = os.path.join(d, f)
                        break
            if found:
                break
        
        if found:
            crop_36_grid(found)
        else:
            print("Usage: python crop_panels.py <path_to_6x6_grid_image.jpg>")
