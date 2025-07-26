import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

def clean_and_standardize(bronze_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes the raw Bronze layer data to create Silver layer dataset.
    
    Steps:
    - Drop duplicates
    - Handle missing values in critical columns ('id', 'name')
    - Standardize column names (lowercase, underscores)
    - Convert data types (e.g., 'id' to string, 'date' to datetime)
    - Add audit columns (e.g., cleaned_timestamp)

    Args:
        bronze_df (pd.DataFrame): Raw ingested Bronze layer data.

    Returns:
        pd.DataFrame: Cleaned and standardized Silver layer data.
    """
    if bronze_df.empty:
        logger.warning("Received empty Bronze DataFrame for cleaning.")
        return bronze_df

    before_count = len(bronze_df)
    df = bronze_df.drop_duplicates()
    after_dedup = len(df)
    logger.info(f"Dropped {before_count - after_dedup} duplicate records.")

    # Drop rows missing critical columns
    df = df.dropna(subset=['id', 'name'])
    after_dropna = len(df)
    logger.info(f"Removed {after_dedup - after_dropna} rows with missing 'id' or 'name'.")

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Convert 'id' to string
    df['id'] = df['id'].astype(str)

    # Convert 'date' to datetime if exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        null_dates = df['date'].isnull().sum()
        if null_dates > 0:
            logger.warning(f"Found {null_dates} rows with invalid 'date' values.")

    # Add audit column
    df['cleaned_timestamp'] = pd.Timestamp.utcnow()

    return df

def clean_bronze_to_silver(bronze_df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    Cleans the Bronze layer DataFrame and saves the Silver layer Parquet file.

    Args:
        bronze_df (pd.DataFrame): Raw Bronze layer data.
        output_path (str): Path to save Silver layer parquet file.

    Returns:
        pd.DataFrame: Cleaned Silver layer DataFrame.
    """
    initial_count = len(bronze_df)
    silver_df = clean_and_standardize(bronze_df)
    final_count = len(silver_df)

    silver_path = Path(output_path)
    silver_path.parent.mkdir(parents=True, exist_ok=True)
    silver_df.to_parquet(silver_path, index=False)

    logger.info(f"Cleaned Bronze data: removed {initial_count - final_count} rows (duplicates/nulls).")
    logger.info(f"Saved Silver data to {silver_path} with {final_count} records.")

    return silver_df
