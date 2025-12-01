# Browser Automation Skill

Control Chrome browser directly via DevTools Protocol for web automation, scraping, and interaction.

## Overview

This skill teaches Claude Code agents how to use the `use_browser` MCP tool to:
- Navigate websites and handle authenticated sessions
- Fill forms and interact with elements (click, type, select)
- Extract content in multiple formats (text, HTML, markdown)
- Manage multiple tabs simultaneously
- Execute JavaScript in page context
- Capture screenshots
- Wait for dynamic content to load

## Prerequisites

This skill requires the Chrome MCP server to be installed and configured.

### Install Chrome MCP Server

The browsing skill uses the `use_browser` MCP tool provided by a Chrome MCP server. This server must be configured in your Claude Code MCP settings.

**Note**: MCP server installation details are specific to your environment. See the Chrome MCP server documentation for setup instructions.

## Usage

### In Claude Code

The skill activates automatically when browser automation is needed. Simply describe what you want to do:

- "Navigate to example.com and extract the page title"
- "Fill out the login form at app.example.com"
- "Search for products and extract prices"
- "Open multiple tabs and compare content"

The skill will use the `use_browser` MCP tool to control Chrome.

## Documentation

- **[SKILL.md](SKILL.md)** - Complete tool reference and actions
- **[examples.md](examples.md)** - Comprehensive usage examples

## Quick Start

Navigate and extract content:
```json
{action: "navigate", payload: "https://example.com"}
{action: "await_element", selector: "h1"}
{action: "extract", payload: "text", selector: "h1"}
```

Fill and submit form:
```json
{action: "navigate", payload: "https://example.com/login"}
{action: "await_element", selector: "input[name=email]"}
{action: "type", selector: "input[name=email]", payload: "user@example.com"}
{action: "type", selector: "input[name=password]", payload: "password123\n"}
{action: "await_text", payload: "Welcome"}
```

See [examples.md](examples.md) for comprehensive patterns including:
- Web scraping
- Form automation
- Multi-tab workflows
- Dynamic content handling
- JavaScript evaluation

## Key Features

### Action-Based Interface

Single unified `use_browser` tool with action parameter:
- **Navigation**: navigate, await_element, await_text
- **Interaction**: click, type, select
- **Extraction**: extract, attr, eval
- **Export**: screenshot
- **Tab Management**: list_tabs, new_tab, close_tab

### Automatic Chrome Startup

Chrome auto-starts with remote debugging enabled on first use.

### Multi-Tab Support

Work across multiple tabs using `tab_index` parameter.

### JavaScript Execution

Execute arbitrary JavaScript in page context for complex extraction or interaction.

## Best Practices

1. **Always wait before interaction** - Use `await_element` after navigation
2. **Use specific selectors** - Avoid generic selectors like "button"
3. **Submit forms with \n** - Append newline to auto-submit
4. **Verify selectors first** - Use `extract` with "html" to check page structure
5. **Increase timeout for slow pages** - Default is 5000ms

See [SKILL.md](SKILL.md) for complete best practices and troubleshooting.
