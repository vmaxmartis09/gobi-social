# VMAX AGENT OPERATING DIRECTIVE: RELENTLESS PROBLEM SOLVING BY DEFAULT
# (MẶC ĐỊNH LÀM ĐẾN CÙNG - KHÔNG CẦN GÕ /GOAL)

## ĐIỀU KHOẢN TỐI CAO: CHẾ ĐỘ MẶC ĐỊNH (DEFAULT RELENTLESS MODE)
- Người dùng **KHÔNG CẦN GÕ `/goal`**. Toàn bộ tác vụ được giao phải được thực hiện với tinh thần và tiêu chuẩn khắt khe nhất của chế độ `/goal`.
- Agent **TUYỆT ĐỐI KHÔNG BỎ CUỘC GIỮA CHỪNG**: Phải tự động thử nghiệm tối thiểu 3-5 giải pháp độc lập khác nhau trước bất kỳ trở ngại nào.
- Chỉ dừng lại khi **MỤC TIÊU CUỐI CÙNG ĐÃ HOÀN TẤT** và có bằng chứng xác minh cụ thể.

## NGUYÊN TẮC BẮT BUỘC (MANDATORY OPERATING DIRECTIVES)

1. **Tự động chuyển đổi chiến lược (Autonomous Pivot Loop):**
   - Khi gặp lỗi phần tử, timeout, anti-bot TikTok/Google, Cloudflare...: Lập tức chuyển đổi từ Direct Selector -> DOM Traversal/JS -> Headed Browser -> CDP Profile Injection. Không bao giờ báo lỗi rồi dừng lại.

2. **Quy chuẩn Browser Automation: Ưu tiên Ego Lite (Mặc định):**
   - Luôn sử dụng trình duyệt **Ego Lite** (`ego-browser` CLI, Node runtime, và skill `ego-browser`). Ego Lite dùng trực tiếp môi trường trình duyệt thật với phiên đăng nhập của người dùng.
   - Thao tác qua Ego Task Spaces (`taskSpace()`), kiểm soát popup OAuth, click tài khoản (ví dụ `dinhthienthoai@gmail.com`) và xác nhận quyền truy cập.


3. **Tự chẩn đoán và khắc phục tự động (Self-Healing):**
   - Chụp ảnh vào `shots/`, kiểm tra DOM, sửa selector và chạy lại script ngay lập tức.
   - Nếu gặp rào cản cần người dùng hỗ trợ (như mã OTP gửi về SMS cá nhân hoặc giải Captcha thủ công): **Giữ nguyên cửa sổ trình duyệt mở trên màn hình**, hướng dẫn rõ ràng, và tự động tiếp quản chạy tiếp 100% các bước còn lại ngay khi người dùng thực hiện xong.

4. **Bằng chứng xác thực kết quả (Proof-of-Work):**
   - Nhiệm vụ chỉ được coi là hoàn thành khi có bằng chứng xác thực rõ ràng: URL profile đích, trạng thái đăng nhập, và ảnh chụp màn hình minh chứng trong thư mục `shots/`.

5. **Giao thức Tự học & Rút kinh nghiệm liên tục (Continuous Learning & Self-Evolution):**
   - Định kỳ nạp, tập trung và sàng lọc tri thức làm KOC AI, quy chuẩn bản quyền, thuật toán TikTok Shop và từ điển cấm vào `configs/koc_ai_knowledge_hub.json` và `configs/koc_learning_memory.json`.
   - Mọi thử nghiệm video và kịch bản đều phải ghi nhận kết quả và tự động tối ưu hóa trọng số prompt qua `src/gobi/services/intelligence/continuous_learning_engine.py` để chu kỳ sau luôn vượt trội hơn chu kỳ trước.

6. **Tuân thủ Kiến trúc & Chống xả rác Codebase (Architecture Governance):**
   - Mọi file mới bắt buộc đặt đúng vị trí theo [`ARCHITECTURE.md`](ARCHITECTURE.md).
   - **CẤM** tạo file rải rác ở root (`/`). Mã logic mới viết vào `src/gobi/`, file nháp/debug tạm thời đặt vào `scratch/`, repo ngoại vi đưa vào `integrations/<repo_name>/`.

7. **Công cụ Dựng & Biên Tập Video Chính: HeyGen HyperFrames (Mặc định bắt buộc):**
   - Từ nay về sau, **HeyGen HyperFrames** (`integrations/hyperframes/`, adapter: `src/gobi/adapters/integrations/hyperframes_adapter.py`, service: `src/gobi/services/media/hyperframes_engine.py`) là **CÔNG CỤ BIÊN TẬP & DỰNG VIDEO CHÍNH THỨC** của toàn bộ hệ sinh thái Gobi Social.
   - Toàn bộ video KOC AI, review thời trang affiliate và social clips được biên tập bằng HTML5/CSS/GSAP HyperFrames tất định, hỗ trợ Safe Zone 9:16, kinetic subtitles, và multi-track audio ducking.


