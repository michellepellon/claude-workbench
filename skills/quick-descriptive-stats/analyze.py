"""
Quick descriptive statistics and exploratory data analysis for CSV files.

This module provides functions to automatically analyze CSV files and
generate comprehensive statistical insights with visualizations.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Constants
DEFAULT_BINS: int = 30
DEFAULT_DPI: int = 150
MAX_CATEGORIES_DISPLAY: int = 10
MAX_CATEGORICAL_PLOTS: int = 4
MAX_NUMERIC_PLOTS: int = 4
MAX_TIMESERIES_PLOTS: int = 3


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load CSV file with error handling and validation.

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame containing CSV data

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV file is empty or cannot be parsed
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    if path.stat().st_size == 0:
        raise ValueError("CSV file is empty")

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except Exception as e:
        raise ValueError(f"Failed to parse CSV file: {e}")

    return df


def analyze_data_quality(df: pd.DataFrame) -> Dict[str, any]:
    """
    Analyze data quality and detect missing values.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary containing:
        - total_missing: Total number of missing values
        - missing_percentage: Percentage of missing values
        - is_complete: True if no missing values
        - missing_by_column: Dict of columns with missing values
    """
    total_cells = df.shape[0] * df.shape[1]
    total_missing = df.isnull().sum().sum()
    missing_percentage = (
        (total_missing / total_cells * 100) if total_cells > 0 else 0.0
    )

    missing_by_column = {}
    for col in df.columns:
        col_missing = df[col].isnull().sum()
        if col_missing > 0:
            col_pct = (col_missing / len(df)) * 100
            missing_by_column[col] = {
                "count": int(col_missing),
                "percentage": round(col_pct, 1)
            }

    return {
        "total_missing": int(total_missing),
        "missing_percentage": round(missing_percentage, 2),
        "is_complete": bool(total_missing == 0),
        "missing_by_column": missing_by_column
    }


def compute_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Compute summary statistics for numeric columns.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary mapping column names to statistics
        (mean, std, min, 25%, 50%, 75%, max)
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        return {}

    stats = {}
    for col in numeric_cols:
        desc = df[col].describe()
        stats[col] = {
            "mean": round(desc["mean"], 2),
            "std": round(desc["std"], 2),
            "min": round(desc["min"], 2),
            "25%": round(desc["25%"], 2),
            "50%": round(desc["50%"], 2),
            "75%": round(desc["75%"], 2),
            "max": round(desc["max"], 2)
        }

    return stats


def analyze_correlations(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Compute correlation matrix for numeric columns.

    Args:
        df: DataFrame to analyze

    Returns:
        Correlation matrix if multiple numeric columns exist,
        None otherwise
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) < 2:
        return None

    return df[numeric_cols].corr()


def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    output_path: str
) -> None:
    """
    Generate correlation heatmap visualization.

    Args:
        corr_matrix: Correlation matrix DataFrame
        output_path: Path to save visualization
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=1
    )
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_path, dpi=DEFAULT_DPI)
    plt.close()


def create_time_series_plots(
    df: pd.DataFrame,
    output_dir: str
) -> List[str]:
    """
    Generate time-series visualizations if date columns exist.

    Args:
        df: DataFrame to visualize
        output_dir: Directory for output files

    Returns:
        List of paths to created visualizations
    """
    date_cols = [
        c for c in df.columns
        if "date" in c.lower() or "time" in c.lower()
    ]

    if not date_cols:
        return []

    date_col = date_cols[0]
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors="coerce")

    numeric_cols = (
        df_copy.select_dtypes(include="number").columns.tolist()
    )
    if not numeric_cols:
        return []

    output_path = f"{output_dir}/time_series_analysis.png"
    n_plots = min(MAX_TIMESERIES_PLOTS, len(numeric_cols))

    fig, axes = plt.subplots(n_plots, 1, figsize=(12, 4 * n_plots))
    if n_plots == 1:
        axes = [axes]

    for idx, num_col in enumerate(numeric_cols[:n_plots]):
        ax = axes[idx]
        daily_data = (
            df_copy.groupby(date_col)[num_col]
            .agg(["mean", "sum", "count"])
        )
        daily_data["mean"].plot(ax=ax, label="Average", linewidth=2)
        ax.set_title(f"{num_col} Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel(num_col)
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=DEFAULT_DPI)
    plt.close()

    return [output_path]


def create_distribution_plots(
    df: pd.DataFrame,
    output_dir: str
) -> List[str]:
    """
    Generate distribution histograms for numeric columns.

    Args:
        df: DataFrame to visualize
        output_dir: Directory for output files

    Returns:
        List of paths to created visualizations
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        return []

    output_path = f"{output_dir}/distributions.png"
    n_cols = min(MAX_NUMERIC_PLOTS, len(numeric_cols))

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, col in enumerate(numeric_cols[:n_cols]):
        axes[idx].hist(
            df[col].dropna(),
            bins=DEFAULT_BINS,
            edgecolor="black",
            alpha=0.7
        )
        axes[idx].set_title(f"Distribution of {col}")
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel("Frequency")
        axes[idx].grid(True, alpha=0.3)

    # Hide unused subplots
    for idx in range(n_cols, 4):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=DEFAULT_DPI)
    plt.close()

    return [output_path]


def create_categorical_plots(
    df: pd.DataFrame,
    output_dir: str
) -> List[str]:
    """
    Generate categorical distribution bar charts.

    Args:
        df: DataFrame to visualize
        output_dir: Directory for output files

    Returns:
        List of paths to created visualizations
    """
    categorical_cols = (
        df.select_dtypes(include=["object"]).columns.tolist()
    )
    categorical_cols = [
        c for c in categorical_cols if "id" not in c.lower()
    ]

    if not categorical_cols:
        return []

    output_path = f"{output_dir}/categorical_distributions.png"
    n_cols = min(MAX_CATEGORICAL_PLOTS, len(categorical_cols))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, col in enumerate(categorical_cols[:n_cols]):
        value_counts = df[col].value_counts().head(MAX_CATEGORIES_DISPLAY)
        axes[idx].barh(range(len(value_counts)), value_counts.values)
        axes[idx].set_yticks(range(len(value_counts)))
        axes[idx].set_yticklabels(value_counts.index)
        axes[idx].set_title(f"Top Values in {col}")
        axes[idx].set_xlabel("Count")
        axes[idx].grid(True, alpha=0.3, axis="x")

    # Hide unused subplots
    for idx in range(n_cols, 4):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=DEFAULT_DPI)
    plt.close()

    return [output_path]


def format_summary_report(
    df: pd.DataFrame,
    quality: Dict,
    stats: Dict,
    corr: Optional[pd.DataFrame],
    charts: List[str]
) -> str:
    """
    Format comprehensive analysis report.

    Args:
        df: Original DataFrame
        quality: Data quality analysis results
        stats: Statistical analysis results
        corr: Correlation matrix (if available)
        charts: List of created visualizations

    Returns:
        Formatted report string
    """
    summary = []

    # Header
    summary.append("=" * 60)
    summary.append("📊 DATA OVERVIEW")
    summary.append("=" * 60)
    summary.append(
        f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}"
    )
    summary.append(
        f"\nColumns: {', '.join(df.columns.tolist())}"
    )

    # Data types
    summary.append("\n📋 DATA TYPES:")
    for col, dtype in df.dtypes.items():
        summary.append(f"  • {col}: {dtype}")

    # Data quality
    summary.append("\n🔍 DATA QUALITY:")
    if quality["is_complete"]:
        summary.append(
            "✓ No missing values - dataset is complete!"
        )
    else:
        summary.append(
            f"Missing values: {quality['total_missing']:,} "
            f"({quality['missing_percentage']:.2f}% of total data)"
        )
        summary.append("Missing by column:")
        for col, info in quality["missing_by_column"].items():
            summary.append(
                f"  • {col}: {info['count']:,} "
                f"({info['percentage']:.1f}%)"
            )

    # Statistics
    if stats:
        summary.append("\n📈 NUMERICAL ANALYSIS:")
        for col, col_stats in stats.items():
            summary.append(f"\n{col}:")
            summary.append(f"  • Mean: {col_stats['mean']}")
            summary.append(f"  • Std Dev: {col_stats['std']}")
            summary.append(
                f"  • Range: {col_stats['min']} - {col_stats['max']}"
            )
            summary.append(f"  • Median: {col_stats['50%']}")

    # Correlations
    if corr is not None:
        summary.append("\n🔗 CORRELATIONS:")
        summary.append(str(corr))

    # Visualizations
    if charts:
        summary.append("\n📊 VISUALIZATIONS CREATED:")
        for chart in charts:
            summary.append(f"  ✓ {Path(chart).name}")

    summary.append("\n" + "=" * 60)
    summary.append("✅ COMPREHENSIVE ANALYSIS COMPLETE")
    summary.append("=" * 60)

    return "\n".join(summary)


def summarize_csv(file_path: str, output_dir: str = ".") -> str:
    """
    Generate comprehensive analysis of CSV file.

    Main entry point that orchestrates all analysis functions.

    Args:
        file_path: Path to CSV file
        output_dir: Directory for output visualizations (default: ".")

    Returns:
        Formatted analysis report

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV file is empty or malformed
    """
    # Load data
    df = load_csv(file_path)

    # Analyze data quality
    quality = analyze_data_quality(df)

    # Compute statistics
    stats = compute_statistics(df)

    # Analyze correlations
    corr = analyze_correlations(df)

    # Generate visualizations
    charts = []

    # Correlation heatmap
    if corr is not None:
        heatmap_path = f"{output_dir}/correlation_heatmap.png"
        create_correlation_heatmap(corr, heatmap_path)
        charts.append(heatmap_path)

    # Time-series plots
    charts.extend(create_time_series_plots(df, output_dir))

    # Distribution plots
    charts.extend(create_distribution_plots(df, output_dir))

    # Categorical plots
    charts.extend(create_categorical_plots(df, output_dir))

    # Format and return report
    return format_summary_report(df, quality, stats, corr, charts)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else "."
    else:
        print("Usage: python analyze.py <csv_file> [output_dir]")
        sys.exit(1)

    print(summarize_csv(csv_path, output))
