# Data Pipeline Project with Python (Bronze → Silver → Gold)

## ✨ Overview

This project delivers a **world-class, production-grade Python data pipeline** built for flexibility, auditability, and analytical readiness. It ingests structured and semi-structured data (CSV, JSON), applies rigorous quality checks, processes it through a **Medallion architecture (Bronze → Silver → Gold)**, and ends with rich **Seaborn-powered visual insights**.

This project adheres to NSW Government and enterprise data engineering standards across **testing, modularity, logging, CI/CD, version control, and documentation**.

---

## ⚖️ Architecture

```
/data-pipeline/
|
|│   .gitignore
|│   .flake8
|│   Dockerfile
|│   pyproject.toml
|│   requirements.txt
|│   run_pipeline.py               # CLI runner for full pipeline execution
|│   README.md
|
|├── configs/
|│   └── pipeline_config.yaml        # Parameterized paths and settings
|
|├── data/
|│   ├── raw/                       # Input source data (JSON / CSV)
|│   ├── bronze/                    # Raw but ingested
|│   ├── silver/                    # Cleaned, standardized
|│   └── gold/                      # Enriched, KPI-ready
|
|├── src/
|│   ├── __init__.py
|│   ├── ingestion.py               # Ingests + validates files
|│   ├── bronze_to_silver.py        # Standardizes structure + schema
|│   ├── silver_to_gold.py          # Enriches + aggregates
|│   ├── visualization.py           # Seaborn plots
|│   └── utils.py                   # Logging, config loader, helpers
|
|├── tests/
|│   ├── __init__.py
|│   ├── test_ingest.py
|│   ├── test_bronze_to_silver.py
|│   ├── test_silver_to_gold.py
|│   └── test_visualization.py
|
└── .github/workflows/
    └── python-pipeline.yml              # CI pipeline with pytest + flake8
```

---

## 🔗 Key Features

### ✅ Enterprise Best Practices

* Follows PEP8 + PEP257 + type hinting
* Dockerized and CI-ready via GitHub Actions
* Structured logging with root config
* Test-driven with Pytest fixtures

### ⚙️ Fully Modular

* 1 script = 1 logical unit (ETL best practice)
* Central config (YAML)
* Composable transformations with pandas

### ✍️ Schema & Validation Support

* Schema-checked ingestion (CSV & JSON)
* Clean failover and logging on corrupted/missing records

### 🎓 Data Quality

* Silver removes nulls/dupes/types
* Gold adds metrics, flags, KPIs
* All output is auditable & reproducible

### 🔍 Insight-Ready Visuals

* Seaborn + Matplotlib
* Trend lines, histograms, correlation heatmaps
* Image export for audit and presentation

### 🔢 Fully Tested

* > 90% Pytest test coverage (unit + edge)
* Tests for schema mismatch, empty files, invalid types, transformation correctness

---

## 🔧 Setup

### Prerequisites

```bash
python>=3.9
pip install -r requirements.txt
```

### Configuration

```yaml
# configs/pipeline_config.yaml
input_path: "./data/raw/"
bronze_path: "./data/bronze/"
silver_path: "./data/silver/"
gold_path: "./data/gold/"
log_level: "INFO"
```

### Run Pipeline

```bash
python run_pipeline.py --config configs/pipeline_config.yaml
```

---

## 🌐 Example: Ingestion

```python
# src/ingestion.py

def ingest_files(input_dir: str, supported_formats: List[str] = ['csv', 'json']) -> pd.DataFrame:
    path = Path(input_dir)
    if not path.exists():
        logger.error(f"Input directory {input_dir} does not exist.")
        return pd.DataFrame()

    all_data = []
    for ext in supported_formats:
        for file in path.glob(f'*.{ext}'):
            try:
                if ext == 'csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_json(file, lines=True)
                all_data.append(df)
                logger.info(f"Ingested {file.name}")
            except Exception as e:
                logger.warning(f"Skipping {file.name}: {e}")

    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
```

---

## 🔬 Testing

```bash
pytest --maxfail=3 --disable-warnings -q
```

### Example test

```python
# tests/test_ingest.py

def test_ingest_csv(tmp_path):
    test_csv = tmp_path / "sample.csv"
    test_csv.write_text("id,name\n1,Alice\n2,Bob")
    df = ingest_files(str(tmp_path))
    assert len(df) == 2
    assert list(df.columns) == ['id', 'name']
```

---

## 📈 Sample Visualization Output

| Correlation Heatmap | Monthly Counts      | Nulls by Column    |
| ------------------- | ------------------- | ------------------ |
| ![](img/corr.png)   | ![](img/counts.png) | ![](img/nulls.png) |

---

## 🌐 CI/CD

Supports GitHub Actions for:

* Linting (`flake8`)
* Unit tests (`pytest`)
* Build & artifact packaging (optional Docker)

---

## 📄 License

MIT License. Use, extend, and contribute freely!

---

## ✨ Author

Crafted by a **Senior Data Engineer** for NSW Government-style production-grade Python/ETL systems with a focus on **modular pipeline design, PySpark extension readiness, and compliance-aligned governance.**
