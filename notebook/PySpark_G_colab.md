
---

### 01\_bronze\_ingestion.ipynb

```python
# 01_bronze_ingestion.ipynb

# ## Bronze Layer Ingestion
# This notebook ingests raw source data files (CSV/JSON) into the Bronze layer.
# Typically raw, uncleaned data, just loaded and saved to parquet for downstream use.

# Import required libraries
from pyspark.sql import SparkSession
from pathlib import Path

# Create Spark session
spark = SparkSession.builder.appName("BronzeIngestion").getOrCreate()

# Define paths
raw_data_path = "/path/to/raw_data"        # Change to your source raw data directory
bronze_output_path = "/path/to/bronze"     # Change to your bronze layer storage location

# Load raw data (example: CSV)
df_bronze = spark.read.option("header", True).csv(raw_data_path)

# Show schema and sample data
df_bronze.printSchema()
df_bronze.show(5)

# Write to Bronze layer as parquet
df_bronze.write.mode("overwrite").parquet(bronze_output_path)

print(f"Bronze data saved to {bronze_output_path}")
```

---

### 02\_silver\_cleaning.ipynb

```python
# 02_silver_cleaning.ipynb

# ## Silver Layer Cleaning and Standardization
# This notebook cleans and standardizes the raw Bronze data for further processing.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, lit
from pathlib import Path

spark = SparkSession.builder.appName("SilverCleaning").getOrCreate()

bronze_path = "/path/to/bronze"
silver_output_path = "/path/to/silver"

# Load Bronze parquet data
df_bronze = spark.read.parquet(bronze_path)

# Show initial count and schema
print(f"Bronze records count: {df_bronze.count()}")
df_bronze.printSchema()

# Drop duplicates
df_clean = df_bronze.dropDuplicates()

# Filter out rows with null critical columns (e.g., id, name)
df_clean = df_clean.filter(col("id").isNotNull() & col("name").isNotNull())

# Cast date columns if applicable
if "date" in df_clean.columns:
    df_clean = df_clean.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))

# Add audit column
from pyspark.sql.functions import current_timestamp
df_clean = df_clean.withColumn("cleaned_timestamp", current_timestamp())

# Show cleaned data count
print(f"Silver records count: {df_clean.count()}")

# Save cleaned Silver data
df_clean.write.mode("overwrite").parquet(silver_output_path)

print(f"Silver data saved to {silver_output_path}")
```

---

### 03\_gold\_aggregation.ipynb

```python
# 03_gold_aggregation.ipynb

# ## Gold Layer Aggregation and KPI Calculation
# Aggregates Silver data to compute KPIs and summary metrics.

from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, sum as _sum, max as _max, col, when, current_timestamp
from pathlib import Path

spark = SparkSession.builder.appName("GoldAggregation").getOrCreate()

silver_path = "/path/to/silver"
gold_output_path = "/path/to/gold"

# Load Silver data
df_silver = spark.read.parquet(silver_path)

# Basic aggregations per 'id' (or 'customer_id')
df_agg = df_silver.groupBy("id").agg(
    count("*").alias("total_count"),
    _sum("value").alias("sum_value"),
    avg("value").alias("avg_value"),
    _max("date").alias("last_date")
)

# Define KPI threshold and flag
threshold = 100
df_agg = df_agg.withColumn("high_value", when(col("sum_value") > threshold, True).otherwise(False))

# Add KPI generated timestamp
df_agg = df_agg.withColumn("kpi_generated_at", current_timestamp())

# Show result
df_agg.show()

# Save Gold data
df_agg.write.mode("overwrite").parquet(gold_output_path)

print(f"Gold data saved to {gold_output_path}")
```

---

### 04\_visualization.ipynb

```python
# 04_visualization.ipynb

# ## Visualization of Gold Layer KPIs and Data Insights
# Uses Pandas/Matplotlib/Seaborn to generate plots and summaries from Gold data.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

gold_path = "/path/to/gold"
output_dir = Path("visualizations")
output_dir.mkdir(exist_ok=True)

# Load Gold parquet into Pandas (for smaller datasets)
df_gold = pd.read_parquet(gold_path)

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df_gold.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig(output_dir / "correlation_heatmap.png")
plt.show()

# Time series of avg_value over last_date
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_gold.sort_values("last_date"), x="last_date", y="avg_value", marker="o")
plt.title("Average Value Over Time")
plt.xticks(rotation=45)
plt.savefig(output_dir / "time_series_avg_value.png")
plt.show()

# Null values plot
null_counts = df_gold.isnull().sum()
null_counts = null_counts[null_counts > 0]
if not null_counts.empty:
    plt.figure(figsize=(10, 6))
    sns.barplot(x=null_counts.index, y=null_counts.values)
    plt.title("Null Values per Column")
    plt.xticks(rotation=45)
    plt.savefig(output_dir / "null_values.png")
    plt.show()

# Histogram of sum_value
plt.figure(figsize=(8, 5))
sns.histplot(df_gold["sum_value"].dropna(), bins=30, kde=True, color="skyblue")
plt.title("Distribution of Sum Value")
plt.savefig(output_dir / "histogram_sum_value.png")
plt.show()
```

---

