import os
import json
import logging
import pandas as pd
from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)

def ingest_files(input_dir: str, supported_formats: List[str] = ["csv", "json"]) -> pd.DataFrame:
    """
    Reads and concatenates all supported files from input_dir into a single DataFrame.
    Handles errors gracefully and logs progress.
    """
    all_data = []
    path = Path(input_dir)
    if not path.exists():
        logger.error(f"Input directory {input_dir} does not exist.")
        return pd.DataFrame()

    for ext in supported_formats:
        files = list(path.glob(f'*.{ext}'))
        logger.info(f"Found {len(files)} {ext} files.")
        for file in files:
            try:
                if ext == 'csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_json(file, lines=True)
                all_data.append(df)
                logger.info(f"Successfully ingested {file.name}")
            except Exception as e:
                logger.error(f"Failed to ingest {file.name}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        logger.warning("No data ingested.")
        return pd.DataFrame()
