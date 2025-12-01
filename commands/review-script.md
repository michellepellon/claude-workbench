Review a shell script for defensive patterns and best practices.

## Target

$ARGUMENTS

If no file specified, find shell scripts in current directory.

## Process

1. Run ShellCheck: `shellcheck "$file"`
2. Review against checklist below
3. Report issues with line numbers and fixes

## Checklist

### Safety
- [ ] Starts with `set -Eeuo pipefail`
- [ ] All variables quoted (`"$var"`)
- [ ] Trap for cleanup on EXIT
- [ ] Temp files use `mktemp`
- [ ] Uses `[[ ]]` not `[ ]` (bash)

### Robustness
- [ ] Arguments validated
- [ ] Required vars checked (`: "${VAR:?}"`)
- [ ] Dependencies verified (`command -v`)
- [ ] Exit codes checked

### Maintainability
- [ ] Functions use `local` variables
- [ ] Meaningful variable names
- [ ] Usage/help function exists
- [ ] No magic numbers

## Output

For each issue found:
```
[SEVERITY] file:line - Issue description
  Current:  <problematic code>
  Fix:      <corrected code>
```

Severities: ERROR (will fail), WARN (potential issue), INFO (style)
