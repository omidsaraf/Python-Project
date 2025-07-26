import pytest
import pandas as pd
from src.ingest import load_data

def test_load_json(tmp_path):
    data = [{'id': 1, 'value': 'a'}, {'id': 2, 'value': 'b'}]
    file = tmp_path / "test.json"
    pd.DataFrame(data).to_json(file, orient='records')

    df = load_data(str(file))
    assert not df.empty
    assert list(df.columns) == ['id', 'value']
    assert df.shape[0] == 2

def test_load_csv(tmp_path):
    data = {'id': [1,2], 'value': ['a','b']}
    file = tmp_path / "test.csv"
    pd.DataFrame(data).to_csv(file, index=False)

    df = load_data(str(file))
    assert not df.empty
    assert list(df.columns) == ['id', 'value']
    assert df.shape[0] == 2
