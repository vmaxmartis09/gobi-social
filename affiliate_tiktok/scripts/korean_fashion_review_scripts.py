"""
VMAX Korean Fashion AI KOC Review Scripts Generator (Expanded Edition)
Tu dong sinh kich ban video review chuan phong cach Han Quoc nhu mi,
tich hop 36 goc may VMAX, Kling 3.0 camera prompts va ky thuat chot don gio hang.
Bao gom du lieu tu 104 video Big Data TikTok voi cac dinh cao 2.6M va 1.0M views.
"""

import sys
import os
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_script_set_cardigan():
    return {
        "product": "Set Áo 2 Dây Kèm Cardigan Len Mỏng Hàn Quốc",
        "price_target": "139.000 VNĐ",
        "vibe": "Nàng thơ mùa thu, dịu dàng, tiểu thư Hàn Quốc",
        "duration": "24 giây",
        "scenes": [
            {
                "time": "0:00 - 0:03 (HOOK MÙA THU)",
                "panel": "Panel 06 (Cận mặt 3/4 biểu cảm tinh nghịch)",
                "camera_kling": "The young woman smiles gently, tilting her head slightly with soft eye contact. Slow cinematic push-in toward the face, 35mm lens, soft morning rim light, 8k resolution.",
                "voiceover": "Thời tiết thu lúc nóng lúc lạnh thế này thì đố chị em tìm được set đồ nào đỉnh hơn set 2 dây kèm cardigan này!",
                "text_on_screen": "SET ĐỒ CHÂN ÁI MÙA THU 🍂"
            },
            {
                "time": "0:03 - 0:12 (SOI CHẤT VẢI & CHI TIẾT)",
                "panel": "Panel 25 (Cận cảnh chất liệu len dệt kim)",
                "camera_kling": "Her hands gently touch and stretch the soft knitted fabric, showcasing delicate stitches. Locked-off tripod shot, natural subtle breathing, soft lighting.",
                "voiceover": "Len dệt kim mỏng nhẹ, mềm mướt không hề bị dặm ngứa một xíu nào. Áo 2 dây bên trong ôm nhẹ tôn dáng, khoác thêm cardigan bên ngoài vừa che bắp tay vừa thanh lịch.",
                "text_on_screen": "LEN DỆT KIM MỀM MƯỚT ✨"
            },
            {
                "time": "0:12 - 0:19 (LÊN DÁNG & XOAY NGƯỜI)",
                "panel": "Panel 26 (Bước đi tự nhiên) + Panel 10 (Nhìn lại qua vai)",
                "camera_kling": "The woman walks naturally and turns smoothly with a confident gentle smile. Camera pans smoothly to the right, parallel tracking, cinematic color grade.",
                "voiceover": "Mặc đi học, đi làm hay đi cafe chụp hình thì chuẩn gu nàng thơ Hàn Quốc luôn. Tone màu be sữa này cực kỳ tôn da.",
                "text_on_screen": "CHUẨN NÀNG THƠ HÀN QUỐC ☕"
            },
            {
                "time": "0:19 - 0:24 (KÊU GỌI BẤM GIỎ HÀNG)",
                "panel": "Panel 02 (Chính diện trung cảnh, chỉ tay góc trái)",
                "camera_kling": "The woman smiles brightly and points downward toward the lower left corner. Slow push-in, inviting expression.",
                "voiceover": "Giá gốc gần 200k nhưng nhà Gobi Boutique đang trợ giá chỉ còn 139 cành ở icon giỏ hàng góc trái màn hình. Các bà bấm vào săn ngay kẻo hết deal nha!",
                "text_on_screen": "GOBI BOUTIQUE SALE 139K GÓC TRÁI 👇"
            }
        ]
    }

def get_script_quan_short():
    return {
        "product": "Quần Short Nắp Túi Cạp Trễ Tôn Dáng",
        "price_target": "99.000 VNĐ",
        "vibe": "Năng động, cá tính nhẹ nhàng, hack chân dài",
        "duration": "18 giây",
        "scenes": [
            {
                "time": "0:00 - 0:03 (HOOK HACK CHÂN)",
                "panel": "Panel 03 (Cận mặt ngạc nhiên)",
                "camera_kling": "Close-up portrait of the young woman with an amazed expression, eyes wide. Slow push-in, shallow depth of field.",
                "voiceover": "Ai bảo đùi to với eo bánh mì là không mặc được quần short nắp túi thì bơi hết vào đây!",
                "text_on_screen": "HACK CHÂN DÀI CHO NÀNG ĐÙI TO 👖"
            },
            {
                "time": "0:03 - 0:10 (SOI FORM DÁNG & NẮP TÚI)",
                "panel": "Panel 22 (Góc ngang hông) + Panel 25 (Cận nắp túi)",
                "camera_kling": "Camera tracks slowly around the waist and pockets, showing firm stitching and flattering cut. Steady subtle glide.",
                "voiceover": "Form cạp trễ vừa phải, nắp túi 2 bên tạo điểm nhấn che khuyết điểm hông cực khéo. Chất kaki jean mềm đầm tay chứ không bị mỏng tanh đâu nha.",
                "text_on_screen": "NẮP TÚI CHE HÔNG CỰC KHÉO 💯"
            },
            {
                "time": "0:10 - 0:18 (XOAY DÁNG & CHỐT DEAL)",
                "panel": "Panel 36 (Tạo dáng nghệ thuật) + Panel 02 (Chỉ giỏ hàng)",
                "camera_kling": "The woman turns 360 degrees showing the back and side profile, then points down left with a cheerful smile.",
                "voiceover": "Phối với áo thun hay sơ mi cũng auto xinh. Đang sale sập sàn chỉ 99k ở giỏ hàng góc trái, chị em múc liền nha!",
                "text_on_screen": "SĂN DEAL 99K GÓC TRÁI 👇"
            }
        ]
    }

def get_script_quan_tay_tuyet_mua():
    """Kịch bản mô phỏng Top 1 Viral Benchmark 2.6M views (@nhat.linh.beauty)"""
    return {
        "product": "Quần Tây Ống Suông Lưng Cao Vải Tuyết Mưa Hack Dáng 1m1",
        "price_target": "129.000 VNĐ",
        "vibe": "Thanh lịch, công sở trẻ, hack chân dài miên man, che bụng dưới",
        "duration": "20 giây",
        "scenes": [
            {
                "time": "0:00 - 0:03 (HOOK HACK DÁNG BÙNG NỔ)",
                "panel": "Panel 01 (Toàn thân bước tới) + Panel 14 (Trung cảnh eo)",
                "camera_kling": "Full body shot of a stylish Asian young woman walking confidently forward in wide-leg black trousers. Low angle looking up slightly, creating an elongated leg effect, smooth dolly forward.",
                "voiceover": "Bà nào chân ngắn với bụng dưới to né gấp chiếc quần này ra... kẻo mặc vào bị nghi đi phẫu thuật kéo chân đó!",
                "text_on_screen": "NÉ GẤP NẾU KHÔNG MUỐN CHÂN DÀI 1M1 🚨"
            },
            {
                "time": "0:03 - 0:09 (SOI CẠP CAO SIẾT BỤNG & CHẤT TUYẾT MƯA)",
                "panel": "Panel 25 (Cận cảnh cạp quần siết phẳng và chất vải tuyết mưa)",
                "camera_kling": "Close-up of hands pulling gently on the high-waisted waistband, showing smooth flat fit over abdomen. Fabric drops smoothly without wrinkles. Locked-off macro shot.",
                "voiceover": "Lưng cao qua rốn khóa giữa 2 cúc siết trọn mỡ bụng dưới. Chất tuyết mưa Vitex dày dặn, đứng form mà rủ suôn mượt, giặt máy thoải mái không lo nhăn xù.",
                "text_on_screen": "CẠP CAO SIẾT TRỌN BỤNG DƯỚI ✨"
            },
            {
                "time": "0:09 - 0:15 (SẢI BƯỚC ĐI DÁNG CHUẨN HÀN)",
                "panel": "Panel 26 (Bước đi tự nhiên góc nghiêng) + Panel 21 (Góc nghiêng 45 độ)",
                "camera_kling": "Side-profile tracking shot as the woman walks past a minimalist aesthetic cafe. Soft natural daylight, trousers swaying elegantly over sneakers, 35mm lens.",
                "voiceover": "Ống suông rộng vừa phải che trọn chân cong đùi to. Phối cùng áo baby tee hay sơ mi đi học đi làm đều sang chảnh chuẩn gái Hàn.",
                "text_on_screen": "CHUẨN PHONG CÁCH HÀN QUỐC 🇰🇷"
            },
            {
                "time": "0:15 - 20:00 (CHỐT DEAL ĐỘC QUYỀN GÓC TRÁI)",
                "panel": "Panel 02 (Chính diện chỉ tay góc trái)",
                "camera_kling": "Medium shot of the young woman smiling warmly, raising her left hand and pointing smoothly toward the bottom-left corner of the frame. Gentle zoom in.",
                "voiceover": "Hôm nay Gobi Boutique trợ giá xả kho chỉ còn 129k kèm freeship. Các nàng bấm vào giỏ hàng góc trái chọn đúng bảng size nha!",
                "text_on_screen": "GOBI BOUTIQUE 129K + FREESHIP 👇"
            }
        ]
    }

def get_script_dam_hoa_nhi_7_cach_phoi():
    """Kịch bản mô phỏng Top 8 Benchmark 682k views, 8.7k saves (@gaumocne) - Nam châm hút lượt Lưu (Save Rate)"""
    return {
        "product": "Đầm 2 Dây Hoa Nhí Ngắn Xòe Nhẹ Style Hàn Quốc",
        "price_target": "135.000 VNĐ",
        "vibe": "Nàng thơ ngọt ngào, đa năng (Capsule Wardrobe), biến hóa phong cách",
        "duration": "22 giây",
        "scenes": [
            {
                "time": "0:00 - 0:03 (HOOK CUỐN HÚT / LƯU VIDEO)",
                "panel": "Panel 06 (Cận mặt 3/4 nụ cười ngọt ngào)",
                "camera_kling": "Close-up portrait of an adorable Asian woman holding a floral dress in front of a wardrobe. Subtle eye contact and welcoming smile, soft pastel lighting.",
                "voiceover": "Chỉ với một chiếc đầm hoa nhí 130 cành này, tui chỉ cho mấy bà 7 cách phối mặc cả tuần không trùng lặp nha!",
                "text_on_screen": "1 CHIẾC ĐẦM - 7 CÁCH PHỐI MẶC CẢ TUẦN 👗"
            },
            {
                "time": "0:03 - 0:14 (SHOW LIÊN TIẾP CÁC OUTFIT PHỐI THEO BEAT)",
                "panel": "Panel 01 (Toàn thân chuyển đổi trang phục nhanh mỗi 1.8s)",
                "camera_kling": "Fast sequential cuts of the woman in different styled layers: Look 1 solo with sandals, Look 2 with white knit cardigan, Look 3 with denim jacket, Look 4 with oversized blazer. Smooth snap transitions.",
                "voiceover": "Thứ hai dịu dàng cùng cardigan len mỏng. Thứ ba cá tính khoác thêm denim jacket. Đi hẹn hò thì mix blazer là sang chảnh hết nước chấm. Hoa nhí nhã nhặn không bị sến xíu nào!",
                "text_on_screen": "THỨ 2: NỮ TÍNH | THỨ 3: NĂNG ĐỘNG | THỨ 4: SANG CHẢNH ✨"
            },
            {
                "time": "0:14 - 0:22 (KÊU GỌI LƯU & BẤM GIỎ HÀNG)",
                "panel": "Panel 10 (Nhìn lại qua vai) + Panel 02 (Chỉ tay giỏ hàng)",
                "camera_kling": "The woman twirls gently showing the pleated hemline floating softly, then turns front with an eye wink, pointing down-left. Soft natural glow.",
                "voiceover": "Mấy bà lưu lại ngay để mỗi sáng đỡ phải nghĩ mặc gì nha. Đầm đang có sẵn đủ 3 màu ở góc trái màn hình, bấm vô săn liền!",
                "text_on_screen": "LƯU LẠI NGAY & BẤM GIỎ HÀNG GÓC TRÁI 👇"
            }
        ]
    }

if __name__ == "__main__":
    scripts = [
        get_script_quan_tay_tuyet_mua(),
        get_script_dam_hoa_nhi_7_cach_phoi(),
        get_script_set_cardigan(),
        get_script_quan_short()
    ]
    for s in scripts:
        print("======================================================================")
        print(f"       KỊCH BẢN KOC AI: {s['product']} ({s['duration']})")
        print(f"       Vibe: {s['vibe']} | Giá: {s['price_target']}")
        print("======================================================================")
        for sc in s["scenes"]:
            print(f"\n[{sc['time']}] - {sc['panel']}")
            print(f"   + Text ghim màn hình: \"{sc['text_on_screen']}\"")
            print(f"   + Lời thoại Voiceover: \"{sc['voiceover']}\"")
            print(f"   + Prompt Kling 3.0: {sc['camera_kling']}")
        print("======================================================================\n")
