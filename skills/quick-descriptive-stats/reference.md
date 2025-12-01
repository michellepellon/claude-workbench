# Quick Descriptive Stats - API Reference

Detailed API documentation for all functions.

## Installation

```bash
cd .claude/skills/analysis/quick-descriptive-stats
uv add pandas matplotlib seaborn
uv add --dev pytest pytest-cov
```

## Module: analyze.py

### load_csv

```python
def load_csv(file_path: str) -> pd.DataFrame
```

Load CSV file with error handling and validation.

**Parameters:**
- `file_path` (str): Path to CSV file

**Returns:**
- `pd.DataFrame`: DataFrame containing CSV data

**Raises:**
- `FileNotFoundError`: If CSV file doesn't exist
- `ValueError`: If CSV file is empty or cannot be parsed

**Example:**
```python
df = load_csv("data.csv")
```

---

### analyze_data_quality

```python
def analyze_data_quality(df: pd.DataFrame) -> Dict[str, any]
```

Analyze data quality and detect missing values.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to analyze

**Returns:**
Dict containing:
- `total_missing` (int): Total number of missing values
- `missing_percentage` (float): Percentage of missing values
- `is_complete` (bool): True if no missing values
- `missing_by_column` (dict): Columns with missing values

**Example:**
```python
quality = analyze_data_quality(df)
if not quality["is_complete"]:
    print(f"Missing: {quality['total_missing']}")
```

---

### compute_statistics

```python
def compute_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]
```

Compute summary statistics for numeric columns.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to analyze

**Returns:**
Dictionary mapping column names to statistics (mean, std, min, 25%, 50%, 75%, max)

**Example:**
```python
stats = compute_statistics(df)
print(f"Mean revenue: {stats['revenue']['mean']}")
```

---

### analyze_correlations

```python
def analyze_correlations(df: pd.DataFrame) -> Optional[pd.DataFrame]
```

Compute correlation matrix for numeric columns.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to analyze

**Returns:**
- `pd.DataFrame`: Correlation matrix if multiple numeric columns exist
- `None`: If fewer than 2 numeric columns

**Example:**
```python
corr = analyze_correlations(df)
if corr is not None:
    print(corr)
```

---

### create_correlation_heatmap

```python
def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    output_path: str
) -> None
```

Generate correlation heatmap visualization.

**Parameters:**
- `corr_matrix` (pd.DataFrame): Correlation matrix
- `output_path` (str): Path to save visualization

**Side Effects:**
- Creates PNG file at output_path

**Example:**
```python
corr = df.corr()
create_correlation_heatmap(corr, "heatmap.png")
```

---

### create_time_series_plots

```python
def create_time_series_plots(
    df: pd.DataFrame,
    output_dir: str
) -> List[str]
```

Generate time-series visualizations if date columns exist.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to visualize
- `output_dir` (str): Directory for output files

**Returns:**
- `List[str]`: List of paths to created visualizations

**Behavior:**
- Detects columns with "date" or "time" in name
- Creates trend plots for numeric columns over time
- Maximum 3 plots (configurable via MAX_TIMESERIES_PLOTS)

**Example:**
```python
charts = create_time_series_plots(df, "./output")
```

---

### create_distribution_plots

```python
def create_distribution_plots(
    df: pd.DataFrame,
    output_dir: str
) -> List[str]
```

Generate distribution histograms for numeric columns.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to visualize
- `output_dir` (str): Directory for output files

**Returns:**
- `List[str]`: List of paths to created visualizations

**Behavior:**
- Creates histograms for numeric columns
- Maximum 4 plots (2x2 grid)
- Uses DEFAULT_BINS (30) for binning

**Example:**
```python
charts = create_distribution_plots(df, "./output")
```

---

### create_categorical_plots

```python
def create_categorical_plots(
    df: pd.DataFrame,
    output_dir: str
) -> List[str]
```

Generate categorical distribution bar charts.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to visualize
- `output_dir` (str): Directory for output files

**Returns:**
- `List[str]`: List of paths to created visualizations

**Behavior:**
- Identifies categorical (object type) columns
- Excludes ID columns (contains "id" in name)
- Shows top MAX_CATEGORIES_DISPLAY (10) values per column

**Example:**
```python
charts = create_categorical_plots(df, "./output")
```

---

### summarize_csv

```python
def summarize_csv(file_path: str, output_dir: str = ".") -> str
```

Generate comprehensive analysis of CSV file.

Main entry point that orchestrates all analysis functions.

**Parameters:**
- `file_path` (str): Path to CSV file
- `output_dir` (str): Directory for visualizations (default: ".")

**Returns:**
- `str`: Formatted analysis report

**Raises:**
- `FileNotFoundError`: If CSV file doesn't exist
- `ValueError`: If CSV file is empty or malformed

**Side Effects:**
- Creates multiple PNG visualization files in output_dir

**Example:**
```python
report = summarize_csv("data.csv", "./analysis")
print(report)
```

---

## Constants

```python
DEFAULT_BINS: int = 30              # Histogram bins
DEFAULT_DPI: int = 150              # Image resolution
MAX_CATEGORIES_DISPLAY: int = 10    # Top categories to show
MAX_CATEGORICAL_PLOTS: int = 4      # Max categorical charts
MAX_NUMERIC_PLOTS: int = 4          # Max distribution plots
MAX_TIMESERIES_PLOTS: int = 3       # Max time-series plots
```

---

## Testing

Run test suite:
```bash
uv run pytest
```

Run with coverage:
```bash
uv run pytest --cov=. --cov-report=term-missing
```

Run specific test file:
```bash
uv run pytest tests/test_loading.py -v
```

---

## Error Handling

All functions use type annotations and include comprehensive error handling:

- **FileNotFoundError**: CSV file not found
- **ValueError**: Empty or malformed CSV
- **pd.errors.EmptyDataError**: pandas-specific empty data error

---

## Best Practices

1. **Always specify output_dir** for visualizations
2. **Check data quality results** before interpreting statistics
3. **Verify correlation matrix exists** before using
4. **Use type hints** when extending functionality
5. **Write tests** for any new analysis functions

---

## Extending the Skill

### Adding New Analysis

1. Write test in `tests/test_*.py`
2. Run test (should fail)
3. Implement function in `analyze.py`
4. Run test (should pass)
5. Add to `summarize_csv` orchestration

### Adding New Visualization

1. Create function following naming pattern `create_*_plots`
2. Return `List[str]` of created file paths
3. Add to `summarize_csv` charts list
4. Document in this reference

---

## Performance Considerations

- **Large CSVs**: pandas loads entire file into memory
- **Many columns**: Visualization creation scales with column count
- **Time-series**: Groupby operations can be slow on large datasets

For CSVs > 100MB, consider:
- Sampling data before analysis
- Disabling certain visualizations
- Processing in chunks
