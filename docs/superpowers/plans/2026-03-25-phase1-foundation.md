# Phase 1: Foundation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up the Agent Factory project scaffold with pyproject.toml, package structure, YAML schemas, schema validator, approval record model, and auxiliary CLI skeleton.

**Architecture:** Python 3.10+ library using hatchling build system. Four production dependencies (click, jinja2, pyyaml, jsonschema). Schema validation via jsonschema, approval hashing via SHA-256. Auxiliary CLI via click.

**Tech Stack:** Python 3.10+, hatchling, click, jinja2, pyyaml, jsonschema, pytest, ruff, mypy

---

## File Structure

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `pyproject.toml` | Build system, dependencies, CLI entry point |
| Create | `.python-version` | Pin Python 3.10 |
| Create | `.gitignore` | Standard Python ignores |
| Create | `factory/__init__.py` | Public API surface + version |
| Create | `factory/__main__.py` | `python -m factory` entry |
| Create | `factory/cli/__init__.py` | CLI package init |
| Create | `factory/cli/main.py` | Click CLI group: version, validate, skills, personas |
| Create | `factory/core/__init__.py` | Core package init |
| Create | `factory/schemas/__init__.py` | Schemas package init |
| Create | `factory/schemas/validator.py` | jsonschema wrapper: load_schema, validate_spec |
| Create | `factory/approval/__init__.py` | Approval package init |
| Create | `factory/approval/records.py` | ApprovalRecord dataclass + SHA-256 hash |
| Create | `factory/registries/__init__.py` | Registries package init |
| Create | `schemas/agent_spec.schema.yaml` | Agent spec JSON Schema in YAML |
| Create | `schemas/policy.schema.yaml` | Policy rules schema |
| Create | `schemas/persona.schema.yaml` | Persona definition schema |
| Create | `schemas/skill.schema.yaml` | Skill metadata schema |
| Create | `tests/__init__.py` | Tests package |
| Create | `tests/unit/__init__.py` | Unit tests package |
| Create | `tests/unit/test_validator.py` | Schema validator tests |
| Create | `tests/unit/test_approval.py` | Approval record tests |
| Create | `tests/unit/test_cli.py` | CLI smoke tests |

---

## Task 1: Project Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.gitignore`

- [ ] **Step 1: Create pyproject.toml**

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
dev = [
    "pytest>=7.0",
    "ruff>=0.4",
    "mypy>=1.0",
    "types-PyYAML",
    "types-jsonschema",
]

[project.scripts]
factory = "factory.cli.main:cli"

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Create .python-version**

```
3.10
```

- [ ] **Step 3: Create .gitignore**

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.mypy_cache/
.ruff_cache/
.pytest_cache/
.venv/
venv/
*.zip
.env
.DS_Store
```

- [ ] **Step 4: Commit**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git init
git add pyproject.toml .python-version .gitignore
git commit -m "chore: initialize project scaffold with pyproject.toml"
```

---

## Task 2: Package Structure

**Files:**
- Create: `factory/__init__.py`
- Create: `factory/__main__.py`
- Create: `factory/cli/__init__.py`
- Create: `factory/core/__init__.py`
- Create: `factory/schemas/__init__.py`
- Create: `factory/approval/__init__.py`
- Create: `factory/registries/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/unit/__init__.py`

- [ ] **Step 1: Create factory/__init__.py with version and future public API stubs**

```python
"""Agent Factory — Generate AI agent repositories through conversation."""

__version__ = "1.0.0"
```

- [ ] **Step 2: Create factory/__main__.py**

```python
"""Allow running as `python -m factory`."""

from factory.cli.main import cli

cli()
```

- [ ] **Step 3: Create all __init__.py files for subpackages**

Each file is empty initially:
- `factory/cli/__init__.py`
- `factory/core/__init__.py`
- `factory/schemas/__init__.py`
- `factory/approval/__init__.py`
- `factory/registries/__init__.py`
- `tests/__init__.py`
- `tests/unit/__init__.py`

- [ ] **Step 4: Install package in dev mode**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pip install -e ".[dev]"`
Expected: Successful install with all dev dependencies.

- [ ] **Step 5: Verify import works**

Run: `python -c "import factory; print(factory.__version__)"`
Expected: `1.0.0`

- [ ] **Step 6: Commit**

```bash
git add factory/ tests/
git commit -m "chore: create package structure with all subpackages"
```

---

## Task 3: YAML Schemas

**Files:**
- Create: `schemas/agent_spec.schema.yaml`
- Create: `schemas/policy.schema.yaml`
- Create: `schemas/persona.schema.yaml`
- Create: `schemas/skill.schema.yaml`

- [ ] **Step 1: Create schemas directory**

```bash
mkdir -p schemas
```

- [ ] **Step 2: Create agent_spec.schema.yaml**

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "Agent Spec"
description: "Schema for Agent Factory agent specification"
type: object
required:
  - name
  - description
  - type
properties:
  name:
    type: string
    pattern: "^[a-z0-9-]+$"
    description: "Agent name in kebab-case"
  description:
    type: string
    minLength: 1
    description: "1-2 sentence agent description"
  type:
    type: string
    enum: ["single", "multi"]
    description: "Agent type: single or multi-agent"
  runtime:
    type: object
    properties:
      primary:
        type: string
        enum: ["claude-code", "codex", "both"]
        default: "both"
    additionalProperties: false
  policies:
    type: object
    properties:
      deny:
        type: array
        items:
          type: string
      ask:
        type: array
        items:
          type: string
      allow:
        type: array
        items:
          type: string
    additionalProperties: false
  persona:
    type: object
    properties:
      tone:
        type: string
      language:
        type: string
      custom_instructions:
        type: string
    additionalProperties: false
  skills:
    type: array
    items:
      type: string
  context:
    type: string
  agents:
    type: array
    items:
      type: object
      required:
        - id
        - role
      properties:
        id:
          type: string
        role:
          type: string
        next:
          type: array
          items:
            type: string
      additionalProperties: false
    maxItems: 5
  topology:
    type: object
    properties:
      entry:
        type: string
      max_loops:
        type: integer
        minimum: 1
        default: 3
      exit_condition:
        type: string
    additionalProperties: false
additionalProperties: false
```

- [ ] **Step 3: Create policy.schema.yaml**

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "Policy"
description: "Schema for DENY/ASK/ALLOW policy rules"
type: object
required:
  - deny
properties:
  deny:
    type: array
    items:
      type: string
  ask:
    type: array
    items:
      type: string
  allow:
    type: array
    items:
      type: string
additionalProperties: false
```

- [ ] **Step 4: Create persona.schema.yaml**

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "Persona"
description: "Schema for agent persona definition"
type: object
required:
  - tone
properties:
  tone:
    type: string
  language:
    type: string
    default: "en"
  custom_instructions:
    type: string
additionalProperties: false
```

- [ ] **Step 5: Create skill.schema.yaml**

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "Skill"
description: "Schema for skill metadata"
type: object
required:
  - id
  - name
  - policy
properties:
  id:
    type: string
    pattern: "^[a-z0-9-]+$"
  name:
    type: string
  description:
    type: string
  policy:
    type: string
    enum: ["DENY", "ASK", "ALLOW"]
additionalProperties: false
```

- [ ] **Step 6: Commit**

```bash
git add schemas/
git commit -m "feat: add YAML schemas for agent spec, policy, persona, skill"
```

---

## Task 4: Schema Validator

**Files:**
- Create: `factory/schemas/validator.py`
- Test: `tests/unit/test_validator.py`

- [ ] **Step 1: Write the failing test for schema loading**

Create `tests/unit/test_validator.py`:

```python
from __future__ import annotations

from factory.schemas.validator import load_schema, validate_spec


def test_load_agent_spec_schema() -> None:
    schema = load_schema("agent_spec")
    assert schema["title"] == "Agent Spec"
    assert "properties" in schema


def test_validate_valid_minimal_spec() -> None:
    spec = {
        "name": "my-bot",
        "description": "A test bot",
        "type": "single",
    }
    errors = validate_spec(spec)
    assert errors == []


def test_validate_missing_required_field() -> None:
    spec = {
        "name": "my-bot",
        # missing description and type
    }
    errors = validate_spec(spec)
    assert len(errors) > 0
    assert any("description" in e or "type" in e for e in errors)


def test_validate_invalid_type_enum() -> None:
    spec = {
        "name": "my-bot",
        "description": "A test bot",
        "type": "invalid",
    }
    errors = validate_spec(spec)
    assert len(errors) > 0


def test_validate_invalid_name_pattern() -> None:
    spec = {
        "name": "My Bot!",
        "description": "A test bot",
        "type": "single",
    }
    errors = validate_spec(spec)
    assert len(errors) > 0


def test_validate_full_spec_with_optional_fields() -> None:
    spec = {
        "name": "data-analyzer",
        "description": "Analyze CSV and SQL data",
        "type": "single",
        "runtime": {"primary": "both"},
        "policies": {
            "deny": ["send_email", "delete_file"],
            "ask": ["sql_execute"],
            "allow": ["*"],
        },
        "persona": {"tone": "professional", "language": "en"},
        "skills": ["csv-reader", "sql-executor"],
        "context": "Used for financial data analysis",
    }
    errors = validate_spec(spec)
    assert errors == []


def test_validate_multi_agent_spec() -> None:
    spec = {
        "name": "team-bot",
        "description": "A multi-agent team",
        "type": "multi",
        "agents": [
            {"id": "planner", "role": "Plan tasks", "next": ["executor"]},
            {"id": "executor", "role": "Execute tasks", "next": ["reviewer"]},
            {"id": "reviewer", "role": "Review results", "next": ["planner"]},
        ],
        "topology": {
            "entry": "planner",
            "max_loops": 3,
            "exit_condition": "reviewer approves",
        },
    }
    errors = validate_spec(spec)
    assert errors == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_validator.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'factory.schemas.validator'` (or ImportError)

- [ ] **Step 3: Implement the schema validator**

Create `factory/schemas/validator.py`:

```python
"""Schema validation using jsonschema."""

from __future__ import annotations

from pathlib import Path

import jsonschema
import yaml


_SCHEMA_DIR = Path(__file__).resolve().parent.parent.parent / "schemas"


def load_schema(name: str) -> dict:  # type: ignore[type-arg]
    """Load a YAML schema file by name (without extension).

    Args:
        name: Schema name, e.g. "agent_spec" loads "agent_spec.schema.yaml"

    Returns:
        Parsed schema dict.

    Raises:
        FileNotFoundError: If schema file doesn't exist.
    """
    path = _SCHEMA_DIR / f"{name}.schema.yaml"
    with open(path) as f:
        schema: dict = yaml.safe_load(f)  # type: ignore[assignment]
    return schema


def validate_spec(data: dict, schema_name: str = "agent_spec") -> list[str]:  # type: ignore[type-arg]
    """Validate data against a named schema.

    Args:
        data: The data dict to validate.
        schema_name: Schema to validate against (default: "agent_spec").

    Returns:
        List of error messages. Empty list means valid.
    """
    schema = load_schema(schema_name)
    validator = jsonschema.Draft7Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path)
        prefix = f"{path}: " if path else ""
        errors.append(f"{prefix}{error.message}")
    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_validator.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Run linters**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && ruff check factory/schemas/ && mypy factory/schemas/ --strict`
Expected: No errors

- [ ] **Step 6: Commit**

```bash
git add factory/schemas/validator.py tests/unit/test_validator.py
git commit -m "feat: implement schema validator with jsonschema"
```

---

## Task 5: Approval Record Model

**Files:**
- Create: `factory/approval/records.py`
- Test: `tests/unit/test_approval.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_approval.py`:

```python
from __future__ import annotations

import hashlib

from factory.approval.records import ApprovalRecord


def _make_valid_record() -> ApprovalRecord:
    return ApprovalRecord(
        decision="APPROVED",
        timestamp="2026-03-25T14:30:00Z",
        user_input="YES",
        action_type="architecture_approval",
        detail="single-agent with csv-reader, sql-executor",
    )


def test_valid_record_has_no_errors() -> None:
    record = _make_valid_record()
    errors = record.validate()
    assert errors == []


def test_hash_is_deterministic() -> None:
    record = _make_valid_record()
    hash1 = ApprovalRecord.compute_hash(
        record.action_type, record.detail, record.timestamp
    )
    hash2 = ApprovalRecord.compute_hash(
        record.action_type, record.detail, record.timestamp
    )
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 hex digest


def test_hash_matches_expected() -> None:
    payload = "architecture_approval:single-agent with csv-reader, sql-executor:2026-03-25T14:30:00Z"
    expected = hashlib.sha256(payload.encode()).hexdigest()
    actual = ApprovalRecord.compute_hash(
        "architecture_approval",
        "single-agent with csv-reader, sql-executor",
        "2026-03-25T14:30:00Z",
    )
    assert actual == expected


def test_hash_changes_with_different_input() -> None:
    hash1 = ApprovalRecord.compute_hash("a", "b", "c")
    hash2 = ApprovalRecord.compute_hash("a", "b", "d")
    assert hash1 != hash2


def test_validate_rejects_non_approved_decision() -> None:
    record = _make_valid_record()
    record.decision = "REJECTED"
    errors = record.validate()
    assert len(errors) > 0
    assert any("APPROVED" in e for e in errors)


def test_validate_rejects_empty_decision() -> None:
    record = _make_valid_record()
    record.decision = ""
    errors = record.validate()
    assert len(errors) > 0


def test_validate_rejects_missing_timestamp() -> None:
    record = _make_valid_record()
    record.timestamp = ""
    errors = record.validate()
    assert len(errors) > 0


def test_validate_rejects_invalid_timestamp() -> None:
    record = _make_valid_record()
    record.timestamp = "not-a-date"
    errors = record.validate()
    assert len(errors) > 0


def test_validate_rejects_empty_action_type() -> None:
    record = _make_valid_record()
    record.action_type = ""
    errors = record.validate()
    assert len(errors) > 0


def test_from_dict_creates_record() -> None:
    data = {
        "decision": "APPROVED",
        "timestamp": "2026-03-25T14:30:00Z",
        "user_input": "YES",
        "action_type": "architecture_approval",
        "detail": "single-agent",
    }
    record = ApprovalRecord.from_dict(data)
    assert record.decision == "APPROVED"
    assert record.action_type == "architecture_approval"


def test_from_dict_raises_on_missing_field() -> None:
    data = {"decision": "APPROVED"}
    try:
        ApprovalRecord.from_dict(data)
        assert False, "Should have raised"
    except (KeyError, TypeError):
        pass


def test_to_dict_round_trips() -> None:
    record = _make_valid_record()
    data = record.to_dict()
    assert data["decision"] == "APPROVED"
    assert data["timestamp"] == "2026-03-25T14:30:00Z"
    assert "hash" in data
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_approval.py -v`
Expected: FAIL — ImportError

- [ ] **Step 3: Implement the approval record model**

Create `factory/approval/records.py`:

```python
"""Approval record model with SHA-256 hashing."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ApprovalRecord:
    """Represents an approval decision for architecture generation.

    All 5 fields are required. decision must be "APPROVED".
    timestamp must be valid ISO 8601.
    """

    decision: str
    timestamp: str
    user_input: str
    action_type: str
    detail: str

    @staticmethod
    def compute_hash(action_type: str, detail: str, timestamp: str) -> str:
        """Compute SHA-256 hash of approval payload.

        Hash = SHA-256(action_type:detail:timestamp)
        """
        payload = f"{action_type}:{detail}:{timestamp}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def validate(self) -> list[str]:
        """Validate the approval record.

        Returns:
            List of error messages. Empty means valid.
        """
        errors: list[str] = []

        if self.decision != "APPROVED":
            errors.append(
                f'decision must be "APPROVED", got "{self.decision}"'
            )

        if not self.timestamp:
            errors.append("timestamp is required")
        else:
            try:
                datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
            except ValueError:
                errors.append(
                    f"timestamp must be valid ISO 8601, got \"{self.timestamp}\""
                )

        if not self.action_type:
            errors.append("action_type is required")

        if not self.detail:
            errors.append("detail is required")

        return errors

    @classmethod
    def from_dict(cls, data: dict) -> ApprovalRecord:  # type: ignore[type-arg]
        """Create an ApprovalRecord from a dict.

        Raises:
            KeyError: If required fields are missing.
        """
        return cls(
            decision=data["decision"],
            timestamp=data["timestamp"],
            user_input=data["user_input"],
            action_type=data["action_type"],
            detail=data["detail"],
        )

    def to_dict(self) -> dict[str, str]:
        """Convert to dict with computed hash included."""
        return {
            "decision": self.decision,
            "timestamp": self.timestamp,
            "user_input": self.user_input,
            "action_type": self.action_type,
            "detail": self.detail,
            "hash": self.compute_hash(
                self.action_type, self.detail, self.timestamp
            ),
        }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_approval.py -v`
Expected: All 12 tests PASS

- [ ] **Step 5: Run linters**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && ruff check factory/approval/ && mypy factory/approval/ --strict`
Expected: No errors

- [ ] **Step 6: Commit**

```bash
git add factory/approval/records.py tests/unit/test_approval.py
git commit -m "feat: implement approval record model with SHA-256 hashing"
```

---

## Task 6: Auxiliary CLI Skeleton

**Files:**
- Create: `factory/cli/main.py`
- Test: `tests/unit/test_cli.py`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/test_cli.py`:

```python
from __future__ import annotations

from click.testing import CliRunner

from factory.cli.main import cli


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_validate_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--help"])
    assert result.exit_code == 0
    assert "Validate" in result.output or "validate" in result.output


def test_skills_placeholder() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0


def test_personas_placeholder() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_cli.py -v`
Expected: FAIL — ImportError

- [ ] **Step 3: Implement the CLI**

Create `factory/cli/main.py`:

```python
"""Auxiliary CLI for Agent Factory utilities."""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from factory import __version__
from factory.schemas.validator import validate_spec


@click.group()
def cli() -> None:
    """Agent Factory — auxiliary utilities."""


@cli.command()
def version() -> None:
    """Print the Agent Factory version."""
    click.echo(f"agent-factory {__version__}")


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def validate(file: str) -> None:
    """Validate a spec YAML file against the schema."""
    path = Path(file)
    with open(path) as f:
        data: dict = yaml.safe_load(f)  # type: ignore[assignment]

    errors = validate_spec(data)
    if errors:
        click.echo(f"Validation failed with {len(errors)} error(s):", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        raise SystemExit(1)
    else:
        click.echo("Valid.")


@cli.command()
def skills() -> None:
    """List available built-in skills."""
    click.echo("Built-in skills: (not yet loaded — Phase 4)")


@cli.command()
def personas() -> None:
    """List available built-in personas."""
    click.echo("Built-in personas: (not yet loaded — Phase 4)")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/unit/test_cli.py -v`
Expected: All 4 tests PASS

- [ ] **Step 5: Verify CLI entry point works**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && factory version`
Expected: `agent-factory 1.0.0`

- [ ] **Step 6: Run linters**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && ruff check factory/cli/ && mypy factory/cli/ --strict`
Expected: No errors

- [ ] **Step 7: Commit**

```bash
git add factory/cli/main.py tests/unit/test_cli.py
git commit -m "feat: add auxiliary CLI with version, validate, skills, personas commands"
```

---

## Task 7: Full Verification

**Files:** None (verification only)

- [ ] **Step 1: Run all tests**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && pytest tests/ -v --tb=short`
Expected: All 23 tests PASS (7 validator + 12 approval + 4 CLI)

- [ ] **Step 2: Run ruff on entire codebase**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && ruff check factory/ tests/`
Expected: No errors

- [ ] **Step 3: Run mypy on entire codebase**

Run: `cd /Users/MoonGwanghoon/hoops/agent-factory && mypy factory/ --strict`
Expected: No errors

- [ ] **Step 4: Verify validate CLI command with a sample spec**

Run:
```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
cat > /tmp/test-spec.yaml << 'EOF'
name: test-bot
description: A test agent
type: single
EOF
factory validate /tmp/test-spec.yaml
```
Expected: `Valid.`

- [ ] **Step 5: Commit final state**

```bash
git add -A
git commit -m "chore: phase 1 complete — foundation scaffold verified"
```

---

## Phase 1 Acceptance Criteria

- [ ] `factory version` prints `agent-factory 1.0.0`
- [ ] `factory validate sample.yaml` validates against schema
- [ ] Approval hash is deterministic (SHA-256)
- [ ] All 23 tests pass
- [ ] `ruff check` zero errors
- [ ] `mypy --strict` zero errors

---

## Subsequent Plans

After Phase 1 is complete, the following plans should be created separately:

| Plan | Depends On | Description |
|------|-----------|-------------|
| Phase 2: Core Generator | Phase 1 | Renderer, repo builder, packager, generate() orchestrator |
| Phase 3: Templates | Phase 2 | All Jinja2 templates for generated agent repos |
| Phase 4: Registry | Phase 1 | Built-in skills (.md), personas (.yaml), registry loader |
| Phase 5: Workflow Files | Phases 2-4 | CLAUDE.md and CODEX.md for Agent Factory itself |
| Phase 6: Polish + Release | All | Integration tests, examples, docs, PyPI prep |

Note: Phase 4 (Registry) can be planned and executed in parallel with Phases 2-3 since it only depends on Phase 1.
