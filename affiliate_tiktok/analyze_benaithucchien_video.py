import os
import subprocess
import imageio_ffmpeg
from PIL import Image

video_path = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_full.mp4"
audio_out = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_audio.mp3"
frames_dir = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\benaithucchien_frames"
os.makedirs(frames_dir, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 1. Extract audio
cmd_audio = [ffmpeg_exe, "-y", "-i", video_path, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", audio_out]
subprocess.run(cmd_audio, check=True)
print(f"Extracted audio to {audio_out}")

# 2. Extract keyframes every 2 seconds
cmd_frames = [ffmpeg_exe, "-y", "-i", video_path, "-vf", "fps=1/2", os.path.join(frames_dir, "frame_%03d.jpg")]
subprocess.run(cmd_frames, check=True)
frame_files = sorted(os.listdir(frames_dir))
print(f"Extracted {len(frame_files)} frames to {frames_dir}")
