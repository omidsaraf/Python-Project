# run_pipeline.py

import argparse
import logging
from src.utils import load_config, init_logging
from src.ingestion import ingest_files
from src.bronze_to_silver import clean_bronze_data
from src.silver_to_gold import aggregate_to_gold
from src.visualization import generate_visuals

def main(config_path: str):
    config = load_config(config_path)
    init_logging(config.get("log_level", "INFO"))
    logger = logging.getLogger(__name__)

    logger.info("🚀 Starting Data Pipeline")

    # Ingestion
    raw_df = ingest_files(config["input_path"])
    raw_df.to_csv(f"{config['bronze_path']}/bronze_output.csv", index=False)

    # Bronze → Silver
    silver_df = clean_bronze_data(raw_df)
    silver_df.to_csv(f"{config['silver_path']}/silver_output.csv", index=False)

    # Silver → Gold
    gold_df = aggregate_to_gold(silver_df)
    gold_df.to_csv(f"{config['gold_path']}/gold_output.csv", index=False)

    # Visualization
    generate_visuals(gold_df)

    logger.info("✅ Pipeline execution completed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full data pipeline with config.")
    parser.add_argument("--config", required=True, help="Path to pipeline_config.yaml")
    args = parser.parse_args()
    main(args.config)
