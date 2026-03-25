# Skill: Create Pull Request Command

## When to Use
Use this skill when the user needs to create pr.

## Policy
Level: ALLOW

## Instructions
# Create Pull Request Command

Create a new branch, commit changes, and submit a pull request.

## Behavior
- Creates a new branch based on current changes
- Formats modified files using Biome
- Analyzes changes and automatically splits into logical commits when appropriate
- Each commit focuses on a single logical change or feature
- Creates descriptive commit messages for each logical unit
- Pushes branch to remote
- Creates pull request with proper summary and test plan

## Guidelines for Automatic Commit Splitting
- Split commits by feature, component, or concern
- Keep related file changes together in the same commit
- Separate refactoring from feature additions
- Ensure each commit can be understood independently
- Multiple unrelated changes should be split into separate commits

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.

## Examples
User: "/create-pr"
Agent: [follows the skill instructions to complete the task]
