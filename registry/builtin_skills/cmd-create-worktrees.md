# Skill: Git Worktree Commands

## When to Use
Use this skill when the user needs to create worktrees.

## Policy
Level: ASK

## Instructions
# Git Worktree Commands

## Create Worktrees for All Open PRs

This command fetches all open pull requests using GitHub CLI, then creates a git worktree for each PR's branch in the `./tree/<BRANCH_NAME>` directory.

```bash
# Ensure GitHub CLI is installed and authenticated
gh auth status || (echo "Please run 'gh auth login' first" && exit 1)

# Create the tree directory if it doesn't exist
mkdir -p ./tree

# List all open PRs and create worktrees for each branch
gh pr list --json headRefName --jq '.[].headRefName' | while read branch; do
  # Handle branch names with slashes (like "feature/foo")
  branch_path="./tree/${branch}"
  
  # For branches with slashes, create the directory structure
  if [[ "$branch" == */* ]]; then
    dir_path=$(dirname "$branch_path")
    mkdir -p "$dir_path"
  fi

  # Check if worktree already exists
  if [ ! -d "$branch_path" ]; then
    echo "Creating worktree for $branch"
    git worktree add "$branch_path" "$branch"
  else
    echo "Worktree for $branch already exists"
  fi
done

# Display all created worktrees
echo "\nWorktree list:"
git worktree list
```

### Example Output

```
Creating worktree for fix-bug-123
HEAD is now at a1b2c3d Fix bug 123
Creating worktree for feature/new-feature
HEAD is now at e4f5g6h Add new feature
Worktree for documentation-update already exists

Worktree list:
/path/to/repo                      abc1234 [main]
/path/to/repo/tree/fix-bug-123     a1b2c3d [fix-bug-123]
/path/to/repo/tree/feature/new-feature e4f5g6h [feature/new-feature]
/path/to/repo/tree/documentation-update d5e6f7g [documentation-update]
```

### Cleanup Stale Worktrees (Optional)

You can add this to remove stale worktrees for branches that no longer exist:

```bash
# Get current branches
current_branches=$(git branch -a | grep -v HEAD | grep -v main | sed 's/^[ *]*//' | sed 's|remotes/origin/||' | sort | uniq)

# Get existing worktrees (excluding main worktree)
worktree_paths=$(git worktree list | tail -n +2 | awk '{print $1}')

for path in $worktree_paths; do
  # Extract branch name from path
  branch_name=$(basename "$path")
  
  # Skip special cases
  if [[ "$branch_name" == "main" ]]; then
    continue
  fi
  
  # Check if branch still exists
  if ! echo "$current_branches" | grep -q "^$branch_name$"; then
    echo "Removing stale worktree for deleted branch: $branch_name"
    git worktree remove --force "$path"
  fi
done
```

## Create New Branch and Worktree

This interactive command creates a new git branch and sets up a worktree for it:

```bash
#!/bin/bash

# Ensure we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Error: Not in a git repository"
  exit 1
fi

# Get the repository root
repo_root=$(git rev-parse --show-toplevel)

# Prompt for branch name
read -p "Enter new branch name: " branch_name

# Validate branch name (basic validation)
if [[ -z "$branch_name" ]]; then
  echo "Error: Branch name cannot be empty"
  exit 1
fi

if git show-ref --verify --quie

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.

## Examples
User: "/create-worktrees"
Agent: [follows the skill instructions to complete the task]
