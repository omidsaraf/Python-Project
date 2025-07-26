import logging
import yaml
from typing import Any

def setup_logger(log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("nsw_data_pipeline")
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(ch)
    return logger

def load_config(path: str) -> Any:
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config
