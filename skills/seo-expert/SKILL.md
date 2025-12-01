---
name: workbench:seo-expert
description: Comprehensive SEO expertise covering technical optimization, content strategy, and analysis. Use for keyword research, content audits, schema markup, meta optimization, and content planning.
when_to_use: When optimizing content for search. When planning content strategy. When auditing existing content. When implementing schema markup. When analyzing keyword opportunities.
version: 1.0.0
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch
---

# SEO Expert

**Announce at start:** "I'm using the seo-expert skill for search optimization."

## Overview

Comprehensive SEO guidance covering technical optimization, content creation, and analysis/monitoring.

**Core principle:** Create value-first content optimized for both search engines and human readers.

## Quick Reference

| Task | Focus Areas |
|------|-------------|
| New content | Keyword strategy, outline, E-E-A-T signals |
| Existing content | Audit, freshness, cannibalization check |
| Technical | Meta tags, schema markup, structure |
| Authority | E-E-A-T signals, trust elements |

## Content Strategy

### Topic Clustering

Build topical authority through structured content:

```
Pillar Page (comprehensive guide)
├── Supporting Article (subtopic 1)
├── Supporting Article (subtopic 2)
├── FAQ Content
├── Glossary/Definitions
└── Comparison/Resource Pages
```

**Internal linking**: Every supporting article links to pillar; pillar links to all supporting content.

### Content Planning Checklist

- [ ] Identify primary topic and subtopics
- [ ] Map search intent (informational, transactional, navigational)
- [ ] Create detailed outline with H2/H3 structure
- [ ] Plan internal linking before writing
- [ ] Assign one primary keyword per page
- [ ] Differentiate from existing content (avoid cannibalization)

## Technical Optimization

### Meta Tags

| Element | Guidelines |
|---------|------------|
| Title | 50-60 chars, primary keyword in first 30 |
| Description | 150-160 chars, include CTA |
| URL | Under 60 chars, lowercase, hyphens |

```html
<title>Primary Keyword - Secondary | Brand</title>
<meta name="description" content="Action verb + keyword + benefit. Clear CTA.">
```

### Header Structure

```
H1: One per page, contains primary keyword
├── H2: Main sections (target secondary keywords)
│   ├── H3: Subsections
│   └── H3: Subsections
└── H2: Next main section
```

**Rules:**
- Never skip levels (H1 → H3)
- Each H2 should be scannable
- Include keywords naturally

### Schema Markup

Priority schema types:

```json
// Article/BlogPosting
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Title here",
  "author": {"@type": "Person", "name": "Author"},
  "datePublished": "2024-01-15",
  "dateModified": "2024-06-01"
}

// FAQ (for People Also Ask)
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question text?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text."
    }
  }]
}

// HowTo (for step-by-step)
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to...",
  "step": [{"@type": "HowToStep", "text": "Step 1..."}]
}

// BreadcrumbList
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://..."}
  ]
}
```

## Keyword Strategy

### Density Guidelines

| Type | Target | Notes |
|------|--------|-------|
| Primary keyword | 0.5-1.5% | Natural placement |
| Secondary keywords | 0.3-0.5% | Semantic variations |
| LSI keywords | Throughout | Related concepts |

### Placement Priority

1. Title tag (first 30 chars)
2. H1 heading
3. First paragraph (first 100 words)
4. H2 headings (naturally)
5. Image alt text
6. URL slug

### Over-optimization Signs

- Keyword density > 2%
- Forced/unnatural phrasing
- Same keyword in every heading
- Keyword stuffing in alt text

## Featured Snippets

### Snippet Formats

**Paragraph (40-60 words):**
```markdown
## What is [topic]?

[Topic] is [direct definition in 40-60 words]. [Key characteristics]. [Primary benefit or use].
```

**List (5-8 items):**
```markdown
## How to [action]

1. First step
2. Second step
3. Third step
...
```

**Table:**
```markdown
## [Comparison topic]

| Feature | Option A | Option B |
|---------|----------|----------|
| Price   | $X       | $Y       |
```

### Optimization Tips

- Place answer immediately after question heading
- Use question-based H2s ("What is...", "How to...")
- Keep paragraphs concise (2-3 sentences)
- Add FAQ section with FAQPage schema

## E-E-A-T Signals

### Experience

- First-hand accounts and case studies
- Original research and data
- Screenshots, photos of real usage
- Specific examples with details

### Expertise

- Author credentials and bio
- Technical depth appropriate to topic
- Industry terminology (with explanations)
- Comprehensive topic coverage

### Authority

- External citations and references
- Backlinks from authoritative sources
- Brand mentions and recognition
- Published research or studies

### Trust

- Clear contact information
- Privacy policy and terms
- Secure site (HTTPS)
- Reviews and testimonials
- Editorial policy

### Implementation

```markdown
<!-- Author box template -->
## About the Author

[Name] is a [credentials] with [X years] experience in [field].
[Relevant achievements]. [Contact/social links].
```

## Content Audit

### Quality Checklist

| Dimension | Score 1-10 | Issues | Recommendations |
|-----------|------------|--------|-----------------|
| Depth | | | |
| E-E-A-T | | | |
| Readability | | | |
| Keywords | | | |
| Structure | | | |
| Trust signals | | | |

### Freshness Signals

Update triggers:
- Statistics > 2 years old
- Examples > 3 years old
- Missing recent developments
- Rankings dropped > 3 positions
- Traffic declining

Update actions:
- Refresh data points quarterly
- Add current case studies
- Update dateModified in schema
- Refresh internal links
- Update images

### Cannibalization Detection

Signs of keyword cannibalization:
- Multiple pages targeting same primary keyword
- Similar title tags and meta descriptions
- Overlapping content and search intent
- Rankings fluctuating between pages

Resolution:
1. Consolidate (merge weaker into stronger)
2. Differentiate (unique angles, different intent)
3. Canonical (point to primary version)
4. Redirect (301 weaker to stronger)

## Content Writing

### Structure Template

```markdown
# [H1: Primary Keyword + Compelling Hook]

[Introduction: 50-100 words, primary keyword in first sentence]

## [H2: First Main Topic]

[2-3 sentence paragraphs]
[Bullet points for lists]
[Include secondary keywords naturally]

### [H3: Subtopic if needed]

## [H2: Second Main Topic]

...

## Key Takeaways

- Point 1
- Point 2
- Point 3

## FAQ

### [Question 1]?
[Concise answer]

### [Question 2]?
[Concise answer]
```

### Quality Metrics

- Reading level: Grade 8-10
- Paragraphs: 2-3 sentences max
- Sentences: 20 words average
- Include: Lists, subheadings, images
- Keyword density: 0.5-1.5%

## Limitations

This skill cannot:
- Check actual search rankings
- Access traffic/volume metrics
- Analyze competitor content not provided
- Verify technical SEO implementation
- Measure real engagement data

For these, use dedicated SEO tools (Ahrefs, SEMrush, Search Console).
