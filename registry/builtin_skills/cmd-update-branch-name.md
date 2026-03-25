# Skill: Update Branch Name

## When to Use
Use this skill when the user needs to update branch name.

## Policy
Level: ALLOW

## Instructions
# Update Branch Name

Follow these steps to update the current branch name:

1. Check differences between current branch and main branch HEAD using `git diff main...HEAD`
2. Analyze the changed files to understand what work is being done
3. Determine an appropriate descriptive branch name based on the changes
4. Update the current branch name using `git branch -m [new-branch-name]`
5. Verify the branch name was updated with `git branch`

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.

## Examples
User: "/update-branch-name"
Agent: [follows the skill instructions to complete the task]
