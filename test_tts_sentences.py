import asyncio
import edge_tts
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

test_sentences = [
    # Scene 1
    ("scene1", "Đừng vội mua tai nghe nếu bạn chưa xem hết video này! Đây là chiếc tai nghe chống ồn tốt nhất hiện nay."),
    # Scene 2
    ("scene2", "Bạn mệt mỏi vì tiếng ồn xung quanh khi làm việc hay đi lại? Đeo tai nghe cũ chỉ một tiếng là đau nhức tai."),
    # Scene 3
    ("scene3", "Nhưng với công nghệ chống ồn chủ động 45 đề-xi-ben và đệm khí siêu êm, bạn sẽ bước vào không gian tĩnh lặng tuyệt đối."),
    # Scene 4
    ("scene4", "Chất âm vòm 360 độ cực kỳ sống động, pin trâu liên tục 40 giờ. Đàm thoại lọc gió rõ nét từng lời."),
    # Scene 5
    ("scene5", "Đang có ưu đãi giảm 40 phần trăm và miễn phí giao hàng ngay trong giỏ hàng góc trái. Bấm đặt ngay kẻo lỡ nhé!")
]

async def test_all():
    voice = "vi-VN-HoaiMyNeural"
    for sid, text in test_sentences:
        try:
            comm = edge_tts.Communicate(text, voice)
            await comm.save(f"assets/audio/{sid}.mp3")
            print(f"SUCCESS: {sid}")
        except Exception as e:
            print(f"FAILED {sid}: {e}")

asyncio.run(test_all())
