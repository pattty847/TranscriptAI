# TranscriptAI 🎙️🤖

> A modern desktop application for downloading videos, transcribing with GPU-accelerated AI, and analyzing content with local LLMs. Process URLs or local files with ease.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

---

## 📸 Screenshots

<div align="center">

| Download & Transcribe | AI Analysis |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/placeholder-image-1" alt="Download Tab" width="100%"/> | <img src="https://github.com/user-attachments/assets/placeholder-image-2" alt="Analysis Tab" width="100%"/> |

*Modern tabbed interface with real-time progress tracking and intuitive controls*

</div>

---

## ✨ Key Features

### 🎯 Universal Video Processing
- **1000+ Supported Sites**: YouTube, TikTok, Twitter, Vimeo, Reddit, Twitch, and more
- **Local File Support**: Browse and process local video files directly
- **Mixed Input Processing**: Process URLs and local files simultaneously
- **Smart File Management**: Copy files to organized assets/ folder or process in-place

### 🚀 GPU-Accelerated Transcription
- **Whisper AI Integration**: State-of-the-art speech recognition
- **CUDA Support**: Leverage your NVIDIA GPU for fast transcription
- **Multiple Model Sizes**: From tiny.en (fast) to large-v3 (accurate)
- **Real-Time Progress**: Visual progress tracking with time-based estimation
- **Smart Filenames**: Auto-generated transcript names with duplicate handling

### 🤖 Local AI Analysis
- **Privacy-First**: All analysis runs locally using Ollama
- **Comprehensive Analysis**: Summaries, quotes, topics, and sentiment
- **Custom Prompts**: Define your own analysis queries
- **Multiple Models**: Support for llama3.2, mistral, codellama, and more

### 🎨 Modern User Interface
- **Dark Theme**: Beautiful, eye-friendly interface
- **Intuitive Workflow**: Tabbed navigation (Download → Analysis → Results)
- **Real-Time Feedback**: Progress bars, status indicators, and validation
- **Clickable Paths**: Quick access to output folders
- **Copy to Clipboard**: One-click copying of transcripts and paths
- **Processing Queue**: Visual queue display for batch operations

### 📁 Organized Storage
- **Centralized Assets**: All content organized in `assets/` folder
- **Smart Organization**: Separate folders for videos, transcripts, and analysis
- **Easy Access**: Click folder paths to open in file explorer

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (3.12 recommended)
- **NVIDIA GPU** with CUDA support (recommended for Whisper)
- **Ollama** installed and running (for AI analysis)
- **Windows 10/11** (tested, may work on Linux/Mac)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/yourusername/TranscriptAI.git
   cd TranscriptAI
   ```

2. **Set up virtual environment and install dependencies**
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment (Windows)
   .venv\Scripts\activate
   
   # Install dependencies
   uv pip install -r requirements.txt
   ```

3. **Install CUDA-enabled PyTorch** (for GPU acceleration)
   ```bash
   uv pip install torch==2.4.1+cu121 --index-url https://download.pytorch.org/whl/cu121
   ```

4. **Set up Ollama** (for AI analysis)
   ```bash
   # Download from https://ollama.ai
   # Pull a model (e.g., llama3.2)
   ollama pull llama3.2
   ```

5. **Launch the application**
   ```bash
   python run.py
   ```
   Or use the Windows launcher:
   ```bash
   TranscriptAI.bat
   ```

---

## 📖 Usage Guide

### Download & Transcribe

1. **Enter Video URL or Select Local Files**
   - Paste any video URL in the input field, or
   - Click "📁 Browse" to select local video files
   - Mix URLs and files: `https://youtube.com/watch?v=abc; C:/videos/file.mp4`

2. **Configure Settings**
   - **Whisper Model**: Choose accuracy vs speed (medium.en recommended)
   - **Keep Video**: Keep downloaded videos after transcription
   - **Copy Files**: Copy local files to assets/ folder (or process in-place)
   - **Download Only**: Skip transcription, just download videos

3. **Start Processing**
   - Click "🚀 Start Download & Transcription"
   - Watch real-time progress in the queue and progress bars
   - View detailed logs in the process log section

### AI Analysis

1. **Transcript Auto-Loads**
   - After transcription, automatically navigates to Analysis tab
   - Transcript is ready for analysis

2. **Select AI Model**
   - Choose from available Ollama models (llama3.2 recommended)
   - Click "🤖 Analyze with AI"

3. **View Results**
   - **Summary**: Concise overview of content
   - **Quotes**: Most memorable and quotable moments
   - **Topics**: Key themes and subjects discussed
   - **Sentiment**: Emotional tone analysis
   - **Custom**: Run your own analysis prompts

4. **Copy Transcript**
   - Click "📋 Copy Transcript" to copy full text to clipboard

### Results & Export

1. **Review Analysis**
   - Navigate through result tabs
   - View formatted analysis results

2. **Export Options**
   - Multiple formats: JSON, Markdown, HTML, PDF, TXT
   - Copy to clipboard
   - Save to file

---

## 🏗️ Project Structure

```
TranscriptAI/
├── src/
│   ├── config/           # Path configuration
│   ├── core/             # Business logic (downloader, transcriber, analyzer)
│   └── ui/               # User interface components
├── assets/               # Generated content
│   ├── videos/           # Downloaded videos
│   ├── transcripts/      # Generated transcripts
│   └── analysis/         # Analysis results (future)
├── requirements.txt      # Python dependencies
└── run.py               # Application entry point
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, AsyncIO for non-blocking operations
- **UI Framework**: PySide6 (Qt for Python) with custom dark theme
- **Video Download**: yt-dlp (supports 1000+ sites)
- **Transcription**: OpenAI Whisper with PyTorch CUDA
- **AI Analysis**: Ollama for local LLM inference
- **Package Management**: uv for fast dependency resolution

---

## 📋 Features in Detail

### Universal Video Download
- Supports any site that yt-dlp supports (YouTube, TikTok, Twitter, Vimeo, etc.)
- Automatic format selection (best quality MP4)
- Progress tracking with download speed and ETA
- Error handling and retry logic

### Local File Processing
- Browse and select multiple video files
- Support for MP4, AVI, MOV, MKV, WebM, FLV, WMV, M4V, 3GP
- Option to copy files to assets/ or process in-place
- Automatic duplicate handling

### Mixed Input Processing
- Process URLs and local files in the same batch
- Real-time input validation
- Visual feedback showing URL/file counts
- Sequential processing with queue visualization

### GPU-Accelerated Transcription
- CUDA acceleration for NVIDIA GPUs
- Multiple Whisper model sizes:
  - `tiny.en`: Fastest, lower accuracy
  - `base.en`: Fast, good for short videos
  - `small.en`: Balanced speed/accuracy
  - `medium.en`: Recommended default
  - `large-v3`: Best accuracy, slower
- Real-time progress estimation
- Smart transcript filename generation

### AI-Powered Analysis
- **Summaries**: Concise overviews of content
- **Quotes**: Extract most memorable moments
- **Topics**: Identify key themes and subjects
- **Sentiment**: Analyze emotional tone
- **Custom**: User-defined analysis prompts
- All processing happens locally (privacy-first)

### Modern UI Features
- Dark theme with teal accents
- Real-time progress indicators
- Color-coded status messages
- Clickable folder paths (open in explorer)
- Copy buttons for quick clipboard access
- Processing queue visualization
- Input validation with visual feedback

---

## ⚙️ Configuration

### Changing Default Paths

Edit `src/config/paths.py`:
```python
class ProjectPaths:
    BASE_DIR = Path.cwd()
    ASSETS_DIR = BASE_DIR / "assets"  # Change this
    VIDEOS_DIR = ASSETS_DIR / "videos"
    TRANSCRIPTS_DIR = ASSETS_DIR / "transcripts"
```

### Changing Default Models

**Whisper Model**: Edit `src/ui/download_tab.py`
```python
self.model_combo.setCurrentText("large-v3")  # Change default
```

**AI Model**: Edit `src/ui/analysis_tab.py`
```python
self.model_combo.addItems([
    "llama3.2", "your-preferred-model"  # Add your model first
])
```

---

## 🐛 Troubleshooting

### CUDA Issues
**Problem**: "torch.cuda.is_available() is False"
- Install CUDA-enabled PyTorch: `uv pip install torch==2.4.1+cu121 --index-url https://download.pytorch.org/whl/cu121`
- Ensure Python version ≤ 3.12
- Verify NVIDIA drivers are up to date

### Transcription Progress Not Updating
**Problem**: Progress bar stuck at 0%
- Install ffmpeg (includes ffprobe) for audio duration detection
- Progress uses time-based estimation (2.5x audio duration)
- Check terminal output for actual Whisper progress

### Ollama Connection Issues
**Problem**: "Model not available"
- Ensure Ollama is running: `ollama serve`
- Pull required models: `ollama pull llama3.2`
- Check firewall isn't blocking localhost

### Import Errors
**Problem**: ModuleNotFoundError
- Activate virtual environment: `.venv\Scripts\activate`
- Install dependencies: `uv pip install -r requirements.txt`
- Check Python path matches your setup

---

## 📝 Requirements

- **OS**: Windows 10/11 (tested), Linux/Mac (may work)
- **Python**: 3.11+ (3.12 recommended)
- **RAM**: 8GB+ recommended
- **GPU**: NVIDIA GPU with CUDA support (recommended)
- **Storage**: ~2GB for models and dependencies
- **Internet**: Required for downloads and model fetching

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for universal video download support
- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Ollama](https://ollama.ai/) for local LLM inference
- [PySide6](https://www.qt.io/qt-for-python) for the UI framework

---

**Built with ❤️ for content creators, researchers, and anyone who wants to extract maximum value from video content.**

*Transform videos into insights, one transcript at a time.* 🚀
