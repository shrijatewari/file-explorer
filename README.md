# 📁 File Explorer - Operating Systems Mini Project

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A modern, feature-rich **File Explorer** desktop application built with **Python** and **Tkinter** that demonstrates core Operating Systems concepts including file handling, directory navigation, process management, and permissions. This project showcases applied OS knowledge through a fully functional file management system.

## ✨ Features

### 🎯 Core Functionality
- **📂 Directory Navigation**: Intuitive browsing with double-click navigation, breadcrumb path bar, and quick access buttons
- **📋 File Listing**: Comprehensive list view with icons, showing file size, type, and modification dates
- **🔍 Search & Filter**: Real-time search functionality with support for filtering by name, type, and hidden files
- **📊 File Details**: Detailed metadata panel showing permissions, timestamps, size, and file type
- **🌓 Dark Mode**: Toggle between light and dark themes for comfortable viewing

### 🛠️ File Operations
- **➕ Create Folders**: Create new directories with validation
- **✏️ Rename**: Rename files and folders with duplicate checking
- **🗑️ Delete**: Safe deletion with confirmation dialogs
- **📂 Open**: Open files with system default applications (cross-platform)
- **👁️ Preview**: In-app text file viewer for quick content preview
- **📋 Copy Path**: Copy file/folder paths to clipboard

### ⚡ Advanced Features
- **🔄 Multi-threaded Loading**: Non-blocking directory loading for large folders
- **📊 Sorting Options**: Sort by name, size, date, or type (ascending/descending)
- **👻 Hidden Files Toggle**: Show/hide hidden files and folders
- **⌨️ Keyboard Shortcuts**: Quick access via keyboard (Ctrl+N, Ctrl+F, Delete, Enter, etc.)
- **🖱️ Context Menu**: Right-click context menu for quick operations
- **📱 Status Bar**: Real-time status updates for all operations
- **🎨 Modern UI**: Clean, intuitive interface with visual indicators

### 🔒 OS Concepts Demonstrated
- **File System Navigation**: Directory traversal and path resolution
- **File Metadata**: Accessing and displaying file system information
- **Permissions**: Reading and interpreting file permission bits (rwx)
- **Process Management**: Opening files with system applications
- **Error Handling**: Graceful handling of permission errors and invalid operations
- **Cross-platform Support**: Windows, macOS, and Linux compatibility

## 📸 Screenshots

> 
> - Main interface with file listing
   <img width="1196" height="775" alt="image" src="https://github.com/user-attachments/assets/c514ee80-fda0-482e-97b7-b11d509e3245" />

> - File details panel
   <img width="1512" height="856" alt="image" src="https://github.com/user-attachments/assets/3782e474-fdfc-4a39-9f34-d70e5f28b8b9" />

> - Search functionality
   <img width="1185" height="182" alt="image" src="https://github.com/user-attachments/assets/85d80777-5ea5-442f-b5b7-413a360f634a" />

> - Additional pictures
   <img width="340" height="296" alt="image" src="https://github.com/user-attachments/assets/fc7fd9cf-5df2-4e64-8261-fb6092d9222e" />

   

## 🚀 Quick Start

### Prerequisites
- **Python 3.6+** (tested on Python 3.8+)
- **Tkinter** (usually comes pre-installed with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/file-explorer.git
   cd file-explorer
   ```

2. **Verify Tkinter installation**
   ```bash
   python3 -c "import tkinter; print('Tkinter is available')"
   ```
   
   If Tkinter is not available:
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **macOS**: Tkinter comes with Python
   - **Windows**: Tkinter comes with Python

3. **Run the application**
   ```bash
   python3 main.py
   ```

> **Note**: No external dependencies required! This project uses only Python standard library modules.

## 📖 Usage Guide

### Navigation
- **Double-click** folders to navigate into them
- **Double-click** files to open with system default application
- Use **Back** button or double-click ".." to go to parent directory
- Use **Home** button to navigate to user home directory
- Enter a path in the path bar and press **Enter** or click **Go**

### File Operations
- **Create Folder**: Click "📁 New" button or press `Ctrl+N`
- **Rename**: Select an item and click "✏️ Rename" button
- **Delete**: Select an item and click "🗑️ Delete" button (confirmation required)
- **Open**: Select an item and click "📂 Open" button or press `Enter`
- **Right-click**: Access context menu for quick operations

### Search & Filter
- Type in the **Search** bar to filter files/folders in real-time
- Use **Sort** dropdown to sort by name, size, date, or type
- Toggle **Show Hidden** checkbox to display hidden files
- Click **Clear** to remove search filter

### Keyboard Shortcuts
- `Ctrl+N` - Create new folder
- `Ctrl+F` - Focus search bar
- `Ctrl+H` - Go to home directory
- `F5` - Refresh current directory
- `Enter` - Open selected item
- `Delete` - Delete selected item

### Viewing Files
- **Single-click** on any item to view its details in the right panel
- **Double-click** text files to choose between in-app viewer or system default
- File content preview is available in the details panel for text files

## 🏗️ Project Structure

```
file-explorer/
├── main.py                 # Application entry point
├── ui/
│   ├── __init__.py
│   ├── explorer_ui.py      # Main UI component
│   └── theme_manager.py    # Theme management
├── utils/
│   ├── __init__.py
│   ├── file_ops.py         # File operations (create, delete, rename, etc.)
│   ├── metadata.py         # File metadata extraction
│   └── search_utils.py     # Search and filtering utilities
├── assets/
│   ├── icons/              # Icon assets (optional)
│   └── config.json         # Application configuration
├── README.md               # This file
└── requirements.txt        # Dependencies (standard library only)
```

## 🧪 Technical Details

### Technologies Used
- **Python 3.6+**: Core programming language
- **Tkinter**: GUI framework (standard library)
- **Standard Libraries**: `os`, `shutil`, `datetime`, `stat`, `subprocess`, `platform`, `threading`, `pathlib`, `json`

### Architecture
- **Modular Design**: Separated into UI, utilities, and core logic
- **Object-Oriented**: Class-based structure for maintainability
- **Threading**: Multi-threaded directory loading to prevent GUI freezing
- **Error Handling**: Comprehensive error handling throughout

### Cross-Platform Support
- **Windows**: Uses `os.startfile()` for opening files
- **macOS**: Uses `subprocess.run(['open', path])`
- **Linux**: Uses `subprocess.run(['xdg-open', path])`

## 🎓 Operating Systems Concepts

This project demonstrates:

1. **File System Operations**
   - Directory traversal and navigation
   - File and directory creation/deletion
   - Path resolution and normalization

2. **File Metadata**
   - File size, type, and permissions
   - Creation, modification, and access timestamps
   - Permission bit interpretation (rwx for owner/group/others)

3. **Process Management**
   - Launching system applications
   - Cross-platform process execution

4. **Error Handling**
   - Permission error handling
   - Invalid path validation
   - Graceful error recovery

5. **System Integration**
   - Platform detection
   - System-specific file operations
   - Clipboard integration

## 🔧 Configuration

Edit `assets/config.json` to customize:
- Default starting path
- Show hidden files preference
- Default sort order
- Theme preference
- Recent and favorite folders

## 🐛 Troubleshooting

### Tkinter Import Error
If you get `ModuleNotFoundError: No module named 'tkinter'`:
- **Linux**: Install with `sudo apt-get install python3-tk`
- **macOS/Windows**: Should be included with Python

### Permission Errors
- The application handles permission errors gracefully
- Some system directories may require elevated permissions
- Check file/folder permissions if operations fail

### Large Directories
- Large directories load in a separate thread to prevent freezing
- Search and filtering may take a moment for directories with many files

## 🚧 Future Enhancements

Potential improvements:
- [ ] Recursive search across subdirectories
- [ ] File/folder copy and move operations
- [ ] File icons/thumbnails for images
- [ ] Multiple selection for batch operations
- [ ] Recent files/directories history
- [ ] Favorite folders quick access
- [ ] Disk usage visualization
- [ ] File compression/decompression (zip, tar)
- [ ] Drag and drop support
- [ ] Auto-refresh on file system changes

## 📝 License

This project is created for educational purposes to demonstrate Operating Systems concepts.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/shrijatewari)
- Email: shrijatewari@gmail.com

## 🙏 Acknowledgments

- Built as part of Operating Systems coursework
- Demonstrates practical application of OS concepts
- Uses only Python standard library for portability

## 📊 Project Status

✅ **Core Features**: Complete  
✅ **File Operations**: Complete  
✅ **UI/UX**: Complete  
✅ **Error Handling**: Complete  
✅ **Cross-platform**: Complete  
🔄 **Documentation**: In Progress  

---

**⭐ If you find this project helpful, consider giving it a star!**
