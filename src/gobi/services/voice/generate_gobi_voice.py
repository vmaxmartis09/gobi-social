import asyncio
import os
import sys
import edge_tts

VOICEOVER_TEXT = (
    "Thời tiết thu lúc nóng lúc lạnh thế này thì đố chị em tìm được set đồ nào đỉnh hơn set 2 dây kèm cardigan này! "
    "Len dệt kim mỏng nhẹ, mềm mướt không hề bị dặm ngứa một xíu nào. "
    "Áo 2 dây bên trong ôm nhẹ tôn dáng, khoác thêm cardigan bên ngoài vừa che bắp tay vừa thanh lịch. "
    "Mặc đi học, đi làm hay đi cafe chụp hình thì chuẩn gu nàng thơ Hàn Quốc luôn. Tone màu be sữa này cực kỳ tôn da. "
    "Giá gốc gần 200k nhưng nhà Gobi Boutique đang trợ giá chỉ còn 139 cành ở icon giỏ hàng góc trái màn hình. "
    "Các bà bấm vào săn ngay kẻo hết deal nha!"
)

OUTPUT_FILE = os.path.abspath("output/audio/gobi_cardigan_voiceover.mp3")

async def generate_voiceover(text: str, output_path: str = OUTPUT_FILE, voice: str = "vi-VN-HoaiMyNeural", rate: str = "+5%", pitch: str = "+2Hz"):
    """Tổng hợp giọng nói tiếng Việt tự nhiên qua Edge-TTS."""
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    print(f"[+] Voiceover generated successfully at: {output_path}")
    return output_path

async def generate_voice():
    return await generate_voiceover(VOICEOVER_TEXT, OUTPUT_FILE)

if __name__ == "__main__":

    asyncio.run(generate_voice())
