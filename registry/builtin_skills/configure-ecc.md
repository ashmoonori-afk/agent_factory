# Skill: Configure Everything Claude Code (ECC)

## When to Use
- User says "configure ecc", "install ecc", "setup everything claude code", or similar
- User wants to selectively install skills or rules from this project
- User wants to verify or fix an existing ECC installation
- User wants to optimize installed skills or rules for their project

## Policy
Level: ALLOW

## Instructions
## Step 0: Clone ECC Repository

Before any installation, clone the latest ECC source to `/tmp`:

```bash
rm -rf /tmp/everything-claude-code
git clone https://github.com/affaan-m/everything-claude-code.git /tmp/everything-claude-code
```

Set `ECC_ROOT=/tmp/everything-claude-code` as the source for all subsequent copy operations.

If the clone fails (network issues, etc.), use `AskUserQuestion` to ask the user to provide a local path to an existing ECC clone.

---

## Step 1: Choose Installation Level

Use `AskUserQuestion` to ask the user where to install:

```
Question: "Where should ECC components be installed?"
Options:
  - "User-level (~/.claude/)" — "Applies to all your Claude Code projects"
  - "Project-level (.claude/)" — "Applies only to the current project"
  - "Both" — "Common/shared items user-level, project-specific items project-level"
```

Store the choice as `INSTALL_LEVEL`. Set the target directory:
- User-level: `TARGET=~/.claude`
- Project-level: `TARGET=.claude` (relative to current project root)
- Both: `TARGET_USER=~/.claude`, `TARGET_PROJECT=.claude`

Create the target directories if they don't exist:
```bash
mkdir -p $TARGET/skills $TARGET/rules
```

---

## Step 2: Select & Install Skills

### 2a: Choose Scope (Core vs Niche)

Default to **Core (recommended for new users)** — copy `.agents/skills/*` plus `skills/search-first/` for research-first workflows. This bundle covers engineering, evals, verification, security, strategic compaction, frontend design, and Anthropic cross-functional skills (article-writing, content-engine, market-research, frontend-slides).

Use `AskUserQuestion` (single select):
```
Question: "Install core skills only, or include niche/framework packs?"
Options:
  - "Core only (recommended)" — "tdd, e2e, evals, verification, research-first, security, frontend patterns, compacting, cross-functional Anthropic skills"
  - "Core + selected niche" — "Add framework/domain-specific skills after core"
  - "Niche only" — "Skip core, install specific framework/domain skills"
Default: Core only
```

If the user chooses niche or core + niche, continue to category selection below and only include those niche skills they pick.

### 2b: Choose Skill Categories

There are 7 selectable category groups below. The detailed confirmation lists that follow cover 45 skills across 8 categories, plus 1 standalone template. Use `AskUserQuestion` with `multiSelect: true`:

```
Question: "Which skill categories do you want to install?"
Options:
  - "Framework & Language" — "Django, Laravel, Spring Boot, Go, Python, Java, Frontend, Backend patterns"
  - "Database" — "PostgreSQL, ClickHouse, JPA/Hibernate patterns"
  - "Workflow & Quality" — "TDD, verification, learning, security review, compaction"
  - "Research & APIs" — "Deep research, Exa search, Claude API patterns"
  - "Social & Content Distribution" — "X/Twitter API, crossposting alongside content-engine"
  - "Media Generation" — "fal.ai image/video/audio alongside VideoDB

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with configure everything claude code (ecc)"
Agent: [follows the skill instructions to complete the task]
