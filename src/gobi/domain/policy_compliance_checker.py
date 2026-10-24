"""
VMAX Policy & Blacklist Compliance Checker for TikTok / Reels / Shorts
Kiem tra kịch bản, text caption, tu ngu nhay cam, tu cam ket tuyet doi,
dieu huong ngoai san, vi pham ban quyen va de xuat tu thay the an toan.
"""

import sys
import re
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Danh sach tu cam va tu nhay cam theo 5 nhom chinh
BLACKLIST_DICTIONARY = {
    "dieu_huong_ngoai_san": {
        "patterns": [
            r"\bfacebook\b", r"\bshopee\b", r"\blazada\b", r"\btiki\b", r"\bsendo\b",
            r"\bzalo\b", r"\binstagram\b", r"\byoutube\b", r"\blink bio\b", r"\bwebsite\b",
            r"\bweb\b", r"\bqua phở bò\b", r"\bin tư\b", r"\bnhắn riêng\b"
        ],
        "risk": "CAO (Bóp reach / Giam 200 view / Mất giỏ hàng)",
        "recommendation": "Thay thế bằng: 'ghé giỏ hàng góc trái', 'tóp tóp', 'nền tảng màu cam/xanh', 'nhấn vào đây'"
    },
    "cam_ket_tuyet_doi": {
        "patterns": [
            r"\bcam kết\b", r"\b100%\b", r"\btuyệt đối\b", r"\bkhỏi hẳn\b", r"\bvĩnh viễn\b",
            r"\btốt nhất\b", r"\bsố 1\b", r"\bduy nhất\b", r"\bhoàn tiền\b", r"\bvô địch\b",
            r"\bsiêu tốc\b", r"\btận gốc\b"
        ],
        "risk": "CAO (Lỗi quảng cáo sai sự thật / Đánh gậy Creator)",
        "recommendation": "Thay thế bằng: 'hỗ trợ cải thiện', 'giúp giảm', 'được yêu thích hàng đầu', 'rất đáng trải nghiệm'"
    },
    "y_te_my_pham_nhay_cam": {
        "patterns": [
            r"\bthuốc\b", r"\bchữa bệnh\b", r"\bđặc trị\b", r"\btriệt lông\b",
            r"\bgiảm cân cấp tốc\b", r"\btăng cân cấp tốc\b", r"\bthần dược\b",
            r"\bbác sĩ khuyên dùng\b", r"\btrắng da cấp tốc\b", r"\btế bào gốc\b"
        ],
        "risk": "CỰC CAO (Khóa giỏ hàng / Tắt sản phẩm / Xóa video)",
        "recommendation": "Thay thế bằng: 'chăm sóc da', 'hỗ trợ vóc dáng', 'mỹ phẩm lành tính', 'giúp da sáng mịn tự nhiên'"
    },
    "thuong_hieu_lon_chua_uy_quyen": {
        "patterns": [
            r"\bnike\b", r"\badidas\b", r"\bgucci\b", r"\bchanel\b", r"\bdior\b",
            r"\blouis vuitton\b", r"\blv\b", r"\bzara\b", r"\brolex\b", r"\bapple\b", r"\biphone\b"
        ],
        "risk": "CAO (Vi phạm sở hữu trí tuệ / Quét bản quyền tự động)",
        "recommendation": "Thay thế bằng: 'hàng hiệu cao cấp', 'thiết kế phong cách retro', 'giày thể thao thời trang'"
    },
    "thong_tin_ca_nhan_giao_dich": {
        "patterns": [
            r"\bsố điện thoại\b", r"\bsđt\b", r"\bhotline\b", r"\bstk\b", r"\bngân hàng\b",
            r"\bchuyển khoản\b", r"\b0\d{9,10}\b"
        ],
        "risk": "CỰC CAO (Vi phạm quyền riêng tư / Nghi ngờ lừa đảo)",
        "recommendation": "Chỉ hướng dẫn thanh toán trực tiếp qua cổng TikTok Shop / Giỏ hàng an toàn"
    }
}

SAFE_ZONE_SPEC = {
    "resolution": "1080x1920",
    "aspect_ratio": "9:16",
    "safe_margins": {
        "top": "Chừa 150px - 280px (Tránh tab Following/For You, camera đục lỗ)",
        "bottom": "Chừa 320px - 650px (Tránh thanh caption dài, tên KOC, icon giỏ hàng TikTok Shop)",
        "left": "Chừa 50px - 100px",
        "right": "Chừa 120px - 180px (Tránh cột icon Tim, Comment, Save, Share, đĩa nhạc)"
    },
    "sweet_spot": "Khu vực trung tâm đắc địa: 900x1400px (Center-Middle)"
}

def scan_text_compliance(text: str):
    violations = []
    text_lower = text.lower()
    
    for category, data in BLACKLIST_DICTIONARY.items():
        matched_words = []
        for pat in data["patterns"]:
            matches = re.findall(pat, text_lower)
            if matches:
                matched_words.extend(matches)
        if matched_words:
            violations.append({
                "category": category,
                "detected": list(set(matched_words)),
                "risk_level": data["risk"],
                "fix_suggestion": data["recommendation"]
            })
            
    is_clean = len(violations) == 0
    return {
        "is_compliant": is_clean,
        "total_violations": len(violations),
        "details": violations,
        "safe_zone_rules": SAFE_ZONE_SPEC
    }

class PolicyComplianceChecker:
    """OOP wrapper for policy compliance checking."""
    @staticmethod
    def scan(text: str) -> dict:
        return scan_text_compliance(text)
    
    @staticmethod
    def check_compliance(text: str) -> dict:
        return scan_text_compliance(text)

if __name__ == "__main__":

    sample_script = (
        "Cam kết 100% áo Cardigan này là số 1 thị trường. Các bạn qua Zalo hoặc Facebook nhắn tin cho Vi, "
        "hoặc chuyển khoản vào stk để Vi gửi mẫu Nike xịn nhé!"
    )
    print("======================================================================")
    print("        VMAX POLICY & BLACKLIST COMPLIANCE SCANNER                     ")
    print("======================================================================")
    print(f"[*] Văn bản kiểm tra:\n\"{sample_script}\"\n")
    report = scan_text_compliance(sample_script)
    print(f"[*] Trạng thái tuân thủ: {'HOÀN HẢO' if report['is_compliant'] else 'CẢNH BÁO VI PHẠM'}")
    print(f"[*] Tổng số vi phạm phát hiện: {report['total_violations']}\n")
    for v in report["details"]:
        print(f"[-] Nhóm: {v['category'].upper()}")
        print(f"    Từ khóa dính bẫy: {v['detected']}")
        print(f"    Mức độ rủi ro:   {v['risk_level']}")
        print(f"    Khuyến nghị sửa:  {v['fix_suggestion']}\n")
    print("======================================================================")
