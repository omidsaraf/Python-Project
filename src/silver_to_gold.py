# src/silver_to_gold.py

from typing import Optional
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def aggregate_and_enrich(silver_df: pd.DataFrame, threshold: float = 100.0) -> pd.DataFrame:
    """
    Aggregates and enriches silver layer data to produce KPIs and summary info for gold layer.

    Expects silver_df with at least the following columns:
    - 'id' (string or int): Unique customer identifier
    - 'date' (datetime or string): Transaction or event date
    - 'value' (numeric): Numeric value for aggregation

    Aggregations performed:
    - total_count: count of records per 'id'
    - sum_value: sum of 'value' per 'id'
    - avg_value: average of 'value' per 'id'
    - last_date: most recent 'date' per 'id'
    - high_value: boolean KPI flag where sum_value > threshold

    Adds audit column 'kpi_generated_at' with current UTC timestamp.

    Parameters:
        silver_df (pd.DataFrame): Input cleaned silver layer data.
        threshold (float): Threshold to flag high_value KPI.

    Returns:
        pd.DataFrame: Aggregated Gold layer DataFrame with KPIs.
    """
    if silver_df.empty:
        logger.warning("Input silver_df is empty. Returning empty DataFrame.")
        return pd.DataFrame()

    logger.info("Starting aggregation and enrichment for Gold layer.")

    # Ensure 'date' column is datetime type
    if 'date' in silver_df.columns:
        silver_df['date'] = pd.to_datetime(silver_df['date'], errors='coerce')
    else:
        logger.warning("'date' column not found in silver_df. Results may be incomplete.")

    # Ensure 'value' column exists and is numeric
    if 'value' not in silver_df.columns:
        logger.error("'value' column not found in silver_df. Cannot perform aggregation.")
        return pd.DataFrame()
    silver_df['value'] = pd.to_numeric(silver_df['value'], errors='coerce').fillna(0)

    # Ensure 'id' column exists
    if 'id' not in silver_df.columns:
        logger.error("'id' column not found in silver_df. Cannot perform aggregation.")
        return pd.DataFrame()

    # Perform aggregation
    grouped = silver_df.groupby('id').agg(
        total_count=pd.NamedAgg(column='id', aggfunc='count'),
        sum_value=pd.NamedAgg(column='value', aggfunc='sum'),
        avg_value=pd.NamedAgg(column='value', aggfunc='mean'),
        last_date=pd.NamedAgg(column='date', aggfunc='max')
    ).reset_index()

    # KPI flag
    grouped['high_value'] = grouped['sum_value'] > threshold

    # Audit timestamp
    grouped['kpi_generated_at'] = datetime.utcnow()

    logger.info(f"Aggregation complete: {len(grouped)} records aggregated for Gold layer.")
    return grouped
