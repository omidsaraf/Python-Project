# tests/test_bronze_to_silver.py

import pytest
import pandas as pd
from src.bronze_to_silver import clean_and_standardize

def test_clean_and_standardize_basic():
    # Input DataFrame with duplicates, missing values, and inconsistent columns
    data = {
        'ID': [1, 1, 2, 3, None],
        'Name': ['Alice', 'Alice', 'Bob', None, 'Charlie'],
        'Date': ['2023-01-01', '2023-01-01', 'invalid_date', '2023-03-01', '2023-04-01'],
        'Extra Column': ['x', 'x', 'y', 'z', 'w']
    }
    bronze_df = pd.DataFrame(data)

    silver_df = clean_and_standardize(bronze_df)

    # Should drop duplicates, rows missing 'id' or 'name'
    # Rows 0 and 1 are duplicates; row 3 missing name; row 4 missing id
    assert len(silver_df) == 2  # Only rows with id=1 and 2 remain

    # Columns should be lowercase and underscored
    assert 'extra_column' in silver_df.columns
    assert 'cleaned_timestamp' in silver_df.columns

    # IDs are strings
    assert silver_df['id'].dtype == object

    # Date column is datetime, with coercion of invalid date to NaT
    assert pd.api.types.is_datetime64_any_dtype(silver_df['date'])
    assert silver_df['date'].isnull().sum() == 1  # invalid_date should be NaT

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
    # Should not raise error and should add cleaned_timestamp
    assert 'cleaned_timestamp' in result.columns
    assert len(result) == 2

