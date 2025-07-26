ef clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the ingested raw data."""
    logger.info("Cleaning data...")
    df = df.drop_duplicates()
    df = df.dropna(how='all')
    return df

# src/silver_to_gold.py

def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich the cleaned data to prepare final KPIs."""
    logger.info("Aggregating data...")
    if 'value' in df.columns:
        return df.groupby('category').agg({'value': 'sum'}).reset_index()
    return df

# src/visualization.py

import seaborn as sns
import matplotlib.pyplot as plt

def plot_kpis(df: pd.DataFrame, output_path: str):
    """Generate seaborn bar plot of KPI data."""
    logger.info("Generating visualization...")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='category', y='value')
    plt.xticks(rotation=45)
    plt.title('KPI Summary by Category')
    plt.tight_layout()
    plot_file = os.path.join(output_path, "kpi_summary.png")
    plt.savefig(plot_file)
    logger.info(f"Visualization saved to {plot_file}")
