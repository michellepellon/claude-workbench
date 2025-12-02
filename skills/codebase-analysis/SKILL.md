---
name: codebase-analysis
description: Analyzes codebase to find similar features, reusable utilities, and architectural patterns before implementation.
when_to_use: Before implementing new features. When needing to understand existing patterns. When discovering reusable utilities. When architectural guidance is needed. When similar features might exist.
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
---

# Codebase Analysis Skill

Analyze a codebase to provide developers with relevant context for implementation tasks.

**Announce at start:** "I am using the codebase-analysis skill to find relevant patterns and utilities."

## When to Use

- Developer needs to understand existing patterns before implementation
- Complex features require architectural guidance
- Reusable utilities need to be discovered
- Similar features might exist that could be referenced

## Analysis Process

### Step 1: Understand the Task

Clarify what feature or functionality is being implemented. Identify:
- Core functionality needed
- Key domain concepts involved
- Technical requirements (APIs, data storage, UI, etc.)

### Step 2: Search for Similar Features

Use Grep and Glob to find related code:

```bash
# Search for related domain terms
Grep: pattern="<domain_term>" (e.g., "user", "payment", "auth")

# Find files with similar naming patterns
Glob: pattern="**/*<feature>*" (e.g., "**/*register*", "**/*checkout*")

# Search for related function/class names
Grep: pattern="(class|function|def)\s+\w*<term>\w*"
```

### Step 3: Identify Architectural Patterns

Look for:
- **Directory structure patterns** - How similar features are organized
- **Service layer patterns** - Business logic location
- **Data access patterns** - Repository/DAO patterns
- **Error handling patterns** - How errors are managed
- **Testing patterns** - How similar features are tested

```bash
# Find service files
Glob: pattern="**/services/**/*.{py,ts,js}"

# Find repository/data access patterns
Grep: pattern="(Repository|DAO|Store|Model)" glob="**/*.{py,ts,js}"

# Find test patterns for similar features
Glob: pattern="**/test*/**/*<feature>*"
```

### Step 4: Discover Reusable Utilities

Search for existing utilities that could be reused:

```bash
# Find utility directories
Glob: pattern="**/utils/**/*" or "**/helpers/**/*" or "**/lib/**/*"

# Search for common utility patterns
Grep: pattern="(validate|format|parse|convert|generate)" glob="**/utils/**/*"
```

### Step 5: Analyze Found Code

Read the most relevant files to understand:
- Implementation approaches
- Code style and conventions
- Integration patterns
- Edge case handling

## Output Format

Return a structured summary:

```
CODEBASE ANALYSIS COMPLETE

## Similar Features Found
- <Feature name> (<file_path>) - <similarity assessment>
  * <Key pattern 1>
  * <Key pattern 2>

## Reusable Utilities
- <UtilityName> (<file_path>) - <function_names>
- <UtilityName> (<file_path>) - <function_names>

## Architectural Patterns
- <Pattern name> - <description and location>
- <Pattern name> - <description and location>

## Suggested Implementation Approach
1. <Step 1 based on findings>
2. <Step 2 referencing existing patterns>
3. <Step 3 using discovered utilities>

## Files to Reference
- <file_path> - <why it's relevant>
- <file_path> - <why it's relevant>
```

## Example Analysis

For a "password reset" feature:

1. **Search terms:** "password", "reset", "token", "email", "auth"
2. **Similar features:** User registration, email verification, login
3. **Utilities to find:** EmailService, TokenGenerator, validation helpers
4. **Patterns to follow:** Authentication flow, transaction handling

## Error Handling

If no similar features found:
1. Broaden search terms
2. Look for adjacent functionality
3. Document that this is a new pattern for the codebase
4. Suggest examining similar open-source projects for patterns

## Key Principles

| Principle | Application |
|-----------|-------------|
| **Search broadly first** | Start with domain terms, narrow down |
| **Read before recommending** | Actually read the code, don't guess |
| **Prioritize recent patterns** | Newer code often reflects current conventions |
| **Note inconsistencies** | If patterns vary, mention it |
| **Be specific** | Include file paths and line numbers |
