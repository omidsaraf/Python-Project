"""
Visualization module - Generates Seaborn plots and summary statistics for data insights.

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

def plot_correlation_heatmap(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plots a correlation heatmap of numeric features.
    """
    try:
        corr = df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Correlation Heatmap")
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved correlation heatmap to {save_path}")
        plt.close()
    except Exception as e:
        logger.error(f"Error generating correlation heatmap: {e}")

def plot_time_series(df: pd.DataFrame, date_col: str, value_col: str, group_col: str = None, save_path: str = None) -> None:
    """
    Plots time series trends. Optionally grouped by a categorical column.
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
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved time series plot to {save_path}")
        plt.close()
    except Exception as e:
        logger.error(f"Error generating time series plot: {e}")

def plot_null_values(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plots bar chart of null values count per column.
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
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved null values plot to {save_path}")
        plt.close()
    except Exception as e:
        logger.error(f"Error generating null values plot: {e}")

def plot_histogram(df: pd.DataFrame, col: str, bins: int = 30, save_path: str = None) -> None:
    """
    Plots histogram for a single numeric column.
    """
    try:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), bins=bins, kde=True, color="skyblue")
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved histogram plot to {save_path}")
        plt.close()
    except Exception as e:
        logger.error(f"Error generating histogram for {col}: {e}")
