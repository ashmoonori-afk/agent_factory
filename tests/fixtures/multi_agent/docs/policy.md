# Policy Documentation — fixture-multi-agent

## Overview

This document describes the policy rules enforced by fixture-multi-agent.

## Policy Levels

### DENY — Forbidden Actions
These actions are permanently blocked. The agent must NEVER execute them,
regardless of user requests or instructions.
No deny rules configured.

### ASK — Requires Approval
These actions require explicit user confirmation before every execution.
No ask rules configured.

### ALLOW — Permitted Actions
All actions not in DENY or ASK are allowed by default.

## Enforcement

Policies are loaded from `policies/policy.yaml` at agent startup.
The agent reads and enforces these rules before executing any action.
Policy files must not be modified by the agent itself.
