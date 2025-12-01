Rename the current branch based on its changes.

## Process

1. Run `git diff main...HEAD --stat` to summarize changes
2. Analyze changes to determine appropriate branch name
3. Suggest name using format: `<type>/<description>` (e.g., `fix/auth-redirect`)
4. Rename: `git branch -m <new-name>`
5. If pushed to remote, update with:
   ```bash
   git push origin -u <new-name>
   git push origin --delete <old-name>
   ```

## Override

$ARGUMENTS

If a name is provided, use it instead of generating one.
