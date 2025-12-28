# Meeting Insights Analyzer

Analyze meeting transcripts to uncover communication patterns, conflict avoidance behaviors, and leadership insights with timestamped, actionable feedback.

## Features

- **Pattern Recognition**: Conflict avoidance, hedging, indirect communication
- **Speaking Analysis**: Ratios, interruptions, turn-taking patterns
- **Filler Word Tracking**: Frequency and situational triggers
- **Active Listening**: Question quality, paraphrasing, building on ideas
- **Facilitation Review**: Decision style, inclusion, time management
- **Trend Tracking**: Compare patterns across time periods

## Quick Start

1. Download meeting transcripts to a folder (e.g., `~/meetings/`)
2. Navigate to that folder in Claude Code
3. Request analysis:

```
Analyze all meetings and tell me when I avoided conflict.
```

```
Look at my meetings from the past month and identify my communication patterns.
```

```
Compare my facilitation style between Q1 and Q2.
```

## Getting Transcripts

### Granola

Granola auto-transcribes meetings with speaker labels.

1. Open Granola preferences
2. Go to Export settings
3. Export transcripts as markdown
4. Save to your meetings folder

### Zoom

1. Enable cloud recording with transcription in Zoom settings
2. After meetings, download VTT or transcript files
3. Store in dedicated folder

### Google Meet

1. Enable transcription in Google Workspace admin
2. Transcripts save to Google Docs automatically
3. Download as .txt or access via Drive

### Otter.ai / Fireflies.ai

1. Connect to your calendar for auto-recording
2. Use bulk export feature
3. Download transcripts to local folder

### Microsoft Teams

1. Enable transcription in meeting settings
2. Download from meeting recap or recording
3. Save .vtt or .docx files locally

## File Naming

Consistent naming helps with date-range analysis:

```
YYYY-MM-DD - Meeting Name.txt
```

Examples:
```
2024-01-15 - Team Standup.txt
2024-01-16 - 1:1 with Sarah.txt
2024-01-17 - Product Review.txt
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Plain text | `.txt` | Universal, simple |
| Markdown | `.md` | Good for structured notes |
| WebVTT | `.vtt` | Zoom, Teams standard |
| SubRip | `.srt` | Common subtitle format |
| Word | `.docx` | Some tools export this |

## Best Practices

**For accurate analysis:**
- Ensure transcripts have speaker labels
- Include timestamps when available
- Use your actual name/identifier consistently
- Keep one meeting per file

**For meaningful insights:**
- Analyze at least 5-10 meetings for patterns
- Compare similar meeting types (1:1s vs team meetings)
- Focus on one improvement area at a time
- Re-analyze monthly to track progress

**For privacy:**
- Keep sensitive transcripts local
- Don't commit meeting data to repos
- Consider anonymizing before sharing analyses

## Common Analysis Requests

```
When do I avoid difficult conversations?
How often do I interrupt others?
What's my speaking vs. listening ratio?
Do I ask good questions?
How do I handle disagreement?
Am I inclusive of all voices?
Do I use too many filler words?
How clear are my action items?
Do I stay on agenda or get sidetracked?
How has my communication changed over time?
```

## Advanced Usage

### Multi-folder comparison
```
Compare my 1:1 meetings in ~/meetings/1on1/
with my team meetings in ~/meetings/team/
```

### Specific behavior deep-dive
```
Find every instance where I used hedging language
and categorize by situation type.
```

### Performance review prep
```
Create a summary of my communication strengths
and growth over the past quarter with specific examples.
```

### Coaching others
```
Analyze [team member]'s speaking patterns and
create developmental feedback.
```

## Related Skills

- `writing-clearly-and-concisely` - Improve written communication
- `brainstorming` - Structure thinking before meetings
