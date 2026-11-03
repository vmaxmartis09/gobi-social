# 📝 TÓM TẮT CUỘC HỘI THOẠI - SESS-019
> **Tiêu đề phiên:** Xây dựng Dashboard Đen Trắng Tinh Tế (Next.js + Zustand + Kokonut UI) quản lý Job Affiliate Video, Process Status, Tương Tác & Bộ Copy Prompt  
> **Thời gian:** 2026-10-20  
> **Người thực hiện:** Người dùng & AI Assistant (Antigravity)  
> **Phân hệ chính:** `[Dashboard / Frontend] | [Next.js / Zustand / Kokonut UI] | [Job Architecture]`  
> **Trạng thái:** Hoàn thành ✅  

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU CUỘC HỘI THOẠI
* **Yêu cầu người dùng:**
  - Định nghĩa mỗi sản phẩm được cào và tải về đầy đủ (MP4 không logo, MP3, link sản phẩm TikTok Shop) thành một **"Job"**.
  - Xây dựng một **Dashboard phong cách Đen Trắng Tinh Tế (Monochrome Minimalist)** sử dụng stack: **Next.js + Zustand + Kokonut UI**.
  - Bổ sung tính năng **Nhập link TikTok trực tiếp từ giao diện (Fast Link Ingestion)** và **thực hiện quy trình xử lý tự động (Process Execution)** cào toàn bộ dữ liệu, tải video sạch watermark, trích xuất audio, sinh bộ Prompt và đưa ngay vào danh sách quản lý.
  - Tính năng cốt lõi:
    1. Theo dõi **Process Status** của Job (Đã làm video chưa, Đang làm, Đã đăng).
    2. Hiển thị đầy đủ **thông tin tương tác** từ video gốc (Views, Likes, Comments, Shares, ER).
    3. Bộ sinh và **1-click Copy Prompt** (Prompt cho Google Flow/Veo, Kịch bản Voiceover LyLy, Caption TikTok, HyperFrames Spec).
    4. Trình phát video gốc không logo trực tiếp trên giao diện.
    5. Thanh nhập link nhanh tại Hero và Modal nạp Job mới với Stepper xử lý thời gian thực.

---

## ⚙️ 2. CÁC HÀNH ĐỘNG KỸ THUẬT ĐÃ TRIỂN KHAI
1. **Khởi tạo và Cấu hình Dashboard (`tools/dashboard/`):**
   - Đặt đúng phân tầng theo [`ARCHITECTURE.md`](../../ARCHITECTURE.md) (Zero Root Pollution).
   - Cài đặt Next.js 14, React 18, Tailwind CSS, Zustand, Lucide React, Clsx.
   - Thiết lập ngôn ngữ thiết kế Kokonut UI: Dark monochrome theme (`#09090b` zinc-950, deep black, white crisp text, glassmorphic cards `kokonut-card`, subtle border overlays).

2. **Xây dựng Tầng Dữ liệu & State (API + Zustand Store):**
   - Định nghĩa kiểu dữ liệu [`tools/dashboard/lib/types.ts`](../../tools/dashboard/lib/types.ts) (`JobItem`, `JobStatus`, `JobPrompts`, `JobStats`).
   - Tạo Zustand store [`tools/dashboard/store/useJobStore.ts`](../../tools/dashboard/store/useJobStore.ts) quản lý: `jobs`, `selectedJob`, `activeFilter`, `searchQuery`, `copiedKey`, `updateJobStatus()`.
   - Viết API Next.js:
     - `GET /api/jobs`: Tự động quét và đọc toàn bộ thư mục sản phẩm trong `data/products/`, trích xuất thông tin từ `product.json` và `video_clean.json`.
     - `POST /api/jobs/status`: Cập nhật trạng thái Job ("Chưa làm video" ➔ "Đang làm" ➔ "Đã làm video" ➔ "Đã đăng") và lưu thẳng vào file `product.json`.
     - `GET /api/media/[...path]`: Stream video MP4 mượt mà hỗ trợ HTTP Range requests và serve ảnh cover.

3. **Phát triển Giao diện Kokonut UI Đen Trắng:**
   - [`Navbar.tsx`](../../tools/dashboard/components/Navbar.tsx): Header tối giản, thanh tìm kiếm theo tên/tác giả/ID, live badge số lượng jobs.
   - [`StatsOverview.tsx`](../../tools/dashboard/components/StatsOverview.tsx): 4 thẻ chỉ số (Tổng Jobs, Tiến độ làm video %, Reach cào về, Engine đồ họa).
   - [`JobFilterTabs.tsx`](../../tools/dashboard/components/JobFilterTabs.tsx): Tab pills lọc theo trạng thái (`Tất cả`, `Chưa làm video`, `Đang làm`, `Đã làm video`, `Đã đăng`).
   - [`JobCard.tsx`](../../tools/dashboard/components/JobCard.tsx): Card sản phẩm với cover, video badge, dải tương tác (Views, Likes, Cmt, Share), nút đổi trạng thái và nút 1-click **Copy Prompt Flow**.
   - [`JobDetailModal.tsx`](../../tools/dashboard/components/JobDetailModal.tsx): Trình inspector chi tiết gồm Stepper quy trình 4 bước, video player HTML5, bảng tương tác chuyên sâu, và **AI Prompt Suite (4 Tabs: Flow, Lyly Voice, Caption, HyperFrames)** kèm nút Copy Prompt với animation phản hồi.

4. **Khắc phục lỗi trích xuất SnapTik & Cấu hình Dynamic Route:**
   - Phát hiện lỗi khi nạp link: `'SnaptikVideoItem' object has no attribute 'cover'` do truy cập nhầm `meta.cover` thay vì `meta.media.cover_url`.
   - Đã sửa lại [`src/gobi/services/product/job_creator.py`](../../src/gobi/services/product/job_creator.py):
     - Truy cập an toàn qua `meta.media.cover_url or meta.media.dynamic_cover_url`.
     - Tự động sao chép hoặc tải ảnh bìa về lưu cố định tại `data/products/<folder>/cover.jpg`.
   - Đặt `export const dynamic = 'force-dynamic'` tại [`tools/dashboard/app/api/jobs/route.ts`](../../tools/dashboard/app/api/jobs/route.ts) để Dashboard luôn nạp dữ liệu thời gian thực không bị Next.js cache tĩnh.
   - Đã kiểm thử nạp link thật thành công 100%, nâng tổng số Jobs sẵn sàng lên 4 Jobs.

5. **Tích hợp Kiến Trúc Đồng Bộ Thời Gian Thực (Real-Time SSE + File Watcher):**
   - Xây dựng endpoint Server-Sent Events [`tools/dashboard/app/api/jobs/stream/route.ts`](../../tools/dashboard/app/api/jobs/stream/route.ts) sử dụng `ReadableStream` và `fs.watch` trên thư mục `data/products/`.
   - Bất cứ khi nào có Job mới được nạp, video mới được render hoặc file `product.json` thay đổi, server tự động đẩy payload `UPDATE` đến toàn bộ trình duyệt đang mở.
   - Thêm cơ chế tự động kết nối lại (SSE auto-reconnect) và polling fallback an toàn tại Zustand Store [`useJobStore.ts`](../../tools/dashboard/store/useJobStore.ts).
   - Hiển thị huy hiệu `REALTIME LIVE` với radar pulse xanh ngọc và thời gian đồng bộ trên Navbar.

6. **Kiểm thử và Xác thực qua Ego Lite:**
   - Build Next.js thành công 100% (`next build`).
   - Chạy server production tại `http://localhost:3000`.
   - Dùng Ego Lite điều hướng, tương tác, bấm copy prompt và chụp ảnh màn hình xác thực:
     - `shots/dashboard_realtime_live_connected.png`
     - `shots/dashboard_realtime_auto_updated.png`
     - `shots/dashboard_4_jobs_fixed.png`
     - `shots/dashboard_new_job_modal_fixed.png`
     - `shots/dashboard_refined_hero_input.png`
     - `shots/dashboard_create_job_modal.png`

---

## 🏆 3. KẾT QUẢ ĐẠT ĐƯỢC & BẰNG CHỨNG (PROOF-OF-WORK)
* **Ứng dụng Dashboard hoàn thiện:** `tools/dashboard/` (Next.js + Zustand + Kokonut UI).
* **Địa chỉ truy cập trực tiếp:** `http://localhost:3000`.
* **Ảnh chụp màn hình thực tế qua Ego Lite:**
  - Tổng quan Dashboard đen trắng: [`shots/dashboard_overview_kokonut_bw.png`](../../shots/dashboard_overview_kokonut_bw.png)
  - Modal chi tiết, Video Player & Bộ Prompt: [`shots/dashboard_detail_modal_kokonut_bw.png`](../../shots/dashboard_detail_modal_kokonut_bw.png)
  - Phản hồi 1-click Copy Prompt: [`shots/dashboard_prompt_copied_feedback.png`](../../shots/dashboard_prompt_copied_feedback.png)
