# Agent Factory — Architecture Redesign Spec

> **Date**: 2026-03-25
> **Status**: Approved
> **Decision**: Migrate from traditional Python CLI to LLM-native meta-agent + Python library hybrid

---

## 1. Context & Problem

Agent Factory was originally designed as a Python CLI tool (`factory create`) using the `click` framework. Users would run the CLI, answer questions via stdin, and receive a generated Python agent repository.

This architecture has a fundamental conflict: the target users (non-technical, may never have used a terminal) must install Python, pip-install the tool, and operate a CLI — the exact friction the product is supposed to eliminate.

The redesign makes Agent Factory run natively inside Claude Code and Codex, where the LLM IS the interface.

---

## 2. Architecture Decision

### Model: Schema-Enforced Hybrid (Approach B)

```
LLM (Claude Code / Codex)         Python Library (factory)
─────────────────────────         ──────────────────────────
● Interview (conversation)         ● Schema validation (jsonschema)
● Normalization (spec dict)        ● Approval verification (reject if missing)
● Architecture proposal            ● Jinja2 template rendering
● Approval gate (collect YES)      ● Directory + file creation
● Error reporting                  ● ZIP packaging
                                   ● meta.yaml + approval_log.jsonl

Token cost: ~3-5K                  Token cost: 0
Time: conversation pace            Time: < 2 seconds
```

**Key principle**: LLM is the brain, Python is the hands. Single contact point: `factory.generate(spec, output, approval_record)`.

### Why Approach B over alternatives

| Approach | Token Efficiency | Output Completeness | Safety |
|----------|-----------------|-------------------|--------|
| A) Thin library (no approval enforcement) | Good | Good | Weak — LLM can skip approval |
| **B) Schema-enforced (chosen)** | **Good** | **Good** | **Strong — Python rejects without approval** |
| C) Full orchestrator | Medium (many round-trips) | Good | Strong but complex |

---

## 3. Public API

```python
import factory

# Validate spec
errors: list[str] = factory.validate(spec)

# Generate (approval_record required — rejects without it)
result: GenerationResult = factory.generate(
    spec=spec_dict,
    output="./my-agent",
    approval_record={
        "decision": "APPROVED",
        "timestamp": "2026-03-25T14:30:00Z",
        "user_input": "YES",
        "action_type": "architecture_approval",
        "detail": "single-agent with sql-executor, csv-reader",
    },
    no_zip=False,
)

# Query registry
skills: list[dict] = factory.get_builtin_skills()
personas: list[dict] = factory.get_builtin_personas()
```

### GenerationResult

```python
@dataclass
class GenerationResult:
    output_path: str        # "./my-agent"
    zip_path: str | None    # "./my-agent.zip"
    file_count: int         # 18
    files: list[str]        # all created file paths
```

### Exceptions

- `ApprovalRequiredError` — approval_record missing or decision != "APPROVED"
- `SpecValidationError` — spec fails schema validation
- `GenerationError` — file creation failed

### Approval Record Schema

```python
approval_record = {
    "decision": str,        # Required: "APPROVED" (only accepted value)
    "timestamp": str,       # Required: ISO 8601 (e.g. "2026-03-25T14:30:00Z")
    "user_input": str,      # Required: exact user input (e.g. "YES")
    "action_type": str,     # Required: e.g. "architecture_approval"
    "detail": str,          # Required: human-readable summary of what was approved
}
```

`generate()` validates:
1. All 5 fields must be present.
2. `decision` must equal `"APPROVED"` (case-sensitive).
3. `timestamp` must be valid ISO 8601.
4. Hash is computed as SHA-256(`action_type` + `detail` + `timestamp`).

### Auxiliary CLI (utilities only)

```bash
factory validate spec.yaml   # Validate a spec file
factory skills               # List built-in skills
factory personas             # List built-in personas
factory version              # Print version
```

---

## 4. generate() Internal Flow

```
1. Validate spec against agent_spec.schema.yaml
   → SpecValidationError if invalid
2. Verify approval_record exists and decision == "APPROVED"
   → ApprovalRequiredError if missing/invalid
3. Compute approval hash: SHA-256(action_type + detail + timestamp)
4. Resolve skills from registry → match skill IDs to .md files
5. Resolve persona from registry → match persona ID to .yaml
6. Select template set (single_agent/ or multi_agent/)
7. Render all Jinja2 templates → in-memory string dict
8. Create output directory tree → os.makedirs
9. Write all rendered files to disk
10. Write meta.yaml (generator version, timestamp, OS)
11. Write approval_log.jsonl (initial approval record with hash)
12. Create ZIP archive (unless no_zip=True)
13. Return GenerationResult
```

---

## 5. Spec Dict Schema

```python
spec = {
    # Required
    "name": str,              # kebab-case, used as folder name
    "description": str,       # 1-2 sentence natural language
    "type": "single" | "multi",
    "runtime": {
        "primary": "both",     # "claude-code" | "codex" | "both" (default: "both")
    },

    # Optional (defaults applied)
    "policies": {
        "deny": list[str],     # default: 8 standard items
        "ask": list[str],      # default: []
        "allow": list[str],    # default: ["*"]
    },
    "persona": {
        "tone": str,           # default: "professional"
        "language": str,       # default: "en"
        "custom_instructions": str,
    },
    "skills": list[str],       # skill IDs, default: []
    "context": str,            # background knowledge, default: ""

    # Multi-agent only (required when type == "multi")
    "agents": list[{
        "id": str,
        "role": str,
        "next": list[str],
    }],
    "topology": {
        "entry": str,
        "max_loops": int,      # default: 3
        "exit_condition": str,
    },
}
```

---

## 6. Agent Factory Package Structure

```
agent-factory/
├── CLAUDE.md                    # Claude Code workflow instructions
├── CODEX.md                     # Codex workflow instructions
├── pyproject.toml               # Library-first, minimal CLI
├── .env.example
├── .gitignore
│
├── factory/
│   ├── __init__.py              # Public API: generate(), validate(), etc.
│   ├── __main__.py              # python -m factory
│   │
│   ├── cli/                     # Auxiliary utilities only
│   │   ├── __init__.py
│   │   └── main.py              # validate, skills, personas, version
│   │
│   ├── core/                    # Generation engine
│   │   ├── __init__.py
│   │   ├── generator.py         # generate() implementation
│   │   ├── renderer.py          # Jinja2 template rendering
│   │   ├── repo_builder.py      # Directory tree + file writing
│   │   └── packager.py          # ZIP creation
│   │
│   ├── schemas/                 # Schema validation
│   │   ├── __init__.py
│   │   └── validator.py         # jsonschema wrapper
│   │
│   ├── approval/                # Record validation only
│   │   ├── __init__.py
│   │   └── records.py           # ApprovalRecord model + hash
│   │
│   └── registries/              # Local registry only
│       ├── __init__.py
│       └── loader.py            # Load built-in skills/personas
│
├── schemas/                     # YAML schema definitions
│   ├── agent_spec.schema.yaml
│   ├── policy.schema.yaml
│   ├── persona.schema.yaml
│   └── skill.schema.yaml
│
├── templates/                   # Jinja2 templates
│   ├── single_agent/
│   │   ├── CLAUDE.md.j2         # Generated agent's Claude Code instructions
│   │   ├── CODEX.md.j2          # Generated agent's Codex instructions
│   │   ├── agent_spec.yaml.j2
│   │   ├── README.md.j2
│   │   ├── meta.yaml.j2
│   │   └── .env.example.j2
│   ├── multi_agent/
│   │   ├── CLAUDE.md.j2
│   │   ├── CODEX.md.j2
│   │   ├── orchestrator.md.j2   # Orchestration instructions
│   │   ├── agents/
│   │   │   └── agent_role.md.j2 # Per-agent instructions
│   │   ├── architecture/
│   │   │   └── topology.yaml.j2
│   │   ├── agent_spec.yaml.j2
│   │   ├── README.md.j2
│   │   └── meta.yaml.j2
│   ├── docs/
│   │   ├── architecture.md.j2
│   │   ├── policy.md.j2
│   │   └── reading_order.md.j2
│   ├── policies/
│   │   ├── policy.yaml.j2
│   │   └── approval_log.jsonl.j2
│   └── tests/
│       ├── test-policy.md.j2
│       └── test-agent.md.j2
│
├── registry/
│   ├── builtin_skills/          # 10 skill .md files
│   │   ├── sql-executor.md
│   │   ├── csv-reader.md
│   │   ├── file-reader.md
│   │   ├── file-writer.md
│   │   ├── web-search.md
│   │   ├── json-parser.md
│   │   ├── text-summarizer.md
│   │   ├── code-reviewer.md
│   │   ├── code-generator.md
│   │   └── shell-executor.md
│   ├── builtin_personas/        # 4 persona YAML files
│   │   ├── professional.yaml
│   │   ├── friendly.yaml
│   │   ├── technical.yaml
│   │   └── minimal.yaml
│   └── sources/
│       └── registry.yaml        # Registry metadata
│
├── tests/
│   ├── unit/
│   │   ├── test_generator.py
│   │   ├── test_renderer.py
│   │   ├── test_validator.py
│   │   ├── test_approval.py
│   │   └── test_registry.py
│   ├── snapshot/
│   │   ├── test_single_agent.py
│   │   └── test_multi_agent.py
│   └── smoke/
│       └── test_full_generation.py
│
└── docs/
    ├── architecture/
    ├── policies/
    └── repo_reading_order/
```

**Source files: ~12 | Schema files: 4 | Template files: ~20 | Registry files: ~15 | Test files: ~8 | Total: ~70**

---

## 7. Generated Agent Repository Structure

The output of `factory.generate()`. This is a CLAUDE.md/CODEX.md-based meta-agent, NOT a Python program.

```
my-agent/
├── CLAUDE.md                     # Claude Code agent instructions
├── CODEX.md                      # Codex agent instructions
├── agent_spec.yaml               # Machine-readable spec (source of truth)
├── meta.yaml                     # Generator version, creation timestamp
├── README.md                     # Human guide: what this agent is, how to open
├── .env.example                  # API key placeholders
│
├── personas/
│   └── default.yaml              # Persona definition
│
├── policies/
│   ├── policy.yaml               # DENY/ASK/ALLOW rules
│   └── approval_log.jsonl        # Architecture approval record
│
├── skills/                       # LLM-executable skill instructions
│   ├── index.yaml                # Skill manifest
│   └── <skill-name>.md           # Per-skill instructions (only selected skills)
│
├── architecture/
│   └── topology.yaml             # Multi-agent topology (multi only)
│
├── context/
│   └── knowledge.md              # User-provided background knowledge
│
├── docs/
│   ├── architecture.md
│   ├── policy.md
│   └── reading_order.md
│
└── tests/
    ├── test-policy.md            # Policy violation test prompt
    └── test-agent.md             # Basic behavior test prompt
```

### Generated CLAUDE.md Structure

```markdown
# {agent_name} — Claude Code Agent

> You are {agent_name}. {description}

## Identity
[Rendered from persona: tone, language, custom instructions]

## Policy Rules
Read `policies/policy.yaml` and enforce strictly:
- DENY: NEVER execute. No override. No exceptions.
- ASK: Confirm with user before every execution.
- ALLOW: Execute freely.

[Full DENY list rendered inline for immediate visibility]

## Available Skills
Read `skills/index.yaml` for the skill list.
For each task, find the matching skill in `skills/{name}.md` and follow its instructions.

## Context
Read `context/knowledge.md` for background knowledge.

## LLM Reading Order
1. This file (CLAUDE.md)
2. agent_spec.yaml
3. policies/policy.yaml
4. personas/default.yaml
5. skills/index.yaml → skills/*.md
6. context/knowledge.md
7. docs/* (as needed)
```

---

## 8. Skill File Format

Skills are `.md` instruction files that Claude Code / Codex follow. NOT Python code.

```markdown
# Skill: {Display Name}

## When to Use
{Natural language description of when this skill applies}

## Policy
Level: {DENY | ASK | ALLOW}
{Policy explanation and constraints}

## Instructions
{Step-by-step instructions the LLM follows}
1. ...
2. ...
3. ...

## Constraints
- {Safety constraint 1}
- {Safety constraint 2}

## Examples
{Example user request → expected agent behavior}
```

### Skill Policy Precedence

Each skill `.md` file contains a `Policy` field (DENY/ASK/ALLOW). This is a **default recommendation**, not an override. The authoritative policy source is always `policies/policy.yaml` in the generated agent repo.

Merge strategy during generation:
1. Start with the global `policies` block from the spec.
2. For each selected skill, if its action is NOT listed in any global policy list, apply the skill's recommended level.
3. Global policy always wins over skill-level recommendations.

Example: If `shell-executor.md` recommends DENY but the user explicitly added `shell_execute` to their ALLOW list, the ALLOW takes precedence.

### v1 Built-in Skills

| Skill ID | Policy | Description |
|----------|--------|-------------|
| sql-executor | ASK | Execute SQL queries via Bash tool |
| csv-reader | ALLOW | Read and analyze CSV files |
| file-reader | ALLOW | Read local text files |
| file-writer | ASK | Write local text files |
| web-search | ASK | Search the web for information |
| json-parser | ALLOW | Parse and query JSON data |
| text-summarizer | ALLOW | Summarize text using LLM capabilities |
| code-reviewer | ALLOW | Review code for issues |
| code-generator | ASK | Generate code from requirements |
| shell-executor | DENY | Execute shell commands (blocked by default) |

---

## 9. CLAUDE.md / CODEX.md Workflow (Agent Factory Itself)

The LLM follows this mandatory workflow when a user wants to create an agent:

```
PHASE 1: Interview
  Ask Q1-Q4 one at a time (name, purpose, single/team, forbidden actions)
  Note: model selection (old Q4) removed — runtime model is determined by
  execution environment (Claude Code uses Claude, Codex uses its configured model)
  Optional: Q5-Q8 (skills, persona, ASK policies, context)
  Optional: Q9-Q11 (multi-agent only)

PHASE 2: Normalize
  Construct spec dict from answers
  Apply defaults for unspecified fields

PHASE 3: Architecture
  Present proposed architecture in readable format

PHASE 4: Approve [MANDATORY GATE]
  Display full architecture
  Require user to type YES
  Construct approval_record dict

PHASE 5: Generate
  Call: factory.generate(spec, output, approval_record)
  via Bash: python -c "import factory; ..."
  or via inline Python execution

PHASE 6: Deliver
  Report: file count, output path, ZIP path
  Show next steps: open in Claude Code / Codex
```

**Safety enforcement is dual-layer:**
1. CLAUDE.md/CODEX.md instructs LLM to collect approval (soft enforcement)
2. `factory.generate()` rejects if approval_record is missing (hard enforcement)

### CODEX.md Content Strategy

CODEX.md follows the same 6-phase workflow as CLAUDE.md. Differences:
- Tool references adapted for Codex capabilities (e.g., file operations, code execution)
- No Claude Code-specific features (e.g., Read/Write/Edit tool names)
- Same approval gate rules, same safety constraints
- Generated agents also receive both CLAUDE.md and CODEX.md with matching adaptations

---

## 10. What Changed from Original Design

### Removed

| Component | Reason |
|-----------|--------|
| `factory/cli/` (full CLI with click) | LLM is the interface; CLI reduced to utilities |
| `factory/interview/` | LLM conducts interview via conversation |
| `factory/normalizer/` | LLM constructs spec dict directly |
| `factory/planner/` | LLM proposes architecture in conversation |
| `factory/approvals/engine.py` | Approval gate is in CLAUDE.md; Python only verifies |
| `factory/approvals/policy.py` | Policy evaluation is LLM's job |
| `factory/approvals/store.py` | SQLite removed; approval in JSONL only |
| `factory/models/` | Generated agents are CLAUDE.md-based meta-agents running inside Claude Code/Codex; no model adapter code needed |
| `factory/runtime/state.py` | SQLite state tracking removed |
| `factory/runtime/failure_ledger.py` | Minimal state decision |
| `factory/runtime/generation_log.py` | Removed |
| `factory/runtime/recovery.py` | LLM handles errors in conversation |
| `state/` directory | No SQLite |
| `bootstrap/` (Agent Factory) | Not needed for meta-agent |
| Generated `main.py` | Generated agent is CLAUDE.md meta-agent, not Python |
| Generated `requirements.txt` | No pip install needed |
| Generated `agent/core.py` | CLAUDE.md replaces this |
| Generated `agent/model_adapter.py` | LLM calls itself; no adapter |
| Generated `bootstrap/` scripts | Open in Claude Code/Codex directly |

### Added

| Component | Reason |
|-----------|--------|
| Generated `CLAUDE.md` | Agent runs as Claude Code meta-agent |
| Generated `CODEX.md` | Agent runs as Codex meta-agent |
| `skills/*.md` | LLM-executable skill instruction files |
| `context/knowledge.md` | User background knowledge |
| `tests/test-*.md` | Verification prompts (not pytest) |
| `templates/**/CLAUDE.md.j2` | Template for generated agent instructions |
| Approval enforcement in `generate()` | Hard safety gate in Python code |

### Unchanged

| Component | Notes |
|-----------|-------|
| 6-phase workflow | Same order, same gates |
| DENY/ASK/ALLOW policy model | Same 3 levels |
| Schema definitions | Same YAML schemas |
| Jinja2 template engine | Same rendering approach |
| Registry (skills + personas) | Same concept, .md format instead of .py |
| agent_spec.yaml as source of truth | Same |
| approval_log.jsonl | Same append-only audit trail |
| meta.yaml | Same generation metadata |

---

## 11. Development Phases (New)

| Phase | Content | Output |
|-------|---------|--------|
| 1 | Project scaffold + schemas + approval record model | pyproject.toml, schemas/, factory/approval/ |
| 2 | Core generator (renderer + repo builder + packager) | factory/core/ |
| 3 | Templates (single/multi CLAUDE.md, CODEX.md, docs, policies, tests) | templates/ |
| 4 | Built-in skills (.md) + personas (.yaml) + registry loader | registry/, factory/registries/ |
| 5 | CLAUDE.md + CODEX.md for Agent Factory itself (**ground-up rewrite** — current files are severely outdated and reference removed CLI/Python structures) | Root workflow files |
| 6 | Tests + auxiliary CLI + examples + release prep | tests/, docs/, examples/ |
| Post-v1 | Curated skill recommendation list from GitHub/MCP marketplace | registry/sources/recommendations.yaml |

---

## 12. File Count Comparison

| Category | Before | After |
|----------|--------|-------|
| Source files | ~40 | ~12 |
| Schema files | 4 | 4 |
| Template files | ~25 | ~20 |
| Registry files | ~28 | ~15 |
| Test files | ~20 | ~8 |
| **Total** | **~120** | **~70** |

---

*End of Architecture Redesign Spec*
