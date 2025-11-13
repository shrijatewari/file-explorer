"""
=== File: explorer_ui.py ===
Main UI component for the File Explorer application.
Handles all GUI elements, user interactions, and integrates with utility modules.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
from datetime import datetime

# Import utility modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.metadata import MetadataExtractor
from utils.file_ops import FileOperations
from utils.search_utils import SearchUtils
from ui.theme_manager import ThemeManager


class FileExplorerUI:
    """Main UI class for File Explorer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer - OS Mini Project")
        self.root.geometry("1200x750")
        
        # Initialize managers
        self.theme_manager = ThemeManager()
        self.metadata_extractor = MetadataExtractor()
        self.file_ops = FileOperations()
        self.search_utils = SearchUtils()
        
        # Current directory
        self.current_path = os.path.expanduser("~")
        
        # Selected item for context menu
        self.selected_item = None
        
        # UI state
        self.show_hidden = False
        self.sort_by = 'name'  # 'name', 'size', 'date', 'type'
        self.sort_reverse = False
        
        # Setup UI
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
        # Load initial directory
        self.navigate_to(self.current_path)
    
    def setup_ui(self):
        """Setup the user interface"""
        theme = self.theme_manager.get_theme()
        
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
        
        new_folder_btn = tk.Button(action_frame, text="📁 New", command=self.create_folder,
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
                             width=35, relief=tk.SUNKEN, bd=2, bg=theme['entry_bg'], fg=theme['entry_fg'])
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
        
        # Search and filter bar
        search_frame = tk.Frame(main_frame, bg=theme['bg'])
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="🔍 Search:", bg=theme['bg'], fg=theme['fg'], font=('Arial', 10))
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10),
                               width=25, relief=tk.SUNKEN, bd=2, bg=theme['entry_bg'], fg=theme['entry_fg'])
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Sort options
        sort_label = tk.Label(search_frame, text="Sort:", bg=theme['bg'], fg=theme['fg'], font=('Arial', 10))
        sort_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.sort_var = tk.StringVar(value='name')
        sort_menu = ttk.Combobox(search_frame, textvariable=self.sort_var, width=10,
                                values=['name', 'size', 'date', 'type'], state='readonly')
        sort_menu.pack(side=tk.LEFT, padx=(0, 5))
        sort_menu.bind('<<ComboboxSelected>>', lambda e: self.apply_sort())
        
        # Hidden files toggle
        self.hidden_var = tk.BooleanVar()
        hidden_check = tk.Checkbutton(search_frame, text="Show Hidden", variable=self.hidden_var,
                                     bg=theme['bg'], fg=theme['fg'], font=('Arial', 9),
                                     command=self.toggle_hidden_files)
        hidden_check.pack(side=tk.LEFT, padx=(10, 5))
        
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
        self.tree.heading('#0', text='Name', anchor=tk.W, command=lambda: self.sort_column('name'))
        self.tree.heading('Size', text='Size', anchor=tk.W, command=lambda: self.sort_column('size'))
        self.tree.heading('Type', text='Type', anchor=tk.W, command=lambda: self.sort_column('type'))
        self.tree.heading('Modified', text='Modified', anchor=tk.W, command=lambda: self.sort_column('date'))
        
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('Size', width=100, minwidth=80)
        self.tree.column('Type', width=100, minwidth=80)
        self.tree.column('Modified', width=150, minwidth=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<ButtonRelease-1>', self.on_item_select)
        self.tree.bind('<Button-3>', self.show_context_menu)  # Right-click
        self.tree.bind('<Delete>', lambda e: self.delete_item())
        self.tree.bind('<Return>', lambda e: self.open_item())
        
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
                                                      bg=theme['text_bg'], fg=theme['text_fg'],
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
        
        # Store widgets for theme updates
        self.widgets = {
            'main_frame': main_frame,
            'nav_frame': nav_frame,
            'left_panel': left_panel,
            'right_panel': right_panel,
            'status_frame': status_frame
        }
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.create_folder())
        self.root.bind('<Control-f>', lambda e: self.focus_search())
        self.root.bind('<Control-h>', lambda e: self.go_home())
        self.root.bind('<F5>', lambda e: self.refresh())
    
    def focus_search(self):
        """Focus on search entry"""
        for widget in self.root.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, tk.Entry) and grandchild.get() == self.search_var.get():
                            grandchild.focus()
                            return
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.theme_manager.toggle_theme()
        theme = self.theme_manager.get_theme()
        self.dark_mode_btn.config(text="☀️ Light" if self.theme_manager.is_dark() else "🌙 Dark")
        self.update_status("Theme switched to " + theme['name'] + " mode")
        # Note: Full theme application would require updating all widgets
    
    def toggle_hidden_files(self):
        """Toggle showing hidden files"""
        self.show_hidden = self.hidden_var.get()
        self.load_directory(self.current_path)
        self.update_status("Hidden files " + ("shown" if self.show_hidden else "hidden"))
    
    def sort_column(self, column):
        """Sort by column"""
        if self.sort_by == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_by = column
            self.sort_reverse = False
        self.apply_sort()
    
    def apply_sort(self):
        """Apply sorting to file list"""
        sort_value = self.sort_var.get()
        if sort_value:
            self.sort_by = sort_value
            self.load_directory(self.current_path)
    
    def get_item_path(self, item_text):
        """Get full path from item text"""
        if item_text.startswith('📁 ') or item_text.startswith('📄 '):
            name = item_text[2:]
        else:
            name = item_text
        
        if name == "..":
            return None
        
        return os.path.join(self.current_path, name)
    
    def load_directory(self, path, filter_text=""):
        """Load directory contents into the treeview (with threading support)"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Use threading for large directories
        def load_thread():
            try:
                # Add parent directory entry
                if path != os.path.dirname(path):
                    self.root.after(0, lambda: self.tree.insert('', 0, text="..", 
                                                               values=('', 'Parent Directory', ''),
                                                               tags=('directory',)))
                
                # Get all items in directory
                items = []
                try:
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        items.append(item_path)
                except PermissionError:
                    self.root.after(0, lambda: self.update_status(f"Permission denied: {path}", error=True))
                    self.root.after(0, lambda: messagebox.showerror("Permission Denied",
                                                                   f"You don't have permission to access: {path}"))
                    return
                
                # Filter hidden files
                if not self.show_hidden:
                    items = self.search_utils.filter_hidden(items, show_hidden=False)
                
                # Apply search filter
                if filter_text:
                    filter_lower = filter_text.lower()
                    items = [item for item in items 
                            if filter_lower in os.path.basename(item).lower()]
                
                # Sort items
                if self.sort_by == 'name':
                    items.sort(key=lambda x: os.path.basename(x).lower(), reverse=self.sort_reverse)
                elif self.sort_by == 'size':
                    def get_size(p):
                        try:
                            if os.path.isdir(p):
                                return self.file_ops.get_directory_size(p)
                            return os.path.getsize(p)
                        except:
                            return 0
                    items.sort(key=get_size, reverse=self.sort_reverse)
                elif self.sort_by == 'date':
                    def get_date(p):
                        try:
                            return os.path.getmtime(p)
                        except:
                            return 0
                    items.sort(key=get_date, reverse=self.sort_reverse)
                elif self.sort_by == 'type':
                    items.sort(key=lambda x: (os.path.isdir(x), 
                                             self.metadata_extractor.get_file_type(x).lower()),
                             reverse=self.sort_reverse)
                
                # Separate directories and files
                directories = [item for item in items if os.path.isdir(item)]
                files = [item for item in items if os.path.isfile(item)]
                
                # Add directories
                dir_items = []
                for item_path in directories:
                    name = os.path.basename(item_path)
                    try:
                        stat_info = os.stat(item_path)
                        size = ""
                        modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        file_type = "Directory"
                        dir_items.append((name, size, file_type, modified))
                    except Exception:
                        pass
                
                # Add files
                file_items = []
                for item_path in files:
                    name = os.path.basename(item_path)
                    try:
                        stat_info = os.stat(item_path)
                        size = self.metadata_extractor.format_size(stat_info.st_size)
                        modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        file_type = self.metadata_extractor.get_file_type(item_path)
                        file_items.append((name, size, file_type, modified))
                    except Exception:
                        pass
                
                # Update UI in main thread
                def update_ui():
                    for name, size, file_type, modified in dir_items:
                        self.tree.insert('', tk.END, text=f"📁 {name}", 
                                       values=(size, file_type, modified), tags=('directory',))
                    for name, size, file_type, modified in file_items:
                        self.tree.insert('', tk.END, text=f"📄 {name}",
                                       values=(size, file_type, modified), tags=('file',))
                    self.tree.tag_configure('directory', foreground='#2196F3')
                    self.tree.tag_configure('file', foreground='#333')
                
                self.root.after(0, update_ui)
                
                # Update status
                item_count = len(directories) + len(files)
                if filter_text:
                    self.root.after(0, lambda: self.update_status(f"Found {item_count} items matching '{filter_text}'"))
                else:
                    self.root.after(0, lambda: self.update_status(f"Loaded {item_count} items from {path}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error loading directory: {str(e)}", error=True))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load directory: {str(e)}"))
        
        # Start loading in thread
        thread = threading.Thread(target=load_thread, daemon=True)
        thread.start()
    
    def navigate_to(self, path):
        """Navigate to a specific directory"""
        try:
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
            context_menu.add_command(label="Copy Path", command=self.copy_path)
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
        
        success, message, new_path = self.file_ops.create_folder(self.current_path, folder_name)
        
        if success:
            self.refresh()
            self.update_status(message)
            messagebox.showinfo("Success", message)
        else:
            self.update_status(message, error=True)
            messagebox.showerror("Error", message)
    
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
        
        if not new_name:
            return
        
        success, message, new_path = self.file_ops.rename_item(old_path, new_name)
        
        if success:
            self.refresh()
            self.update_status(message)
            messagebox.showinfo("Success", message)
        else:
            self.update_status(message, error=True)
            messagebox.showerror("Error", message)
    
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
        
        success, message = self.file_ops.delete_item(item_path)
        
        if success:
            self.refresh()
            self.update_status(message)
            messagebox.showinfo("Success", message)
        else:
            self.update_status(message, error=True)
            messagebox.showerror("Error", message)
    
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
        
        # Check if it's a text file for in-app viewing
        if os.path.isfile(item_path) and self.metadata_extractor.is_text_file(item_path):
            response = messagebox.askyesnocancel("Open File", 
                                                f"Open '{os.path.basename(item_path)}' in:\n\n"
                                                "Yes - View in app\n"
                                                "No - Open with system default\n"
                                                "Cancel - Do nothing")
            if response is True:
                self.view_file_in_app(item_path)
                return
            elif response is False:
                pass  # Continue to system default
            else:
                return
        
        success, message = self.file_ops.open_with_system(item_path)
        
        if success:
            self.update_status(message)
        else:
            self.update_status(message, error=True)
            messagebox.showerror("Error", message)
    
    def copy_path(self):
        """Copy selected item path to clipboard"""
        if not self.selected_item or self.selected_item == "..":
            return
        
        item_path = self.get_item_path(self.selected_item)
        if item_path:
            self.root.clipboard_clear()
            self.root.clipboard_append(item_path)
            self.update_status(f"Path copied to clipboard: {item_path}")
    
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
    
    def view_file_in_app(self, file_path):
        """View text file content in a new window"""
        view_window = tk.Toplevel(self.root)
        view_window.title(f"File Viewer - {os.path.basename(file_path)}")
        view_window.geometry("800x600")
        
        text_area = scrolledtext.ScrolledText(view_window, wrap=tk.WORD,
                                             font=('Courier', 11))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                text_area.insert(1.0, content)
        except Exception as e:
            text_area.insert(1.0, f"Error reading file: {str(e)}")
        
        text_area.config(state=tk.DISABLED)
        self.update_status(f"Opened file in app: {os.path.basename(file_path)}")
    
    def update_status(self, message, error=False):
        """Update status bar with message"""
        theme = self.theme_manager.get_theme()
        self.status_label.config(text=message)
        if error:
            self.status_label.config(fg=theme['error_fg'])
        else:
            self.status_label.config(fg=theme['status_fg'])
    
    def show_file_details(self, file_path):
        """Show detailed information about a file"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        try:
            info = self.metadata_extractor.get_file_info(file_path)
            
            if 'error' in info:
                self.details_text.insert(1.0, f"Error: {info['error']}")
            else:
                details = []
                details.append("=" * 50)
                details.append("FILE INFORMATION")
                details.append("=" * 50)
                details.append(f"\nName: {info['name']}")
                details.append(f"Full Path: {info['full_path']}")
                details.append(f"Type: {info['type']}")
                details.append(f"Size: {info['size']}")
                details.append(f"\nPermissions: {info['permissions']}")
                details.append(f"\nCreated: {info['created']}")
                details.append(f"Modified: {info['modified']}")
                details.append(f"Accessed: {info['accessed']}")
                
                # Try to read file content if it's a text file
                if os.path.isfile(file_path) and self.metadata_extractor.is_text_file(file_path):
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
            info = self.metadata_extractor.get_file_info(dir_path)
            
            if 'error' in info:
                self.details_text.insert(1.0, f"Error: {info['error']}")
            else:
                details = []
                details.append("=" * 50)
                details.append("DIRECTORY INFORMATION")
                details.append("=" * 50)
                details.append(f"\nName: {info['name']}")
                details.append(f"Full Path: {info['full_path']}")
                details.append(f"Type: Directory")
                details.append(f"\nSubdirectories: {info.get('subdirectories', 'Unknown')}")
                details.append(f"Files: {info.get('files', 'Unknown')}")
                details.append(f"\nPermissions: {info['permissions']}")
                details.append(f"\nCreated: {info['created']}")
                details.append(f"Modified: {info['modified']}")
                details.append(f"Accessed: {info['accessed']}")
                
                self.details_text.insert(1.0, '\n'.join(details))
            
        except Exception as e:
            self.details_text.insert(1.0, f"Error reading directory details: {str(e)}")
        
        self.details_text.config(state=tk.DISABLED)

