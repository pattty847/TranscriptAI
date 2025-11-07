"""
Download and transcription tab with modern UI
"""
import asyncio
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal, QTimer, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QProgressBar, QTextEdit, QGroupBox,
    QComboBox, QCheckBox, QFrame, QSplitter
)

from src.core.downloader import UniversalDownloader, DownloadProgress
from src.core.transcriber import WhisperTranscriber, TranscriptionProgress


class DownloadWorker(QThread):
    """Worker thread for downloading and transcribing"""
    progress_updated = Signal(str)  # Progress message
    download_progress = Signal(float)  # Download percentage
    transcription_progress = Signal(float)  # Transcription percentage
    completed = Signal(Path, str)  # (file_path, transcript_text)
    error_occurred = Signal(str)  # Error message
    
    def __init__(self, url: str, model: str = "medium.en", download_only: bool = False, keep_video: bool = False):
        super().__init__()
        self.url = url
        self.model = model
        self.download_only = download_only
        self.keep_video = keep_video
        self.downloader = UniversalDownloader()
        self.transcriber = WhisperTranscriber(model) if not download_only else None
        
    def run(self):
        """Run the download and transcription process"""
        try:
            # Create event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the async workflow
            loop.run_until_complete(self.download_and_transcribe())
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if 'loop' in locals():
                loop.close()
                
    async def download_and_transcribe(self):
        """Download video and transcribe audio"""
        try:
            # Download phase
            self.progress_updated.emit("Starting download...")
            
            def download_callback(progress: DownloadProgress):
                self.download_progress.emit(progress.percent)
                self.progress_updated.emit(f"Downloading: {progress.filename} - {progress}")
                
            video_path = await self.downloader.download(self.url, download_callback)
            self.progress_updated.emit(f"Download completed: {video_path.name}")
            self.download_progress.emit(100.0)  # Download done
            
            if self.download_only:
                # Download only - skip transcription
                self.progress_updated.emit("Download completed! (Transcription skipped)")
                self.completed.emit(video_path, "")  # Empty transcript
            else:
                # Transcription phase
                self.progress_updated.emit("Starting transcription...")
                
                def transcription_callback(progress: TranscriptionProgress):
                    self.transcription_progress.emit(progress.percent)
                    self.progress_updated.emit(str(progress))
                    
                transcript, transcript_path = await self.transcriber.transcribe_and_save(
                    video_path, transcripts_dir=self.downloader.transcripts_dir, progress_callback=transcription_callback
                )
                
                self.progress_updated.emit(f"Transcription completed: {transcript_path.name}")
                self.completed.emit(transcript_path, transcript)
                
                # Clean up video if not keeping it
                if not self.keep_video:
                    try:
                        video_path.unlink()
                        self.progress_updated.emit(f"Removed video file: {video_path.name}")
                    except Exception:
                        pass  # Ignore cleanup errors
            
        except Exception as e:
            self.error_occurred.emit(f"Process failed: {str(e)}")


class DownloadTab(QWidget):
    """Download and transcription tab"""
    transcription_completed = Signal(Path, str)  # (file_path, transcript_text)
    
    def __init__(self):
        super().__init__()
        self.worker: Optional[DownloadWorker] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the download tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Input section
        input_group = self.create_input_section()
        layout.addWidget(input_group)
        
        # Folder info section
        folder_group = self.create_folder_info_section()
        layout.addWidget(folder_group)
        
        # Progress section
        progress_group = self.create_progress_section()
        layout.addWidget(progress_group)
        
        # Log section
        log_group = self.create_log_section()
        layout.addWidget(log_group)
        
        layout.addStretch()
        
    def create_input_section(self) -> QGroupBox:
        """Create the URL input section"""
        group = QGroupBox("Video Input")
        layout = QVBoxLayout(group)
        
        # URL input
        url_layout = QHBoxLayout()
        
        url_label = QLabel("Video URL:")
        url_label.setMinimumWidth(100)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://youtube.com/watch?v=... (or any video URL)")
        self.url_input.returnPressed.connect(self.start_process)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        
        layout.addLayout(url_layout)
        
        # Settings row
        settings_layout = QHBoxLayout()
        
        # Model selection
        model_label = QLabel("Whisper Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "tiny.en", "base.en", "small.en", "medium.en", "large-v3"
        ])
        self.model_combo.setCurrentText("medium.en")
        
        # Options checkboxes
        self.keep_video_check = QCheckBox("Keep video file")
        self.keep_video_check.setChecked(False)
        
        self.download_only_check = QCheckBox("Download only (skip transcription)")
        self.download_only_check.setChecked(False)
        
        # Connect download_only checkbox to disable keep_video when download-only is selected
        self.download_only_check.toggled.connect(self.on_download_only_changed)
        
        settings_layout.addWidget(model_label)
        settings_layout.addWidget(self.model_combo)
        settings_layout.addStretch()
        settings_layout.addWidget(self.keep_video_check)
        settings_layout.addWidget(self.download_only_check)
        
        layout.addLayout(settings_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("🚀 Start Download & Transcription")
        self.start_button.clicked.connect(self.start_process)
        
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.clicked.connect(self.stop_process)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        return group
        
    def create_folder_info_section(self) -> QGroupBox:
        """Create folder information section"""
        group = QGroupBox("Output Folders")
        layout = QVBoxLayout(group)
        
        # Videos folder
        videos_layout = QHBoxLayout()
        videos_layout.addWidget(QLabel("Videos:"))
        self.videos_path_label = QLabel("downloads/videos/")
        self.videos_path_label.setStyleSheet("QLabel { color: #0d7377; font-family: monospace; }")
        videos_layout.addWidget(self.videos_path_label)
        videos_layout.addStretch()
        layout.addLayout(videos_layout)
        
        # Transcripts folder  
        transcripts_layout = QHBoxLayout()
        transcripts_layout.addWidget(QLabel("Transcripts:"))
        self.transcripts_path_label = QLabel("downloads/transcripts/")
        self.transcripts_path_label.setStyleSheet("QLabel { color: #0d7377; font-family: monospace; }")
        transcripts_layout.addWidget(self.transcripts_path_label)
        transcripts_layout.addStretch()
        layout.addLayout(transcripts_layout)
        
        return group
        
    def create_progress_section(self) -> QGroupBox:
        """Create the progress tracking section"""
        group = QGroupBox("Progress")
        layout = QVBoxLayout(group)
        
        # Download progress
        download_layout = QHBoxLayout()
        download_layout.addWidget(QLabel("Download:"))
        
        self.download_progress = QProgressBar()
        self.download_progress.setVisible(False)
        download_layout.addWidget(self.download_progress)
        
        layout.addLayout(download_layout)
        
        # Transcription progress  
        transcription_layout = QHBoxLayout()
        transcription_layout.addWidget(QLabel("Transcription:"))
        
        self.transcription_progress = QProgressBar()
        self.transcription_progress.setVisible(False)
        transcription_layout.addWidget(self.transcription_progress)
        
        layout.addLayout(transcription_layout)
        
        # Status label
        self.status_label = QLabel("Ready to start...")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        return group
        
    def create_log_section(self) -> QGroupBox:
        """Create the log output section"""
        group = QGroupBox("Process Log")
        layout = QVBoxLayout(group)
        
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(200)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        return group
        
    def start_process(self):
        """Start the download and transcription process"""
        url = self.url_input.text().strip()
        if not url:
            self.add_log("❌ Please enter a video URL")
            return
            
        if self.worker and self.worker.isRunning():
            self.add_log("❌ Process already running")
            return
            
        # Get settings first
        model = self.model_combo.currentText()
        download_only = self.download_only_check.isChecked()
        keep_video = self.keep_video_check.isChecked()
            
        # Reset UI
        self.download_progress.setValue(0)
        self.transcription_progress.setValue(0)
        self.download_progress.setVisible(True)
        self.transcription_progress.setVisible(not download_only)  # Hide if download-only
        
        # Disable start button
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Clear log
        self.log_output.clear()
        
        self.worker = DownloadWorker(url, model, download_only, keep_video)
        
        # Connect signals
        self.worker.progress_updated.connect(self.update_status)
        self.worker.download_progress.connect(self.download_progress.setValue)
        self.worker.transcription_progress.connect(self.transcription_progress.setValue)
        self.worker.completed.connect(self.on_completed)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_worker_finished)
        
        self.worker.start()
        self.add_log(f"🚀 Starting process for: {url}")
        
    def stop_process(self):
        """Stop the current process"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait(3000)  # Wait up to 3 seconds
        elif self.worker:
            # Worker exists but not running, wait briefly for cleanup
            self.worker.wait(1000)
            
        self.on_worker_finished()
        self.add_log("⏹ Process stopped by user")
        
    def update_status(self, message: str):
        """Update status label and log"""
        self.status_label.setText(message)
        self.add_log(message)
        
    def add_log(self, message: str):
        """Add message to log output"""
        self.log_output.append(message)
        
    def on_download_only_changed(self, checked: bool):
        """Handle download-only checkbox changes"""
        if checked:
            # Disable keep_video when download-only is selected (it's always kept)
            self.keep_video_check.setEnabled(False)
            self.keep_video_check.setChecked(True)  # Auto-check since we always keep in download-only
            self.keep_video_check.setText("Keep video file (always enabled)")
        else:
            # Re-enable keep_video when transcription is enabled
            self.keep_video_check.setEnabled(True)
            self.keep_video_check.setChecked(False)  # Default to false
            self.keep_video_check.setText("Keep video file")
            
    def on_completed(self, file_path: Path, transcript_text: str):
        """Handle successful completion"""
        is_download_only = self.download_only_check.isChecked()
        
        if is_download_only:
            self.add_log(f"✅ Download completed successfully!")
            self.add_log(f"📹 Video saved to: {file_path}")
            # Don't emit transcription_completed signal for download-only
        else:
            self.add_log(f"✅ Process completed successfully!")
            self.add_log(f"📄 Transcript saved to: {file_path}")
            # Only emit signal if we have a transcript (auto-navigate to analysis)
            self.transcription_completed.emit(file_path, transcript_text)
        
    def on_error(self, error_message: str):
        """Handle error"""
        self.add_log(f"❌ Error: {error_message}")
        self.status_label.setText(f"Error: {error_message}")
        
    def on_worker_finished(self):
        """Handle worker thread completion"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Ready for next task")
        
        if self.worker:
            self.worker.deleteLater()
            self.worker = None