import pytest
import pandas as pd
from pathlib import Path
from src.ingestion import ingest_files

# Minimal schema to pass validation for tests
minimal_schema = {
    "columns": ["id", "name"]
}

def test_ingest_empty_directory(tmp_path):
    output_dir = tmp_path / "bronze"
    df = ingest_files(str(tmp_path), str(output_dir), minimal_schema)
    assert df.empty

def test_ingest_csv(tmp_path):
    output_dir = tmp_path / "bronze"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")
    df = ingest_files(str(tmp_path), str(output_dir), minimal_schema)
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]

def test_ingest_json(tmp_path):
    output_dir = tmp_path / "bronze"
    json_file = tmp_path / "test.json"
    json_file.write_text('{"id":1,"name":"Alice"}\n{"id":2,"name":"Bob"}\n')
    df = ingest_files(str(tmp_path), str(output_dir), minimal_schema)
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]

def test_ingest_mixed_files(tmp_path):
    output_dir = tmp_path / "bronze"
    (tmp_path / "test.csv").write_text("id,name\n1,Alice")
    (tmp_path / "test.json").write_text('{"id":2,"name":"Bob"}\n')
    df = ingest_files(str(tmp_path), str(output_dir), minimal_schema)
    assert not df.empty
    assert len(df) == 2

def test_ingest_corrupt_file(tmp_path, caplog):
    output_dir = tmp_path / "bronze"
    corrupt_file = tmp_path / "corrupt.csv"
    corrupt_file.write_text("id,name\n1,Alice\n2")  # Malformed row
    with caplog.at_level("WARNING"):
        df = ingest_files(str(tmp_path), str(output_dir), minimal_schema)
        assert "Skipping" in caplog.text or "Error" in caplog.text
    assert df.empty
