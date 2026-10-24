import os
import sys
import shutil
import subprocess
import imageio_ffmpeg
from gradio_client import Client, handle_file

sys.stdout.reconfigure(encoding='utf-8')
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

os.makedirs("assets/cloned_voices/koc_neil_girl", exist_ok=True)
os.makedirs("output", exist_ok=True)

video_src = "mau-voice.mp4"

# 1. Cắt chuẩn 4.2 giây giọng sạch (câu đầu tiên rõ chữ nhất, lọc tạp âm nền bằng afftdn) cho VieNeu-TTS
ref_4s = os.path.abspath("assets/cloned_voices/koc_neil_girl/ref_4s_clean.wav")
subprocess.run([
    FFMPEG, "-y",
    "-ss", "00:00:00.2",
    "-t", "4.2",
    "-i", video_src,
    "-vn",
    "-af", "highpass=f=80,lowpass=f=12000,afftdn=nf=-25",
    "-ar", "48000",
    "-ac", "1",
    ref_4s
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"[1] Đã tách mẫu 4.2s chuẩn cho VieNeu-TTS: {ref_4s}")

# 2. Cắt 15 giây giọng giàu năng lượng Action từ mau-voice.mp4 làm Target cho Seed-VC (Voice Conversion)
ref_15s = os.path.abspath("assets/cloned_voices/koc_neil_girl/ref_15s_target_vc.wav")
subprocess.run([
    FFMPEG, "-y",
    "-ss", "00:00:00.2",
    "-t", "15.0",
    "-i", video_src,
    "-vn",
    "-af", "highpass=f=80,lowpass=f=12000,afftdn=nf=-25",
    "-ar", "44100",
    "-ac", "1",
    ref_15s
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"[2] Đã tách mẫu 15s giàu năng lượng Action cho Voice Conversion: {ref_15s}")

# 3. Chạy Stage 1: VieNeu-TTS v3 Turbo với mẫu 4.2s chuẩn
script = (
    "Mấy bà ơi, hôm nay em lên tiếp một mã áo thun chống nắng siêu đỉnh cho mùa hè này nhé! "
    "Chất vải siêu co giãn, mặc mát lạnh cực kỳ, nhanh tay bấm ngay vào giỏ hàng góc trái kẻo hết size nha mấy bà!"
)

print("\n[3] Stage 1: Đang sinh giọng Tiếng Việt chuẩn với mẫu 4.2s trên VieNeu-TTS v3 Turbo...")
c_vieneu = Client("pnnbao-ump/VieNeu-TTS-v3-Turbo")
res_vieneu = c_vieneu.predict(
    text=script,
    voice="Thùy Dung",
    ref_audio=handle_file(ref_4s),
    temperature=0.75,
    top_k=25,
    top_p=0.95,
    repetition_penalty=1.2,
    max_new_frames=400,
    max_chars=256,
    api_name="/synthesize"
)

stage1_wav = os.path.abspath("output/stage1_vieneu_4s_opt.wav")
stage1_mp3 = os.path.abspath("output/stage1_vieneu_4s_opt.mp3")
shutil.copy2(res_vieneu[0], stage1_wav)
subprocess.run([FFMPEG, "-y", "-i", stage1_wav, "-b:a", "192k", stage1_mp3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f" -> Đã lưu Stage 1 (VieNeu 4.2s tối ưu): {stage1_mp3}")

# 4. Chạy Stage 2 (Lựa chọn 2 - Voice Conversion): Dùng Seed-VC để đắp dây thanh quản & style của mau-voice.mp4 lên Stage 1
print("\n[4] Stage 2A: Đang chạy Voice Conversion (Seed-VC Diffusion) tráo thanh quản sang mẫu thật mau-voice.mp4...")
c_vc = Client("Plachta/Seed-VC")

# Mode 1: /predict_1 (High-fidelity Timbre & Auto-F0 Pitch Matching)
res_vc1 = c_vc.predict(
    source_audio_path=handle_file(stage1_wav),
    target_audio_path=handle_file(ref_15s),
    diffusion_steps=30,
    length_adjust=0.95, # Tăng nhẹ tốc độ 5% cho giống nhịp nói nhanh của bạn nữ trong mau-voice.mp4
    inference_cfg_rate=0.75,
    f0_condition=False,
    auto_f0_adjust=True,
    pitch_shift=0,
    api_name="/predict_1"
)
full_vc1 = res_vc1[1] if isinstance(res_vc1, (list, tuple)) and len(res_vc1) > 1 else res_vc1[0]
out_vc1_wav = os.path.abspath("output/option2_vc_timbre_cloned.wav")
out_vc1_mp3 = os.path.abspath("output/option2_vc_timbre_cloned.mp3")
shutil.copy2(full_vc1, out_vc1_wav)
subprocess.run([FFMPEG, "-y", "-i", out_vc1_wav, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", out_vc1_mp3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f" -> Đã lưu Option 2A (Voice Conversion Timbre + Pitch): {out_vc1_mp3}")

# Mode 2: /predict (V2 Voice + Action Style Conversion)
print("\n[5] Stage 2B: Đang chạy Seed-VC V2 (Chuyển đổi cả Giọng + Ngữ điệu Action Style)...")
try:
    res_vc2 = c_vc.predict(
        source_audio_path=handle_file(stage1_wav),
        target_audio_path=handle_file(ref_15s),
        diffusion_steps=30,
        length_adjust=0.95,
        intelligebility_cfg_rate=0.5,
        similarity_cfg_rate=0.8,
        top_p=0.9,
        temperature=1.0,
        repetition_penalty=1.0,
        convert_style=True,
        anonymization_only=False,
        api_name="/predict"
    )
    full_vc2 = res_vc2[1] if isinstance(res_vc2, (list, tuple)) and len(res_vc2) > 1 else res_vc2[0]
    out_vc2_wav = os.path.abspath("output/option2_vc_style_action_cloned.wav")
    out_vc2_mp3 = os.path.abspath("output/option2_vc_style_action_cloned.mp3")
    shutil.copy2(full_vc2, out_vc2_wav)
    subprocess.run([FFMPEG, "-y", "-i", out_vc2_wav, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", out_vc2_mp3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f" -> Đã lưu Option 2B (Voice + Action Style Conversion): {out_vc2_mp3}")
except Exception as e:
    print(f" -> Lưu ý Stage 2B: {e}")

# 6. Ghép vào video mẫu hoàn chỉnh
video_out = os.path.abspath("output/mau_voice_option2_vc_video.mp4")
subprocess.run([
    FFMPEG, "-y",
    "-ss", "00:00:00",
    "-t", "10.0",
    "-i", video_src,
    "-i", out_vc1_mp3,
    "-c:v", "copy",
    "-c:a", "aac",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-shortest",
    video_out
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"\n[HOÀN TẤT] Video ghép giọng Option 2 VC: {video_out}")
