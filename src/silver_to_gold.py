# src/silver_to_gold.py

import pandas as pd
import logging

logger = logging.getLogger(__name__)

def aggregate_silver_to_gold(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    # Example KPI aggregation
    grouped = df.groupby('category').agg(
        total_amount=pd.NamedAgg(column='amount', aggfunc='sum'),
        avg_amount=pd.NamedAgg(column='amount', aggfunc='mean'),
        record_count=pd.NamedAgg(column='amount', aggfunc='count')
    ).reset_index()

    logger.info(f"Aggregated {len(df)} rows to {len(grouped)} KPI groups.")

    grouped.to_parquet(output_path, index=False)
    logger.info(f"Saved Gold data to {output_path}")
    return grouped
