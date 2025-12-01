# claude-workbench

A curated collection of reusable [Claude Code](https://claude.ai/code) skills and commands for software development workflows.

## Installation

```bash
# Install as a Claude Code plugin
claude plugin add michellepellon/claude-workbench
```

Or clone and symlink manually:

```bash
git clone https://github.com/michellepellon/claude-workbench.git
ln -sf "$(pwd)/claude-workbench/skills" ~/.claude/skills
ln -sf "$(pwd)/claude-workbench/commands" ~/.claude/commands
```

## What's Included

### Commands (9)

Slash commands for common development tasks:

| Command | Description |
|---------|-------------|
| `/accessibility-audit` | Run accessibility audit on the current project |
| `/analyze-issue` | Analyze GitHub issue and create technical specification |
| `/commit` | Create well-formatted commit for staged changes |
| `/create-pr` | Create pull request for the current branch |
| `/plan` | Create implementation plan for provided input |
| `/rename-branch` | Rename current branch based on its changes |
| `/review-script` | Review shell script for defensive patterns and best practices |
| `/session-summary` | Summarize session and output to console |
| `/worktree` | Create git worktree for isolated development |

### Skills (19)

Reusable expertise modules that Claude activates when relevant:

#### Development

| Skill | Description |
|-------|-------------|
| `workbench:python-development` | Expert Python 3.12+, async patterns, FastAPI/Django, pytest |
| `workbench:javascript-typescript` | ES6+ patterns, advanced types, async, Node.js, Jest/Vitest |
| `workbench:shell-scripting` | Production Bash with defensive patterns, error handling, testability |
| `workbench:sql-db-design` | PostgreSQL schema design, constraints, indexing, JSONB |
| `workbench:sql-optimization` | Query optimization via EXPLAIN analysis, indexing, query rewriting |

#### Testing & Quality

| Skill | Description |
|-------|-------------|
| `workbench:test-driven-development` | Strict TDD workflow with comprehensive coverage |
| `workbench:semantic-refactoring` | Safe codebase-wide refactoring with Serena MCP |
| `workbench:simplifying-control-flow` | Flatten nested conditionals with early returns |

#### Data & Visualization

| Skill | Description |
|-------|-------------|
| `workbench:data-visualization` | Effective visualizations with Tufte's principles, D3.js |
| `workbench:quick-descriptive-stats` | Automatic EDA and statistics for CSV files |
| `workbench:pdf` | Extract, create, merge, split PDF documents |
| `workbench:xlsx` | Excel operations with formulas, formatting, analysis |

#### Content & SEO

| Skill | Description |
|-------|-------------|
| `workbench:seo-expert` | Technical SEO, content strategy, schema markup |
| `workbench:writing-clearly-and-concisely` | Strunk's rules for clear prose |

#### Workflow

| Skill | Description |
|-------|-------------|
| `workbench:brainstorming` | Refine ideas through Socratic questioning |
| `workbench:creating-skills` | TDD for process documentation |
| `workbench:executing-plans` | Controlled batch execution with checkpoints |
| `workbench:remembering-conversations` | Search past Claude Code sessions |
| `workbench:browsing` | Chrome automation via DevTools Protocol |

### MCP Servers

Configuration guides for Model Context Protocol servers:

| Server | Purpose |
|--------|---------|
| `serena` | Semantic code understanding for refactoring |

## Usage

### Commands

Commands are invoked with slash notation:

```
/commit
/analyze-issue 123
/plan Build user authentication with OAuth
```

### Skills

Skills activate automatically based on context. You can also invoke them explicitly:

```
I need help with a FastAPI endpoint (activates workbench:python-development)
Review this shell script (activates workbench:shell-scripting)
```

Or reference them directly:

```
Using the workbench:sql-optimization skill, analyze this query...
```

## Project Structure

```
claude-workbench/
├── .claude-plugin/
│   └── manifest.json      # Plugin manifest
├── commands/              # Slash commands
│   ├── commit.md
│   ├── create-pr.md
│   └── ...
├── skills/                # Skill modules
│   ├── python-development/
│   │   └── SKILL.md
│   ├── javascript-typescript/
│   │   └── SKILL.md
│   └── ...
├── mcp-servers/           # MCP server configs
│   └── serena.md
├── CLAUDE.md              # Project coding standards
└── README.md
```

## Customization

### CLAUDE.md

The included `CLAUDE.md` provides coding standards and guidelines. Customize it for your team:

- Communication preferences
- Code style rules
- Testing requirements
- Git workflow
- Debugging process

### Adding Skills

Create a new skill directory with a `SKILL.md` file:

```markdown
---
name: my-skill
description: What this skill does
when_to_use: When to activate this skill
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash
---

# My Skill

Instructions for Claude when this skill is active...
```

Note: The `workbench:` prefix is added automatically by the plugin system.

Add the skill to `.claude-plugin/manifest.json`:

```json
{
  "skills": [
    "skills/my-skill"
  ]
}
```

### Adding Commands

Create a markdown file in `commands/`:

```markdown
Do something useful.

## Input

$ARGUMENTS

## Process

1. First step
2. Second step
```

Add to manifest:

```json
{
  "commands": [
    "commands/my-command.md"
  ]
}
```

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Git (for version control commands)
- Optional: `gh` CLI (for GitHub commands)
- Optional: `shellcheck` (for shell script review)

## Credits

Skills and commands adapted from:

- [wshobson/agents](https://github.com/wshobson/agents) - Python, JS/TS, SQL, shell scripting, SEO
- [jerseycheese/Narraitor](https://github.com/jerseycheese/Narraitor) - Issue analysis
- [evmts/tevm-monorepo](https://github.com/evmts/tevm-monorepo) - Commit formatting, worktrees
- [liam-hq/liam](https://github.com/liam-hq/liam) - PR creation
- [giselles-ai/giselle](https://github.com/giselles-ai/giselle) - Branch renaming
- [chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill) - D3.js visualization
- [oraios/serena](https://github.com/oraios/serena) - Semantic refactoring

## License

MIT
