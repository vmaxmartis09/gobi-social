@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

chcp 65001 >nul
echo 1. Tat tat ca tien trinh Edge...
taskkill /f /im msedge.exe >nul 2>&1
taskkill /f /im msedgewebview2.exe >nul 2>&1
taskkill /f /im MicrosoftEdgeUpdate.exe >nul 2>&1

echo 2. Go bo cac Service va Task chay ngam cua Edge...
sc stop edgeupdate >nul 2>&1
sc delete edgeupdate >nul 2>&1
sc stop edgeupdatem >nul 2>&1
sc delete edgeupdatem >nul 2>&1
schtasks /delete /tn "MicrosoftEdgeUpdateTaskMachineCore" /f >nul 2>&1
schtasks /delete /tn "MicrosoftEdgeUpdateTaskMachineUA" /f >nul 2>&1

echo 3. Mo khoa quyen he thong va xoa triet de file chuong trinh Edge...
takeown /f "C:\Program Files (x86)\Microsoft\Edge" /r /d y >nul 2>&1
icacls "C:\Program Files (x86)\Microsoft\Edge" /grant administrators:F /t >nul 2>&1
rd /s /q "C:\Program Files (x86)\Microsoft\Edge" >nul 2>&1

takeown /f "C:\Program Files (x86)\Microsoft\EdgeCore" /r /d y >nul 2>&1
icacls "C:\Program Files (x86)\Microsoft\EdgeCore" /grant administrators:F /t >nul 2>&1
rd /s /q "C:\Program Files (x86)\Microsoft\EdgeCore" >nul 2>&1

echo 4. Xoa Registry Menu va Startup cua Edge...
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\EdgeUpdate" /v DoNotUpdateToEdgeWithChromium /t REG_DWORD /d 1 /f >nul 2>&1

echo 5. Xoa Shortcut trong Start Menu...
del /f /q "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk" >nul 2>&1

echo ========================================================
echo DA XOA TAN GOC MICROSOFT EDGE VA FILE CHUONG TRINH!
echo ========================================================
pause