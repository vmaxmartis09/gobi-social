"""
TikTok Affiliate Review Script Generator for Dinh Thien Thoai
Tu dong sinh kich ban video review 30s - 45s toi uu ty le nhap gio hang TikTok Shop.
"""

import sys
import os
import json

# Dam bao in duoc tieng Viet va Emoji tren Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def generate_script(product_name: str, price: str = "199k", commission_rate: str = "20%"):
    script = f"""
================================================================================
🎥 KỊCH BẢN TIKTOK AFFILIATE CHUẨN VIRAL: REVIEW ĐỒ NỮ
Kênh: Thiên Thoại Review | Tác giả: Đinh Thiên Thoại
Sản phẩm: {product_name}
Giá tham khảo: {price} | Hoa hồng dự kiến: {commission_rate}
================================================================================

[0:00 - 0:03] 💥 PHẦN 1: HOOK (GIỮ CHÂN NGƯỜI XEM TRONG 3 GIÂY ĐẦU)
  - Khung hình: Thoại cầm sản phẩm trên tay, vẻ mặt ngạc nhiên hoặc tò mò. Text to đùng trên màn hình: "CON TRAI THẨM ĐỒ NỮ?".
  - Lời thoại (Voiceover):
    "Đố các bạn nữ biết, con trai tụi tui nhìn vào chiếc {product_name} này thì thấy điểm gì đầu tiên?"

[0:03 - 0:15] 🔍 PHẦN 2: SOI CHI TIẾT & SỰ THẬT VỀ CHẤT LIỆU (UNBOX CHÂN THẬT)
  - Khung hình: Cận cảnh (Close-up) bàn tay Thoại kéo giãn chất vải, zoom sát đường chỉ may, khóa kéo hoặc các góc cạnh.
  - Lời thoại:
    "Cầm trên tay thì cảm nhận đầu tiên là chất vải khá đầm tay, không hề bị mỏng hay lộ như mấy mẫu rẻ tiền trôi nổi. Đường may mũi chỉ ở nách và viền áo bo rất gọn gàng. Điểm cộng lớn là form chuẩn, không bị nhăn nhúm."

[0:15 - 0:25] 👗 PHẦN 3: LÊN DÁNG & ĐÁNH GIÁ ĐỘ CUỐN HÚT
  - Khung hình: Mẫu nữ mặc thử bước đi hoặc Thoại ướm thử sản phẩm, xoay 360 độ góc nghiêng và góc sau lưng.
  - Lời thoại:
    "Mặc lên thì tôn dáng dã man, tạo cảm giác eo thon và cực kỳ thanh lịch. Các ông mà mua tặng người yêu món này thì đảm bảo nàng chấm 10 điểm tinh tế liền!"

[0:25 - 0:35] 🛒 PHẦN 4: CALL TO ACTION (KÊU GỌI BẤM VÀO GIỎ HÀNG)
  - Khung hình: Thoại chỉ tay xuống góc dưới bên trái màn hình. Mũi tên động nhấp nháy chỉ thẳng vào icon Giỏ hàng màu vàng.
  - Lời thoại:
    "Giá gốc hơn 300k nhưng Thoại đã săn được mã trợ giá chỉ còn {price} ở ngay GIỎ HÀNG GÓC TRÁI màn hình. Số lượng có hạn, chị em bấm vào giỏ hàng săn liền nha!"

--------------------------------------------------------------------------------
📌 HASHTAGS ĐỀ XUẤT ĐỂ LÊN XU HƯỚNG:
#thienthoaireview #reviewdonu #thoitrangnu #gocnhinnamgioi #goidonuchonang #tiktokshopaffiliate #reviewquanao #sandealtiktok
================================================================================
"""
    return script

if __name__ == "__main__":
    prod = sys.argv[1] if len(sys.argv) > 1 else "Váy Body Cổ Vuông Tay Dài Tôn Dáng"
    price = sys.argv[2] if len(sys.argv) > 2 else "249.000 VNĐ"
    print(generate_script(prod, price))
