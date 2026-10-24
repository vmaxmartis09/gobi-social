import sys
import asyncio
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))  # repo src/ -> gobi.*
from gobi.services.os_kernel import AgentOS

def print_banner():
    print("""
==========================================================
             AI AGENT OS - MULTI-PLATFORM SYSTEM
  - Web & Social Reach (Agent-Reach Engine)
  - Video & Subtitle Inspector (YouTube, Bilibili)
  - AI Job Search & CV Hunter (MadsLorentzen/ai-job-search)
  - Browser Automation Engine (browser-use + Chrome CDP)
==========================================================
""")

async def main():
    print_banner()
    os_kernel = AgentOS()

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print("Cac che do:")
        print("  1. Nhap URL (YouTube / Web) de doc, quet noi dung bang Agent-Reach")
        print("  2. Nhap yeu cau thao tac trinh duyet (vi du: 'dang nhap va tim kiem...')")
        user_input = input("\n[?] Nhap yeu cau hoac URL: ").strip()

    if not user_input:
        print("Yeu cau khong hop le!")
        return

    # Kiem tra neu la URL can quet doc noi dung / xem video
    if user_input.startswith("http://") or user_input.startswith("https://"):
        os_kernel.run_media_inspect(user_input)
    else:
        # Neu la tac vu duyet web tu dong hoa
        await os_kernel.run_browser_automation(user_input)

if __name__ == "__main__":
    asyncio.run(main())