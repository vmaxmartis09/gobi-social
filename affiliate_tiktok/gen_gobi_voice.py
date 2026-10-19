import sys
import asyncio
import os
import edge_tts
from mutagen.mp3 import MP3

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_9S = "Hello ông kẹ, em là Gobi thúi của anh đây! Hôm nay cùng em lên đồ thật xinh và dạo phố nha, yêu anh nhiều!"
OUT_DIR = r"./affiliate_tiktok\sample_video\audio"
os.makedirs(OUT_DIR, exist_ok=True)
OUT_AUDIO = os.path.join(OUT_DIR, "gobi_thui_9s.mp3")
OUT_VTT = os.path.join(OUT_DIR, "gobi_thui_9s.vtt")

async def gen():
    comm = edge_tts.Communicate(SCRIPT_9S, "vi-VN-HoaiMyNeural", rate="-2%")
    submaker = edge_tts.SubMaker()
    with open(OUT_AUDIO, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    with open(OUT_VTT, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())
    audio = MP3(OUT_AUDIO)
    print(f"Generated audio: {OUT_AUDIO}")
    print(f"Duration: {audio.info.length:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(gen())
