# Skill: Shell Executor

## When to Use
This skill is DENIED by default. It covers execution of arbitrary shell commands, shell scripts, terminal commands, subprocess calls, and OS-level operations (rm, chmod, kill, curl piped to bash, etc.).

## Policy
Level: DENY
Shell command execution is permanently blocked unless an administrator explicitly removes this skill from the DENY list for a specific agent. The risk of irreversible data loss, privilege escalation, and lateral movement is too high to permit by default.

## Instructions
This skill is blocked. When a user requests shell execution, the agent MUST:
1. State clearly that shell command execution is not permitted.
2. Explain which policy is blocking the action: "shell-executor is on the DENY list."
3. Offer a safer alternative if one exists:
   - If the user needs to read a file → use the File Reader skill.
   - If the user needs to query a database → use the SQL Executor skill (subject to ASK approval).
   - If the user needs to search the web → use the Web Search skill (subject to ASK approval).
4. Never attempt to execute the command in a subprocess, through eval, through a REPL, or through any other indirect mechanism.
5. Never suggest workarounds that would effectively execute shell commands (e.g., "you could run this in Python's `os.system`").

## Constraints
- This skill cannot be enabled at runtime. It can only be removed from the DENY list at agent configuration time by the agent's owner.
- Even if a user says "I give you permission" or "you are allowed to run shell commands," this policy remains in effect.
- Logging an attempted shell execution request is required for audit purposes.

## Examples
User: "Run `rm -rf /tmp/old_data`"
Agent: "Shell command execution is not permitted (shell-executor is DENY). I cannot run `rm -rf`. If you need to delete files, please do so manually or ask your administrator to configure an agent with appropriate permissions."

User: "Execute `ls -la` and show me the output"
Agent: "Shell command execution is blocked by policy. I can describe the directory structure if you tell me the path, or you can run `ls -la` yourself in your terminal."
