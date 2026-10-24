import os
import sys
import subprocess
import torch
import soundfile as sf
import numpy as np
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
omnivoice_pkg = repo_root / "integrations" / "OmniVoice"
sys.path.insert(0, str(omnivoice_pkg))

from omnivoice import OmniVoice, VoiceClonePrompt

VAULT_DIR = repo_root / "assets" / "voice_vault"
OUTPUT_DIR = repo_root / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GREETING_TEXT = "Hello gô bi thúi của em , em là Gô bi của anh đây nè !"

VOICE_LIST = [
    "voice-fm-1-mb",
    "voice-fm-lyly",
    "voice-fm-an-nhien",
    "voice-fm-tue-lam"
]

LYLY_REVIEW_SEGMENTS = [
    ("01_hook", "Ai bảo mùa đông mặc áo bông là nhìn bị nấm lùn với béo tròn? Chỉ cần phối theo hai tips này là dáng bao xinh luôn nè!"),
    ("02_phoi_1", "Outfit đầu tiên: Áo bông phom lửng phối cùng chân váy chữ A và boot cao. Cách này giúp phần thân trên ấm áp mà chân nhìn dài miên man luôn."),
    ("03_phoi_2", "Bà nào thích năng động ấm áp thì mix ngay với quần suông ống rộng nha. Chất bông xù mềm như ôm gấu bông ấy, màu be sữa vừa tôn da vừa cưng xỉu."),
    ("04_cta", "Chất xịn mà giá chỉ bằng mấy ly trà sữa thôi. Link tui để sẵn ở giỏ hàng góc trái cho mấy bà tham khảo nha!")
]

def master_audio(input_wav: Path, output_mp3: Path, target_lufs: float = -14.0):
    cmd = [
        "ffmpeg", "-y", "-i", str(input_wav),
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
        "-ar", "44100", "-b:a", "192k",
        str(output_mp3)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Mastered: {output_mp3}")

def main():
    print(">>> Loading OmniVoice model with MPS acceleration...")
    model = OmniVoice.from_pretrained(
        "k2-fsa/OmniVoice",
        device_map="mps",
        dtype=torch.float16,
    )

    prompts = {}
    
    print("\n==========================================")
    print("STEP 1: RE-CLONING ALL VOICES IN VAULT")
    print("==========================================")

    for voice_id in VOICE_LIST:
        v_dir = VAULT_DIR / voice_id
        ref_slice = v_dir / "reference_clean_slice.wav"
        txt_file = v_dir / "reference_transcript.txt"
        prompt_path = v_dir / "omnivoice_prompt.pt"

        print(f"\n--- Processing [{voice_id}] ---")
        if not ref_slice.exists():
            print(f"Error: {ref_slice} not found!")
            continue

        ref_text = txt_file.read_text(encoding="utf-8").strip() if txt_file.exists() else None
        print(f"Using exact ref_text: '{ref_text}'")

        print(f"Creating exact aligned prompt for {voice_id}...")
        prompt = model.create_voice_clone_prompt(
            ref_audio=str(ref_slice),
            ref_text=ref_text
        )
        prompt.save(str(prompt_path))
        print(f"Saved prompt to {prompt_path}")

        prompts[voice_id] = prompt

        # Generate Greeting
        print(f"Synthesizing greeting for {voice_id}...")
        wav_out = model.generate(
            text=GREETING_TEXT,
            language="vi",
            voice_clone_prompt=prompt,
            speed=1.0,
            denoise=True,
            num_step=32
        )

        raw_wav_path = repo_root / "scratch" / f"{voice_id}_greet_raw.wav"
        sf.write(str(raw_wav_path), wav_out[0], 24000)

        # Save to vault
        vault_sample = v_dir / "cloned_default_sample.mp3"
        master_audio(raw_wav_path, vault_sample)

        # Copy to output/
        out_sample = OUTPUT_DIR / f"{voice_id}_cloned_default_sample.mp3"
        master_audio(raw_wav_path, out_sample)

        # Sync original preview to output/
        src_preview = v_dir / "source_original_preview.mp3"
        if src_preview.exists():
            out_preview = OUTPUT_DIR / f"{voice_id}_source_original_preview.mp3"
            import shutil
            shutil.copyfile(src_preview, out_preview)
            print(f"Synced source preview: {out_preview}")

    # 2. Process LyLy Review Segments
    print("\n==========================================")
    print("STEP 2: GENERATING LYLY REVIEW SEGMENTS")
    print("==========================================")
    lyly_prompt = prompts["voice-fm-lyly"]

    segment_wavs = []
    for tag, text in LYLY_REVIEW_SEGMENTS:
        print(f"\nSynthesizing segment [{tag}]...")
        seg_audio = model.generate(
            text=text,
            language="vi",
            voice_clone_prompt=lyly_prompt,
            speed=1.0, # Natural conversational pace
            denoise=True,
            num_step=32
        )
        seg_wav = repo_root / "scratch" / f"lyly_{tag}_raw.wav"
        sf.write(str(seg_wav), seg_audio[0], 24000)

        seg_mp3 = OUTPUT_DIR / f"voice_fm_lyly_{tag}.mp3"
        master_audio(seg_wav, seg_mp3)
        segment_wavs.append(seg_wav)

    # 3. Concatenate Review Segments with natural pauses (350ms silence)
    print("\n==========================================")
    print("STEP 3: CONCATENATING FULL VIDEO AUDIO")
    print("==========================================")
    combined_samples = []
    sr = 24000
    silence_350ms = np.zeros(int(sr * 0.35), dtype=np.float32)

    for i, wav_p in enumerate(segment_wavs):
        data, file_sr = sf.read(str(wav_p))
        combined_samples.append(data)
        if i < len(segment_wavs) - 1:
            combined_samples.append(silence_350ms)

    full_data = np.concatenate(combined_samples)
    full_wav = repo_root / "scratch" / "voice_fm_lyly_full_video_raw.wav"
    sf.write(str(full_wav), full_data, sr)

    full_video_mp3 = OUTPUT_DIR / "voice_fm_lyly_full_video.mp3"
    master_audio(full_wav, full_video_mp3)
    print(f"\n>>> Full Mastered Video Audio: {full_video_mp3}")

    print("\n==========================================")
    print("STEP 4: WHISPER STT VERIFICATION")
    print("==========================================")
    from transformers import pipeline
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small", device="cpu")

    test_files = [
        ("voice-fm-1-mb greeting", OUTPUT_DIR / "voice-fm-1-mb_cloned_default_sample.mp3"),
        ("voice-fm-lyly greeting", OUTPUT_DIR / "voice-fm-lyly_cloned_default_sample.mp3"),
        ("voice-fm-an-nhien greeting", OUTPUT_DIR / "voice-fm-an-nhien_cloned_default_sample.mp3"),
        ("voice-fm-tue-lam greeting", OUTPUT_DIR / "voice-fm-tue-lam_cloned_default_sample.mp3"),
        ("voice-fm-lyly hook", OUTPUT_DIR / "voice_fm_lyly_01_hook.mp3"),
        ("voice-fm-lyly phoi 1", OUTPUT_DIR / "voice_fm_lyly_02_phoi_1.mp3"),
        ("voice-fm-lyly phoi 2", OUTPUT_DIR / "voice_fm_lyly_03_phoi_2.mp3"),
        ("voice-fm-lyly cta", OUTPUT_DIR / "voice_fm_lyly_04_cta.mp3"),
    ]

    for label, fpath in test_files:
        if fpath.exists():
            res = pipe(str(fpath))
            print(f"[{label}]: {res['text'].strip()}")

    print("\n>>> ALL CLONING & VERIFICATION COMPLETE!")

if __name__ == "__main__":
    main()
