"""
VMAX KOC AI Video Prompt & Production Script Generator
Tich hop cong thuc camera Kling 3.0, thuat toan TikTok Shop Affiliate 2026,
va quy chuan Commercial Sound Library (CML).
"""

import sys
import os
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CAMERA_MOVEMENTS = {
    "push_in": "Slow cinematic push-in toward the subject, 35mm lens, shallow depth of field, subtle motion blur",
    "pull_back": "Slow steady pull-back revealing the wider ambient background, stable gimbal movement",
    "pan_right": "Camera pans smoothly to the right, maintaining parallel tracking of the subject",
    "tilt_up": "Camera tilts up slowly from waist level to eye level, smooth vertical glide",
    "static_subtle": "Locked-off tripod shot, natural subtle breathing motion, realistic eye contact and blinking"
}

def generate_kling_video_prompt(subject_action: str, camera_move: str = "push_in", lighting: str = "soft studio rim light"):
    """
    Quy tac Kling One-Move Rule:
    [Subject Action] + [Camera Move] + [Lighting & Style]
    """
    cam_str = CAMERA_MOVEMENTS.get(camera_move, CAMERA_MOVEMENTS["push_in"])
    prompt = (
        f"{subject_action}. "
        f"{cam_str}. "
        f"{lighting}, photorealistic skin texture, natural pores, 8k resolution, no warping, cinematic color grade."
    )
    return prompt

def generate_tiktok_affiliate_package(product_name: str, price_sale: str, pain_point: str, hook_type: str = "curiosity"):
    hooks = {
        "curiosity": f"Đố các bạn biết, tại sao chiếc {product_name} này lại cháy hàng suốt 2 tuần qua?",
        "warning": f"Đừng dại mua {product_name} nếu bạn chưa biết sự thật này...",
        "contrarian": f"Ai bảo {product_name} đắt tiền mới xịn? Xem hết video để thấy điều bất ngờ!",
        "problem_solver": f"Nếu bạn đang gặp tình trạng {pain_point}, thì đây chính là vị cứu tinh của bạn!"
    }
    
    hook_sentence = hooks.get(hook_type, hooks["curiosity"])
    
    package = {
        "metadata": {
            "title_seo": f"Review chân thực {product_name} - Có đáng mua không? | KOC AI",
            "hashtags": [f"#{product_name.replace(' ', '')}", "#reviewhangngay", "#kocai", "#tiktokshopaffiliate", "#sandealtiktok"],
            "sound_policy": "BẮT BUỘC dùng Commercial Sound Library (Nhạc thương mại TikTok) để không bị tắt tiếng",
            "aigc_setting": "Bật công tắc 'Nội dung do AI tạo (AI-generated content)' ON"
        },
        "video_structure": [
            {
                "timing": "0:00 - 0:03 (HOOK VÀNG)",
                "koc_panel": "Cận mặt 3/4 hoặc Cận mặt chính diện (Panel 03 / 06)",
                "kling_prompt": generate_kling_video_prompt("The young woman looks surprised, tilting her head slightly with an inquiring expression", "push_in"),
                "voiceover": hook_sentence
            },
            {
                "timing": "0:03 - 0:15 (SOI CHI TIẾT & BÓC TÁCH)",
                "koc_panel": "Góc ngang hông hoặc Cận cảnh chất liệu (Panel 22 / 25)",
                "kling_prompt": generate_kling_video_prompt("Her hands gently showcase and touch the product texture, demonstrating flexibility", "static_subtle"),
                "voiceover": f"Cầm trên tay thì điểm cộng lớn nhất là chất lượng hoàn thiện cực kỳ chắc chắn. Tuy nhiên, điểm trừ nhỏ là thời gian giao hàng hơi lâu một chút vì quá hot."
            },
            {
                "timing": "0:15 - 0:25 (TRẢI NGHIỆM THỰC TẾ)",
                "koc_panel": "Bước đi tự nhiên hoặc Xoay người (Panel 26 / 36)",
                "kling_prompt": generate_kling_video_prompt("The woman walks naturally and turns smoothly toward the camera, smiling genuinely", "pan_right"),
                "voiceover": f"Khi sử dụng thực tế thì giải quyết triệt để vấn đề {pain_point}. Đánh giá cá nhân 9/10 điểm rất đáng tiền."
            },
            {
                "timing": "0:25 - 0:30 (KÊU GỌI BẤM GIỎ HÀNG)",
                "koc_panel": "Chính diện trung cảnh, chỉ tay góc trái (Panel 02)",
                "kling_prompt": generate_kling_video_prompt("The woman smiles and points downward toward the lower left corner", "push_in"),
                "voiceover": f"Giá gốc hơn 300k nhưng shop đang trợ giá còn {price_sale} ở icon giỏ hàng góc trái màn hình. Mọi người bấm vào săn ngay trước khi hết deal nha!"
            }
        ]
    }
    return package

if __name__ == "__main__":
    pkg = generate_tiktok_affiliate_package("Áo Cardigan Dệt Kim", "189k", "mặc áo len bị dặm ngứa")
    print("======================================================================")
    print("           VMAX KOC AI COMPLETE CAMPAIGN PACKAGE                      ")
    print("======================================================================")
    print(f"[*] Title SEO: {pkg['metadata']['title_seo']}")
    print(f"[*] Chính sách âm thanh: {pkg['metadata']['sound_policy']}")
    print(f"[*] Nhãn AIGC: {pkg['metadata']['aigc_setting']}")
    print("\n--- 4 Phân cảnh sản xuất Kling 3.0 & Voiceover ---")
    for s in pkg["video_structure"]:
        print(f"\n[{s['timing']}] - Panel: {s['koc_panel']}")
        print(f"   + Prompt Kling: {s['kling_prompt']}")
        print(f"   + Lời thoại: \"{s['voiceover']}\"")
    print("======================================================================")
