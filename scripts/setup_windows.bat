@echo off
setlocal
cd /d "%~dp0\.."

where uv >nul 2>nul
if errorlevel 1 (
    echo uv is not installed.
    echo Install from: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo Installing project dependencies...
uv sync
if errorlevel 1 (
    echo Dependency install failed.
    pause
    exit /b 1
)

echo.
echo Setup complete.
echo Launch with: Start Subtext.bat
pause
