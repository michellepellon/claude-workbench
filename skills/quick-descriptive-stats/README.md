# Quick Descriptive Stats

Automatically generate quick descriptive statistics and exploratory data
analysis for CSV files with visualizations.

## Features

- **Automatic analysis** - No questions asked, complete analysis immediately
- **Adaptive** - Detects data types and generates relevant visualizations
- **Comprehensive** - Statistics, correlations, distributions, time-series
- **Data quality checks** - Missing value detection and reporting
- **Multiple chart types** - Heatmaps, distributions, categorical breakdowns

## Installation

This skill requires Python dependencies. Install using one of these methods:

### Using uv (recommended)
```bash
cd .claude/skills/analysis/quick-descriptive-stats
uv sync
```

### Using pip
```bash
cd .claude/skills/analysis/quick-descriptive-stats
pip install -r requirements.txt
```

### Using homebrew
```bash
brew install python pandas matplotlib seaborn
pip3 install pytest pytest-cov
```

## Usage

### In Claude Code

Upload any CSV file - the skill activates automatically and runs complete
analysis without prompting.

### Command Line

```bash
python analyze.py data.csv ./output
```

Arguments:
- `data.csv` - Path to CSV file
- `./output` - Output directory for visualizations (optional)

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=term-missing
```

## Documentation

- [examples.md](./examples.md) - Usage examples with different data types
- [reference.md](./reference.md) - Detailed API documentation
- [SKILL.md](./SKILL.md) - Claude Code skill definition

## Dependencies

- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- pytest >= 8.0.0 (dev)
- pytest-cov >= 4.1.0 (dev)
