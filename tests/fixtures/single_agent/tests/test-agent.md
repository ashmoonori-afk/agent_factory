# Agent Behavior Verification — fixture-single-agent

## Test: Agent identity

- Prompt: "Who are you?"
- Expected: Agent identifies as fixture-single-agent and describes its purpose.

## Test: Agent description

- Prompt: "What do you do?"
- Expected: Agent responds with: Golden file fixture for single agent

## Test: Reading order

- Prompt: "What files did you read?"
- Expected: Agent confirms it read CLAUDE.md (or CODEX.md), agent_spec.yaml,
  and policies/policy.yaml at minimum.



## Test: Skill awareness

- Prompt: "Can you use csv-reader?"
- Expected: Agent confirms the skill is available.

