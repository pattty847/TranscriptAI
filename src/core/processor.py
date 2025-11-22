"""
Unified processing pipeline for URLs and local files
"""
import asyncio
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Callable

from src.core.downloader import UniversalDownloader, DownloadProgress
from src.core.transcriber import WhisperTranscriber, TranscriptionProgress
from src.core.input_processor import InputProcessor
from src.config.paths import ProjectPaths


class ProcessingItem:
    """Represents a single item in the processing queue"""
    def __init__(self, source: str, item_type: str, needs_download: bool = False):
        self.source = source
        self.type = item_type  # 'url' or 'file'
        self.needs_download = needs_download
        self.status = "pending"  # pending, downloading, transcribing, analyzing, completed, error
        self.progress = 0.0
        self.error_message = None
        self.video_path: Optional[Path] = None
        self.transcript_path: Optional[Path] = None


class UnifiedProcessor:
    """Unified processor for URLs and local files"""
    
    def __init__(self, model: str = "medium.en", download_only: bool = False, keep_video: bool = False, copy_files: bool = True):
        self.downloader = UniversalDownloader()
        self.transcriber = WhisperTranscriber(model) if not download_only else None
        self.download_only = download_only
        self.keep_video = keep_video
        self.copy_files = copy_files  # Whether to copy local files to assets/
    
    def generate_transcript_filename(self, video_path: Path, source: str) -> str:
        """Generate smart transcript filename"""
        base_name = video_path.stem
        
        # For URLs: try to extract title from video metadata (future enhancement)
        # For now, use video filename
        
        # Clean filename: remove invalid characters
        cleaned = re.sub(r'[<>:"|?*\\]', '', base_name)
        cleaned = cleaned.replace(' ', '_')
        
        # Ensure uniqueness
        counter = 1
        filename = f"{cleaned}.txt"
        while (ProjectPaths.TRANSCRIPTS_DIR / filename).exists():
            filename = f"{cleaned}_{counter}.txt"
            counter += 1
        
        return filename
    
    async def process_mixed_input(self, input_text: str, 
                                  progress_callback: Optional[Callable[[str], None]] = None,
                                  download_progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
                                  transcription_progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None) -> List[ProcessingItem]:
        """Process mixed input (URLs and files)"""
        
        # Parse input
        items = InputProcessor.parse_mixed_input(input_text)
        
        # Create processing queue
        queue: List[ProcessingItem] = []
        
        # Add URLs to queue
        for url in items["urls"]:
            queue.append(ProcessingItem(url, "url", needs_download=True))
        
        # Add files to queue
        for file_path in items["files"]:
            queue.append(ProcessingItem(file_path, "file", needs_download=False))
        
        # Process queue sequentially
        results = []
        for item in queue:
            try:
                result = await self.process_single_item(
                    item,
                    progress_callback,
                    download_progress_callback,
                    transcription_progress_callback
                )
                results.append(result)
            except Exception as e:
                item.status = "error"
                item.error_message = str(e)
                results.append(item)
        
        return results
    
    async def process_single_item(self, item: ProcessingItem,
                                  progress_callback: Optional[Callable[[str], None]] = None,
                                  download_progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
                                  transcription_progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None) -> ProcessingItem:
        """Process single URL or file"""
        
        if progress_callback:
            progress_callback(f"Processing {item.source}...")
        
        # Step 1: Get video file
        if item.needs_download:
            # Download URL
            item.status = "downloading"
            video_path = await self.downloader.download(item.source, download_progress_callback)
            item.video_path = video_path
        else:
            # Handle local file
            source_path = Path(item.source)
            
            if self.copy_files:
                # Copy to assets/videos/
                item.status = "copying"
                if progress_callback:
                    progress_callback(f"Copying {source_path.name} to assets/videos/...")
                
                dest_path = ProjectPaths.VIDEOS_DIR / source_path.name
                # Handle duplicates
                counter = 1
                while dest_path.exists():
                    stem = source_path.stem
                    dest_path = ProjectPaths.VIDEOS_DIR / f"{stem}_{counter}{source_path.suffix}"
                    counter += 1
                
                shutil.copy2(source_path, dest_path)
                item.video_path = dest_path
            else:
                # Use file in-place
                item.video_path = source_path
        
        # Step 2: Transcribe (if not download-only)
        if not self.download_only and self.transcriber:
            item.status = "transcribing"
            
            # Generate transcript filename
            transcript_name = self.generate_transcript_filename(item.video_path, item.source)
            transcript_path = ProjectPaths.TRANSCRIPTS_DIR / transcript_name
            
            # Transcribe
            transcript_text, saved_path = await self.transcriber.transcribe_and_save(
                item.video_path,
                output_path=transcript_path,
                transcripts_dir=ProjectPaths.TRANSCRIPTS_DIR,
                progress_callback=transcription_progress_callback
            )
            
            item.transcript_path = saved_path
            
            # Clean up video if not keeping it
            if not self.keep_video and item.video_path.exists():
                try:
                    item.video_path.unlink()
                except Exception:
                    pass
        
        item.status = "completed"
        item.progress = 100.0
        
        return item

