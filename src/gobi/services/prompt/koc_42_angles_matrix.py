"""
GOBI SOCIAL - MASTER KOC 42-ANGLE PROMPT MATRIX
================================================
Ma trận 42 góc máy ảnh và tư thế chuẩn hóa khóa nhân dạng tuyệt đối (Character DNA)
Dựa trên hình ảnh gốc: assets/datasets/koc/MASTER_KOC_DNA.jpg
"""

import json
from pathlib import Path
from typing import List, Dict, Any

# DNA nhân vật bất biến (Immutable Character DNA)
CHARACTER_DNA = (
    "A stunning 21-year-old Vietnamese female KOC model named Gobi. "
    "Features identical to MASTER_KOC_DNA: long glossy straight jet-black hair parted neatly in the middle falling past shoulders, "
    "delicate Asian facial structure, soft natural double eyelids, warm expressive dark-brown almond eyes, slender elegant nose bridge, "
    "soft natural rosy lips, subtle youthful smile, flawless natural skin texture with visible fine pores and delicate peach fuzz (strictly no plastic smoothing, no excessive airbrushing, no cartoon filter). "
    "Outfit: luxurious ivory white silk satin cowl-neck camisole top, draped effortlessly with a cozy milk-beige oversized knit cardigan falling softly off one shoulder, "
    "paired with tailored high-waisted beige pleated straight-leg trousers, delicate minimalist fine gold chain necklace around collarbone. "
    "Lighting: soft diffused warm studio lighting, 5400K color temperature, gentle directional rim light, high-end Korean aesthetic lookbook editorial style. "
    "Photography: shot on Hasselblad H6D-100c, 8K ultra-sharp resolution, cinematic color grading, hyper-realistic depth of field, aspect ratio 9:16."
)

NEGATIVE_PROMPT = (
    "ugly, deformed eyes, cross-eyed, blurry, bad anatomy, bad hands, missing fingers, extra fingers, floating limbs, "
    "disfigured, mutated, plastic skin, 3d render, cartoon, anime, illustration, oversaturated, beauty filter, fake skin, "
    "face drift, different person, cropped head, watermark, logo, text, subtitles, low resolution, bad lighting."
)

ANGLES_42_DEFINITIONS = [
    # -------------------------------------------------------------
    # NHÓM 1: CẬN CẢNH CHÂN DUNG & BIỂU CẢM NGŨ QUAN (8 GÓC)
    # -------------------------------------------------------------
    {
        "id": "angle_01_can_mat_chinh_dien",
        "category": "portrait_closeup",
        "vn_title": "Cận mặt chính diện trực diện camera",
        "camera": "85mm f/1.4, eye-level, shallow depth of field",
        "action": "Close-up portrait facing directly forward into camera lens, soft calm eye contact, gentle subtle smile, cardigan draped loosely, sharp focus on facial features."
    },
    {
        "id": "angle_02_can_mat_goc_3_4_trai",
        "category": "portrait_closeup",
        "vn_title": "Cận mặt góc 3/4 nghiêng trái",
        "camera": "85mm f/1.4, eye-level, creamy bokeh background",
        "action": "Close-up portrait turned 45 degrees to the left, eyes gazing gently toward viewer, soft studio rim light highlighting her jawline and cheekbone."
    },
    {
        "id": "angle_03_can_mat_goc_3_4_phai",
        "category": "portrait_closeup",
        "vn_title": "Cận mặt góc 3/4 nghiêng phải",
        "camera": "85mm f/1.4, eye-level, soft warm backlight",
        "action": "Close-up portrait turned 45 degrees to the right, hair tucked softly behind right ear, subtle elegant expression, showing delicate gold necklace."
    },
    {
        "id": "angle_04_can_mat_profile_nghieng_90_trai",
        "category": "portrait_closeup",
        "vn_title": "Góc nghiêng 90 độ sườn mặt bên trái",
        "camera": "85mm f/1.8, profile angle, minimalist warm grey backdrop",
        "action": "Pure 90-degree side profile silhouette of left face, highlighting the delicate nose slope, eyelashes, soft lips and jawline contour."
    },
    {
        "id": "angle_05_can_mat_profile_nghieng_90_phai",
        "category": "portrait_closeup",
        "vn_title": "Góc nghiêng 90 độ sườn mặt bên phải",
        "camera": "85mm f/1.8, profile angle, clean editorial framing",
        "action": "Pure 90-degree side profile view of right face, cardigan draped over shoulder, calm contemplative expression."
    },
    {
        "id": "angle_06_can_mat_goc_cao_nhin_len",
        "category": "portrait_closeup",
        "vn_title": "Cận mặt góc máy cao (High-angle) nhìn lên",
        "camera": "50mm f/1.8, high-angle looking downward 30 degrees",
        "action": "Camera looking down at a 30-degree high angle, Gobi tilts head upward gazing softly toward the lens, big clear eyes, feminine and endearing look."
    },
    {
        "id": "angle_07_can_mat_goc_thap_nhin_xuong",
        "category": "portrait_closeup",
        "vn_title": "Cận mặt góc máy thấp (Low-angle) sang trọng",
        "camera": "50mm f/2.0, low-angle looking upward 25 degrees",
        "action": "Camera positioned slightly lower looking up, Gobi gazing slightly downward with confident calm poise, sculpted jawline, high-fashion aura."
    },
    {
        "id": "angle_08_can_canh_macro_anh_mat_nu_cuoi",
        "category": "portrait_closeup",
        "vn_title": "Macro cận cảnh ánh mắt và nụ cười rạng rỡ",
        "camera": "105mm macro f/2.8, tight framing",
        "action": "Tight macro portrait focusing from nose to eyes and lips, genuine sweet smile with lips slightly parted, sparkling lively eyes."
    },

    # -------------------------------------------------------------
    # NHÓM 2: BÁN THÂN & TRUNG CẢNH TƯƠNG TÁC (10 GÓC)
    # -------------------------------------------------------------
    {
        "id": "angle_09_trung_canh_chinh_dien",
        "category": "medium_shot",
        "vn_title": "Bán thân chính diện từ thắt lưng trở lên",
        "camera": "50mm f/1.8, eye-level waist-up shot",
        "action": "Medium shot from waist up facing forward, arms resting naturally in front, satin camisole and oversized knit cardigan clearly visible, confident KOC look."
    },
    {
        "id": "angle_10_trung_canh_goc_3_4_trai",
        "category": "medium_shot",
        "vn_title": "Bán thân góc 3/4 nghiêng trái",
        "camera": "50mm f/1.8, waist-up, three-quarter view",
        "action": "Medium shot turned 45 degrees left, one hand casually touching the cardigan lapel, looking at camera with friendly warmth."
    },
    {
        "id": "angle_11_trung_canh_goc_3_4_phai",
        "category": "medium_shot",
        "vn_title": "Bán thân góc 3/4 nghiêng phải",
        "camera": "50mm f/1.8, waist-up, three-quarter view",
        "action": "Medium shot turned 45 degrees right, cardigan slipping off one shoulder revealing satin strap and delicate collarbone, chic aesthetic."
    },
    {
        "id": "angle_12_trung_canh_nghieng_dau_nhe",
        "category": "medium_shot",
        "vn_title": "Bán thân nghiêng đầu đáng yêu (Head-tilt)",
        "camera": "50mm f/1.8, medium portrait",
        "action": "Medium shot with head tilted playfully to one side, sweet engaging smile as if listening intently to a friend, charming conversational pose."
    },
    {
        "id": "angle_13_trung_canh_dua_tuong_kinh",
        "category": "medium_shot",
        "vn_title": "Bán thân tựa lưng gương soi lookbook",
        "camera": "50mm f/2.0, medium framing with subtle mirror reflection",
        "action": "Medium shot leaning gently against a sleek minimalist full-length mirror, subtle double reflection in the glass adding editorial depth."
    },
    {
        "id": "angle_14_trung_canh_khoanh_tay_thanh_lich",
        "category": "medium_shot",
        "vn_title": "Bán thân khoanh tay nhẹ trước ngực",
        "camera": "50mm f/1.8, waist-up",
        "action": "Medium shot with arms loosely and elegantly crossed in front of chest, relaxed posture, poised and professional fashion creator look."
    },
    {
        "id": "angle_15_trung_canh_vuot_toc",
        "category": "medium_shot",
        "vn_title": "Bán thân tay vuốt nhẹ lọn tóc tự nhiên",
        "camera": "50mm f/1.8, dynamic candid feel",
        "action": "Medium shot with one slender hand gently brushing long black hair away from her face, natural candid motion capture."
    },
    {
        "id": "angle_16_trung_canh_chinh_ao_khoac",
        "category": "medium_shot",
        "vn_title": "Bán thân tay kéo nhẹ vạt áo len cardigan",
        "camera": "50mm f/2.0, waist-up",
        "action": "Medium shot with both hands lightly holding and adjusting the cardigan opening, showcasing the soft fluffy wool texture."
    },
    {
        "id": "angle_17_trung_canh_cam_ly_ca_phe",
        "category": "medium_shot",
        "vn_title": "Bán thân cầm ly cà phê gốm sứ phong cách sống",
        "camera": "50mm f/1.8, lifestyle editorial",
        "action": "Medium shot holding an artisanal minimalist ceramic warm-beige coffee cup with both hands, steam rising, cozy morning mood."
    },
    {
        "id": "angle_18_trung_canh_nhin_lai_qua_vai",
        "category": "medium_shot",
        "vn_title": "Bán thân xoay người nhìn lại qua vai (Over-the-shoulder)",
        "camera": "85mm f/1.8, over-the-shoulder perspective",
        "action": "Medium shot turned away from camera, glancing back gracefully over her shoulder, hair sweeping behind, alluring and cinematic."
    },

    # -------------------------------------------------------------
    # NHÓM 3: TOÀN THÂN & HACK DÁNG LOOKBOOK OUTFIT (12 GÓC)
    # -------------------------------------------------------------
    {
        "id": "angle_19_toan_than_chinh_dien_thang",
        "category": "full_body",
        "vn_title": "Toàn thân đứng thẳng chính diện chuẩn catalogue",
        "camera": "35mm f/2.8, eye-level full-length shot",
        "action": "Full-body head-to-toe shot standing straight, facing forward, arms relaxed at sides, high-waisted beige trousers falling elegantly to feet."
    },
    {
        "id": "angle_20_toan_than_goc_3_4_buoc_di",
        "category": "full_body",
        "vn_title": "Toàn thân góc 3/4 sải bước tự nhiên",
        "camera": "35mm f/2.8, dynamic motion capture",
        "action": "Full-body shot turned 45 degrees, walking forward naturally in mid-stride, cardigan floating gently with motion, effortless street style."
    },
    {
        "id": "angle_21_toan_than_goc_thap_hack_chan",
        "category": "full_body",
        "vn_title": "Toàn thân góc thấp (Low-angle) kéo dài chân hack dáng",
        "camera": "28mm f/4.0, low knee-height angle shooting upward",
        "action": "Low-angle upward shot from knee height, accentuating the long elegant leg silhouette of the high-waisted trousers, 1m62 looking statuesque."
    },
    {
        "id": "angle_22_toan_than_goc_cao_downward",
        "category": "full_body",
        "vn_title": "Toàn thân góc cao nhìn xuống bao quát bối cảnh",
        "camera": "35mm f/2.8, elevated 45-degree downward angle",
        "action": "High-angle shot looking down at full body, Gobi standing gracefully on warm polished wooden floor with soft ambient studio shadows."
    },
    {
        "id": "angle_23_toan_than_nghieng_dang_chu_S",
        "category": "full_body",
        "vn_title": "Toàn thân đứng tạo dáng chữ S mềm mại",
        "camera": "50mm f/2.8, full-length portrait",
        "action": "Full-body pose with one hip slightly cocked creating a gentle feminine S-curve line, one foot pointed forward, highlighting waistline."
    },
    {
        "id": "angle_24_toan_than_bo_tay_tui_quan",
        "category": "full_body",
        "vn_title": "Toàn thân hai tay đút túi quần tây thanh lịch",
        "camera": "35mm f/2.8, full body fashion catalog",
        "action": "Full-body shot with hands tucked casually inside the front pockets of beige trousers, shoulders relaxed, effortlessly chic Parisian-Korean vibe."
    },
    {
        "id": "angle_25_toan_than_xoay_nguoi_khoe_lung",
        "category": "full_body",
        "vn_title": "Toàn thân xoay lưng khoe phom dáng phía sau",
        "camera": "50mm f/2.8, full rear view",
        "action": "Full-body rear view showcasing the clean fit of the trousers from behind and the drape of the cardigan, head turned slightly profile."
    },
    {
        "id": "angle_26_toan_than_goc_rong_wide_room",
        "category": "full_body",
        "vn_title": "Toàn cảnh góc rộng không gian studio tối giản",
        "camera": "24mm f/4.0, ultra-wide architectural framing",
        "action": "Wide cinematic environmental shot, Gobi standing in a spacious minimalist Korean interior with soft sheer curtains and architectural arch."
    },
    {
        "id": "angle_27_toan_than_chieu_ngang_side_walk",
        "category": "full_body",
        "vn_title": "Toàn thân góc ngang sườn bước ngang qua khung hình",
        "camera": "50mm f/2.8, lateral side profile",
        "action": "Full side profile walking shot across the frame, showcasing the straight silhouette of the trousers and fluid drape of the cardigan."
    },
    {
        "id": "angle_28_toan_than_dung_canh_guong_lon",
        "category": "full_body",
        "vn_title": "Toàn thân soi gương đứng nhìn bóng phản chiếu",
        "camera": "35mm f/2.8, dual reflection lookbook",
        "action": "Full-body shot standing beside a large floor mirror, looking into the mirror with her back three-quarters to the real camera, dual visual story."
    },
    {
        "id": "angle_29_toan_than_hai_chan_cheo_nhe",
        "category": "full_body",
        "vn_title": "Toàn thân đứng bắt chéo chân nhẹ nhàng",
        "camera": "50mm f/2.8, full body",
        "action": "Full-body pose with ankles delicately crossed, hands clasping loosely in front, soft innocent Korean lookbook stance."
    },
    {
        "id": "angle_30_toan_than_xoay_nhe_vat_ao",
        "category": "full_body",
        "vn_title": "Toàn thân chuyển động xoay nhẹ tạo độ bay",
        "camera": "35mm f/2.8, 1/500s fast shutter freeze motion",
        "action": "Full-body in slight mid-twirl motion, cardigan hem flaring out subtly, capturing dynamic vitality and movement."
    },

    # -------------------------------------------------------------
    # NHÓM 4: TẠO DÁNG NGỒI & TƯƠNG TÁC NGHỆ THUẬT (6 GÓC)
    # -------------------------------------------------------------
    {
        "id": "angle_31_ngoi_ghe_bar_cao_vat_chan",
        "category": "sitting_pose",
        "vn_title": "Ngồi trên ghế bar cao thả dài chân",
        "camera": "50mm f/2.0, full sitting shot",
        "action": "Sitting gracefully atop a high minimalist oak barstool, one leg extended downward touching floor, the other resting on rung, sleek leg line."
    },
    {
        "id": "angle_32_ngoi_ghe_sofa_don_thu_thai",
        "category": "sitting_pose",
        "vn_title": "Ngồi thư thái trên ghế sofa bành nỉ ấm áp",
        "camera": "50mm f/1.8, cozy interior shot",
        "action": "Relaxing in a low cream bouclé armchair, legs tucked casually to the side, leaning on one armrest, warm inviting smile."
    },
    {
        "id": "angle_33_ngoi_bet_san_go_aesthetic",
        "category": "sitting_pose",
        "vn_title": "Ngồi bệt trên sàn gỗ phong cách Hàn Quốc",
        "camera": "35mm f/2.0, low angle from floor level",
        "action": "Sitting casually on polished light wood floor with legs curled softly, leaning back on one hand, natural bohemian Korean indoor vibe."
    },
    {
        "id": "angle_34_ngoi_chong_cam_suy_tu",
        "category": "sitting_pose",
        "vn_title": "Ngồi chống cằm ngắm nhìn xa xăm suy tư",
        "camera": "85mm f/1.8, medium close-up sitting",
        "action": "Resting elbow on table with chin supported softly by fingers, gazing out window with gentle thoughtful expression, poetic lighting."
    },
    {
        "id": "angle_35_ngoi_nghieng_dua_ban_go",
        "category": "sitting_pose",
        "vn_title": "Ngồi nghiêng tựa nhẹ vào bàn gỗ mộc",
        "camera": "50mm f/1.8, waist-up sitting",
        "action": "Seated sideways at an organic wooden dining table, one arm resting across the surface, warm direct gaze into camera."
    },
    {
        "id": "angle_36_ngoi_vat_ao_qua_vai",
        "category": "sitting_pose",
        "vn_title": "Ngồi vắt áo len hờ hững qua vai",
        "camera": "50mm f/2.0, medium editorial",
        "action": "Sitting upright on a minimalist wooden bench, cardigan casually slung over one shoulder like a cape, striking modern high-fashion pose."
    },

    # -------------------------------------------------------------
    # NHÓM 5: SOI CHI TIẾT VẢI, PHỤ KIỆN & GÓC NGHỆ THUẬT (6 GÓC)
    # -------------------------------------------------------------
    {
        "id": "angle_37_macro_soi_soi_len_det_kim",
        "category": "macro_details",
        "vn_title": "Cực cận (Macro) thớ vải len dệt kim và tay KOC",
        "camera": "100mm macro f/2.8, extreme close-up",
        "action": "Extreme macro close-up of Gobi's delicate fingers gently feeling the soft fluffy knit texture of the milk-beige cardigan, rich tactile feel."
    },
    {
        "id": "angle_38_macro_cap_quan_ton_eo",
        "category": "macro_details",
        "vn_title": "Cận cảnh cạp quần siết phẳng bụng tôn eo",
        "camera": "85mm f/2.8, waist close-up",
        "action": "Close-up shot focusing on the waistline: tailored high-waisted trousers with precise pleats and fine belt loops, tucked-in silk camisole."
    },
    {
        "id": "angle_39_macro_vong_co_va_xuong_quai_xanh",
        "category": "macro_details",
        "vn_title": "Cận cảnh xương quai xanh và dây chuyền vàng",
        "camera": "105mm macro f/2.0, collarbone close-up",
        "action": "Close-up of the delicate collarbone, dainty gold chain necklace, and the fluid draped cowl-neckline of the ivory silk satin camisole."
    },
    {
        "id": "angle_40_editorial_anh_sang_nua_mat_chiaroscuro",
        "category": "artistic_editorial",
        "vn_title": "Nghệ thuật vệt sáng nửa mặt điện ảnh",
        "camera": "85mm f/1.4, dramatic chiaroscuro lighting",
        "action": "Moody editorial portrait where one side of her face is bathed in golden warm sunbeam while the other rests in soft velvet shadow."
    },
    {
        "id": "angle_41_editorial_bong_nang_qua_rem",
        "category": "artistic_editorial",
        "vn_title": "Bóng nắng râm qua rèm cửa sổ (Sunlight Shadows)",
        "camera": "50mm f/1.8, artistic shadows",
        "action": "Soft geometric shadows from venetian blinds cast across her face and cardigan, creating an evocative high-fashion summer-winter mood."
    },
    {
        "id": "angle_42_editorial_chup_qua_lop_kinh_trong",
        "category": "artistic_editorial",
        "vn_title": "Chụp xuyên qua lớp kính trong suốt mờ ảo",
        "camera": "85mm f/1.4, shoot-through glass with subtle flares",
        "action": "Shooting through a transparent glass pane with subtle soft reflections and gentle lens flare, creating a dreamy poetic visual finish."
    }
]


def build_full_prompt(angle_dict: Dict[str, Any]) -> str:
    """Xây dựng prompt hoàn chỉnh cho một góc cụ thể."""
    prompt = (
        f"{CHARACTER_DNA} "
        f"Specific Shot: {angle_dict['action']} "
        f"Camera parameters: {angle_dict['camera']}."
    )
    return prompt


def export_42_prompts_json(output_path: Path):
    """Xuất toàn bộ 42 prompt chuẩn ra tệp JSON."""
    prompts_data = []
    for item in ANGLES_42_DEFINITIONS:
        full_p = build_full_prompt(item)
        prompts_data.append({
            "angle_number": len(prompts_data) + 1,
            "id": item["id"],
            "vn_title": item["vn_title"],
            "category": item["category"],
            "camera": item["camera"],
            "action": item["action"],
            "prompt": full_p,
            "negative_prompt": NEGATIVE_PROMPT
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Đã xuất ma trận 42 prompt chuẩn hóa: {output_path}")


if __name__ == "__main__":
    out_file = Path("assets/datasets/koc/koc_42_master_prompts.json")
    export_42_prompts_json(out_file)
