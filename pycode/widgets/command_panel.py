# === ./pycode/widgets/command_panel.py ===

from pathlib import Path
from typing import List, Dict, Tuple
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Static, ListView, ListItem, Label
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message

from ..services.file_service import FileService
from ..messages import OpenFile, UpdateStatus

class CommandPanel(Widget):
    """
    A multi-functional command/search panel at the bottom of the IDE.
    """
    class FileSelected(Message):
        """Posted when a file is selected from the search results."""
        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()

    DEFAULT_CSS = """
    CommandPanel {
        height: auto;
        min-height: 1;
        max-height: 50%;
    }
    #search-input {
        display: none;
        border: heavy #44475a;
        padding: 0 1;
    }
    #results-list {
        display: none;
        height: 1fr;
        border: heavy #44475a;
    }
    #status-bar {
        height: 1;
        width: 100%;
        padding: 0 1;
        background: $primary-lighten-2;
        color: $text;
    }
    """
    
    # Reactive variable to control the display mode
    show_search = reactive(False)

    def __init__(
        self, 
        files: List[Path],
        git_statuses: Dict[str, str],
        git_branch: str,
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.all_files = files
        self.git_statuses = git_statuses
        self.file_service = FileService()
        self.status_text = f"Branch: {git_branch}"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for files...", id="search-input")
        yield ListView(id="results-list")
        yield Static(self.status_text, id="status-bar")
    
    def on_mount(self) -> None:
        self.post_message(UpdateStatus(self.status_text))

    def watch_show_search(self, show_search: bool) -> None:
        """Called when the show_search reactive variable changes."""
        self.query_one("#search-input").display = show_search
        self.query_one("#results-list").display = show_search
        self.query_one("#status-bar").display = not show_search

        if show_search:
            self.query_one("#search-input").focus()
        else:
            self.query_one("#search-input").value = ""
            self.query_one(ListView).clear()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle changes in the search input."""
        search_query = event.value
        list_view = self.query_one(ListView)
        list_view.clear()

        if search_query:
            results = self.file_service.fuzzy_search_files(search_query, self.all_files)
            for path, score in results:
                status = self.git_statuses.get(str(path), "")
                list_item = ListItem(Label(f"{path.name} [dim]{path.parent}[/]  [yellow]({status})[/]"))
                list_item.path = path
                list_view.append(list_item)
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Called when a file is selected from the list."""
        selected_item = event.item
        if hasattr(selected_item, "path"):
            self.post_message(OpenFile(path=selected_item.path))
            self.show_search = False

    def action_activate_search(self) -> None:
        """Action to activate search mode, called by a key binding."""
        self.show_search = True

    def action_cancel_search(self) -> None:
        """Action to cancel search mode."""
        self.show_search = False