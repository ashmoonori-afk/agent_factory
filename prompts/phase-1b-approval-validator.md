# Phase 1B: Schema Validator + Approval Record Model

> **Depends on**: phase-1a
> **Read first**: `00-overview.md`

## Objective

Implement schema validation and approval record model with SHA-256 hashing.

---

## Task 1: Schema Validator

Create `factory/schemas/validator.py`:
- `load_schema(name: str) -> dict` — Load YAML schema from `schemas/` directory
- `validate_spec(data: dict, schema_name: str = "agent_spec") -> list[str]` — Validate and return errors

Wire into `factory validate` CLI command.

## Task 2: Approval Record Model

Create `factory/approval/records.py`:

```python
@dataclass
class ApprovalRecord:
    decision: str           # must be "APPROVED"
    timestamp: str          # ISO 8601
    user_input: str         # exact input
    action_type: str        # e.g. "architecture_approval"
    detail: str             # what was approved

    @staticmethod
    def compute_hash(action_type: str, detail: str, timestamp: str) -> str:
        """SHA-256(action_type:detail:timestamp)"""

    def validate(self) -> list[str]:
        """Return errors. Empty = valid."""

    @classmethod
    def from_dict(cls, data: dict) -> "ApprovalRecord":
        """Create from dict, validate all fields present."""
```

Validation rules:
1. All 5 fields required.
2. `decision` must equal `"APPROVED"`.
3. `timestamp` must be valid ISO 8601.

## Task 3: Unit Tests

`tests/unit/test_validator.py`:
- Valid minimal spec passes
- Missing required field fails
- Invalid type enum fails

`tests/unit/test_approval.py`:
- Hash is deterministic
- Hash changes with different inputs
- Validation rejects missing fields
- Validation rejects non-APPROVED decision

## Verification

```bash
pytest tests/unit/test_validator.py tests/unit/test_approval.py -v
factory validate --help
ruff check factory/
mypy factory/ --strict
```
