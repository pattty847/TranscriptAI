@echo off
cd /d "%~dp0"
title Subtext

where uv >nul 2>nul
if errorlevel 1 (
    echo uv is not installed.
    echo Install it from: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Setting up environment with uv sync...
    uv sync
    if errorlevel 1 (
        echo Setup failed.
        pause
        exit /b 1
    )
)

echo.
echo  [1] Desktop   - full app on this computer
echo  [2] Web       - browser UI (this PC + same Wi-Fi devices)
echo.
set /p pick="Choose 1 or 2: "

if "%pick%"=="2" (
    echo.
    echo Starting Web UI... Open http://127.0.0.1:8765 in your browser.
    echo From phone/tablet on same Wi-Fi: http://YOUR_PC_IP:8765
    echo.
    uv run python run_web.py
) else (
    if not "%pick%"=="1" (
        echo Unknown option. Starting Desktop.
        echo.
    )
    echo Launching Subtext (Desktop)...
    uv run python run.py
)

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
