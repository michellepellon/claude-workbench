# Quick Descriptive Stats - Examples

Usage examples with different types of CSV data.

## Example 1: Sales Data Analysis

**Input CSV** (sales_data.csv):
```csv
date,product,quantity,revenue,region
2024-01-01,Widget A,10,150.50,North
2024-01-02,Widget B,15,225.75,South
2024-01-03,Widget A,8,120.40,East
```

**Claude Code Usage:**
```
Upload sales_data.csv

Claude automatically detects CSV and runs analysis
```

**Output:**
```
============================================================
📊 DATA OVERVIEW
============================================================
Rows: 10 | Columns: 5

Columns: date, product, quantity, revenue, region

📋 DATA TYPES:
  • date: object
  • product: object
  • quantity: int64
  • revenue: float64
  • region: object

🔍 DATA QUALITY:
✓ No missing values - dataset is complete!

📈 NUMERICAL ANALYSIS:

quantity:
  • Mean: 14.2
  • Std Dev: 5.3
  • Range: 8 - 25
  • Median: 14.0

revenue:
  • Mean: 213.45
  • Std Dev: 79.87
  • Range: 120.40 - 375.00
  • Median: 210.70

📊 VISUALIZATIONS CREATED:
  ✓ time_series_analysis.png
  ✓ distributions.png
  ✓ categorical_distributions.png
```

## Example 2: Financial Data

**Input CSV** (financial_metrics.csv):
```csv
metric_a,metric_b,metric_c
10.5,20.3,15.7
12.3,22.1,18.2
9.8,19.5,14.9
```

**Usage:**
```python
from analyze import summarize_csv

report = summarize_csv("financial_metrics.csv", output_dir="./analysis")
print(report)
```

**Generated Files:**
- `correlation_heatmap.png` - Heatmap showing relationships
- `distributions.png` - Distribution histograms for all metrics

## Example 3: Data with Missing Values

**Input CSV** (incomplete_data.csv):
```csv
date,product,quantity,revenue
2024-01-01,Widget A,10,150.50
2024-01-02,,15,225.75
2024-01-03,Widget A,,120.40
```

**Output Highlights:**
```
🔍 DATA QUALITY:
Missing values: 2 (8.33% of total data)
Missing by column:
  • product: 1 (16.7%)
  • quantity: 1 (16.7%)
```

## Example 4: Categorical Data Analysis

**Input CSV** (survey_responses.csv):
```csv
category,region,status
A,North,Active
B,South,Inactive
A,East,Active
C,West,Pending
```

**Generated Files:**
- `categorical_distributions.png` - Bar charts for each categorical column

## Command-Line Usage

Analyze CSV from terminal:
```bash
python analyze.py data.csv ./output
```

Arguments:
- `data.csv` - Path to CSV file
- `./output` - Output directory for visualizations (optional, defaults to ".")

## Integration with Claude Code

The skill activates automatically when:
- A CSV file is uploaded
- User asks to analyze tabular data
- User requests data summary

No prompting needed - complete analysis runs immediately.

## Key Features Demonstrated

1. **Automatic Adaptation** - Analysis adjusts based on data types found
2. **Time-Series Detection** - Automatically plots trends for date columns
3. **Correlation Analysis** - Generates heatmap for multiple numeric columns
4. **Distribution Plots** - Histograms for numeric data
5. **Categorical Breakdown** - Bar charts for categorical variables
6. **Data Quality Reporting** - Missing value detection and percentages

## Common Use Cases

- **Sales Analysis** - Revenue trends, product performance
- **Financial Data** - Transaction patterns, correlations
- **Survey Data** - Response distributions, demographics
- **Operational Metrics** - Performance indicators, time-series
- **Customer Data** - Segmentation, geographic analysis
