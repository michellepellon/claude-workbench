---
name: workbench:quick-descriptive-stats
description: Automatically generate quick descriptive statistics and exploratory data analysis for CSV files with visualizations. Use when a CSV file is uploaded, when analyzing tabular data, when requesting data summaries, or when exploring dataset structure and quality. Proactively runs full analysis without asking questions or offering options.
when_to_use: When CSV file is uploaded. When exploring new dataset. When requesting data summary. When checking data quality. When starting data analysis project. Activate immediately without asking.
allowed-tools: Bash, Read, Write
---

# Quick Descriptive Stats

Automatically generates comprehensive descriptive statistics and exploratory
data analysis (EDA) for CSV files.

**Announce at start:** "I'm using the quick-descriptive-stats skill to analyze this dataset."

## Core Principle

**Act immediately. No questions. Complete analysis.**

When a CSV file is detected:
1. Load and inspect data structure
2. Generate all relevant analyses automatically
3. Create appropriate visualizations
4. Present complete results

## Critical Behavior

**DO NOT:**
- Ask what the user wants to do with the data
- Offer options or choices
- Wait for user direction before analyzing
- Provide partial analysis requiring follow-up

**IMMEDIATELY:**
- Run comprehensive analysis
- Generate ALL relevant visualizations
- Present complete results
- No questions, no options, no waiting

## Analysis Components

The skill adapts to data type and generates relevant analyses:

**Data Overview:**
- Dimensions (rows, columns)
- Column names and data types
- Data structure inspection

**Data Quality:**
- Missing value detection and percentages
- Missing value breakdown by column
- Data completeness assessment

**Statistical Analysis:**
- Summary statistics (mean, median, std, min, max)
- Correlation analysis (if multiple numeric columns)
- Distribution characteristics

**Time-Series Analysis** (if date columns present):
- Date range and span
- Temporal trends
- Time-based aggregations

**Categorical Analysis:**
- Value distributions
- Top categories by frequency
- Category percentages

## Visualizations

Adaptively generates only relevant charts:

- **Correlation heatmaps** - Multiple numeric columns
- **Time-series plots** - Date/timestamp columns present
- **Distribution histograms** - Numeric column distributions
- **Categorical bar charts** - Categorical column breakdowns

All visualizations saved to working directory.

## Usage

```python
from analyze import summarize_csv

# Generate comprehensive analysis
report = summarize_csv("data.csv", output_dir="./analysis")
print(report)
```

## Dependencies

Install with uv:
```bash
uv add pandas matplotlib seaborn
```

## See Also

- [examples.md](./examples.md) - Usage examples with different data types
- [reference.md](./reference.md) - Detailed API documentation
- [templates/](./templates/) - Custom analysis templates
- [tests/](./tests/) - Test suite with fixtures
