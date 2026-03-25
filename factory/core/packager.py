"""ZIP packager for generated agent repositories."""

from __future__ import annotations

import zipfile
from pathlib import Path


def create_zip(source_dir: Path, zip_path: Path | None = None) -> Path:
    """Create a ZIP archive of *source_dir*.

    Args:
        source_dir: Directory to compress.  Must exist.
        zip_path: Destination ``.zip`` file.  Defaults to
                  ``<source_dir.parent>/<source_dir.name>.zip``.

    Returns:
        Absolute path to the created ZIP file.

    Raises:
        FileNotFoundError: If *source_dir* does not exist.
        NotADirectoryError: If *source_dir* is not a directory.
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"source_dir does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"source_dir is not a directory: {source_dir}")

    if zip_path is None:
        zip_path = source_dir.parent / f"{source_dir.name}.zip"

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(source_dir.rglob("*")):
            if file.is_file():
                arcname = file.relative_to(source_dir)
                zf.write(file, arcname)

    return zip_path.resolve()
