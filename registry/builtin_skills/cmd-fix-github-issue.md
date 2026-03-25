# Skill: Fix Github Issue

## When to Use
Use this skill when the user needs to fix github issue.

## Policy
Level: ALLOW

## Instructions
Please analyze and fix the GitHub issue: $ARGUMENTS.

Follow these steps:

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message

Remember to use the GitHub CLI (`gh`) for all GitHub-related tasks.

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.

## Examples
User: "/fix-github-issue"
Agent: [follows the skill instructions to complete the task]
