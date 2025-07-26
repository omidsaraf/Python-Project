import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger("nsw_data_pipeline.visualization")

def plot_customer_transactions(df: pd.DataFrame, output_path: str) -> None:
    """
    Creates and saves a histogram of total transactions per customer.
    """
    if df.empty:
        logger.warning("Empty DataFrame received for visualization. Skipping plot.")
        return

    logger.info("Creating customer transactions histogram...")

    plt.figure(figsize=(10,6))
    sns.histplot(df['total_transactions'], bins=30, kde=False)
    plt.title('Distribution of Total Transactions per Customer')
    plt.xlabel('Total Transactions')
    plt.ylabel('Number of Customers')
    plt.tight_layout()

    plt.savefig(output_path)
    logger.info(f"Histogram saved to {output_path}")
    plt.close()
