import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).parent.parent / "scripts")
)

from pdf_operations import (
    read_pdf,
    extract_metadata,
    extract_text,
    merge_pdfs,
    split_pdf,
    PDFOperationError,
)


class TestPDFBasicOperations(unittest.TestCase):
    """Test basic PDF reading and manipulation operations."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.sample_pdf = self._create_sample_pdf()

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        import shutil

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def _create_sample_pdf(self):
        """Create a simple test PDF with reportlab."""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        pdf_path = os.path.join(self.test_dir, "sample.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, "Test Page 1")
        c.showPage()
        c.drawString(100, 750, "Test Page 2")
        c.save()
        return pdf_path

    def test_read_pdf_success(self):
        """Test reading a valid PDF file."""
        reader = read_pdf(self.sample_pdf)
        self.assertIsNotNone(reader)
        self.assertEqual(len(reader.pages), 2)

    def test_read_pdf_file_not_found(self):
        """Test reading a non-existent PDF file."""
        with self.assertRaises(PDFOperationError) as context:
            read_pdf("nonexistent.pdf")
        self.assertIn("not found", str(context.exception).lower())

    def test_extract_metadata_success(self):
        """Test extracting metadata from a PDF."""
        metadata = extract_metadata(self.sample_pdf)
        self.assertIsInstance(metadata, dict)
        self.assertIn("pages", metadata)
        self.assertEqual(metadata["pages"], 2)

    def test_extract_text_success(self):
        """Test extracting text from a PDF."""
        text = extract_text(self.sample_pdf)
        self.assertIsInstance(text, str)
        self.assertIn("Test Page 1", text)
        self.assertIn("Test Page 2", text)

    def test_extract_text_from_page(self):
        """Test extracting text from a specific page."""
        text = extract_text(self.sample_pdf, page_number=1)
        self.assertIn("Test Page 1", text)
        self.assertNotIn("Test Page 2", text)

    def test_merge_pdfs_success(self):
        """Test merging multiple PDF files."""
        pdf2_path = os.path.join(self.test_dir, "sample2.pdf")
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        c = canvas.Canvas(pdf2_path, pagesize=letter)
        c.drawString(100, 750, "Test Page 3")
        c.save()

        output_path = os.path.join(self.test_dir, "merged.pdf")
        merge_pdfs([self.sample_pdf, pdf2_path], output_path)

        self.assertTrue(os.path.exists(output_path))
        reader = read_pdf(output_path)
        self.assertEqual(len(reader.pages), 3)

    def test_merge_pdfs_empty_list(self):
        """Test merging with empty list of PDFs."""
        output_path = os.path.join(self.test_dir, "merged.pdf")
        with self.assertRaises(PDFOperationError) as context:
            merge_pdfs([], output_path)
        self.assertIn("empty", str(context.exception).lower())

    def test_split_pdf_success(self):
        """Test splitting a PDF into individual pages."""
        output_dir = os.path.join(self.test_dir, "split")
        os.makedirs(output_dir)

        files = split_pdf(self.sample_pdf, output_dir)

        self.assertEqual(len(files), 2)
        self.assertTrue(
            all(os.path.exists(f) for f in files)
        )

        for i, file_path in enumerate(files, 1):
            reader = read_pdf(file_path)
            self.assertEqual(len(reader.pages), 1)

    def test_split_pdf_invalid_output_dir(self):
        """Test splitting PDF with invalid output directory."""
        with self.assertRaises(PDFOperationError) as context:
            split_pdf(
                self.sample_pdf, "/nonexistent/path"
            )
        self.assertIn("directory", str(context.exception).lower())


if __name__ == "__main__":
    unittest.main()
