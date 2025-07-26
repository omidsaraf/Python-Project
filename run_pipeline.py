from src.utils import load_config, configure_logging
from src.ingestion import ingest_files
from src.bronze_to_silver import clean_data
from src.silver_to_gold import aggregate_data
from src.visualization import plot_kpis

import argparse

def main(config_path: str):
    config = load_config(config_path)
    configure_logging(config.get("log_level", "INFO"))

    df_bronze = ingest_files(config['input_path'])
    df_bronze.to_csv(config['bronze_path'] + "/bronze_output.csv", index=False)

    df_silver = clean_data(df_bronze)
    df_silver.to_csv(config['silver_path'] + "/silver_output.csv", index=False)

    df_gold = aggregate_data(df_silver)
    df_gold.to_csv(config['gold_path'] + "/gold_output.csv", index=False)

    plot_kpis(df_gold, config['gold_path'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Path to config YAML file')
    args = parser.parse_args()
    main(args.config)
