# Serena MCP Server

Semantic code understanding via Language Server Protocol.

## Installation

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Add to Claude Code
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project "$(pwd)"
```

Use `--context ide-assistant` to avoid duplicating Claude Code's built-in file tools.

## Tools

### Symbol Navigation

| Tool | Purpose |
|------|---------|
| `find_symbol` | Search for symbols by name/pattern |
| `find_referencing_symbols` | Find where a symbol is used |
| `get_symbols_overview` | List top-level symbols in a file |

### Symbol Editing

| Tool | Purpose |
|------|---------|
| `replace_symbol_body` | Replace a symbol's implementation |
| `insert_after_symbol` | Add code after a symbol |
| `insert_before_symbol` | Add code before a symbol |
| `rename_symbol` | Rename across entire codebase |

### File Operations

| Tool | Purpose |
|------|---------|
| `read_file` | Read file contents |
| `create_text_file` | Create or overwrite file |
| `replace_content` | Find/replace in file |
| `search_for_pattern` | Regex search across project |

## Language Support

30+ languages via LSP: Python, TypeScript, JavaScript, Rust, Go, Java, C/C++, and more.

## Links

- [Repository](https://github.com/oraios/serena)
- [Documentation](https://oraios.github.io/serena/)
