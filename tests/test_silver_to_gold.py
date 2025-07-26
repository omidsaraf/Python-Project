import pytest
import pandas as pd
from src.silver_to_gold import aggregate_customer_data

def test_aggregate_customer_data():
    data = {
        'customer_id': [1, 1, 2],
        'transaction_id': [101, 102, 201],
        'transaction_value': [10.0, 20.0, 30.0]
    }
    df = pd.DataFrame(data)
    aggregated = aggregate_customer_data(df)
    assert len(aggregated) == 2
    assert 'total_transactions' in aggregated.columns
    assert aggregated.loc[aggregated['customer_id'] == 1, 'total_transactions'].iloc[0] == 2
    assert round(aggregated.loc[aggregated['customer_id'] == 1, 'avg_transaction_value'].iloc[0], 2) == 15.0

def test_aggregate_empty_df():
    empty_df = pd.DataFrame()
    aggregated = aggregate_customer_data(empty_df)
    assert aggregated.empty
