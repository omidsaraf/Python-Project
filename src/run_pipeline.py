import argparse
import logging
from src.utils import setup_logger, load_config
from src.ingestion import ingest_files
from src.bronze_to_silver import clean_and_standardize
from src.silver_to_gold import aggregate_customer_data
from src.visualization import plot_customer_transactions
import os

def main(config_path: str):
    config = load_config(config_path)
    logger = setup_logger(config.get('log_level', 'INFO'))
    logger.info("Starting NSW Data Pipeline...")

    # Ingest data (Bronze)
    raw_df = ingest_files(config['input_path'])

    # Bronze to Silver
    silver_df = clean_and_standardize(raw_df)

    # Save silver data
    os.makedirs(config['silver_path'], exist_ok=True)
    silver_file = os.path.join(config['silver_path'], 'silver_data.csv')
    silver_df.to_csv(silver_file, index=False)
    logger.info(f"Silver data saved at {silver_file}")

    # Silver to Gold
    gold_df = aggregate_customer_data(silver_df)

    # Save gold data
    os.makedirs(config['gold_path'], exist_ok=True)
    gold_file = os.path.join(config['gold_path'], 'gold_data.csv')
    gold_df.to_csv(gold_file, index=False)
    logger.info(f"Gold data saved at {gold_file}")

    # Visualization
    viz_output = os.path.join(config['gold_path'], 'customer_transactions_histogram.png')
    plot_customer_transactions(gold_df, viz_output)

    logger.info("Pipeline execution complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run NSW Data Pipeline")
    parser.add_argument('--config', type=str, required=True, help='Path to config YAML file')
    args = parser.parse_args()
    main(args.config)
