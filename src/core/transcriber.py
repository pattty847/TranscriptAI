"""
Modern audio transcription with Whisper AI
"""
import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Optional
import whisper


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

    async def transcribe(self, audio_path: Path, progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None) -> str:
        """Transcribe audio file to text"""
        
        if self.model is None:
            await self.load_model(progress_callback)
            
        progress = TranscriptionProgress()
        progress.stage = "processing"
        progress.message = f"Transcribing {audio_path.name}..."
        if progress_callback:
            progress_callback(progress)
            
        loop = asyncio.get_event_loop()
        
        def _transcribe():
            result = self.model.transcribe(str(audio_path), fp16=True, verbose=False)
            return result["text"].strip()
            
        try:
            transcript = await loop.run_in_executor(None, _transcribe)
            
            progress.stage = "saving"
            progress.percent = 100.0
            progress.message = "Transcription complete"
            if progress_callback:
                progress_callback(progress)
                
            return transcript
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

    async def transcribe_and_save(self, audio_path: Path, output_path: Optional[Path] = None, transcripts_dir: Optional[Path] = None, progress_callback: Optional[Callable[[TranscriptionProgress], None]] = None) -> tuple[str, Path]:
        """Transcribe and save to file, returns (transcript_text, output_file_path)"""
        
        transcript = await self.transcribe(audio_path, progress_callback)
        
        if output_path is None:
            # Save to organized transcripts directory
            if transcripts_dir:
                output_path = transcripts_dir / f"{audio_path.stem}.txt"
            else:
                output_path = audio_path.with_suffix('.txt')
            
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