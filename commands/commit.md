Create a well-formatted commit for staged changes.

## Process

1. Run `git status` to check staged files
2. If nothing staged, run `git add -p` to interactively stage
3. Run `git diff --cached` to analyze changes
4. If multiple logical changes detected, suggest splitting into atomic commits
5. Create commit with conventional format: `<emoji> <type>: <description>`

## Commit Types

| Emoji | Type | Use for |
|-------|------|---------|
| ✨ | feat | New feature |
| 🐛 | fix | Bug fix |
| 📝 | docs | Documentation |
| 💄 | style | Formatting, no code change |
| ♻️ | refactor | Code restructuring |
| ⚡️ | perf | Performance |
| ✅ | test | Tests |
| 🔧 | chore | Config, tooling, deps |

## Guidelines

- **Atomic**: One logical change per commit
- **Present tense**: "add feature" not "added feature"
- **Concise**: First line under 72 characters
- **Split when**: mixing types, unrelated files, or large changes
