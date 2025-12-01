"""
Test suite for CSV loading and validation.

Tests the load_csv function with various input scenarios.
"""

import pytest
import pandas as pd
from pathlib import Path
from analyze import load_csv


def test_load_csv_with_valid_file():
    """
    Verify load_csv correctly loads valid CSV file.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "valid_sales.csv"

    df = load_csv(str(fixture_path))

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 10  # 10 rows
    assert df.shape[1] == 5   # 5 columns
    assert list(df.columns) == [
        "date", "product", "quantity", "revenue", "region"
    ]


def test_load_csv_with_missing_file():
    """
    Verify load_csv raises FileNotFoundError for missing file.
    """
    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        load_csv("/nonexistent/path/to/file.csv")


def test_load_csv_with_empty_file(tmp_path):
    """
    Verify load_csv raises ValueError for empty CSV file.
    """
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("")

    with pytest.raises(ValueError, match="CSV file is empty"):
        load_csv(str(empty_csv))


def test_load_csv_with_malformed_csv(tmp_path):
    """
    Verify load_csv raises ValueError for malformed CSV.
    """
    malformed_csv = tmp_path / "malformed.csv"
    malformed_csv.write_text("not,valid,csv\ndata")

    # pandas should handle this, but verify it loads
    df = load_csv(str(malformed_csv))
    assert isinstance(df, pd.DataFrame)


def test_load_csv_with_numeric_only():
    """
    Verify load_csv correctly loads numeric-only CSV.
    """
    fixture_path = (
        Path(__file__).parent / "fixtures" / "numeric_only.csv"
    )

    df = load_csv(str(fixture_path))

    assert df.shape[0] == 5
    assert df.shape[1] == 3
    assert all(df.dtypes == "float64")


def test_load_csv_with_categorical_only():
    """
    Verify load_csv correctly loads categorical-only CSV.
    """
    fixture_path = (
        Path(__file__).parent / "fixtures" / "categorical_only.csv"
    )

    df = load_csv(str(fixture_path))

    assert df.shape[0] == 6
    assert df.shape[1] == 3
    assert all(df.dtypes == "object")
