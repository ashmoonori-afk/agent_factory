# Template Changelog

All notable changes to Agent Factory templates are documented here.
Changes are classified as:
- **MAJOR**: Alters generated agent behavior (policy, persona, skill rendering)
- **MINOR**: Adds new output files or optional sections
- **PATCH**: Typo fixes, formatting, comments

## [1.0.1] - 2026-03-25

### Fixed (PATCH)
- YAML alias parse error: policy values like `*` now quoted as `"*"` in agent_spec.yaml and policy.yaml
- Dead reference: `context/knowledge.md` mention removed from CLAUDE.md/CODEX.md when no context is specified
- Dead reference: `skills/index.yaml` mention conditional on skills being present
- Reading order in docs/reading_order.md now conditional for context and skills entries

## [1.0.0] - 2026-03-25

### Added (MINOR)
- **Single-agent templates** (6): CLAUDE.md, CODEX.md, README.md, agent_spec.yaml, meta.yaml, .env.example
- **Multi-agent templates** (8+): Above 6 + orchestrator.md, agents/agent_role.md, architecture/topology.yaml
- **Shared templates** (7): policies/policy.yaml, policies/approval_log.jsonl, docs/architecture.md, docs/policy.md, docs/reading_order.md, tests/test-agent.md, tests/test-policy.md
- Full PRD 12.1 file structure support (18+ files per generation)
- Resolved skill content injection (skills/*.md from registry)
- Auto-generated skills/index.yaml manifest
- Resolved persona data injection (personas/default.yaml from registry)
- Template version embedded in meta.yaml via templates/VERSION
