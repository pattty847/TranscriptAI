"""
Main application window and tab coordination.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout,
    QHBoxLayout, QWidget, QLabel, QFrame, QToolBar
)

from src.config.paths import ProjectPaths
from src.ui.analysis_tab import AnalysisTab
from src.ui.download_tab import DownloadTab
from src.ui.results_tab import ResultsTab
from src.ui.styles import DARK_THEME


class MainWindow(QMainWindow):
    """Main app shell."""

    def __init__(self):
        super().__init__()
        ProjectPaths.initialize()
        self.setup_ui()
        self.setup_theme()

    def setup_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle("Subtext - Modern Video Analysis")
        self.setMinimumSize(980, 680)
        self.resize(1120, 760)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.create_header())

        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(False)

        self.download_tab = DownloadTab()
        self.analysis_tab = AnalysisTab()
        self.results_tab = ResultsTab()

        self.tab_widget.addTab(self.download_tab, "Download & Transcribe")
        self.tab_widget.addTab(self.analysis_tab, "AI Analysis")
        self.tab_widget.addTab(self.results_tab, "Results & Export")
        main_layout.addWidget(self.tab_widget)

        self.create_toolbar()
        self.setup_connections()

    def create_toolbar(self):
        """Create quick-action toolbar."""
        toolbar = QToolBar("Quick Actions", self)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setObjectName("mainToolbar")
        self.addToolBar(toolbar)

        new_session = toolbar.addAction("New Session")
        new_session.triggered.connect(self.reset_session)

        open_videos = toolbar.addAction("Open Videos")
        open_videos.triggered.connect(lambda: self.download_tab.open_folder(ProjectPaths.VIDEOS_DIR))

        open_transcripts = toolbar.addAction("Open Transcripts")
        open_transcripts.triggered.connect(lambda: self.download_tab.open_folder(ProjectPaths.TRANSCRIPTS_DIR))

        clear_results = toolbar.addAction("Clear Results")
        clear_results.triggered.connect(self.results_tab.clear_results)

    def create_header(self) -> QFrame:
        """Create a compact app header."""
        header = QFrame()
        header.setObjectName("header")
        header.setMaximumHeight(62)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("Subtext")
        title.setObjectName("title")
        subtitle = QLabel("Download, transcribe, and analyze locally")
        subtitle.setObjectName("subtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addWidget(title_widget)
        layout.addStretch()

        version_label = QLabel("v1.0.0")
        version_label.setObjectName("version")
        layout.addWidget(version_label)
        return header

    def setup_theme(self):
        """Apply global theme and fonts."""
        self.setStyleSheet(DARK_THEME)
        font = QFont("Segoe UI", 10)
        self.setFont(font)
        QApplication.instance().setFont(font)

    def setup_connections(self):
        """Connect cross-tab signals."""
        self.download_tab.transcription_completed.connect(self.on_transcription_completed)
        self.analysis_tab.analysis_completed.connect(self.on_analysis_completed)

    def on_transcription_completed(self, transcript_path: Path, transcript_text: str):
        """Load transcript into analysis tab and move user there."""
        self.analysis_tab.load_transcript(transcript_text)
        self.tab_widget.setCurrentIndex(1)

    def on_analysis_completed(self, analysis_result):
        """Load analysis result into results tab and move user there."""
        self.results_tab.load_results(analysis_result)
        self.tab_widget.setCurrentIndex(2)

    def reset_session(self):
        """Reset analysis and results for a fresh workflow."""
        self.analysis_tab.clear_transcript_session(confirm=False)
        self.results_tab.clear_results()
        self.tab_widget.setCurrentIndex(0)


def create_app() -> QApplication:
    """Create and configure QApplication."""
    app = QApplication(sys.argv)
    app.setApplicationName("Subtext")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Subtext")
    return app


def main():
    """Main application entry point."""
    app = create_app()
    window = MainWindow()
    window.show()

    screen = app.primaryScreen().geometry()
    window_size = window.geometry()
    x = (screen.width() - window_size.width()) // 2
    y = (screen.height() - window_size.height()) // 2
    window.move(x, y)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
