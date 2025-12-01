# Excel/XLSX Skill

Comprehensive Excel spreadsheet manipulation toolkit for Claude Code agents.

## Features

- **Read & Analyze**: Load Excel files with pandas for data analysis
- **Create**: Generate spreadsheets with formulas and formatting
- **Formulas**: Add Excel formulas that recalculate automatically
- **Formatting**: Apply colors per financial model standards
- **Recalculation**: Verify formulas with LibreOffice integration
- **Error Handling**: Robust error detection and reporting

## Installation

### Prerequisites

- Python 3.10+
- uv package manager
- LibreOffice (for formula recalculation)

### macOS
```bash
brew install libreoffice
```

### Ubuntu/Debian
```bash
sudo apt-get install libreoffice
```

### Install Dependencies

```bash
cd ~/.claude/skills/documents/xlsx
uv sync
```

## Quick Start

### Reading Excel Files

```python
from scripts.xlsx_operations import read_excel

df = read_excel('data.xlsx')
print(df.head())
```

### Creating Excel Files

```python
from scripts.xlsx_operations import write_dataframe
import pandas as pd

df = pd.DataFrame({
    'Product': ['Widget', 'Gadget'],
    'Price': [10.99, 24.99]
})

write_dataframe(df, 'products.xlsx')
```

### Adding Formulas

```python
from openpyxl import Workbook
from scripts.xlsx_operations import add_formula, set_cell_color

wb = Workbook()
ws = wb.active

ws['A1'] = 'Total'
ws['B1'] = 100
ws['B2'] = 200

add_formula(ws, 'B3', '=SUM(B1:B2)')
set_cell_color(ws, 'B3', 'black')  # Formulas are black

wb.save('total.xlsx')
```

### Recalculating Formulas

**CRITICAL**: Always recalculate after creating/modifying Excel files.

```bash
python scripts/recalc.py total.xlsx
```

Output:
```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 1
}
```

## Financial Model Standards

### Color Coding

| Color | Use Case | Function |
|-------|----------|----------|
| **Blue** | Hardcoded inputs | `set_cell_color(ws, 'A1', 'blue')` |
| **Black** | Formulas | `set_cell_color(ws, 'A1', 'black')` |
| **Green** | Internal links | `set_cell_color(ws, 'A1', 'green')` |
| **Red** | External links | `set_cell_color(ws, 'A1', 'red')` |

### Best Practices

1. **Use Formulas**: Never hardcode calculated values
2. **Recalculate Always**: Run `recalc.py` after changes
3. **Zero Errors Required**: Fix all formula errors before delivery
4. **Color Code**: Apply standard colors for clarity

## Testing

Run the test suite:

```bash
uv run python -m pytest tests/ -v
```

All tests follow TDD approach:
- Unit tests for basic operations
- Integration tests for pandas/openpyxl
- Error handling tests

## Documentation

- **[SKILL.md](SKILL.md)** - Quick reference and API overview
- **[examples.md](examples.md)** - Comprehensive usage examples

## Dependencies

| Library | Purpose |
|---------|---------|
| pandas | Data analysis and I/O |
| openpyxl | Excel file creation/editing |
| LibreOffice | Formula recalculation |

## Common Operations

### Data Analysis
```python
import pandas as pd

df = pd.read_excel('sales.xlsx')
summary = df.groupby('Region')['Sales'].sum()
```

### Create Financial Model
```python
from openpyxl import Workbook
from scripts.xlsx_operations import add_formula, set_cell_color

wb = Workbook()
ws = wb.active

# Revenue (input - blue)
ws['A1'] = 'Revenue'
ws['B1'] = 1000000
set_cell_color(ws, 'B1', 'blue')

# Growth rate (input - blue)
ws['A2'] = 'Growth %'
ws['B2'] = 0.15
set_cell_color(ws, 'B2', 'blue')

# Next year (formula - black)
ws['A3'] = 'Year 2'
add_formula(ws, 'B3', '=B1*(1+B2)')
set_cell_color(ws, 'B3', 'black')

wb.save('projection.xlsx')

# Recalculate
import subprocess
subprocess.run(['python', 'scripts/recalc.py', 'projection.xlsx'])
```

## Error Handling

All operations raise `ExcelOperationError`:

```python
from scripts.xlsx_operations import read_excel, ExcelOperationError

try:
    df = read_excel('data.xlsx')
except ExcelOperationError as e:
    print(f"Error: {e}")
```

## Troubleshooting

### Formula Errors

If `recalc.py` reports errors:

```json
{
  "status": "errors_found",
  "total_errors": 2,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

Fix the formulas at the specified locations and recalculate again.

### LibreOffice Not Found

Ensure LibreOffice is installed and `soffice` is in PATH:

```bash
which soffice
```

## Contributing

This skill follows strict TDD practices:
1. Write failing test
2. Implement minimal code to pass
3. Refactor while keeping tests green

See `tests/` for examples.

## License

Part of claude-workbench. See [LICENSE](../../LICENSE).
