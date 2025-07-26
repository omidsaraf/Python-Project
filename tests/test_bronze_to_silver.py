# tests/test_bronze_to_silver.py

import pytest
import pandas as pd
from src.bronze_to_silver import clean_and_standardize

def test_clean_and_standardize_basic():
    data = {
        'ID': [1, 1, 2, 3, None],
        'Name': ['Alice', 'Alice', 'Bob', None, 'Charlie'],
        'Date': ['2023-01-01', '2023-01-01', 'invalid_date', '2023-03-01', '2023-04-01'],
        'Extra Column': ['x', 'x', 'y', 'z', 'w']
    }
    bronze_df = pd.DataFrame(data)

    silver_df = clean_and_standardize(bronze_df)

    # Should drop duplicates and rows missing 'id' or 'name'
    assert len(silver_df) == 2  # Only valid rows remain

    # Columns standardized (lowercase, underscores)
    assert 'extra_column' in silver_df.columns
    assert 'cleaned_timestamp' in silver_df.columns

    # IDs converted to string type
    assert silver_df['id'].dtype == object

    # Date column is datetime with coercion for invalid dates
    assert pd.api.types.is_datetime64_any_dtype(silver_df['date'])
    assert silver_df['date'].isnull().sum() == 1  # One invalid date converted to NaT

    # cleaned_timestamp column is datetime64[ns]
    assert pd.api.types.is_datetime64_any_dtype(silver_df['cleaned_timestamp'])

def test_clean_and_standardize_empty_df():
    empty_df = pd.DataFrame()
    result = clean_and_standardize(empty_df)
    assert result.empty

def test_clean_and_standardize_no_date_column():
    data = {
        'ID': [1, 2],
        'Name': ['Alice', 'Bob']
    }
    df = pd.DataFrame(data)
    result = clean_and_standardize(df)
    assert 'cleaned_timestamp' in result.columns
    assert len(result) == 2
    assert pd.api.types.is_datetime64_any_dtype(result['cleaned_timestamp'])
