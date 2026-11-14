@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================================
echo    KHOI CHAY AI AGENT CHAY NGAM (LIVE VIEWPORT MONITOR)
echo ======================================================================
echo.

set "TARGET_URL=%~1"
if "!TARGET_URL!"=="" (
    set /p "TARGET_URL=Nhap URL can AI xu ly (Enter de mac dinh): "
)
if "!TARGET_URL!"=="" (
    set "TARGET_URL=https://news.ycombinator.com"
)

.\.venv\Scripts\python.exe core\stealth_monitor.py "!TARGET_URL!"

pause
