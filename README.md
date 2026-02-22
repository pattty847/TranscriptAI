# Subtext

Desktop app for downloading media, generating transcripts, and running local AI analysis.

## What It Does

- Download videos/audio from URLs (`yt-dlp`)
- Process local media files
- Generate transcripts with:
  - YouTube captions first (fast path, when available)
  - Whisper fallback
- Analyze transcripts locally with Ollama (summary, quotes, topics, sentiment)
- Export analysis to JSON/Markdown/HTML/PDF/TXT

## Requirements

- Windows 10/11 or macOS
- Python 3.11+
- `uv` installed: https://docs.astral.sh/uv/getting-started/installation/
- FFmpeg (`ffmpeg` and `ffprobe` on PATH): https://www.ffmpeg.org/download.html
- Optional but recommended:
  - Ollama for analysis
  - NVIDIA CUDA for faster Whisper on supported Windows/Linux systems

## Quick Start

```bash
uv sync
uv run python run.py
```

Launch helpers:
- Windows: double-click `win-launch.bat`
- macOS/Linux: run `./mac-launch`

## FFmpeg Setup

Whisper transcription requires FFmpeg.

1. Install from: https://www.ffmpeg.org/download.html
2. Make sure both `ffmpeg` and `ffprobe` are available in your terminal `PATH`.
3. Restart Subtext after installation.

## First-Time Setup (AI Analysis)

1. Install Ollama: https://ollama.com/download/windows
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. In Subtext:
   - Analysis tab -> `Refresh Models`
   - Select model
   - Click `Test Model`

## Recommended Workflow

1. Paste URL(s) or browse local files
2. Keep `YouTube Captions First` enabled for fast transcript generation on YouTube
3. Click `Start`
4. Review/edit transcript in Analysis tab
5. Run AI analysis and export results

## Optional CUDA Setup

If you want GPU acceleration for Whisper:

```bash
scripts\install_cuda.bat
```

Whisper device selection is automatic:
- `cuda` when available
- `mps` on supported Apple Silicon setups
- `cpu` fallback otherwise

## Project Structure

```text
Subtext/
  src/
    config/        # paths and app configuration
    core/          # downloader, transcriber, analyzer, processor
    ui/            # window, tabs, workers, widgets, styles
  docs/
    ARCHITECTURE.md
  scripts/
    build_exe.py
    install_cuda.bat
  assets/          # generated files (videos/transcripts/analysis)
```

## Web UI (same network)

Run a minimal web interface so you can transcribe from your phone or another device on your home network:

```bash
uv run python run_web.py
```

- On this PC: open **http://127.0.0.1:8765**
- From iPhone/tablet (same Wi‑Fi): open **http://\<this-PC-IP\>:8765**  
  (Find IP: `ipconfig` on Windows, `ip addr` or System Settings on Mac/Linux.)

Paste a video URL (YouTube, Instagram, X, TikTok, etc.) or upload a file, pick a Whisper model, then copy or download the transcript. Uses the same yt-dlp and Whisper setup as the desktop app.

## Useful Commands

- Run app: `uv run python run.py`
- Run web UI: `uv run python run_web.py`
- Build exe: `uv run python scripts/build_exe.py`
- Update deps: `uv sync --upgrade`
- Check installed models: `ollama list`

## Troubleshooting

- `Could not load model ...`:
  - Ensure Ollama is running and model is installed (`ollama list`)
  - In app click `Refresh Models`

- YouTube caption `429 Too Many Requests`:
  - Use browser cookies option
  - Retry later or switch network
  - App falls back to Whisper automatically

- High memory usage:
  - Use smaller Whisper model (`small.en` / `base.en`)
  - Use smaller Ollama models (`llama3.2:1b`, etc.)
  - Stop active Ollama models: `ollama ps` then `ollama stop <model>`

## License

MIT
