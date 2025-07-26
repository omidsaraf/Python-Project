# src/bronze_to_silver.py

import logging
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)

def clean_and_standardize(bronze_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes the raw Bronze layer data to create Silver layer dataset.
    
    Steps include:
    - Drop duplicates
    - Handle missing values (simple fill or drop)
    - Standardize column names and types
    - Filter out invalid rows
    - Add/update audit columns if needed

    Args:
        bronze_df (pd.DataFrame): Raw ingested data (Bronze layer).

    Returns:
        pd.DataFrame: Cleaned and standardized Silver layer data.
    """
    if bronze_df.empty:
        logger.warning("Received empty Bronze DataFrame for cleaning.")
        return bronze_df

    # Drop exact duplicates
    before_count = len(bronze_df)
    df = bronze_df.drop_duplicates()
    after_count = len(df)
    logger.info(f"Dropped {before_count - after_count} duplicate records.")

    # Handle missing values - example strategy:
    # Drop rows where 'id' or 'name' is missing (critical columns)
    df = df.dropna(subset=['id', 'name'])
    logger.info(f"Removed rows with missing 'id' or 'name'. Remaining records: {len(df)}")

    # Standardize column names (lowercase, underscores)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Convert id column to string type (for consistency)
    df['id'] = df['id'].astype(str)

    # Example of standardizing date columns if present
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        null_dates = df['date'].isnull().sum()
        if null_dates > 0:
            logger.warning(f"Found {null_dates} rows with invalid dates.")

    # Add audit column (e.g., cleaned_timestamp)
    df['cleaned_timestamp'] = pd.Timestamp.now()

    logger.info(f"Silver layer data prepared with {len(df)} records.")

    return df
