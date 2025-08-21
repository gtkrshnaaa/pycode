# === ./pycode/app.py ===

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer

from .widgets.directory_tree import DirTree
from .widgets.editor import Editor
from .widgets.terminal import IntegratedTerminal

class PycodeApp(App):
    """A lightweight and modular TUI IDE."""

    # Definisikan CSS untuk styling dan layout
    CSS = """
    Screen {
        layout: vertical;
    }

    #main-container {
        layout: horizontal;
        height: 1fr;
    }

    #sidebar {
        width: 30;
        min-width: 20;
        dock: left;
        border-right: heavy #44475a;
    }
    
    #editor-container {
        layout: vertical;
        width: 1fr;
    }

    Editor {
        height: 1fr;
        border-bottom: heavy #44475a;
    }

    IntegratedTerminal {
        height: 12;
        min-height: 5;
    }
    """

    # Definisikan key bindings
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+s", "save_file", "Save"),
        ("ctrl+p", "find_file", "Find File"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal(id="main-container"):
            yield DirTree(".", id="sidebar")
            with Vertical(id="editor-container"):
                yield Editor()
                yield IntegratedTerminal()
        yield Footer()

    def action_quit(self) -> None:
        """An action to quit the application."""
        self.exit()

    # Placeholder untuk actions lainnya
    def action_save_file(self) -> None:
        pass

    def action_find_file(self) -> None:
        pass