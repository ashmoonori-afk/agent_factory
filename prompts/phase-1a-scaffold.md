# Phase 1A: Project Scaffold + Package Structure + Schemas

> **Depends on**: Nothing (first step)
> **Read first**: `00-overview.md`

## Objective

Set up the project: pyproject.toml, package structure, YAML schemas, auxiliary CLI skeleton.

---

## Task 1: pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "agent-factory"
version = "1.0.0"
description = "Generate AI agent repositories through LLM-guided interviews"
requires-python = ">=3.10"
license = "MIT"
dependencies = [
    "click>=8.0",
    "jinja2>=3.0",
    "pyyaml>=6.0",
    "jsonschema>=4.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff>=0.4", "mypy>=1.0", "types-PyYAML", "types-jsonschema"]

[project.scripts]
factory = "factory.cli.main:cli"

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.mypy]
python_version = "3.10"
strict = true
```

Also create `.python-version` (3.10) and `.gitignore`.

## Task 2: Package Structure

Create `__init__.py` in all subpackages:
- `factory/` (with `__version__ = "1.0.0"`)
- `factory/cli/`
- `factory/core/`
- `factory/schemas/`
- `factory/approval/`
- `factory/registries/`

Create `factory/__main__.py` for `python -m factory`.

## Task 3: YAML Schemas

Create 4 schema files under `schemas/`:
- `agent_spec.schema.yaml` — See tech spec Section 4
- `policy.schema.yaml`
- `persona.schema.yaml`
- `skill.schema.yaml`

Key: `agent_spec` requires `name`, `description`, `type`. The `runtime.primary` field replaces the old `model` block.

## Task 4: Auxiliary CLI Skeleton

Create `factory/cli/main.py` with click:
- `factory version` — print version
- `factory validate <file>` — placeholder
- `factory skills` — placeholder
- `factory personas` — placeholder

## Verification

```bash
pip install -e ".[dev]"
factory version
ruff check factory/
mypy factory/ --strict
```
