"""
Job Pipeline Tracker & Application Dashboard
Monitors job criteria (Quy Nhon, Office hours, Mon-Fri, 8-10M) and tracks application pipeline.
"""

import json
import os
from datetime import datetime

class JobPipeline:
    def __init__(self, data_file="configs/job_pipeline.json"):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.pipeline = json.load(f)
            except Exception:
                self.pipeline = self.init_default_pipeline()
        else:
            self.pipeline = self.init_default_pipeline()
            self.save_data()

    def init_default_pipeline(self):
        return {
            "candidate": "Nguyen Thi Xuan Huong",
            "criteria": {
                "location": "Quy Nhơn, Bình Định",
                "schedule": "Giờ hành chính (Nghỉ Thứ 7, Chủ nhật)",
                "salary_range": "8.000.000 - 10.000.000 VNĐ",
                "benefits": "Đóng BHXH đầy đủ, thưởng lễ tết"
            },
            "jobs": [
                {
                    "id": "QN-01",
                    "company": "FPT Software Quy Nhơn (AI Valley)",
                    "title": "Chuyên Viên Truyền Thông & Marketing Nội Bộ",
                    "source": "TopCV / LinkedIn",
                    "salary": "9.000.000 - 12.000.000 VNĐ",
                    "schedule": "Thứ 2 - Thứ 6 (Nghỉ T7, CN)",
                    "fit_score": "95%",
                    "status": "Ready to Apply (Chờ duyệt)"
                },
                {
                    "id": "QN-02",
                    "company": "Tập đoàn TMS / Khách sạn Pullman Quy Nhơn",
                    "title": "Marketing & Content Creator (Bilingual En-Vi)",
                    "source": "Vieclam24h",
                    "salary": "8.500.000 - 10.000.000 VNĐ",
                    "schedule": "Hành chính (Thứ 2 - Thứ 6)",
                    "fit_score": "90%",
                    "status": "Ready to Apply (Chờ duyệt)"
                },
                {
                    "id": "QN-03",
                    "company": "Trung Tâm Ngoại Ngữ Quốc Tế Quy Nhơn",
                    "title": "Chuyên Viên Tư Vấn & Phát Triển Nội Dung Khóa Học",
                    "source": "Facebook Job Groups",
                    "salary": "8.000.000 - 11.000.000 VNĐ",
                    "schedule": "Hành chính",
                    "fit_score": "92%",
                    "status": "Ready to Apply (Chờ duyệt)"
                }
            ],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.pipeline, f, ensure_ascii=False, indent=2)

    def display_pipeline(self):
        print("\n" + "="*70)
        print("          BẢNG THEO DÕI TIẾN TRÌNH RẢI CV TỰ ĐỘNG (JOB PIPELINE)")
        print("="*70)
        print(f"Ứng viên: {self.pipeline['candidate']}")
        print(f"Tiêu chí: {self.pipeline['criteria']['location']} | {self.pipeline['criteria']['schedule']} | {self.pipeline['criteria']['salary_range']}")
        print("-" * 70)
        for job in self.pipeline["jobs"]:
            print(f"[{job['id']}] {job['company']} - {job['title']}")
            print(f"      Lương: {job['salary']} | Lịch: {job['schedule']} | Độ phù hợp: {job['fit_score']}")
            print(f"      Trạng thái: -> {job['status']}")
            print("-" * 70)

if __name__ == "__main__":
    tracker = JobPipeline()
    tracker.display_pipeline()
