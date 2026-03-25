# Skill: Claude DevFleet Multi-Agent Orchestration

## When to Use
Use this skill when you need to dispatch multiple Claude Code agents to work on coding tasks in parallel. Each agent runs in an isolated git worktree with full tooling.

Requires a running Claude DevFleet instance connected via MCP:
```bash
claude mcp add devfleet --transport http http://localhost:18801/mcp
```

## Policy
Level: ALLOW

## Instructions
## How It Works

```
User → "Build a REST API with auth and tests"
  ↓
plan_project(prompt) → project_id + mission DAG
  ↓
Show plan to user → get approval
  ↓
dispatch_mission(M1) → Agent 1 spawns in worktree
  ↓
M1 completes → auto-merge → auto-dispatch M2 (depends_on M1)
  ↓
M2 completes → auto-merge
  ↓
get_report(M2) → files_changed, what_done, errors, next_steps
  ↓
Report back to user
```

### Tools

| Tool | Purpose |
|------|---------|
| `plan_project(prompt)` | AI breaks a description into a project with chained missions |
| `create_project(name, path?, description?)` | Create a project manually, returns `project_id` |
| `create_mission(project_id, title, prompt, depends_on?, auto_dispatch?)` | Add a mission. `depends_on` is a list of mission ID strings (e.g., `["abc-123"]`). Set `auto_dispatch=true` to auto-start when deps are met. |
| `dispatch_mission(mission_id, model?, max_turns?)` | Start an agent on a mission |
| `cancel_mission(mission_id)` | Stop a running agent |
| `wait_for_mission(mission_id, timeout_seconds?)` | Block until a mission completes (see note below) |
| `get_mission_status(mission_id)` | Check mission progress without blocking |
| `get_report(mission_id)` | Read structured report (files changed, tested, errors, next steps) |
| `get_dashboard()` | System overview: running agents, stats, recent activity |
| `list_projects()` | Browse all projects |
| `list_missions(project_id, status?)` | List missions in a project |

> **Note on `wait_for_mission`:** This blocks the conversation for up to `timeout_seconds` (default 600). For long-running missions, prefer polling with `get_mission_status` every 30–60 seconds instead, so the user sees progress updates.

### Workflow: Plan → Dispatch → Monitor → Report

1. **Plan**: Call `plan_project(prompt="...")` → returns `project_id` + list of missions with `depends_on` chains and `auto_dispatch=true`.
2. **Show plan**: Present mission titles, types, and dependency chain to the user.
3. **Dispatch**: Call `dispatch_mission(mission_id=<first_mission_id>)` on the root mission (empty `depends_on`). Remaining missions auto-dispatch as their dependencies complete (because `plan_project` sets `auto_dispatch=true` on them).
4. **Monitor**: Call `get_mission_status(mission_id=...)` or `get_dashboard()` to check progress.
5. **Report**: Call `get_report(mission_id=...)` when missions complete. Share highlights with the user.

### Concurrency

DevFleet runs up to 3 concurrent agents by default (configurable via `DEVFLEET_MAX_AGENTS`). When all slots are full, missions with `auto_dispatch=true` queue in the mission watcher and dispatch automatically as slots free up. Check `get_dashboard()` for current slot usage.

## Examples

### Full auto: plan and launch

1. `plan_project(prompt="...")` → shows plan with missions and dependencies.
2. Dispatch the first mission (the one with empty `depends_on`).
3. Remaining missions auto-dispatch as dependencies resolve (they have `auto_dispatch=true`)

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with claude devfleet multi-agent orchestration"
Agent: [follows the skill instructions to complete the task]
