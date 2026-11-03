# 🧠 TOPIC 04: BIG DATA, KNOWLEDGE HUB & CONTINUOUS LEARNING
> **Tổng hợp chuyên đề:** Khai phá Big Data sản phẩm trending, quét tuân thủ chính sách AIGC TikTok, và vòng lặp tự học tiến hóa liên tục của Agent.

---

## 1. MỤC ĐÍCH & Ý NGHĨA TRONG BỨC TRANH VMAX
* Không sản xuất video theo cảm tính: Mọi kịch bản và sản phẩm đều xuất phát từ phân tích dữ liệu lớn (sản phẩm có lượng bán cao, lượt xem khủng, tỷ lệ chuyển đổi tốt).
* Bảo vệ an toàn tuyệt đối cho kênh TikTok Affiliate: Chủ động loại bỏ các từ khóa cấm kỵ (từ khóa cam kết 100%, từ ngữ lừa đảo, nhãn hiệu bản quyền chưa đăng ký).
* Tự động hoàn thiện kỹ năng sau mỗi chiến dịch: Hệ thống ghi nhớ các video thành công (viral) và video thất bại (flop) để tinh chỉnh trọng số prompt cho các lần tạo tiếp theo.

---

## 2. CƠ CHẾ HOẠT ĐỘNG

### 2.1. Cào & Phân tích Big Data thị trường
* **Bộ cào dữ liệu:** [`scripts/tiktok/mass_tiktok_fashion_miner.py`](../../scripts/tiktok/mass_tiktok_fashion_miner.py), [`scripts/tiktok/scrape_tiktok_fashion.py`](../../scripts/tiktok/scrape_tiktok_fashion.py).
* **Kho dữ liệu khai phá:**
  * [`configs/koc_fashion_bigdata_harvest.json`](../../configs/koc_fashion_bigdata_harvest.json) (~730KB dữ liệu sản phẩm, lượt tim, giá thành).
  * [`configs/koc_fashion_bigdata_analytics.json`](../../configs/koc_fashion_bigdata_analytics.json).
* **Phân tích dữ liệu:** [`src/gobi/services/intelligence/analyze_bigdata_harvest.py`](../../src/gobi/services/intelligence/analyze_bigdata_harvest.py).

### 2.2. Kiểm tra tuân thủ chính sách (Policy Compliance Checker)
* File mã nguồn: [`src/gobi/domain/policy_compliance_checker.py`](../../src/gobi/domain/policy_compliance_checker.py).
* Kho từ khóa cấm & Quy chuẩn nội dung: [`configs/koc_ai_knowledge_hub.json`](../../configs/koc_ai_knowledge_hub.json).
* Tự động quét kịch bản trước khi đưa vào phòng thu âm (TTS) để lọc sạch các từ có thể khiến video bị bóp tương tác hoặc cấm kênh.

### 2.3. Động cơ tự học liên tục (Continuous Learning Engine)
* File mã nguồn: [`src/gobi/services/intelligence/continuous_learning_engine.py`](../../src/gobi/services/intelligence/continuous_learning_engine.py).
* Sổ cái lưu bài học: [`configs/koc_learning_memory.json`](../../configs/koc_learning_memory.json).
* Tự động cập nhật:
  * Trọng số biểu cảm, ánh sáng, góc quay camera (`auto_tuned_prompt_weights`).
  * Danh sách bài học kinh nghiệm lịch sử (`historical_lessons`).

---

## 3. CÁC FILE LIÊN QUAN CHÍNH
* [`src/gobi/services/intelligence/continuous_learning_engine.py`](../../src/gobi/services/intelligence/continuous_learning_engine.py)
* [`configs/koc_ai_knowledge_hub.json`](../../configs/koc_ai_knowledge_hub.json)
* [`configs/koc_learning_memory.json`](../../configs/koc_learning_memory.json)
* [`src/gobi/domain/policy_compliance_checker.py`](../../src/gobi/domain/policy_compliance_checker.py)
