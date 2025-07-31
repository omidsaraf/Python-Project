# src/__init__.py

from .ingestion import ingest_files, validate_schema
from .bronze_to_silver import clean_bronze_to_silver
from .silver_to_gold import aggregate_and_enrich
from .visualization import generate_visualizations

__all__ = [
    "ingest_files",
    "validate_schema",
    "clean_bronze_to_silver",
    "aggregate_and_enrich",
    "generate_visualizations",
]


## how to use: from src import load_data, transform_bronze_to_silver
