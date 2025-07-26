"""
run_pipeline.py - CLI entry point to execute the full Bronze → Silver → Gold pipeline and generate visualizations.

Usage:
    python run_pipeline.py --config configs/pipeline_config.yaml
"""

import argparse
import logging
import sys
from src.utils import setup_logging, load_config
from src.ingestion import ingest_files
from src.bronze_to_silver import bronze_to_silver
from src.silver_to_gold import silver_to_gold
from src.visualization import plot_correlation_heatmap, plot_time_series, plot_null_values, plot_histogram
from pathlib import Path
import pandas as pd

def main(config_path: str):
    # Load configuration
    config = load_config(config_path)

    # Setup logging
    setup_logging(config.get('log_level', 'INFO'))

    logger = logging.getLogger(__name__)
    logger.info("Starting data pipeline...")

    # Step 1: Ingest raw data to Bronze
    logger.info("Step 1: Ingesting raw files to Bronze layer...")
    bronze_df = ingest_files(config['input_path'])
    if bronze_df.empty:
        logger.error("No data ingested. Exiting pipeline.")
        sys.exit(1)

    bronze_dir = Path(config['bronze_path'])
    bronze_dir.mkdir(parents=True, exist_ok=True)
    bronze_output_path = bronze_dir / "bronze_data.parquet"
    bronze_df.to_parquet(bronze_output_path, index=False)
    logger.info(f"Bronze data saved to {bronze_output_path}")

    # Step 2: Bronze to Silver transformation
    logger.info("Step 2: Cleaning and transforming Bronze to Silver layer...")
    silver_df = bronze_to_silver(bronze_df)
    silver_dir = Path(config['silver_path'])
    silver_dir.mkdir(parents=True, exist_ok=True)
    silver_output_path = silver_dir / "silver_data.parquet"
    silver_df.to_parquet(silver_output_path, index=False)
    logger.info(f"Silver data saved to {silver_output_path}")

    # Step 3: Silver to Gold aggregation
    logger.info("Step 3: Aggregating Silver to Gold layer...")
    gold_df = silver_to_gold(silver_df)
    gold_dir = Path(config['gold_path'])
    gold_dir.mkdir(parents=True, exist_ok=True)
    gold_output_path = gold_dir / "gold_data.parquet"
    gold_df.to_parquet(gold_output_path, index=False)
    logger.info(f"Gold data saved to {gold_output_path}")

    # Step 4: Visualizations
    logger.info("Step 4: Generating visualizations...")
    vis_dir = Path("output/visualizations")
    vis_dir.mkdir(parents=True, exist_ok=True)

    plot_correlation_heatmap(gold_df, save_path=str(vis_dir / "correlation_heatmap.png"))
    plot_time_series(gold_df, date_col='date', value_col='value', save_path=str(vis_dir / "time_series.png"))  # Update date_col/value_col as per your gold_df schema
    plot_null_values(gold_df, save_path=str(vis_dir / "null_values.png"))

    # Example histogram on a numeric column - update column name as needed
    numeric_cols = gold_df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        plot_histogram(gold_df, col=numeric_cols[0], save_path=str(vis_dir / "histogram.png"))
    else:
        logger.warning("No numeric columns found for histogram visualization.")

    logger.info("Pipeline execution completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full data pipeline")
    parser.add_argument('--config', required=True, help="Path to pipeline config YAML file")
    args = parser.parse_args()

    main(args.config)
