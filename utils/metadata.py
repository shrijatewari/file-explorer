"""
=== File: metadata.py ===
Handles file and directory metadata extraction and formatting.
Provides utilities for getting file information like size, permissions, timestamps.
"""

import os
import stat
from datetime import datetime
from pathlib import Path


class MetadataExtractor:
    """Extract and format file/directory metadata"""
    
    @staticmethod
    def format_size(size):
        """
        Format file size in human-readable format.
        
        Args:
            size: File size in bytes
            
        Returns:
            Formatted string (e.g., "1.23 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    @staticmethod
    def get_file_type(path):
        """
        Get file type description based on extension.
        
        Args:
            path: File path
            
        Returns:
            File type string
        """
        if os.path.isdir(path):
            return "Directory"
        elif os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            type_map = {
                '.py': 'Python Script', '.txt': 'Text File', '.pdf': 'PDF Document',
                '.jpg': 'JPEG Image', '.jpeg': 'JPEG Image', '.png': 'PNG Image',
                '.gif': 'GIF Image', '.bmp': 'Bitmap Image', '.svg': 'SVG Image',
                '.mp4': 'MP4 Video', '.avi': 'AVI Video', '.mov': 'QuickTime Video',
                '.mp3': 'MP3 Audio', '.wav': 'WAV Audio', '.flac': 'FLAC Audio',
                '.zip': 'ZIP Archive', '.tar': 'TAR Archive', '.gz': 'GZIP Archive',
                '.doc': 'Word Document', '.docx': 'Word Document',
                '.xls': 'Excel Spreadsheet', '.xlsx': 'Excel Spreadsheet',
                '.html': 'HTML File', '.css': 'CSS File', '.js': 'JavaScript File',
                '.json': 'JSON File', '.xml': 'XML File', '.md': 'Markdown File',
                '.log': 'Log File', '.csv': 'CSV File', '.sql': 'SQL File',
            }
            return type_map.get(ext, 'File')
        else:
            return "Unknown"
    
    @staticmethod
    def get_file_permissions(path):
        """
        Get file permissions in readable format (rwxrwxrwx).
        
        Args:
            path: File or directory path
            
        Returns:
            Permission string (e.g., "rwxr-xr--")
        """
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
        except Exception:
            return "Unknown"
    
    @staticmethod
    def get_file_info(path):
        """
        Get comprehensive file information.
        
        Args:
            path: File or directory path
            
        Returns:
            Dictionary with file metadata
        """
        try:
            stat_info = os.stat(path)
            
            info = {
                'name': os.path.basename(path),
                'full_path': path,
                'type': MetadataExtractor.get_file_type(path),
                'size': MetadataExtractor.format_size(stat_info.st_size) if os.path.isfile(path) else "",
                'permissions': MetadataExtractor.get_file_permissions(path),
                'created': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'accessed': datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                'is_directory': os.path.isdir(path),
                'is_file': os.path.isfile(path),
            }
            
            # Add directory-specific info
            if os.path.isdir(path):
                try:
                    items = os.listdir(path)
                    info['subdirectories'] = sum(1 for item in items if os.path.isdir(os.path.join(path, item)))
                    info['files'] = sum(1 for item in items if os.path.isfile(os.path.join(path, item)))
                except:
                    info['subdirectories'] = "Unknown"
                    info['files'] = "Unknown"
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def is_text_file(path):
        """
        Check if a file is a text file based on extension.
        
        Args:
            path: File path
            
        Returns:
            True if file is likely a text file
        """
        if not os.path.isfile(path):
            return False
        
        ext = os.path.splitext(path)[1].lower()
        text_extensions = ['.txt', '.py', '.js', '.html', '.css', '.json', 
                          '.xml', '.md', '.log', '.csv', '.sql', '.sh', 
                          '.bat', '.yml', '.yaml', '.ini', '.cfg', '.conf']
        return ext in text_extensions

