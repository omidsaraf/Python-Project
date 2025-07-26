import pytest
import pandas as pd
from src.bronze_to_silver import clean_and_standardize

def test_clean_and_standardize_removes_duplicates():
    data = {
        'Customer ID': [1, 1, 2],
        'Email': ['a@example.com', 'a@example.com', 'b@example.com']
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_and_standardize(df)
    assert len(cleaned_df) == 2
    assert 'customer_id' in cleaned_df.columns

def test_clean_and_standardize_drops_nulls():
    data = {
        'Customer ID': [1, None, 2],
        'Email': ['a@example.com', 'b@example.com', None]
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_and_standardize(df)
    assert cleaned_df['customer_id'].isnull().sum() == 0
    assert len(cleaned_df) == 2

def test_clean_and_standardize_empty_df():
    empty_df = pd.DataFrame()
    cleaned_df = clean_and_standardize(empty_df)
    assert cleaned_df.empty
