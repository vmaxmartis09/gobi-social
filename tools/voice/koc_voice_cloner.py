"""
KOC AI Voice Cloner & Mastering Pipeline
=========================================
Integrated system to clone real voices from TikTok/review videos into persistent Sound Profiles
and synthesize new review scripts with TikTok Action KOC energy.

Based on:
- VieNeu-TTS v3 Turbo architecture (the core engine powering EverAI v1.6 as taught by @benaithucchien)
- TikTok Broadcast Audio Mastering (-14 LUFS, presence EQ, vocal compand)
- Automated Video-Audio Dubbing & Subtitling
"""

import os
import sys
import json
import time
import subprocess
import soundfile as sf
import numpy as np
from pathlib import Path
import imageio_ffmpeg

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

class KOCVoiceCloner:
    def __init__(self, profiles_dir: str = "assets/voice_profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self._tts = None

    def _get_tts(self):
        if self._tts is None:
            print("[KOCVoiceCloner] Loading VieNeu-TTS v3 Turbo model (ONNX CPU)...")
            from vieneu import Vieneu
            self._tts = Vieneu(mode="v3turbo")
            print("[KOCVoiceCloner] Model loaded successfully!")
        return self._tts

    def extract_audio_from_video(self, video_path: str, output_wav: str) -> str:
        """Extract high-quality 48kHz mono WAV from video."""
        cmd = [
            self.ffmpeg_exe, "-y",
            "-i", str(video_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "48000",
            "-ac", "1",
            str(output_wav)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_wav

    def find_best_reference_slice(self, wav_path: str, target_duration: float = 4.2) -> tuple:
        """
        Find the cleanest, most energetic continuous speech segment (3-5s).
        Avoids silent parts or overly loud distortion.
        """
        data, sr = sf.read(wav_path)
        if len(data.shape) > 1:
            data = data[:, 0]
        
        target_samples = int(target_duration * sr)
        step_samples = int(0.25 * sr)
        
        if len(data) <= target_samples:
            return data, sr

        best_score = -1e9
        best_start = 0

        # Scan windows to find optimal voice energy and stability
        for start in range(0, len(data) - target_samples, step_samples):
            window = data[start:start + target_samples]
            rms = np.sqrt(np.mean(window**2))
            
            # Avoid silence (< 0.05) or clipped audio (> 0.6)
            if rms < 0.05 or rms > 0.6:
                continue

            # Spectral energy concentration score
            zero_crossings = np.sum(np.abs(np.diff(np.sign(window)))) / len(window)
            score = rms * 10.0 - abs(zero_crossings - 0.12) * 5.0
            
            if score > best_score:
                best_score = score
                best_start = start

        best_window = data[best_start:best_start + target_samples]
        return best_window, sr

    def create_profile(
        self,
        media_path: str,
        profile_id: str,
        speaker_name: str = "KOC Neil Girl",
        gender: str = "female",
        accent: str = "vietnamese_north",
        style: str = "tiktok_action_review"
    ) -> dict:
        """
        Create a permanent sound profile from any video or audio file.
        """
        profile_path = self.profiles_dir / profile_id
        profile_path.mkdir(parents=True, exist_ok=True)

        media_path = Path(media_path)
        temp_wav = profile_path / "raw_extracted.wav"

        print(f"[KOCVoiceCloner] Extracting audio from {media_path}...")
        self.extract_audio_from_video(media_path, str(temp_wav))

        # Extract optimal 4.2s clean reference slice (best practice for VieNeu-TTS v3 Turbo)
        clean_slice, sr = self.find_best_reference_slice(str(temp_wav), target_duration=4.2)
        ref_wav_path = profile_path / "reference_clean_4s.wav"
        sf.write(str(ref_wav_path), clean_slice, sr)

        # Also save full speech wav for voice conversion models
        full_ref_path = profile_path / "reference_full.wav"
        if not full_ref_path.exists():
            import shutil
            shutil.copyfile(str(temp_wav), str(full_ref_path))

        metadata = {
            "profile_id": profile_id,
            "speaker_name": speaker_name,
            "gender": gender,
            "accent": accent,
            "style": style,
            "source_media": str(media_path.resolve()),
            "clean_ref_wav": str(ref_wav_path.resolve()),
            "full_ref_wav": str(full_ref_path.resolve()),
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        meta_file = profile_path / "profile.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"[KOCVoiceCloner] Profile '{profile_id}' created successfully at {profile_path}!")
        return metadata

    def synthesize(
        self,
        profile_id: str,
        text: str,
        output_path: str,
        speed: float = 1.05,
        master_for_tiktok: bool = True
    ) -> str:
        """
        Synthesize speech using the cloned voice profile and apply TikTok Action mastering.
        """
        profile_dir = self.profiles_dir / profile_id
        meta_file = profile_dir / "profile.json"
        
        # Fallback to koc_neil_girl in assets/cloned_voices if profile not in voice_profiles
        if not meta_file.exists():
            alt_ref = Path("assets/cloned_voices/koc_neil_girl/ref_4s_clean.wav")
            if alt_ref.exists():
                ref_audio = str(alt_ref)
            else:
                raise FileNotFoundError(f"Profile {profile_id} not found in {self.profiles_dir}")
        else:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            ref_audio = meta["clean_ref_wav"]

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        raw_output_wav = output_path.with_suffix(".raw.wav")

        print(f"[KOCVoiceCloner] Synthesizing speech with profile '{profile_id}'...")
        print(f"Text: \"{text}\"")
        tts = self._get_tts()
        
        audio_data = tts.infer(
            text=text,
            ref_audio=ref_audio,
            denoise=True,
            apply_watermark=False,
            temperature=0.75,
            top_k=25,
            top_p=0.95
        )
        sf.write(str(raw_output_wav), audio_data, 48000)

        if master_for_tiktok:
            print("[KOCVoiceCloner] Mastering audio for TikTok Action KOC presence...")
            # Master filter:
            # - Vocal compressor (punch and consistency)
            # - Presence boost around 3.2kHz (+3.5dB)
            # - Warmth boost around 250Hz (+1.2dB)
            # - TikTok standard loudness (-14 LUFS)
            # - Dynamic tempo adjustment
            af_filter = (
                f"acompressor=threshold=-18dB:ratio=4:attack=5:release=50,"
                f"equalizer=f=3200:t=q:w=1.2:g=3.5,"
                f"equalizer=f=250:t=q:w=1.0:g=1.2,"
                f"loudnorm=I=-14:TP=-1.5:LRA=7,"
                f"atempo={speed}"
            )
            
            cmd = [
                self.ffmpeg_exe, "-y",
                "-i", str(raw_output_wav),
                "-af", af_filter,
                "-ar", "48000",
                "-b:a", "192k",
                str(output_path)
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Clean up raw temp wav if mp3 requested
            if output_path.suffix.lower() == ".mp3" and raw_output_wav.exists():
                try:
                    raw_output_wav.unlink()
                except Exception:
                    pass
        else:
            if output_path.suffix.lower() == ".mp3":
                cmd = [self.ffmpeg_exe, "-y", "-i", str(raw_output_wav), "-b:a", "192k", str(output_path)]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                raw_output_wav.unlink()

        print(f"[KOCVoiceCloner] Synthesized and mastered audio saved: {output_path}")
        return str(output_path)

    def render_demo_video(
        self,
        video_source: str,
        audio_path: str,
        script_text: str,
        output_video: str
    ) -> str:
        """
        Multiplex the generated voice with video footage and add TikTok stylized subtitles.
        """
        output_video = Path(output_video)
        output_video.parent.mkdir(parents=True, exist_ok=True)

        info = sf.info(audio_path)
        audio_duration = info.duration

        print(f"[KOCVoiceCloner] Rendering demo video ({audio_duration:.1f}s)...")

        # Create ASS subtitle file for gorgeous TikTok Safe Zone subtitles
        words = script_text.split()
        mid = len(words) // 2
        chunk1 = " ".join(words[:mid])
        chunk2 = " ".join(words[mid:])
        half_dur = audio_duration / 2.0

        def format_ass_time(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = sec % 60
            return f"{h:01d}:{m:02d}:{s:05.2f}"

        ass_path = output_video.with_suffix(".ass")
        ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTokKOC,Arial,65,&H0000FFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,40,40,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{format_ass_time(0.2)},{format_ass_time(half_dur)},TikTokKOC,,0,0,0,,{chunk1}
Dialogue: 0,{format_ass_time(half_dur)},{format_ass_time(audio_duration - 0.2)},TikTokKOC,,0,0,0,,{chunk2}
"""
        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_content)

        ass_filter_path = str(ass_path).replace("\\", "/").replace(":", "\\:")
        vf = f"ass='{ass_filter_path}'"

        cmd = [
            self.ffmpeg_exe, "-y",
            "-stream_loop", "-1",
            "-i", str(video_source),
            "-i", str(audio_path),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-t", f"{audio_duration:.2f}",
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video)
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            # Fallback without subtitle filter if libass encounters font path issue
            fallback_cmd = [
                self.ffmpeg_exe, "-y",
                "-stream_loop", "-1",
                "-i", str(video_source),
                "-i", str(audio_path),
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-t", f"{audio_duration:.2f}",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(output_video)
            ]
            subprocess.run(fallback_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if ass_path.exists():
            try:
                ass_path.unlink()
            except Exception:
                pass

        print(f"[KOCVoiceCloner] Demo video successfully rendered: {output_video}")
        return str(output_video)

if __name__ == "__main__":
    cloner = KOCVoiceCloner()
    
    # 1. Create Profile from mau-voice.mp4
    video_file = "mau-voice.mp4"
    profile_id = "koc_neil_girl"
    
    print("=== STEP 1: Creating Voice Profile ===")
    profile = cloner.create_profile(video_file, profile_id)
    
    # 2. Synthesize new TikTok review script
    script = (
        "Mấy bà ơi, hôm nay em lên tiếp một mã áo thun chống nắng siêu đỉnh cho mùa hè này nhé! "
        "Chất vải siêu co giãn, thoáng mát cực kỳ. "
        "Nhanh tay bấm ngay vào giỏ hàng góc trái bên dưới kẻo hết size nha!"
    )
    
    print("\n=== STEP 2: Synthesizing Script with Cloned Voice ===")
    out_mp3 = "output/koc_neil_girl_review_action.mp3"
    cloner.synthesize(profile_id, script, out_mp3, speed=1.05)
    
    # 3. Render complete video with subtitles
    print("\n=== STEP 3: Rendering TikTok Demo Video ===")
    out_mp4 = "output/koc_neil_girl_review_demo.mp4"
    cloner.render_demo_video(video_file, out_mp3, script, out_mp4)
    print("\n=== ALL COMPLETE! ===")
