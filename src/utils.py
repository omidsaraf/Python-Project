

import os
import yaml
import logging
from typing import Dict
import logging.config
import yaml
import os
from typing import Any, Dict

def load_config(config_path: str) -> Dict:
    """
    Load YAML configuration file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
def setup_logging(default_path: str = 'configs/logging.yaml', default_level: int = logging.INFO) -> None:
    """Setup logging configuration from YAML file or fallback to basic config."""
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')

def load_config(path: str) -> Dict[str, Any]:
    """Load YAML config with support for environment variable overrides."""
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    # Example override pattern (extend as needed)
    for key, value in config.items():
        env_value = os.getenv(key.upper())
        if env_value is not None:
            config[key] = env_value
    return config

def init_logging(log_level: str = "INFO") -> None:
def validate_schema(df, schema: Dict[str, Any]) -> bool:
    """
    Initialize global logging configuration.
    Basic schema validation:
    - Check required columns exist
    - Check column types (optional)
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    required_columns = schema.get("columns", [])
    for col in required_columns:
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return False
    # Additional type checks can be added here
    return True
