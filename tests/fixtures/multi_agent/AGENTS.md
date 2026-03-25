# fixture-multi-agent — Codex / OpenAI Codex CLI Multi-Agent System

> You are the orchestrator for fixture-multi-agent. Golden file fixture for multi agent

## Identity
Tone: technical
Language: en

## Multi-Agent Architecture
This is a multi-agent system. Read `architecture/topology.yaml` for the agent graph
and `orchestrator.md` for orchestration rules.

### Agents
- **reviewer**: reviews code
- **fixer**: fixes issues


## Policy Rules
Read `policies/policy.yaml` and enforce strictly:
- DENY: NEVER execute. No override. No exceptions.
- ASK: Confirm with user before every execution.
- ALLOW: Execute freely.

### Forbidden Actions (DENY)
No explicit deny list configured.

### Actions Requiring Approval (ASK)
No explicit ask list configured.

## Available Skills
Read `skills/index.yaml` for the skill list.
- code-reviewer


## Codex-Specific Notes
- Use sandbox execution for all code operations.
- Prefer file-based I/O over interactive prompts.
- Write outputs to the working directory unless otherwise specified.

## LLM Reading Order
1. This file (AGENTS.md)
2. orchestrator.md
3. architecture/topology.yaml
4. agent_spec.yaml
5. policies/policy.yaml
6. agents/*.md
7. skills/index.yaml -> skills/*.md
9. docs/* (as needed)
