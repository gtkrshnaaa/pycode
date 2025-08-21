# === ./pycode/app.py ===

from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer

from .services.git_service import GitService
from .services.file_service import FileService
from .widgets.directory_tree import DirTree
from .widgets.editor import Editor
from .widgets.command_panel import CommandPanel
from .messages import OpenFile, UpdateStatus

class PycodeApp(App):
    """A lightweight and modular TUI IDE."""

    CSS_PATH = "app.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+s", "save_file", "Save File"),
        ("ctrl+p", "activate_search", "Find File"),
        ("escape", "cancel_search", "Cancel Search"),
    ]

    def __init__(self, path: str = "."):
        self.base_path = Path(path)
        self.git_service = GitService(self.base_path)
        self.file_service = FileService()
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        git_statuses = self.git_service.get_file_statuses()
        project_files = self.file_service.get_project_files(self.base_path)
        git_branch = self.git_service.get_current_branch()

        yield Header()
        with Horizontal(id="main-container"):
            yield DirTree(str(self.base_path), id="sidebar", git_statuses=git_statuses)
            with Vertical(id="editor-container"):
                yield Editor()
                yield CommandPanel(
                    files=project_files, 
                    git_statuses=git_statuses,
                    git_branch=git_branch
                )
        yield Footer()

    def on_open_file(self, message: OpenFile) -> None:
        """Message handler for opening a file."""
        editor = self.query_one(Editor)
        editor.load_file(message.path)
        self.sub_title = str(message.path)
        self.post_message(UpdateStatus(f"Opened: {message.path.name}"))

    def on_update_status(self, message: UpdateStatus) -> None:
        """Message handler for updating the status bar."""
        # This could be useful for more complex status updates later.
        pass

    def action_save_file(self) -> None:
        """Action to save the current file."""
        editor = self.query_one(Editor)
        if editor.current_path:
            content = editor.text
            success = self.file_service.write_file(editor.current_path, content)
            if success:
                self.post_message(UpdateStatus(f"Saved: {editor.current_path.name}"))
            else:
                self.post_message(UpdateStatus(f"Error saving: {editor.current_path.name}"))

    def action_activate_search(self) -> None:
        """Forward the action to the command panel."""
        self.query_one(CommandPanel).action_activate_search()

    def action_cancel_search(self) -> None:
        """Forward the action to the command panel."""
        self.query_one(CommandPanel).action_cancel_search()