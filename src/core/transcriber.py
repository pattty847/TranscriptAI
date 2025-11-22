"""
Modern audio transcription with Whisper AI
"""
import asyncio
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Callable, Optional
import whisper

from src.config.paths import ProjectPaths


class TranscriptionProgress:
    def __init__(self):
        self.stage = "loading"  # loading, processing, saving
        self.percent = 0.0
        self.message = ""

    def __str__(self):
        return f"{self.stage.title()}: {self.message} ({self.percent:.1f}%)"


class WhisperTranscriber:
    def __init__(self, model_name: str = "medium.en", device: str = "cuda"):
        self.model_name = model_name
        self.device = device
        self.model = None
        
    async def load_model(self, progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None):
        """Load Whisper model asynchronously"""
        if self.model is not None:
            return
            
        progress = TranscriptionProgress()
        progress.stage = "loading"
        progress.message = f"Loading {self.model_name} model..."
        if progress_callback:
            progress_callback(progress)
            
        loop = asyncio.get_event_loop()
        
        def _load_model():
            return whisper.load_model(self.model_name, device=self.device)
            
        self.model = await loop.run_in_executor(None, _load_model)
        
        progress.percent = 100.0
        progress.message = "Model loaded successfully"
        if progress_callback:
            progress_callback(progress)

    def _get_audio_duration(self, audio_path: Path) -> float:
        """Get audio duration in seconds using ffprobe"""
        try:
            result = subprocess.run(
                [
                    'ffprobe', '-v', 'error', '-show_entries',
                    'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
                    str(audio_path)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return float(result.stdout.strip())
        except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
            pass
        return 0.0
    
    async def transcribe(self, audio_path: Path, progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None) -> str:
        """Transcribe audio file to text"""
        
        if self.model is None:
            await self.load_model(progress_callback)
        
        # Get audio duration for progress estimation
        audio_duration = self._get_audio_duration(audio_path)
        start_time = time.time()
        last_progress_update = 0.0
        transcription_complete = threading.Event()
        
        progress = TranscriptionProgress()
        progress.stage = "processing"
        progress.message = f"Transcribing {audio_path.name}..."
        progress.percent = 0.0
        if progress_callback:
            progress_callback(progress)
        
        # Background thread to update progress based on elapsed time
        progress_thread = None
        if progress_callback:
            def update_progress_periodically():
                nonlocal last_progress_update
                update_count = 0
                while not transcription_complete.is_set():
                    elapsed = time.time() - start_time
                    
                    if audio_duration > 0:
                        # Estimate progress: transcription typically takes 2-3x audio duration on GPU
                        # Use a conservative estimate of 2.5x duration
                        estimated_total_time = audio_duration * 2.5
                        estimated_percent = min(95.0, (elapsed / estimated_total_time) * 100)
                    else:
                        # Fallback: show indeterminate progress that slowly increases
                        # Update every 2 seconds, cap at 90% until complete
                        update_count += 1
                        estimated_percent = min(90.0, update_count * 2.0)  # 2% per update, max 90%
                    
                    # Only update if progress increased by at least 0.5%
                    if estimated_percent - last_progress_update >= 0.5:
                        last_progress_update = estimated_percent
                        progress_obj = TranscriptionProgress()
                        progress_obj.stage = "processing"
                        progress_obj.percent = estimated_percent
                        if audio_duration > 0:
                            progress_obj.message = f"Transcribing... {estimated_percent:.1f}%"
                        else:
                            progress_obj.message = f"Transcribing... ({int(elapsed)}s elapsed)"
                        progress_callback(progress_obj)
                    
                    time.sleep(0.5)  # Update every 500ms
            
            progress_thread = threading.Thread(target=update_progress_periodically, daemon=True)
            progress_thread.start()
        
        loop = asyncio.get_event_loop()
        
        def _transcribe():
            # Use verbose mode to see progress in terminal, but we estimate progress via time
            result = self.model.transcribe(str(audio_path), fp16=True, verbose=True)
            transcription_complete.set()  # Signal that transcription is done
            return result["text"].strip()
            
        try:
            transcript = await loop.run_in_executor(None, _transcribe)
            
            # Wait a moment for final progress update
            if progress_thread:
                progress_thread.join(timeout=1.0)
            
            progress.stage = "saving"
            progress.percent = 100.0
            progress.message = "Transcription complete"
            if progress_callback:
                progress_callback(progress)
                
            return transcript
            
        except Exception as e:
            transcription_complete.set()  # Signal error
            if progress_thread:
                progress_thread.join(timeout=0.5)
            raise Exception(f"Transcription failed: {str(e)}")

    async def transcribe_and_save(self, audio_path: Path, output_path: Optional[Path] = None, transcripts_dir: Optional[Path] = None, progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None) -> tuple[str, Path]:
        """Transcribe and save to file, returns (transcript_text, output_file_path)"""
        
        transcript = await self.transcribe(audio_path, progress_callback)
        
        if output_path is None:
            # Save to organized transcripts directory
            if transcripts_dir:
                output_path = transcripts_dir / f"{audio_path.stem}.txt"
            else:
                # Use default transcripts directory
                ProjectPaths.ensure_directories()
                output_path = ProjectPaths.TRANSCRIPTS_DIR / f"{audio_path.stem}.txt"
            
        progress = TranscriptionProgress()
        progress.stage = "saving"
        progress.message = f"Saving to {output_path.name}..."
        progress.percent = 90.0
        if progress_callback:
            progress_callback(progress)
            
        output_path.write_text(transcript, encoding='utf-8')
        
        progress.percent = 100.0
        progress.message = f"Saved to {output_path.name}"
        if progress_callback:
            progress_callback(progress)
            
        return transcript, output_path


async def test_transcriber():
    """Test the transcriber with a sample file"""
    transcriber = WhisperTranscriber()
    
    def progress_callback(progress: TranscriptionProgress):
        print(f"\r{progress}", end="", flush=True)
    
    # For testing, you'd need an actual audio file
    # audio_path = Path("test_audio.mp4")
    # if audio_path.exists():
    #     transcript, output_file = await transcriber.transcribe_and_save(audio_path, progress_callback=progress_callback)
    #     print(f"\nTranscript saved to: {output_file}")
    #     print(f"First 200 chars: {transcript[:200]}...")
    # else:
    #     print("No test audio file found")
    
    print("Transcriber ready for use")


if __name__ == "__main__":
    asyncio.run(test_transcriber())