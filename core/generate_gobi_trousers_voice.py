"""
VMAX KOC AI - Voiceover Generator for Gobi Boutique
Product: Quan Tay Ong Suong Tuyet Mua Hack Dang
Engine: edge-tts (vi-VN-HoaiMyNeural)
"""

import asyncio
import os
import sys
import edge_tts

SCENES = [
    {
        "id": "scene_1_hook",
        "text": "Ai bảo dưới 1 mét 6 mặc quần ống suông là bị nuốt dáng? Nhìn chiếc quần hack chân dài này đi các nàng ơi!",
        "filename": "output/audio/gobi_trousers_scene1_hook.mp3"
    },
    {
        "id": "scene_2_fabric",
        "text": "Chất tuyết mưa cao cấp cầm cực kỳ đầm tay, co giãn nhẹ và đặc biệt là giặt máy không bao giờ lo nhăn xù.",
        "filename": "output/audio/gobi_trousers_scene2_fabric.mp3"
    },
    {
        "id": "scene_3_experience",
        "text": "Đi làm hay đi học cả ngày vẫn cực kỳ thoải mái, cảm giác kéo đôi chân dài thêm ít nhất 5 phân luôn nha.",
        "filename": "output/audio/gobi_trousers_scene3_experience.mp3"
    },
    {
        "id": "scene_4_cta",
        "text": "Giá gốc gần 200 cành nhưng hôm nay shop đang trợ giá cực hời ở giỏ hàng góc trái màn hình. Chị em bấm vào săn ngay trước khi hết deal nha!",
        "filename": "output/audio/gobi_trousers_scene4_cta.mp3"
    }
]

FULL_TEXT = " ".join([s["text"] for s in SCENES])
FULL_OUTPUT = "output/audio/gobi_trousers_full_voiceover.mp3"

async def generate_all():
    os.makedirs("output/audio", exist_ok=True)
    voice = "vi-VN-HoaiMyNeural"
    
    print("[*] Dang sinh voiceover cho tung canh...")
    for s in SCENES:
        out_path = os.path.abspath(s["filename"])
        comm = edge_tts.Communicate(s["text"], voice=voice, rate="+5%", pitch="+2Hz")
        await comm.save(out_path)
        print(f"[+] Hoan thanh: {s['id']} -> {out_path}")
        
    print("[*] Dang sinh voiceover hop nhat toan bai...")
    full_path = os.path.abspath(FULL_OUTPUT)
    comm_full = edge_tts.Communicate(FULL_TEXT, voice=voice, rate="+5%", pitch="+2Hz")
    await comm_full.save(full_path)
    print(f"[+] Hoan thanh full voiceover -> {full_path}")

if __name__ == "__main__":
    asyncio.run(generate_all())
