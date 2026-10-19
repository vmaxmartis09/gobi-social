import json
import os
import subprocess
import re
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

scenes = [
    {
        "id": "scene1",
        "image": "assets/images/scene1_hook.jpg",
        "text": "Đừng vội mua tai nghe nếu bạn chưa xem hết video này! Đây là chiếc tai nghe chống ồn đang cực hot 2026.",
        "hook_title": "DỪNG LẠI 3 GIÂY!",
        "subtitle_1": "Đừng vội mua tai nghe nếu chưa xem hết video!",
        "subtitle_2": "Chiếc tai nghe chống ồn đang cực hot 2026",
        "badge": "🔥 TOP TRENDING 2026"
    },
    {
        "id": "scene2",
        "image": "assets/images/scene2_problem.jpg",
        "text": "Bạn mệt mỏi vì tiếng ồn xung quanh khi làm việc hay đi lại? Đeo tai nghe cũ chỉ một tiếng là đau nhức tai.",
        "hook_title": "BẠN CÓ ĐANG BỊ?",
        "subtitle_1": "Mệt mỏi vì tiếng ồn văn phòng và ngoài đường?",
        "subtitle_2": "Đeo tai nghe cũ bị đau nhức tai?",
        "badge": "⚠️ NỖI ĐAU PHỔ BIẾN"
    },
    {
        "id": "scene3",
        "image": "assets/images/scene3_solution.jpg",
        "text": "Nhưng với công nghệ chống ồn chủ động ANC 45dB và đệm khí siêu êm, bạn sẽ bước vào không gian tĩnh lặng tuyệt đối.",
        "hook_title": "CÔNG NGHỆ ĐỘT PHÁ",
        "subtitle_1": "Chống ồn chủ động ANC 45dB đỉnh cao",
        "subtitle_2": "Đệm khí công thái học êm ái suốt ngày dài",
        "badge": "✨ CÔNG NGHỆ MỚI"
    },
    {
        "id": "scene4",
        "image": "assets/images/scene4_proof.jpg",
        "text": "Chất âm vòm 360 độ cực sống động, pin trâu liên tục 40 giờ. Test thực tế đàm thoại lọc gió cực kỳ rõ nét!",
        "hook_title": "TEST THỰC TẾ 10/10",
        "subtitle_1": "Âm thanh vòm 360 độ - Bass căng đét",
        "subtitle_2": "Pin 40 giờ liên tục - Đàm thoại lọc gió",
        "badge": "⭐ ĐÁNH GIÁ 5 SAO"
    },
    {
        "id": "scene5",
        "image": "assets/images/scene5_cta.jpg",
        "text": "Đang có ưu đãi giảm 40% và miễn phí giao hàng độc quyền ngay giỏ hàng góc trái. Bấm đặt ngay kẻo hết nhé!",
        "hook_title": "ƯU ĐÃI KHỦNG HÔM NAY",
        "subtitle_1": "Ưu đãi độc quyền: Giảm ngay 40%",
        "subtitle_2": "Miễn phí ship toàn quốc - Bấm giỏ hàng ngay!",
        "badge": "🎁 SỐ LƯỢNG CÓ HẠN"
    }
]

os.makedirs('assets/audio', exist_ok=True)
os.makedirs('assets/texts', exist_ok=True)

voice = "vi-VN-HoaiMyNeural"

for s in scenes:
    txt_file = f"assets/texts/{s['id']}.txt"
    audio_file = f"assets/audio/{s['id']}.mp3"
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(s['text'])
        
    cmd_tts = ["edge-tts", "--file", txt_file, "--voice", voice, "--write-media", audio_file]
    subprocess.run(cmd_tts, check=True)
    
    # Get duration using ffmpeg
    cmd = [ffmpeg_exe, "-i", audio_file]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        dur = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
        s['duration'] = round(dur + 0.35, 2)
    else:
        s['duration'] = 6.0
    print(f"Generated {s['id']}: duration = {s['duration']}s")

with open("scenes_config.json", "w", encoding="utf-8") as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)

print("\nSUCCESS: All voiceovers generated and scenes_config.json updated!")
