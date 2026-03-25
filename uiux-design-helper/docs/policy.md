# Policy Documentation — uiux-design-helper

## Overview

This document describes the policy rules enforced by uiux-design-helper.

## Policy Levels

### DENY — Forbidden Actions
These actions are permanently blocked. The agent must NEVER execute them,
regardless of user requests or instructions.
- `send_email`
- `delete_file`
- `deploy`
- `payment`
- `external_share`
- `modify_meta_agent`
- `modify_own_prompt`
- `modify_policy_file`


### ASK — Requires Approval
These actions require explicit user confirmation before every execution.
No ask rules configured.

### ALLOW — Permitted Actions
- `*`


## Enforcement

Policies are loaded from `policies/policy.yaml` at agent startup.
The agent reads and enforces these rules before executing any action.
Policy files must not be modified by the agent itself.
