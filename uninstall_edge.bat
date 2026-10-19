@echo off
:: Kiem tra va yeu cau quyen Administrator (UAC)
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Dang yeu cau quyen Administrator...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

chcp 65001 >nul
echo ========================================================
echo        TIEN TRINH GO CAI DAT MICROSOFT EDGE
echo ========================================================
echo.

echo 1. Dang tat toan bo tien trinh Edge dang chay...
taskkill /f /im msedge.exe >nul 2>&1
taskkill /f /im msedgewebview2.exe >nul 2>&1

echo 2. Dang mo khoa quyen go cai dat trong Registry...
reg add "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" /v NoRemove /t REG_DWORD /d 0 /f >nul 2>&1

echo 3. Dang go cai dat Microsoft Edge...
for /f "tokens=*" %%i in ('dir /b /s "C:\Program Files (x86)\Microsoft\Edge\Application\setup.exe" 2^>nul') do (
    echo Dang thuc thi go bo tai: %%i
    "%%i" --uninstall --msedge --channel=stable --system-level --verbose-logging --force-uninstall
)

echo 4. Chan Windows tu dong cai dat lai Edge khi Update...
reg add "HKLM\SOFTWARE\Microsoft\EdgeUpdate" /v DoNotUpdateToEdgeWithChromium /t REG_DWORD /d 1 /f >nul 2>&1

echo.
echo ========================================================
echo GO CAI DAT HOAN TAT!
echo ========================================================
pause
