import pytest
from src.ingestion import ingest_files
import pandas as pd
from pathlib import Path

def test_ingest_empty_dir(tmp_path):
    df = ingest_files(str(tmp_path))
    assert df.empty

def test_ingest_csv(tmp_path):
    test_csv = tmp_path / "test.csv"
    test_csv.write_text("id,name\n1,Alice\n2,Bob")
    df = ingest_files(str(tmp_path))
    assert len(df) == 2
    assert list(df.columns) == ['id', 'name']

def test_ingest_json(tmp_path):
    test_json = tmp_path / "test.json"
    test_json.write_text('{"id":1,"name":"Alice"}\n{"id":2,"name":"Bob"}')
    df = ingest_files(str(tmp_path))
    assert len(df) == 2
    assert list(df.columns) == ['id', 'name']
