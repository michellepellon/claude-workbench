# Shell Scripting Patterns Reference

Extended patterns for production shell scripts.

## Process Management

### Background Tasks with Cleanup

```bash
PIDS=()

cleanup() {
    for pid in "${PIDS[@]}"; do
        kill -TERM "$pid" 2>/dev/null || true
    done
    wait
}
trap cleanup SIGTERM SIGINT EXIT

start_task &
PIDS+=($!)

another_task &
PIDS+=($!)

wait
```

### Timeout for Commands

```bash
# Timeout after 30 seconds
timeout 30s long_running_command || {
    echo "Command timed out" >&2
    exit 1
}
```

### Retry Logic

```bash
retry() {
    local -r max_attempts="${1:-3}"
    local -r delay="${2:-5}"
    shift 2
    local attempt=1

    until "$@"; do
        if ((attempt >= max_attempts)); then
            echo "Failed after $attempt attempts" >&2
            return 1
        fi
        echo "Attempt $attempt failed, retrying in ${delay}s..." >&2
        sleep "$delay"
        ((attempt++))
    done
}

retry 3 5 curl -f https://example.com/api
```

## File Operations

### Atomic Write

```bash
atomic_write() {
    local -r target="$1"
    local tmpfile
    tmpfile=$(mktemp) || return 1

    cat > "$tmpfile"
    mv "$tmpfile" "$target"
}

echo "content" | atomic_write /etc/config
```

### Safe File Processing

```bash
# Process files with special characters
process_files() {
    local -r dir="$1"

    while IFS= read -r -d '' file; do
        echo "Processing: $file"
    done < <(find "$dir" -type f -name "*.txt" -print0)
}
```

### Lock File

```bash
LOCKFILE="/var/run/myscript.lock"

acquire_lock() {
    exec 200>"$LOCKFILE"
    flock -n 200 || {
        echo "Another instance is running" >&2
        exit 1
    }
}

acquire_lock
# Script continues...
```

## Input/Output

### Read Config File

```bash
# config format: KEY=value
load_config() {
    local -r config_file="$1"

    [[ -f "$config_file" ]] || return 1

    while IFS='=' read -r key value; do
        [[ "$key" =~ ^[[:space:]]*# ]] && continue  # Skip comments
        [[ -z "$key" ]] && continue                  # Skip empty
        export "$key"="$value"
    done < "$config_file"
}
```

### Parse JSON with jq

```bash
parse_response() {
    local -r json="$1"

    local status name
    status=$(echo "$json" | jq -r '.status // empty')
    name=$(echo "$json" | jq -r '.data.name // empty')

    [[ -n "$status" ]] || return 1
    echo "Status: $status, Name: $name"
}
```

### Here Documents

```bash
# Variable expansion
cat <<EOF
Hello $USER
Today is $(date)
EOF

# No expansion (quoted delimiter)
cat <<'EOF'
Literal $USER and $(date)
EOF

# Indented (tabs stripped with <<-)
	cat <<-EOF
	Indented content
	EOF
```

## Platform Compatibility

### Detect OS

```bash
case "$(uname -s)" in
    Linux*)  OS=linux ;;
    Darwin*) OS=macos ;;
    *)       OS=unknown ;;
esac

# BSD vs GNU sed
if [[ "$OS" == "macos" ]]; then
    sed -i '' 's/old/new/' file
else
    sed -i 's/old/new/' file
fi
```

### Check Bash Version

```bash
require_bash_version() {
    local -r required="$1"
    local -r current="${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}"

    if [[ "$(printf '%s\n' "$required" "$current" | sort -V | head -n1)" != "$required" ]]; then
        echo "Requires bash >= $required (have $current)" >&2
        exit 1
    fi
}

require_bash_version 4.4
```

## Idempotent Operations

```bash
ensure_directory() {
    local -r dir="$1"
    [[ -d "$dir" ]] && return 0
    mkdir -p "$dir"
}

ensure_line_in_file() {
    local -r line="$1"
    local -r file="$2"

    grep -qF "$line" "$file" 2>/dev/null || echo "$line" >> "$file"
}

ensure_symlink() {
    local -r target="$1"
    local -r link="$2"

    [[ -L "$link" && "$(readlink "$link")" == "$target" ]] && return 0
    ln -sf "$target" "$link"
}
```

## Arrays

### Associative Arrays (Bash 4+)

```bash
declare -A config
config[host]="localhost"
config[port]="8080"

for key in "${!config[@]}"; do
    echo "$key = ${config[$key]}"
done
```

### Array from Command Output

```bash
mapfile -t lines < <(grep "pattern" file.txt)

for line in "${lines[@]}"; do
    echo "Line: $line"
done
```

## Common ShellCheck Codes

| Code | Issue | Fix |
|------|-------|-----|
| SC2086 | Unquoted variable | Quote: `"$var"` |
| SC2181 | Check `$?` | Use: `if cmd; then` |
| SC2015 | `&&`/`||` confusion | Use `if/else` |
| SC2046 | Unquoted command sub | Quote: `"$(cmd)"` |
| SC2034 | Unused variable | Remove or export |
| SC2155 | Declare and assign | Separate: `local x; x=$(cmd)` |
| SC2164 | `cd` without `||` | Add: `cd dir || exit` |

## Bats Testing Patterns

### Mock External Commands

```bash
setup() {
    STUBS="$TMPDIR/stubs"
    mkdir -p "$STUBS"
    export PATH="$STUBS:$PATH"
}

stub_command() {
    local -r cmd="$1" output="$2" code="${3:-0}"
    cat > "$STUBS/$cmd" <<EOF
#!/bin/bash
echo "$output"
exit $code
EOF
    chmod +x "$STUBS/$cmd"
}

@test "handles API failure" {
    stub_command curl "Connection refused" 1
    run my_api_function
    [ "$status" -ne 0 ]
}
```

### Test File Operations

```bash
@test "creates output file" {
    run my_function "$TMPDIR/input.txt" "$TMPDIR/output.txt"
    [ "$status" -eq 0 ]
    [ -f "$TMPDIR/output.txt" ]
}

@test "output matches expected" {
    my_function "$FIXTURES/input.txt" "$TMPDIR/output.txt"
    diff "$TMPDIR/output.txt" "$FIXTURES/expected.txt"
}
```
