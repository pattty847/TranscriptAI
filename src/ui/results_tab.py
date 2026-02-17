"""
Results and export tab with complete export support.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from PySide6.QtGui import QFont, QTextDocument
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QGroupBox, QComboBox, QFileDialog, QFrame,
    QMessageBox, QTabWidget, QApplication
)

from src.core.analyzer import AnalysisResult


class ResultsTab(QWidget):
    """Results display and export tab."""

    def __init__(self):
        super().__init__()
        self.current_result: Optional[AnalysisResult] = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the results tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        export_group = self.create_export_section()
        layout.addWidget(export_group)

        results_group = self.create_results_display()
        layout.addWidget(results_group)

    def create_export_section(self) -> QGroupBox:
        """Create export controls section."""
        group = QGroupBox("Export")
        layout = QHBoxLayout(group)
        layout.setSpacing(8)

        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "JSON (Data)", "Markdown (Blog)", "HTML (Web)", "PDF (Report)", "TXT (Simple)"
        ])

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setEnabled(False)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setProperty("class", "secondary")
        self.clear_button.clicked.connect(self.clear_results)
        self.clear_button.setEnabled(False)

        self.status_label = QLabel("Waiting for analysis results...")
        self.status_label.setProperty("class", "status")

        layout.addWidget(format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.export_button)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.clear_button)
        layout.addStretch()
        layout.addWidget(self.status_label)

        return group

    def create_results_display(self) -> QGroupBox:
        """Create the main results display."""
        group = QGroupBox("Analysis Results")
        layout = QVBoxLayout(group)

        self.results_tabs = QTabWidget()

        overview_widget = self.create_overview_tab()
        self.results_tabs.addTab(overview_widget, "Overview")

        self.summary_display = QTextEdit()
        self.summary_display.setReadOnly(True)
        self.results_tabs.addTab(self.summary_display, "Summary")

        self.quotes_display = QTextEdit()
        self.quotes_display.setReadOnly(True)
        self.results_tabs.addTab(self.quotes_display, "Quotes")

        self.topics_display = QTextEdit()
        self.topics_display.setReadOnly(True)
        self.results_tabs.addTab(self.topics_display, "Topics")

        self.sentiment_display = QTextEdit()
        self.sentiment_display.setReadOnly(True)
        self.results_tabs.addTab(self.sentiment_display, "Sentiment")

        self.raw_data_display = QTextEdit()
        self.raw_data_display.setReadOnly(True)
        self.raw_data_display.setFont(QFont("Consolas", 10))
        self.results_tabs.addTab(self.raw_data_display, "Raw Data")

        layout.addWidget(self.results_tabs)
        return group

    def create_overview_tab(self) -> QWidget:
        """Create overview tab with summary statistics."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)

        stats_layout = QHBoxLayout()
        summary_card = self.create_stat_card("Summary", "Waiting for analysis...")
        quotes_card = self.create_stat_card("Quotes", "0 extracted")
        topics_card = self.create_stat_card("Topics", "0 identified")
        stats_layout.addWidget(summary_card)
        stats_layout.addWidget(quotes_card)
        stats_layout.addWidget(topics_card)
        layout.addLayout(stats_layout)

        insights_frame = QFrame()
        insights_frame.setObjectName("card")
        insights_layout = QVBoxLayout(insights_frame)
        insights_title = QLabel("Key Insights")
        insights_title.setProperty("class", "card-title-large")
        self.insights_text = QLabel("Analysis results will appear here.")
        self.insights_text.setWordWrap(True)
        self.insights_text.setProperty("class", "insights-text")
        insights_layout.addWidget(insights_title)
        insights_layout.addWidget(self.insights_text)
        layout.addWidget(insights_frame)
        layout.addStretch()

        self.summary_card = summary_card
        self.quotes_card = quotes_card
        self.topics_card = topics_card
        return widget

    def create_stat_card(self, title: str, value: str) -> QFrame:
        """Create a statistics card."""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        title_label = QLabel(title)
        title_label.setProperty("class", "card-title")
        value_label = QLabel(value)
        value_label.setWordWrap(True)
        value_label.setProperty("class", "card-value")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.value_label = value_label
        return card

    def load_results(self, result: AnalysisResult):
        """Load and display analysis results."""
        self.current_result = result
        self.export_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.clear_button.setEnabled(True)

        self.summary_display.setPlainText(result.summary or "")
        self.quotes_display.setPlainText(
            "\n\n".join([f'- "{quote}"' for quote in result.quotes]) if result.quotes else "No quotes extracted."
        )
        self.topics_display.setPlainText(
            "\n".join([f"- {topic}" for topic in result.topics]) if result.topics else "No topics identified."
        )
        self.sentiment_display.setPlainText(result.sentiment or "No sentiment output.")

        raw_data = {
            "summary": result.summary,
            "quotes": result.quotes,
            "topics": result.topics,
            "sentiment": result.sentiment,
            "custom_analysis": result.custom_analysis,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.raw_data_display.setPlainText(json.dumps(raw_data, indent=2, ensure_ascii=False))
        self.update_overview(result)
        self.status_label.setText("Results loaded. Ready to export or copy.")

    def update_overview(self, result: AnalysisResult):
        """Update overview tab with statistics."""
        summary = result.summary.strip() if result.summary else "No summary generated."
        self.summary_card.value_label.setText(summary[:120] + "..." if len(summary) > 120 else summary)
        self.quotes_card.value_label.setText(f"{len(result.quotes)} extracted")
        self.topics_card.value_label.setText(f"{len(result.topics)} identified")

        insights = []
        if result.quotes:
            insights.append(f"Found {len(result.quotes)} notable quote(s).")
        if result.topics:
            insights.append(f"Identified {len(result.topics)} topic(s).")
        if result.sentiment:
            insights.append(f"Sentiment: {result.sentiment}")
        self.insights_text.setText("\n".join(insights) if insights else "No insights returned.")

    def clear_results(self):
        """Clear loaded analysis results."""
        self.current_result = None
        self.summary_display.clear()
        self.quotes_display.clear()
        self.topics_display.clear()
        self.sentiment_display.clear()
        self.raw_data_display.clear()
        self.summary_card.value_label.setText("Waiting for analysis...")
        self.quotes_card.value_label.setText("0 extracted")
        self.topics_card.value_label.setText("0 identified")
        self.insights_text.setText("Analysis results will appear here.")
        self.export_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.status_label.setText("Results cleared.")

    def export_results(self):
        """Export results in selected format."""
        if not self.current_result:
            return

        format_text = self.format_combo.currentText()
        filter_map = {
            "JSON (Data)": "JSON files (*.json)",
            "Markdown (Blog)": "Markdown files (*.md)",
            "HTML (Web)": "HTML files (*.html)",
            "PDF (Report)": "PDF files (*.pdf)",
            "TXT (Simple)": "Text files (*.txt)",
        }
        file_filter = filter_map.get(format_text, "All files (*.*)")
        default_name = f"transcript_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Results", default_name, file_filter)
        if not file_path:
            return

        try:
            if format_text == "PDF (Report)":
                self._export_pdf(Path(file_path))
            else:
                content = self.format_export_content(format_text)
                Path(file_path).write_text(content, encoding="utf-8")

            self.status_label.setText(f"Exported to {file_path}")
            QMessageBox.information(self, "Export Successful", f"Results exported to:\n{file_path}")
        except Exception as e:
            self.status_label.setText(f"Export failed: {e}")
            QMessageBox.critical(self, "Export Failed", f"Failed to export results:\n{str(e)}")

    def _export_pdf(self, file_path: Path):
        """Export report as PDF through Qt printing."""
        result = self.current_result
        html = self._format_html_report(result)
        doc = QTextDocument()
        doc.setHtml(html)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(str(file_path))
        doc.print(printer)

    def _format_html_report(self, result: AnalysisResult) -> str:
        quotes_html = "".join([f"<li>{self._escape_html(q)}</li>" for q in result.quotes]) or "<li>None</li>"
        topics_html = "".join([f"<li>{self._escape_html(t)}</li>" for t in result.topics]) or "<li>None</li>"
        return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Transcript Analysis Report</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 36px; color: #1f2933; }}
    h1 {{ color: #0a6772; margin-bottom: 4px; }}
    .meta {{ color: #52606d; font-size: 12px; margin-bottom: 20px; }}
    h2 {{ border-bottom: 1px solid #d9e2ec; padding-bottom: 6px; margin-top: 22px; }}
    li {{ margin-bottom: 8px; }}
    .panel {{ background: #f8fafc; border: 1px solid #d9e2ec; border-radius: 8px; padding: 12px; }}
  </style>
</head>
<body>
  <h1>Transcript Analysis Report</h1>
  <div class="meta">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
  <h2>Summary</h2>
  <div class="panel">{self._escape_html(result.summary or "No summary generated.")}</div>
  <h2>Best Quotes</h2>
  <ul>{quotes_html}</ul>
  <h2>Topics</h2>
  <ul>{topics_html}</ul>
  <h2>Sentiment</h2>
  <div class="panel">{self._escape_html(result.sentiment or "No sentiment output.")}</div>
</body>
</html>
"""

    def _escape_html(self, text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def format_export_content(self, format_type: str) -> str:
        """Format results for non-PDF export."""
        result = self.current_result
        if format_type == "JSON (Data)":
            data = {
                "summary": result.summary,
                "quotes": result.quotes,
                "topics": result.topics,
                "sentiment": result.sentiment,
                "custom_analysis": result.custom_analysis,
                "generated_at": datetime.now().isoformat(timespec="seconds"),
            }
            return json.dumps(data, indent=2, ensure_ascii=False)

        if format_type == "Markdown (Blog)":
            quote_lines = "\n".join([f'- "{quote}"' for quote in result.quotes]) or "- None"
            topic_lines = "\n".join([f"- {topic}" for topic in result.topics]) or "- None"
            return f"""# Transcript Analysis Results

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
{result.summary or "No summary generated."}

## Best Quotes
{quote_lines}

## Key Topics
{topic_lines}

## Sentiment Analysis
{result.sentiment or "No sentiment output."}
"""

        if format_type == "HTML (Web)":
            return self._format_html_report(result)

        if format_type == "TXT (Simple)":
            quotes = "\n".join([f"{idx}. \"{quote}\"" for idx, quote in enumerate(result.quotes, 1)]) or "1. None"
            topics = "\n".join([f"{idx}. {topic}" for idx, topic in enumerate(result.topics, 1)]) or "1. None"
            return f"""TRANSCRIPT ANALYSIS RESULTS
==========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
{result.summary or "No summary generated."}

BEST QUOTES:
{quotes}

KEY TOPICS:
{topics}

SENTIMENT:
{result.sentiment or "No sentiment output."}
"""

        return "Unsupported export format."

    def copy_to_clipboard(self):
        """Copy textual report to clipboard."""
        if not self.current_result:
            return
        content = self.format_export_content("TXT (Simple)")
        QApplication.clipboard().setText(content)
        self.status_label.setText("Copied results to clipboard.")
        QMessageBox.information(self, "Copied", "Results copied to clipboard successfully.")
