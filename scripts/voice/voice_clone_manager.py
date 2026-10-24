"""
=============================================================================
NEURAL VOICE CLONE ENGINE - VMAX AI FACTORY
Sử dụng mô hình F5-TTS / E2-TTS Zero-Shot Voice Cloning thực sự:
1. Trích xuất audio mẫu từ video người thật (MP4/TikTok).
2. Tự động nhận diện chữ gốc (Reference Text).
3. Đưa vào Neural Diffusion Transformer (DiT) để nội suy giọng nói người thật.
4. Xuất file âm thanh đọc kịch bản mới bằng chính giọng đó 100%.
=============================================================================
"""

import os
import sys
import shutil
import subprocess
from gradio_client import Client, handle_file
import imageio_ffmpeg

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICES_DIR = os.path.abspath("assets/cloned_voices")

def extract_reference_from_video(video_path, voice_name, start_time="00:00:00", duration="10"):
    """Tách đoạn âm thanh mẫu từ video người thật."""
    profile_dir = os.path.join(VOICES_DIR, voice_name)
    os.makedirs(profile_dir, exist_ok=True)
    
    ref_wav = os.path.join(profile_dir, "reference_voice.wav")
    cmd = [
        FFMPEG, "-y",
        "-ss", start_time,
        "-t", str(duration),
        "-i", video_path,
        "-vn",
        "-ar", "24000",
        "-ac", "1",
        ref_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return ref_wav

def clone_and_speak_neural(ref_audio_path, ref_text, new_script, output_path):
    """
    Sử dụng mô hình Neural F5-TTS Zero-Shot Voice Clone thực thụ:
    Nạp audio người thật + text tương ứng -> Tự sinh kịch bản mới bằng chất giọng đó.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    print("\n[NEURAL VOICE CLONE] Đang kết nối mô hình F5-TTS Zero-Shot Voice Cloning...")
    client = Client("mrfakename/E2-F5-TTS")
    
    print(f"-> Mẫu âm thanh người thật: {ref_audio_path}")
    print(f"-> Text đối chiếu gốc: \"{ref_text[:50]}...\"")
    print(f"-> Kịch bản mới cần đọc: \"{new_script}\"")
    
    result = client.predict(
        ref_audio=handle_file(ref_audio_path),
        ref_text=ref_text,
        gen_text=new_script,
        remove_silence=True,
        api_name="/predict"
    )
    
    src_file = result[0] if isinstance(result, (list, tuple)) else result
    
    # Chuyển đổi sang MP3 hoặc giữ WAV theo yêu cầu
    if output_path.endswith('.mp3'):
        cmd_convert = [FFMPEG, "-y", "-i", src_file, "-b:a", "192k", output_path]
        subprocess.run(cmd_convert, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        shutil.copy2(src_file, output_path)
        
    print(f"\n[THÀNH CÔNG] File âm thanh Clone bằng Neural AI đã tạo:")
    print(f"-> {os.path.abspath(output_path)} ({os.path.getsize(output_path):,} bytes)")
    return output_path

if __name__ == '__main__':
    # Chạy thử nghiệm ngay với mau-voice.mp4
    video = "mau-voice.mp4"
    voice_name = "koc_neil_girl"
    
    ref_wav = extract_reference_from_video(video, voice_name, start_time="00:00:00", duration="10")
    ref_txt = "Còn một em áo thun vừa thời trang lại vừa rất là nhiều công năng cho mấy bà luôn nha. Chất thì rất là co giãn đàn hồi."
    
    new_script = "Mấy bà ơi, hôm nay em lên tiếp một mã áo thun chống nắng siêu đỉnh cho mùa hè này nhé! Nhanh tay bấm giỏ hàng kẻo hết size nha!"
    out_file = "output/true_neural_cloned_voice.mp3"
    
    clone_and_speak_neural(ref_wav, ref_txt, new_script, out_file)
