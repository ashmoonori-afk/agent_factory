"""Unit tests for RepoBuilder."""

from __future__ import annotations

from pathlib import Path

from factory.core.repo_builder import RepoBuilder


def test_build_creates_files(tmp_path: Path) -> None:
    files = {
        "README.md": "# Hello",
        "src/main.py": "print('hi')",
    }
    builder = RepoBuilder()
    created = builder.build(files, tmp_path / "out")

    assert (tmp_path / "out" / "README.md").read_text() == "# Hello"
    assert (tmp_path / "out" / "src" / "main.py").read_text() == "print('hi')"
    assert len(created) == 2


def test_build_returns_absolute_paths(tmp_path: Path) -> None:
    builder = RepoBuilder()
    created = builder.build({"a.txt": "content"}, tmp_path / "out")
    assert all(Path(p).is_absolute() for p in created)


def test_build_creates_nested_dirs(tmp_path: Path) -> None:
    files = {"a/b/c/deep.txt": "deep"}
    builder = RepoBuilder()
    builder.build(files, tmp_path / "out")
    assert (tmp_path / "out" / "a" / "b" / "c" / "deep.txt").exists()


def test_build_creates_output_dir_if_missing(tmp_path: Path) -> None:
    out = tmp_path / "brand" / "new" / "dir"
    RepoBuilder().build({"f.txt": "x"}, out)
    assert out.is_dir()


def test_build_overwrites_existing_file(tmp_path: Path) -> None:
    out = tmp_path / "out"
    RepoBuilder().build({"f.txt": "first"}, out)
    RepoBuilder().build({"f.txt": "second"}, out)
    assert (out / "f.txt").read_text() == "second"


def test_build_empty_files_dict_returns_empty_list(tmp_path: Path) -> None:
    result = RepoBuilder().build({}, tmp_path / "out")
    assert result == []


def test_build_preserves_utf8_content(tmp_path: Path) -> None:
    content = "안녕하세요 — héllo — 日本語"
    RepoBuilder().build({"unicode.txt": content}, tmp_path / "out")
    assert (tmp_path / "out" / "unicode.txt").read_text(encoding="utf-8") == content
