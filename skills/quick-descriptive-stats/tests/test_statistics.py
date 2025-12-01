"""
Test suite for statistical analysis functions.

Tests compute_statistics and analyze_correlations functions.
"""

import pytest
import pandas as pd
from pathlib import Path
from analyze import (
    load_csv,
    compute_statistics,
    analyze_correlations
)


def test_compute_statistics_with_numeric_columns():
    """
    Verify statistics computation for numeric columns.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "valid_sales.csv"
    df = load_csv(str(fixture_path))

    stats = compute_statistics(df)

    assert "quantity" in stats
    assert "revenue" in stats
    assert "mean" in stats["quantity"]
    assert "std" in stats["quantity"]
    assert "min" in stats["quantity"]
    assert "max" in stats["quantity"]


def test_compute_statistics_with_no_numeric_columns():
    """
    Verify statistics returns empty dict for non-numeric data.
    """
    fixture_path = (
        Path(__file__).parent / "fixtures" / "categorical_only.csv"
    )
    df = load_csv(str(fixture_path))

    stats = compute_statistics(df)

    assert stats == {}


def test_analyze_correlations_with_multiple_numeric():
    """
    Verify correlation analysis with multiple numeric columns.
    """
    fixture_path = (
        Path(__file__).parent / "fixtures" / "numeric_only.csv"
    )
    df = load_csv(str(fixture_path))

    corr = analyze_correlations(df)

    assert corr is not None
    assert isinstance(corr, pd.DataFrame)
    assert corr.shape[0] == 3  # 3x3 matrix
    assert corr.shape[1] == 3


def test_analyze_correlations_with_single_numeric():
    """
    Verify correlation returns None for single numeric column.
    """
    df = pd.DataFrame({"col_a": [1, 2, 3, 4, 5]})

    corr = analyze_correlations(df)

    assert corr is None
