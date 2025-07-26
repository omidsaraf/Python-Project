import pandas as pd
import logging

logger = logging.getLogger("nsw_data_pipeline.bronze_to_silver")

def clean_and_standardize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes raw data:
    - Removes duplicates
    - Standardizes column names (lowercase, snake_case)
    - Fills or drops nulls (customize as needed)
    """
    if df.empty:
        logger.warning("Input DataFrame is empty. Skipping cleaning.")
        return df

    logger.info("Starting data cleaning and standardization...")

    # Lowercase column names and convert spaces to underscores
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]

    # Drop duplicates
    before_count = len(df)
    df = df.drop_duplicates()
    after_count = len(df)
    logger.info(f"Removed {before_count - after_count} duplicate records.")

    # Example: Fill missing values for a specific column (customize as needed)
    # df['email'] = df['email'].fillna('unknown@example.com')

    # Drop records with nulls in critical columns (example)
    critical_columns = ['customer_id']
    df = df.dropna(subset=critical_columns)
    logger.info(f"Data after dropping nulls in critical columns: {len(df)} records.")

    return df
