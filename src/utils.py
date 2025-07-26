import os
import yaml
import logging
import logging.config
from typing import Any, Dict
import pandas as pd

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load YAML configuration file with environment variable overrides.

    Args:
        config_path (str): Path to YAML config file.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Override config keys with environment variables if set
    for key, value in config.items():
        env_value = os.getenv(key.upper())
        if env_value is not None:
            config[key] = env_value

    return config

def setup_logging(default_path: str = 'configs/logging.yaml', default_level: int = logging.INFO) -> None:
    """
    Setup logging configuration from YAML file or fallback to basic config.

    Args:
        default_path (str): Path to logging config YAML.
        default_level (int): Default logging level if YAML is missing.
    """
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f)  # fixed here: pass file handle directly
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )

def init_logging(log_level: str = "INFO") -> None:
    """
    Initialize global logging with a specified log level.

    Args:
        log_level (str): Logging level as string (e.g., "INFO", "DEBUG").
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()]
    )
    # Reduce noise from noisy libraries
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def validate_schema(df: pd.DataFrame, schema: Dict[str, Any]) -> bool:
    """
    Basic schema validation for a DataFrame.

    Checks required columns are present in df.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        schema (Dict[str, Any]): Schema definition dictionary with 'columns' key.

    Returns:
        bool: True if schema valid, False otherwise.
    """
    required_columns = schema.get("columns", [])
    for col in required_columns:
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return False
    # Additional type checks can be added here if needed
    return True
