@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ==========================================================
echo           BROWSER-USE AI AGENT (ALL-IN-ONE)
echo ==========================================================
echo.

set "ENV_FILE=%~dp0.env"
set "KEY_FOUND=0"

if exist "%ENV_FILE%" (
    for /f "usebackq tokens=1,* delims==" %%A in ("%ENV_FILE%") do (
        if /i "%%A"=="GEMINI_API_KEY" (
            if not "%%B"=="" if not "%%B"=="your_gemini_api_key_here" (
                set "KEY_FOUND=1"
            )
        )
    )
)

if "%KEY_FOUND%"=="0" (
    echo [!] Chua tim thay Gemini API Key trong he thong.
    echo Ban chi can nhap 1 LAN DUY NHAT, he thong se tu dong luu lai.
    echo (Lay key mien phi tai: https://aistudio.google.com/app/apikey)
    echo.
    set /p "USER_KEY=>> Vui long dan GEMINI_API_KEY roi an Enter: "
    if "!USER_KEY!"=="" (
        echo [X] API Key khong duoc de trong!
        pause
        exit /b 1
    )
    echo GEMINI_API_KEY=!USER_KEY!> "%ENV_FILE%"
    echo.
    echo [OK] Da luu API Key thanh cong!
    echo.
)

echo [*] Dang kiem tra ket noi Chrome...
curl -s http://localhost:9222/json/version >nul 2>&1
if errorlevel 1 (
    echo [*] Chrome Debugging chua mo. Dang tu dong bat Chrome voi profile rieng...
    call launch_chrome_debug.bat
    timeout /t 3 >nul
) else (
    echo [OK] Chrome dang hoat dong san sang.
)

echo.
echo [*] Khoi chay AI Agent...
.\.venv\Scripts\python.exe run_agent.py %*

echo.
echo ==========================================================
pause