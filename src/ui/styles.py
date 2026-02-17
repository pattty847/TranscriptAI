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
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 500;
    font-size: 12px;
}

QTabBar::tab:selected {
    background-color: #0d7377;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #4c4c4c;
}

QLineEdit {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 13px;
    color: #ffffff;
    selection-background-color: #0d7377;
}

QLineEdit:focus {
    border: 2px solid #0d7377;
    background-color: #2d2d2d;
    outline: none;
}

QLineEdit:hover {
    border-color: #5c5c5c;
}

QPushButton {
    background-color: #0d7377;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 13px;
    min-height: 18px;
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
    opacity: 0.6;
}

QPushButton.secondary {
    background-color: #3c3c3c;
    border: 1px solid #5c5c5c;
}

QPushButton.secondary:hover {
    background-color: #4c4c4c;
    border-color: #6c6c6c;
}

QPushButton.secondary:pressed {
    background-color: #2c2c2c;
}

QPushButton.danger {
    background-color: #c92a2a;
}

QPushButton.danger:hover {
    background-color: #e03131;
}

QPushButton.danger:pressed {
    background-color: #a61e1e;
}

QPushButton.multi-select {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    text-align: left;
    padding: 10px 12px;
}

QPushButton.multi-select:hover {
    border-color: #5c5c5c;
}

QMenu#multi-select-menu {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 4px;
}

QMenu#multi-select-menu QPushButton {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px 12px;
    text-align: left;
    min-width: 180px;
    font-size: 10pt;
}

QMenu#multi-select-menu QPushButton:hover {
    background-color: #3c3c3c;
    border-color: #5c5c5c;
}

QMenu#multi-select-menu QPushButton:checked {
    background-color: #0d7377;
    border-color: #0d7377;
    color: #ffffff;
}

QMenu#multi-select-menu QPushButton:checked:hover {
    background-color: #14a085;
}

QProgressBar {
    border: 1px solid #404040;
    border-radius: 6px;
    text-align: center;
    background-color: #1e1e1e;
    color: #ffffff;
    font-weight: 500;
    height: 20px;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #0d7377;
    border-radius: 0px;
}

QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    color: #e0e0e0;
    line-height: 1.5;
    selection-background-color: #0d7377;
}

QTextEdit:focus {
    border-color: #5c5c5c;
    outline: none;
}

QTextEdit#queue {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    border-radius: 6px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    padding: 10px;
    color: #e0e0e0;
}

QTextEdit#log {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    color: #e0e0e0;
    line-height: 1.5;
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
    color: #e0e0e0;
    font-size: 14px;
}

QLabel.section-title {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

QLabel.status {
    color: #9c9c9c;
    font-size: 13px;
}

QLabel#title {
    font-size: 24px;
    font-weight: 700;
    color: #0d7377;
    margin: 0px;
}

QLabel#subtitle {
    font-size: 12px;
    color: #9c9c9c;
    margin: 0px;
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

QLabel#validation {
    color: #9c9c9c;
    font-size: 11px;
    padding-left: 4px;
    margin-top: -8px;
}

QLabel#validation.validation-error {
    color: #ff6b6b;
    font-size: 11px;
    padding-left: 4px;
    margin-top: -8px;
}

QLabel#validation.validation-success {
    color: #51cf66;
    font-size: 11px;
    padding-left: 4px;
    margin-top: -8px;
}

QLabel.status-error {
    color: #ff6b6b;
    font-size: 13px;
}

QLabel.status-success {
    color: #51cf66;
    font-size: 13px;
    font-weight: bold;
}

QLabel.status-info {
    color: #0d7377;
    font-size: 13px;
}

QLabel#version {
    font-size: 12px;
    color: #6c6c6c;
    padding: 4px 8px;
    background-color: #3c3c3c;
    border-radius: 4px;
}

QLabel#llmHealthBadge {
    border: 1px solid #404040;
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}

QFrame.card {
    background-color: #2d2d2d;
    border: 1px solid #3c3c3c;
    border-radius: 12px;
    padding: 16px;
}

QFrame#card {
    background-color: #2d2d2d;
    border: 1px solid #3c3c3c;
    border-radius: 12px;
    padding: 16px;
    min-width: 200px;
}

QLabel.card-title {
    font-size: 14px;
    font-weight: 600;
    color: #0d7377;
    margin-bottom: 4px;
}

QLabel.card-title-large {
    font-size: 16px;
    font-weight: 600;
    color: #0d7377;
    margin-bottom: 8px;
}

QLabel#value {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
}

QLabel.insights-text {
    color: #ffffff;
    font-size: 14px;
    line-height: 1.4;
}

QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 7px 10px;
    color: #ffffff;
    font-size: 13px;
    min-height: 18px;
}

QComboBox:hover {
    border-color: #5c5c5c;
}

QComboBox:focus {
    border: 2px solid #0d7377;
    outline: none;
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
    margin-top: 8px;
    padding-top: 8px;
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

QFrame.divider {
    background-color: #404040;
    max-height: 1px;
    min-height: 1px;
    border: none;
    margin: 8px 0px;
}

QToolBar#mainToolbar {
    background: #232323;
    border: 1px solid #353535;
    border-radius: 6px;
    spacing: 6px;
    padding: 4px;
}

QToolBar#mainToolbar QToolButton {
    background: #303030;
    color: #ededed;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}

QToolBar#mainToolbar QToolButton:hover {
    background: #3a3a3a;
    border-color: #555;
}

QLabel.card-value {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
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
    border-radius: 0px;
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
    border-radius: 0px;
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
    border-radius: 0px;
    padding: 12px 16px;
    font-size: 14px;
    color: #333333;
}

QLineEdit:focus {
    border-color: #0d7377;
}
"""
