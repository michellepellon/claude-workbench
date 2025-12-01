# PDF Skill

Comprehensive PDF manipulation toolkit for Claude Code agents.

## Features

- **Read & Extract**: Text, tables, metadata, images
- **Create**: Generate PDFs from scratch with reportlab
- **Manipulate**: Merge, split, rotate, crop PDFs
- **Forms**: Fill both fillable and non-fillable PDF forms
- **Convert**: PDF to images for analysis
- **Error Handling**: Robust error handling for common issues

## Installation

### Prerequisites

- Python 3.10+
- uv package manager
- poppler-utils (for PDF to image conversion)

### macOS
```bash
brew install poppler
```

### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

### Install Dependencies

```bash
cd ~/.claude/skills/documents/pdf
uv sync
```

## Quick Start

### Python API

```python
from scripts.pdf_operations import (
    extract_text,
    merge_pdfs,
    split_pdf
)

# Extract text
text = extract_text("document.pdf")

# Merge PDFs
merge_pdfs(["doc1.pdf", "doc2.pdf"], "merged.pdf")

# Split into pages
files = split_pdf("document.pdf", "output/")
```

### Command-Line Tools

```bash
# Check if PDF has fillable fields
python scripts/check_fillable_fields.py document.pdf

# Convert PDF to images
python scripts/convert_pdf_to_images.py document.pdf output_dir/

# Extract form field information
python scripts/extract_form_field_info.py form.pdf fields.json

# Fill form
python scripts/fill_fillable_fields.py input.pdf values.json output.pdf
```

## Testing

Run the test suite:

```bash
uv run python -m pytest tests/ -v
```

## Documentation

- **[SKILL.md](SKILL.md)** - Quick reference and API overview
- **[examples.md](examples.md)** - Practical usage examples
- **[forms.md](forms.md)** - Complete form filling workflow
- **[reference.md](reference.md)** - Advanced features and troubleshooting

## Dependencies

| Library | Purpose |
|---------|---------|
| pypdf | Core PDF operations |
| pdfplumber | Text and table extraction |
| reportlab | PDF creation |
| pdf2image | Convert PDFs to images |
| poppler-utils | System backend for image conversion |

## Common Tasks

### Merge PDFs
```python
from scripts.pdf_operations import merge_pdfs
merge_pdfs(["file1.pdf", "file2.pdf"], "combined.pdf")
```

### Extract Tables
```python
import pdfplumber
with pdfplumber.open("data.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()
```

### Create PDF
```python
from reportlab.pdfgen import canvas
c = canvas.Canvas("output.pdf")
c.drawString(100, 750, "Hello")
c.save()
```

## Error Handling

All operations raise `PDFOperationError` with descriptive messages:

```python
from scripts.pdf_operations import read_pdf, PDFOperationError

try:
    reader = read_pdf("document.pdf")
except PDFOperationError as e:
    print(f"Failed: {e}")
```

## Contributing

This skill follows strict TDD practices:
1. Write failing test
2. Implement minimal code to pass
3. Refactor while keeping tests green

See `tests/` for examples.

## License

Part of claude-workbench. See [LICENSE](../../LICENSE).
