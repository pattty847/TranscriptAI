#!/usr/bin/env python3
"""
Quick launcher for TranscriptAI
"""
import subprocess
import sys
from pathlib import Path

def main():
    # Get the project directory
    project_dir = Path(__file__).parent
    
    # Python executable in venv
    if sys.platform == "win32":
        python_exe = project_dir / ".venv" / "Scripts" / "python.exe"
    else:
        python_exe = project_dir / ".venv" / "bin" / "python"
    
    # Main script
    main_script = project_dir / "src" / "main.py"
    
    # Check if files exist
    if not python_exe.exists():
        print("Virtual environment not found. Run setup first.")
        print("   uv venv && uv pip install -r requirements.txt")
        return 1
        
    if not main_script.exists():
        print("Main script not found.")
        return 1
        
    # Launch the application
    print("Launching TranscriptAI...")
    try:
        subprocess.run([str(python_exe), str(main_script)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Application failed to start: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nTranscriptAI closed by user")
        return 0
        
    return 0

if __name__ == "__main__":
    sys.exit(main())