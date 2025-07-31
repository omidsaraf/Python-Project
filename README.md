# 📊 Data Pipeline Project with Python & PySpark

[![CI](https://github.com/omidsaraf/Python-Project/actions/workflows/python-pipeline.yml/badge.svg)](https://github.com/omidsaraf/Python-Project/actions) [![Coverage Status](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/omidsaraf/Python-Project)

#### (Ingest → Bronze → Silver → Gold → Visual)

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/5963f10a-a3cf-4cc8-b92c-5759e52f8a26" />

---

## 🚦 Quick Start

1. **Clone & Install**
   ```bash
   git clone https://github.com/omidsaraf/Python-Project.git
   cd Python-Project
   pip install -r requirements.txt
   ```
2. **Edit Configuration**
   - Copy `configs/pipeline_config.yaml.example` to `configs/pipeline_config.yaml` and update paths as needed.
3. **Prepare Environment**
   - Copy `.env.example` to `.env` and fill in secrets if needed.
4. **Run a Basic Test**
   ```bash
   pytest tests/
   ```
5. **Run the Pipeline**
   ```bash
   python run_pipeline.py --config configs/pipeline_config.yaml
   ```

---

## ✨ Overview

This repository implements a **production-grade, modular Python data pipeline** that processes structured and semi-structured data (CSV/JSON) through a **Medallion architecture (Bronze → Silver → Gold → Visual)**.

Built with **data engineering best practices**, the project ensures:

* ✅ Rigorous data quality enforcement
* ✅ Test-driven development with **Pytest**
* ✅ Continuous Integration and Deployment via **GitHub Actions**
* ✅ Containerization using **Docker**
* ✅ Support for **PySpark-based Google Colab notebooks** for scalable exploration
* ✅ Compliance with **PEP8/PEP257**, modularity, traceability, and governance
* ✅ Enterprise-grade **Security and Data Governance**

---

## ⚖️ Architecture

```plaintext
(data pipeline tree as before)
```

---

## 🧱 Setup

### Prerequisites

```bash
Python 3.9+
Java 8 or 11 (required for PySpark)
Docker (optional, for containerization)
```

- Install Java: [Instructions](https://adoptopenjdk.net/)
- Make sure Docker is installed and running (if using containerization).

### Configuration

- Edit `configs/pipeline_config.yaml` as shown below:
```yaml
input_path: "./data/raw/"
bronze_path: "./data/bronze/"
silver_path: "./data/silver/"
gold_path: "./data/gold/"
log_level: "INFO"
```
- Create a `.env` file locally (excluded from repo) or use environment variables for secrets.

---

## ▶️ Running the Pipeline

```bash
python run_pipeline.py --config configs/pipeline_config.yaml
```

---

## 🧪 Running Tests with Pytest

```bash
pytest tests/ --maxfail=3 --disable-warnings -v --cov=src --cov-report=term-missing
```
* Uses isolated temp directories and mocks to avoid side effects
* Reports code coverage and shows missing lines for continuous improvement
* Runs quickly and fails fast for efficient debugging

---

## 📥 Example Python: Ingestion Module with PySpark

```python
# src/ingestion.py
... (leave this section unchanged) ...
```

---

## 📈 Sample Output Visualizations

| Correlation Heatmap | Monthly KPI Count  | Null Distribution  |
| ------------------- | ------------------ | ------------------ |
| ![](img/corr.png)   | ![](img/count.png) | ![](img/nulls.png) |

---

## 🚀 CI/CD via GitHub Actions

Automatically triggered on every push and pull request, the pipeline includes:

* ✅ Linting using **Flake8**
* ✅ Unit testing using **Pytest** with coverage reports
* ✅ Code formatting checks via **Black**
* ✅ Static typing checks with **Mypy**
* ✅ Security scans using **Bandit** for Python vulnerabilities

Configured in `.github/workflows/python-pipeline.yml`

---

## 📦 Docker Container

Build the Docker image:
```bash
docker build -t datapipeline:latest .
```
Run the pipeline inside the container (mount current directory):
```bash
docker run --rm -v "$PWD":/app datapipeline:latest python run_pipeline.py --config configs/pipeline_config.yaml
```

---

## 📓 PySpark Notebooks

Explore the pipeline step-by-step using the provided **PySpark-based** Jupyter notebooks in `/notebooks/` — fully compatible with Google Colab and scalable Spark clusters.

Each notebook prepends the `src` directory to Python path and initializes Spark:
```python
import sys
sys.path.append('../src')
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("Data Pipeline EDA") \
    .getOrCreate()
```
Notebook workflow:
1. `01_bronze_ingestion.ipynb` — Ingest raw JSON/CSV
2. `02_silver_cleaning.ipynb` — Clean and standardize data
3. `03_gold_aggregation.ipynb` — KPI calculation and enrichment
4. `04_visualization.ipynb` — Generate visual insights

---

## 🛠️ Troubleshooting

- **ModuleNotFoundError**: Ensure you are running from the project root and Python paths are correct.
- **PySpark errors**: Confirm Java is installed and JAVA_HOME is set.
- **Docker issues**: Check Docker is running and permissions are correct.
- **Config errors**: Double-check all paths in `configs/pipeline_config.yaml`.
- **Test failures**: Run `pytest` with `-s` for more verbose output.

---

## 📜 License

MIT License

---

## 👤 Author

Created by a **Senior Data Engineer**, specializing in:

* Production-grade Python ETL pipelines
* Modular, testable, secure data engineering systems
* Public sector and enterprise compliance-ready solutions
* Cloud-agnostic, scalable architectures

---