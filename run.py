#!/usr/bin/env python3
"""
Lightweight launcher for Subtext.

Recommended usage:
    uv run python run.py
"""
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_dir = Path(__file__).parent
    main_script = project_dir / "src" / "main.py"

    if not main_script.exists():
        print("Main script not found: src/main.py")
        return 1

    print("Launching Subtext...")
    try:
        subprocess.run([sys.executable, str(main_script)], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Application failed to start: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nSubtext closed by user")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
