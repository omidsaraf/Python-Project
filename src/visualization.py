# src/visualization.py

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def plot_correlation_heatmap(df: pd.DataFrame, output_path: str) -> None:
    plt.figure(figsize=(10,8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Saved correlation heatmap to {output_path}")

def plot_time_series(df: pd.DataFrame, time_col: str, value_col: str, output_path: str) -> None:
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df, x=time_col, y=value_col)
    plt.title(f'{value_col} Over Time')
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Saved time series plot to {output_path}")
