# src/silver_to_gold.py

from typing import Optional
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger("nsw_data_pipeline.silver_to_gold")
logger = logging.getLogger(__name__)

def aggregate_customer_data(df: pd.DataFrame) -> pd.DataFrame:
def aggregate_and_enrich(silver_df: pd.DataFrame) -> pd.DataFrame:
"""
    Aggregates and enriches silver layer data to produce KPIs and summary info for gold layer.
    Example aggregations:
    - Count of transactions per customer
    - Average order value, etc.
    Aggregate and enrich Silver layer data to produce KPI-ready Gold layer.

    This example assumes silver_df contains cleaned data with at least:
    - 'id' (string or int)
    - 'date' (datetime)
    - 'value' (numeric)

    Aggregations:
    - Total count per id
    - Sum of 'value' per id
    - Average 'value' per id
    - Most recent 'date' per id
    - KPI flag: high_value = True if sum(value) > threshold (e.g., 100)

    Returns:
        pd.DataFrame: Gold dataset with aggregated KPIs.
   """
    if df.empty:
        logger.warning("Input DataFrame is empty. Skipping aggregation.")
        return df

    logger.info("Starting data aggregation for Gold layer...")
    if silver_df.empty:
        logger.warning("Input silver_df is empty. Returning empty DataFrame.")
        return pd.DataFrame()

    # Example aggregation by customer_id
    grouped = df.groupby('customer_id').agg(
        total_transactions=pd.NamedAgg(column='transaction_id', aggfunc='count'),
        avg_transaction_value=pd.NamedAgg(column='transaction_value', aggfunc='mean')
    # Ensure 'date' is datetime
    if 'date' in silver_df.columns:
        silver_df['date'] = pd.to_datetime(silver_df['date'], errors='coerce')
    else:
        logger.warning("'date' column not found in silver_df.")

    # Fill missing values for aggregation columns
    silver_df['value'] = pd.to_numeric(silver_df['value'], errors='coerce').fillna(0)

    grouped = silver_df.groupby('id').agg(
        total_count=pd.NamedAgg(column='id', aggfunc='count'),
        sum_value=pd.NamedAgg(column='value', aggfunc='sum'),
        avg_value=pd.NamedAgg(column='value', aggfunc='mean'),
        last_date=pd.NamedAgg(column='date', aggfunc='max')
).reset_index()

    logger.info(f"Aggregated to {len(grouped)} customer records.")
    # KPI flag: high_value (example threshold 100)
    threshold = 100
    grouped['high_value'] = grouped['sum_value'] > threshold

    # Add audit columns
    grouped['kpi_generated_at'] = datetime.utcnow()

    logger.info(f"Aggregated {len(grouped)} records into Gold layer.")

return grouped
