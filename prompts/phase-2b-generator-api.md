# Phase 2B: generate() Orchestrator + Public API

> **Depends on**: phase-2a
> **Read first**: `00-overview.md`, `../technical_spec.md` Sections 2-3

## Objective

Implement the `factory.generate()` function and wire the public API.

---

## Task 1: Generator Orchestrator

Create `factory/core/generator.py`:

```python
def generate(
    spec: dict,
    output: str,
    approval_record: dict,
    *,
    no_zip: bool = False,
) -> GenerationResult:
    """
    Full generation pipeline:
    1. Validate spec (jsonschema)           → SpecValidationError
    2. Validate approval_record             → ApprovalRequiredError
    3. Compute approval hash (SHA-256)
    4. Resolve skills from registry
    5. Resolve persona from registry
    6. Select template set (single/multi)
    7. Build template context dict
    8. Render all templates
    9. Create directory tree + write files
    10. Write meta.yaml
    11. Write approval_log.jsonl
    12. Create ZIP (unless no_zip)
    13. Return GenerationResult
    """
```

Exception classes:
- `ApprovalRequiredError(Exception)`
- `SpecValidationError(Exception)`
- `GenerationError(Exception)`

## Task 2: Public API

Wire in `factory/__init__.py`:

```python
from factory.core.generator import generate, GenerationResult
from factory.schemas.validator import validate_spec as validate
from factory.registries.loader import list_skills as get_builtin_skills
from factory.registries.loader import list_personas as get_builtin_personas
from factory.core.generator import (
    ApprovalRequiredError,
    SpecValidationError,
    GenerationError,
)
```

## Task 3: Unit Tests

`tests/unit/test_generator.py`:
- Valid spec + approval → generates files (use temp dir)
- Missing approval → raises ApprovalRequiredError
- Invalid spec → raises SpecValidationError
- no_zip=True → no ZIP created
- Generated files include CLAUDE.md, agent_spec.yaml, policy.yaml

## Verification

```bash
pytest tests/unit/test_generator.py -v
python3 -c "import factory; print(factory.generate.__doc__)"
ruff check factory/
mypy factory/ --strict
```
