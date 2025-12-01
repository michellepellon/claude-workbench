---
name: workbench:semantic-refactoring
description: Perform safe, codebase-wide refactoring using semantic code understanding. Leverages Serena MCP tools when available for symbol-level operations.
when_to_use: When renaming symbols across files. When moving functions/classes. When refactoring requires understanding all references. When grep-based search is insufficient.
version: 1.0.0
allowed-tools: Read, Edit, Grep, Glob, Bash, mcp__serena__*
---

# Semantic Refactoring

Refactor code safely using semantic understanding rather than text search.

**Announce at start:** "I'm using the semantic-refactoring skill to safely refactor across the codebase."

## Prerequisites

This skill works best with Serena MCP server installed. See `mcp-servers/serena.md` for setup.

Without Serena, falls back to grep-based search (less accurate for overloaded names).

## Quick Reference

| Task | With Serena | Without Serena |
|------|-------------|----------------|
| Find all uses | `find_referencing_symbols` | `Grep` + manual filtering |
| Rename symbol | `rename_symbol` | `Edit` each file |
| Understand structure | `get_symbols_overview` | `Read` + parse |

## Process

### 1. Understand Scope

Before refactoring, understand what you're changing:

```
# With Serena
find_symbol(name="MyClass")
find_referencing_symbols(symbol="MyClass")

# Without Serena
Grep for "MyClass" + Read files to understand context
```

### 2. Plan Changes

List all locations that need modification:
- Direct references
- Imports
- Type annotations
- Documentation/comments
- Tests

### 3. Execute Refactoring

**Renaming (with Serena):**
```
rename_symbol(symbol="old_name", new_name="new_name")
```

**Renaming (without Serena):**
1. Find all files: `Grep` for symbol
2. Read each file to confirm context
3. Edit each occurrence
4. Update imports

### 4. Verify

After refactoring:
1. Run tests
2. Run type checker if available
3. Search for any remaining references

## Common Refactorings

### Rename Function/Method

```
# Find usages first
find_referencing_symbols(symbol="old_function_name")

# Rename across codebase
rename_symbol(symbol="old_function_name", new_name="new_function_name")
```

### Extract Function

1. Use `get_symbols_overview` to understand file structure
2. Use `insert_after_symbol` to add new function
3. Use `replace_symbol_body` to update caller

### Move Symbol to New File

1. `find_symbol` to get full definition
2. `create_text_file` for new location
3. `find_referencing_symbols` to find all imports
4. Update imports in all referencing files
5. Remove from original file

## Key Principles

| Principle | Why |
|-----------|-----|
| **Understand before changing** | Know all references before modifying |
| **Semantic over textual** | "UserID" the type vs "UserID" in a string |
| **Verify after** | Tests catch what static analysis misses |
| **Atomic commits** | One logical refactoring per commit |
