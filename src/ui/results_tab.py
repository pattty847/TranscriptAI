"""
Results and export tab with modern data visualization
"""
import json
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QGroupBox, QComboBox, QFileDialog,
    QSplitter, QFrame, QScrollArea, QMessageBox, QTabWidget
)
from PySide6.QtGui import QFont

from src.core.analyzer import AnalysisResult


class ResultsTab(QWidget):
    """Results display and export tab"""
    
    def __init__(self):
        super().__init__()
        self.current_result: Optional[AnalysisResult] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the results tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Export controls
        export_group = self.create_export_section()
        layout.addWidget(export_group)
        
        # Results display
        results_group = self.create_results_display()
        layout.addWidget(results_group)
        
    def create_export_section(self) -> QGroupBox:
        """Create export controls section"""
        group = QGroupBox("Export & Share")
        layout = QHBoxLayout(group)
        
        # Format selection
        format_label = QLabel("Export Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "JSON (Data)", "Markdown (Blog)", "HTML (Web)", "PDF (Report)", "TXT (Simple)"
        ])
        
        # Export buttons
        self.export_button = QPushButton("📁 Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        
        self.copy_button = QPushButton("📋 Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setEnabled(False)
        
        self.share_button = QPushButton("🔗 Generate Share Link")
        self.share_button.clicked.connect(self.generate_share_link)
        self.share_button.setEnabled(False)
        
        layout.addWidget(format_label)
        layout.addWidget(self.format_combo)
        layout.addStretch()
        layout.addWidget(self.export_button)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.share_button)
        
        return group
        
    def create_results_display(self) -> QGroupBox:
        """Create the main results display"""
        group = QGroupBox("Analysis Results")
        layout = QVBoxLayout(group)
        
        # Create tabbed display
        self.results_tabs = QTabWidget()
        
        # Overview tab
        overview_widget = self.create_overview_tab()
        self.results_tabs.addTab(overview_widget, "📊 Overview")
        
        # Detailed results tabs
        self.summary_display = QTextEdit()
        self.summary_display.setReadOnly(True)
        self.results_tabs.addTab(self.summary_display, "📝 Summary")
        
        self.quotes_display = QTextEdit()
        self.quotes_display.setReadOnly(True)
        self.results_tabs.addTab(self.quotes_display, "💬 Best Quotes")
        
        self.topics_display = QTextEdit()
        self.topics_display.setReadOnly(True)
        self.results_tabs.addTab(self.topics_display, "🏷️ Topics")
        
        self.sentiment_display = QTextEdit()
        self.sentiment_display.setReadOnly(True)
        self.results_tabs.addTab(self.sentiment_display, "😊 Sentiment")
        
        self.raw_data_display = QTextEdit()
        self.raw_data_display.setReadOnly(True)
        self.raw_data_display.setFont(QFont("Consolas", 10))
        self.results_tabs.addTab(self.raw_data_display, "🔧 Raw Data")
        
        layout.addWidget(self.results_tabs)
        
        return group
        
    def create_overview_tab(self) -> QWidget:
        """Create overview tab with key statistics"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Summary card
        summary_card = self.create_stat_card("Summary", "Waiting for analysis...")
        stats_layout.addWidget(summary_card)
        
        # Quotes card
        quotes_card = self.create_stat_card("Best Quotes", "0 quotes extracted")
        stats_layout.addWidget(quotes_card)
        
        # Topics card
        topics_card = self.create_stat_card("Topics", "0 topics identified")
        stats_layout.addWidget(topics_card)
        
        layout.addLayout(stats_layout)
        
        # Key insights
        insights_frame = QFrame()
        insights_frame.setObjectName("card")
        insights_frame.setStyleSheet("""
            QFrame#card {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        insights_layout = QVBoxLayout(insights_frame)
        
        insights_title = QLabel("🔍 Key Insights")
        insights_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #0d7377;
                margin-bottom: 8px;
            }
        """)
        
        self.insights_text = QLabel("Analysis results will appear here...")
        self.insights_text.setWordWrap(True)
        self.insights_text.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                line-height: 1.4;
            }
        """)
        
        insights_layout.addWidget(insights_title)
        insights_layout.addWidget(self.insights_text)
        
        layout.addWidget(insights_frame)
        layout.addStretch()
        
        # Store references to update later
        self.summary_card = summary_card
        self.quotes_card = quotes_card
        self.topics_card = topics_card
        
        return widget
        
    def create_stat_card(self, title: str, value: str) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 12px;
                padding: 16px;
                min-width: 200px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #0d7377;
                margin-bottom: 4px;
            }
        """)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet("""
            QLabel#value {
                font-size: 18px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        value_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        # Store reference for updates
        card.value_label = value_label
        
        return card
        
    def load_results(self, result: AnalysisResult):
        """Load and display analysis results"""
        self.current_result = result
        
        # Enable export buttons
        self.export_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.share_button.setEnabled(True)
        
        # Update individual displays
        self.summary_display.setPlainText(result.summary)
        
        # Format quotes nicely
        if result.quotes:
            quotes_text = "\n\n".join([f"• \"{quote}\"" for quote in result.quotes])
            self.quotes_display.setPlainText(quotes_text)
        else:
            self.quotes_display.setPlainText("No quotes extracted.")
            
        # Format topics
        if result.topics:
            topics_text = "\n".join([f"• {topic}" for topic in result.topics])
            self.topics_display.setPlainText(topics_text)
        else:
            self.topics_display.setPlainText("No topics identified.")
            
        self.sentiment_display.setPlainText(result.sentiment)
        
        # Raw data
        raw_data = {
            "summary": result.summary,
            "quotes": result.quotes,
            "topics": result.topics,
            "sentiment": result.sentiment,
            "custom_analysis": result.custom_analysis
        }
        self.raw_data_display.setPlainText(json.dumps(raw_data, indent=2))
        
        # Update overview cards
        self.update_overview(result)
        
    def update_overview(self, result: AnalysisResult):
        """Update overview tab with statistics"""
        # Update stat cards
        self.summary_card.value_label.setText(result.summary[:100] + "..." if len(result.summary) > 100 else result.summary)
        self.quotes_card.value_label.setText(f"{len(result.quotes)} quotes extracted")
        self.topics_card.value_label.setText(f"{len(result.topics)} topics identified")
        
        # Update key insights
        insights = []
        if result.quotes:
            insights.append(f"• Found {len(result.quotes)} memorable quotes")
        if result.topics:
            insights.append(f"• Identified {len(result.topics)} key topics")
        insights.append(f"• Overall sentiment: {result.sentiment}")
        
        self.insights_text.setText("\n".join(insights))
        
    def export_results(self):
        """Export results in selected format"""
        if not self.current_result:
            return
            
        format_text = self.format_combo.currentText()
        
        # Get save location
        filter_map = {
            "JSON (Data)": "JSON files (*.json)",
            "Markdown (Blog)": "Markdown files (*.md)",
            "HTML (Web)": "HTML files (*.html)",
            "PDF (Report)": "PDF files (*.pdf)",
            "TXT (Simple)": "Text files (*.txt)"
        }
        
        file_filter = filter_map.get(format_text, "All files (*.*)")
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", f"transcript_analysis", file_filter
        )
        
        if not file_path:
            return
            
        try:
            content = self.format_export_content(format_text)
            Path(file_path).write_text(content, encoding='utf-8')
            
            QMessageBox.information(
                self, "Export Successful", 
                f"Results exported to:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Export Failed", 
                f"Failed to export results:\n{str(e)}"
            )
            
    def format_export_content(self, format_type: str) -> str:
        """Format results for export"""
        result = self.current_result
        
        if format_type == "JSON (Data)":
            data = {
                "summary": result.summary,
                "quotes": result.quotes,
                "topics": result.topics,
                "sentiment": result.sentiment,
                "custom_analysis": result.custom_analysis
            }
            return json.dumps(data, indent=2)
            
        elif format_type == "Markdown (Blog)":
            content = f"""# Transcript Analysis Results

## Summary
{result.summary}

## Best Quotes
"""
            for quote in result.quotes:
                content += f"- \"{quote}\"\n"
                
            content += f"""
## Key Topics
"""
            for topic in result.topics:
                content += f"- {topic}\n"
                
            content += f"""
## Sentiment Analysis
{result.sentiment}
"""
            return content
            
        elif format_type == "TXT (Simple)":
            content = f"""TRANSCRIPT ANALYSIS RESULTS
==========================

SUMMARY:
{result.summary}

BEST QUOTES:
"""
            for i, quote in enumerate(result.quotes, 1):
                content += f"{i}. \"{quote}\"\n"
                
            content += f"""
KEY TOPICS:
"""
            for i, topic in enumerate(result.topics, 1):
                content += f"{i}. {topic}\n"
                
            content += f"""
SENTIMENT:
{result.sentiment}
"""
            return content
            
        # Add HTML and PDF formats as needed
        return "Export format not yet implemented"
        
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        if not self.current_result:
            return
            
        content = self.format_export_content("TXT (Simple)")
        
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(content)
        
        QMessageBox.information(
            self, "Copied to Clipboard", 
            "Results copied to clipboard successfully!"
        )
        
    def generate_share_link(self):
        """Generate shareable link (placeholder)"""
        QMessageBox.information(
            self, "Share Link", 
            "Share link generation coming soon!\n\nFor now, use the copy or export functions."
        )