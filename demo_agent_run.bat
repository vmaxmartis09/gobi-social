@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

set "AGENT_BIN=%~dp0bin\agent-browser.exe"
set "PROFILE_DIR=C:\Users\HAI\.agent-browser\profiles\ai_profile"

echo ======================================================================
echo    DEMO THUC THI AI AGENT VOI PROFILE DOC LAP DA LUU
echo ======================================================================
echo.

set "TARGET_URL=%~1"
if "!TARGET_URL!"=="" (
    set "TARGET_URL=https://news.ycombinator.com"
)

echo [*] Dang khoi chay Agent Browser voi Profile:
echo     !PROFILE_DIR!
echo [*] Dang truy cap: !TARGET_URL!
echo.

"!AGENT_BIN!" --profile "!PROFILE_DIR!" open "!TARGET_URL!"
if errorlevel 1 (
    echo [X] Co loi khi mo trang!
    pause
    exit /b 1
)

echo.
echo [+] Da truy cap thanh cong! Dang trich xuat phan tu tuong tac tren trang (Snapshot):
echo ----------------------------------------------------------------------
"!AGENT_BIN!" snapshot -i

echo.
echo ----------------------------------------------------------------------
echo [+] Dong phien Agent:
"!AGENT_BIN!" close

echo.
echo [HOAN TAT] Agent da thuc thi thanh cong ma khong anh huong trinh duyet chinh!
pause
