"""
Crop the 36 poses from the master storyboard v4 into individual reference images.
Grid is 6 columns x 6 rows = 36 cells.
"""

import os
from pathlib import Path
from PIL import Image

SRC_PATH = Path("/Volumes/Data/gobi-social/assets/datasets/koc/archive_old/master_koc_36_storyboard_v4_new.jpg")
OUT_DIR = Path("/Volumes/Data/gobi-social/assets/datasets/koc/old_reference_poses")
OUT_DIR.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC_PATH)
width, height = im.size

COLS = 6
ROWS = 6

cell_w = width / COLS
cell_h = height / ROWS

POSE_NAMES = [
    "01_chinh_dien_toan_than",
    "02_chinh_dien_trung_canh",
    "03_can_mat_chinh_dien",
    "04_goc_3_4_toan_than",
    "05_goc_3_4_trung_canh",
    "06_can_mat_3_4",
    "07_goc_nghieng_toan_than",
    "08_can_mat_goc_nghieng",
    "09_goc_chup_sau_lung",
    "10_nhin_lai_qua_vai",
    "11_goc_cao_toan_than",
    "12_goc_cao_can_mat",
    "13_goc_thap_toan_than",
    "14_goc_thap_can_mat",
    "15_goc_90_do_tren_xuong",
    "16_top_down_trung_canh",
    "17_top_down_nam_ngua",
    "18_top_down_ngoi_bet",
    "19_goc_rong_toan_canh",
    "20_can_canh_goc_rong",
    "21_goc_nghieng_ha_lan",
    "22_goc_ngang_hong",
    "23_khoanh_tay_truoc_nguc",
    "24_cham_tay_len_co_ao",
    "25_can_canh_chat_lieu",
    "26_buoc_di_tu_nhien",
    "27_ngoi_ghe_dau",
    "28_dua_tuong_ao",
    "29_nguoc_nhin_len",
    "30_cui_nhin_xuong",
    "31_can_canh_doi_mat",
    "32_anh_sang_bong_do",
    "33_goc_chup_nua_mat",
    "34_cui_nguoi_ve_truoc",
    "35_chinh_toc",
    "36_tao_dang_nghe_thuat"
]

for idx, name in enumerate(POSE_NAMES):
    r = idx // COLS
    c = idx % COLS
    
    left = int(c * cell_w)
    top = int(r * cell_h)
    right = int((c + 1) * cell_w) if c < COLS - 1 else width
    bottom = int((r + 1) * cell_h) if r < ROWS - 1 else height
    
    cell_img = im.crop((left, top, right, bottom))
    out_file = OUT_DIR / f"{name}.jpg"
    cell_img.save(out_file, quality=95)
    print(f"Saved: {out_file.name} ({cell_img.size})")

print(f"\nSuccessfully cropped {len(POSE_NAMES)} reference poses into {OUT_DIR}")
