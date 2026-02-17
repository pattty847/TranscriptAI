@echo off
cd /d "%~dp0"
title TranscriptAI

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

echo Launching TranscriptAI...
uv run python run.py
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
