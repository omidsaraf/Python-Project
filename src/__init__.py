# src/__init__.py

from .ingestion import ingest_files, validate_data
from .bronze_to_silver import clean_bronze_to_silver
from .silver_to_gold import aggregate_and_enrich
from .visualization import generate_visualizations

__all__ = [
    "load_data",
    "validate_data",
    "transform_bronze_to_silver",
    "transform_silver_to_gold",
    "generate_visualizations",
]


## how to use: from src import load_data, transform_bronze_to_silver
