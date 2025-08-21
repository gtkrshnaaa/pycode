# === ./pycode/services/git_service.py ===

import git
from pathlib import Path
from typing import Dict, Optional

class GitService:
    """
    Handles all interactions with the Git repository.
    """
    def __init__(self, base_path: Path):
        self.repo: Optional[git.Repo] = self._find_git_repo(base_path)

    def _find_git_repo(self, path: Path) -> Optional[git.Repo]:
        """
        Finds a Git repository in the given path or its parents.
        """
        try:
            return git.Repo(path, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            return None

    def get_current_branch(self) -> str:
        """
        Gets the current active branch name.
        Returns 'DETACHED' if in a detached HEAD state.
        """
        if not self.repo:
            return "Not a Git repository"
        try:
            return self.repo.active_branch.name
        except TypeError:
            return "DETACHED"

    def get_file_statuses(self) -> Dict[str, str]:
        """
        Gets the status of all files in the repository.
        Returns a dictionary mapping file paths to their status codes.
        'M' = Modified, 'A' = Added, 'D' = Deleted, '??' = Untracked.
        """
        if not self.repo:
            return {}

        repo_dir = Path(self.repo.working_dir)
        statuses = {}

        # Modified files
        modified_files = {item.a_path for item in self.repo.index.diff(None)}
        for path in modified_files:
            statuses[str(repo_dir / path)] = "M"

        # Untracked files
        for path in self.repo.untracked_files:
            statuses[str(repo_dir / path)] = "??"
        
        # TODO: Add logic for staged files ('A'), etc. if needed.
        
        return statuses