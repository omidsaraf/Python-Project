# src/ingestion.py

from pathlib import Path
import pandas as pd
import shutil
import logging
from typing import List
from src.utils import validate_schema

logger = logging.getLogger(__name__)

def ingest_files(input_dir: str, output_dir: str, schema: dict, supported_formats: List[str] = ['csv', 'json']) -> pd.DataFrame:
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        logger.error(f"Input directory {input_dir} does not exist.")
        return pd.DataFrame()

    all_data = []
    for ext in supported_formats:
        for file_path in input_path.glob(f'*.{ext}'):
            try:
                if ext == 'csv':
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_json(file_path, lines=True)
                
                if not validate_schema(df, schema):
                    logger.warning(f"Schema validation failed for {file_path.name}. Skipping file.")
                    continue

                # Copy original file to bronze folder for lineage
                dest_file = output_path / file_path.name
                shutil.copy2(file_path, dest_file)
                logger.info(f"Ingested and copied {file_path.name} to bronze zone.")

                all_data.append(df)
            except Exception as e:
                logger.error(f"Failed to ingest {file_path.name}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()
