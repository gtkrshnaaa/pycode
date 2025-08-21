# === ./pycode/widgets/editor.py ===

from pathlib import Path
from textual.widgets import TextArea
from ..services.file_service import FileService

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

class Editor(TextArea):
    """
    The main text editor widget that can load and track files,
    and supports syntax highlighting.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.current_path: Path | None = None
        self.file_service = FileService()
        
        # Set the built-in "dracula" theme directly for syntax highlighting.
        # The background transparency will be handled by the CSS file.
        self.theme = "dracula"
        
        self.text = "# Welcome to Pycode!\n\n# Select a file to start editing."

    def load_file(self, path: Path) -> None:
        """
        Loads the content of a file into the text area and automatically
        detects the language for syntax highlighting.
        """
        content = self.file_service.read_file(path)
        self.text = content
        self.current_path = path

        # Automatically detect the language using Pygments
        try:
            lexer = get_lexer_for_filename(str(path))
            self.language = lexer.aliases[0]
        except ClassNotFound:
            self.language = None