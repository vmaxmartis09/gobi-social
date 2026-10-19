@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

if not exist "%LOCALAPPDATA%\Google\Chrome\AI_Agent_Profile" (
    mkdir "%LOCALAPPDATA%\Google\Chrome\AI_Agent_Profile"
)

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\AI_Agent_Profile"