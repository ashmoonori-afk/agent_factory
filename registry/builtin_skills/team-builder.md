# Skill: Team Builder

## When to Use
- You have multiple agent personas (markdown files) and want to pick which ones to use for a task
- You want to compose an ad-hoc team from different domains (e.g., Security + SEO + Architecture)
- You want to browse what agents are available before deciding

## Policy
Level: ASK

## Instructions
## Configuration

Agent directories are probed in order and results are merged:

1. `./agents/**/*.md` + `./agents/*.md` — project-local agents (both depths)
2. `~/.claude/agents/**/*.md` + `~/.claude/agents/*.md` — global agents (both depths)

Results from all locations are merged and deduplicated by agent name. Project-local agents take precedence over global agents with the same name. A custom path can be used instead if the user specifies one.

## How It Works

### Step 1: Discover Available Agents

Glob agent directories using the probe order above. Exclude README files. For each file found:
- **Subdirectory layout:** extract the domain from the parent folder name
- **Flat layout:** collect all filename prefixes (text before the first `-`). A prefix qualifies as a domain only if it appears in 2 or more filenames (e.g., `engineering-security-engineer.md` and `engineering-software-architect.md` both start with `engineering` → Engineering domain). Files with unique prefixes (e.g., `code-reviewer.md`, `tdd-guide.md`) are grouped under "General"
- Extract the agent name from the first `# Heading`. If no heading is found, derive the name from the filename (strip `.md`, replace hyphens with spaces, title-case)
- Extract a one-line summary from the first paragraph after the heading

If no agent files are found after probing all locations, inform the user: "No agent files found. Checked: [list paths probed]. Expected: markdown files in one of those directories." Then stop.

### Step 2: Present Domain Menu

```
Available agent domains:
1. Engineering — Software Architect, Security Engineer
2. Marketing — SEO Specialist
3. Sales — Discovery Coach, Outbound Strategist

Pick domains or name specific agents (e.g., "1,3" or "security + seo"):
```

- Skip domains with zero agents (empty directories)
- Show agent count per domain

### Step 3: Handle Selection

Accept flexible input:
- Numbers: "1,3" selects all agents from Engineering and Sales
- Names: "security + seo" fuzzy-matches against discovered agents
- "all from engineering" selects every agent in that domain

If more than 5 agents are selected, list them alphabetically and ask the user to narrow down: "You selected N agents (max 5). Pick which to keep, or say 'first 5' to use the first five alphabetically."

Confirm selection:
```
Selected: Security Engineer + SEO Specialist
What should they work on? (describe the task):
```

### Step 4: Spawn Agents in Parallel

1. Read each selected agent's markdown file
2. Prompt for the task description if not already provided
3. Spawn all agents in parallel using the Agent tool:
   - `subagent_type: "general-purpose"`
   - `prompt: "{agent file content}\n\nTask: {task description}"`
   - Each agent runs independently — no inter-agent communication needed
4. If an agent fails (error, timeout, or empty output), note the failure inline (e.g., "Security Engineer: failed — [reason]") and continue with results from agents that succeeded

### Step 5: Synthesize Resul

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with team builder"
Agent: [follows the skill instructions to complete the task]
