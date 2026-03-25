"""Unit tests for create_zip."""

from __future__ import annotations

import zipfile
from pathlib import Path

from factory.core.packager import create_zip


def _populate(base: Path) -> None:
    """Write a few files into base for zipping."""
    (base / "README.md").write_text("# hi")
    (base / "src").mkdir()
    (base / "src" / "main.py").write_text("print('hi')")
    (base / "a" / "b").mkdir(parents=True)
    (base / "a" / "b" / "deep.txt").write_text("deep")


def test_create_zip_produces_file(tmp_path: Path) -> None:
    src = tmp_path / "agent"
    src.mkdir()
    _populate(src)
    zip_path = create_zip(src)
    assert zip_path.exists()
    assert zip_path.suffix == ".zip"


def test_create_zip_default_path_is_sibling(tmp_path: Path) -> None:
    src = tmp_path / "my-bot"
    src.mkdir()
    _populate(src)
    zip_path = create_zip(src)
    assert zip_path == tmp_path / "my-bot.zip"


def test_create_zip_explicit_path(tmp_path: Path) -> None:
    src = tmp_path / "agent"
    src.mkdir()
    _populate(src)
    explicit = tmp_path / "custom_name.zip"
    result = create_zip(src, explicit)
    assert result == explicit
    assert explicit.exists()


def test_create_zip_is_valid_zip(tmp_path: Path) -> None:
    src = tmp_path / "agent"
    src.mkdir()
    _populate(src)
    zip_path = create_zip(src)
    assert zipfile.is_zipfile(zip_path)


def test_create_zip_contains_all_files(tmp_path: Path) -> None:
    src = tmp_path / "agent"
    src.mkdir()
    _populate(src)
    zip_path = create_zip(src)
    with zipfile.ZipFile(zip_path) as zf:
        names = {n.replace("\\", "/") for n in zf.namelist()}
    assert "README.md" in names
    assert "src/main.py" in names
    assert "a/b/deep.txt" in names


def test_create_zip_paths_are_relative_not_absolute(tmp_path: Path) -> None:
    src = tmp_path / "agent"
    src.mkdir()
    _populate(src)
    zip_path = create_zip(src)
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            assert not name.startswith("/"), f"Absolute path in ZIP: {name}"


def test_create_zip_overwrites_existing(tmp_path: Path) -> None:
    src = tmp_path / "agent"
    src.mkdir()
    (src / "f.txt").write_text("v1")
    zip_path = create_zip(src)
    (src / "f.txt").write_text("v2")
    zip_path2 = create_zip(src, zip_path)
    assert zip_path2 == zip_path


def test_create_zip_empty_dir_produces_valid_zip(tmp_path: Path) -> None:
    src = tmp_path / "empty"
    src.mkdir()
    zip_path = create_zip(src)
    assert zipfile.is_zipfile(zip_path)
