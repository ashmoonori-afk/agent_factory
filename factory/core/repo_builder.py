"""Writes a filename→content dict to disk as a directory tree."""

from __future__ import annotations

import os
import stat
from pathlib import Path

# File extensions that should be marked executable (launchers, shell scripts).
_EXECUTABLE_EXTENSIONS = {".command", ".sh"}


class RepoBuilder:
    """Creates a directory tree from a mapping of relative paths to file content.

    Usage::

        builder = RepoBuilder()
        paths = builder.build({"README.md": "# Hi", "src/main.py": "..."}, Path("./out"))
    """

    def build(self, files: dict[str, str], output_dir: Path) -> list[str]:
        """Write every entry in *files* to *output_dir* and return created paths.

        Args:
            files: Mapping of relative file path (forward-slash separated) to
                   UTF-8 text content.
            output_dir: Destination directory. Created (including parents) if it
                        does not exist.

        Returns:
            Sorted list of absolute path strings for every file written.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        created: list[str] = []

        for rel_path, content in files.items():
            dest = output_dir / Path(rel_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            # Set executable permission for launcher/shell scripts.
            if dest.suffix in _EXECUTABLE_EXTENSIONS:
                dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            created.append(str(dest.resolve()))

        return sorted(created)
