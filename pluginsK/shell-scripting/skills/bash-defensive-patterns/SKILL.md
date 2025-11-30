---
name: bash-defensive-patterns
description: Master defensive Bash programming techniques 위한 production-grade scripts. Use when writing 강력한 shell scripts, CI/CD pipelines, 또는 system utilities requiring fault tolerance 및 safety.
---

# Bash Defensive Patterns

포괄적인 guidance 위한 writing production-ready Bash scripts 사용하여 defensive programming techniques, error handling, 및 safety 모범 사례 에 prevent common pitfalls 및 ensure 신뢰성.

## When 에 Use This Skill

- Writing production 자동화 scripts
- Building CI/CD 파이프라인 scripts
- Creating system administration utilities
- Developing error-복원력 있는 배포 자동화
- Writing scripts that must handle edge cases safely
- Building 유지 관리 가능한 shell script libraries
- Implementing 포괄적인 logging 및 모니터링
- Creating scripts that must work 전반에 걸쳐 different platforms

## Core Defensive Principles

### 1. Strict Mode
Enable bash strict mode 에서 the start of every script 에 catch errors early.

```bash
#!/bin/bash
set -Eeuo pipefail  # Exit on error, unset variables, pipe failures
```

**Key flags:**
- `set -E`: Inherit ERR trap 에서 functions
- `set -e`: Exit 에 any error (command returns non-zero)
- `set -u`: Exit 에 undefined variable reference
- `set -o pipefail`: Pipe fails if any command fails (not just last)

### 2. Error Trapping 및 Cleanup
Implement proper cleanup 에 script exit 또는 error.

```bash
#!/bin/bash
set -Eeuo pipefail

trap 'echo "Error on line $LINENO"' ERR
trap 'echo "Cleaning up..."; rm -rf "$TMPDIR"' EXIT

TMPDIR=$(mktemp -d)
# Script code here
```

### 3. Variable Safety
Always quote variables 에 prevent word splitting 및 globbing issues.

```bash
# Wrong - unsafe
cp $source $dest

# Correct - safe
cp "$source" "$dest"

# Required variables - fail with message if unset
: "${REQUIRED_VAR:?REQUIRED_VAR is not set}"
```

### 4. Array Handling
Use arrays safely 위한 복잡한 data handling.

```bash
# Safe array iteration
declare -a items=("item 1" "item 2" "item 3")

for item in "${items[@]}"; do
    echo "Processing: $item"
done

# Reading output into array safely
mapfile -t lines < <(some_command)
readarray -t numbers < <(seq 1 10)
```

### 5. Conditional Safety
Use `[[ ]]` 위한 Bash-specific features, `[ ]` 위한 POSIX.

```bash
# Bash - safer
if [[ -f "$file" && -r "$file" ]]; then
    content=$(<"$file")
fi

# POSIX - portable
if [ -f "$file" ] && [ -r "$file" ]; then
    content=$(cat "$file")
fi

# Test for existence before operations
if [[ -z "${VAR:-}" ]]; then
    echo "VAR is not set or is empty"
fi
```

## Fundamental Patterns

### 패턴 1: Safe Script Directory Detection

```bash
#!/bin/bash
set -Eeuo pipefail

# Correctly determine script directory
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
SCRIPT_NAME="$(basename -- "${BASH_SOURCE[0]}")"

echo "Script location: $SCRIPT_DIR/$SCRIPT_NAME"
```

### 패턴 2: 포괄적인 Function Templat

```bash
#!/bin/bash
set -Eeuo pipefail

# Prefix for functions: handle_*, process_*, check_*, validate_*
# Include documentation and error handling

validate_file() {
    local -r file="$1"
    local -r message="${2:-File not found: $file}"

    if [[ ! -f "$file" ]]; then
        echo "ERROR: $message" >&2
        return 1
    fi
    return 0
}

process_files() {
    local -r input_dir="$1"
    local -r output_dir="$2"

    # Validate inputs
    [[ -d "$input_dir" ]] || { echo "ERROR: input_dir not a directory" >&2; return 1; }

    # Create output directory if needed
    mkdir -p "$output_dir" || { echo "ERROR: Cannot create output_dir" >&2; return 1; }

    # Process files safely
    while IFS= read -r -d '' file; do
        echo "Processing: $file"
        # Do work
    done < <(find "$input_dir" -maxdepth 1 -type f -print0)

    return 0
}
```

### 패턴 3: Safe Temporary File Handling

```bash
#!/bin/bash
set -Eeuo pipefail

trap 'rm -rf -- "$TMPDIR"' EXIT

# Create temporary directory
TMPDIR=$(mktemp -d) || { echo "ERROR: Failed to create temp directory" >&2; exit 1; }

# Create temporary files in directory
TMPFILE1="$TMPDIR/temp1.txt"
TMPFILE2="$TMPDIR/temp2.txt"

# Use temporary files
touch "$TMPFILE1" "$TMPFILE2"

echo "Temp files created in: $TMPDIR"
```

### 패턴 4: 강력한 Argument Parsing

```bash
#!/bin/bash
set -Eeuo pipefail

# Default values
VERBOSE=false
DRY_RUN=false
OUTPUT_FILE=""
THREADS=4

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
    -v, --verbose       Enable verbose output
    -d, --dry-run       Run without making changes
    -o, --output FILE   Output file path
    -j, --jobs NUM      Number of parallel jobs
    -h, --help          Show this help message
EOF
    exit "${1:-0}"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -j|--jobs)
            THREADS="$2"
            shift 2
            ;;
        -h|--help)
            usage 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            usage 1
            ;;
    esac
done

# Validate required arguments
[[ -n "$OUTPUT_FILE" ]] || { echo "ERROR: -o/--output is required" >&2; usage 1; }
```

### 패턴 5: Structured Logging

```bash
#!/bin/bash
set -Eeuo pipefail

# Logging functions
log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" >&2
}

log_warn() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARN: $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] DEBUG: $*" >&2
    fi
}

# Usage
log_info "Starting script"
log_debug "Debug information"
log_warn "Warning message"
log_error "Error occurred"
```

### 패턴 6: Process 오케스트레이션 와 함께 Signals

```bash
#!/bin/bash
set -Eeuo pipefail

# Track background processes
PIDS=()

cleanup() {
    log_info "Shutting down..."

    # Terminate all background processes
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    # Wait for graceful shutdown
    for pid in "${PIDS[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
}

trap cleanup SIGTERM SIGINT

# Start background tasks
background_task &
PIDS+=($!)

another_task &
PIDS+=($!)

# Wait for all background processes
wait
```

### 패턴 7: Safe File Operations

```bash
#!/bin/bash
set -Eeuo pipefail

# Use -i flag to move safely without overwriting
safe_move() {
    local -r source="$1"
    local -r dest="$2"

    if [[ ! -e "$source" ]]; then
        echo "ERROR: Source does not exist: $source" >&2
        return 1
    fi

    if [[ -e "$dest" ]]; then
        echo "ERROR: Destination already exists: $dest" >&2
        return 1
    fi

    mv "$source" "$dest"
}

# Safe directory cleanup
safe_rmdir() {
    local -r dir="$1"

    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Not a directory: $dir" >&2
        return 1
    fi

    # Use -I flag to prompt before rm (BSD/GNU compatible)
    rm -rI -- "$dir"
}

# Atomic file writes
atomic_write() {
    local -r target="$1"
    local -r tmpfile
    tmpfile=$(mktemp) || return 1

    # Write to temp file first
    cat > "$tmpfile"

    # Atomic rename
    mv "$tmpfile" "$target"
}
```

### 패턴 8: Idempotent Script 설계

```bash
#!/bin/bash
set -Eeuo pipefail

# Check if resource already exists
ensure_directory() {
    local -r dir="$1"

    if [[ -d "$dir" ]]; then
        log_info "Directory already exists: $dir"
        return 0
    fi

    mkdir -p "$dir" || {
        log_error "Failed to create directory: $dir"
        return 1
    }

    log_info "Created directory: $dir"
}

# Ensure configuration state
ensure_config() {
    local -r config_file="$1"
    local -r default_value="$2"

    if [[ ! -f "$config_file" ]]; then
        echo "$default_value" > "$config_file"
        log_info "Created config: $config_file"
    fi
}

# Rerunning script multiple times should be safe
ensure_directory "/var/cache/myapp"
ensure_config "/etc/myapp/config" "DEBUG=false"
```

### 패턴 9: Safe Command Substitution

```bash
#!/bin/bash
set -Eeuo pipefail

# Use $() instead of backticks
name=$(<"$file")  # Modern, safe variable assignment from file
output=$(command -v python3)  # Get command location safely

# Handle command substitution with error checking
result=$(command -v node) || {
    log_error "node command not found"
    return 1
}

# For multiple lines
mapfile -t lines < <(grep "pattern" "$file")

# NUL-safe iteration
while IFS= read -r -d '' file; do
    echo "Processing: $file"
done < <(find /path -type f -print0)
```

### 패턴 10: Dry-Run Support

```bash
#!/bin/bash
set -Eeuo pipefail

DRY_RUN="${DRY_RUN:-false}"

run_cmd() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] Would execute: $*"
        return 0
    fi

    "$@"
}

# Usage
run_cmd cp "$source" "$dest"
run_cmd rm "$file"
run_cmd chown "$owner" "$target"
```

## 고급 Defensive Techniques

### Named Parameters 패턴

```bash
#!/bin/bash
set -Eeuo pipefail

process_data() {
    local input_file=""
    local output_dir=""
    local format="json"

    # Parse named parameters
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --input=*)
                input_file="${1#*=}"
                ;;
            --output=*)
                output_dir="${1#*=}"
                ;;
            --format=*)
                format="${1#*=}"
                ;;
            *)
                echo "ERROR: Unknown parameter: $1" >&2
                return 1
                ;;
        esac
        shift
    done

    # Validate required parameters
    [[ -n "$input_file" ]] || { echo "ERROR: --input is required" >&2; return 1; }
    [[ -n "$output_dir" ]] || { echo "ERROR: --output is required" >&2; return 1; }
}
```

### Dependency Checking

```bash
#!/bin/bash
set -Eeuo pipefail

check_dependencies() {
    local -a missing_deps=()
    local -a required=("jq" "curl" "git")

    for cmd in "${required[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo "ERROR: Missing required commands: ${missing_deps[*]}" >&2
        return 1
    fi
}

check_dependencies
```

## 모범 사례 Summary

1. **Always use strict mode** - `set -Eeuo pipefail`
2. **Quote all variables** - `"$variable"` prevents word splitting
3. **Use [[ ]] conditionals** - More 강력한 than [ ]
4. **Implement error trapping** - Catch 및 handle errors gracefully
5. **Validate all inputs** - Check file existence, permissions, formats
6. **Use functions 위한 reusability** - Prefix 와 함께 meaningful names
7. **Implement structured logging** - Include timestamps 및 levels
8. **Support dry-run mode** - Allow users 에 preview changes
9. **Handle temporary files safely** - Use mktemp, cleanup 와 함께 trap
10. **설계 위한 idempotency** - Scripts should be safe 에 rerun
11. **Document requirements** - List dependencies 및 minimum versions
12. **Test error paths** - Ensure error handling works correctly
13. **Use `command -v`** - Safer than `which` 위한 checking executables
14. **Prefer printf over echo** - More predictable 전반에 걸쳐 systems

## Resources

- **Bash Strict Mode**: http://redsymbol.net/articles/unofficial-bash-strict-mode/
- **Google Shell Style Guide**: https://google.github.io/styleguide/shellguide.html
- **Defensive BASH Programming**: https://www.lifepipe.net/
