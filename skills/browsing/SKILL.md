---
name: workbench:browsing
description: Control Chrome browser directly via DevTools Protocol using the use_browser MCP tool. Use when you need browser automation - authenticated sessions, multi-tab management, form filling, content extraction, web scraping. Provides navigate, click, type, extract, screenshot, eval, and tab management actions. Use this instead of WebFetch for interactive sites requiring authentication or JavaScript execution.
when_to_use: When sites require authentication or login. When JavaScript execution is needed. When automating form filling. When extracting content from interactive sites. When WebFetch fails or is insufficient. When multi-step browser workflows are required.
allowed-tools: mcp__chrome__use_browser
---

# Browser Automation with Chrome

## Overview

Control Chrome via DevTools Protocol using the `use_browser` MCP tool. Single unified interface with auto-starting Chrome.

**Important**: When using this skill, announce: "I'm using the browsing skill to control Chrome."

## When to Use This Skill

**Use this skill when:**
- Controlling authenticated browser sessions
- Managing multiple tabs in running browser
- Filling forms and clicking buttons
- Extracting content from JavaScript-heavy sites
- Web scraping requiring interaction
- Sites that don't work with simple HTTP requests

**Use WebFetch instead when:**
- Simple HTTP GET requests are sufficient
- No authentication or interaction needed
- Static content extraction

**Use Playwright MCP instead when:**
- Need fresh isolated browser instances
- Generating screenshots or PDFs at scale
- Prefer higher-level abstractions

## The use_browser MCP Tool

Single MCP tool with action-based interface. Chrome auto-starts on first use.

### Parameters

- `action` (required): Operation to perform
- `tab_index` (optional): Tab to operate on (default: 0)
- `selector` (optional): CSS selector for element operations
- `payload` (optional): Action-specific data
- `timeout` (optional): Timeout in ms for await operations (default: 5000)

## Quick Start Pattern

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

Note: `\n` at end of password submits the form.

## Actions Reference

### Navigation Actions

#### navigate
Navigate to URL.
- `payload`: URL string
- Example: `{action: "navigate", payload: "https://example.com"}`

#### await_element
Wait for element to appear in DOM.
- `selector`: CSS selector
- `timeout`: Max wait time in ms (default: 5000)
- Example: `{action: "await_element", selector: ".loaded", timeout: 10000}`

#### await_text
Wait for text to appear anywhere on page.
- `payload`: Text to wait for
- `timeout`: Max wait time in ms
- Example: `{action: "await_text", payload: "Welcome", timeout: 10000}`

### Interaction Actions

#### click
Click element.
- `selector`: CSS selector
- Example: `{action: "click", selector: "button.submit"}`

#### type
Type text into input field. Append `\n` to submit form.
- `selector`: CSS selector
- `payload`: Text to type
- Example: `{action: "type", selector: "#email", payload: "user@example.com"}`
- Example (submit): `{action: "type", selector: "#password", payload: "pass123\n"}`

#### select
Select dropdown option.
- `selector`: CSS selector for <select> element
- `payload`: Option value(s) to select
- Example: `{action: "select", selector: "select[name=state]", payload: "CA"}`

### Extraction Actions

#### extract
Get page or element content in various formats.
- `payload`: Format ('markdown'|'text'|'html')
- `selector`: Optional - limit to specific element
- Example (full page): `{action: "extract", payload: "markdown"}`
- Example (element): `{action: "extract", payload: "text", selector: "h1"}`

#### attr
Get element attribute value.
- `selector`: CSS selector
- `payload`: Attribute name
- Example: `{action: "attr", selector: "a.download", payload: "href"}`

#### eval
Execute JavaScript in page context.
- `payload`: JavaScript code string
- Returns: Result of JavaScript expression
- Example: `{action: "eval", payload: "document.title"}`
- Example: `{action: "eval", payload: "document.querySelectorAll('a').length"}`

### Export Actions

#### screenshot
Capture screenshot of page or element.
- `payload`: Filename/path for screenshot
- `selector`: Optional - screenshot specific element only
- Example (full page): `{action: "screenshot", payload: "/tmp/page.png"}`
- Example (element): `{action: "screenshot", payload: "/tmp/btn.png", selector: ".submit-button"}`

### Tab Management Actions

#### list_tabs
List all open tabs with their indices and URLs.
- Example: `{action: "list_tabs"}`

#### new_tab
Create new tab.
- Returns: Index of new tab
- Example: `{action: "new_tab"}`

#### close_tab
Close specific tab.
- `tab_index`: Tab to close
- Example: `{action: "close_tab", tab_index: 2}`

## Common Patterns

### Web Scraping - Article Content
```json
{action: "navigate", payload: "https://blog.example.com/article"}
{action: "await_element", selector: "article"}
{action: "extract", payload: "text", selector: "article h1"}
{action: "extract", payload: "text", selector: ".author-name"}
{action: "extract", payload: "text", selector: "article .content"}
```

### Form Automation - Multi-Step
```json
{action: "navigate", payload: "https://example.com/register"}
{action: "await_element", selector: "input[name=firstName]"}

// Step 1
{action: "type", selector: "input[name=firstName]", payload: "John"}
{action: "type", selector: "input[name=lastName]", payload: "Doe"}
{action: "type", selector: "input[name=email]", payload: "john@example.com"}
{action: "click", selector: "button.next"}

// Wait for step 2
{action: "await_element", selector: "input[name=address]"}

// Step 2
{action: "type", selector: "input[name=address]", payload: "123 Main St"}
{action: "select", selector: "select[name=state]", payload: "IL"}
{action: "type", selector: "input[name=zip]", payload: "62701"}
{action: "click", selector: "button.submit"}

{action: "await_text", payload: "Registration complete"}
```

### Multi-Tab Workflow
```json
// List all tabs
{action: "list_tabs"}

// Work in specific tab (tab index 2)
{action: "click", tab_index: 2, selector: "a.email"}
{action: "await_element", tab_index: 2, selector: ".content"}
{action: "extract", tab_index: 2, payload: "text", selector: ".amount"}
```

### Extract Structured Data with JavaScript
```json
{action: "navigate", payload: "https://shop.example.com/products"}
{action: "await_element", selector: ".product-grid"}

{action: "eval", payload: `
  Array.from(document.querySelectorAll('.product-card')).map(card => ({
    name: card.querySelector('.product-name').textContent.trim(),
    price: card.querySelector('.price').textContent.trim(),
    image: card.querySelector('img').src,
    url: card.querySelector('a').href
  }))
`}
```

### Dynamic Content - Wait for AJAX
```json
{action: "navigate", payload: "https://app.com/dashboard"}

// Wait for loading spinner to disappear
{action: "eval", payload: `
  new Promise(resolve => {
    const check = () => {
      if (!document.querySelector('.spinner')) {
        resolve(true);
      } else {
        setTimeout(check, 100);
      }
    };
    check();
  })
`}

{action: "extract", payload: "text", selector: ".dashboard-data"}
```

## Best Practices

### 1. Always Wait Before Interaction

Don't click or fill immediately after navigate - pages need time to load.

```json
// BAD - might fail if page slow
{action: "navigate", payload: "https://example.com"}
{action: "click", selector: "button"}  // May fail!

// GOOD - wait for element first
{action: "navigate", payload: "https://example.com"}
{action: "await_element", selector: "button"}
{action: "click", selector: "button"}
```

### 2. Use Specific Selectors

Avoid generic selectors that match multiple elements.

```json
// BAD - matches first button found
{action: "click", selector: "button"}

// GOOD - specific selector
{action: "click", selector: "button[type=submit]"}
{action: "click", selector: "#login-button"}
{action: "click", selector: "button.submit-form"}
```

### 3. Submit Forms with \n

Append newline to text to submit forms automatically.

```json
// Submit search
{action: "type", selector: "#search", payload: "my query\n"}

// Submit login
{action: "type", selector: "input[name=password]", payload: "password123\n"}
```

### 4. Verify Selectors First

Extract page HTML to verify selectors before building workflow.

```json
// Check full page structure
{action: "extract", payload: "html"}

// Check specific element
{action: "extract", payload: "html", selector: "form"}
```

### 5. Increase Timeout for Slow Pages

Default timeout is 5000ms - increase for slow-loading content.

```json
// Slow-loading element
{action: "await_element", selector: ".lazy-content", timeout: 30000}

// Slow AJAX request
{action: "await_text", payload: "Data loaded", timeout: 15000}
```

## Troubleshooting

### Element Not Found
- Use `await_element` before interaction
- Verify selector with `extract` using 'html' format
- Check if element is in iframe (not currently supported)

### Timeout Errors
- Increase timeout: `{timeout: 30000}` for slow pages
- Wait for specific element instead of text
- Check if page loaded correctly with `extract`

### Tab Index Out of Range
- Use `list_tabs` to get current indices
- Remember: tab indices change when tabs close
- Don't cache tab indices across operations

### Form Submission Not Working
- Ensure `\n` is at end of text payload
- Or use explicit `click` on submit button
- Wait for submission to complete with `await_text` or `await_element`

## Advanced Usage

For detailed examples and advanced patterns, see [examples.md](examples.md).

For Chrome DevTools Protocol documentation: https://chromedevtools.github.io/devtools-protocol/
