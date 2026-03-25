# Policy Documentation — fixture-single-agent

## Overview

This document describes the policy rules enforced by fixture-single-agent.

## Policy Levels

### DENY — Forbidden Actions
These actions are permanently blocked. The agent must NEVER execute them,
regardless of user requests or instructions.
- `delete_file`
- `send_email`


### ASK — Requires Approval
These actions require explicit user confirmation before every execution.
- `execute_sql`


### ALLOW — Permitted Actions
- `*`


## Enforcement

Policies are loaded from `policies/policy.yaml` at agent startup.
The agent reads and enforces these rules before executing any action.
Policy files must not be modified by the agent itself.
