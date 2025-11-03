"""
Modern dark theme styling for TranscriptAI
"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTabWidget::pane {
    border: 1px solid #3c3c3c;
    background-color: #2d2d2d;
    border-radius: 8px;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background-color: #3c3c3c;
    color: #ffffff;
    padding: 12px 24px;
    margin-right: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 500;
    font-size: 13px;
}

QTabBar::tab:selected {
    background-color: #0d7377;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #4c4c4c;
}

QLineEdit {
    background-color: #3c3c3c;
    border: 2px solid #5c5c5c;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: #ffffff;
}

QLineEdit:focus {
    border-color: #0d7377;
}

QPushButton {
    background-color: #0d7377;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #14a085;
}

QPushButton:pressed {
    background-color: #0a5d61;
}

QPushButton:disabled {
    background-color: #5c5c5c;
    color: #9c9c9c;
}

QProgressBar {
    border: 2px solid #3c3c3c;
    border-radius: 8px;
    text-align: center;
    background-color: #2d2d2d;
    color: #ffffff;
    font-weight: 500;
}

QProgressBar::chunk {
    background-color: #0d7377;
    border-radius: 6px;
}

QTextEdit {
    background-color: #2d2d2d;
    border: 2px solid #3c3c3c;
    border-radius: 8px;
    padding: 16px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
    color: #ffffff;
    line-height: 1.4;
}

QScrollBar:vertical {
    background-color: #3c3c3c;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #5c5c5c;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6c6c6c;
}

QLabel {
    color: #ffffff;
    font-size: 14px;
}

QLabel.title {
    font-size: 18px;
    font-weight: 600;
    color: #0d7377;
    margin-bottom: 8px;
}

QLabel.subtitle {
    font-size: 16px;
    font-weight: 500;
    color: #ffffff;
    margin-bottom: 4px;
}

QLabel.hint {
    color: #9c9c9c;
    font-size: 12px;
    font-style: italic;
}

QFrame.card {
    background-color: #2d2d2d;
    border: 1px solid #3c3c3c;
    border-radius: 12px;
    padding: 16px;
}

QComboBox {
    background-color: #3c3c3c;
    border: 2px solid #5c5c5c;
    border-radius: 8px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 14px;
}

QComboBox:focus {
    border-color: #0d7377;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #3c3c3c;
    border: 1px solid #5c5c5c;
    selection-background-color: #0d7377;
    color: #ffffff;
}

QGroupBox {
    font-weight: 600;
    border: 2px solid #3c3c3c;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #0d7377;
}

QCheckBox {
    color: #ffffff;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #5c5c5c;
    background-color: #3c3c3c;
}

QCheckBox::indicator:checked {
    background-color: #0d7377;
    border-color: #0d7377;
}

QCheckBox::indicator:checked::after {
    content: "✓";
    color: #ffffff;
    font-weight: bold;
}
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #ffffff;
    color: #333333;
}

QTabWidget::pane {
    border: 1px solid #e0e0e0;
    background-color: #fafafa;
    border-radius: 8px;
}

QTabBar::tab {
    background-color: #f5f5f5;
    color: #333333;
    padding: 12px 24px;
    margin-right: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 500;
    font-size: 13px;
}

QTabBar::tab:selected {
    background-color: #0d7377;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #e0e0e0;
}

QPushButton {
    background-color: #0d7377;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #14a085;
}

QLineEdit {
    background-color: #ffffff;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: #333333;
}

QLineEdit:focus {
    border-color: #0d7377;
}
"""