"""
Worker thread for downloading and transcribing videos
"""
import asyncio
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from src.core.processor import UnifiedProcessor


class DownloadWorker(QThread):
    """Worker thread for downloading and transcribing"""
    progress_updated = Signal(str)  # Progress message
    download_progress = Signal(float)  # Download percentage
    transcription_progress = Signal(float)  # Transcription percentage
    completed = Signal(Path, str)  # (file_path, transcript_text)
    batch_completed = Signal(object)  # List[tuple[Path, str]]
    error_occurred = Signal(str)  # Error message
    
    def __init__(
        self,
        input_text: str,
        model: str = "medium.en",
        download_only: bool = False,
        keep_video: bool = False,
        copy_files: bool = True,
        youtube_captions_first: bool = True,
        use_browser_cookies: bool = True,
        caption_retry_count: int = 3,
        caption_backoff_seconds: float = 8.0,
        caption_batch_delay_seconds: float = 2.0,
    ):
        super().__init__()
        self.input_text = input_text  # Changed from self.url
        self.model = model
        self.download_only = download_only
        self.keep_video = keep_video
        self.copy_files = copy_files
        self.youtube_captions_first = youtube_captions_first
        self.use_browser_cookies = use_browser_cookies
        self.caption_retry_count = caption_retry_count
        self.caption_backoff_seconds = caption_backoff_seconds
        self.caption_batch_delay_seconds = caption_batch_delay_seconds
        
        # Use unified processor
        self.processor = UnifiedProcessor(
            model=model,
            download_only=download_only,
            keep_video=keep_video,
            copy_files=copy_files,
            youtube_captions_first=youtube_captions_first,
            use_browser_cookies=use_browser_cookies,
            caption_retry_count=caption_retry_count,
            caption_backoff_seconds=caption_backoff_seconds,
            caption_batch_delay_seconds=caption_batch_delay_seconds,
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

            completed_items = []
            errors = []

            for result in results:
                if result.status == "completed":
                    if result.transcript_path:
                        transcript_text = result.transcript_path.read_text(encoding="utf-8")
                        payload = (result.transcript_path, transcript_text)
                        completed_items.append(payload)
                        self.completed.emit(*payload)
                    elif result.video_path:
                        payload = (result.video_path, "")
                        completed_items.append(payload)
                        self.completed.emit(*payload)
                elif result.status == "error":
                    errors.append(result.error_message or f"Failed to process: {result.source}")

            self.batch_completed.emit(completed_items)
            if errors:
                self.error_occurred.emit("; ".join(errors))

        except Exception as e:
            self.error_occurred.emit(f"Process failed: {str(e)}")

