# 🛠️ TOPIC 05: EXTENDED TOOLS (JOB SEARCH & MULTI-CHANNEL REACH)
> **Tổng hợp chuyên đề:** Các phân hệ công cụ mở rộng tích hợp trong dự án VMAX: Săn việc làm tự động (Job Hunter) và Tiếp cận đa kênh (Agent Reach).

---

## 1. MỤC ĐÍCH & Ý NGHĨA TRONG BỨC TRANH VMAX
* Bên cạnh trọng tâm video marketing, VMAX sở hữu hạ tầng mở rộng mạnh mẽ cho việc tự động hóa các tác vụ nghiên cứu nghề nghiệp và phân phối thông tin mạng xã hội diện rộng.
* Thể hiện tính linh hoạt của kiến trúc Agentic: Dùng chung hạt nhân tự động hóa trình duyệt và trích xuất dữ liệu để phục vụ nhiều mục tiêu khác nhau.

---

## 2. PHÂN HỆ JOB SEARCH (`tools/job_search/`)
* **Chức năng:** Tự động tìm kiếm vị trí tuyển dụng phù hợp trên nhiều cổng (LinkedIn, Jobindex, Jobnet, Jobdanmark...).
* **Tailoring CV & Cover Letter:** Tự động đối chiếu yêu cầu công việc (Job Description) và chỉnh sửa file CV HTML/PDF tương thích tối đa với bộ lọc ATS.
* **Tự động nộp đơn:** Hỗ trợ điền form ứng tuyển và theo dõi kết quả nộp đơn qua Google Sheets / Notion / Gmail sync.
* **File quản lý:**
  * [`tools/job_search/job_hunter.py`](../../tools/job_search/job_hunter.py)
  * [`tools/job_search/job_pipeline.py`](../../tools/job_search/job_pipeline.py)
  * [`tools/job_search/salary_lookup.py`](../../tools/job_search/salary_lookup.py)

---

## 3. PHÂN HỆ AGENT REACH (`tools/reach/`)
* **Chức năng:** Kết nối và đăng bài tự động trên nhiều nền tảng mạng xã hội khác nhau (Twitter/X, Reddit, Xiaohongshu, LinkedIn).
* **Quản lý Cookie & Session:** Xuất nhập cookie an toàn để không cần đăng nhập lại nhiều lần.
* **Thư mục:** [`tools/reach/agent-reach/`](../../tools/reach/agent-reach)

---

## 4. CÁC FILE LIÊN QUAN CHÍNH
* [`tools/job_search/README.md`](../../tools/job_search/README.md)
* [`tools/reach/agent-reach/README.md`](../../tools/reach/agent-reach/README.md)
