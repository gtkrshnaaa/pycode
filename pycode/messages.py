# === ./pycode/messages.py ===

from pathlib import Path
from textual.message import Message

class OpenFile(Message):
    """
    Message to request opening a file in the editor.
    """
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()

class UpdateStatus(Message):
    """
    Message to request an update to a status display.
    """
    def __init__(self, text: str) -> None:
        self.text = text
        super().__init__()