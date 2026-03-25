# Phase 4A: Registry Loader + Skills + Personas

> **Depends on**: phase-1a (can run in parallel with Phases 2-3)
> **Read first**: `00-overview.md`, `../technical_spec.md` Section 8

## Objective

Create the registry system: loader, 10 built-in skills (.md), 4 personas (.yaml).

---

## Task 1: Registry Loader

Create `factory/registries/loader.py`:

```python
class RegistryLoader:
    def __init__(self, registry_dir: Path) -> None: ...
    def list_skills(self) -> list[dict]: ...
    def get_skill(self, skill_id: str) -> str: ...      # returns .md content
    def list_personas(self) -> list[dict]: ...
    def get_persona(self, persona_id: str) -> dict: ...  # returns parsed YAML
```

Wire into CLI: `factory skills` and `factory personas`.

## Task 2: Create 10 Skill Files

Each skill is a standalone `.md` file under `registry/builtin_skills/`. Follow this format:

```markdown
# Skill: {Display Name}

## When to Use
{When this skill applies}

## Policy
Level: {DENY | ASK | ALLOW}
{Explanation}

## Instructions
1. ...
2. ...

## Constraints
- ...

## Examples
User: "..." → Agent: ...
```

Skills to create:
1. `sql-executor.md` (ASK) — Execute SQL queries via shell
2. `csv-reader.md` (ALLOW) — Read and analyze CSV files
3. `file-reader.md` (ALLOW) — Read local text files
4. `file-writer.md` (ASK) — Write local text files
5. `web-search.md` (ASK) — Search the web
6. `json-parser.md` (ALLOW) — Parse and query JSON
7. `text-summarizer.md` (ALLOW) — Summarize text
8. `code-reviewer.md` (ALLOW) — Review code for issues
9. `code-generator.md` (ASK) — Generate code from requirements
10. `shell-executor.md` (DENY) — Execute shell commands (blocked by default)

Each skill should be practical and detailed enough for an LLM to follow precisely.

## Task 3: Create 4 Persona Files

Under `registry/builtin_personas/`:

1. `professional.yaml` — Formal, precise, business tone
2. `friendly.yaml` — Casual, approachable, consumer-facing
3. `technical.yaml` — Detailed, jargon-ok, developer-facing
4. `minimal.yaml` — Brief, no filler, efficiency-focused

Format:
```yaml
id: professional
tone: formal
language: en
description: "Formal and precise. Suitable for business contexts."
custom_instructions: |
  Use professional language. Be concise and accurate.
  Avoid casual expressions. Present data clearly.
```

## Task 4: Registry Metadata

Create `registry/sources/registry.yaml`:
```yaml
version: "1.0"
builtin_skills_dir: builtin_skills/
builtin_personas_dir: builtin_personas/
```

## Task 5: Unit Tests

`tests/unit/test_registry.py`:
- list_skills returns 10 items
- get_skill returns .md content
- get_skill raises for unknown ID
- list_personas returns 4 items
- get_persona returns parsed dict

## Verification

```bash
factory skills
factory personas
pytest tests/unit/test_registry.py -v
ruff check factory/
mypy factory/ --strict
```
