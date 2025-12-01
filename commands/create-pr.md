Create a pull request for the current branch.

## Process

1. Run `git status` to verify branch and changes
2. Run `git log main..HEAD --oneline` to summarize commits
3. Generate PR title using conventional format: `<emoji>(<scope>): <description>`
4. Generate PR body with:
   - Summary of changes
   - Test plan
   - Related issues (if any)
5. Create draft PR: `gh pr create --draft --title "..." --body "..."`

## PR Title Format

| Emoji | Type |
|-------|------|
| ✨ | feat |
| 🐛 | fix |
| 📝 | docs |
| ♻️ | refactor |
| ✅ | test |
| 🔧 | chore |

## Useful Follow-ups

```bash
gh pr ready           # Mark ready for review
gh pr edit --add-reviewer <user>
gh pr merge --squash
```
