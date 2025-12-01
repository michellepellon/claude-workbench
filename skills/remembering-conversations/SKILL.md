---
name: workbench:remembering-conversations
description: Search previous Claude Code conversations for facts, patterns, decisions, and context. Use when user mentions "we discussed this before", when debugging similar issues, when looking for architectural decisions, or before reinventing solutions.
when_to_use: When user says "we discussed this before". When debugging similar issues. When looking for past architectural decisions. When searching for code patterns from previous work. Before reinventing solutions.
allowed-tools: Bash, Read, Task
---

# Remembering Conversations

Search archived conversations for past decisions, patterns, and context.

**Core principle:** Search before reinventing.

**Announce:** "I'm searching previous conversations for [topic]."

## When to Use

**Search when:**
- User mentions "we discussed this before"
- Debugging similar issues
- Looking for architectural decisions or patterns
- Before implementing something familiar

**Don't search when:**
- Info is in current conversation
- Question is about current codebase (use Grep/Read)

## Setup Required

This skill requires conversation archiving infrastructure. Options:

1. **Manual export**: Export conversations to markdown files
2. **Automated archiving**: Use hooks to save conversations on completion
3. **Semantic search**: Index with embeddings for similarity search

See `tool/` directory for reference implementation with semantic search.

## Search Modes

| Mode | Use Case |
|------|----------|
| **Semantic** | "How did we handle auth errors?" - finds conceptually similar |
| **Text** | "a1b2c3d4" - finds exact git SHAs, error messages |

## Usage

```bash
# Semantic search (default)
search-conversations "React Router authentication errors"

# Exact text match
search-conversations --text "a1b2c3d4"

# With date filters
search-conversations --after 2025-01-01 "refactoring"
```

## Relationship to Serena

| Tool | Searches | Use For |
|------|----------|---------|
| **This skill** | Past conversations | Decisions, rationale, context |
| **Serena** | Current codebase | Symbols, references, code structure |

They're complementary: Serena for code understanding, this for institutional memory.
