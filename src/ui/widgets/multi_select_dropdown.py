"""
Multi-select dropdown widget with toggleable options
"""
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton, QMenu, QWidgetAction


class MultiSelectDropdown(QPushButton):
    """Custom multi-select dropdown widget with toggleable buttons"""
    
    option_changed = Signal(str, bool)  # Signal emitted when an option changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        base_font = QFont(self.font())
        base_font.setPointSize(10)
        self.setFont(base_font)
        self.options = {
            "Retain Video": False,
            "Download Only": False,
            "Copy to Assets": True,  # Default enabled
            "YouTube Captions First": True,
            "Use Browser Cookies": True,
        }
        self.update_display()
        self.setMenu(self.create_menu())
        # Style the dropdown button itself
        self.setProperty("class", "multi-select")
        
    def create_menu(self) -> QMenu:
        """Create the dropdown menu with toggleable buttons"""
        menu = QMenu(self)
        menu.setObjectName("multi-select-menu")
        
        for option_name in self.options.keys():
            btn = QPushButton(option_name)
            btn_font = QFont(btn.font())
            btn_font.setPointSize(10)
            btn.setFont(btn_font)
            btn.setCheckable(True)
            btn.setChecked(self.options[option_name])
            
            def make_handler(name, m):
                def handler():
                    self.toggle_option(name)
                    m.close()
                return handler
            
            btn.clicked.connect(make_handler(option_name, menu))
            
            action = QWidgetAction(menu)
            action.setDefaultWidget(btn)
            menu.addAction(action)
        
        return menu
    
    def toggle_option(self, option_name: str):
        """Toggle an option on/off"""
        self.options[option_name] = not self.options[option_name]
        self.update_display()
        # Update the button state in the menu
        menu = self.menu()
        if menu:
            for action in menu.actions():
                widget = action.defaultWidget()
                if isinstance(widget, QPushButton) and widget.text() == option_name:
                    widget.setChecked(self.options[option_name])
        # Emit signal for option change
        self.option_changed.emit(option_name, self.options[option_name])
    
    def update_display(self):
        """Update the button text to show selected options"""
        selected = [name for name, checked in self.options.items() if checked]
        if selected:
            self.setText(", ".join(selected))
        else:
            self.setText("Options")
    
    def get_retain_video(self) -> bool:
        """Get Retain Video option"""
        return self.options.get("Retain Video", False)
    
    def get_download_only(self) -> bool:
        """Get Download Only option"""
        return self.options.get("Download Only", False)
    
    def get_copy_to_assets(self) -> bool:
        """Get Copy to Assets option"""
        return self.options.get("Copy to Assets", True)

    def get_youtube_captions_first(self) -> bool:
        """Get YouTube captions first option."""
        return self.options.get("YouTube Captions First", True)

    def get_use_browser_cookies(self) -> bool:
        """Get browser-cookie option used for YouTube subtitle requests."""
        return self.options.get("Use Browser Cookies", True)

