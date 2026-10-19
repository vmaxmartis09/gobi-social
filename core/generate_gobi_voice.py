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

async def generate_voice():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    # vi-VN-HoaiMyNeural is natural, warm, feminine Vietnamese voice
    communicate = edge_tts.Communicate(VOICEOVER_TEXT, voice="vi-VN-HoaiMyNeural", rate="+5%", pitch="+2Hz")
    await communicate.save(OUTPUT_FILE)
    print(f"[+] Voiceover generated successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_voice())
