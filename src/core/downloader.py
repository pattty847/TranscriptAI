"""
Modern YouTube downloader with progress tracking
"""
import asyncio
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Optional
import yt_dlp

from src.config.paths import ProjectPaths


class DownloadProgress:
    def __init__(self):
        self.percent = 0.0
        self.speed = ""
        self.eta = ""
        self.filename = ""

    def __str__(self):
        return f"{self.percent:.1f}% - {self.speed} - ETA: {self.eta}"


class UniversalDownloader:
    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            # Use new assets structure
            self.downloads_dir = ProjectPaths.VIDEOS_DIR
            self.transcripts_dir = ProjectPaths.TRANSCRIPTS_DIR
        else:
            self.downloads_dir = output_dir / "videos"
            self.transcripts_dir = output_dir / "transcripts"
        
        # Ensure directories exist
        ProjectPaths.ensure_directories()
        
        # Keep backwards compatibility
        self.output_dir = self.downloads_dir
        
    def _progress_hook(self, d, callback: Optional[Callable[[DownloadProgress], None]] = None):
        """Progress callback for yt-dlp"""
        if callback and d['status'] == 'downloading':
            progress = DownloadProgress()
            
            # Clean and parse percentage
            percent_str = d.get('_percent_str', '0')
            if percent_str:
                # Remove ANSI codes and non-numeric characters except decimal point
                import re
                clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', str(percent_str))  # Remove ANSI codes
                clean_percent = re.sub(r'[^\d.]', '', clean_percent)  # Keep only digits and decimal
                try:
                    progress.percent = float(clean_percent) if clean_percent else 0.0
                except ValueError:
                    progress.percent = 0.0
            else:
                progress.percent = 0.0
                
            progress.speed = d.get('_speed_str', '')
            progress.eta = d.get('_eta_str', '')
            progress.filename = Path(d.get('filename', '')).name
            callback(progress)

    async def download(self, url: str, progress_callback: Optional[Callable[[DownloadProgress], None]] = None) -> Path:
        """Download video and return path to downloaded file"""
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': str(self.output_dir / '%(title).80B [%(id)s].%(ext)s'),
            'restrictfilenames': True,
            'windowsfilenames': True,
            'progress_hooks': [lambda d: self._progress_hook(d, progress_callback)],
            'quiet': True,
            'no_warnings': True,
            'no_color': True,  # Disable ANSI color codes
        }
        
        # Run download in thread to avoid blocking UI
        loop = asyncio.get_event_loop()
        
        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Get the actual filename
                filename = ydl.prepare_filename(info)
                return Path(filename)
        
        try:
            filepath = await loop.run_in_executor(None, _download)
            return filepath
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")


async def test_downloader():
    """Test the downloader"""
    downloader = UniversalDownloader()
    
    def progress_callback(progress: DownloadProgress):
        print(f"\r{progress}", end="", flush=True)
    
    try:
        # Test with a short video (works with any supported site)
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - short and safe for testing
        filepath = await downloader.download(url, progress_callback)
        print(f"\nDownloaded: {filepath}")
        return filepath
    except Exception as e:
        print(f"\nError: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(test_downloader())