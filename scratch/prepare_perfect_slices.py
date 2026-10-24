import subprocess
from pathlib import Path

VAULT_DIR = Path("assets/voice_vault")

SLICES = {
    "voice-fm-1-mb": {
        "start": "0.0",
        "duration": "3.75",
        "text": "Vừa thời trang lại vừa rất nhiều công năng cho mấy bà luôn nha."
    },
    "voice-fm-lyly": {
        "start": "0.0",
        "duration": "5.25",
        "text": "Ly không biết là mọi người nhận ra mình trưởng thành từ lúc nào."
    },
    "voice-fm-an-nhien": {
        "start": "0.0",
        "duration": "5.95",
        "text": "Và là lần đầu tiên sau rất lâu, thì mình thấy cuộc đời thật ra cũng không tệ như thế."
    },
    "voice-fm-tue-lam": {
        "start": "0.0",
        "duration": "3.85",
        "text": "Những người thất bại tư duy mà thấp kém, họ luôn luôn có một cái điểm chung."
    }
}

for voice_id, cfg in SLICES.items():
    v_dir = VAULT_DIR / voice_id
    raw_wav = v_dir / "raw_extracted_clean.wav"
    slice_wav = v_dir / "reference_clean_slice.wav"
    txt_file = v_dir / "reference_transcript.txt"
    preview_mp3 = v_dir / "source_original_preview.mp3"

    print(f"Creating perfect slice for {voice_id}...")
    cmd_slice = [
        "ffmpeg", "-y", "-ss", cfg["start"], "-t", cfg["duration"],
        "-i", str(raw_wav),
        "-ar", "24000", "-ac", "1",
        str(slice_wav)
    ]
    subprocess.run(cmd_slice, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Preview MP3
    cmd_prev = [
        "ffmpeg", "-y", "-i", str(slice_wav),
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-ar", "44100", "-b:a", "192k",
        str(preview_mp3)
    ]
    subprocess.run(cmd_prev, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Save transcript
    txt_file.write_text(cfg["text"], encoding="utf-8")
    print(f"  -> Slice: {slice_wav} ({cfg['duration']}s)")
    print(f"  -> Text: {cfg['text']}")

print("All perfect slices prepared!")
