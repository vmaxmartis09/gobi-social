@echo off
chcp 65001 >nul
title MỞ GOOGLE FLOW VEO 3.1
echo ======================================================================
echo    ĐANG KHỞI ĐỘNG GOOGLE FLOW STUDIO TRÊN CHROME (CỔNG DEBUG 9222)
echo ======================================================================
echo.
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=os.path.join(os.path.expanduser("~"), ".agent-browser", r"profiles\ai_profile") "https://flow.google.com"
echo [+] Chrome đã được bật! Vui lòng đăng nhập dinhthienthoai@gmail.com
echo [*] Agent đang tự động kết nối qua cổng 9222 để điều khiển...
