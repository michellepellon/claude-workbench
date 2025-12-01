"""
Core PDF operations for reading, writing, and manipulating PDF files.

This module provides functions for common PDF operations including:
- Reading and extracting metadata
- Text extraction
- Merging and splitting PDFs
- Error handling for common PDF issues
"""

import os
from typing import Dict, List

from pypdf import PdfReader, PdfWriter


class PDFOperationError(Exception):
    """Raised when a PDF operation fails."""

    pass


def read_pdf(pdf_path: str) -> PdfReader:
    """
    Read a PDF file and return a PdfReader object.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        PdfReader object

    Raises:
        PDFOperationError: If file not found or cannot be read
    """
    if not os.path.exists(pdf_path):
        raise PDFOperationError(
            f"PDF file not found: {pdf_path}"
        )

    try:
        reader = PdfReader(pdf_path)
        return reader
    except Exception as e:
        raise PDFOperationError(
            f"Failed to read PDF: {str(e)}"
        )


def extract_metadata(pdf_path: str) -> Dict[str, any]:
    """
    Extract metadata from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing metadata (pages, title, author, etc.)

    Raises:
        PDFOperationError: If file cannot be read
    """
    reader = read_pdf(pdf_path)

    metadata = {
        "pages": len(reader.pages),
        "title": None,
        "author": None,
        "subject": None,
        "creator": None,
    }

    if reader.metadata:
        metadata["title"] = reader.metadata.title
        metadata["author"] = reader.metadata.author
        metadata["subject"] = reader.metadata.subject
        metadata["creator"] = reader.metadata.creator

    return metadata


def extract_text(pdf_path: str, page_number: int = None) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file
        page_number: Specific page to extract (1-indexed), or None
                     for all pages

    Returns:
        Extracted text as a string

    Raises:
        PDFOperationError: If file cannot be read or page invalid
    """
    reader = read_pdf(pdf_path)

    if page_number is not None:
        if page_number < 1 or page_number > len(reader.pages):
            raise PDFOperationError(
                f"Invalid page number: {page_number}"
            )
        return reader.pages[page_number - 1].extract_text()

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text.strip()


def merge_pdfs(pdf_paths: List[str], output_path: str) -> None:
    """
    Merge multiple PDF files into a single PDF.

    Args:
        pdf_paths: List of paths to PDF files to merge
        output_path: Path where merged PDF will be saved

    Raises:
        PDFOperationError: If input list empty or files cannot be read
    """
    if not pdf_paths:
        raise PDFOperationError(
            "Cannot merge empty list of PDFs"
        )

    writer = PdfWriter()

    for pdf_path in pdf_paths:
        reader = read_pdf(pdf_path)
        for page in reader.pages:
            writer.add_page(page)

    try:
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
    except Exception as e:
        raise PDFOperationError(
            f"Failed to write merged PDF: {str(e)}"
        )


def split_pdf(pdf_path: str, output_dir: str) -> List[str]:
    """
    Split a PDF into individual pages.

    Args:
        pdf_path: Path to the PDF file to split
        output_dir: Directory where split PDFs will be saved

    Returns:
        List of paths to the created PDF files

    Raises:
        PDFOperationError: If output directory invalid or split fails
    """
    if not os.path.exists(output_dir):
        raise PDFOperationError(
            f"Output directory does not exist: {output_dir}"
        )

    if not os.path.isdir(output_dir):
        raise PDFOperationError(
            f"Output path is not a directory: {output_dir}"
        )

    reader = read_pdf(pdf_path)
    output_files = []

    base_name = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    for i, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = os.path.join(
            output_dir, f"{base_name}_page_{i}.pdf"
        )
        try:
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            output_files.append(output_path)
        except Exception as e:
            raise PDFOperationError(
                f"Failed to write page {i}: {str(e)}"
            )

    return output_files
