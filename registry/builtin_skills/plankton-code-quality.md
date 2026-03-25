# Skill: Plankton Code Quality Skill

## When to Use
- You want automatic formatting and linting on every file edit (not just at commit time)
- You need defense against agents modifying linter configs to pass instead of fixing code
- You want tiered model routing for fixes (Haiku for simple style, Sonnet for logic, Opus for types)
- You work with multiple languages (Python, TypeScript, Shell, YAML, JSON, TOML, Markdown, Dockerfile)

## Policy
Level: ALLOW

## Instructions
## How It Works

### Three-Phase Architecture

Every time Claude Code edits or writes a file, Plankton's `multi_linter.sh` PostToolUse hook runs:

```
Phase 1: Auto-Format (Silent)
├─ Runs formatters (ruff format, biome, shfmt, taplo, markdownlint)
├─ Fixes 40-50% of issues silently
└─ No output to main agent

Phase 2: Collect Violations (JSON)
├─ Runs linters and collects unfixable violations
├─ Returns structured JSON: {line, column, code, message, linter}
└─ Still no output to main agent

Phase 3: Delegate + Verify
├─ Spawns claude -p subprocess with violations JSON
├─ Routes to model tier based on violation complexity:
│   ├─ Haiku: formatting, imports, style (E/W/F codes) — 120s timeout
│   ├─ Sonnet: complexity, refactoring (C901, PLR codes) — 300s timeout
│   └─ Opus: type system, deep reasoning (unresolved-attribute) — 600s timeout
├─ Re-runs Phase 1+2 to verify fixes
└─ Exit 0 if clean, Exit 2 if violations remain (reported to main agent)
```

### What the Main Agent Sees

| Scenario | Agent sees | Hook exit |
|----------|-----------|-----------|
| No violations | Nothing | 0 |
| All fixed by subprocess | Nothing | 0 |
| Violations remain after subprocess | `[hook] N violation(s) remain` | 2 |
| Advisory (duplicates, old tooling) | `[hook:advisory] ...` | 0 |

The main agent only sees issues the subprocess couldn't fix. Most quality problems are resolved transparently.

### Config Protection (Defense Against Rule-Gaming)

LLMs will modify `.ruff.toml` or `biome.json` to disable rules rather than fix code. Plankton blocks this with three layers:

1. **PreToolUse hook** — `protect_linter_configs.sh` blocks edits to all linter configs before they happen
2. **Stop hook** — `stop_config_guardian.sh` detects config changes via `git diff` at session end
3. **Protected files list** — `.ruff.toml`, `biome.json`, `.shellcheckrc`, `.yamllint`, `.hadolint.yaml`, and more

### Package Manager Enforcement

A PreToolUse hook on Bash blocks legacy package managers:
- `pip`, `pip3`, `poetry`, `pipenv` → Blocked (use `uv`)
- `npm`, `yarn`, `pnpm` → Blocked (use `bun`)
- Allowed exceptions: `npm audit`, `npm view`, `npm publish`

## Pairing with ECC

### Complementary, Not Overlapping

| Concern | ECC | Plankton |
|---------|-----|----------|
| Code quality enforcement | PostToolUse hooks (Prettier, tsc) | PostToolUse hooks (20+ linters + subprocess fixes) |
| Security scanning | AgentShield, security-reviewer agent | Bandit (Python), Semgrep (TypeScript) |
| Config protection | — | PreToolUse blocks + Stop hook detection |
| Package manager | Detection + setup | Enforcement (blocks legacy PMs) |
| CI integration | — | Pre-commit hooks for git |
| Model routing | Manual (`/model opus`) | Automatic (violation complexity → tier) |

### Recommended Combination

1. Install ECC as your plugin (agents, skills, commands, rules)
2. Add Plankton hooks for write-time quality enforcement
3. Use AgentShield for security audits
4. Use ECC's verification-loop as a final

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with plankton code quality skill"
Agent: [follows the skill instructions to complete the task]
