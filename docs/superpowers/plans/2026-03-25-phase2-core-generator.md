# Phase 2: Core Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `factory.generate()` function that orchestrates Jinja2 template rendering, directory/file creation, ZIP packaging, approval verification, and meta-data emission into a single callable public API.

**Architecture:** Four modules in `factory/core/` form a pipeline: `renderer.py` turns Jinja2 templates into a filename→content dict, `repo_builder.py` writes that dict to disk, `packager.py` zips the resulting directory, and `generator.py` ties them together with spec validation, approval gating, and result reporting. The public `factory/__init__.py` re-exports only the symbols callers need. Templates do not exist yet (Phase 3); the renderer is written to handle a missing or empty template directory gracefully so tests can inject synthetic templates.

**Tech Stack:** Python 3.10+, Jinja2 3.x, zipfile (stdlib), pathlib (stdlib), json (stdlib), yaml (pyyaml), existing `factory.schemas.validator` and `factory.approval.records` from Phase 1.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `factory/core/renderer.py` | Jinja2 template loader + renderer |
| Create | `factory/core/repo_builder.py` | Write filename→content dict to disk |
| Create | `factory/core/packager.py` | Zip an output directory |
| Create | `factory/core/generator.py` | Orchestrator: validate → approve → render → build → zip → return |
| Modify | `factory/__init__.py` | Re-export public API symbols |
| Create | `tests/unit/test_renderer.py` | Unit tests for TemplateRenderer |
| Create | `tests/unit/test_generator.py` | Unit tests for generate() orchestrator |

---

## Task 1: Renderer

**Files:**
- Create: `factory/core/renderer.py`
- Test: `tests/unit/test_renderer.py`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/test_renderer.py`:

```python
"""Unit tests for TemplateRenderer."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from factory.core.renderer import TemplateRenderer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_template_dir(tmp_path: Path, templates: dict[str, str]) -> Path:
    """Write a synthetic template set under tmp_path and return the dir."""
    tset_dir = tmp_path / "templates" / "single_agent"
    tset_dir.mkdir(parents=True)
    for rel, content in templates.items():
        dest = tset_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    return tmp_path / "templates"


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_renderer_accepts_none_template_dir() -> None:
    """TemplateRenderer can be constructed without a template directory."""
    r = TemplateRenderer(template_dir=None)
    assert r is not None


def test_renderer_accepts_path_template_dir(tmp_path: Path) -> None:
    tdir = tmp_path / "templates"
    tdir.mkdir()
    r = TemplateRenderer(template_dir=tdir)
    assert r is not None


# ---------------------------------------------------------------------------
# render_template
# ---------------------------------------------------------------------------

def test_render_template_basic_substitution(tmp_path: Path) -> None:
    tdir = _make_template_dir(tmp_path, {"CLAUDE.md.j2": "Agent: {{ name }}"})
    r = TemplateRenderer(template_dir=tdir)
    result = r.render_template("single_agent/CLAUDE.md.j2", {"name": "my-bot"})
    assert result == "Agent: my-bot"


def test_render_template_multiline(tmp_path: Path) -> None:
    template_content = textwrap.dedent("""\
        # {{ name }}
        Type: {{ type }}
        """)
    tdir = _make_template_dir(tmp_path, {"README.md.j2": template_content})
    r = TemplateRenderer(template_dir=tdir)
    output = r.render_template("single_agent/README.md.j2", {"name": "bot", "type": "single"})
    assert "# bot" in output
    assert "Type: single" in output


def test_render_template_missing_raises(tmp_path: Path) -> None:
    tdir = tmp_path / "templates"
    tdir.mkdir()
    r = TemplateRenderer(template_dir=tdir)
    with pytest.raises(Exception):
        r.render_template("single_agent/nonexistent.j2", {})


def test_render_template_undefined_variable_raises(tmp_path: Path) -> None:
    """Strict mode: referencing an undefined variable should raise."""
    tdir = _make_template_dir(tmp_path, {"t.j2": "Hello {{ undefined_var }}"})
    r = TemplateRenderer(template_dir=tdir)
    with pytest.raises(Exception):
        r.render_template("single_agent/t.j2", {})


# ---------------------------------------------------------------------------
# render_all
# ---------------------------------------------------------------------------

def test_render_all_returns_dict_of_paths_to_content(tmp_path: Path) -> None:
    templates = {
        "CLAUDE.md.j2": "# {{ name }}",
        "README.md.j2": "desc: {{ description }}",
        "src/main.py.j2": "# {{ name }} main",
    }
    tdir = _make_template_dir(tmp_path, templates)
    r = TemplateRenderer(template_dir=tdir)
    context = {"name": "bot", "description": "a bot"}
    result = r.render_all("single_agent", context)

    assert "CLAUDE.md" in result
    assert "README.md" in result
    assert "src/main.py" in result
    assert result["CLAUDE.md"] == "# bot"
    assert result["README.md"] == "desc: a bot"


def test_render_all_strips_j2_extension(tmp_path: Path) -> None:
    tdir = _make_template_dir(tmp_path, {"pyproject.toml.j2": "[project]\nname = \"{{ name }}\""})
    r = TemplateRenderer(template_dir=tdir)
    result = r.render_all("single_agent", {"name": "bot"})
    assert "pyproject.toml" in result
    assert ".j2" not in list(result.keys())[0]


def test_render_all_empty_template_set_returns_empty_dict(tmp_path: Path) -> None:
    tdir = tmp_path / "templates"
    (tdir / "single_agent").mkdir(parents=True)
    r = TemplateRenderer(template_dir=tdir)
    result = r.render_all("single_agent", {})
    assert result == {}


def test_render_all_missing_template_set_returns_empty_dict(tmp_path: Path) -> None:
    tdir = tmp_path / "templates"
    tdir.mkdir()
    r = TemplateRenderer(template_dir=tdir)
    result = r.render_all("nonexistent_set", {})
    assert result == {}


def test_render_all_preserves_nested_directory_structure(tmp_path: Path) -> None:
    templates = {
        "a/b/c/deep.txt.j2": "deep {{ val }}",
    }
    tdir = _make_template_dir(tmp_path, templates)
    r = TemplateRenderer(template_dir=tdir)
    result = r.render_all("single_agent", {"val": "x"})
    assert "a/b/c/deep.txt" in result
    assert result["a/b/c/deep.txt"] == "deep x"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_renderer.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'factory.core.renderer'`

- [ ] **Step 3: Write minimal implementation**

Create `factory/core/renderer.py`:

```python
"""Jinja2 template renderer for Agent Factory."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateRenderer:
    """Loads Jinja2 templates from a directory and renders them with a context dict.

    Args:
        template_dir: Root directory containing template sets (e.g. ``templates/``).
                      If ``None``, the default ``templates/`` directory adjacent to the
                      ``factory`` package is used. Pass an explicit path in tests.
    """

    def __init__(self, template_dir: Path | None = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).resolve().parent.parent.parent / "templates"
        self._template_dir = template_dir

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render_template(self, template_path: str, context: dict[str, object]) -> str:
        """Render a single template file and return the result as a string.

        Args:
            template_path: Path relative to *template_dir*, e.g.
                           ``"single_agent/CLAUDE.md.j2"``.
            context: Variables available inside the template.

        Returns:
            Rendered string content.

        Raises:
            jinja2.TemplateNotFound: If *template_path* does not exist.
            jinja2.UndefinedError: If the template references an undefined variable.
        """
        env = self._make_env(self._template_dir)
        template = env.get_template(template_path)
        return template.render(**context)

    def render_all(self, template_set: str, context: dict[str, object]) -> dict[str, str]:
        """Render every template inside a named template set directory.

        Args:
            template_set: Sub-directory name inside *template_dir*,
                          e.g. ``"single_agent"`` or ``"multi_agent"``.
            context: Variables available inside all templates.

        Returns:
            Dict mapping rendered output paths (relative, ``.j2`` suffix stripped)
            to rendered content strings.  Returns an empty dict if the template
            set directory does not exist or contains no templates.
        """
        set_dir = self._template_dir / template_set
        if not set_dir.is_dir():
            return {}

        env = self._make_env(self._template_dir)
        result: dict[str, str] = {}

        for template_file in sorted(set_dir.rglob("*")):
            if not template_file.is_file():
                continue

            # Build the path relative to template_dir so Jinja can load it.
            rel_from_root = template_file.relative_to(self._template_dir)
            # Build the output path relative to set_dir (no leading set name).
            rel_from_set = template_file.relative_to(set_dir)
            output_key = str(rel_from_set)

            # Strip .j2 suffix from output filename.
            if output_key.endswith(".j2"):
                output_key = output_key[:-3]

            template = env.get_template(str(rel_from_root))
            result[output_key] = template.render(**context)

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _make_env(template_dir: Path) -> Environment:
        """Return a Jinja2 Environment configured with StrictUndefined."""
        return Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
            autoescape=False,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_renderer.py -v`
Expected: All 11 tests PASS

- [ ] **Step 5: Run linters**

Run:
```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
ruff check factory/core/renderer.py
mypy factory/core/renderer.py --strict
```
Expected: No errors

- [ ] **Step 6: Commit**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/core/renderer.py tests/unit/test_renderer.py
git commit -m "feat: implement TemplateRenderer with Jinja2 StrictUndefined"
```

---

## Task 2: Repo Builder

**Files:**
- Create: `factory/core/repo_builder.py`
- Test: (inline in `tests/unit/test_generator.py` — covered in Task 4; a focused smoke test is added here for fast feedback)

- [ ] **Step 1: Write the failing test**

Add `tests/unit/test_repo_builder.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_repo_builder.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'factory.core.repo_builder'`

- [ ] **Step 3: Write minimal implementation**

Create `factory/core/repo_builder.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_repo_builder.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Run linters**

Run:
```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
ruff check factory/core/repo_builder.py
mypy factory/core/repo_builder.py --strict
```
Expected: No errors

- [ ] **Step 6: Commit**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/core/repo_builder.py tests/unit/test_repo_builder.py
git commit -m "feat: implement RepoBuilder — write file dict to directory tree"
```

---

## Task 3: Packager

**Files:**
- Create: `factory/core/packager.py`
- Test: (inline smoke tests added here)

- [ ] **Step 1: Write the failing test**

Add `tests/unit/test_packager.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_packager.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'factory.core.packager'`

- [ ] **Step 3: Write minimal implementation**

Create `factory/core/packager.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_packager.py -v`
Expected: All 8 tests PASS

- [ ] **Step 5: Run linters**

Run:
```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
ruff check factory/core/packager.py
mypy factory/core/packager.py --strict
```
Expected: No errors

- [ ] **Step 6: Commit**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/core/packager.py tests/unit/test_packager.py
git commit -m "feat: implement create_zip packager using stdlib zipfile"
```

---

## Task 4: Generator (Orchestrator)

**Files:**
- Create: `factory/core/generator.py`
- Test: `tests/unit/test_generator.py`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/test_generator.py`:

```python
"""Unit tests for the generate() orchestrator."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from factory.core.generator import (
    ApprovalRequiredError,
    GenerationError,
    GenerationResult,
    SpecValidationError,
    generate,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

VALID_SPEC: dict[str, object] = {
    "name": "test-bot",
    "description": "A test agent for unit tests",
    "type": "single",
}

VALID_APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "test-bot single-agent",
}


def _run(tmp_path: Path, **overrides: object) -> GenerationResult:
    """Call generate() with sensible defaults; overrides replace individual kwargs."""
    kwargs: dict[str, object] = {
        "spec": VALID_SPEC,
        "output": str(tmp_path / "test-bot"),
        "approval_record": VALID_APPROVAL,
    }
    kwargs.update(overrides)
    return generate(**kwargs)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# GenerationResult dataclass
# ---------------------------------------------------------------------------

def test_generation_result_fields() -> None:
    r = GenerationResult(
        output_path="/tmp/x",
        zip_path="/tmp/x.zip",
        file_count=3,
        files=["/tmp/x/a", "/tmp/x/b", "/tmp/x/c"],
    )
    assert r.output_path == "/tmp/x"
    assert r.zip_path == "/tmp/x.zip"
    assert r.file_count == 3
    assert len(r.files) == 3


# ---------------------------------------------------------------------------
# SpecValidationError
# ---------------------------------------------------------------------------

def test_invalid_spec_raises_spec_validation_error(tmp_path: Path) -> None:
    bad_spec: dict[str, object] = {"name": "My Bot!"}  # missing description, type; bad name
    with pytest.raises(SpecValidationError):
        _run(tmp_path, spec=bad_spec)


def test_spec_validation_error_is_exception() -> None:
    assert issubclass(SpecValidationError, Exception)


# ---------------------------------------------------------------------------
# ApprovalRequiredError
# ---------------------------------------------------------------------------

def test_missing_approval_raises_approval_required_error(tmp_path: Path) -> None:
    bad_approval = {**VALID_APPROVAL, "decision": "REJECTED"}
    with pytest.raises(ApprovalRequiredError):
        _run(tmp_path, approval_record=bad_approval)


def test_empty_approval_dict_raises_approval_required_error(tmp_path: Path) -> None:
    with pytest.raises((ApprovalRequiredError, KeyError)):
        _run(tmp_path, approval_record={})


def test_approval_required_error_is_exception() -> None:
    assert issubclass(ApprovalRequiredError, Exception)


# ---------------------------------------------------------------------------
# Successful generation
# ---------------------------------------------------------------------------

def test_generate_returns_generation_result(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert isinstance(result, GenerationResult)


def test_generate_creates_output_directory(tmp_path: Path) -> None:
    out = tmp_path / "test-bot"
    _run(tmp_path, output=str(out))
    assert out.is_dir()


def test_generate_result_output_path_exists(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert Path(result.output_path).is_dir()


def test_generate_writes_meta_yaml(tmp_path: Path) -> None:
    result = _run(tmp_path)
    meta = Path(result.output_path) / "meta.yaml"
    assert meta.exists()


def test_generate_meta_yaml_contains_name(tmp_path: Path) -> None:
    import yaml

    result = _run(tmp_path)
    meta = Path(result.output_path) / "meta.yaml"
    data = yaml.safe_load(meta.read_text())
    assert data["name"] == "test-bot"


def test_generate_writes_approval_log(tmp_path: Path) -> None:
    result = _run(tmp_path)
    log = Path(result.output_path) / "approval_log.jsonl"
    assert log.exists()


def test_generate_approval_log_is_valid_jsonl(tmp_path: Path) -> None:
    result = _run(tmp_path)
    log = Path(result.output_path) / "approval_log.jsonl"
    for line in log.read_text().splitlines():
        parsed = json.loads(line)
        assert "decision" in parsed
        assert "hash" in parsed


def test_generate_file_count_matches_files_list(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.file_count == len(result.files)


# ---------------------------------------------------------------------------
# ZIP behaviour
# ---------------------------------------------------------------------------

def test_generate_creates_zip_by_default(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.zip_path is not None
    assert Path(result.zip_path).exists()


def test_generate_no_zip_flag_skips_zip(tmp_path: Path) -> None:
    result = _run(tmp_path, no_zip=True)
    assert result.zip_path is None


def test_generate_zip_is_valid_archive(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.zip_path is not None
    assert zipfile.is_zipfile(result.zip_path)


def test_generate_zip_contains_meta_yaml(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.zip_path is not None
    with zipfile.ZipFile(result.zip_path) as zf:
        names = zf.namelist()
    assert "meta.yaml" in names


# ---------------------------------------------------------------------------
# Template set selection
# ---------------------------------------------------------------------------

def test_generate_single_agent_uses_single_agent_template_set(tmp_path: Path) -> None:
    """No error when type=single (template dir may be empty in test env)."""
    result = _run(tmp_path, spec={**VALID_SPEC, "type": "single"})
    assert isinstance(result, GenerationResult)


def test_generate_multi_agent_uses_multi_agent_template_set(tmp_path: Path) -> None:
    """No error when type=multi (template dir may be empty in test env)."""
    multi_spec: dict[str, object] = {
        "name": "team-bot",
        "description": "A multi-agent team",
        "type": "multi",
    }
    result = _run(tmp_path, spec=multi_spec)
    assert isinstance(result, GenerationResult)


# ---------------------------------------------------------------------------
# GenerationError
# ---------------------------------------------------------------------------

def test_generation_error_is_exception() -> None:
    assert issubclass(GenerationError, Exception)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_generator.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'factory.core.generator'`

- [ ] **Step 3: Write minimal implementation**

Create `factory/core/generator.py`:

```python
"""Orchestrator: validate → approve → render → build → zip → return result."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from factory.approval.records import ApprovalRecord
from factory.core.packager import create_zip
from factory.core.renderer import TemplateRenderer
from factory.core.repo_builder import RepoBuilder
from factory.schemas.validator import validate_spec


# ---------------------------------------------------------------------------
# Public exceptions
# ---------------------------------------------------------------------------


class SpecValidationError(Exception):
    """Raised when the agent spec fails schema validation."""


class ApprovalRequiredError(Exception):
    """Raised when the approval record is missing, invalid, or not APPROVED."""


class GenerationError(Exception):
    """Raised for unexpected errors during generation."""


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class GenerationResult:
    """Returned by :func:`generate` describing what was created.

    Attributes:
        output_path: Absolute path to the generated directory.
        zip_path: Absolute path to the ZIP archive, or ``None`` if ``no_zip=True``.
        file_count: Number of files written (excludes the ZIP itself).
        files: Sorted list of absolute file paths written to *output_path*.
    """

    output_path: str
    zip_path: str | None
    file_count: int
    files: list[str]


# ---------------------------------------------------------------------------
# Registry stubs (Phase 4 will replace these)
# ---------------------------------------------------------------------------


def _resolve_skills(skill_ids: list[str]) -> list[dict[str, str]]:
    """Stub: return skill ids as minimal dicts until Phase 4 registry is ready."""
    return [{"id": sid} for sid in skill_ids]


def _resolve_persona(persona: dict[str, object]) -> dict[str, object]:
    """Stub: pass persona through unchanged until Phase 4 registry is ready."""
    return persona


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


def generate(
    spec: dict[str, object],
    output: str,
    approval_record: dict[str, str],
    *,
    no_zip: bool = False,
) -> GenerationResult:
    """Generate a complete agent repository from a validated spec.

    Steps (in order):

    1. Validate *spec* against the agent_spec schema.
    2. Construct and validate the :class:`~factory.approval.records.ApprovalRecord`.
    3. Resolve skills and persona from the registry (stub in Phase 2).
    4. Select the Jinja2 template set based on ``spec["type"]``.
    5. Render all templates into a filename→content dict.
    6. Write every file to *output* directory.
    7. Write ``meta.yaml`` into *output*.
    8. Append one JSON line to ``approval_log.jsonl``.
    9. Create a ZIP archive of *output* (unless *no_zip* is ``True``).
    10. Return a :class:`GenerationResult`.

    Args:
        spec: Agent specification dict (must satisfy ``agent_spec`` JSON Schema).
        output: Destination directory path (created if absent).
        approval_record: Approval dict with keys ``decision``, ``timestamp``,
                         ``user_input``, ``action_type``, ``detail``.
        no_zip: If ``True``, skip ZIP creation.

    Returns:
        :class:`GenerationResult` describing generated artefacts.

    Raises:
        SpecValidationError: If *spec* fails schema validation.
        ApprovalRequiredError: If *approval_record* is invalid or not APPROVED.
        GenerationError: For unexpected errors during file creation.
    """
    # ------------------------------------------------------------------
    # Step 1 — Validate spec
    # ------------------------------------------------------------------
    errors = validate_spec(spec)
    if errors:
        raise SpecValidationError(
            f"Spec validation failed with {len(errors)} error(s):\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    # ------------------------------------------------------------------
    # Step 2 — Verify approval record
    # ------------------------------------------------------------------
    try:
        record = ApprovalRecord.from_dict(approval_record)
    except (KeyError, TypeError) as exc:
        raise ApprovalRequiredError(
            f"approval_record is missing required fields: {exc}"
        ) from exc

    approval_errors = record.validate()
    if approval_errors:
        raise ApprovalRequiredError(
            "approval_record is not valid:\n"
            + "\n".join(f"  - {e}" for e in approval_errors)
        )

    # ------------------------------------------------------------------
    # Step 3 — Compute approval hash + resolve registry stubs
    # ------------------------------------------------------------------
    approval_hash = ApprovalRecord.compute_hash(
        record.action_type, record.detail, record.timestamp
    )

    skill_ids: list[str] = [str(s) for s in (spec.get("skills") or [])]  # type: ignore[union-attr]
    _resolve_skills(skill_ids)

    persona_raw: dict[str, object] = spec.get("persona") or {}  # type: ignore[assignment]
    _resolve_persona(persona_raw)

    # ------------------------------------------------------------------
    # Step 4 — Select template set
    # ------------------------------------------------------------------
    agent_type = str(spec.get("type", "single"))
    template_set = "single_agent" if agent_type == "single" else "multi_agent"

    # ------------------------------------------------------------------
    # Step 5 — Render templates
    # ------------------------------------------------------------------
    renderer = TemplateRenderer()
    context: dict[str, object] = {
        "spec": spec,
        "name": spec.get("name", ""),
        "description": spec.get("description", ""),
        "type": agent_type,
        "skills": skill_ids,
        "persona": persona_raw,
        "approval_hash": approval_hash,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    rendered_files = renderer.render_all(template_set, context)

    # ------------------------------------------------------------------
    # Step 6 — Write files to output directory
    # ------------------------------------------------------------------
    output_dir = Path(output)
    try:
        builder = RepoBuilder()
        written = builder.build(rendered_files, output_dir)
    except OSError as exc:
        raise GenerationError(f"Failed to write files to {output_dir}: {exc}") from exc

    # ------------------------------------------------------------------
    # Step 7 — Write meta.yaml
    # ------------------------------------------------------------------
    meta: dict[str, object] = {
        "name": spec.get("name"),
        "description": spec.get("description"),
        "type": agent_type,
        "generated_at": context["generated_at"],
        "approval_hash": approval_hash,
        "factory_version": "1.0.0",
    }
    meta_path = output_dir / "meta.yaml"
    meta_path.write_text(yaml.dump(meta, default_flow_style=False), encoding="utf-8")
    written.append(str(meta_path.resolve()))

    # ------------------------------------------------------------------
    # Step 8 — Append to approval_log.jsonl
    # ------------------------------------------------------------------
    log_entry: dict[str, str] = {
        **record.to_dict(),
        "generated_at": str(context["generated_at"]),
    }
    log_path = output_dir / "approval_log.jsonl"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(log_entry) + "\n")
    written.append(str(log_path.resolve()))

    written_sorted = sorted(set(written))

    # ------------------------------------------------------------------
    # Step 9 — Create ZIP
    # ------------------------------------------------------------------
    zip_result: str | None = None
    if not no_zip:
        zip_path = create_zip(output_dir)
        zip_result = str(zip_path)

    # ------------------------------------------------------------------
    # Step 10 — Return result
    # ------------------------------------------------------------------
    return GenerationResult(
        output_path=str(output_dir.resolve()),
        zip_path=zip_result,
        file_count=len(written_sorted),
        files=written_sorted,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_generator.py -v`
Expected: All 23 tests PASS

- [ ] **Step 5: Run linters**

Run:
```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
ruff check factory/core/generator.py
mypy factory/core/generator.py --strict
```
Expected: No errors

- [ ] **Step 6: Commit**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/core/generator.py tests/unit/test_generator.py
git commit -m "feat: implement generate() orchestrator with approval gate and ZIP output"
```

---

## Task 5: Public API + Full Verification

**Files:**
- Modify: `factory/__init__.py`
- Test: (re-run full suite)

- [ ] **Step 1: Write the failing test for the public API surface**

Add the following block to the bottom of `tests/unit/test_generator.py` (or in a new file `tests/unit/test_public_api.py` — either works):

```python
# tests/unit/test_public_api.py
"""Smoke-tests that the public factory namespace exports are correct."""

from __future__ import annotations


def test_generate_importable_from_factory() -> None:
    from factory import generate  # noqa: F401


def test_validate_importable_from_factory() -> None:
    from factory import validate  # noqa: F401


def test_generation_result_importable_from_factory() -> None:
    from factory import GenerationResult  # noqa: F401


def test_spec_validation_error_importable_from_factory() -> None:
    from factory import SpecValidationError  # noqa: F401


def test_approval_required_error_importable_from_factory() -> None:
    from factory import ApprovalRequiredError  # noqa: F401


def test_generation_error_importable_from_factory() -> None:
    from factory import GenerationError  # noqa: F401


def test_version_present() -> None:
    import factory

    assert factory.__version__ == "1.0.0"


def test_generate_is_callable() -> None:
    import factory

    assert callable(factory.generate)


def test_validate_is_callable() -> None:
    import factory

    assert callable(factory.validate)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_public_api.py -v`
Expected: FAIL — `ImportError: cannot import name 'generate' from 'factory'`

- [ ] **Step 3: Wire the public API**

Replace the contents of `factory/__init__.py`:

```python
"""Agent Factory — Generate AI agent repositories through conversation."""

from __future__ import annotations

from factory.core.generator import ApprovalRequiredError as ApprovalRequiredError
from factory.core.generator import GenerationError as GenerationError
from factory.core.generator import GenerationResult as GenerationResult
from factory.core.generator import SpecValidationError as SpecValidationError
from factory.core.generator import generate as generate
from factory.schemas.validator import validate_spec as validate

__version__ = "1.0.0"

__all__ = [
    "generate",
    "validate",
    "GenerationResult",
    "SpecValidationError",
    "ApprovalRequiredError",
    "GenerationError",
    "__version__",
]
```

- [ ] **Step 4: Run public API tests to verify they pass**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_public_api.py -v`
Expected: All 9 tests PASS

- [ ] **Step 5: Run the full test suite**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/ -v --tb=short`
Expected: All tests PASS (Phase 1 tests 23 + renderer 11 + repo_builder 7 + packager 8 + generator 23 + public API 9 = 81 total)

- [ ] **Step 6: Run ruff on the entire codebase**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && ruff check factory/ tests/`
Expected: No errors

- [ ] **Step 7: Run mypy on the entire factory package**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && mypy factory/ --strict`
Expected: No errors

- [ ] **Step 8: Smoke-test the public API end-to-end from the CLI**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
python3 - <<'EOF'
import factory, json, tempfile, pathlib

spec = {
    "name": "smoke-bot",
    "description": "Smoke test agent",
    "type": "single",
}
approval = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "smoke-bot single-agent",
}
with tempfile.TemporaryDirectory() as td:
    result = factory.generate(
        spec=spec,
        output=str(pathlib.Path(td) / "smoke-bot"),
        approval_record=approval,
    )
    print(f"output_path : {result.output_path}")
    print(f"zip_path    : {result.zip_path}")
    print(f"file_count  : {result.file_count}")
    print("PASS")
EOF
```
Expected: Prints `output_path`, `zip_path`, `file_count`, and `PASS`.

- [ ] **Step 9: Commit**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/__init__.py tests/unit/test_public_api.py
git commit -m "feat: wire public API in factory/__init__.py — Phase 2 complete"
```

---

## Phase 2 Acceptance Criteria

- [ ] `factory.generate(spec, output, approval_record)` creates a complete output directory
- [ ] `meta.yaml` is written inside the output directory with `name`, `type`, `generated_at`, `approval_hash`
- [ ] `approval_log.jsonl` is written with one valid JSON line per call, including `hash`
- [ ] ZIP archive is created by default; omitted when `no_zip=True`
- [ ] `ApprovalRequiredError` is raised when `decision != "APPROVED"` or fields are missing
- [ ] `SpecValidationError` is raised when the spec fails schema validation
- [ ] All rendered template variables substitute correctly (verified with synthetic test templates)
- [ ] `factory.validate(spec)` is importable and callable from the public namespace
- [ ] All 81 tests pass
- [ ] `ruff check` zero errors
- [ ] `mypy --strict` zero errors

---

## Subsequent Plans

| Plan | Depends On | Description |
|------|-----------|-------------|
| Phase 3: Templates | Phase 2 | All Jinja2 `.j2` templates for `single_agent/` and `multi_agent/` sets |
| Phase 4: Registry | Phase 1 | Built-in skills (`.md`), personas (`.yaml`), registry loader replacing stubs in `generator.py` |
| Phase 5: Workflow Files | Phases 2–4 | `CLAUDE.md` and `CODEX.md` for Agent Factory itself |
| Phase 6: Polish + Release | All | Integration tests, examples, documentation, PyPI prep |
