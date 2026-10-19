@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

set "PROFILE_DIR=C:\Users\HAI\.agent-browser\profiles\ai_profile"

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "CHROME_BIN=C:\Program Files\Google\Chrome\Application\chrome.exe"
) else (
    set "CHROME_BIN=C:\Users\HAI\.agent-browser\browsers\chrome-155.0.8059.84\chrome.exe"
)

echo ======================================================================
echo    MO TRINH DUYET SETUP PROFILE CHO AI AGENT
echo ======================================================================
echo.
echo [*] Profile Folder: !PROFILE_DIR!
echo [*] Trinh duyet:    !CHROME_BIN!
echo.
echo [!] Huong dan:
echo   - Cua so Chrome se duoc mo len ngay tren man hinh.
echo   - Ban hay dang nhap vao cac tai khoan mong muon (Google, Facebook, Github...).
echo   - Dang nhap xong thi chi can DONG cua so Chrome lai.
echo   - Moi session va cookie se duoc luu lai vinh vien cho AI su dung.
echo.

start "" "!CHROME_BIN!" --user-data-dir="!PROFILE_DIR!" --no-first-run --no-default-browser-check "https://accounts.google.com"
