"""
Main application window with modern tabbed interface
"""
import asyncio
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, QTimer, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
    QHBoxLayout, QWidget, QLabel, QFrame, QSplitter
)

from src.ui.styles import DARK_THEME
from src.ui.download_tab import DownloadTab
from src.ui.analysis_tab import AnalysisTab
from src.ui.results_tab import ResultsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_theme()
        
    def setup_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle("TranscriptAI - Modern Video Analysis")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(False)
        
        # Create tabs
        self.download_tab = DownloadTab()
        self.analysis_tab = AnalysisTab()
        self.results_tab = ResultsTab()
        
        # Add tabs
        self.tab_widget.addTab(self.download_tab, "📥 Download & Transcribe")
        self.tab_widget.addTab(self.analysis_tab, "🤖 AI Analysis")
        self.tab_widget.addTab(self.results_tab, "📊 Results & Export")
        
        main_layout.addWidget(self.tab_widget)
        
        # Connect signals
        self.setup_connections()
        
    def create_header(self) -> QFrame:
        """Create the application header"""
        header = QFrame()
        header.setObjectName("header")
        header.setMaximumHeight(80)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        title = QLabel("TranscriptAI")
        title.setObjectName("title")
        title.setStyleSheet("""
            QLabel#title {
                font-size: 28px;
                font-weight: 700;
                color: #0d7377;
                margin: 0px;
            }
        """)
        
        subtitle = QLabel("Download • Transcribe • Analyze with AI")
        subtitle.setObjectName("subtitle")
        subtitle.setStyleSheet("""
            QLabel#subtitle {
                font-size: 14px;
                color: #9c9c9c;
                margin: 0px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_widget)
        layout.addStretch()
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6c6c6c;
                padding: 4px 8px;
                background-color: #3c3c3c;
                border-radius: 4px;
            }
        """)
        layout.addWidget(version_label)
        
        return header
        
    def setup_theme(self):
        """Apply the dark theme"""
        self.setStyleSheet(DARK_THEME)
        
        # Set font
        font = QFont("Segoe UI", 10)
        self.setFont(font)
        QApplication.instance().setFont(font)
        
    def setup_connections(self):
        """Connect signals between tabs"""
        # When download completes, switch to analysis tab
        self.download_tab.transcription_completed.connect(self.on_transcription_completed)
        
        # When analysis completes, switch to results tab
        self.analysis_tab.analysis_completed.connect(self.on_analysis_completed)
        
    def on_transcription_completed(self, transcript_path: Path, transcript_text: str):
        """Handle transcription completion"""
        # Pass data to analysis tab
        self.analysis_tab.load_transcript(transcript_text)
        
        # Switch to analysis tab
        self.tab_widget.setCurrentIndex(1)
        
    def on_analysis_completed(self, analysis_result):
        """Handle analysis completion"""
        # Pass data to results tab
        self.results_tab.load_results(analysis_result)
        
        # Switch to results tab
        self.tab_widget.setCurrentIndex(2)


def create_app() -> QApplication:
    """Create and configure the QApplication"""
    app = QApplication(sys.argv)
    app.setApplicationName("TranscriptAI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("TranscriptAI")
    
    # Set application icon (if available)
    # app.setWindowIcon(QIcon("icon.png"))
    
    return app


def main():
    """Main application entry point"""
    app = create_app()
    
    window = MainWindow()
    window.show()
    
    # Center the window
    screen = app.primaryScreen().geometry()
    window_size = window.geometry()
    x = (screen.width() - window_size.width()) // 2
    y = (screen.height() - window_size.height()) // 2
    window.move(x, y)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()