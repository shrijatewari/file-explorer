#!/usr/bin/env python3
"""
=== File: main.py ===
Main entry point for the File Explorer application.
Initializes the GUI and starts the application.
"""

import tkinter as tk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.explorer_ui import FileExplorerUI


def show_splash_screen():
    """Display a minimal splash screen"""
    splash = tk.Tk()
    splash.title("File Explorer")
    splash.geometry("400x200")
    splash.configure(bg='#2196F3')
    
    # Center the window
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (200 // 2)
    splash.geometry(f"400x200+{x}+{y}")
    
    # Remove window decorations for splash effect
    splash.overrideredirect(True)
    
    # Splash content
    title_label = tk.Label(splash, text="File Explorer", 
                          font=('Arial', 24, 'bold'), 
                          bg='#2196F3', fg='white')
    title_label.pack(pady=30)
    
    subtitle_label = tk.Label(splash, text="OS Mini Project", 
                             font=('Arial', 12), 
                             bg='#2196F3', fg='white')
    subtitle_label.pack()
    
    loading_label = tk.Label(splash, text="Loading...", 
                            font=('Arial', 10), 
                            bg='#2196F3', fg='white')
    loading_label.pack(pady=20)
    
    splash.update()
    
    return splash


def main():
    """Main entry point"""
    # Show splash screen
    splash = show_splash_screen()
    splash.after(1000, splash.destroy)  # Show for 1 second
    splash.mainloop()
    
    # Create and run main application
    root = tk.Tk()
    app = FileExplorerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

