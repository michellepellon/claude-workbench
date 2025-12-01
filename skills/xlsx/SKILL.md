---
name: workbench:xlsx
description: Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Use when working with Excel files for data analysis, financial models, reporting, or any spreadsheet operations.
when_to_use: When creating or editing Excel files. When building financial models. When analyzing spreadsheet data. When generating reports in Excel format. When working with formulas and formatting. When reading or writing .xlsx files.
allowed-tools: Read, Write, Bash
---

# Excel/XLSX Operations

**Announce at start:** "I'm using the xlsx skill to work with Excel spreadsheets."

## Quick Start

### Reading Data with pandas
```python
import pandas as pd

# Read Excel file
df = pd.read_excel('data.xlsx')

# Read specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# Read all sheets
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)
```

### Creating Excel Files with openpyxl
```python
from scripts.xlsx_operations import (
    create_workbook,
    add_formula,
    set_cell_color
)

# Create workbook
wb = create_workbook('output.xlsx')
ws = wb.active

# Add data
ws['A1'] = 'Revenue'
ws['B1'] = 100000

# Add formula
add_formula(ws, 'B2', '=B1*1.1')

# Set colors per financial model standards
set_cell_color(ws, 'B1', 'blue')  # Input
set_cell_color(ws, 'B2', 'black')  # Formula

wb.save('output.xlsx')
```

### Writing DataFrames
```python
from scripts.xlsx_operations import write_dataframe

write_dataframe(df, 'output.xlsx', sheet_name='Data')
```

## Financial Model Standards

### Color Coding
Per industry standards (configurable):

| Color | Use Case | RGB |
|-------|----------|-----|
| **Blue** | Hardcoded inputs | 0,0,255 |
| **Black** | Formulas and calculations | 0,0,0 |
| **Green** | Links within workbook | 0,128,0 |
| **Red** | External file links | 255,0,0 |
| **Yellow bg** | Key assumptions | 255,255,0 |

### Number Formatting
- **Years**: Text format ("2024" not "2,024")
- **Currency**: $#,##0 with units in header
- **Zeros**: Display as "-"
- **Percentages**: 0.0% (one decimal)
- **Negatives**: Parentheses (123) not minus -123

## Formula Recalculation

**CRITICAL**: Always recalculate formulas after creating/modifying Excel files.

```bash
python scripts/recalc.py output.xlsx [timeout_seconds]
```

Returns JSON with error details:
```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {}
}
```

If errors found:
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

Fix all errors before delivering files.

## Common Operations

### Data Analysis
```python
import pandas as pd

df = pd.read_excel('sales.xlsx')

# Basic statistics
print(df.describe())

# Filtering
high_value = df[df['Amount'] > 1000]

# Grouping
by_region = df.groupby('Region')['Sales'].sum()
```

### Creating Formulas
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Data
ws['A1'] = 'Item'
ws['B1'] = 'Price'
ws['A2'] = 'Widget'
ws['B2'] = 100

# Formula (BLACK color for all formulas)
ws['B3'] = '=SUM(B2:B2)'
ws['B3'].font = Font(color='00000000')

wb.save('output.xlsx')
```

### Advanced Formatting
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active

# Bold header
ws['A1'].font = Font(bold=True)

# Center align
ws['A1'].alignment = Alignment(horizontal='center')

# Yellow background for assumptions
ws['A1'].fill = PatternFill(
    'solid', start_color='FFFF00'
)

wb.save('formatted.xlsx')
```

## Error Handling

All operations raise `ExcelOperationError`:

```python
from scripts.xlsx_operations import (
    read_excel,
    ExcelOperationError
)

try:
    df = read_excel('data.xlsx')
except ExcelOperationError as e:
    print(f"Error: {e}")
```

## Best Practices

### Use Formulas, Not Hardcoded Values
```python
# ❌ WRONG - Hardcoding calculated values
total = df['Sales'].sum()
ws['B10'] = total  # Hardcodes 5000

# ✅ CORRECT - Using Excel formulas
ws['B10'] = '=SUM(B2:B9)'
```

### Formula Placement
- Put ALL assumptions in separate cells
- Use cell references, not hardcoded values
- Example: `=B5*(1+$B$6)` not `=B5*1.05`

### Always Recalculate
```bash
# After creating/modifying Excel file
python scripts/recalc.py output.xlsx

# Check for errors in output JSON
# Fix any errors before delivering
```

## Dependencies

- **pandas** - Data analysis and I/O
- **openpyxl** - Excel file creation/editing
- **LibreOffice** - Formula recalculation (system)

## See Also

- `examples.md` - Comprehensive usage examples
- `README.md` - Installation and setup
