---
name: workbench:creating-skills
description: TDD for process documentation - test with subagents before writing, iterate until bulletproof
when_to_use: When you discover a technique, pattern, or tool worth documenting for reuse. When you've written a skill and need to verify it works before deploying.
version: 4.0.0
languages: all
---

# Creating Skills

**Announce at start:** "I'm using the creating-skills skill to build and validate this skill."

## Overview

Creating skills IS Test-Driven Development applied to process documentation.

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## TDD Cycle for Skills

| TDD Phase | Skill Creation |
|-----------|----------------|
| **RED** | Run scenario WITHOUT skill, document baseline failures |
| **GREEN** | Write minimal skill addressing those failures |
| **REFACTOR** | Find new loopholes, plug them, re-test |

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this across projects
- Others would benefit

**Don't create for:**
- One-off solutions
- Project-specific conventions (use CLAUDE.md)

## SKILL.md Structure

```markdown
---
name: skill-name
description: One-line summary
when_to_use: Symptoms and situations (include error messages, keywords)
version: 1.0.0
languages: all
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## Quick Reference
Table for scanning common operations.

## Process / Pattern
Step-by-step or before/after examples.

## Common Mistakes
What goes wrong + fixes.
```

## Search Optimization

Future Claude needs to FIND your skill:

1. **Rich when_to_use** - Include symptoms, error messages, keywords
2. **Descriptive naming** - `creating-skills` not `skill-creation`
3. **Keyword coverage** - Error messages, tool names, synonyms

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Write skill before testing? Delete it. Start over.

## Checklist

**RED Phase:**
- [ ] Run scenarios WITHOUT skill
- [ ] Document baseline failures/rationalizations

**GREEN Phase:**
- [ ] Write minimal skill addressing failures
- [ ] Run scenarios WITH skill - verify compliance

**REFACTOR Phase:**
- [ ] Find new loopholes
- [ ] Add explicit counters
- [ ] Re-test until bulletproof

## Anti-Patterns

- ❌ Narrative stories ("In session X, we found...")
- ❌ Multi-language examples (one good example is enough)
- ❌ Generic labels (helper1, step2)
- ❌ Deploying without testing
