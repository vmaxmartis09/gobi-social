import os
import sys
import shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_DIR = os.path.join(PROJECT_ROOT, "affiliate_tiktok", "sample_video", "images")
os.makedirs(DEST_DIR, exist_ok=True)

SRC_DIR = r"C:\Users\HAI\.gemini\antigravity\brain\383fa778-c3ea-408f-bf80-315f12e6d6f3"

IMAGE_MAP = {
    "cardigan_model_cafe_1792250793583.jpg": "01_hook_model_cafe.jpg",
    "cardigan_texture_closeup_1792250811052.jpg": "02_texture_fabric_buttons.jpg",
    "cardigan_fullbody_ootd_1792250827708.jpg": "03_fullbody_korean_ootd.jpg",
    "cardigan_cta_pointing_clean_1792250865400.jpg": "04_cta_pointing_cart.jpg"
}

print("="*60)
print("📦 SAO CHÉP ẢNH MẪU AI VÀO WORKSPACE...")
print("="*60)

for src_name, dst_name in IMAGE_MAP.items():
    src_path = os.path.join(SRC_DIR, src_name)
    dst_path = os.path.join(DEST_DIR, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"[+] Đã sao chép: {dst_name} ({os.path.getsize(dst_path)/1024:.1f} KB)")
    else:
        print(f"[!] Không tìm thấy nguồn: {src_path}")

print("[+] Hoàn tất thiết lập thư mục ảnh mẫu!")
