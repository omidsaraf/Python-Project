from src.utils import load_config

def test_load_config(tmp_path):
    config_file = tmp_path / "test.yaml"
    config_file.write_text("key: value")
    config = load_config(str(config_file))
    assert config["key"] == "value"
