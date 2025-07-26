import pytest
import pandas as pd
import os
from src.visualization import plot_customer_transactions

def test_plot_customer_transactions_creates_file(tmp_path):
    data = {
        'total_transactions': [1, 2, 3, 4, 5, 5, 3]
    }
    df = pd.DataFrame(data)
    output_file = tmp_path / "histogram.png"
    plot_customer_transactions(df, str(output_file))
    assert output_file.exists()

def test_plot_customer_transactions_empty_df(tmp_path):
    empty_df = pd.DataFrame()
    output_file = tmp_path / "histogram.png"
    plot_customer_transactions(empty_df, str(output_file))
    assert not output_file.exists()
