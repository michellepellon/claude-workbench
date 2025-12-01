---
name: workbench:shell-scripting
description: Write production-grade Bash scripts with defensive patterns, proper error handling, and testability. Use when writing automation, CI/CD pipelines, or system utilities.
when_to_use: When writing shell scripts. When reviewing bash code. When debugging script failures. When setting up CI/CD pipelines. When script needs to be robust and maintainable.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash
---

# Shell Scripting

**Announce at start:** "I'm using the shell-scripting skill for defensive bash patterns."

## Overview

Write production-grade shell scripts that fail safely and are easy to maintain.

**Core principle:** Scripts should fail loudly and early, never silently corrupt data.

## Script Template

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

trap 'echo "Error on line $LINENO" >&2' ERR
trap 'cleanup' EXIT

cleanup() {
    rm -rf -- "${TMPDIR:-}"
}

main() {
    TMPDIR=$(mktemp -d)
    # Script logic here
}

main "$@"
```

## Strict Mode

**Always start with:**
```bash
set -Eeuo pipefail
```

| Flag | Effect |
|------|--------|
| `-E` | ERR trap inherited by functions |
| `-e` | Exit on any error |
| `-u` | Exit on undefined variable |
| `-o pipefail` | Pipe fails if any command fails |

## Quick Reference

| Pattern | Bad | Good |
|---------|-----|------|
| Variables | `$var` | `"$var"` |
| Conditionals | `[ ]` | `[[ ]]` (bash) |
| Command check | `which cmd` | `command -v cmd` |
| Read lines | `for f in $(cat)` | `while IFS= read -r` |
| Temp files | `touch /tmp/x` | `mktemp` |
| Required var | `if [ -z "$X" ]` | `: "${X:?required}"` |

## Defensive Patterns

### Variable Safety

```bash
# Always quote
cp "$source" "$dest"

# Required variable with message
: "${API_KEY:?API_KEY is required}"

# Default value
output="${OUTPUT_FILE:-/dev/stdout}"

# Local variables in functions
my_func() {
    local -r input="$1"
    local result
}
```

### Safe Iteration

```bash
# Files with spaces/special chars
while IFS= read -r -d '' file; do
    echo "Processing: $file"
done < <(find . -type f -print0)

# Array iteration
declare -a items=("item 1" "item 2")
for item in "${items[@]}"; do
    process "$item"
done
```

### Argument Parsing

```bash
usage() {
    cat <<EOF
Usage: $0 [OPTIONS] <input>

Options:
    -v, --verbose    Verbose output
    -o, --output F   Output file
    -h, --help       Show help
EOF
    exit "${1:-0}"
}

VERBOSE=false
OUTPUT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose) VERBOSE=true; shift ;;
        -o|--output)  OUTPUT="$2"; shift 2 ;;
        -h|--help)    usage 0 ;;
        --)           shift; break ;;
        -*)           echo "Unknown: $1" >&2; usage 1 ;;
        *)            break ;;
    esac
done

[[ $# -ge 1 ]] || { echo "Missing input" >&2; usage 1; }
INPUT="$1"
```

### Cleanup and Traps

```bash
TMPDIR=""
cleanup() {
    [[ -n "$TMPDIR" ]] && rm -rf -- "$TMPDIR"
}
trap cleanup EXIT

TMPDIR=$(mktemp -d)
```

### Dependency Checking

```bash
check_deps() {
    local -a missing=()
    for cmd in jq curl git; do
        command -v "$cmd" &>/dev/null || missing+=("$cmd")
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Missing: ${missing[*]}" >&2
        return 1
    fi
}
```

### Logging

```bash
log_info()  { echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" >&2; }
log_warn()  { echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARN: $*" >&2; }
log_error() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2; }
```

### Dry-Run Support

```bash
DRY_RUN="${DRY_RUN:-false}"

run_cmd() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] $*" >&2
        return 0
    fi
    "$@"
}

run_cmd rm -rf "$target"
```

## ShellCheck

Always run ShellCheck before committing:

```bash
shellcheck script.sh
```

**Common fixes:**

```bash
# SC2086: Quote variables
rm $file        # Bad
rm "$file"      # Good

# SC2181: Check directly
cmd; if [ $? -eq 0 ]   # Bad
if cmd; then           # Good

# SC2015: Use if/else
[[ -f x ]] && echo y || echo n  # Unclear
if [[ -f x ]]; then echo y; else echo n; fi  # Clear
```

**Suppress when needed:**
```bash
# shellcheck disable=SC2086
cmd $unquoted_intentionally
```

## Testing with Bats

```bash
# test_script.bats
#!/usr/bin/env bats

setup() {
    TMPDIR=$(mktemp -d)
    source "${BATS_TEST_DIRNAME}/../script.sh"
}

teardown() {
    rm -rf "$TMPDIR"
}

@test "returns 0 on valid input" {
    run my_function "valid"
    [ "$status" -eq 0 ]
}

@test "fails on missing arg" {
    run my_function
    [ "$status" -ne 0 ]
    [[ "$output" == *"required"* ]]
}
```

Run: `bats tests/*.bats`

## Checklist

Before committing scripts:

- [ ] Starts with `set -Eeuo pipefail`
- [ ] All variables quoted
- [ ] Trap for cleanup on EXIT
- [ ] ShellCheck passes
- [ ] Arguments validated
- [ ] Dependencies checked
- [ ] Temp files use mktemp
