# tests/test_silver_to_gold.py

import pytest
import pandas as pd
from src.silver_to_gold import aggregate_and_enrich

def test_aggregate_and_enrich_basic():
    # Sample input data
    data = {
        'id': ['A', 'A', 'B', 'B', 'B'],
        'date': ['2025-07-01', '2025-07-02', '2025-07-01', '2025-07-03', '2025-07-02'],
        'value': [10, 20, 30, 40, 50]
    }
    df = pd.DataFrame(data)

    result = aggregate_and_enrich(df)

    assert not result.empty
    assert set(result.columns).issuperset({'id', 'total_count', 'sum_value', 'avg_value', 'last_date', 'high_value', 'kpi_generated_at'})
    # Check aggregations
    row_a = result[result['id'] == 'A'].iloc[0]
    assert row_a['total_count'] == 2
    assert row_a['sum_value'] == 30
    assert abs(row_a['avg_value'] - 15) < 1e-6
    assert pd.to_datetime(row_a['last_date']) == pd.to_datetime('2025-07-02')
    assert row_a['high_value'] is False

    row_b = result[result['id'] == 'B'].iloc[0]
    assert row_b['total_count'] == 3
    assert row_b['sum_value'] == 120
    assert abs(row_b['avg_value'] - 40) < 1e-6
    assert pd.to_datetime(row_b['last_date']) == pd.to_datetime('2025-07-03')
    assert row_b['high_value'] is True

def test_aggregate_and_enrich_empty_df():
    empty_df = pd.DataFrame()
    result = aggregate_and_enrich(empty_df)
    assert result.empty

def test_aggregate_and_enrich_missing_date_value_columns():
    data = {
        'id': ['A', 'B'],
        'value': [10, 20]  # missing 'date'
    }
    df = pd.DataFrame(data)
    result = aggregate_and_enrich(df)
    assert 'last_date' in result.columns
    # last_date should be NaT or null because missing 'date' column
    assert result['last_date'].isnull().all()

def test_aggregate_and_enrich_non_numeric_values():
    data = {
        'id': ['A', 'A'],
        'date': ['2025-07-01', '2025-07-02'],
        'value': ['10', 'invalid']
    }
    df = pd.DataFrame(data)
    result = aggregate_and_enrich(df)
    # The invalid value should be coerced to 0
    row = result[result['id'] == 'A'].iloc[0]
    assert row['sum_value'] == 10
    assert row['high_value'] is False
