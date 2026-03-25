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
