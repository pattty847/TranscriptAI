@echo off
cd /d "%~dp0"
title TranscriptAI - Modern Video Analysis
echo 🚀 Launching TranscriptAI...
call .venv\Scripts\activate.bat
python run.py
if errorlevel 1 (
    echo.
    echo ❌ Error occurred. Press any key to exit...
    pause >nul
)