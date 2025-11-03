"""
TranscriptAI - Modern Video Analysis Application
Entry point for the application
"""
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent
project_dir = src_dir.parent
sys.path.insert(0, str(project_dir))

from src.ui.main_window import main

if __name__ == "__main__":
    main()