# Subtext - Lightweight Spec

## Core Vision
A beautiful, modern desktop app that transforms video content into actionable insights through transcription and AI analysis.

## Key Components

### 1. Core Engine (`src/core/`)
- **Downloader**: YouTube video download (yt-dlp wrapper)
- **Transcriber**: Audio → text (Whisper integration) 
- **Analyzer**: Text → insights (Ollama integration)

### 2. Modern UI (`src/ui/`)
- **Main Window**: Tabbed interface with modern styling
- **Download Tab**: URL input, progress tracking, settings
- **Analysis Tab**: AI-powered text analysis with live results
- **Results Tab**: Export, share, and manage processed content

### 3. AI Features
- **Smart Summaries**: Key points extraction
- **Quote Mining**: Most interesting/quotable moments
- **Topic Analysis**: Automatic categorization
- **Sentiment Tracking**: Emotional flow through content
- **Custom Prompts**: User-defined analysis types

## Design Principles
- **Sleek & Modern**: Dark theme by default, clean typography
- **Responsive**: Real-time feedback and progress indication  
- **Intuitive**: One-click workflows with smart defaults
- **Extensible**: Plugin architecture for custom analyzers

## MVP Workflow
1. Paste YouTube URL
2. Download & transcribe (with progress)
3. AI analysis with live streaming results
4. Export in multiple formats

## Tech Choices
- **PySide6**: Native performance, modern Qt widgets
- **Ollama**: Privacy-first local LLM processing
- **Modern Python**: Type hints, async/await, dataclasses