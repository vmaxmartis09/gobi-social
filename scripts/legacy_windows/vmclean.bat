@echo off
chcp 65001 >nul

title TOOL DON RAC VA TOI UU WINDOWS - 1 CLICK
color 0A
cls

echo ========================================================
echo             HE THONG DANG TIEN HANH TOI UU...
echo ========================================================
echo.

:: Kiem tra quyen Administrator
openfiles >nul 2>&1
if '%errorlevel%' NEQ '0' (
    echo [CANH BAO] File can duoc chay bang quyen Administrator (Run as Administrator)!
    echo Dang thu tu dong yeu cau quyen Administrator...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: 1. Tat SysMain (Superfetch) - Thu pham so 1 gay Full Disk 100%
echo [*] Dang tat service SysMain (Superfetch - chong Full Disk)...
sc config "SysMain" start= disabled >nul 2>&1
net stop "SysMain" >nul 2>&1

:: 2. Tat Connected User Experiences and Telemetry (DiagTrack)
echo [*] Dang tat Telemetry (DiagTrack - ghi log theo doi ngam)...
sc config "DiagTrack" start= disabled >nul 2>&1
net stop "DiagTrack" >nul 2>&1

:: 3. Tat Windows Error Reporting & Diagnostic Services
echo [*] Dang tat Windows Error Reporting & Diagnostic Services...
sc config "WerSvc" start= disabled >nul 2>&1
net stop "WerSvc" >nul 2>&1
sc config "DPS" start= disabled >nul 2>&1
net stop "DPS" >nul 2>&1

:: 4. Tat Delivery Optimization (DoSvc) - Chia se update P2P qua mang
echo [*] Dang tat Delivery Optimization (DoSvc - chong an mang va ghi dia)...
sc config "DoSvc" start= disabled >nul 2>&1
net stop "DoSvc" >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" /v DODownloadMode /t REG_DWORD /d 0 /f >nul 2>&1

:: 5. Tat Sleep Hibernation (Giai phong 8GB - 32GB hiberfil.sys)
echo [*] Dang tat Hibernation (giai phong file hiberfil.sys)...
powercfg -h off >nul 2>&1

:: 6. Mo khoa Ultimate Performance Power Plan
echo [*] Dang kich hoat goi nguon Ultimate Performance...
powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 >nul 2>&1

:: 7. Vo hieu hoa cac task Telemetry / CEIP trong Task Scheduler
echo [*] Dang vo hieu hoa cac Task Telemetry trong Task Scheduler...
schtasks /change /tn "Microsoft\Windows\Customer Experience Improvement Program\Consolidator" /disable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\Customer Experience Improvement Program\UsbCeip" /disable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser" /disable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\Application Experience\ProgramDataUpdater" /disable >nul 2>&1

:: 8. Tat chay ngam Edge vinh vien trong Registry
echo [*] Dang tat chay ngam Microsoft Edge (StartupBoost & BackgroundMode)...
reg add "HKCU\Software\Policies\Microsoft\Edge" /v StartupBoostEnabled /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKCU\Software\Policies\Microsoft\Edge" /v BackgroundModeEnabled /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v StartupBoostEnabled /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v BackgroundModeEnabled /t REG_DWORD /d 0 /f >nul 2>&1

:: 9. Dong cac tien trinh chay ngam khong can thiet
echo [*] Dang giai phong RAM cac tien trinh chay ngam (msedge)...
taskkill /f /im msedge.exe >nul 2>&1

:: 10. Don dep User Temp
echo [*] Dang xoa User Temp (%TEMP%)...
del /s /f /q "%temp%\*.*" >nul 2>&1
for /d %%p in ("%temp%\*.*") do rmdir "%%p" /s /q >nul 2>&1

:: 11. Don dep Windows Temp
echo [*] Dang xoa Windows System Temp (C:\Windows\Temp)...
del /s /f /q "C:\Windows\Temp\*.*" >nul 2>&1
for /d %%p in ("C:\Windows\Temp\*.*") do rmdir "%%p" /s /q >nul 2>&1

:: 12. Don dep Prefetch
echo [*] Dang xoa Windows Prefetch...
del /s /f /q "C:\Windows\Prefetch\*.*" >nul 2>&1

:: 13. Don dep Windows Update Download Cache
echo [*] Dang xoa Cache cap nhat SoftwareDistribution...
net stop wuauserv >nul 2>&1
del /s /f /q "C:\Windows\SoftwareDistribution\Download\*.*" >nul 2>&1
net start wuauserv >nul 2>&1

:: 14. Xoa Crash Dumps
echo [*] Dang xoa Crash Dumps...
del /s /f /q "%LOCALAPPDATA%\CrashDumps\*.*" >nul 2>&1
del /s /f /q "%SystemRoot%\Minidump\*.*" >nul 2>&1

:: 15. Xoa Thumbnail Cache
echo [*] Dang xoa Thumbnail cache...
del /f /s /q /a "%LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db" >nul 2>&1

:: 16. Xoa sach Thung rac (Recycle Bin)
echo [*] Dang don sach Thung rac (Recycle Bin)...
rd /s /q %systemdrive%\$Recycle.bin >nul 2>&1

:: 17. Xoa DNS Cache
echo [*] Xoa DNS Cache (Lam moi mang)...
ipconfig /flushdns >nul 2>&1

:: 18. Chay TRIM toi uu SSD o C:
echo [*] Dang chay TRIM toi uu hoa o dia C: (ReTrim SSD)...
powershell -NoProfile -Command "Optimize-Volume -DriveLetter C -ReTrim -ErrorAction SilentlyContinue" >nul 2>&1

echo.
echo ========================================================
echo               DA TOI UU VA DON DEP HOAN TAT!
echo ========================================================
echo.
echo ========================================================
echo       DANH SACH TOP 10 UNG DUNG DANG NGON RAM NHAT
echo ========================================================
echo.

:: Show top process an RAM bang PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 @{Name='Ten Tien Trinh';Expression={$_.ProcessName}}, @{Name='Dung Luong RAM (MB)';Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}} | Format-Table -AutoSize"

echo.
echo ========================================================
echo [Thanh cong]: He thong da tat cac service rac va toi uu hoa dia!
echo ========================================================
echo.
echo Nhan phim bat ky de thoat...
pause >nul
exit
