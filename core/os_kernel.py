"""
AI Agent OS Router
Manages tool routing: Browser automation (browser-use) + Cross-platform media inspection (Agent-Reach).
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Nap cau hinh moi truong
load_dotenv()

# Dam bao import duoc cac tools trong he thong
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools.reach.media_tool import MediaReachTool
from tools.job_search.job_hunter import JobHunterTool

class AgentOS:
    def __init__(self):
        self.reach_tool = MediaReachTool()
        self.job_tool = JobHunterTool()
        self.api_key = os.getenv("GEMINI_API_KEY")

    def run_media_inspect(self, target_url: str):
        """Quet va doc noi dung video hoac trang web."""
        if "youtube.com" in target_url or "youtu.be" in target_url:
            print(f"\n[AI Agent OS] Dang phan tich video YouTube: {target_url}...")
            info = self.reach_tool.inspect_youtube(target_url)
            print("\n=== KET QUA QUET YOUTUBE ===")
            for k, v in info.items():
                print(f"[{k.upper()}]: {v}")
            return info
        else:
            print(f"\n[AI Agent OS] Dang quet doc noi dung web qua Jina Reader: {target_url}...")
            content = self.reach_tool.read_web_content(target_url)
            print(f"\n[+] Da trich xuat noi dung (do dai: {len(content)} ky tu):")
            print(content[:600] + ("..." if len(content) > 600 else ""))
            return content

    async def run_browser_automation(self, task: str):
        """Khoi chay browser-use de tu dong hoa trinh duyet."""
        from browser_use import Agent, BrowserProfile, Browser, ChatGoogle

        if not self.api_key:
            print("[!] GEMINI_API_KEY khong ton tai trong .env!")
            return

        llm = ChatGoogle(model="gemini-2.0-flash", api_key=self.api_key)
        profile = BrowserProfile(cdp_url="http://localhost:9222")
        browser = Browser(profile=profile)

        relentless_directive = (
            "\n[VMAX AGENT RELENTLESS EXECUTION PROTOCOL]\n"
            "1. TUYỆT ĐỐI KHÔNG BỎ CUỘC GIỮA CHỪNG: Dù gặp bất kỳ trở ngại nào (phần tử động, popup, "
            "xác thực OAuth, captcha, thay đổi giao diện), phải kiên trì thử các cách tiếp cận khác nhau "
            "(tìm text tương tự, thử XPath/ARIA, cuộn trang, click lại sau delay, kiểm tra tab mới) cho đến khi đạt mục tiêu.\n"
            "2. KIỂM SOÁT ĐA CỬA SỔ & POPUP: Khi có popup OAuth (Google, Facebook...), lập tức chuyển sang popup "
            "để hoàn tất đăng nhập/xác nhận rồi quay lại tab chính.\n"
            "3. XÁC THỰC BẰNG CHỨNG THỰC TẾ: Chỉ kết thúc khi đạt được kết quả cuối cùng hoặc đã kiểm chứng bằng chứng xác thực."
        )

        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            extend_system_message=relentless_directive,
            max_failures=10,
            enable_planning=True,
            planning_replan_on_stall=3
        )
        print(f"\n[AI Agent OS] Dang thuc thi tren Browser (Relentless Mode): '{task}'...")
        history = await agent.run()
        print("\n[+] Browser Agent hoan thanh!")
        print(history.final_result())
