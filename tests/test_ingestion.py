import pytest
import pandas as pd
from pathlib import Path
from src.ingestion import ingest_files

def test_ingest_empty_directory(tmp_path):
    # Should return empty DataFrame if no files
    df = ingest_files(str(tmp_path))
    assert df.empty

def test_ingest_csv(tmp_path):
    # Create a simple CSV file
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")
    df = ingest_files(str(tmp_path))
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]

def test_ingest_json(tmp_path):
    # Create a simple JSON file (line-delimited)
    json_file = tmp_path / "test.json"
    json_file.write_text('{"id":1,"name":"Alice"}\n{"id":2,"name":"Bob"}\n')
    df = ingest_files(str(tmp_path))
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]

def test_ingest_mixed_files(tmp_path):
    # Create CSV + JSON files in same dir
    (tmp_path / "test.csv").write_text("id,name\n1,Alice")
    (tmp_path / "test.json").write_text('{"id":2,"name":"Bob"}\n')
    df = ingest_files(str(tmp_path))
    assert not df.empty
    assert len(df) == 2

def test_ingest_corrupt_file(tmp_path, caplog):
    # Create a corrupt CSV file and check for warning log
    corrupt_file = tmp_path / "corrupt.csv"
    corrupt_file.write_text("id,name\n1,Alice\n2")  # Malformed row
    with caplog.at_level("WARNING"):
        df = ingest_files(str(tmp_path))
        assert "Skipping" in caplog.text or "Error" in caplog.text
    # Should skip corrupt file and return empty DataFrame
    assert df.empty
