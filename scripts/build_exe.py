"""
Build a Windows executable for TranscriptAI using PyInstaller.

Run from project root:
    uv run python scripts/build_exe.py
"""
import subprocess
import sys
from pathlib import Path


def build_executable() -> None:
    project_root = Path(__file__).resolve().parents[1]
    icon_path = project_root / "assets" / "icon.ico"
    entry_path = project_root / "src" / "main.py"

    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "TranscriptAI",
        "--add-data", f"{project_root / 'src'};src",
        "--hidden-import", "PySide6",
        "--hidden-import", "torch",
        "--hidden-import", "whisper",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "ollama",
        str(entry_path),
    ]

    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])

    print("Building executable...")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True, cwd=project_root)
    print("Build complete: dist/TranscriptAI.exe")


if __name__ == "__main__":
    build_executable()
