import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TARGET_W = 1080
TARGET_H = 1920

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DNA_PATH = os.path.join(PROJECT_ROOT, "affiliate_tiktok", "dataset_koc", "MASTER_KOC_DNA.jpg")
PANEL_DIR = os.path.join(PROJECT_ROOT, "affiliate_tiktok", "dataset_koc", "ethereal_koc_panels_v3")
SHOTS_DIR = os.path.join(PROJECT_ROOT, "shots")

# Fonts
try:
    font_title = ImageFont.truetype("arialbd.ttf", 32)
    font_badge = ImageFont.truetype("arialbd.ttf", 26)
    font_main = ImageFont.truetype("arialbd.ttf", 44)
    font_cta = ImageFont.truetype("arialbd.ttf", 34)
except Exception:
    font_title = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_main = ImageFont.load_default()
    font_cta = ImageFont.load_default()

def create_ambient_frame(fg_img, badge_text, badge_color, sub_text, cta_active=False, zoom=1.03):
    frame = Image.new("RGB", (TARGET_W, TARGET_H), (15, 15, 20))
    
    # 1. Background Ambient Fill
    bg = fg_img.resize((TARGET_W, TARGET_H), Image.Resampling.BILINEAR)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=32))
    # Dim background slightly
    dimmer = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 90))
    bg.paste(dimmer, (0, 0), dimmer)
    frame.paste(bg, (0, 0))
    
    # 2. Foreground Card
    # Dimensions: 960x1200 rounded card
    card_w = 960
    card_h = 1200
    card_x = (TARGET_W - card_w) // 2
    card_y = 220
    
    # Zoom crop
    fw, fh = fg_img.size
    crop_w = int(fw / zoom)
    crop_h = int((fw / zoom) * (card_h / card_w))
    if crop_h > fh:
        crop_h = fh
        crop_w = int(fh * (card_w / card_h))
    
    cx, cy = fw // 2, fh // 2
    crop_box = (cx - crop_w // 2, cy - crop_h // 2, cx + crop_w // 2, cy + crop_h // 2)
    cropped_fg = fg_img.crop(crop_box).resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    # Rounded corners mask
    mask = Image.new("L", (card_w, card_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), (card_w, card_h)], radius=36, fill=255)
    
    # Shadow behind card
    shadow = Image.new("RGBA", (card_w + 40, card_h + 40), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.rounded_rectangle([(15, 15), (card_w + 25, card_h + 25)], radius=36, fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    frame.paste(shadow, (card_x - 20, card_y - 20), shadow)
    
    # Paste card
    frame.paste(cropped_fg, (card_x, card_y), mask)
    
    # Card subtle border
    overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=36, outline=(255, 255, 255, 70), width=2)
    
    # 3. Header KOC Channel Pill
    chan_text = "🌷 Mây Mây Review | 1m58 - 46kg 👗"
    tb = draw.textbbox((0, 0), chan_text, font=font_title)
    tb_w = tb[2] - tb[0]
    pill_w = tb_w + 48
    pill_h = 56
    pill_x = (TARGET_W - pill_w) // 2
    pill_y = 70
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=28, fill=(15, 15, 25, 200), outline=(255, 255, 255, 90), width=1)
    draw.text((pill_x + 24, pill_y + 10), chan_text, font=font_title, fill=(255, 255, 255, 240))
    
    # 4. Badge Pill (on the card)
    bb = draw.textbbox((0, 0), badge_text, font=font_badge)
    bb_w = bb[2] - bb[0]
    b_pill_w = bb_w + 36
    b_pill_h = 44
    b_pill_x = card_x + 36
    b_pill_y = card_y + 36
    draw.rounded_rectangle([(b_pill_x, b_pill_y), (b_pill_x + b_pill_w, b_pill_y + b_pill_h)], radius=22, fill=(badge_color[0], badge_color[1], badge_color[2], 230))
    draw.text((b_pill_x + 18, b_pill_y + 8), badge_text, font=font_badge, fill=(255, 255, 255, 255))
    
    # 5. Subtitle Card (TikTok Safe Zone: y = 1480)
    sub_y = 1480
    sb = draw.textbbox((0, 0), sub_text, font=font_main)
    sb_w = sb[2] - sb[0]
    sub_card_w = max(sb_w + 64, 600)
    sub_card_h = 100
    sub_card_x = (TARGET_W - sub_card_w) // 2
    
    draw.rounded_rectangle([(sub_card_x, sub_y), (sub_card_x + sub_card_w, sub_y + sub_card_h)], radius=26, fill=(10, 10, 18, 220), outline=(255, 255, 255, 60), width=2)
    # Shadow text
    draw.text((sub_card_x + (sub_card_w - sb_w) // 2 + 2, sub_y + 24 + 2), sub_text, font=font_main, fill=(0, 0, 0, 220))
    # Glowing yellow text
    draw.text((sub_card_x + (sub_card_w - sb_w) // 2, sub_y + 24), sub_text, font=font_main, fill=(255, 235, 80, 255))
    
    # 6. CTA Cart Callout (if active)
    if cta_active:
        cta_x = 70
        cta_y = 1640
        cta_text = "👇 SĂN DEAL GIỎ HÀNG GÓC TRÁI"
        cb = draw.textbbox((0, 0), cta_text, font=font_cta)
        cb_w = cb[2] - cb[0]
        draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cb_w + 48, cta_y + 72)], radius=36, fill=(255, 71, 87, 240), outline=(255, 255, 255, 230), width=2)
        draw.text((cta_x + 24, cta_y + 16), cta_text, font=font_cta, fill=(255, 255, 255, 255))
    
    frame.paste(overlay, (0, 0), overlay)
    return frame

if __name__ == "__main__":
    p3 = Image.open(os.path.join(PANEL_DIR, "panel_03_can_mat_chinh_dien.jpg")).convert("RGB")
    f1 = create_ambient_frame(p3, "🚨 DỪNG LẠI 3 GIÂY", (255, 71, 87), "MẤY BÀ ƠI, DỪNG LẠI BA GIÂY!")
    f1.save(os.path.join(SHOTS_DIR, "preview_shot_1.jpg"), quality=95)
    
    p25 = Image.open(os.path.join(PANEL_DIR, "panel_25_can_canh_chat_lieu.jpg")).convert("RGB")
    f4 = create_ambient_frame(p25, "🔍 THẨM ĐỊNH VẢI", (46, 213, 115), "CẬN CẢNH LEN DỆT KIM SIÊU MỀM MỊN")
    f4.save(os.path.join(SHOTS_DIR, "preview_shot_4.jpg"), quality=95)
    
    p2 = Image.open(os.path.join(PANEL_DIR, "panel_02_chinh_dien_trung_canh.jpg")).convert("RGB")
    f10 = create_ambient_frame(p2, "⚡ SĂN DEAL GIÁ HỜI", (255, 71, 87), "GIÁ SALE DƯỚI 100 CÀNH Ở GIỎ HÀNG!", cta_active=True)
    f10.save(os.path.join(SHOTS_DIR, "preview_shot_10.jpg"), quality=95)
    
    print("[OK] Preview frames generated!")
