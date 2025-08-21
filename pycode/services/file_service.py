# === ./pycode/services/file_service.py ===

import os
from pathlib import Path
from typing import List, Tuple

from thefuzz import process

class FileService:
    """
    Handles file system operations like reading, writing, and searching.
    """
    IGNORE_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}
    IGNORE_FILES = {".DS_Store"}

    def get_project_files(self, root_path: Path) -> List[Path]:
        """
        Recursively finds all files in a project directory, ignoring specified folders.
        """
        project_files = []
        for root, dirs, files in os.walk(root_path, topdown=True):
            # Modify dirs in-place to prune search
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            for file in files:
                if file not in self.IGNORE_FILES:
                    project_files.append(Path(root) / file)
        
        return project_files

    def read_file(self, file_path: Path) -> str:
        """
        Reads the content of a file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (FileNotFoundError, IOError, UnicodeDecodeError) as e:
            return f"Error reading file: {e}"

    def write_file(self, file_path: Path, content: str) -> bool:
        """
        Writes content to a file.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except IOError:
            return False

    def fuzzy_search_files(self, query: str, files: List[Path], limit: int = 10) -> List[Tuple[Path, int]]:
        """
        Performs a fuzzy search on a list of files.
        Returns a list of tuples containing (path, score).
        """
        if not query:
            return []
        
        # We pass string paths to the fuzzy search function
        str_files = [str(f) for f in files]
        results = process.extract(query, str_files, limit=limit)
        
        # Convert string paths back to Path objects
        return [(Path(path), score) for path, score in results]