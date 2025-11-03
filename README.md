# TranscriptAI 🎙️🤖

A sleek, modern desktop app for downloading, transcribing, and AI-analyzing video content.

## Features
- **Download & Transcribe**: Any video/audio URL → text with Whisper AI
- **AI Analysis**: Local LLM analysis via Ollama
- **Modern UI**: Sleek PySide6 interface with dark theme
- **Smart Processing**: Extract quotes, summaries, topics, sentiment
- **Export Everything**: Multiple formats for your content

## Screenshots
*Modern tabbed interface with real-time progress tracking*

## Prerequisites
- Python 3.11+
- CUDA-capable GPU (recommended for Whisper)
- Ollama installed and running (for AI analysis)

## Quick Start
```bash
# Clone or download the project
# Navigate to the TranscriptAI folder

# Install dependencies (first time only)
uv venv
uv pip install -r requirements.txt

# Launch the app
python run.py
```

## Usage
1. **Download Tab**: Paste any video URL (YouTube, Vimeo, TikTok, etc.), select Whisper model, start transcription
2. **Analysis Tab**: AI-powered analysis with local LLM via Ollama  
3. **Results Tab**: View, export, and share your analysis results

## Tech Stack
- **Backend**: Python 3.13, yt-dlp, OpenAI Whisper
- **Frontend**: PySide6 (Qt for Python)
- **AI**: Ollama for local LLM processing
- **Packaging**: uv for fast dependency management

## Features in Detail

### Download & Transcribe
- **1000+ supported sites**: YouTube, Vimeo, TikTok, Twitter, Reddit, Twitch, podcasts, news sites, educational platforms
- High-quality video/audio download via yt-dlp
- GPU-accelerated transcription with Whisper
- Multiple model sizes (tiny to large-v3)
- Real-time progress tracking

### AI Analysis
- Local LLM processing (privacy-first)
- Automatic summaries and key points
- Quote extraction for memorable moments
- Topic identification and categorization
- Sentiment analysis
- Custom analysis prompts

### Modern UI
- Beautiful dark theme interface
- Tabbed workflow for easy navigation
- Real-time progress indicators
- Export in multiple formats (JSON, Markdown, HTML, PDF, TXT)

## Requirements
- Windows 10/11 (tested)
- 8GB+ RAM recommended
- NVIDIA GPU for optimal Whisper performance
- Internet connection for downloads

Built with ❤️ for content creators who want to extract maximum value from their transcripts.