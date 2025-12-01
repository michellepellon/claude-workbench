"""
Test suite for data quality analysis.

Tests the analyze_data_quality function with various data scenarios.
"""

import pytest
import pandas as pd
from pathlib import Path
from analyze import load_csv, analyze_data_quality


def test_analyze_data_quality_with_no_missing_values():
    """
    Verify data quality analysis with complete dataset.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "valid_sales.csv"
    df = load_csv(str(fixture_path))

    quality = analyze_data_quality(df)

    assert quality["total_missing"] == 0
    assert quality["missing_percentage"] == 0.0
    assert quality["is_complete"] is True
    assert quality["missing_by_column"] == {}


def test_analyze_data_quality_with_missing_values():
    """
    Verify data quality analysis detects missing values.
    """
    fixture_path = (
        Path(__file__).parent / "fixtures" / "missing_values.csv"
    )
    df = load_csv(str(fixture_path))

    quality = analyze_data_quality(df)

    assert quality["total_missing"] == 4
    assert quality["missing_percentage"] > 0
    assert quality["is_complete"] is False
    assert len(quality["missing_by_column"]) > 0


def test_analyze_data_quality_with_all_missing_column():
    """
    Verify data quality analysis handles column with all missing values.
    """
    df = pd.DataFrame({
        "col_a": [1, 2, 3],
        "col_b": [None, None, None],
        "col_c": ["x", "y", "z"]
    })

    quality = analyze_data_quality(df)

    assert quality["total_missing"] == 3
    assert quality["is_complete"] is False
    assert "col_b" in quality["missing_by_column"]
    assert quality["missing_by_column"]["col_b"]["count"] == 3
    assert quality["missing_by_column"]["col_b"]["percentage"] == 100.0
