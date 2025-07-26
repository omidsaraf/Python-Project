# src/bronze_to_silver.py

import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_bronze_to_silver(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    initial_count = len(df)
    # Example: drop duplicates and rows with nulls in critical columns
    df_clean = df.drop_duplicates()
    df_clean = df_clean.dropna(subset=['id', 'timestamp'])  # example critical columns

    final_count = len(df_clean)
    logger.info(f"Cleaned Bronze data: {initial_count - final_count} rows removed (duplicates/nulls).")

    df_clean.to_parquet(output_path, index=False)
    logger.info(f"Saved Silver data to {output_path}")
    return df_clean
