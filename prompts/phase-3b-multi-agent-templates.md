# Phase 3B: Multi-Agent Templates + Snapshot Tests

> **Depends on**: phase-3a
> **Read first**: `00-overview.md`, `../prd_final.md` Section 14

## Objective

Create multi-agent templates and snapshot tests for both single and multi generation.

---

## Multi-Agent Templates

Under `templates/multi_agent/`:

### 1. CLAUDE.md.j2

Like single-agent but includes:
- Orchestration instructions (which agent handles what)
- Topology reference (architecture/topology.yaml)
- Per-agent skill assignments
- Communication flow description

### 2. CODEX.md.j2

Same as CLAUDE.md.j2 adapted for Codex.

### 3. orchestrator.md.j2

Instructions for how the LLM orchestrates multiple agents:
- Entry agent
- Handoff rules (which agent passes to which)
- Max loops (prevent infinite feedback)
- Exit condition

### 4. agents/agent_role.md.j2

Rendered once per agent in the topology:
```markdown
# Agent: {{ agent.id }}

## Role
{{ agent.role }}

## Next
Passes results to: {{ agent.next | join(", ") }}

## Skills
{% for skill in agent.skills %}
- {{ skill }}
{% endfor %}
```

### 5. architecture/topology.yaml.j2

```yaml
topology:
  entry: {{ topology.entry }}
  max_loops: {{ topology.max_loops }}
  exit_condition: "{{ topology.exit_condition }}"
  agents:
  {% for agent in agents %}
    - id: {{ agent.id }}
      role: "{{ agent.role }}"
      next: {{ agent.next | tojson }}
  {% endfor %}
```

### 6. agent_spec.yaml.j2, README.md.j2, meta.yaml.j2

Same structure as single-agent but with agents and topology fields included.

---

## Snapshot Tests

Create `tests/snapshot/test_single_agent.py`:
- Define a fixed spec dict
- Call `factory.generate()` with temp output dir
- Assert: all expected files exist
- Assert: CLAUDE.md contains agent name, DENY list
- Assert: policy.yaml contains correct deny list
- Assert: approval_log.jsonl contains approval record

Create `tests/snapshot/test_multi_agent.py`:
- Define a fixed multi-agent spec
- Assert: topology.yaml has correct agents
- Assert: per-agent .md files created for each role
- Assert: orchestrator.md references all agents

## Verification

```bash
ls templates/multi_agent/CLAUDE.md.j2
ls templates/multi_agent/orchestrator.md.j2
pytest tests/snapshot/ -v
```
