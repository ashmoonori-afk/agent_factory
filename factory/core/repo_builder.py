"""Writes a filename→content dict to disk as a directory tree."""

from __future__ import annotations

from pathlib import Path


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
            created.append(str(dest.resolve()))

        return sorted(created)
