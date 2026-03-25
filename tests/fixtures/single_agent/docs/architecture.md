# Architecture — fixture-single-agent

## Overview

Golden file fixture for single agent

**Type:** single

## Components

### Agent Instructions
- `CLAUDE.md` — Instructions for Claude Code
- `CODEX.md` — Instructions for Codex

### Policies
Policy enforcement is defined in `policies/policy.yaml`.
All actions are classified as DENY, ASK, or ALLOW.

### Skills
This agent uses the following skills:
- csv-reader


