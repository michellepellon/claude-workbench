---
name: workbench:pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. Use when you need to programmatically process, generate, or analyze PDF documents.
when_to_use: When extracting text or tables from PDFs. When merging or splitting PDF files. When creating PDFs programmatically. When filling PDF forms. When converting PDFs to images. When processing PDFs at scale.
allowed-tools: Read, Write, Bash
---

# PDF Processing

**Announce at start:** "I'm using the pdf skill to process PDF documents."

## Quick Start

Basic operations available through `pdf_operations.py`:

```python
from pdf_operations import (
    read_pdf,
    extract_metadata,
    extract_text,
    merge_pdfs,
    split_pdf
)

# Read PDF
reader = read_pdf("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = extract_text("document.pdf")
text_page_1 = extract_text("document.pdf", page_number=1)

# Extract metadata
metadata = extract_metadata("document.pdf")
print(f"Title: {metadata['title']}")

# Merge PDFs
merge_pdfs(["doc1.pdf", "doc2.pdf"], "merged.pdf")

# Split PDF into individual pages
split_pdf("document.pdf", "output_dir/")
```

## Form Filling

Check if PDF has fillable fields:
```bash
python scripts/check_fillable_fields.py document.pdf
```

For fillable forms:
1. Extract field info: `python scripts/extract_form_field_info.py input.pdf fields.json`
2. Create field values JSON
3. Fill form: `python scripts/fill_fillable_fields.py input.pdf values.json output.pdf`

For non-fillable forms, see `forms.md` for complete workflow.

## Advanced Operations

### Text and Table Extraction
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        # Extract text
        text = page.extract_text()

        # Extract tables
        tables = page.extract_tables()
```

### PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=letter)
c.drawString(100, 750, "Hello World!")
c.save()
```

### Command-Line Tools

Convert PDF to images:
```bash
python scripts/convert_pdf_to_images.py document.pdf output_dir/
```

## Error Handling

All operations raise `PDFOperationError` for:
- File not found
- Invalid page numbers
- Empty merge lists
- Invalid output directories
- Corrupted PDFs

## Dependencies

- pypdf - PDF reading/writing/merging
- pdfplumber - Text and table extraction
- reportlab - PDF creation
- pdf2image - Convert PDFs to images
- poppler-utils (system) - Image conversion backend

## Documentation

- `forms.md` - Complete form filling workflow
- `reference.md` - Advanced features and troubleshooting
- `examples.md` - Usage examples
- `README.md` - Installation and setup
