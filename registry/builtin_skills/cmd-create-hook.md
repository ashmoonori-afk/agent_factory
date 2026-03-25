# Skill: Create Hook Command

## When to Use
Use this skill when the user needs to create hook.

## Policy
Level: ALLOW

## Instructions
# Create Hook Command

Analyze the project, suggest practical hooks, and create them with proper testing.

## Your Task (/create-hook)

1. **Analyze environment** - Detect tooling and existing hooks
2. **Suggest hooks** - Based on your project configuration
3. **Configure hook** - Ask targeted questions and create the script
4. **Test & validate** - Ensure the hook works correctly

## Your Workflow

### 1. Environment Analysis & Suggestions

Automatically detect the project tooling and suggest relevant hooks:

**When TypeScript is detected (`tsconfig.json`):**

- PostToolUse hook: "Type-check files after editing"
- PreToolUse hook: "Block edits with type errors"

**When Prettier is detected (`.prettierrc`, `prettier.config.js`):**

- PostToolUse hook: "Auto-format files after editing"
- PreToolUse hook: "Require formatted code"

**When ESLint is detected (`.eslintrc.*`):**

- PostToolUse hook: "Lint and auto-fix after editing"
- PreToolUse hook: "Block commits with linting errors"

**When package.json has scripts:**

- `test` script → "Run tests before commits"
- `build` script → "Validate build before commits"

**When a git repository is detected:**

- PreToolUse/Bash hook: "Prevent commits with secrets"
- PostToolUse hook: "Security scan on file changes"

**Decision Tree:**

```
Project has TypeScript? → Suggest type checking hooks
Project has formatter? → Suggest formatting hooks
Project has tests? → Suggest test validation hooks
Security sensitive? → Suggest security hooks
+ Scan for additional patterns and suggest custom hooks based on:
  - Custom scripts in package.json
  - Unique file patterns or extensions
  - Development workflow indicators
  - Project-specific tooling configurations
```

### 2. Hook Configuration

Start by asking: **"What should this hook do?"** and offer relevant suggestions from your analysis.

Then understand the context from the user's description and **only ask about details you're unsure about**:

1. **Trigger timing**: When should it run?
   - `PreToolUse`: Before file operations (can block)
   - `PostToolUse`: After file operations (feedback/fixes)
   - `UserPromptSubmit`: Before processing requests
   - Other event types as needed

2. **Tool matcher**: Which tools should trigger it? (`Write`, `Edit`, `Bash`, `*` etc)

3. **Scope**: `global`, `project`, or `project-local`

4. **Response approach**:
   - **Exit codes only**: Simple (exit 0 = success, exit 2 = block in PreToolUse)
   - **JSON response**: Advanced control (blocking, context, decisions)
   - Guide based on complexity: simple pass/fail → exit codes, rich feedback → JSON

5. **Blocking behavior** (if relevant): "Should this stop operations when issues are found?"
   - PreToolUse: Can block operations (security, validation)
   - PostToolUse: Usually provide feedback only

6. **Claude integration** (CRITICAL): "Should Claude Code automatically see and fix issues this hook detects?"
   - If YES: Use `additionalContext` for error communication
   - If NO:

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.

## Examples
User: "/create-hook"
Agent: [follows the skill instructions to complete the task]
