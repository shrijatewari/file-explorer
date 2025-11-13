"""
=== File: file_ops.py ===
Handles creation, deletion, renaming, and movement of files and directories.
Provides OS-level file operations with error handling.
"""

import os
import shutil
import subprocess
import platform
from pathlib import Path


class FileOperations:
    """Handle file and directory operations"""
    
    @staticmethod
    def create_folder(parent_path, folder_name):
        """
        Create a new folder in the specified parent directory.
        
        Args:
            parent_path: Parent directory path
            folder_name: Name of the new folder
            
        Returns:
            Tuple (success: bool, message: str, path: str)
        """
        if not folder_name or not folder_name.strip():
            return False, "Folder name cannot be empty", None
        
        folder_name = folder_name.strip()
        new_folder_path = os.path.join(parent_path, folder_name)
        
        try:
            if os.path.exists(new_folder_path):
                return False, f"Folder '{folder_name}' already exists", None
            
            os.makedirs(new_folder_path, exist_ok=True)
            return True, f"Folder '{folder_name}' created successfully", new_folder_path
            
        except PermissionError:
            return False, f"Permission denied: Cannot create folder in {parent_path}", None
        except Exception as e:
            return False, f"Error creating folder: {str(e)}", None
    
    @staticmethod
    def rename_item(old_path, new_name):
        """
        Rename a file or folder.
        
        Args:
            old_path: Current path of the item
            new_name: New name for the item
            
        Returns:
            Tuple (success: bool, message: str, new_path: str)
        """
        if not new_name or not new_name.strip():
            return False, "Name cannot be empty", None
        
        new_name = new_name.strip()
        parent_dir = os.path.dirname(old_path)
        new_path = os.path.join(parent_dir, new_name)
        
        try:
            if os.path.exists(new_path):
                return False, f"An item with name '{new_name}' already exists", None
            
            os.rename(old_path, new_path)
            return True, f"Renamed to '{new_name}' successfully", new_path
            
        except PermissionError:
            return False, f"Permission denied: Cannot rename {os.path.basename(old_path)}", None
        except Exception as e:
            return False, f"Error renaming: {str(e)}", None
    
    @staticmethod
    def delete_item(item_path):
        """
        Delete a file or folder.
        
        Args:
            item_path: Path to the item to delete
            
        Returns:
            Tuple (success: bool, message: str)
        """
        if not os.path.exists(item_path):
            return False, "Item does not exist"
        
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                return True, f"Folder '{os.path.basename(item_path)}' deleted successfully"
            else:
                os.remove(item_path)
                return True, f"File '{os.path.basename(item_path)}' deleted successfully"
                
        except PermissionError:
            return False, f"Permission denied: Cannot delete {os.path.basename(item_path)}"
        except Exception as e:
            return False, f"Error deleting: {str(e)}"
    
    @staticmethod
    def open_with_system(item_path):
        """
        Open a file or folder with the system's default application.
        
        Args:
            item_path: Path to the file or folder
            
        Returns:
            Tuple (success: bool, message: str)
        """
        if not os.path.exists(item_path):
            return False, "Item does not exist"
        
        try:
            system = platform.system()
            
            if system == 'Windows':
                os.startfile(item_path)
            elif system == 'Darwin':  # macOS
                subprocess.run(['open', item_path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', item_path], check=True)
            
            item_type = "directory" if os.path.isdir(item_path) else "file"
            return True, f"Opened {item_type}: {os.path.basename(item_path)}"
            
        except subprocess.CalledProcessError:
            return False, "Failed to open with default application"
        except Exception as e:
            return False, f"Error opening: {str(e)}"
    
    @staticmethod
    def copy_item(source_path, dest_path):
        """
        Copy a file or folder to a new location.
        
        Args:
            source_path: Source file/folder path
            dest_path: Destination path
            
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)
            else:
                shutil.copy2(source_path, dest_path)
            return True, f"Copied successfully to {dest_path}"
        except Exception as e:
            return False, f"Error copying: {str(e)}"
    
    @staticmethod
    def move_item(source_path, dest_path):
        """
        Move a file or folder to a new location.
        
        Args:
            source_path: Source file/folder path
            dest_path: Destination path
            
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            shutil.move(source_path, dest_path)
            return True, f"Moved successfully to {dest_path}"
        except Exception as e:
            return False, f"Error moving: {str(e)}"
    
    @staticmethod
    def get_directory_size(path):
        """
        Calculate total size of a directory.
        
        Args:
            path: Directory path
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        pass
        except Exception:
            pass
        return total_size

