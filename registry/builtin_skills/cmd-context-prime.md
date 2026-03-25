# Skill: Context Prime

## When to Use
Use this skill when the user needs to context prime.

## Policy
Level: ALLOW

## Instructions
Read README.md, THEN run `git ls-files | grep -v -f (sed 's|^|^|; s|$|/|' .cursorignore | psub)` to understand the context of the project

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.

## Examples
User: "/context-prime"
Agent: [follows the skill instructions to complete the task]
