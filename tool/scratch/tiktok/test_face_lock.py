import numpy as np
from PIL import Image, ImageFilter

dna_path = r"./assets/datasets/koc/MASTER_KOC_DNA.jpg"
g2_path = r"./assets/datasets/koc/cinematic_koc_36_storyboard_v2.jpg"

dna = Image.open(dna_path).convert("RGB")
g2 = Image.open(g2_path).convert("RGB")

# Build hair-free inner feature mask on MASTER_KOC_DNA.jpg (768x1376)
# Brows: y=225..245, Eyes: y=255..280 (left eye x=348..405, right eye x=462..502)
# Nose: x=415..468, y=265..355
# Mouth: x=402..474, y=372..415
def build_dna_clean_feature_mask(size):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx = 430.0
    cy = 320.0
    # Asymmetric right boundary so it stays strictly left of the hair strand at x >= 504
    rx_left = 96.0
    # Taper right radius from 74 at eye level (x=504) down to 56 at mouth level (x=486)
    rx_right = 74.0 - 0.14 * np.clip(yy - 265.0, 0.0, 160.0)
    ry_top = 102.0  # reaches y = 218 (cleanly above eyebrows at y=228)
    ry_bot = 115.0  # reaches y = 435 (cleanly below lips at y=412)

    dx = np.where(xx < cx, (cx - xx) / rx_left, (xx - cx) / np.maximum(rx_right, 1.0))
    dy = np.where(yy < cy, (cy - yy) / ry_top, (yy - cy) / ry_bot)
    dist = np.sqrt(dx * dx + dy * dy)

    # Flat top 1.0 out to dist=0.76, smooth cosine feather 0.76..1.0
    m = np.clip((1.0 - dist) / 0.24, 0.0, 1.0)
    m = 0.5 - 0.5 * np.cos(m * np.pi)
    return Image.fromarray((m * 255).astype(np.uint8))

DNA_CLEAN_MASK = build_dna_clean_feature_mask(dna.size)

def sculpt_and_lock_dna(img_512, eye_mid, mouth_pt, nose_pt=None, jaw_slim=0.16, nose_slim=0.22, lock_features=True, eye_dist_dst=82.0):
    arr = np.asarray(img_512, dtype=np.float32)
    h, w, _ = arr.shape
    em = np.array(eye_mid, dtype=np.float32)
    mo = np.array(mouth_pt, dtype=np.float32)
    no = 0.38 * em + 0.62 * mo if nose_pt is None else np.array(nose_pt, dtype=np.float32)

    face_h = np.linalg.norm(mo - em)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # 1. Smooth V-line cheek/jaw slimming + petite nose slimming
    jaw_cx, jaw_cy = mo[0], 0.25 * em[1] + 0.75 * mo[1]
    dx_j = (xx - jaw_cx) / max(face_h * 1.15, 1.0)
    dy_j = (yy - jaw_cy) / max(face_h * 1.25, 1.0)
    pull_jaw = np.exp(-(dx_j * dx_j + dy_j * dy_j) * 1.45) * np.clip((dy_j + 0.35) / 0.45, 0.0, 1.0) * jaw_slim

    nose_cx, nose_cy = no[0], 0.45 * em[1] + 0.55 * no[1]
    dx_n = (xx - nose_cx) / max(face_h * 0.28, 1.0)
    dy_n = (yy - nose_cy) / max(face_h * 0.42, 1.0)
    pull_nose = np.exp(-(dx_n * dx_n + dy_n * dy_n) * 1.8) * nose_slim

    src_x = np.clip(xx + (xx - jaw_cx) * pull_jaw + (xx - nose_cx) * pull_nose, 0, w - 1.001)
    chin_cy = mo[1] + 0.42 * face_h
    dy_c = (yy - chin_cy) / max(face_h * 0.5, 1.0)
    src_y = np.clip(yy + np.exp(-(dx_j * dx_j + dy_c * dy_c) * 2.0) * (face_h * 0.025), 0, h - 1.001)

    x0, y0 = np.floor(src_x).astype(np.int32), np.floor(src_y).astype(np.int32)
    wx, wy = (src_x - x0)[:, :, None], (src_y - y0)[:, :, None]
    warped = (arr[y0, x0] * (1 - wx) + arr[y0, x0 + 1] * wx) * (1 - wy) + (arr[y0 + 1, x0] * (1 - wx) + arr[y0 + 1, x0 + 1] * wx) * wy

    # Nose bridge studio highlight
    dx_hl = (xx - nose_cx) / max(face_h * 0.055, 1.0)
    dy_hl = (yy - (0.48 * em[1] + 0.52 * no[1])) / max(face_h * 0.30, 1.0)
    hl = np.exp(-(dx_hl * dx_hl * 1.5 + dy_hl * dy_hl * 1.8))[:, :, None]
    warped = warped + hl * np.array([10.0, 8.5, 7.0], dtype=np.float32)

    if lock_features:
        # Orthogonal similarity warp from MASTER_KOC_DNA (src_cx=431, src_cy=267, eye_dist=110, eye_to_mouth=125)
        sx = 110.0 / max(eye_dist_dst, 1.0)
        sy = 125.0 / max(mo[1] - em[1], 1.0)
        aff = (sx, 0.0, 431.0 - sx * float(em[0]), 0.0, sy, 267.0 - sy * float(em[1]))
        w_dna = np.asarray(dna.transform((512, 512), Image.Transform.AFFINE, data=aff, resample=Image.Resampling.BICUBIC), dtype=np.float32)
        w_mask = np.asarray(DNA_CLEAN_MASK.transform((512, 512), Image.Transform.AFFINE, data=aff, resample=Image.Resampling.BICUBIC), dtype=np.float32) / 255.0

        # Match skin tone strictly on the feather zone (0.2 < w_mask < 0.85)
        ring = (w_mask > 0.20) & (w_mask < 0.85)
        if np.any(ring):
            for c in range(3):
                t_m, s_m = np.mean(warped[:, :, c][ring]), np.mean(w_dna[:, :, c][ring])
                t_s, s_s = np.std(warped[:, :, c][ring]) + 1e-5, np.std(w_dna[:, :, c][ring]) + 1e-5
                w_dna[:, :, c] = (w_dna[:, :, c] - s_m) * (0.82 * t_s / s_s + 0.18) + (0.85 * t_m + 0.15 * s_m)

        m3 = (w_mask * 0.92)[:, :, None]
        warped = warped * (1.0 - m3) + np.clip(w_dna, 0, 255) * m3

    res = Image.fromarray(np.clip(warped, 0, 255).astype(np.uint8))
    return res.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2))

def extract_cell_512(grid_img, r, c, top=7, bot=21, left=7, right=7):
    w, h = grid_img.size
    cw, ch = w / 6.0, h / 6.0
    box = (int(round(c * cw)) + left, int(round(r * ch)) + top, int(round((c + 1) * cw)) - right, int(round((r + 1) * ch)) - bot)
    return grid_img.crop(box).resize((512, 512), Image.Resampling.LANCZOS)

c3 = extract_cell_512(g2, 0, 2)
out3 = sculpt_and_lock_dna(c3, (257.0, 182.0), (258.0, 276.0), (258.0, 236.0), lock_features=True, eye_dist_dst=82.0)

comp = Image.new("RGB", (1024, 512))
comp.paste(dna.crop((140, 60, 660, 580)).resize((512, 512), Image.Resampling.LANCZOS), (0, 0))
comp.paste(out3, (512, 0))
comp.save(r"./assets/datasets/koc/debug_sculpt_plus_dna.jpg", quality=95)
print("Saved debug_sculpt_plus_dna.jpg")
