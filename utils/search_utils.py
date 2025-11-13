"""
=== File: search_utils.py ===
Handles file and folder search functionality.
Supports both simple name matching and recursive directory search.
"""

import os
from pathlib import Path


class SearchUtils:
    """Utility class for searching files and directories"""
    
    @staticmethod
    def search_in_directory(directory, query, recursive=False, case_sensitive=False):
        """
        Search for files and folders matching a query.
        
        Args:
            directory: Directory to search in
            query: Search query string
            recursive: Whether to search recursively in subdirectories
            case_sensitive: Whether search should be case-sensitive
            
        Returns:
            List of matching file/folder paths
        """
        if not query or not query.strip():
            return []
        
        query = query.strip()
        if not case_sensitive:
            query = query.lower()
        
        matches = []
        
        try:
            if recursive:
                # Recursive search
                for root, dirs, files in os.walk(directory):
                    # Search in directories
                    for dir_name in dirs:
                        name_to_check = dir_name if case_sensitive else dir_name.lower()
                        if query in name_to_check:
                            matches.append(os.path.join(root, dir_name))
                    
                    # Search in files
                    for file_name in files:
                        name_to_check = file_name if case_sensitive else file_name.lower()
                        if query in name_to_check:
                            matches.append(os.path.join(root, file_name))
            else:
                # Non-recursive search (current directory only)
                try:
                    items = os.listdir(directory)
                    for item in items:
                        item_path = os.path.join(directory, item)
                        name_to_check = item if case_sensitive else item.lower()
                        if query in name_to_check:
                            matches.append(item_path)
                except PermissionError:
                    pass
                    
        except Exception:
            pass
        
        return matches
    
    @staticmethod
    def filter_by_extension(items, extensions):
        """
        Filter items by file extension.
        
        Args:
            items: List of file paths
            extensions: List of extensions to filter by (e.g., ['.txt', '.py'])
            
        Returns:
            Filtered list of paths
        """
        if not extensions:
            return items
        
        extensions = [ext.lower() for ext in extensions]
        filtered = []
        
        for item in items:
            if os.path.isfile(item):
                ext = os.path.splitext(item)[1].lower()
                if ext in extensions:
                    filtered.append(item)
            elif os.path.isdir(item) and 'dir' in extensions:
                filtered.append(item)
        
        return filtered
    
    @staticmethod
    def filter_hidden(items, show_hidden=False):
        """
        Filter out hidden files and folders.
        
        Args:
            items: List of file/folder paths
            show_hidden: Whether to include hidden items
            
        Returns:
            Filtered list
        """
        if show_hidden:
            return items
        
        filtered = []
        for item in items:
            name = os.path.basename(item)
            # Check if hidden (starts with . on Unix, or has hidden attribute on Windows)
            if not name.startswith('.'):
                filtered.append(item)
        
        return filtered

