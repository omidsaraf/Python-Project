import pandas as pd
from src.bronze_to_silver import clean_data

def test_clean_data_removes_nulls():
    df = pd.DataFrame({"id": [1, None], "value": ["A", "B"]})
    cleaned = clean_data(df)
    assert cleaned.shape[0] == 1
    assert cleaned.iloc[0]["id"] == 1
