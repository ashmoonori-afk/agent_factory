# Agent Factory

An LLM-native meta-agent and Python library that generates AI agent repositories through conversation. Agent Factory conducts interviews, enforces approval gates, and produces complete agent repos ready for Claude Code and Codex.

## Install

```bash
pip install agent-factory
```

Or for development:

```bash
git clone <repo-url> && cd agent-factory
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick Start

### As a Claude Code / Codex meta-agent

Open this project in Claude Code. The LLM reads `CLAUDE.md` and becomes the Agent Factory interviewer. It will:

1. Ask you questions about the agent you want to build
2. Show you the proposed architecture
3. Request your explicit approval
4. Call `factory.generate()` to create the complete repo

### As a Python library

```python
import factory

spec = {
    "name": "my-bot",
    "description": "Analyzes data and generates reports",
    "type": "single",
    "skills": ["csv-reader", "sql-executor"],
    "persona": {"tone": "professional", "language": "en"},
    "policies": {
        "deny": ["send_email", "delete_file", "deploy"],
        "ask": ["execute_sql"],
        "allow": ["*"],
    },
}

approval = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "my-bot single-agent approved",
}

result = factory.generate(
    spec=spec,
    output="./my-bot",
    approval_record=approval,
)

print(f"Generated {result.file_count} files at {result.output_path}")
```

### From a YAML spec

```bash
# Validate a spec
python -m factory validate examples/data-analysis-bot.yaml

# List available skills
python -m factory skills

# List available personas
python -m factory personas
```

## What Gets Generated

Each generated agent repo contains:

- `CLAUDE.md` / `CODEX.md` -- the agent's system prompt for Claude Code and Codex
- `agent_spec.yaml` -- the full agent specification
- `meta.yaml` -- generation metadata and factory version
- `policies/` -- deny, ask, and allow policy definitions
- `approval_log.jsonl` -- immutable audit trail of the approval decision
- `.env.example` -- environment variable template

For multi-agent specs, additional files include orchestrator definitions, agent role descriptions, and topology configuration.

## Examples

See `examples/` for ready-to-use specs:

- `examples/data-analysis-bot.yaml` -- single agent with SQL and CSV skills
- `examples/code-assistant.yaml` -- single agent with code review and generation skills

Generated repos from these specs are in `examples/data-analysis-bot/` and `examples/code-assistant/`.

## Testing

```bash
pytest tests/ -v
ruff check factory/ tests/
mypy factory/ --strict
```

## License

MIT -- see [LICENSE](LICENSE).
