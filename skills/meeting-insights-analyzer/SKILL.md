---
name: meeting-insights-analyzer
description: Analyzes meeting transcripts to uncover communication patterns, conflict avoidance, and leadership behaviors with timestamped, actionable feedback.
when_to_use: When analyzing meeting transcripts or recordings. When looking for communication patterns. When identifying conflict avoidance. When measuring speaking ratios. When tracking filler words. When evaluating facilitation style. When preparing performance reviews. When coaching on communication skills.
version: 1.0.0
allowed-tools: Read, Glob, Grep, Write
---

# Meeting Insights Analyzer

**Announce at start:** "I'm using the meeting-insights-analyzer skill to analyze your transcripts."

## Overview

Transform meeting transcripts into actionable feedback about communication patterns.

**Core principle:** Every insight must include a specific example, why it matters, and how to improve.

## Quick Reference

| Analysis Type | What to Look For |
|---------------|------------------|
| **Conflict Avoidance** | Hedging ("maybe", "kind of"), indirect requests, changing subjects under tension |
| **Speaking Ratio** | % of meeting spent talking, interruptions given/received, turn length |
| **Filler Words** | "um", "uh", "like", "you know", "actually" - frequency per minute |
| **Active Listening** | Questions referencing others' points, paraphrasing, building on ideas |
| **Facilitation** | Decision style, handling disagreement, inclusion, time management |

## Process

### 1. Discover Available Data

```
Scan folder for: .txt, .md, .vtt, .srt, .docx
Check for: speaker labels, timestamps
Identify: user's name/identifier, date range
```

### 2. Clarify Analysis Goals

If not specified, ask what they want to learn:
- Specific behaviors (conflict avoidance, interruptions, filler words)
- Communication effectiveness (clarity, directness, listening)
- Meeting facilitation skills
- Speaking patterns and ratios

### 3. Pattern Detection

**Conflict Avoidance Signals:**
- Hedging: "maybe we could potentially consider..."
- Deflection: "whatever you think is best"
- Subject changes when tension rises
- Agreeing without commitment: "yeah, but..."

**Speaking Analysis:**
- Calculate speaking percentage per participant
- Count interruptions (by and of user)
- Measure average turn length
- Track question vs. statement ratio

**Filler Word Tracking:**
- Count occurrences per speaking turn
- Note situational increases (nervous, uncertain)
- Calculate frequency per minute

**Active Listening Markers:**
- Questions referencing previous points
- Paraphrasing others' ideas
- Building on contributions
- Clarifying questions

### 4. Format Findings

For each pattern, provide:

```markdown
### [Pattern Name]

**Finding**: [One-sentence summary]
**Frequency**: [X times across Y meetings]

**Example** - [Meeting Name] at [Timestamp]:
> [Actual quote from transcript]

**Why This Matters**: [Impact or missed opportunity]

**Better Approach**: [Specific alternative]
```

### 5. Synthesize Report

Use the template structure:
- Key patterns identified (top 3)
- Communication strengths (with examples)
- Growth opportunities (actionable)
- Speaking statistics
- Concrete next steps

## Output Format

See `templates/analysis-report.md` for the full report structure.

**Key sections:**
1. Analysis metadata (date range, meeting count, duration)
2. Pattern findings with timestamped examples
3. Strengths and growth areas
4. Statistics table
5. Action items

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generic feedback without examples | Always include timestamp + quote |
| Listing patterns without impact | Explain WHY each matters |
| Criticism without alternatives | Provide specific better phrasing |
| Analyzing without context | Ask about user's role/goals first |
| Single-meeting conclusions | Note when patterns need more data |

## Anti-Patterns

- Vague observations ("you talk a lot")
- Judgmental tone instead of developmental
- Missing the positive patterns
- Overwhelming with too many insights at once
- Not offering follow-up options

## See Also

- `templates/analysis-report.md` - Full output template
- `README.md` - Setup and transcript sources
- `examples.md` - Complete analysis examples
