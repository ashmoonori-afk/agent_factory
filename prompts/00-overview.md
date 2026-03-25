# Agent Factory — Project Context

> Read this file first. It provides shared context for all phase prompts.

## What We Are Building

Agent Factory is a **meta-agent + Python library hybrid**.

- **CLAUDE.md / CODEX.md** — Workflow files that make the LLM conduct interviews and enforce approvals.
- **Python library (`factory`)** — Takes a spec dict + approval record, renders Jinja2 templates, writes 20+ files to disk in < 2 seconds. Zero token cost.

The LLM does the talking. Python does the file generation.

## Generated Output

Generated agents are **CLAUDE.md/CODEX.md-based meta-agents**, NOT Python programs. They have:
- `CLAUDE.md` / `CODEX.md` — Agent instructions
- `skills/*.md` — LLM-executable skill files
- `policies/policy.yaml` — DENY/ASK/ALLOW enforcement
- No `main.py`, no `requirements.txt`, no Python runtime code.

## Key Documents

- `../prd_final.md` — Product requirements (v2.0.0)
- `../technical_spec.md` — Module architecture, API, templates (v2.0.0)
- `../development_plan.md` — Phase breakdown, dependencies (v2.0.0)
- `docs/superpowers/specs/2026-03-25-architecture-redesign.md` — Architecture decision record

## Technology Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Runtime |
| Jinja2 | Template engine |
| PyYAML | YAML parsing |
| jsonschema | Schema validation |
| click | Auxiliary CLI only |
| pytest | Testing |
| ruff | Linting |
| mypy | Type checking (strict) |

## Package Structure

```
agent-factory/
├── factory/              # Python library (~12 source files)
│   ├── __init__.py       # Public API: generate(), validate()
│   ├── cli/              # Auxiliary: validate, skills, personas, version
│   ├── core/             # generator, renderer, repo_builder, packager
│   ├── schemas/          # jsonschema validator
│   ├── approval/         # ApprovalRecord model + hash
│   └── registries/       # Built-in skill/persona loader
├── schemas/              # YAML schema definitions (4 files)
├── templates/            # Jinja2 templates (~18 files)
├── registry/             # Built-in skills (.md) + personas (.yaml) (~15 files)
├── tests/                # Unit + snapshot + smoke (~8 files)
├── CLAUDE.md             # Agent Factory workflow (Claude Code)
└── CODEX.md              # Agent Factory workflow (Codex)
```

## Verification After Every Step

```bash
ruff check factory/
mypy factory/ --strict
pytest tests/ -v --tb=short
```
