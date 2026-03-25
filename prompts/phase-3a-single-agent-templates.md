# Phase 3A: Single-Agent Jinja2 Templates

> **Depends on**: phase-2b
> **Read first**: `00-overview.md`, `../prd_final.md` Section 12

## Objective

Create all Jinja2 templates for single-agent repository generation.

---

## Templates to Create

All under `templates/single_agent/`:

### 1. CLAUDE.md.j2

The generated agent's Claude Code instructions. Must include:
- Agent identity (name, description, from persona)
- Policy rules (DENY/ASK/ALLOW lists rendered inline)
- Available skills (list with references to skills/*.md)
- Context reference (context/knowledge.md)
- LLM reading order

### 2. CODEX.md.j2

Same content as CLAUDE.md.j2 but adapted for Codex tool conventions.

### 3. agent_spec.yaml.j2

Machine-readable spec. Render all spec fields as YAML.

### 4. README.md.j2

- What this agent does
- How to open in Claude Code / Codex
- Skills available
- Policy summary
- .env setup instructions

### 5. meta.yaml.j2

```yaml
generator_version: "{{ meta.generator_version }}"
generated_at: "{{ meta.generated_at }}"
spec_version: "1.0"
```

### 6. .env.example.j2

API key placeholders if needed. May be empty for agents that don't need external APIs.

## Shared Templates (under `templates/`)

### docs/architecture.md.j2, docs/policy.md.j2, docs/reading_order.md.j2

Human-readable documentation.

### policies/policy.yaml.j2

```yaml
deny: {{ policies.deny | tojson }}
ask: {{ policies.ask | tojson }}
allow: {{ policies.allow | tojson }}
```

### policies/approval_log.jsonl.j2

Initial approval record as first line.

### tests/test-policy.md.j2, tests/test-agent.md.j2

Verification prompts the LLM can follow to test the agent.

---

## Template Guidelines

- Every template receives the context dict from tech spec Section 5.2.
- Use `{{ agent.name }}`, `{{ agent.description }}`, `{{ policies.deny }}`, etc.
- DENY list must be rendered inline in CLAUDE.md.j2 for immediate visibility.
- Skills are referenced by ID; actual .md files are copied separately by the generator.

## Verification

```bash
ls templates/single_agent/CLAUDE.md.j2
ls templates/single_agent/CODEX.md.j2
ls templates/single_agent/agent_spec.yaml.j2
ls templates/docs/reading_order.md.j2
ls templates/policies/policy.yaml.j2
ls templates/tests/test-policy.md.j2
```
