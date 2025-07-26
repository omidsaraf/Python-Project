"""
Visualization module - Generates Seaborn plots and summary statistics for data insights.
# src/visualization.py

Includes:
- Correlation heatmap
- Time series / trend plots
- Null value bar chart
- Histogram distributions

Author: Senior Data Engineer
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def plot_correlation_heatmap(df: pd.DataFrame, output_path: str = None) -> None:
    """
    Plots and saves a correlation heatmap of numeric features.

    Args:
        df (pd.DataFrame): Input dataframe.
        output_path (str, optional): Path to save the plot image. If None, plot is not saved.
    """
    try:
        plt.figure(figsize=(10, 8))
        corr = df.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Correlation Heatmap")
        plt.tight_layout()

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            logger.info(f"Saved correlation heatmap to {output_path}")

        plt.close()
    except Exception as e:
        logger.error(f"Error generating correlation heatmap: {e}")

def plot_time_series(df: pd.DataFrame, date_col: str, value_col: str, group_col: str = None, output_path: str = None) -> None:
    """
    Plots and saves time series trends, optionally grouped by a categorical column.

    Args:
        df (pd.DataFrame): Input dataframe.
        date_col (str): Column name for dates.
        value_col (str): Column name for values to plot.
        group_col (str, optional): Column name for grouping lines. Defaults to None.
        output_path (str, optional): Path to save the plot image. If None, plot is not saved.
    """
    try:
        plt.figure(figsize=(12, 6))
        if group_col and group_col in df.columns:
            sns.lineplot(data=df, x=date_col, y=value_col, hue=group_col, marker='o')
        else:
            sns.lineplot(data=df, x=date_col, y=value_col, marker='o')
        plt.title(f"Time Series Trend of {value_col}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            logger.info(f"Saved time series plot to {output_path}")

        plt.close()
    except Exception as e:
        logger.error(f"Error generating time series plot: {e}")

def plot_null_values(df: pd.DataFrame, output_path: str = None) -> None:
    """
    Plots and saves a bar chart showing count of null values per column.

    Args:
        df (pd.DataFrame): Input dataframe.
        output_path (str, optional): Path to save the plot image. If None, plot is not saved.
    """
    try:
        null_counts = df.isnull().sum()
        null_counts = null_counts[null_counts > 0].sort_values(ascending=False)

        if null_counts.empty:
            logger.info("No null values to plot.")
            return

        plt.figure(figsize=(10, 6))
        sns.barplot(x=null_counts.index, y=null_counts.values, palette="viridis")
        plt.title("Null Values per Column")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            logger.info(f"Saved null values plot to {output_path}")

        plt.close()
    except Exception as e:
        logger.error(f"Error generating null values plot: {e}")

def plot_histogram(df: pd.DataFrame, col: str, bins: int = 30, output_path: str = None) -> None:
    """
    Plots and saves a histogram for a single numeric column.

    Args:
        df (pd.DataFrame): Input dataframe.
        col (str): Column name to plot.
        bins (int, optional): Number of histogram bins. Defaults to 30.
        output_path (str, optional): Path to save the plot image. If None, plot is not saved.
    """
    try:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), bins=bins, kde=True, color="skyblue")
        plt.title(f"Distribution of {col}")
        plt.tight_layout()

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            logger.info(f"Saved histogram plot to {output_path}")

        plt.close()
    except Exception as e:
        logger.error(f"Error generating histogram for {col}: {e}")

def generate_visualizations(df: pd.DataFrame, output_dir: str) -> None:
    """
    Helper to generate all key visualizations and save them to output directory.

    Args:
        df (pd.DataFrame): Data to visualize.
        output_dir (str): Directory to save plot images.
    """
    plot_correlation_heatmap(df, output_path=f"{output_dir}/correlation_heatmap.png")

    # Example time series plot (needs 'date' and a numeric column)
    if 'date' in df.columns:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            plot_time_series(df, date_col='date', value_col=numeric_cols[0], output_path=f"{output_dir}/time_series.png")

    plot_null_values(df, output_path=f"{output_dir}/null_values.png")

    # Example histogram for first numeric column
    if numeric_cols:
        plot_histogram(df, col=numeric_cols[0], output_path=f"{output_dir}/histogram.png")
