# XLSX Skill Examples

## Reading Excel Files

### Basic Reading
```python
from scripts.xlsx_operations import read_excel

# Read first sheet
df = read_excel('data.xlsx')
print(df.head())

# Read specific sheet
df = read_excel('data.xlsx', sheet_name='Q1Sales')
```

### Read Multiple Sheets
```python
import pandas as pd

# Read all sheets into dictionary
sheets = pd.read_excel('report.xlsx', sheet_name=None)

for sheet_name, df in sheets.items():
    print(f"\n{sheet_name}:")
    print(df.head())
```

## Creating Excel Files

### Simple Spreadsheet
```python
from scripts.xlsx_operations import write_dataframe
import pandas as pd

df = pd.DataFrame({
    'Product': ['Widget', 'Gadget', 'Doohickey'],
    'Price': [10.99, 24.99, 5.99],
    'Quantity': [100, 50, 200]
})

write_dataframe(df, 'inventory.xlsx')
```

### With Formulas
```python
from openpyxl import Workbook
from scripts.xlsx_operations import add_formula, set_cell_color

wb = Workbook()
ws = wb.active

# Headers
ws['A1'] = 'Product'
ws['B1'] = 'Unit Price'
ws['C1'] = 'Quantity'
ws['D1'] = 'Total'

# Data (BLUE for inputs)
ws['A2'] = 'Widget'
ws['B2'] = 10.99
ws['C2'] = 100
set_cell_color(ws, 'B2', 'blue')
set_cell_color(ws, 'C2', 'blue')

# Formula (BLACK for formulas)
add_formula(ws, 'D2', '=B2*C2')
set_cell_color(ws, 'D2', 'black')

wb.save('sales.xlsx')
```

## Financial Models

### Revenue Projection
```python
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active

# Years header
ws['A1'] = 'Metric'
ws['B1'] = '2024'
ws['C1'] = '2025'
ws['D1'] = '2026'

# Base revenue (BLUE - input)
ws['A2'] = 'Revenue'
ws['B2'] = 1000000
ws['B2'].font = Font(color='000000FF')

# Growth rate assumption (BLUE - input)
ws['A3'] = 'Growth Rate'
ws['B3'] = 0.15
ws['B3'].font = Font(color='000000FF')

# Projected revenue (BLACK - formulas)
ws['C2'] = '=B2*(1+$B$3)'
ws['D2'] = '=C2*(1+$B$3)'
ws['C2'].font = Font(color='00000000')
ws['D2'].font = Font(color='00000000')

wb.save('revenue_projection.xlsx')
```

### Income Statement
```python
from openpyxl import Workbook
from scripts.xlsx_operations import add_formula, set_cell_color

wb = Workbook()
ws = wb.active

# Headers
ws['A1'] = 'Income Statement'
ws['B1'] = 'FY2024'

# Revenue (input - BLUE)
ws['A2'] = 'Revenue'
ws['B2'] = 5000000
set_cell_color(ws, 'B2', 'blue')

# COGS as % of revenue (input - BLUE)
ws['A3'] = 'COGS %'
ws['B3'] = 0.60
set_cell_color(ws, 'B3', 'blue')

# Calculated COGS (formula - BLACK)
ws['A4'] = 'COGS'
add_formula(ws, 'B4', '=B2*B3')
set_cell_color(ws, 'B4', 'black')

# Gross Profit (formula - BLACK)
ws['A5'] = 'Gross Profit'
add_formula(ws, 'B5', '=B2-B4')
set_cell_color(ws, 'B5', 'black')

wb.save('income_statement.xlsx')
```

## Data Analysis

### Sales Analysis
```python
import pandas as pd
from scripts.xlsx_operations import write_dataframe

# Read data
df = pd.read_excel('sales_raw.xlsx')

# Analysis
summary = df.groupby('Region').agg({
    'Sales': ['sum', 'mean', 'count'],
    'Profit': 'sum'
})

# Write results
write_dataframe(summary, 'sales_summary.xlsx')
```

### Pivot Table
```python
import pandas as pd

df = pd.read_excel('transactions.xlsx')

# Create pivot table
pivot = pd.pivot_table(
    df,
    values='Amount',
    index='Category',
    columns='Month',
    aggfunc='sum',
    fill_value=0
)

pivot.to_excel('monthly_by_category.xlsx')
```

## Advanced Formatting

### Number Formats
```python
from openpyxl import Workbook
from openpyxl.styles import numbers

wb = Workbook()
ws = wb.active

# Currency
ws['A1'] = 1234.56
ws['A1'].number_format = '$#,##0.00'

# Percentage
ws['A2'] = 0.1234
ws['A2'].number_format = '0.0%'

# Date
ws['A3'] = '2024-01-15'
ws['A3'].number_format = 'yyyy-mm-dd'

# Show zeros as dash
ws['A4'] = 0
ws['A4'].number_format = '#,##0;(#,##0);-'

wb.save('formatted_numbers.xlsx')
```

### Conditional Formatting
```python
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active

# Add data
for i in range(1, 11):
    ws[f'A{i}'] = i * 10

# Highlight values > 50
red_fill = PatternFill(
    start_color='FFFF0000',
    end_color='FFFF0000',
    fill_type='solid'
)

ws.conditional_formatting.add(
    'A1:A10',
    CellIsRule(
        operator='greaterThan',
        formula=['50'],
        fill=red_fill
    )
)

wb.save('conditional.xlsx')
```

## Formula Recalculation

### Basic Recalculation
```bash
# Create Excel file with formulas
python scripts/create_model.py

# Recalculate all formulas
python scripts/recalc.py model.xlsx

# Check output for errors
# {"status": "success", "total_errors": 0, ...}
```

### Error Detection
```python
import json
import subprocess

# Recalculate and check for errors
result = subprocess.run(
    ['python', 'scripts/recalc.py', 'model.xlsx'],
    capture_output=True,
    text=True
)

output = json.loads(result.stdout)

if output['status'] == 'errors_found':
    print(f"Found {output['total_errors']} errors:")
    for error_type, details in output['error_summary'].items():
        print(f"\n{error_type}: {details['count']} occurrences")
        for location in details['locations']:
            print(f"  - {location}")
```

## Multi-Sheet Workbooks

### Create Multiple Sheets
```python
from openpyxl import Workbook
import pandas as pd

wb = Workbook()

# Remove default sheet
wb.remove(wb.active)

# Add multiple sheets
for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
    ws = wb.create_sheet(title=quarter)
    ws['A1'] = f'{quarter} Sales'
    ws['A2'] = 'Product'
    ws['B2'] = 'Revenue'

wb.save('quarterly_sales.xlsx')
```

### Link Between Sheets
```python
from openpyxl import Workbook
from scripts.xlsx_operations import set_cell_color

wb = Workbook()

# Sheet 1: Quarterly data
ws1 = wb.active
ws1.title = 'Q1'
ws1['A1'] = 'Q1 Revenue'
ws1['B1'] = 100000

# Sheet 2: Summary (GREEN for internal links)
ws2 = wb.create_sheet('Summary')
ws2['A1'] = 'Total Revenue'
ws2['B1'] = '=Q1!B1'
set_cell_color(ws2, 'B1', 'green')

wb.save('linked_sheets.xlsx')
```

## Error Handling

### Robust Reading
```python
from scripts.xlsx_operations import read_excel, ExcelOperationError

try:
    df = read_excel('data.xlsx')
    print(f"Loaded {len(df)} rows")
except ExcelOperationError as e:
    print(f"Failed to read file: {e}")
    # Handle error appropriately
```

## See Also

- [SKILL.md](SKILL.md) - Complete skill reference
- [README.md](README.md) - Installation guide
