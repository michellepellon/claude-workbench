Run an accessibility audit on the current project.

## Target

$ARGUMENTS

If no target specified, audit the main entry point or URL.

## Process

1. **Automated scan**: Run axe-core or similar tool
2. **Manual checklist**: Verify items that can't be automated
3. **Report**: List violations by severity with remediation guidance

## Automated Checks

```bash
# If using npm project with axe
npx axe <url>

# Or pa11y CLI
npx pa11y <url>

# Or use browser DevTools Lighthouse accessibility audit
```

## Manual Checklist

### Keyboard
- [ ] All interactive elements reachable via Tab
- [ ] Focus indicator visible
- [ ] No keyboard traps
- [ ] Escape closes modals

### Screen Reader
- [ ] Page has descriptive title
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] Images have alt text
- [ ] Form fields have labels

### Visual
- [ ] Text readable at 200% zoom
- [ ] Color is not sole means of conveying info
- [ ] Contrast ratio meets WCAG AA (4.5:1 normal, 3:1 large)

## Output

Report violations grouped by severity (critical → minor) with:
- Element/location
- Issue description
- Remediation suggestion
