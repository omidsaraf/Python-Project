import argparse
import logging
import sys
from pathlib import Path
import yaml

from src.utils import setup_logging, load_config
from src.ingestion import ingest_files
from src.bronze_to_silver import bronze_to_silver
from src.silver_to_gold import silver_to_gold
from src.visualization import generate_visualizations

def main(config_path: Path):
    # Load config and setup logging
    config = load_config(config_path)
    setup_logging(config.get("log_level", "INFO"))
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Data Pipeline Execution")

    # Ingest raw data → Bronze
    logger.info("Starting ingestion to Bronze layer")
    bronze_df = ingest_files(config["input_path"])
    if bronze_df.empty:
        logger.warning("No data ingested. Exiting pipeline.")
        sys.exit(1)
    
    bronze_path = Path(config["bronze_path"])
    bronze_path.mkdir(parents=True, exist_ok=True)
    bronze_file = bronze_path / "bronze_data.parquet"
    bronze_df.to_parquet(bronze_file, index=False)
    logger.info(f"Bronze data saved to {bronze_file}")

    # Bronze → Silver
    logger.info("Starting Bronze to Silver transformation")
    silver_df = bronze_to_silver(bronze_df)
    silver_path = Path(config["silver_path"])
    silver_path.mkdir(parents=True, exist_ok=True)
    silver_file = silver_path / "silver_data.parquet"
    silver_df.to_parquet(silver_file, index=False)
    logger.info(f"Silver data saved to {silver_file}")

    # Silver → Gold
    logger.info("Starting Silver to Gold transformation")
    gold_df = silver_to_gold(silver_df)
    gold_path = Path(config["gold_path"])
    gold_path.mkdir(parents=True, exist_ok=True)
    gold_file = gold_path / "gold_data.parquet"
    gold_df.to_parquet(gold_file, index=False)
    logger.info(f"Gold data saved to {gold_file}")

    # Generate visualizations
    logger.info("Generating visualizations")
    generate_visualizations(gold_df, output_dir=Path("reports/"))
    logger.info("Visualizations generated and saved")

    logger.info("Data Pipeline Execution completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full data pipeline")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to pipeline YAML configuration file"
    )
    args = parser.parse_args()
    main(args.config)
