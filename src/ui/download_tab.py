"""
Download and transcription tab with modern UI
"""
import asyncio
import os
import platform
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal, QTimer, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QProgressBar, QTextEdit, QGroupBox,
    QComboBox, QCheckBox, QFrame, QSplitter, QFileDialog
)



class DownloadWorker(QThread):
    """Worker thread for downloading and transcribing"""
    progress_updated = Signal(str)  # Progress message
    download_progress = Signal(float)  # Download percentage
    transcription_progress = Signal(float)  # Transcription percentage
    completed = Signal(Path, str)  # (file_path, transcript_text)
    error_occurred = Signal(str)  # Error message
    
    def __init__(self, input_text: str, model: str = "medium.en", download_only: bool = False, keep_video: bool = False, copy_files: bool = True):
        super().__init__()
        self.input_text = input_text  # Changed from self.url
        self.model = model
        self.download_only = download_only
        self.keep_video = keep_video
        self.copy_files = copy_files
        
        # Use unified processor
        from src.core.processor import UnifiedProcessor
        self.processor = UnifiedProcessor(
            model=model,
            download_only=download_only,
            keep_video=keep_video,
            copy_files=copy_files
        )
        
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
        """Process mixed input using unified processor"""
        try:
            results = await self.processor.process_mixed_input(
                self.input_text,
                progress_callback=lambda msg: self.progress_updated.emit(msg),
                download_progress_callback=lambda p: self.download_progress.emit(p.percent),
                transcription_progress_callback=lambda p: self.transcription_progress.emit(p.percent)
            )
            
            # Handle results (for now, process first successful result)
            # Future: handle multiple results for batch processing
            for result in results:
                if result.status == "completed":
                    if result.transcript_path:
                        transcript_text = result.transcript_path.read_text(encoding='utf-8')
                        self.completed.emit(result.transcript_path, transcript_text)
                    else:
                        # Download-only mode
                        self.completed.emit(result.video_path, "")
                    break
                elif result.status == "error":
                    self.error_occurred.emit(result.error_message)
                    
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
        self.url_input.setPlaceholderText("Enter video URL(s) or click Browse to select local files (separate multiple with semicolons)")
        self.url_input.returnPressed.connect(self.start_process)
        self.url_input.textChanged.connect(self.on_input_changed)  # NEW: for validation
        self.url_input.setToolTip("You can enter URLs, select local files, or mix both. Separate multiple items with semicolons (;).")
        
        # NEW: Browse button
        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.setFixedWidth(120)
        self.browse_btn.clicked.connect(self.on_browse_clicked)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input, stretch=1)  # Takes remaining space
        url_layout.addWidget(self.browse_btn)
        
        layout.addLayout(url_layout)
        
        # NEW: Validation feedback label
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("QLabel { color: #9c9c9c; font-size: 11px; padding-left: 4px; }")
        layout.addWidget(self.validation_label)
        
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
        
        # NEW: Copy files checkbox
        self.copy_files_check = QCheckBox("Copy local files to assets/")
        self.copy_files_check.setChecked(True)  # Default: copy files
        self.copy_files_check.setToolTip(
            "When checked: Files are copied to assets/videos/ before processing.\n"
            "When unchecked: Files are processed in their original location (faster, but files stay where they are)."
        )
        
        # Connect download_only checkbox to disable keep_video when download-only is selected
        self.download_only_check.toggled.connect(self.on_download_only_changed)
        
        settings_layout.addWidget(model_label)
        settings_layout.addWidget(self.model_combo)
        settings_layout.addStretch()
        settings_layout.addWidget(self.keep_video_check)
        settings_layout.addWidget(self.download_only_check)
        settings_layout.addWidget(self.copy_files_check)
        
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
        from src.config.paths import ProjectPaths
        
        group = QGroupBox("Output Folders")
        layout = QVBoxLayout(group)
        
        # Videos folder
        videos_layout = QHBoxLayout()
        videos_layout.addWidget(QLabel("Videos:"))
        self.videos_path_label = QLabel("assets/videos/")
        self.videos_path_label.setStyleSheet("QLabel { color: #0d7377; font-family: monospace; }")
        self.videos_path_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.videos_path_label.mousePressEvent = lambda e: self.open_folder(ProjectPaths.VIDEOS_DIR)
        self.videos_path_label.setToolTip(f"Click to open folder\n{ProjectPaths.VIDEOS_DIR}")
        videos_layout.addWidget(self.videos_path_label)
        
        # Copy button for videos path
        videos_copy_btn = QPushButton("📋")
        videos_copy_btn.setFixedWidth(30)
        videos_copy_btn.setToolTip("Copy path to clipboard")
        videos_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(str(ProjectPaths.VIDEOS_DIR)))
        videos_layout.addWidget(videos_copy_btn)
        videos_layout.addStretch()
        layout.addLayout(videos_layout)
        
        # Transcripts folder  
        transcripts_layout = QHBoxLayout()
        transcripts_layout.addWidget(QLabel("Transcripts:"))
        self.transcripts_path_label = QLabel("assets/transcripts/")
        self.transcripts_path_label.setStyleSheet("QLabel { color: #0d7377; font-family: monospace; }")
        self.transcripts_path_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.transcripts_path_label.mousePressEvent = lambda e: self.open_folder(ProjectPaths.TRANSCRIPTS_DIR)
        self.transcripts_path_label.setToolTip(f"Click to open folder\n{ProjectPaths.TRANSCRIPTS_DIR}")
        transcripts_layout.addWidget(self.transcripts_path_label)
        
        # Copy button for transcripts path
        transcripts_copy_btn = QPushButton("📋")
        transcripts_copy_btn.setFixedWidth(30)
        transcripts_copy_btn.setToolTip("Copy path to clipboard")
        transcripts_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(str(ProjectPaths.TRANSCRIPTS_DIR)))
        transcripts_layout.addWidget(transcripts_copy_btn)
        transcripts_layout.addStretch()
        layout.addLayout(transcripts_layout)
        
        return group
        
    def create_progress_section(self) -> QGroupBox:
        """Create the progress tracking section"""
        group = QGroupBox("Progress")
        layout = QVBoxLayout(group)
        
        # NEW: Processing queue display
        queue_label = QLabel("Processing Queue:")
        queue_label.setStyleSheet("QLabel { font-weight: bold; }")
        layout.addWidget(queue_label)
        
        self.queue_list = QTextEdit()
        self.queue_list.setMaximumHeight(120)
        self.queue_list.setReadOnly(True)
        self.queue_list.setStyleSheet("""
            QTextEdit {
                background-color: #2c2c2c;
                border: 1px solid #404040;
                border-radius: 4px;
                font-family: monospace;
                font-size: 11px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.queue_list)
        
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
        self.status_label.setStyleSheet("QLabel { color: #9c9c9c; }")
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
        input_text = self.url_input.text().strip()
        if not input_text:
            self.add_log("❌ Please enter a video URL or select files")
            return
        
        # Validate input
        from src.core.input_processor import InputProcessor
        items = InputProcessor.parse_mixed_input(input_text)
        total_items = len(items["urls"]) + len(items["files"])
        
        if total_items == 0:
            self.add_log("❌ No valid URLs or files found in input")
            return
            
        if self.worker and self.worker.isRunning():
            self.add_log("❌ Process already running")
            return
            
        # Get settings first
        model = self.model_combo.currentText()
        download_only = self.download_only_check.isChecked()
        keep_video = self.keep_video_check.isChecked()
        copy_files = self.copy_files_check.isChecked()
        
        # Update queue display
        queue_items = []
        for url in items["urls"]:
            queue_items.append({"source": url, "status": "pending", "type": "url"})
        for file_path in items["files"]:
            queue_items.append({"source": file_path, "status": "pending", "type": "file"})
        self.update_queue_display(queue_items)
            
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
        
        self.worker = DownloadWorker(input_text, model, download_only, keep_video, copy_files)
        
        # Connect signals
        self.worker.progress_updated.connect(self.update_status)
        self.worker.download_progress.connect(self.download_progress.setValue)
        self.worker.transcription_progress.connect(self.transcription_progress.setValue)
        self.worker.completed.connect(self.on_completed)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_worker_finished)
        
        self.worker.start()
        self.add_log(f"🚀 Starting process for {total_items} item(s)...")
    
    def update_queue_display(self, items: list[dict]):
        """Update the visual queue display"""
        from pathlib import Path
        
        queue_text = []
        for i, item in enumerate(items, 1):
            status = item.get("status", "pending")
            status_icon = {
                "pending": "⏸️",
                "downloading": "⏳",
                "copying": "📁",
                "transcribing": "🎤",
                "completed": "✅",
                "error": "❌"
            }.get(status, "⏸️")
            
            source = item.get("source", "")
            full_path = source
            
            # Show just filename for file paths, truncate URLs
            try:
                path = Path(source)
                if path.exists() and path.is_file():
                    display_name = path.name
                    tooltip = str(path)
                else:
                    # URL or invalid path
                    if len(source) > 60:
                        display_name = source[:57] + "..."
                    else:
                        display_name = source
                    tooltip = source
            except:
                if len(source) > 60:
                    display_name = source[:57] + "..."
                else:
                    display_name = source
                tooltip = source
            
            # Add visual styling based on status
            if status == "completed":
                queue_text.append(f"{i}. {status_icon} {display_name}")
            elif status == "error":
                queue_text.append(f"{i}. {status_icon} {display_name}")
            elif status in ["downloading", "copying", "transcribing"]:
                queue_text.append(f"{i}. {status_icon} {display_name} (processing...)")
            else:
                queue_text.append(f"{i}. {status_icon} {display_name}")
        
        self.queue_list.setPlainText("\n".join(queue_text))
        
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
        # Update styling based on message type
        if "Error" in message or "❌" in message:
            self.status_label.setStyleSheet("QLabel { color: #ff6b6b; }")
        elif "completed" in message.lower() or "✅" in message:
            self.status_label.setStyleSheet("QLabel { color: #51cf66; }")
        elif "processing" in message.lower() or "downloading" in message.lower() or "transcribing" in message.lower():
            self.status_label.setStyleSheet("QLabel { color: #0d7377; }")
        else:
            self.status_label.setStyleSheet("QLabel { color: #9c9c9c; }")
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
        
        # Reset status label styling
        self.status_label.setStyleSheet("")
        
        if is_download_only:
            self.add_log(f"✅ Download completed successfully!")
            self.add_log(f"📹 Video saved to: {file_path}")
            self.status_label.setText(f"✅ Download completed! Video saved to: {file_path.name}")
            # Don't emit transcription_completed signal for download-only
        else:
            self.add_log(f"✅ Process completed successfully!")
            self.add_log(f"📄 Transcript saved to: {file_path}")
            # Show transcript preview
            preview = transcript_text[:100] + "..." if len(transcript_text) > 100 else transcript_text
            char_count = len(transcript_text)
            self.status_label.setText(f"✅ Transcription completed! ({char_count:,} characters) - {file_path.name}")
            self.status_label.setStyleSheet("QLabel { color: #51cf66; font-weight: bold; }")
            # Only emit signal if we have a transcript (auto-navigate to analysis)
            self.transcription_completed.emit(file_path, transcript_text)
        
        # Update queue to show completed status
        current_text = self.queue_list.toPlainText()
        if current_text:
            lines = current_text.split('\n')
            updated_lines = []
            for line in lines:
                if '⏸️' in line or '⏳' in line or '📁' in line or '🎤' in line:
                    updated_lines.append(line.replace('⏸️', '✅').replace('⏳', '✅').replace('📁', '✅').replace('🎤', '✅'))
                else:
                    updated_lines.append(line)
            self.queue_list.setPlainText('\n'.join(updated_lines))
        
    def open_folder(self, folder_path: Path):
        """Open folder in file explorer"""
        path_str = str(folder_path.resolve())
        
        if platform.system() == "Windows":
            os.startfile(path_str)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{path_str}'")
        else:  # Linux
            os.system(f"xdg-open '{path_str}'")
    
    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.add_log(f"📋 Copied to clipboard: {text}")
    
    def on_error(self, error_message: str):
        """Handle error"""
        self.add_log(f"❌ Error: {error_message}")
        self.status_label.setText(f"❌ Error: {error_message}")
        self.status_label.setStyleSheet("QLabel { color: #ff6b6b; font-weight: bold; }")
        # Update queue to show error status
        current_text = self.queue_list.toPlainText()
        if current_text:
            # Replace pending items with error status
            lines = current_text.split('\n')
            updated_lines = []
            for line in lines:
                if '⏸️' in line or '⏳' in line or '📁' in line or '🎤' in line:
                    updated_lines.append(line.replace('⏸️', '❌').replace('⏳', '❌').replace('📁', '❌').replace('🎤', '❌'))
                else:
                    updated_lines.append(line)
            self.queue_list.setPlainText('\n'.join(updated_lines))
        
    def on_worker_finished(self):
        """Handle worker thread completion"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Ready for next task")
        self.status_label.setStyleSheet("QLabel { color: #9c9c9c; }")
        
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
    
    def on_browse_clicked(self):
        """Open file dialog for multiple video file selection"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            str(Path.home()),
            "Video Files (*.mp4 *.avi *.mov *.mkv *.webm *.flv *.wmv *.m4v *.3gp);;All Files (*)"
        )
        
        if files:
            self.handle_selected_files(files)
    
    def handle_selected_files(self, file_paths: list[str]):
        """Handle files selected via Browse button"""
        # Add files to input box (semicolon separated)
        current_text = self.url_input.text().strip()
        file_text = "; ".join(file_paths)
        
        if current_text:
            combined_text = f"{current_text}; {file_text}"
        else:
            combined_text = file_text
        
        self.url_input.setText(combined_text)
        # Trigger validation update
        self.on_input_changed()
    
    def on_input_changed(self):
        """Validate input on every keystroke/file selection"""
        from src.core.input_processor import InputProcessor
        
        input_text = self.url_input.text().strip()
        if not input_text:
            self.validation_label.setText("")
            return
        
        items = InputProcessor.parse_mixed_input(input_text)
        
        total_items = len(items["urls"]) + len(items["files"])
        invalid_items = len(items["invalid"])
        
        if invalid_items > 0:
            self.validation_label.setText(f"⚠️ {invalid_items} invalid input(s) detected")
            self.validation_label.setStyleSheet("QLabel { color: #ff6b6b; font-size: 11px; }")
        elif total_items > 0:
            url_count = len(items["urls"])
            file_count = len(items["files"])
            if url_count > 0 and file_count > 0:
                self.validation_label.setText(f"✓ {url_count} URL(s), {file_count} local file(s) ready")
            elif url_count > 0:
                self.validation_label.setText(f"✓ {url_count} URL(s) ready")
            else:
                self.validation_label.setText(f"✓ {file_count} local file(s) ready")
            self.validation_label.setStyleSheet("QLabel { color: #51cf66; font-size: 11px; }")
        else:
            self.validation_label.setText("")