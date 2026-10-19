# 🧭 GOBI SOCIAL: HANDOVER & CONTINUITY GUIDE
# (SỔ TAY TIẾP QUẢN DỰ ÁN & HƯỚNG DẪN TIẾP TỤC DÀNH CHO AI AGENT / DEVELOPER)

> [!IMPORTANT]
> **DÀNH CHO AI AGENT HOẶC KỸ SƯ MỚI TIẾP QUẢN TRÊN MÁY KHÁC:**
> Đọc kỹ tài liệu này trước khi thực hiện bất kỳ thay đổi nào. Dự án này tuân thủ **Quy chế Vận hành Kiên trì Tuyệt đối (Relentless Execution Protocol)** tại [`AGENTS.md`](AGENTS.md):
> - **Mặc định hành động đến cùng:** Không cần gõ `/goal`. Luôn kiên trì thử 3-5 giải pháp trước khi dừng.
> - **Khóa cứng tính nhất quán:** Nhân vật KOC AI "Gô Bi (Gobi Thúi)" đã được khóa cấu trúc DNA thị giác và giọng nói.
> - **Hệ thống tự học liên tục:** Mọi kết quả sản xuất mới phải được nạp ngược lại vào bộ nhớ tri thức.

---

## 📌 1. BỨC TRANH TOÀN CẢNH DỰ ÁN (PROJECT OVERVIEW)

* **Tên dự án:** Gobi Social (Hệ sinh thái Tự động hóa & Sản xuất KOC AI Đa kênh).
* **Nhân vật KOC AI Master:**
  * **Tên:** Gô Bi (biệt danh: Gobi Thúi).
  * **Định vị:** Nữ KOC thời trang & phong cách sống Gen Z (chiều cao 1m62, nặng 48kg), phong cách tự nhiên, gần gũi, giọng nói miền Bắc/Nam ngọt ngào, chuyên review set đồ thời trang Hàn Quốc, đầm, áo cardigan, quần ống suông.
  * **Kênh chính:** TikTok Shop Affiliate, Facebook Reels, YouTube Shorts.
* **Mục tiêu hệ thống:** Tự động hóa 100% chu trình sản xuất nội dung từ phân tích xu hướng triệu view (Big Data) -> Sinh kịch bản & Prompt camera 36 góc -> Tổng hợp giọng nói cảm xúc -> Dựng video Ken Burns 9:16 chuẩn Safe Zone TikTok -> Quét chính sách vi phạm -> Xuất bản.

---

## 🗺️ 2. BẢN ĐỒ TRI THỨC & NƠI LƯU TRỮ DỮ LIỆU

Mọi thành phần cốt lõi của hệ thống được tổ chức hoàn toàn độc lập và không phụ thuộc đường dẫn cứng:

| Phân hệ | Vị trí tệp | Vai trò & Cách sử dụng |
| :--- | :--- | :--- |
| **Trung tâm Tri thức** | [`configs/koc_ai_knowledge_hub.json`](configs/koc_ai_knowledge_hub.json) | Bộ thông số chuẩn: Safe Zone TikTok (Top 180px, Bottom 320px), từ điển cấm AIGC, ma trận 36 góc quay, hệ số prompt. |
| **Sổ cái Tự học** | [`configs/koc_learning_memory.json`](configs/koc_learning_memory.json) | Bộ nhớ lưu vết bài học từ các chiến dịch video, lịch sử tự động tinh chỉnh trọng số prompt (`auto_tuned_prompt_weights`). |
| **Big Data 104 Video** | [`configs/koc_fashion_bigdata_analytics.json`](configs/koc_fashion_bigdata_analytics.json)<br>[`configs/koc_fashion_bigdata_harvest.json`](configs/koc_fashion_bigdata_harvest.json) | Bản phân tích 104 video thời trang triệu view (15M+ lượt xem): thời lượng hook, nhịp cắt cảnh 1.8s - 2.5s, vị trí nút CTA. |
| **Danh mục Sản phẩm** | [`configs/koc_fashion_korean_products.json`](configs/koc_fashion_korean_products.json) | Cơ sở dữ liệu mẫu áo cardigan, set đồ thời trang kèm kịch bản review mẫu và góc quay tương ứng. |
| **Neo Thị giác Master** | [`MASTER_GOBI_OFFICIAL.jpg`](MASTER_GOBI_OFFICIAL.jpg)<br>[`GOBI_36_PANELS_OFFICIAL.jpg`](GOBI_36_PANELS_OFFICIAL.jpg) | 2 tệp ảnh neo gốc dùng để khóa khuôn mặt và góc quay trong Veo, Midjourney, Flux. |
| **Bộ ảnh 36 Panels** | [`affiliate_tiktok/dataset_koc/`](affiliate_tiktok/dataset_koc/) | 36 panel độc lập cắt từ ma trận gốc, kèm file `manifest.json` sẵn sàng cho huấn luyện Face-ID / LoRA. |
| **Lịch sử Phiên** | [`conversation/SESSION_INDEX.md`](conversation/SESSION_INDEX.md) | Bảng theo dõi 16 phiên làm việc đã hoàn thành (SESS-001 -> SESS-016). |

---

## ⚙️ 3. CÁC ĐỘNG CƠ CỐT LÕI & CÁCH CHẠY (CORE ENGINES)

### 3.1. Động cơ Tự học & Tiến hóa (`core/continuous_learning_engine.py`)
* **Chức năng:** Nạp kết quả video thực tế (views, completion rate, click giỏ hàng), trích xuất bài học và tối ưu trọng số câu lệnh.
* **Cách chạy:**
  ```bash
  python core/continuous_learning_engine.py
  ```

### 3.2. Trình sinh Kịch bản & Prompt 36 Góc (`core/koc_prompt_generator.py`)
* **Chức năng:** Sinh prompt 4K điện ảnh kết hợp neo nhân vật Gô Bi và các góc máy trong ma trận.
* **Cách chạy:**
  ```bash
  python core/koc_prompt_generator.py
  ```

### 3.3. Bộ Quét Vi phạm Chính sách & Vùng An toàn (`tools/video/policy_compliance_checker.py`)
* **Chức năng:** Quét kịch bản, phụ đề trước khi render để loại bỏ từ khóa cấm của TikTok Shop.
* **Cách chạy:**
  ```bash
  python tools/video/policy_compliance_checker.py --script "Set áo cardigan này cực xinh, giá chỉ 139 cành ở giỏ hàng góc trái!"
  ```

### 3.4. Bộ Dựng Video Ken Burns & Phụ đề Safe Zone (`core/render_gobi_boutique_v1.py`)
* **Chức năng:** Dựng video review 9:16 chuẩn 1080x1920, 30fps, Ken Burns motion, ducking âm thanh BGM thông minh.
* **Cách chạy:**
  ```bash
  python core/render_gobi_boutique_v1.py
  ```

### 3.5. Pipeline Nhân bản Giọng nói Thật (`tools/voice/koc_voice_cloner.py`)
* **Chức năng:** Tách giọng nói mẫu từ video/audio ngắn, lọc tạp âm và tạo profile giọng KOC.
* **Cách chạy:**
  ```bash
  python clone_voice_from_video.py --input path/to/sample.mp4 --name koc_gobi
  ```

### 3.6. Giám sát Tự động hóa Trực quan (`live_viewer.html`)
* Mở trực tiếp `live_viewer.html` trong trình duyệt bất kỳ để theo dõi trạng thái automation và hình ảnh thời gian thực.

---

## 📋 4. TRẠNG THÁI HIỆN TẠI & HÀNG ĐỢI CÔNG VIỆC TIẾP THEO (NEXT BACKLOG)

### Những gì đã hoàn thành 100%:
1. [x] Khóa DNA Master KOC Gô Bi & Ma trận 36 góc chụp (`SESS-002`, `SESS-012`).
2. [x] Khai phá Big Data 104 video triệu view thời trang (`SESS-007`, `SESS-011`).
3. [x] Xây dựng Video Engine & AI Concat Auto-Editor (`SESS-004`, `SESS-011`).
4. [x] Pipeline Voice Clone tiếng Việt và Edge-TTS Hoài My (`SESS-003`, `SESS-015`).
5. [x] Sản xuất video review Áo Cardigan 45s mở miệng nói chuẩn Safe Zone (`SESS-016`).
6. [x] Đóng gói toàn bộ tri thức và đẩy lên kho mã nguồn `gobi-social`.

### Nhiệm vụ tiếp tục ưu tiên (Next Actions for Agent/Developer):
1. **Mở rộng Series Video Review Sản phẩm Mới:**
   - Sử dụng danh mục trong [`configs/koc_fashion_korean_products.json`](configs/koc_fashion_korean_products.json) để sản xuất tiếp các video cho:
     - Set đầm lụa cổ vuông kiểu Pháp.
     - Áo croptop dệt kim cổ tim.
     - Quần ống suông cạp cao tôn dáng.
2. **Cập nhật Vòng lặp Tự học (Continuous Learning):**
   - Khi có thêm số liệu tương tác từ các kênh TikTok thực tế, chạy `core/continuous_learning_engine.py` để nạp các trường hợp video thành công / thất bại vào `configs/koc_learning_memory.json`.
3. **Mở rộng Đa kênh qua Agent Reach:**
   - Tận dụng phân hệ [`tools/reach/`](tools/reach/) để cào và phân tích thêm dữ liệu từ Facebook Reels, Tiểu Hồng Thư (XHS) và YouTube Shorts.

---

## 💻 5. THIẾT LẬP MÔI TRƯỜNG TRÊN MÁY MỚI (ENVIRONMENT SETUP)

```bash
# 1. Clone repository
git clone git@github.com:vmaxmartis09/gobi-social.git
cd gobi-social

# 2. Tạo môi trường ảo Python
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Trên Linux/Mac:
source .venv/bin/activate

# 3. Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# 4. Thiết lập biến môi trường
copy .env.example .env
# Điền các API keys cần thiết (Gemini / Groq / OpenAI) vào .env
```

---

## ⚡ 6. QUY TẮC BẮT BUỘC DÀNH CHO AI AGENT
- **Luôn đọc `AGENTS.md`** để duy trì tư duy "Làm việc đến cùng" (Relentless Execution).
- **Không bao giờ dùng đường dẫn tuyệt đối dạng `C:\Users\...`** trong mã nguồn mới; luôn dùng `os.path.dirname(os.path.abspath(__file__))` hoặc biến môi trường.
- **Sau mỗi phiên làm việc mới:** Tạo log theo mẫu [`conversation/TEMPLATE_CONVERSATION_LOG.md`](conversation/TEMPLATE_CONVERSATION_LOG.md) và cập nhật một dòng mới vào [`conversation/SESSION_INDEX.md`](conversation/SESSION_INDEX.md).
