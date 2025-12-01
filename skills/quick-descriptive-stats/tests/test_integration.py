"""
Integration tests for complete CSV analysis workflow.

Tests the full summarize_csv orchestration.
"""

import pytest
from pathlib import Path
from analyze import summarize_csv


def test_summarize_csv_with_valid_sales_data(tmp_path):
    """
    Verify complete analysis workflow with valid sales CSV.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "valid_sales.csv"

    report = summarize_csv(str(fixture_path), str(tmp_path))

    assert isinstance(report, str)
    assert "DATA OVERVIEW" in report
    assert "DATA QUALITY" in report
    assert "NUMERICAL ANALYSIS" in report
    assert "VISUALIZATIONS CREATED" in report
    assert len(report) > 0


def test_summarize_csv_creates_visualizations(tmp_path):
    """
    Verify visualizations are created in output directory.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "valid_sales.csv"

    summarize_csv(str(fixture_path), str(tmp_path))

    # Check for expected visualization files
    expected_files = [
        "correlation_heatmap.png",
        "time_series_analysis.png",
        "distributions.png",
        "categorical_distributions.png"
    ]

    for filename in expected_files:
        filepath = tmp_path / filename
        assert filepath.exists(), f"Expected {filename} to be created"


def test_summarize_csv_with_numeric_only_data(tmp_path):
    """
    Verify analysis handles numeric-only datasets.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "numeric_only.csv"

    report = summarize_csv(str(fixture_path), str(tmp_path))

    assert "NUMERICAL ANALYSIS" in report
    assert "CORRELATIONS" in report
    # Should have correlation heatmap and distributions
    assert (tmp_path / "correlation_heatmap.png").exists()
    assert (tmp_path / "distributions.png").exists()
