# tests/test_visualization.py

import pandas as pd
import pytest
from src.visualization import plot_correlation_heatmap, plot_time_series, plot_null_values, plot_histogram

@pytest.fixture
def sample_df():
    data = {
        'date': pd.date_range(start='2025-01-01', periods=5),
        'category': ['A', 'B', 'A', 'B', 'C'],
        'value1': [1, 3, 5, 7, 9],
        'value2': [2, 4, None, 8, 10]
    }
    return pd.DataFrame(data)

def test_plot_correlation_heatmap(tmp_path, sample_df):
    save_path = tmp_path / "corr_heatmap.png"
    plot_correlation_heatmap(sample_df, save_path=str(save_path))
    assert save_path.exists()
    assert save_path.stat().st_size > 0

def test_plot_time_series(tmp_path, sample_df):
    save_path = tmp_path / "time_series.png"
    plot_time_series(sample_df, 'date', 'value1', 'category', save_path=str(save_path))
    assert save_path.exists()
    assert save_path.stat().st_size > 0

def test_plot_null_values(tmp_path, sample_df):
    save_path = tmp_path / "null_values.png"
    plot_null_values(sample_df, save_path=str(save_path))
    assert save_path.exists()
    assert save_path.stat().st_size > 0

def test_plot_histogram(tmp_path, sample_df):
    save_path = tmp_path / "histogram.png"
    plot_histogram(sample_df, 'value1', save_path=str(save_path))
    assert save_path.exists()
    assert save_path.stat().st_size > 0
