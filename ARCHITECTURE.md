# TranscriptAI Architecture Documentation 🏗️

A comprehensive guide to understanding, extending, and modifying TranscriptAI.

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [UI Components](#ui-components)
5. [Data Flow](#data-flow)
6. [File Organization](#file-organization)
7. [Key Design Patterns](#key-design-patterns)
8. [Adding Features](#adding-features)
9. [Common Modifications](#common-modifications)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

TranscriptAI is a modern desktop application for downloading videos from 1000+ websites, transcribing them with GPU-accelerated AI, and analyzing content with local LLMs.

### Key Features
- **Universal Video Download**: yt-dlp supports YouTube, TikTok, Twitter, Vimeo, etc.
- **GPU-Accelerated Transcription**: CUDA-optimized Whisper AI
- **Local AI Analysis**: Privacy-first analysis using Ollama
- **Modern UI**: Dark-themed PySide6 interface
- **Organized Storage**: Automatic folder organization
- **Flexible Workflows**: Download-only or full transcription+analysis

### Tech Stack
- **Backend**: Python 3.12, AsyncIO for non-blocking operations
- **UI**: PySide6 (Qt for Python) with custom dark theme
- **Video Download**: yt-dlp (fork of youtube-dl)
- **Transcription**: OpenAI Whisper with PyTorch CUDA
- **AI Analysis**: Ollama for local LLM inference
- **Dependencies**: uv for fast package management

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   UI Layer                      │
│  ┌─────────────┬─────────────┬─────────────┐    │
│  │ Download    │ Analysis    │ Results     │    │
│  │ Tab         │ Tab         │ Tab         │    │
│  └─────────────┴─────────────┴─────────────┘    │
└─────────────────┬───────────────────────────────┘
                  │ Qt Signals/Slots
┌─────────────────┴───────────────────────────────┐
│                Core Layer                       │
│  ┌─────────────┬─────────────┬─────────────┐    │
│  │ Downloader  │ Transcriber │ Analyzer    │    │
│  │ (yt-dlp)    │ (Whisper)   │ (Ollama)    │    │
│  └─────────────┴─────────────┴─────────────┘    │
└─────────────────┬───────────────────────────────┘
                  │ Async/Await
┌─────────────────┴───────────────────────────────┐
│              External Services                  │
│  ┌─────────────┬─────────────┬─────────────┐    │
│  │ Video Sites │ CUDA/GPU    │ Local LLM   │    │
│  │ (1000+)     │ Hardware    │ Models      │    │
│  └─────────────┴─────────────┴─────────────┘    │
└─────────────────────────────────────────────────┘
```

### Design Principles
1. **Separation of Concerns**: UI, Core Logic, and External Services are distinct
2. **Async-First**: Non-blocking operations for responsive UI
3. **Thread Safety**: Worker threads for heavy operations
4. **Event-Driven**: Qt signals/slots for loose coupling
5. **User-Centric**: UX-driven design decisions

---

## 🔧 Core Components

### 1. UniversalDownloader (`src/core/downloader.py`)

**Purpose**: Download videos from any supported website using yt-dlp

**Key Features**:
- Organized folder structure (`downloads/videos/`, `downloads/transcripts/`)
- Real-time progress tracking via callbacks
- ANSI color code sanitization for Windows compatibility
- Robust error handling

**Usage**:
```python
downloader = UniversalDownloader()
video_path = await downloader.download(url, progress_callback)
```

**Key Methods**:
- `download()`: Main download method with progress tracking
- `_progress_hook()`: Parses yt-dlp progress and sanitizes data

### 2. WhisperTranscriber (`src/core/transcriber.py`)

**Purpose**: GPU-accelerated audio transcription using OpenAI Whisper

**Key Features**:
- CUDA acceleration for RTX GPUs
- Multiple model sizes (tiny.en to large-v3)
- Organized transcript storage
- Progress tracking for loading and transcription phases

**Usage**:
```python
transcriber = WhisperTranscriber(model="medium.en", device="cuda")
transcript, path = await transcriber.transcribe_and_save(video_path, transcripts_dir=transcripts_dir)
```

**Key Methods**:
- `load_model()`: Async model loading with progress
- `transcribe()`: Core transcription method
- `transcribe_and_save()`: Full workflow with file management

### 3. OllamaAnalyzer (`src/core/analyzer.py`)

**Purpose**: AI-powered content analysis using local LLMs

**Key Features**:
- Privacy-first local processing
- Multiple analysis types (summary, quotes, topics, sentiment)
- Streaming responses for real-time updates
- Custom analysis prompts

**Usage**:
```python
analyzer = OllamaAnalyzer(model="llama3.2")
result = await analyzer.full_analysis(transcript)
```

**Key Methods**:
- `ensure_model()`: Check and download models if needed
- `full_analysis()`: Complete analysis suite
- `custom_analysis()`: User-defined analysis prompts

---

## 🎨 UI Components

### 1. MainWindow (`src/ui/main_window.py`)

**Purpose**: Application shell with tabbed interface

**Key Features**:
- Modern dark theme styling
- Tab navigation between major workflows
- Signal coordination between tabs
- Responsive layout management

### 2. DownloadTab (`src/ui/download_tab.py`)

**Purpose**: Video download and transcription interface

**Key Features**:
- URL input with universal support indication
- Model selection (Whisper model sizes)
- Download-only vs. full transcription modes
- Smart checkbox logic (keep video becomes disabled in download-only)
- Real-time progress bars for download and transcription
- Process logging with timestamps

**Key Components**:
- `DownloadWorker`: Background thread for heavy operations
- Progress tracking via Qt signals
- Folder path display for user awareness

### 3. AnalysisTab (`src/ui/analysis_tab.py`)

**Purpose**: AI analysis interface and controls

**Key Features**:
- Transcript display and editing
- AI model selection (Ollama models)
- Tabbed results (Summary, Quotes, Topics, Sentiment, Custom)
- Custom analysis prompt input
- Real-time analysis progress

### 4. ResultsTab (`src/ui/results_tab.py`)

**Purpose**: Results visualization and export

**Key Features**:
- Overview dashboard with statistics cards
- Multiple export formats (JSON, Markdown, HTML, PDF, TXT)
- Copy to clipboard functionality
- Tabbed detailed results view
- Raw data inspection

---

## 🔄 Data Flow

### Complete Workflow
```
1. User Input (URL) 
   ↓
2. DownloadWorker Thread
   ↓
3. UniversalDownloader.download()
   ↓
4. Video File (downloads/videos/)
   ↓
5. WhisperTranscriber.transcribe_and_save() [if not download-only]
   ↓
6. Transcript File (downloads/transcripts/)
   ↓
7. Auto-navigation to Analysis Tab [if transcribed]
   ↓
8. OllamaAnalyzer.full_analysis()
   ↓
9. AnalysisResult Object
   ↓
10. Auto-navigation to Results Tab
    ↓
11. Results Display + Export Options
```

### Signal Flow
```
DownloadTab.transcription_completed 
   → MainWindow.on_transcription_completed()
   → AnalysisTab.load_transcript()
   → Switch to Analysis Tab

AnalysisTab.analysis_completed
   → MainWindow.on_analysis_completed() 
   → ResultsTab.load_results()
   → Switch to Results Tab
```

---

## 📁 File Organization

```
TranscriptAI/
├── src/                          # Source code
│   ├── core/                     # Business logic
│   │   ├── __init__.py
│   │   ├── downloader.py         # Video download (yt-dlp wrapper)
│   │   ├── transcriber.py        # Audio transcription (Whisper)
│   │   └── analyzer.py           # AI analysis (Ollama)
│   ├── ui/                       # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py        # Application shell
│   │   ├── download_tab.py       # Download/transcription UI
│   │   ├── analysis_tab.py       # AI analysis UI
│   │   ├── results_tab.py        # Results display UI
│   │   └── styles.py             # Dark theme CSS
│   └── main.py                   # Application entry point
├── downloads/                    # Generated content (gitignored)
│   ├── videos/                   # Downloaded video files
│   └── transcripts/              # Generated transcript files
├── .venv/                        # Virtual environment (gitignored)
├── requirements.txt              # Python dependencies
├── run.py                        # Quick launcher script
├── TranscriptAI.bat              # Windows launcher
├── build_exe.py                  # PyInstaller build script
├── install_cuda.bat              # CUDA setup helper
├── README.md                     # User documentation
├── SPEC.md                       # Feature specification
├── ARCHITECTURE.md               # This document
└── .gitignore                    # Git ignore rules
```

---

## 🎯 Key Design Patterns

### 1. Worker Thread Pattern
Heavy operations (download, transcription, analysis) run in separate QThread instances to keep the UI responsive.

```python
class DownloadWorker(QThread):
    progress_updated = Signal(str)
    completed = Signal(Path, str)
    
    def run(self):
        # Heavy work in background thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_work())
```

### 2. Signal/Slot Communication
Qt signals provide loose coupling between UI components and background operations.

```python
# Tab coordination
self.download_tab.transcription_completed.connect(self.on_transcription_completed)
self.analysis_tab.analysis_completed.connect(self.on_analysis_completed)
```

### 3. Async/Await for I/O
Core operations use async/await for non-blocking I/O operations.

```python
async def download_and_transcribe(self):
    video_path = await self.downloader.download(url)
    transcript = await self.transcriber.transcribe(video_path)
```

### 4. Progress Callback Pattern
Real-time progress updates via callback functions.

```python
def progress_callback(progress: DownloadProgress):
    self.progress_signal.emit(progress.percent)
```

### 5. Factory Methods for UI
UI components built through factory methods for consistency.

```python
def create_input_section(self) -> QGroupBox:
    group = QGroupBox("Video Input")
    # Build and return configured group
    return group
```

---

## ➕ Adding Features

### Adding a New Analysis Type

1. **Extend AnalysisResult dataclass** (`src/core/analyzer.py`):
```python
@dataclass
class AnalysisResult:
    # ... existing fields
    new_analysis: str
```

2. **Add analysis method**:
```python
async def extract_new_analysis(self, transcript: str) -> str:
    prompt = "Your analysis prompt here..."
    return await self._generate_response(prompt, system_prompt)
```

3. **Update full_analysis method**:
```python
async def full_analysis(self, transcript: str) -> AnalysisResult:
    # ... existing analyses
    new_analysis = await self.extract_new_analysis(transcript)
    
    return AnalysisResult(
        # ... existing fields
        new_analysis=new_analysis
    )
```

4. **Add UI tab** (`src/ui/analysis_tab.py`):
```python
self.new_analysis_text = QTextEdit()
self.results_tabs.addTab(self.new_analysis_text, "🆕 New Analysis")
```

5. **Update results display** (`src/ui/results_tab.py`):
```python
def load_results(self, result: AnalysisResult):
    # ... existing updates
    self.new_analysis_display.setPlainText(result.new_analysis)
```

### Adding a New Export Format

1. **Update format combo** (`src/ui/results_tab.py`):
```python
self.format_combo.addItems([
    # ... existing formats
    "New Format (description)"
])
```

2. **Extend format_export_content method**:
```python
def format_export_content(self, format_type: str) -> str:
    # ... existing formats
    elif format_type == "New Format (description)":
        return self.format_new_format()
        
def format_new_format(self) -> str:
    # Implementation here
    return formatted_content
```

### Adding New Download Sources

yt-dlp handles this automatically! If yt-dlp supports a site, TranscriptAI will too. No code changes needed.

---

## 🔧 Common Modifications

### Changing Default Whisper Model
`src/ui/download_tab.py`, line ~158:
```python
self.model_combo.setCurrentText("large-v3")  # Change from "medium.en"
```

### Changing Default AI Model
`src/ui/analysis_tab.py`, line ~134:
```python
self.model_combo.addItems([
    "llama3.2", "mistral", "your-model-here"  # Add your preferred model first
])
```

### Customizing Download Directory
`src/core/downloader.py`, line ~26:
```python
def __init__(self, output_dir: Optional[Path] = None):
    if output_dir is None:
        base_dir = Path("C:/YourCustomPath")  # Change default location
```

### Adding Custom Themes
`src/ui/styles.py` - duplicate DARK_THEME and modify colors:
```python
YOUR_THEME = """
QMainWindow {
    background-color: #your-bg-color;
    color: #your-text-color;
}
# ... more styles
"""
```

### Changing Window Size/Behavior
`src/ui/main_window.py`, line ~27:
```python
def setup_ui(self):
    self.setWindowTitle("Your App Name")
    self.setMinimumSize(1400, 900)  # Change default size
    self.resize(1600, 1000)
```

---

## 🐛 Troubleshooting

### CUDA Issues
**Problem**: "torch.cuda.is_available() is False"
**Solution**: 
1. Install CUDA-enabled PyTorch: `uv pip install torch==2.4.1+cu121 --index-url https://download.pytorch.org/whl/cu121`
2. Ensure Python version <= 3.12 (CUDA wheels not available for 3.13+)
3. Verify NVIDIA drivers are up to date

### Import Errors
**Problem**: ModuleNotFoundError when running the app
**Solution**:
1. Ensure virtual environment is activated: `.venv\Scripts\activate.bat`
2. Install all dependencies: `uv pip install -r requirements.txt`
3. Check Python path in run.py matches your setup

### Download Failures
**Problem**: yt-dlp download errors
**Solution**:
1. Update yt-dlp: `uv pip install --upgrade yt-dlp`
2. Check URL validity in a browser first
3. Some sites require authentication - check yt-dlp docs

### UI Crashes
**Problem**: Worker thread AttributeError crashes
**Solution**:
1. Check variable ordering in start_process method
2. Ensure worker cleanup in stop_process method
3. Add null checks before calling worker methods

### Ollama Connection Issues
**Problem**: "Model not available" or connection errors
**Solution**:
1. Ensure Ollama is installed and running: `ollama serve`
2. Pull required models: `ollama pull llama3.2`
3. Check firewall isn't blocking localhost connections

---

## 🚀 Performance Tips

### GPU Optimization
- Use `large-v3` Whisper model for best accuracy (if you have VRAM)
- Use `tiny.en` for fastest transcription
- Enable CUDA with proper PyTorch installation

### Download Optimization
- Use download-only mode for batch operations
- Higher quality formats take longer but give better transcription results
- Consider network bandwidth when downloading large videos

### UI Responsiveness
- Heavy operations always run in worker threads
- Use signals for progress updates, not direct UI manipulation from threads
- Avoid blocking the main thread with synchronous operations

---

## 📚 Resources

### Documentation
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Ollama Documentation](https://ollama.ai/docs)

### Development Tools
- [Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html) for UI design
- [PyInstaller](https://pyinstaller.org/) for executable creation
- [uv](https://github.com/astral-sh/uv) for package management

---

**Built with ❤️ using Claude Code**
*Architecture designed for extensibility, performance, and developer happiness* 🚀