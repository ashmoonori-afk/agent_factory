# Architecture — fixture-multi-agent

## Overview

Golden file fixture for multi agent

**Type:** multi

## Components

### Agent Instructions
- `CLAUDE.md` — Instructions for Claude Code
- `CODEX.md` — Instructions for Codex

### Policies
Policy enforcement is defined in `policies/policy.yaml`.
All actions are classified as DENY, ASK, or ALLOW.

### Skills
This agent uses the following skills:
- code-reviewer


## Multi-Agent Topology
- **reviewer**: reviews code
- **fixer**: fixes issues


See `architecture/topology.yaml` and `orchestrator.md` for details.
