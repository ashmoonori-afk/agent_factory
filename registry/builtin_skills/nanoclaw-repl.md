# Skill: NanoClaw REPL

## When to Use
Operate and extend NanoClaw v2, ECC's zero-dependency session-aware REPL built on claude -p.

## Policy
Level: ALLOW

## Instructions
## Capabilities

- persistent markdown-backed sessions
- model switching with `/model`
- dynamic skill loading with `/load`
- session branching with `/branch`
- cross-session search with `/search`
- history compaction with `/compact`
- export to md/json/txt with `/export`
- session metrics with `/metrics`

## Operating Guidance

1. Keep sessions task-focused.
2. Branch before high-risk changes.
3. Compact after major milestones.
4. Export before sharing or archival.

## Extension Rules

- keep zero external runtime dependencies
- preserve markdown-as-database compatibility
- keep command handlers deterministic and local

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with nanoclaw repl"
Agent: [follows the skill instructions to complete the task]
