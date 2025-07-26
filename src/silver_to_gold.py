import pandas as pd
import logging

logger = logging.getLogger("nsw_data_pipeline.silver_to_gold")

def aggregate_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates and enriches silver layer data to produce KPIs and summary info for gold layer.
    Example aggregations:
    - Count of transactions per customer
    - Average order value, etc.
    """
    if df.empty:
        logger.warning("Input DataFrame is empty. Skipping aggregation.")
        return df

    logger.info("Starting data aggregation for Gold layer...")

    # Example aggregation by customer_id
    grouped = df.groupby('customer_id').agg(
        total_transactions=pd.NamedAgg(column='transaction_id', aggfunc='count'),
        avg_transaction_value=pd.NamedAgg(column='transaction_value', aggfunc='mean')
    ).reset_index()

    logger.info(f"Aggregated to {len(grouped)} customer records.")

    return grouped
