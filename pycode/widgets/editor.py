# === ./pycode/widgets/editor.py ===

from textual.widgets import TextArea

class Editor(TextArea):
    """
    The main text editor widget.
    For now, it's a simple TextArea.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.text = "# Welcome to Pycode!\n\n"
        self.theme = "dracula" 