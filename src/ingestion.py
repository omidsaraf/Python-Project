# src/ingestion.py

import logging
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype

logger = logging.getLogger(__name__)


def ingest_files(input_dir: Union[str, Path], supported_formats: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Ingest all files of supported types (CSV, JSON) from the input directory.
    Reads each file, validates basic schema consistency, and concatenates into a single DataFrame.

    Args:
        input_dir (str | Path): Directory containing source files.
        supported_formats (List[str], optional): List of file extensions to read ['csv', 'json'] by default.

    Returns:
        pd.DataFrame: Combined data from all successfully ingested files.
    """
    if supported_formats is None:
        supported_formats = ['csv', 'json']

    input_path = Path(input_dir)
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Input directory '{input_dir}' does not exist or is not a directory.")
        return pd.DataFrame()

    all_dfs = []

    for ext in supported_formats:
        files = list(input_path.glob(f"*.{ext}"))
        logger.info(f"Found {len(files)} .{ext} files to ingest.")

        for file in files:
            try:
                if ext == 'csv':
                    df = pd.read_csv(file)
                else:  # json
                    df = pd.read_json(file, lines=True)

                if df.empty:
                    logger.warning(f"File {file.name} is empty, skipping.")
                    continue

                # Basic schema validation - example: check for consistent columns and types (can be expanded)
                if not _validate_schema(df):
                    logger.warning(f"File {file.name} failed schema validation, skipping.")
                    continue

                logger.info(f"Successfully ingested {file.name} with {len(df)} records.")
                all_dfs.append(df)

            except Exception as e:
                logger.error(f"Error ingesting file {file.name}: {e}")

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        logger.info(f"Total records ingested: {len(combined_df)}")
        return combined_df

    logger.warning("No valid data ingested from files.")
    return pd.DataFrame()


def _validate_schema(df: pd.DataFrame) -> bool:
    """
    Basic placeholder for schema validation logic.
    Checks for required columns and types as an example.

    Returns:
        bool: True if schema checks pass, False otherwise.
    """
    required_columns = {'id', 'name'}  # Example required columns, customize for your data
    df_columns = set(df.columns)

    if not required_columns.issubset(df_columns):
        missing = required_columns - df_columns
        logger.warning(f"Missing required columns: {missing}")
        return False

    # Example: check if 'id' column is numeric or string
    if not (is_numeric_dtype(df['id']) or is_string_dtype(df['id'])):
        logger.warning("Column 'id' must be numeric or string type.")
        return False

    return True
