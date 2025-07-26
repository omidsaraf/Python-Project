# src/utils.py

import logging
import logging.config
import yaml
import os
from typing import Any, Dict

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

def validate_schema(df, schema: Dict[str, Any]) -> bool:
    """
    Basic schema validation:
    - Check required columns exist
    - Check column types (optional)
    """
    required_columns = schema.get("columns", [])
    for col in required_columns:
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return False
    # Additional type checks can be added here
    return True
