# tests/test_utils.py

import pytest
from src.utils import load_config

def test_load_config(tmp_path):
    config_file = tmp_path / "test.yaml"
    config_file.write_text("key: value")
    config = load_config(str(config_file))
    assert config["key"] == "value"

def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yaml")
