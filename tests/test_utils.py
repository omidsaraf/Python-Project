import os
import pytest
from src.utils import load_config


def test_load_config_reads_yaml(tmp_path):
    """Test basic YAML config loading."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text("key: value")
    config = load_config(str(config_file))
    assert config["key"] == "value"


def test_load_config_missing_file_raises():
    """Test that missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yaml")


def test_load_config_env_override(monkeypatch, tmp_path):
    """Test that environment variable overrides the YAML value."""
    config_file = tmp_path / "test.yaml"
    config_file.write_text("log_level: INFO")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    config = load_config(str(config_file))
    assert config["log_level"] == "DEBUG"
