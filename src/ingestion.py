from typing import List
from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger("nsw_data_pipeline.ingestion")

def ingest_files(input_dir: str, supported_formats: List[str] = ['csv', 'json']) -> pd.DataFrame:
    """
    Ingests all files with supported formats from input_dir into a single DataFrame.
    Supports CSV and JSON (line-delimited) formats.
    """
    all_data = []
    path = Path(input_dir)
    if not path.exists():
        logger.error(f"Input directory {input_dir} does not exist.")
        return pd.DataFrame()

    for ext in supported_formats:
        files = list(path.glob(f'*.{ext}'))
        logger.info(f"Found {len(files)} {ext.upper()} files.")
        for file in files:
            try:
                if ext == 'csv':
                    df = pd.read_csv(file)
                elif ext == 'json':
                    df = pd.read_json(file, lines=True)
                else:
                    logger.warning(f"Unsupported file extension: {ext}")
                    continue
                all_data.append(df)
                logger.info(f"Ingested {file.name} successfully.")
            except Exception as e:
                logger.error(f"Failed to ingest {file.name}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        logger.info(f"Total records ingested: {len(combined_df)}")
        return combined_df
    else:
        logger.warning("No data ingested.")
        return pd.DataFrame()
