Create a git worktree for isolated development.

## Usage

$ARGUMENTS

- If argument is a PR number: create worktree for that PR's branch
- If argument is a branch name: create worktree for that branch
- If no argument: list existing worktrees

## Process

1. Create `./tree/` directory if needed
2. For PR number: `gh pr view $ARGUMENTS --json headRefName -q .headRefName` to get branch name
3. Create worktree: `git worktree add ./tree/<branch> <branch>`
4. Report the path for the user to `cd` into

## Common Operations

```bash
git worktree list              # List all worktrees
git worktree remove ./tree/x   # Remove a worktree
git worktree prune             # Clean up stale references
```

## Notes

- Worktrees share the same `.git` directory (disk efficient)
- Each worktree can have different branches checked out simultaneously
- Delete the directory and run `git worktree prune` to clean up
