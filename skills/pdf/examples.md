# PDF Skill Examples

## Basic Operations

### Extract Text from PDF
```python
from scripts.pdf_operations import extract_text

# Extract all text
full_text = extract_text("document.pdf")
print(full_text)

# Extract specific page
page_1_text = extract_text("document.pdf", page_number=1)
```

### Merge Multiple PDFs
```python
from scripts.pdf_operations import merge_pdfs

pdf_files = ["intro.pdf", "chapter1.pdf", "chapter2.pdf", "conclusion.pdf"]
merge_pdfs(pdf_files, "complete_book.pdf")
```

### Split PDF into Pages
```python
from scripts.pdf_operations import split_pdf

files = split_pdf("report.pdf", "pages/")
print(f"Created {len(files)} page files")
```

### Extract Metadata
```python
from scripts.pdf_operations import extract_metadata

metadata = extract_metadata("document.pdf")
print(f"Title: {metadata['title']}")
print(f"Author: {metadata['author']}")
print(f"Pages: {metadata['pages']}")
```

## Table Extraction

### Extract Tables from PDF
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("financial_report.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Save to Excel
if all_tables:
    combined = pd.concat(all_tables, ignore_index=True)
    combined.to_excel("extracted_data.xlsx", index=False)
```

## PDF Creation

### Simple Document
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "Created with reportlab")
c.save()
```

### Multi-Page Report
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

title = Paragraph("Annual Report", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("Report content here...", styles['Normal'])
story.append(body)

doc.build(story)
```

## Form Filling

### Check for Fillable Fields
```bash
python scripts/check_fillable_fields.py application.pdf
```

### Extract Field Information
```bash
python scripts/extract_form_field_info.py application.pdf field_info.json
```

### Fill Form Fields
Create `field_values.json`:
```json
[
  {
    "field_id": "first_name",
    "description": "Applicant's first name",
    "page": 1,
    "value": "John"
  },
  {
    "field_id": "last_name",
    "description": "Applicant's last name",
    "page": 1,
    "value": "Doe"
  }
]
```

Fill the form:
```bash
python scripts/fill_fillable_fields.py application.pdf field_values.json completed_application.pdf
```

## PDF to Images

### Convert All Pages
```bash
python scripts/convert_pdf_to_images.py presentation.pdf slides/
```

Output: `slides/page_1.png`, `slides/page_2.png`, etc.

## Advanced Use Cases

### Batch Process PDFs
```python
import glob
from scripts.pdf_operations import extract_text

for pdf_file in glob.glob("documents/*.pdf"):
    text = extract_text(pdf_file)
    output_file = pdf_file.replace('.pdf', '.txt')
    with open(output_file, 'w') as f:
        f.write(text)
```

### Extract Specific Page Range
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("full_document.pdf")
writer = PdfWriter()

# Extract pages 5-10
for page_num in range(4, 10):
    writer.add_page(reader.pages[page_num])

with open("excerpt.pdf", "wb") as output:
    writer.write(output)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

## Error Handling

```python
from scripts.pdf_operations import read_pdf, PDFOperationError

try:
    reader = read_pdf("document.pdf")
    print(f"Successfully read {len(reader.pages)} pages")
except PDFOperationError as e:
    print(f"Error: {e}")
```

## See Also

- [SKILL.md](SKILL.md) - Complete skill reference
- [forms.md](forms.md) - Form filling workflow
- [reference.md](reference.md) - Advanced features
