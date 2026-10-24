import json
from pathlib import Path
import soundfile as sf
from faster_whisper import WhisperModel

audio_path = "data/raw/user_input_product/audio_extracted.wav"
print("Loading audio array via soundfile...")
audio_array, sr = sf.read(audio_path, dtype="float32")

print(f"Loaded audio: shape={audio_array.shape}, sr={sr}")
print("Loading faster-whisper model...")
model = WhisperModel("base", device="cpu", compute_type="int8")

print(f"Transcribing audio array...")
segments, info = model.transcribe(audio_array, language="vi", beam_size=5)

results = []
full_text = []

for s in segments:
    entry = {
        "start": round(s.start, 2),
        "end": round(s.end, 2),
        "text": s.text.strip()
    }
    results.append(entry)
    full_text.append(s.text.strip())
    print(f"[{entry['start']}s -> {entry['end']}s]: {entry['text']}")

output = {
    "language": info.language,
    "duration": round(info.duration, 2),
    "full_transcript": " ".join(full_text),
    "segments": results
}

out_path = Path("data/raw/user_input_product/transcript.json")
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Transcript saved to {out_path}")
