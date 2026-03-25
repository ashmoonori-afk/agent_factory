# Phase 6B: Release Prep

> **Depends on**: phase-6a
> **Read first**: `00-overview.md`

## Objective

README, open-source files, final validation, PyPI prep.

---

## Task 1: README.md

Write project README:
- What Agent Factory is (meta-agent + Python library)
- How to install (`pip install agent-factory`)
- How to use in Claude Code (open folder, start conversation)
- How to use in Codex (same)
- How to use the Python library directly
- How to use YAML spec mode
- Built-in skills list
- Built-in personas list

## Task 2: Open-Source Files

- `LICENSE` — MIT
- `CONTRIBUTING.md` — How to contribute
- `SECURITY.md` — Security policy
- `.env.example` — Empty (Agent Factory itself needs no API keys)

## Task 3: Final Validation

```bash
pip install -e .
factory version
factory skills
factory personas
factory validate examples/data-analysis-bot.yaml
pytest tests/ -v --tb=short
ruff check .
mypy factory/ --strict
```

All must pass with zero errors.

## Task 4: PyPI Prep

- Verify `pyproject.toml` metadata is complete
- `pip install build && python -m build`
- Test with `pip install dist/agent_factory-1.0.0-py3-none-any.whl`
- Verify `factory version` works from fresh install

## Verification

```bash
pip install -e .
factory version
pytest tests/ -v --tb=short
ruff check .
mypy factory/ --strict
```

v1.0.0 is ready.
