# Phase 2A: Jinja2 Renderer + Repo Builder + Packager

> **Depends on**: phase-1b
> **Read first**: `00-overview.md`, `../technical_spec.md` Section 5

## Objective

Implement the three core generation components.

---

## Task 1: Jinja2 Renderer

Create `factory/core/renderer.py`:

```python
class TemplateRenderer:
    def __init__(self, template_dir: Path) -> None: ...

    def render_template(self, template_path: str, context: dict) -> str:
        """Render a single .j2 template with the given context."""

    def render_all(self, template_set: str, context: dict) -> dict[str, str]:
        """Render all templates in a set (e.g., 'single_agent').
        Returns {relative_path: rendered_content}."""
```

- Template sets: `single_agent/`, `multi_agent/`
- Shared templates: `docs/`, `policies/`, `tests/` (always included)
- Context dict follows tech spec Section 5.2

## Task 2: Repo Builder

Create `factory/core/repo_builder.py`:

```python
class RepoBuilder:
    def build(self, output_dir: str, files: dict[str, str]) -> list[str]:
        """Create directory tree and write all files.
        files: {relative_path: content}
        Returns list of created file paths."""
```

- Create directories with `os.makedirs(exist_ok=True)`
- Write files with UTF-8 encoding
- Return list of all created paths

## Task 3: ZIP Packager

Create `factory/core/packager.py`:

```python
class Packager:
    def create_zip(self, source_dir: str, zip_path: str) -> str:
        """Create ZIP of source_dir. Returns zip_path."""
```

## Task 4: Unit Tests

`tests/unit/test_renderer.py`:
- Renders a simple template with context
- Handles missing template gracefully
- render_all returns correct file paths

## Verification

```bash
pytest tests/unit/test_renderer.py -v
ruff check factory/
mypy factory/ --strict
```
