import os
from typing import List
import json
from pathlib import Path

def ensure_directory(path: str) -> str:
    """
    Ensure directory exists, create if it doesn't
    Returns the directory path
    """
    os.makedirs(path, exist_ok=True)
    return path

def get_safe_filename(filename: str) -> str:
    """
    Convert filename to safe version by removing invalid characters
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()

def save_metadata(metadata: dict, filepath: str) -> str:
    """
    Save metadata to JSON file
    Returns the file path
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    return filepath

def load_metadata(filepath: str) -> dict:
    """
    Load metadata from JSON file
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def cleanup_temp_files(file_paths: List[str]) -> None:
    """
    Clean up temporary files
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {str(e)}")
