import os
import sys
import asyncio
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "assets", "samples", "sample_video")
AUDIO_DIR = os.path.join(SAMPLE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Kịch bản chuẩn 20 giây TikTok Shop Affiliate (45-50 từ)
# Hook (3s) -> Lợi ích & Chất vải (12s) -> CTA Giỏ hàng (5s)
SCRIPT_TEXT = (
    "Mấy bà đang tìm áo cardigan mặc đi học, đi làm vừa ấm vừa tôn dáng thì xem ngay em này nha! "
    "Chất len dệt kim mềm mịn, dày dặn mà không hề dặm ngứa. "
    "Form rộng chuẩn Hàn Quốc giấu dáng cực đỉnh, phối cùng chân váy hay quần suông đều xinh xỉu. "
    "Giá đang sale hời dưới một trăm cành ở giỏ hàng góc trái, mấy bà tranh thủ săn ngay kẻo hết nha!"
)

VOICE = "vi-VN-HoaiMyNeural"
RATE = "+10%"  # Hơi nhanh một chút cho năng động, đúng nhịp TikTok
OUTPUT_AUDIO = os.path.join(AUDIO_DIR, "cardigan_voiceover.mp3")
OUTPUT_SUB = os.path.join(AUDIO_DIR, "cardigan_subtitles.vtt")

async def generate():
    print("="*60)
    print("🎙️ ĐANG TẠO GIỌNG ĐỌC AI TIẾNG VIỆT CHUẨN TIKTOK...")
    print(f"[*] Voice:  {VOICE}")
    print(f"[*] Tốc độ: {RATE}")
    print(f"[*] Script: {SCRIPT_TEXT}")
    print("="*60)

    communicate = edge_tts.Communicate(SCRIPT_TEXT, VOICE, rate=RATE)
    submaker = edge_tts.SubMaker()
    
    with open(OUTPUT_AUDIO, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    with open(OUTPUT_SUB, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())

    print(f"\n[+] Đã xuất file âm thanh: {OUTPUT_AUDIO}")
    print(f"[+] Đã xuất file phụ đề:   {OUTPUT_SUB}")
    
    # Check audio length using mutagen or pydub if available, else os size
    size_kb = os.path.getsize(OUTPUT_AUDIO) / 1024
    print(f"[+] Kích thước file: {size_kb:.1f} KB")

if __name__ == "__main__":
    asyncio.run(generate())
