import pytest
import pandas as pd
from src.ingestion import ingest_files
from pathlib import Path

def test_ingest_empty_directory(tmp_path):
    df = ingest_files(str(tmp_path))
    assert df.empty

def test_ingest_csv_file(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text("id,name\n1,Alice\n2,Bob")
    df = ingest_files(str(tmp_path))
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]

def test_ingest_json_file(tmp_path):
    file = tmp_path / "sample.json"
    file.write_text('{"id": 1, "name": "Alice"}\n{"id": 2, "name": "Bob"}')
    df = ingest_files(str(tmp_path))
    assert len(df) == 2
    assert "id" in df.columns
    assert "name" in df.columns
