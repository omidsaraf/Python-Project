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

    # Override with environment variables (flat keys only)
    for key in config:
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
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        log_dir = "./logs"
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            level=default_level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(log_dir, "pipeline.log")),
                logging.StreamHandler()
            ]
        )


def init_logging(log_level: str = "INFO") -> None:
    """
    Initialize basic logging with a specified log level.

    Args:
        log_level (str): Logging level as string (e.g., "INFO", "DEBUG").
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()]
    )

    # Silence noisy libraries
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def validate_schema(df: pd.DataFrame, schema: Dict[str, Any]) -> bool:
    """
    Validates a DataFrame against a schema dict with column types and nullability.

    Args:
        df (pd.DataFrame): Input DataFrame.
        schema (Dict[str, Any]): Schema config from YAML (expects 'columns').

    Returns:
        bool: True if schema is valid, False otherwise.
    """
    columns = schema.get("columns", {})
    for col_name, props in columns.items():
        if col_name not in df.columns:
            logging.error(f"Missing required column: {col_name}")
            return False

        if not props.get("nullable", True) and df[col_name].isnull().any():
            logging.error(f"Non-nullable column '{col_name}' contains null values.")
            return False

        expected_type = props.get("type")
        if expected_type:
            try:
                if expected_type == "int":
                    df[col_name] = pd.to_numeric(df[col_name], errors="coerce").astype("Int64")
                elif expected_type == "float":
                    df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
                elif expected_type == "date":
                    df[col_name] = pd.to_datetime(df[col_name], errors="coerce")
                elif expected_type == "string":
                    df[col_name] = df[col_name].astype(str)
            except Exception as e:
                logging.error(f"Type coercion failed for column '{col_name}': {e}")
                return False

    return True
