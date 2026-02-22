"""
Web server for Subtext: URL or file upload -> download (yt-dlp) -> transcribe (Whisper).
Reuses core processor; reachable on 0.0.0.0 for home network (e.g. from phone).
"""
import asyncio
import uuid
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.config.paths import ProjectPaths
from src.core.processor import UnifiedProcessor, ProcessingItem
from src.core.downloader import DownloadProgress
from src.core.transcriber import TranscriptionProgress

# Ensure assets exist
ProjectPaths.initialize()

app = FastAPI(title="Subtext Web", description="Transcribe video from URL or upload")
JOBS: dict[str, dict[str, Any]] = {}

WHISPER_MODELS = ["tiny.en", "base.en", "small.en", "medium.en", "large-v3"]


def _update_job(job_id: str, **kwargs: Any) -> None:
    if job_id in JOBS:
        JOBS[job_id].update(kwargs)


@app.post("/api/transcribe")
async def create_transcribe_job(
    model: str = Form("small.en"),
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = None,
) -> dict[str, str]:
    """Start a transcription job. Provide either `url` or `file`, not both."""
    if not url and not file:
        raise HTTPException(400, "Provide either a URL or an uploaded file.")
    if url and file:
        raise HTTPException(400, "Provide either a URL or a file, not both.")

    model = (model or "small.en").strip()
    if model not in WHISPER_MODELS:
        model = "small.en"

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        "status": "pending",
        "progress": 0.0,
        "message": "Starting…",
        "transcript": None,
        "error": None,
    }

    if url:
        input_text = url.strip()
    else:
        # Save uploaded file to assets/videos with a unique name
        assert file is not None
        suffix = Path(file.filename or "upload").suffix or ".mp4"
        safe_name = f"web_upload_{job_id}{suffix}"
        dest = ProjectPaths.VIDEOS_DIR / safe_name
        content = await file.read()
        dest.write_bytes(content)
        input_text = str(dest)

    asyncio.create_task(_run_job(job_id, input_text, model))
    return {"job_id": job_id}


async def _run_job(job_id: str, input_text: str, model: str) -> None:
    _update_job(job_id, status="running", message="Processing…")

    def progress_cb(msg: str) -> None:
        _update_job(job_id, message=msg)

    def download_cb(dp: DownloadProgress) -> None:
        _update_job(job_id, progress=dp.percent, message=f"Downloading… {dp.percent:.1f}%")

    def transcription_cb(tp: TranscriptionProgress) -> None:
        _update_job(job_id, progress=tp.percent, message=tp.message)

    processor = UnifiedProcessor(
        model=model,
        download_only=False,
        keep_video=False,
        copy_files=False,
        youtube_captions_first=True,
        use_browser_cookies=True,
    )
    try:
        results = await processor.process_mixed_input(
            input_text,
            progress_callback=progress_cb,
            download_progress_callback=download_cb,
            transcription_progress_callback=transcription_cb,
        )
        item: Optional[ProcessingItem] = results[0] if results else None
        if item and item.status == "completed" and item.transcript_path and item.transcript_path.exists():
            transcript = item.transcript_path.read_text(encoding="utf-8")
            _update_job(
                job_id,
                status="completed",
                progress=100.0,
                message="Done",
                transcript=transcript,
            )
        elif item and item.status == "error" and item.error_message:
            _update_job(job_id, status="error", error=item.error_message)
        else:
            _update_job(job_id, status="error", error="No transcript produced.")
    except Exception as e:
        _update_job(job_id, status="error", error=str(e))


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str) -> dict[str, Any]:
    """Get current job status and result."""
    if job_id not in JOBS:
        raise HTTPException(404, "Job not found.")
    return JOBS[job_id]


# Static files (HTML, CSS, JS)
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    index_html = STATIC_DIR / "index.html"
    if not index_html.exists():
        raise HTTPException(404, "Static files not found. Run from project root.")
    return HTMLResponse(content=index_html.read_text(encoding="utf-8"))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
