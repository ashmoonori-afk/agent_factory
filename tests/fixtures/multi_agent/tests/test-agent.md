# Agent Behavior Verification — fixture-multi-agent

## Test: Agent identity

- Prompt: "Who are you?"
- Expected: Agent identifies as fixture-multi-agent and describes its purpose.

## Test: Agent description

- Prompt: "What do you do?"
- Expected: Agent responds with: Golden file fixture for multi agent

## Test: Reading order

- Prompt: "What files did you read?"
- Expected: Agent confirms it read CLAUDE.md (or CODEX.md), agent_spec.yaml,
  and policies/policy.yaml at minimum.


## Test: Multi-agent orchestration

- Prompt: "How do you coordinate agents?"
- Expected: Agent describes the topology and orchestrator rules.

## Test: Agent roster

- Verify agent knows about reviewer (reviews code).
- Verify agent knows about fixer (fixes issues).

## Test: Skill awareness

- Prompt: "Can you use code-reviewer?"
- Expected: Agent confirms the skill is available.

