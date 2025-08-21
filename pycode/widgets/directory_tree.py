# === ./pycode/widgets/directory_tree.py ===

from pathlib import Path
from typing import Dict
from textual.widgets import DirectoryTree
from textual.widgets._tree import TreeNode
from textual.widgets._directory_tree import DirEntry
from rich.text import Text

from ..messages import OpenFile

class DirTree(DirectoryTree):
    """
    A DirectoryTree that shows Git statuses and emits an OpenFile message on selection.
    """
    def __init__(self, path: str, *, id: str | None = None, git_statuses: Dict[str, str]):
        self.git_statuses = git_statuses
        super().__init__(path, id=id)

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """
        Called when a file is selected in the tree.
        """
        event.stop()
        self.post_message(OpenFile(path=event.path))

    def render_label(
        self, node: TreeNode[DirEntry], is_cursor: bool, is_expanded: bool
    ) -> Text:
        """
        Renders a label for a directory entry, adding a Git status indicator.
        """
        # Get the original label from the base class, which is a Text object
        label = super().render_label(node, is_cursor, is_expanded)
        
        node_path = node.data.path
        if node_path is None:
            return label

        status = self.git_statuses.get(str(node_path))
        if status:
            # Append the status to the Text object to preserve its type
            status_style = "green" if status == "??" else "yellow"
            label.append(f" [b {status_style}]({status})[/]")
        
        return label