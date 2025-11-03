"""
Build standalone executable for TranscriptAI
"""
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Install PyInstaller if not present
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name", "TranscriptAI",       # Executable name
        "--icon", "assets/icon.ico",    # Icon (if you have one)
        "--add-data", "src;src",        # Include source files
        "--hidden-import", "PySide6",
        "--hidden-import", "torch",
        "--hidden-import", "whisper", 
        "--hidden-import", "yt_dlp",
        "--hidden-import", "ollama",
        "src/main.py"                   # Entry point
    ]
    
    # Remove icon if file doesn't exist
    if not Path("assets/icon.ico").exists():
        cmd.remove("--icon")
        cmd.remove("assets/icon.ico")
    
    print("Building executable...")
    print(" ".join(cmd))
    
    subprocess.run(cmd, check=True)
    
    print("\n✅ Build complete!")
    print("📁 Executable location: dist/TranscriptAI.exe")
    print("🚀 Double-click to launch!")

if __name__ == "__main__":
    build_executable()