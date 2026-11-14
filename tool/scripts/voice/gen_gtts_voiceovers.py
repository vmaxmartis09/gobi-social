import json
import os
import subprocess
import re
from gtts import gTTS
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

scenes = [
    {
        "id": "scene1",
        "image": "assets/images/scene1_hook.jpg",
        "text": "Đừng vội mua tai nghe nếu bạn chưa xem hết video này! Đây là chiếc tai nghe chống ồn đang làm mưa làm gió thị trường.",
        "hook_title": "DỪNG LẠI 3 GIÂY!",
        "subtitle_1": "Đừng vội mua tai nghe nếu chưa xem hết video!",
        "subtitle_2": "Chiếc tai nghe chống ồn đang cực hot 2026",
        "badge": "🔥 TOP TRENDING"
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
        "text": "Nhưng với công nghệ chống ồn chủ động 45 đề-xi-ben và đệm khí siêu êm, bạn sẽ bước vào không gian tĩnh lặng tuyệt đối.",
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
        "text": "Đang có deal giảm 40 phần trăm và miễn phí giao hàng độc quyền ngay giỏ hàng góc trái. Bấm đặt ngay kẻo hết nhé!",
        "hook_title": "ƯU ĐÃI KHỦNG HÔM NAY",
        "subtitle_1": "Ưu đãi độc quyền: Giảm ngay 40%",
        "subtitle_2": "Miễn phí ship toàn quốc - Bấm giỏ hàng ngay!",
        "badge": "🎁 SỐ LƯỢNG CÓ HẠN"
    }
]

os.makedirs('assets/audio', exist_ok=True)

for s in scenes:
    audio_file = f"assets/audio/{s['id']}.mp3"
    tts = gTTS(text=s['text'], lang='vi', slow=False)
    tts.save(audio_file)
    
    # Get exact duration using ffmpeg
    cmd = [ffmpeg_exe, "-i", audio_file]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        dur = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
        s['duration'] = round(dur + 0.35, 2)
    else:
        s['duration'] = 6.0
    print(f"Generated {s['id']}: duration = {s['duration']}s, file size = {os.path.getsize(audio_file)} bytes")

with open("configs/scenes_config.json", "w", encoding="utf-8") as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)

print("\nSUCCESS: All scene voiceovers generated cleanly with gTTS!")
