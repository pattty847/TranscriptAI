# TranscriptAI

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

- Windows 10/11
- Python 3.11+
- `uv` installed: https://docs.astral.sh/uv/getting-started/installation/
- Optional but recommended:
  - Ollama for analysis
  - NVIDIA CUDA for faster Whisper

## Quick Start

```bash
uv sync
uv run python run.py
```

Or double-click `TranscriptAI.bat` on Windows.

## First-Time Setup (AI Analysis)

1. Install Ollama: https://ollama.com/download/windows
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. In TranscriptAI:
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

## Project Structure

```text
TranscriptAI/
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

## Useful Commands

- Run app: `uv run python run.py`
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
