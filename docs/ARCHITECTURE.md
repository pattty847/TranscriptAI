# Subtext Architecture

This document describes the current structure and data flow of Subtext.

## Overview

Subtext is a PySide6 desktop app with asynchronous core services and QThread workers.

High-level flow:

```text
Input URLs/files -> Download/Captions -> Transcription -> LLM Analysis -> Export
```

## Layers

## UI Layer (`src/ui`)

- `main_window.py`: app shell, toolbar, tab coordination
- `download_tab.py`: input, queue, progress, process logs
- `analysis_tab.py`: transcript review, model controls, analysis actions
- `results_tab.py`: formatted results + export
- `workers/`: thread workers that bridge Qt signals to async core logic

## Core Layer (`src/core`)

- `input_processor.py`: parse/validate mixed URL + file input
- `downloader.py`: media downloads + YouTube caption retrieval and parsing
- `transcriber.py`: Whisper model loading/transcription/saving
- `analyzer.py`: Ollama model management + analysis prompts
- `processor.py`: orchestration across downloader/transcriber with fallback paths

## Config Layer (`src/config`)

- `paths.py`: centralized project paths (`assets/videos`, `assets/transcripts`, `assets/analysis`)

## Key Runtime Patterns

1. UI thread remains responsive.
2. Heavy tasks run in `QThread` workers.
3. Each worker creates its own asyncio event loop.
4. UI updates occur only through Qt signals.

## Download + Transcript Pipeline

For each queue item:

1. Parse item type (`URL` or `file`)
2. If URL and YouTube captions-first enabled:
   - try subtitle fetch/parsing first
   - if success: produce transcript immediately
   - if fail/rate-limited: fallback to media download + Whisper
3. If local file:
   - copy to assets or use in-place (configurable)
4. Transcribe with Whisper unless bypassed by captions or download-only mode
5. Save transcript and emit completion signals

Notes:
- Caption requests use retry/backoff + optional browser cookies.
- Batch processing is sequential (intentional for memory stability).
- Whisper device is auto-selected (`cuda` -> `mps` -> `cpu` fallback).
- Whisper transcription requires FFmpeg binaries (`ffmpeg`/`ffprobe`) on PATH.
- Whisper resources are explicitly unloaded after processing.

## Analysis Pipeline

1. Ensure Ollama model availability (supports alias resolution like `llama3.2` -> `llama3.2:latest`)
2. Run separate prompt-driven tasks:
   - summary
   - quotes
   - topics
   - sentiment
3. Populate `AnalysisResult`
4. Emit to Results tab

Memory behavior:
- Ollama requests use `keep_alive="0s"` to release model memory between calls.
- Analysis is sequential to reduce RAM spikes.

## Export Pipeline

Results tab supports:
- JSON
- Markdown
- HTML
- PDF (Qt printer)
- TXT

## Signal Routing

```text
DownloadTab.transcription_completed -> MainWindow -> AnalysisTab.load_transcript
AnalysisTab.analysis_completed -> MainWindow -> ResultsTab.load_results
```

## Web Layer (`src/web`)

- `server.py`: FastAPI app; POST `/api/transcribe` (URL or file + model), GET `/api/jobs/{id}` for status/result. Serves static HTML/CSS/JS.
- `static/`: Single-page UI — URL input, file upload, Whisper model select, progress, transcript with copy/download. Designed for use from phone or desktop on the same network.
- Launched with `run_web.py` (uvicorn on `0.0.0.0:8765`). Reuses `UnifiedProcessor`, `ProjectPaths`, and existing download/Whisper behaviour.

## Current Directory Layout

```text
src/
  config/
  core/
  ui/
    workers/
    widgets/
  web/
    static/   (index.html, style.css, app.js)
    server.py
docs/
  ARCHITECTURE.md
scripts/
  build_exe.py
  install_cuda.bat
assets/
```

## Extension Points

- Add analysis types in `src/core/analyzer.py` + corresponding UI/result tabs.
- Add export formats in `src/ui/results_tab.py`.
- Add new input options in `src/ui/widgets/multi_select_dropdown.py`.
- Add new processing behavior in `src/core/processor.py`.

## Testing Checklist

- URL with captions-first success path
- URL with captions fallback to Whisper
- Local file transcription (copy/in-place)
- Batch mixed input flow
- Ollama model refresh/install/test in Analysis tab
- Export each format from Results tab
