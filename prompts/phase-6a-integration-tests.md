# Phase 6A: Integration Tests + Examples

> **Depends on**: phase-5a
> **Read first**: `00-overview.md`

## Objective

Full smoke tests, example agents, validation.

---

## Task 1: Smoke Test

Create `tests/smoke/test_full_generation.py`:

```python
def test_single_agent_generation(tmp_path):
    """Full pipeline: valid spec → generate → verify all files."""
    spec = {
        "name": "test-bot",
        "description": "A test agent",
        "type": "single",
        "runtime": {"primary": "both"},
        "policies": {"deny": ["send_email"], "ask": [], "allow": ["*"]},
        "persona": {"tone": "professional", "language": "en"},
        "skills": ["csv-reader"],
        "context": "Test context",
    }
    approval = {
        "decision": "APPROVED",
        "timestamp": "2026-01-01T00:00:00Z",
        "user_input": "YES",
        "action_type": "architecture_approval",
        "detail": "test",
    }
    result = factory.generate(spec, str(tmp_path / "test-bot"), approval)

    assert result.file_count > 0
    assert (tmp_path / "test-bot" / "CLAUDE.md").exists()
    assert (tmp_path / "test-bot" / "CODEX.md").exists()
    assert (tmp_path / "test-bot" / "agent_spec.yaml").exists()
    assert (tmp_path / "test-bot" / "policies" / "policy.yaml").exists()
    assert (tmp_path / "test-bot" / "skills" / "csv-reader.md").exists()
    assert result.zip_path is not None

def test_multi_agent_generation(tmp_path):
    """Multi-agent spec → verify topology + per-agent files."""
    ...

def test_approval_required():
    """generate() without approval → ApprovalRequiredError."""
    ...

def test_invalid_spec():
    """Invalid spec → SpecValidationError."""
    ...
```

## Task 2: Example Specs

Create `examples/data-analysis-bot.yaml`:
```yaml
name: data-analysis-bot
description: "Analyze CSV and SQL data, generate summary reports"
type: single
runtime:
  primary: both
policies:
  deny: [send_email, delete_file, deploy, payment, external_share]
  ask: [execute_sql]
  allow: ["*"]
persona:
  tone: professional
  language: en
skills:
  - sql-executor
  - csv-reader
  - json-parser
  - text-summarizer
context: |
  This agent helps users analyze data from CSV files and SQL databases.
  It can summarize findings and answer questions about the data.
```

Create `examples/code-assistant.yaml` similarly.

## Task 3: Generate Example Repos

Use `factory.generate()` to produce example repos under `examples/`.

## Verification

```bash
pytest tests/ -v --tb=short
ruff check .
mypy factory/ --strict
```
