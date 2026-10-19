import os
import sys
import shutil
from PIL import Image
import pillow_heif

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pillow_heif.register_heif_opener()

SRC_DIR = r"C:\Users\HAI\Downloads\Mauz"
DST_DIR = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\affiliate_tiktok\dataset_koc\raw_photos"
os.makedirs(DST_DIR, exist_ok=True)

print("="*60)
print("🖼️ ĐANG XỬ LÝ VÀ CHUYỂN ĐỔI BỘ ẢNH MẪU KOC...")
print(f"[*] Nguồn: {SRC_DIR}")
print(f"[*] Đích:  {DST_DIR}")
print("="*60)

files = sorted(os.listdir(SRC_DIR))
converted_count = 0
summary = []

for idx, fname in enumerate(files, 1):
    src_path = os.path.join(SRC_DIR, fname)
    if not os.path.isfile(src_path):
        continue

    ext = os.path.splitext(fname)[1].lower()
    dst_name = f"koc_{idx:02d}.jpg"
    dst_path = os.path.join(DST_DIR, dst_name)

    try:
        with Image.open(src_path) as im:
            # Handle orientation if present
            im = im.convert("RGB")
            w, h = im.size
            im.save(dst_path, "JPEG", quality=95)
            converted_count += 1
            summary.append({
                "id": idx,
                "orig": fname,
                "file": dst_name,
                "size": f"{w}x{h}",
                "aspect": f"{w/h:.2f}"
            })
            print(f"  [✓] {fname} ({w}x{h}) -> {dst_name}")
    except Exception as e:
        print(f"  [!] Lỗi xử lý {fname}: {e}")

print("="*60)
print(f"🎉 ĐÃ CHUYỂN ĐỔI THÀNH CÔNG {converted_count}/{len(files)} ẢNH SANG ĐỊNH DẠNG CHUẨN!")
print(f"[*] Thư mục lưu: {DST_DIR}")
print("="*60)
