---
name: workbench:data-visualization
description: Create effective data visualizations following Tufte's principles. Use D3.js for custom interactive graphics, or simpler libraries for standard charts. Emphasizes data-ink ratio, clarity, and avoiding chartjunk.
when_to_use: When creating charts, graphs, dashboards. When visualizing data for presentations or reports. When building interactive data explorations. When standard charts feel cluttered or unclear.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash
---

# Data Visualization

**Announce at start:** "I'm using the data-visualization skill to create effective graphics."

## Overview

Create visualizations that communicate data clearly and honestly.

**Core principle:** Maximize data-ink ratio. Every drop of ink should present data.

## Tufte's Principles

| Principle | Application |
|-----------|-------------|
| **Data-ink ratio** | Remove non-data ink (chartjunk, unnecessary gridlines, decorations) |
| **Lie factor** | Visual representation should match data proportions |
| **Small multiples** | Repeat same design for comparison across categories |
| **Sparklines** | Data-intense, word-sized graphics for inline context |
| **Layering** | Separate data from context through visual hierarchy |

## Anti-Patterns (Chartjunk)

Avoid:
- 3D effects on 2D data
- Excessive gridlines
- Decorative elements that don't encode data
- Redundant legends when labels suffice
- Overly thick axes that compete with data
- Moiré patterns and heavy hatching

## Tool Selection

| Need | Tool | Why |
|------|------|-----|
| Standard charts, quick iteration | matplotlib, seaborn, plotly | Fast, good defaults |
| Custom interactive graphics | D3.js | Full control over every element |
| Dashboards | Observable, Streamlit | Built-in interactivity |
| Publication quality | D3.js, matplotlib | Fine-grained styling |

## D3.js Quick Reference

### Setup

```javascript
import * as d3 from 'd3';

// Standard dimensions pattern
const width = 800, height = 400;
const margin = { top: 20, right: 30, bottom: 40, left: 50 };
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;
```

### Common Scales

```javascript
// Continuous → continuous
d3.scaleLinear().domain([0, max]).range([0, width])

// Categorical → continuous
d3.scaleBand().domain(categories).range([0, width]).padding(0.1)

// Continuous → color
d3.scaleSequential(d3.interpolateBlues).domain([0, max])

// Categorical → color
d3.scaleOrdinal(d3.schemeCategory10).domain(categories)
```

### Data Binding

```javascript
svg.selectAll("circle")
  .data(data)
  .join("circle")  // enter + update + exit
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", 5);
```

### Transitions

```javascript
selection
  .transition()
  .duration(750)
  .attr("y", d => yScale(d.value));
```

## Visualization Checklist

Before finalizing:

- [ ] **Data-ink ratio**: Can anything be removed without losing information?
- [ ] **Lie factor**: Do visual proportions match data proportions?
- [ ] **Labels**: Are axes and data points clearly labeled?
- [ ] **Color**: Is color meaningful or decorative? Colorblind-safe?
- [ ] **Context**: Does viewer have enough context to interpret?
- [ ] **Accessibility**: Alt text, ARIA labels for interactive elements?

## Common Patterns

### Bar Chart (Tufte-style)

```javascript
// Minimal: no gridlines, light axis, data labels on bars
g.selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", d => xScale(d.category))
  .attr("y", d => yScale(d.value))
  .attr("width", xScale.bandwidth())
  .attr("height", d => innerHeight - yScale(d.value))
  .attr("fill", "#4a4a4a");

// Direct labels instead of axis
g.selectAll("text.value")
  .data(data)
  .join("text")
  .attr("class", "value")
  .attr("x", d => xScale(d.category) + xScale.bandwidth() / 2)
  .attr("y", d => yScale(d.value) - 5)
  .attr("text-anchor", "middle")
  .text(d => d.value);
```

### Sparkline

```javascript
// Word-sized inline graphic
const sparkline = d3.line()
  .x((d, i) => i * 2)
  .y(d => sparkScale(d));

svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "#333")
  .attr("stroke-width", 1)
  .attr("d", sparkline);
```

### Small Multiples

```javascript
// Same chart repeated for each category
const categories = [...new Set(data.map(d => d.category))];

categories.forEach((cat, i) => {
  const g = svg.append("g")
    .attr("transform", `translate(${(i % 3) * cellWidth}, ${Math.floor(i / 3) * cellHeight})`);

  drawMiniChart(g, data.filter(d => d.category === cat));
});
```

## Python Alternative (matplotlib)

```python
import matplotlib.pyplot as plt

# Tufte-style defaults
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.major.width'] = 0.5

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(categories, values, color='#4a4a4a', width=0.6)
ax.set_ylabel('Value')
plt.tight_layout()
```

## Resources

- Tufte, E. *The Visual Display of Quantitative Information*
- D3.js documentation: https://d3js.org
- Observable: https://observablehq.com (D3 notebooks)
