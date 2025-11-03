"""
AI Analysis tab with real-time processing
"""
import asyncio
from typing import Optional

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QGroupBox, QComboBox, QLineEdit, QSplitter,
    QProgressBar, QTabWidget, QScrollArea, QFrame
)

from src.core.analyzer import OllamaAnalyzer, AnalysisResult


class AnalysisWorker(QThread):
    """Worker thread for AI analysis"""
    progress_updated = Signal(str)  # Progress message
    analysis_completed = Signal(object)  # AnalysisResult
    error_occurred = Signal(str)  # Error message
    
    def __init__(self, transcript: str, model: str = "llama3.2"):
        super().__init__()
        self.transcript = transcript
        self.model = model
        self.analyzer = OllamaAnalyzer(model)
        
    def run(self):
        """Run the AI analysis"""
        try:
            # Create event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run analysis
            loop.run_until_complete(self.run_analysis())
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if 'loop' in locals():
                loop.close()
                
    async def run_analysis(self):
        """Run the full analysis"""
        try:
            self.progress_updated.emit("🤖 Checking model availability...")
            
            # Ensure model is available
            if not await self.analyzer.ensure_model():
                raise Exception(f"Could not load model: {self.model}")
                
            self.progress_updated.emit("🔍 Running AI analysis...")
            
            # Run full analysis
            result = await self.analyzer.full_analysis(self.transcript)
            
            self.progress_updated.emit("✅ Analysis completed!")
            self.analysis_completed.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(f"Analysis failed: {str(e)}")


class AnalysisTab(QWidget):
    """AI Analysis tab"""
    analysis_completed = Signal(object)  # AnalysisResult
    
    def __init__(self):
        super().__init__()
        self.current_transcript = ""
        self.worker: Optional[AnalysisWorker] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the analysis tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Create splitter for input and results
        splitter = QSplitter(Qt.Vertical)
        
        # Input section
        input_section = self.create_input_section()
        splitter.addWidget(input_section)
        
        # Results section
        results_section = self.create_results_section()
        splitter.addWidget(results_section)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
    def create_input_section(self) -> QGroupBox:
        """Create the transcript input section"""
        group = QGroupBox("Transcript & Settings")
        layout = QVBoxLayout(group)
        
        # Model selection and controls
        controls_layout = QHBoxLayout()
        
        model_label = QLabel("AI Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "llama3.2", "llama3.1", "mistral", "codellama", "phi3"
        ])
        
        self.analyze_button = QPushButton("🤖 Analyze with AI")
        self.analyze_button.clicked.connect(self.start_analysis)
        self.analyze_button.setEnabled(False)
        
        self.stop_button = QPushButton("⏹ Stop Analysis")
        self.stop_button.clicked.connect(self.stop_analysis)
        self.stop_button.setEnabled(False)
        
        controls_layout.addWidget(model_label)
        controls_layout.addWidget(self.model_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.analyze_button)
        controls_layout.addWidget(self.stop_button)
        
        layout.addLayout(controls_layout)
        
        # Transcript display
        self.transcript_display = QTextEdit()
        self.transcript_display.setPlaceholderText("Transcript will appear here after download and transcription...")
        self.transcript_display.setMaximumHeight(200)
        self.transcript_display.setReadOnly(True)
        layout.addWidget(self.transcript_display)
        
        # Status
        self.status_label = QLabel("Waiting for transcript...")
        layout.addWidget(self.status_label)
        
        return group
        
    def create_results_section(self) -> QGroupBox:
        """Create the analysis results section"""
        group = QGroupBox("AI Analysis Results")
        layout = QVBoxLayout(group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        layout.addWidget(self.progress_bar)
        
        # Results tabs
        self.results_tabs = QTabWidget()
        
        # Summary tab
        self.summary_text = QTextEdit()
        self.summary_text.setPlaceholderText("AI-generated summary will appear here...")
        self.summary_text.setReadOnly(True)
        self.results_tabs.addTab(self.summary_text, "📝 Summary")
        
        # Quotes tab
        self.quotes_text = QTextEdit()
        self.quotes_text.setPlaceholderText("Best quotes and memorable moments...")
        self.quotes_text.setReadOnly(True)
        self.results_tabs.addTab(self.quotes_text, "💬 Quotes")
        
        # Topics tab
        self.topics_text = QTextEdit()
        self.topics_text.setPlaceholderText("Key topics and themes...")
        self.topics_text.setReadOnly(True)
        self.results_tabs.addTab(self.topics_text, "🏷️ Topics")
        
        # Sentiment tab
        self.sentiment_text = QTextEdit()
        self.sentiment_text.setPlaceholderText("Emotional tone and sentiment analysis...")
        self.sentiment_text.setReadOnly(True)
        self.results_tabs.addTab(self.sentiment_text, "😊 Sentiment")
        
        # Custom analysis tab
        custom_widget = QWidget()
        custom_layout = QVBoxLayout(custom_widget)
        
        custom_input_layout = QHBoxLayout()
        self.custom_prompt = QLineEdit()
        self.custom_prompt.setPlaceholderText("Enter custom analysis prompt...")
        
        self.custom_analyze_button = QPushButton("Analyze")
        self.custom_analyze_button.clicked.connect(self.run_custom_analysis)
        self.custom_analyze_button.setEnabled(False)
        
        custom_input_layout.addWidget(self.custom_prompt)
        custom_input_layout.addWidget(self.custom_analyze_button)
        
        self.custom_results = QTextEdit()
        self.custom_results.setPlaceholderText("Custom analysis results...")
        self.custom_results.setReadOnly(True)
        
        custom_layout.addLayout(custom_input_layout)
        custom_layout.addWidget(self.custom_results)
        
        self.results_tabs.addTab(custom_widget, "🔧 Custom")
        
        layout.addWidget(self.results_tabs)
        
        return group
        
    def load_transcript(self, transcript: str):
        """Load transcript for analysis"""
        self.current_transcript = transcript
        self.transcript_display.setPlainText(transcript)
        self.analyze_button.setEnabled(True)
        self.custom_analyze_button.setEnabled(True)
        self.status_label.setText(f"Transcript loaded ({len(transcript)} characters). Ready for analysis.")
        
    def start_analysis(self):
        """Start AI analysis"""
        if not self.current_transcript:
            self.status_label.setText("❌ No transcript available")
            return
            
        if self.worker and self.worker.isRunning():
            self.status_label.setText("❌ Analysis already running")
            return
            
        # Reset UI
        self.clear_results()
        self.progress_bar.setVisible(True)
        self.analyze_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Start worker
        model = self.model_combo.currentText()
        self.worker = AnalysisWorker(self.current_transcript, model)
        
        # Connect signals
        self.worker.progress_updated.connect(self.update_status)
        self.worker.analysis_completed.connect(self.on_analysis_completed)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_worker_finished)
        
        self.worker.start()
        
    def stop_analysis(self):
        """Stop current analysis"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait(3000)
            
        self.on_worker_finished()
        self.status_label.setText("⏹ Analysis stopped by user")
        
    def run_custom_analysis(self):
        """Run custom analysis with user prompt"""
        prompt = self.custom_prompt.text().strip()
        if not prompt or not self.current_transcript:
            return
            
        # TODO: Implement custom analysis
        self.custom_results.setPlainText("Custom analysis not yet implemented...")
        
    def update_status(self, message: str):
        """Update status message"""
        self.status_label.setText(message)
        
    def clear_results(self):
        """Clear all result displays"""
        self.summary_text.clear()
        self.quotes_text.clear()
        self.topics_text.clear()
        self.sentiment_text.clear()
        self.custom_results.clear()
        
    def on_analysis_completed(self, result: AnalysisResult):
        """Handle analysis completion"""
        # Populate results
        self.summary_text.setPlainText(result.summary)
        
        # Format quotes nicely
        if result.quotes:
            quotes_formatted = "\n\n".join([f"• \"{quote}\"" for quote in result.quotes])
            self.quotes_text.setPlainText(quotes_formatted)
            
        # Format topics
        if result.topics:
            topics_formatted = "\n".join([f"• {topic}" for topic in result.topics])
            self.topics_text.setPlainText(topics_formatted)
            
        self.sentiment_text.setPlainText(result.sentiment)
        
        self.status_label.setText("✅ Analysis completed successfully!")
        
        # Emit signal for main window
        self.analysis_completed.emit(result)
        
    def on_error(self, error_message: str):
        """Handle analysis error"""
        self.status_label.setText(f"❌ Error: {error_message}")
        
    def on_worker_finished(self):
        """Handle worker completion"""
        self.progress_bar.setVisible(False)
        self.analyze_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if self.worker:
            self.worker.deleteLater()
            self.worker = None