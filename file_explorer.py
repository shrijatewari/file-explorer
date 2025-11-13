#!/usr/bin/env python3
"""
File Explorer Application
A comprehensive file explorer that demonstrates Operating Systems concepts
including file handling, directory navigation, and OS-level operations.
Operating Systems Mini Project
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from pathlib import Path
from datetime import datetime
import stat
import shutil
import subprocess
import platform


class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer - OS Mini Project")
        self.root.geometry("1200x750")
        
        # Theme management
        self.dark_mode = False
        self.setup_themes()
        
        # Current directory
        self.current_path = os.path.expanduser("~")
        
        # Selected item for context menu
        self.selected_item = None
        
        # Setup UI
        self.setup_ui()
        
        # Load initial directory
        self.navigate_to(self.current_path)
    
    def setup_themes(self):
        """Setup light and dark theme colors"""
        self.light_theme = {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'panel_bg': '#ffffff',
            'header_bg': '#2196F3',
            'header_fg': '#ffffff',
            'details_bg': '#4CAF50',
            'status_bg': '#333333',
            'status_fg': '#ffffff',
            'text_bg': '#fafafa',
            'entry_bg': '#ffffff',
            'button_bg': '#2196F3',
            'button_fg': '#ffffff'
        }
        
        self.dark_theme = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'panel_bg': '#2d2d2d',
            'header_bg': '#0d47a1',
            'header_fg': '#ffffff',
            'details_bg': '#1b5e20',
            'status_bg': '#000000',
            'status_fg': '#ffffff',
            'text_bg': '#252525',
            'entry_bg': '#3d3d3d',
            'button_bg': '#1565C0',
            'button_fg': '#ffffff'
        }
        
        self.current_theme = self.light_theme
    
    def apply_theme(self):
        """Apply current theme to all widgets"""
        theme = self.dark_theme if self.dark_mode else self.light_theme
        self.current_theme = theme
        
        # Update root window
        self.root.configure(bg=theme['bg'])
        
        # Update all frames and widgets (this is a simplified version)
        # In a full implementation, you'd recursively update all widgets
    
    def setup_ui(self):
        """Setup the user interface"""
        theme = self.current_theme
        
        # Main container
        main_frame = tk.Frame(self.root, bg=theme['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame - Navigation bar
        nav_frame = tk.Frame(main_frame, bg=theme['bg'])
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Navigation buttons
        button_frame = tk.Frame(nav_frame, bg=theme['bg'])
        button_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        back_btn = tk.Button(button_frame, text="← Back", command=self.go_back,
                            bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                            padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        back_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        home_btn = tk.Button(button_frame, text="🏠 Home", command=self.go_home,
                            bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
                            padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        home_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh", command=self.refresh,
                               bg='#FF9800', fg='white', font=('Arial', 10, 'bold'),
                               padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Action buttons
        action_frame = tk.Frame(nav_frame, bg=theme['bg'])
        action_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        new_folder_btn = tk.Button(action_frame, text="📁 New Folder", command=self.create_folder,
                                   bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'),
                                   padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        new_folder_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        rename_btn = tk.Button(action_frame, text="✏️ Rename", command=self.rename_item,
                               bg='#E91E63', fg='white', font=('Arial', 10, 'bold'),
                               padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        rename_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = tk.Button(action_frame, text="🗑️ Delete", command=self.delete_item,
                              bg='#F44336', fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        open_btn = tk.Button(action_frame, text="📂 Open", command=self.open_item,
                            bg='#00BCD4', fg='white', font=('Arial', 10, 'bold'),
                            padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        open_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Path entry
        path_label = tk.Label(nav_frame, text="Path:", bg=theme['bg'], fg=theme['fg'], font=('Arial', 10))
        path_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.path_var = tk.StringVar()
        path_entry = tk.Entry(nav_frame, textvariable=self.path_var, font=('Arial', 10),
                             width=40, relief=tk.SUNKEN, bd=2, bg=theme['entry_bg'], fg=theme['fg'])
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        path_entry.bind('<Return>', lambda e: self.navigate_from_entry())
        
        go_btn = tk.Button(nav_frame, text="Go", command=self.navigate_from_entry,
                          bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'),
                          padx=15, pady=5, cursor='hand2', relief=tk.RAISED)
        go_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Dark mode toggle
        self.dark_mode_btn = tk.Button(nav_frame, text="🌙 Dark", command=self.toggle_dark_mode,
                                      bg='#424242', fg='white', font=('Arial', 9),
                                      padx=10, pady=5, cursor='hand2', relief=tk.RAISED)
        self.dark_mode_btn.pack(side=tk.RIGHT)
        
        # Search bar
        search_frame = tk.Frame(main_frame, bg=theme['bg'])
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="🔍 Search:", bg=theme['bg'], fg=theme['fg'], font=('Arial', 10))
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10),
                               width=30, relief=tk.SUNKEN, bd=2, bg=theme['entry_bg'], fg=theme['fg'])
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_search_btn = tk.Button(search_frame, text="Clear", command=self.clear_search,
                                    bg='#757575', fg='white', font=('Arial', 9),
                                    padx=10, pady=5, cursor='hand2', relief=tk.RAISED)
        clear_search_btn.pack(side=tk.LEFT)
        
        # Middle frame - File list and details
        content_frame = tk.Frame(main_frame, bg=theme['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - File list
        left_panel = tk.Frame(content_frame, bg=theme['panel_bg'], relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # File list header
        list_header = tk.Label(left_panel, text="Files and Folders", bg=theme['header_bg'],
                              fg=theme['header_fg'], font=('Arial', 12, 'bold'), pady=10)
        list_header.pack(fill=tk.X)
        
        # Treeview for files
        tree_frame = tk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=('Size', 'Type', 'Modified'),
                                show='tree headings', yscrollcommand=v_scrollbar.set,
                                xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading('#0', text='Name', anchor=tk.W)
        self.tree.heading('Size', text='Size', anchor=tk.W)
        self.tree.heading('Type', text='Type', anchor=tk.W)
        self.tree.heading('Modified', text='Modified', anchor=tk.W)
        
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('Size', width=100, minwidth=80)
        self.tree.column('Type', width=100, minwidth=80)
        self.tree.column('Modified', width=150, minwidth=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<ButtonRelease-1>', self.on_item_select)
        self.tree.bind('<Button-3>', self.show_context_menu)  # Right-click
        
        # Right panel - File details
        right_panel = tk.Frame(content_frame, bg=theme['panel_bg'], relief=tk.RAISED, bd=2, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        right_panel.pack_propagate(False)
        
        # Details header
        details_header = tk.Label(right_panel, text="File Details", bg=theme['details_bg'],
                                 fg='white', font=('Arial', 12, 'bold'), pady=10)
        details_header.pack(fill=tk.X)
        
        # Details text area
        self.details_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD,
                                                      font=('Courier', 10),
                                                      bg=theme['text_bg'], fg=theme['fg'],
                                                      relief=tk.FLAT, padx=10, pady=10)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.details_text.config(state=tk.DISABLED)
        
        # Bottom frame - Status bar
        status_frame = tk.Frame(main_frame, bg=theme['status_bg'], height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", bg=theme['status_bg'],
                                    fg=theme['status_fg'], font=('Arial', 9), anchor=tk.W, padx=10)
        self.status_label.pack(fill=tk.BOTH, expand=True)
        
        # Store all widgets for theme updates
        self.theme_widgets = {
            'main_frame': main_frame,
            'nav_frame': nav_frame,
            'left_panel': left_panel,
            'right_panel': right_panel,
            'status_frame': status_frame
        }
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.dark_mode_btn.config(text="☀️ Light" if self.dark_mode else "🌙 Dark")
        self.update_status("Theme switched to " + ("Dark" if self.dark_mode else "Light") + " mode")
    
    def format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def get_file_type(self, path):
        """Get file type description"""
        if os.path.isdir(path):
            return "Directory"
        elif os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            type_map = {
                '.py': 'Python Script', '.txt': 'Text File', '.pdf': 'PDF Document',
                '.jpg': 'JPEG Image', '.jpeg': 'JPEG Image', '.png': 'PNG Image',
                '.gif': 'GIF Image', '.mp4': 'MP4 Video', '.mp3': 'MP3 Audio',
                '.zip': 'ZIP Archive', '.doc': 'Word Document', '.docx': 'Word Document',
                '.xls': 'Excel Spreadsheet', '.xlsx': 'Excel Spreadsheet',
                '.html': 'HTML File', '.css': 'CSS File', '.js': 'JavaScript File',
            }
            return type_map.get(ext, 'File')
        else:
            return "Unknown"
    
    def get_file_permissions(self, path):
        """Get file permissions in readable format"""
        try:
            st = os.stat(path)
            mode = st.st_mode
            perms = []
            
            # Owner permissions
            perms.append('r' if mode & stat.S_IRUSR else '-')
            perms.append('w' if mode & stat.S_IWUSR else '-')
            perms.append('x' if mode & stat.S_IXUSR else '-')
            
            # Group permissions
            perms.append('r' if mode & stat.S_IRGRP else '-')
            perms.append('w' if mode & stat.S_IWGRP else '-')
            perms.append('x' if mode & stat.S_IXGRP else '-')
            
            # Others permissions
            perms.append('r' if mode & stat.S_IROTH else '-')
            perms.append('w' if mode & stat.S_IWOTH else '-')
            perms.append('x' if mode & stat.S_IXOTH else '-')
            
            return ''.join(perms)
        except:
            return "Unknown"
    
    def get_item_path(self, item_text):
        """Get full path from item text"""
        # Remove emoji prefix if present
        if item_text.startswith('📁 ') or item_text.startswith('📄 '):
            name = item_text[2:]
        else:
            name = item_text
        
        if name == "..":
            return None
        
        return os.path.join(self.current_path, name)
    
    def load_directory(self, path, filter_text=""):
        """Load directory contents into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Add parent directory entry
            if path != os.path.dirname(path):
                parent_path = os.path.dirname(path)
                self.tree.insert('', 0, text="..", values=('', 'Parent Directory', ''),
                               tags=('directory',))
            
            # Get all items in directory
            items = []
            try:
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    items.append(item_path)
            except PermissionError:
                self.update_status(f"Permission denied: {path}", error=True)
                messagebox.showerror("Permission Denied",
                                   f"You don't have permission to access: {path}")
                return
            
            # Apply search filter
            if filter_text:
                filter_lower = filter_text.lower()
                items = [item for item in items 
                        if filter_lower in os.path.basename(item).lower()]
            
            # Sort: directories first, then files
            directories = [item for item in items if os.path.isdir(item)]
            files = [item for item in items if os.path.isfile(item)]
            
            directories.sort(key=lambda x: os.path.basename(x).lower())
            files.sort(key=lambda x: os.path.basename(x).lower())
            
            # Add directories
            for item_path in directories:
                name = os.path.basename(item_path)
                try:
                    stat_info = os.stat(item_path)
                    size = ""
                    modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    file_type = "Directory"
                    
                    self.tree.insert('', tk.END, text=f"📁 {name}", 
                                   values=(size, file_type, modified),
                                   tags=('directory',))
                except Exception as e:
                    self.tree.insert('', tk.END, text=f"📁 {name} (Error)",
                                   values=('', 'Error', ''),
                                   tags=('directory',))
            
            # Add files
            for item_path in files:
                name = os.path.basename(item_path)
                try:
                    stat_info = os.stat(item_path)
                    size = self.format_size(stat_info.st_size)
                    modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    file_type = self.get_file_type(item_path)
                    
                    self.tree.insert('', tk.END, text=f"📄 {name}",
                                   values=(size, file_type, modified),
                                   tags=('file',))
                except Exception as e:
                    self.tree.insert('', tk.END, text=f"📄 {name} (Error)",
                                   values=('', 'Error', ''),
                                   tags=('file',))
            
            # Configure tags
            self.tree.tag_configure('directory', foreground='#2196F3')
            self.tree.tag_configure('file', foreground='#333')
            
            # Update status
            item_count = len(directories) + len(files)
            if filter_text:
                self.update_status(f"Found {item_count} items matching '{filter_text}'")
            else:
                self.update_status(f"Loaded {item_count} items from {path}")
            
        except Exception as e:
            self.update_status(f"Error loading directory: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to load directory: {str(e)}")
    
    def navigate_to(self, path):
        """Navigate to a specific directory"""
        try:
            # Normalize path
            path = os.path.abspath(path)
            
            if not os.path.exists(path):
                self.update_status(f"Path does not exist: {path}", error=True)
                messagebox.showerror("Error", f"Path does not exist: {path}")
                return
            
            if not os.path.isdir(path):
                self.update_status(f"Not a directory: {path}", error=True)
                messagebox.showerror("Error", f"Not a directory: {path}")
                return
            
            self.current_path = path
            self.path_var.set(path)
            filter_text = self.search_var.get().strip()
            self.load_directory(path, filter_text)
            self.update_status(f"Navigated to: {path}")
            
        except Exception as e:
            self.update_status(f"Navigation failed: {str(e)}", error=True)
            messagebox.showerror("Error", f"Navigation failed: {str(e)}")
    
    def navigate_from_entry(self):
        """Navigate to path from entry field"""
        path = self.path_var.get().strip()
        if path:
            self.navigate_to(path)
    
    def go_back(self):
        """Go to parent directory"""
        parent = os.path.dirname(self.current_path)
        if parent != self.current_path:
            self.navigate_to(parent)
            self.update_status("Moved to parent directory")
    
    def go_home(self):
        """Go to home directory"""
        self.navigate_to(os.path.expanduser("~"))
        self.update_status("Navigated to home directory")
    
    def refresh(self):
        """Refresh current directory"""
        self.navigate_to(self.current_path)
        self.update_status("Directory refreshed")
    
    def on_search_change(self, *args):
        """Handle search text change"""
        filter_text = self.search_var.get().strip()
        self.load_directory(self.current_path, filter_text)
    
    def clear_search(self):
        """Clear search filter"""
        self.search_var.set("")
        self.load_directory(self.current_path)
        self.update_status("Search cleared")
    
    def on_item_double_click(self, event):
        """Handle double-click on tree item"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
        
        text = self.tree.item(item, 'text')
        
        # Handle parent directory
        if text == "..":
            self.go_back()
            return
        
        item_path = self.get_item_path(text)
        if not item_path:
            return
        
        if os.path.isdir(item_path):
            self.navigate_to(item_path)
            self.update_status(f"Opened directory: {os.path.basename(item_path)}")
        elif os.path.isfile(item_path):
            self.open_item()
    
    def on_item_select(self, event):
        """Handle single-click selection"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
        
        text = self.tree.item(item, 'text')
        self.selected_item = text
        
        # Handle parent directory
        if text == "..":
            self.show_directory_details(self.current_path)
            return
        
        item_path = self.get_item_path(text)
        if not item_path:
            return
        
        if os.path.isdir(item_path):
            self.show_directory_details(item_path)
        elif os.path.isfile(item_path):
            self.show_file_details(item_path)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.selected_item = self.tree.item(item, 'text')
            
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Open", command=self.open_item)
            context_menu.add_separator()
            context_menu.add_command(label="Rename", command=self.rename_item)
            context_menu.add_command(label="Delete", command=self.delete_item)
            context_menu.add_separator()
            context_menu.add_command(label="Properties", command=self.show_properties)
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def create_folder(self):
        """Create a new folder in the current directory"""
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        
        if not folder_name:
            return
        
        if not folder_name.strip():
            self.update_status("Folder name cannot be empty", error=True)
            messagebox.showerror("Error", "Folder name cannot be empty")
            return
        
        new_folder_path = os.path.join(self.current_path, folder_name.strip())
        
        try:
            if os.path.exists(new_folder_path):
                self.update_status(f"Folder already exists: {folder_name}", error=True)
                messagebox.showerror("Error", f"Folder '{folder_name}' already exists")
                return
            
            os.makedirs(new_folder_path)
            self.refresh()
            self.update_status(f"Folder '{folder_name}' created successfully")
            messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully")
            
        except PermissionError:
            self.update_status(f"Permission denied: Cannot create folder", error=True)
            messagebox.showerror("Permission Denied", 
                               f"You don't have permission to create folders in: {self.current_path}")
        except Exception as e:
            self.update_status(f"Error creating folder: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to create folder: {str(e)}")
    
    def rename_item(self):
        """Rename selected file or folder"""
        if not self.selected_item:
            self.update_status("Please select an item to rename", error=True)
            messagebox.showwarning("No Selection", "Please select a file or folder to rename")
            return
        
        if self.selected_item == "..":
            self.update_status("Cannot rename parent directory", error=True)
            messagebox.showwarning("Invalid Operation", "Cannot rename parent directory")
            return
        
        old_path = self.get_item_path(self.selected_item)
        if not old_path or not os.path.exists(old_path):
            return
        
        old_name = os.path.basename(old_path)
        new_name = simpledialog.askstring("Rename", f"Enter new name:", initialvalue=old_name)
        
        if not new_name or new_name.strip() == "":
            return
        
        new_name = new_name.strip()
        new_path = os.path.join(self.current_path, new_name)
        
        try:
            if os.path.exists(new_path):
                self.update_status(f"Item with name '{new_name}' already exists", error=True)
                messagebox.showerror("Error", f"An item with name '{new_name}' already exists")
                return
            
            os.rename(old_path, new_path)
            self.refresh()
            self.update_status(f"Renamed '{old_name}' to '{new_name}' successfully")
            messagebox.showinfo("Success", f"Renamed '{old_name}' to '{new_name}'")
            
        except PermissionError:
            self.update_status(f"Permission denied: Cannot rename item", error=True)
            messagebox.showerror("Permission Denied", 
                               f"You don't have permission to rename: {old_name}")
        except Exception as e:
            self.update_status(f"Error renaming item: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to rename: {str(e)}")
    
    def delete_item(self):
        """Delete selected file or folder with confirmation"""
        if not self.selected_item:
            self.update_status("Please select an item to delete", error=True)
            messagebox.showwarning("No Selection", "Please select a file or folder to delete")
            return
        
        if self.selected_item == "..":
            self.update_status("Cannot delete parent directory", error=True)
            messagebox.showwarning("Invalid Operation", "Cannot delete parent directory")
            return
        
        item_path = self.get_item_path(self.selected_item)
        if not item_path or not os.path.exists(item_path):
            return
        
        item_name = os.path.basename(item_path)
        is_directory = os.path.isdir(item_path)
        
        # Confirmation dialog
        item_type = "folder" if is_directory else "file"
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete this {item_type}?\n\n"
                                     f"Name: {item_name}\n"
                                     f"Path: {item_path}\n\n"
                                     f"This action cannot be undone!",
                                     icon='warning')
        
        if not confirm:
            self.update_status("Delete operation cancelled")
            return
        
        try:
            if is_directory:
                shutil.rmtree(item_path)
                self.update_status(f"Folder '{item_name}' deleted successfully")
                messagebox.showinfo("Success", f"Folder '{item_name}' deleted successfully")
            else:
                os.remove(item_path)
                self.update_status(f"File '{item_name}' deleted successfully")
                messagebox.showinfo("Success", f"File '{item_name}' deleted successfully")
            
            self.refresh()
            
        except PermissionError:
            self.update_status(f"Permission denied: Cannot delete item", error=True)
            messagebox.showerror("Permission Denied", 
                               f"You don't have permission to delete: {item_name}")
        except Exception as e:
            self.update_status(f"Error deleting item: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def open_item(self):
        """Open file or folder with system default application"""
        if not self.selected_item:
            self.update_status("Please select an item to open", error=True)
            messagebox.showwarning("No Selection", "Please select a file or folder to open")
            return
        
        if self.selected_item == "..":
            self.go_back()
            return
        
        item_path = self.get_item_path(self.selected_item)
        if not item_path or not os.path.exists(item_path):
            return
        
        try:
            system = platform.system()
            
            if os.path.isdir(item_path):
                # Open directory in file explorer
                if system == 'Windows':
                    os.startfile(item_path)
                elif system == 'Darwin':  # macOS
                    subprocess.run(['open', item_path])
                else:  # Linux
                    subprocess.run(['xdg-open', item_path])
                self.update_status(f"Opened directory: {os.path.basename(item_path)}")
            else:
                # Open file with default application
                if system == 'Windows':
                    os.startfile(item_path)
                elif system == 'Darwin':  # macOS
                    subprocess.run(['open', item_path])
                else:  # Linux
                    subprocess.run(['xdg-open', item_path])
                self.update_status(f"Opened file: {os.path.basename(item_path)}")
                
        except Exception as e:
            self.update_status(f"Error opening item: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to open: {str(e)}")
    
    def show_properties(self):
        """Show properties of selected item"""
        if not self.selected_item or self.selected_item == "..":
            return
        
        item_path = self.get_item_path(self.selected_item)
        if not item_path:
            return
        
        if os.path.isdir(item_path):
            self.show_directory_details(item_path)
        else:
            self.show_file_details(item_path)
    
    def update_status(self, message, error=False):
        """Update status bar with message"""
        self.status_label.config(text=message)
        if error:
            self.status_label.config(fg='#ff6b6b')
        else:
            theme = self.dark_theme if self.dark_mode else self.light_theme
            self.status_label.config(fg=theme['status_fg'])
    
    def show_file_details(self, file_path):
        """Show detailed information about a file"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        try:
            stat_info = os.stat(file_path)
            
            details = []
            details.append("=" * 50)
            details.append("FILE INFORMATION")
            details.append("=" * 50)
            details.append(f"\nName: {os.path.basename(file_path)}")
            details.append(f"Full Path: {file_path}")
            details.append(f"Type: {self.get_file_type(file_path)}")
            details.append(f"Size: {self.format_size(stat_info.st_size)}")
            details.append(f"\nPermissions: {self.get_file_permissions(file_path)}")
            details.append(f"\nCreated: {datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            details.append(f"Modified: {datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            details.append(f"Accessed: {datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Try to read file content if it's a text file
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                text_extensions = ['.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.log', '.csv']
                
                if ext in text_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if len(content) > 10000:
                                content = content[:10000] + "\n\n... (File too large, showing first 10000 characters)"
                            details.append("\n" + "=" * 50)
                            details.append("FILE CONTENT (Preview)")
                            details.append("=" * 50)
                            details.append("\n" + content)
                    except Exception as e:
                        details.append(f"\n\nCould not read file content: {str(e)}")
            
            self.details_text.insert(1.0, '\n'.join(details))
            
        except Exception as e:
            self.details_text.insert(1.0, f"Error reading file details: {str(e)}")
        
        self.details_text.config(state=tk.DISABLED)
    
    def show_directory_details(self, dir_path):
        """Show detailed information about a directory"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        try:
            stat_info = os.stat(dir_path)
            
            # Count items in directory
            try:
                items = os.listdir(dir_path)
                dir_count = sum(1 for item in items if os.path.isdir(os.path.join(dir_path, item)))
                file_count = sum(1 for item in items if os.path.isfile(os.path.join(dir_path, item)))
            except:
                dir_count = file_count = "Unknown"
            
            details = []
            details.append("=" * 50)
            details.append("DIRECTORY INFORMATION")
            details.append("=" * 50)
            details.append(f"\nName: {os.path.basename(dir_path)}")
            details.append(f"Full Path: {dir_path}")
            details.append(f"Type: Directory")
            details.append(f"\nSubdirectories: {dir_count}")
            details.append(f"Files: {file_count}")
            details.append(f"\nPermissions: {self.get_file_permissions(dir_path)}")
            details.append(f"\nCreated: {datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            details.append(f"Modified: {datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            details.append(f"Accessed: {datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')}")
            
            self.details_text.insert(1.0, '\n'.join(details))
            
        except Exception as e:
            self.details_text.insert(1.0, f"Error reading directory details: {str(e)}")
        
        self.details_text.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
