"""
=== File: theme_manager.py ===
Manages UI themes (light and dark mode).
Provides centralized theme configuration and application.
"""


class ThemeManager:
    """Manage application themes"""
    
    LIGHT_THEME = {
        'name': 'Light',
        'bg': '#f0f0f0',
        'fg': '#000000',
        'panel_bg': '#ffffff',
        'header_bg': '#2196F3',
        'header_fg': '#ffffff',
        'details_bg': '#4CAF50',
        'status_bg': '#333333',
        'status_fg': '#ffffff',
        'text_bg': '#fafafa',
        'text_fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'button_bg': '#2196F3',
        'button_fg': '#ffffff',
        'error_fg': '#ff6b6b',
        'success_fg': '#4CAF50',
        'tree_bg': '#ffffff',
        'tree_fg': '#000000',
        'tree_select_bg': '#2196F3',
        'tree_select_fg': '#ffffff',
    }
    
    DARK_THEME = {
        'name': 'Dark',
        'bg': '#1e1e1e',
        'fg': '#ffffff',
        'panel_bg': '#2d2d2d',
        'header_bg': '#0d47a1',
        'header_fg': '#ffffff',
        'details_bg': '#1b5e20',
        'status_bg': '#000000',
        'status_fg': '#ffffff',
        'text_bg': '#252525',
        'text_fg': '#ffffff',
        'entry_bg': '#3d3d3d',
        'entry_fg': '#ffffff',
        'button_bg': '#1565C0',
        'button_fg': '#ffffff',
        'error_fg': '#ff6b6b',
        'success_fg': '#4CAF50',
        'tree_bg': '#2d2d2d',
        'tree_fg': '#ffffff',
        'tree_select_bg': '#1565C0',
        'tree_select_fg': '#ffffff',
    }
    
    def __init__(self):
        self.current_theme = self.LIGHT_THEME
        self.dark_mode = False
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.dark_mode = not self.dark_mode
        self.current_theme = self.DARK_THEME if self.dark_mode else self.LIGHT_THEME
        return self.current_theme
    
    def set_theme(self, dark_mode):
        """Set theme explicitly"""
        self.dark_mode = dark_mode
        self.current_theme = self.DARK_THEME if dark_mode else self.LIGHT_THEME
        return self.current_theme
    
    def get_theme(self):
        """Get current theme"""
        return self.current_theme
    
    def is_dark(self):
        """Check if dark mode is enabled"""
        return self.dark_mode

