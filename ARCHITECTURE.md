# 🏛️ TIÊU CHUẨN KIẾN TRÚC & QUY TẮC CẤU TRÚC THƯ MỤC GOBI SOCIAL
# (GOBI SOCIAL SYSTEM ARCHITECTURE & REPOSITORY GOVERNANCE STANDARDS)

> [!CRITICAL]
> **ĐIỀU KHOẢN BẮT BUỘC ĐỐI VỚI MỌI DEVELOPER VÀ AI AGENT:**
> 1. **CHÍNH SÁCH THƯ MỤC GỐC KHÔNG RÁC (ZERO-ROOT-POLLUTION):** Tuyệt đối **KHÔNG ĐƯỢC TẠO** bất kỳ file `.py`, `.mjs`, `.txt`, `.json`, `.bat`, `.sh` hay file media tự do nào ở thư mục gốc (`/`). Thư mục gốc chỉ chứa các file meta của repository (`README.md`, `pyproject.toml`, `requirements.txt`, tài liệu chỉ dẫn Agent).
> 2. **QUY TẮC THIẾT KẾ ĐÚNG TẦNG (SEPARATION OF CONCERNS):** Mọi logic mới, tính năng mới hoặc repo mới được thêm vào hệ thống bắt buộc phải đặt đúng phân tầng theo cây quyết định trong tài liệu này.

---

## 🗺️ 1. CÂY THƯ MỤC CHUẨN MỰC (STANDARD DIRECTORY LAYOUT)

Hệ thống tuân thủ mô hình **Modular Monolith** kết hợp **Clean Architecture (Ports & Adapters)**. Cấu trúc chuẩn mực duy nhất của dự án như sau:

```
gobi-social/
├── pyproject.toml                     # Cấu hình đóng gói Python package chuẩn PEP 621
├── requirements.txt                   # Danh sách dependencies cốt lõi
├── README.md                          # Giới thiệu & Quickstart
├── ARCHITECTURE.md                    # [TÀI LIỆU NÀY] Tiêu chuẩn kiến trúc & quy tắc đặt file
├── CONTINUITY.md                      # Nhật ký bàn giao kỹ thuật & tiến độ
├── AGENTS.md / GEMINI.md / CLAUDE.md  # Chỉ dẫn hành vi cho AI Agent
│
├── src/                               # 📦 SOURCE CODE DUY NHẤT CỦA HỆ THỐNG
│   └── gobi/                          # Package namespace chính (import gobi.*)
│       ├── __init__.py
│       │
│       ├── domain/                    # [TẦNG 1: DOMAIN] Thực thể, luật nghiệp vụ, schemas
│       │   ├── __init__.py
│       │   ├── models.py              # Pydantic models (VideoSpec, AudioTrack, ProductInfo)
│       │   ├── persona.py             # Định nghĩa DNA nhân vật KOC Gô Bi, 36 góc quay
│       │   └── policies.py            # Luật TikTok Safe Zone, từ điển cấm AIGC
│       │
│       ├── services/                  # [TẦNG 2: SERVICES] Nghiệp vụ lõi (Application Core)
│       │   ├── __init__.py
│       │   ├── media/                 # Xử lý video, Ken Burns, auto-concat, subtitles
│       │   │   ├── hyperframes_engine.py # [CHÍNH THỨC] Engine dựng video HyperFrames HTML5/GSAP
│       │   │   ├── video_engine.py    # Engine dựng video FFmpeg / Concat (Legacy fallback)
│       │   │   ├── ai_concat_auto_editor.py # Concat theo nhịp triệu view (Legacy)
│       │   │   └── snaptik_service.py # Dịch vụ tải video TikTok sạch watermark
│       │   ├── voice/                 # Xử lý âm thanh & tổng hợp giọng nói
│       │   │   ├── scripts/voice/voice_studio.py    # Quản lý Voice Vault & synthesizer
│       │   │   ├── tts_engine.py      # Edge-TTS / gTTS engine
│       │   │   └── audio_master.py    # Master âm lượng, lọc tạp âm, ducking nhạc
│       │   ├── prompt/                # Sinh kịch bản & prompt camera
│       │   │   ├── script_writer.py   # Tạo kịch bản review thời trang KOC
│       │   │   └── camera_matrix.py   # Ghép neo nhân vật và góc máy 36 panels
│       │   └── intelligence/          # Học máy & phân tích xu hướng
│       │       ├── learning_engine.py # Động cơ tự học liên tục (Continuous Learning)
│       │       └── trend_analyzer.py  # Phân tích Big Data video triệu view
│       │
│       ├── adapters/                  # [TẦNG 3: ADAPTERS] Tương tác ngoại vi & Driver bên thứ 3
│       │   ├── __init__.py
│       │   ├── browser/               # Trình duyệt tự động hóa chung
│       │   │   ├── ego_client.py      # Giao tiếp Ego Task Spaces & session thật
│       │   │   └── stealth.py         # Cờ chống bot detection, human-like delays
│       │   ├── platforms/             # Adapter riêng cho từng nền tảng
│       │   │   ├── tiktok/            # TikTok bot, Auth, Session, Publisher
│       │   │   ├── facebook/          # Facebook Reels scraper & parser
│       │   │   └── flow_ai/           # Google Flow Studio / Veo / EverAI driver
│       │   └── scrapers/              # Scraper cào dữ liệu chuyên sâu
│       │       ├── tiktok_miner.py    # Cào video xu hướng theo hashtag/từ khóa
│       │       └── social_extractor.py# Tách audio, transcripts, video sạch watermark
│       │
│       └── cli/                       # [TẦNG 4: CLI] Điểm vào dòng lệnh duy nhất (Unified CLI)
│           ├── __init__.py
│           ├── main.py                # Router chính: `python -m gobi <subcommand>`
│           ├── cmd_video.py           # gobi video render | concat | sub
│           ├── cmd_voice.py           # gobi voice synth | clone | vault
│           ├── cmd_tiktok.py          # gobi tiktok publish | login | status
│           └── cmd_scrape.py          # gobi scrape tiktok | fb
│
├── configs/                           # ⚙️ CẤU HÌNH HỆ THỐNG (JSON / YAML)
│   ├── koc_ai_knowledge_hub.json      # Tri thức chuẩn: Safe Zone, từ điển cấm, hệ số
│   ├── koc_learning_memory.json       # Sổ cái học tập: trọng số prompt tối ưu
│   ├── products/                      # Danh mục sản phẩm (Cardigan, Đầm, Croptop)
│   └── pipeline_settings.json         # Cấu hình render video, độ phân giải, bitrates
│
├── assets/                            # 🎨 ASSETS VÀNG & TÀI NGUYÊN TĨNH BẤT BIẾN
│   ├── koc_dna/                       # Ảnh neo thị giác gốc (Master DNA)
│   │   ├── assets/koc_dna/MASTER_GOBI_OFFICIAL.jpg
│   │   └── assets/koc_dna/GOBI_36_PANELS_OFFICIAL.jpg
│   ├── datasets/                      # Dữ liệu ảnh cắt lát phục vụ Face-ID / LoRA
│   │   └── koc_36_panels/             # 36 panel độc lập đã crop + manifest.json
│   ├── voice_vault/                   # Kho giọng mẫu chuẩn đã lọc tạp âm
│   ├── templates/                     # Video intro/outro, nhạc nền BGM, font chữ
│   └── mockups/                       # Ảnh sản phẩm thời trang mẫu
│
├── data/                              # 📊 DỮ LIỆU THU THẬP & CÀO VỀ (KHÔNG CHỨA CODE)
│   ├── raw/                           # Dữ liệu cào thô (JSON, TXT, Subtitle dumps)
│   │   ├── tiktok/
│   │   ├── facebook/
│   │   └── subtitles/
│   └── analytics/                     # Dữ liệu sau xử lý / Báo cáo Big Data
│       ├── koc_fashion_bigdata_harvest.json
│       └── koc_fashion_bigdata_analytics.json
│
├── output/                            # 🚀 SẢN PHẨM RENDER HOÀN THIỆN (GITIGNORED)
│   ├── videos/                        # Video mp4 xuất bản
│   ├── audio/                         # File audio, voiceover mp3/wav
│   └── logs/                          # Screenshots, run logs
│
├── integrations/                      # 🔌 SUB-PROJECTS & REPO BÊN THỨ 3 (ISOLATED)
│   ├── hyperframes/                   # HeyGen HyperFrames - Engine dựng video HTML5/GSAP chính
│   ├── OmniVoice/                     # Framework nhân bản giọng nói thuần Việt
│   ├── job_search/                    # ai-job-search framework
│   └── agent_reach/                   # Agent-Reach crawler framework
│
├── scripts/                           # 🛠️ SCRIPT VẬN HÀNH & BẢO TRÌ (RUNBOOKS)
│   ├── setup_environment.sh           # Cài đặt môi trường máy mới
│   ├── clean_workspace.py             # Dọn dẹp cache / temporary files
│   └── legacy_windows/                # Script .bat cũ phục vụ tham chiếu
│
├── tests/                             # 🧪 KIỂM THỬ TỰ ĐỘNG
│   ├── unit/                          # Unit tests kiểm tra hàm & policies
│   ├── integration/                   # Integration tests kiểm tra pipeline video/voice
│   └── e2e/                           # End-to-End tests kiểm tra tự động hóa trình duyệt
│
├── scratch/                           # 🔬 VÙNG ĐÀO BỚI / THỬ NGHIỆM TẠM THỜI (DEV SANDBOX)
│   │                                  # (Mọi file debug, inspect DOM, test click bắt buộc ở đây)
│   └── debug_logs/
│
└── docs/                              # 📚 TÀI LIỆU DỰ ÁN
    ├── architecture/                  # Sơ đồ thiết kế hệ thống
    └── sessions/                      # Nhật ký các phiên làm việc (SESS-001 -> SESS-xxx)
```

---

## 🧭 2. CÂY QUYẾT ĐỊNH SINH FILE MỚI (NEW FILE PLACEMENT DECISION TREE)

Mỗi khi bạn (hoặc AI Agent) chuẩn bị tạo một file mới, hãy tra cứu bảng quy chuẩn sau trước khi đặt bút viết:

| Bản chất của File bạn muốn tạo | Vị trí BẮT BUỘC | Ví dụ file cụ thể | Điều cấm |
| :--- | :--- | :--- | :--- |
| **Logic render video, auto-cut, subtitle** | `src/gobi/services/media/` | `video_engine.py`, `smart_cropper.py` | CẤM tạo file `render_*.py` ở root |
| **Xử lý âm thanh, voice clone, TTS** | `src/gobi/services/voice/` | `f5_tts_adapter.py`, `audio_ducking.py` | CẤM tạo `gen_voice.py` ở root |
| **Sinh kịch bản, prompt camera** | `src/gobi/services/prompt/` | `script_generator.py`, `lens_calculator.py` | CẤM tạo `prompt_*.py` ở root |
| **Học máy, tự tối ưu prompt, analytics**| `src/gobi/services/intelligence/` | `learning_engine.py`, `retention_model.py` | CẤM tạo file phân tích ở root |
| **Điều khiển trình duyệt (Ego/Playwright)**| `src/gobi/adapters/browser/` | `ego_client.py`, `stealth_context.py` | CẤM vứt file `.mjs` tự do ở root |
| **Tương tác TikTok / Facebook / Google** | `src/gobi/adapters/platforms/<platform>/` | `tiktok_uploader.py`, `flow_client.py` | CẤM gom thành thư mục rác như `affiliate_tiktok/` |
| **Cào dữ liệu từ web / API mạng xã hội** | `src/gobi/adapters/scrapers/` | `douyin_miner.py`, `reels_downloader.py` | CẤM tạo `scrape_*.py` ở root |
| **Lệnh chạy dòng lệnh mới (CLI)** | `src/gobi/cli/` | `cmd_youtube.py`, `cmd_analytics.py` | Mọi lệnh phải tích hợp vào `main.py` |
| **Data model, Pydantic schema, Enums** | `src/gobi/domain/` | `models.py`, `policies.py` | Không định nghĩa schema rải rác |
| **File cấu hình tham số hệ thống** | `configs/` | `configs/products/summer_collection.json` | CẤM vứt file config JSON ở root |
| **Tài nguyên ảnh gốc, giọng mẫu, BGM** | `assets/<subfolder>/` | `assets/voice_vault/gobi_sweet.wav` | CẤM để ảnh `.jpg` ở root |
| **Dữ liệu thô cào về (JSON, TXT dump)** | `data/raw/<source>/` | `data/raw/tiktok/trending_cardigans.json` | CẤM vứt dump data ra root |
| **Script debug, inspect DOM, test tạm** | `scratch/` | `scratch/inspect_modal_popup.py` | **BẮT BUỘC NẰM TRONG `scratch/`** |
| **Kiểm thử tự động chính thức (Unit/E2E)**| `tests/<type>/` | `tests/unit/test_safe_zone.py` | CẤM tạo `test_*.py` ở root |
| **Script cài đặt môi trường, bảo trì máy**| `scripts/` | `scripts/setup_mac.sh`, `scripts/prune_cache.py` | Không tạo `.bat`/`.sh` ở root |
| **Nhúng 1 repo bên thứ 3 từ GitHub về** | `integrations/<repo_name>/` | `integrations/ai_voice_clone/` | CẤM clone repo ngoài thẳng vào `tools/` |

---

## 🔌 3. QUY CHUẨN TÍCH HỢP REPO NGOẠI VI (THIRD-PARTY REPO INGESTION)

Khi cần tích hợp một thư viện, framework hoặc repository mã nguồn mở từ bên ngoài (ví dụ: một scraper mới, một engine tạo phụ đề, một tool AI):

1. **Vị trí lưu trữ độc quyền:**
   - Toàn bộ repo được clone hoặc nhúng phải nằm trong `integrations/<tên_dự_án>/`.
   - Tuyệt đối không clone bừa bãi vào root, vào `tools/`, hay vào `src/`.
2. **Quy tắc tạo Adapter Bridge:**
   - Mã nguồn nội bộ của `gobi-social` **KHÔNG BAO GIỜ** gọi trực tiếp các file nội bộ sâu trong `integrations/`.
   - Bắt buộc tạo một Adapter mỏng tại `src/gobi/adapters/integrations/<tên_dự_án>_adapter.py` để đóng gói lời gọi.
   - Khi repo ngoại vi thay đổi hoặc được thay thế bằng tool khác, chỉ cần cập nhật Adapter này mà không làm ảnh hưởng toàn bộ hệ thống.
3. **Quản lý Dependencies:**
   - Nếu repo ngoại vi có `requirements.txt` riêng xung đột với hệ thống chính, phải thiết lập runner chạy cô lập qua subprocess hoặc micro-virtualenv, không cài đè làm hỏng môi trường chính của `gobi-social`.
4. **Tài liệu hóa tích hợp:**
   - Mỗi repo trong `integrations/<tên_dự_án>/` phải có file `INTEGRATION_NOTE.md` tóm tắt: Nguồn gốc repo, mục đích sử dụng, file wrapper adapter tương ứng.

---

## 🔬 4. NGUYÊN TẮC QUẢN LÝ VÙNG ĐÀO BỚI (SCRATCHPAD & DEBUG PROTOCOL)

Trong quá trình AI Agent thực hiện tôn chỉ **Relentless Execution (Làm đến cùng)**:
- Agent thường xuyên cần viết script kiểm tra vi mô (micro-testing): inspect cây DOM, tìm tọa độ button, bắt request network, test một đoạn prompt nhỏ.
- **QUY ĐỊNH SẮT ĐÁ:**
  - Tất cả các file này **PHẢI ĐƯỢC TẠO TRONG THƯ MỤC `scratch/`** (ví dụ: `scratch/inspect_button.py`, `scratch/test_click.mjs`).
  - Thư mục `scratch/` được coi là vùng nháp (sandbox). Mã trong `scratch/` không được phép import ngược vào `src/`.
  - Định kỳ sau mỗi milestone, các script thành công trong `scratch/` sẽ được trích xuất logic chuẩn mực để đưa vào `src/gobi/adapters/` hoặc `tests/`, các file thừa sẽ được dọn dẹp an toàn.

---

## 💻 5. QUY CHUẨN GIAO DIỆN DÒNG LỆNH (UNIFIED CLI STANDARD)

Thay vì chạy các script rời rạc, mọi tính năng của hệ thống được gọi qua **Gobi CLI**:

```bash
# Cú pháp mẫu
python -m gobi <subcommand> <action> [flags]
```

### Các nhóm lệnh chính:
- **`gobi video`**: Render video review, ghép clip Ken Burns, căn lề phụ đề Safe Zone.
- **`gobi voice`**: Sinh giọng đọc tiếng Việt, lọc tạp âm, nhân bản giọng KOC, quản lý Voice Vault.
- **`gobi prompt`**: Sinh prompt ma trận 36 góc quay, kết hợp neo DNA Master.
- **`gobi policy`**: Quét kịch bản/video kiểm tra vi phạm từ cấm TikTok Shop và chuẩn AIGC.
- **`gobi scrape`**: Cào video triệu view, khai thác Big Data thời trang từ TikTok/Facebook.
- **`gobi tiktok`**: Đăng tải video, quản lý session đăng nhập, cập nhật profile KOC.
- **`gobi learn`**: Ghi nhận số liệu thực tế của video và tự động tối ưu hóa trọng số prompt.

---

## 🛡️ 6. CAM KẾT CHẤT LƯỢNG SENIOR BACKEND (DEFINITION OF DONE)

Một tính năng hoặc một module mới chỉ được coi là hoàn tất khi:
1. **Đúng vị trí:** Đặt đúng thư mục theo bảng quy chuẩn ở Mục 2.
2. **Không rác ở root:** Không sinh thêm bất kỳ file tạm nào ngoài thư mục gốc.
3. **Có Schema rõ ràng:** Các cấu trúc dữ liệu truyền qua lại đều có Pydantic model trong `src/gobi/domain/`.
4. **Không phụ thuộc đường dẫn cứng (No Hardcoded Paths):** Sử dụng `pathlib.Path` hoặc biến môi trường `PROJECT_ROOT`, tuyệt đối không hardcode đường dẫn ổ đĩa tuyệt đối.
5. **Có lệnh CLI tương ứng:** Tính năng có thể kích hoạt qua lệnh trong `src/gobi/cli/`.
6. **Được ghi nhận nhật ký:** Cập nhật tóm tắt vào `CONTINUITY.md` và `conversation/SESSION_INDEX.md`.
