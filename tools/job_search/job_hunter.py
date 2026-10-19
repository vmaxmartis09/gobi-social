"""
Job Application & Career Hunter Module
Integrates MadsLorentzen/ai-job-search with Agent-Reach for multi-platform job evaluation,
CV tailoring, and cover letter generation.
"""

import os
import sys
from tools.reach.media_tool import MediaReachTool

class JobHunterTool:
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.job_search_dir = os.path.join(self.base_dir, "tools", "job_search")
        self.claude_md_path = os.path.join(self.job_search_dir, "CLAUDE.md")
        self.reach_tool = MediaReachTool()

    def get_candidate_profile(self) -> str:
        """Doc thong tin ung vien tu CLAUDE.md."""
        if os.path.exists(self.claude_md_path):
            with open(self.claude_md_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Chua khoi tao ho so ung vien (CLAUDE.md)."

    def parse_job_posting(self, job_url: str) -> str:
        """Quet noi dung bai dang tuyen dung tu URL (LinkedIn, Boss, VietnamWorks, ITviec, Web...)."""
        print(f"[*] Dang quet JD tu URL: {job_url} qua Jina Reader...")
        return self.reach_tool.read_web_content(job_url)

    def evaluate_fit_prompt(self, job_description: str) -> str:
        """Tao prompt danh gia do phu hop (Fit Evaluation) giua ho so ung vien va JD."""
        profile = self.get_candidate_profile()
        return f"""
Ban la AI Career Advisor & Job Application Assistant.
Hay danh gia muc do phu hop (Fit Evaluation) giua Ho So Ung Vien va Bai Dang Tuyen Dung sau:

### HO SO UNG VIEN:
{profile}

### NOI DUNG TUYEN DUNG (JD):
{job_description[:3000]}

---
YEU CAU DANH GIA:
1. Ty le phu hop ky nang ky thuat (Technical Skills Match): ... %
2. Kinh nghiem & Trinh do (Experience Match)
3. Diem manh noi bat cua ung vien cho vi tri nay
4. Cac lo hong ky nang con thieu (Skill Gaps)
5. Ket luan khuyen nghi: Nen Apply hay Bo qua? Vi sao?
"""
