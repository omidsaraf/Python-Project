#  Data Pipeline Project

## Overview

This project implements a robust, modular Python-based data ingestion and transformation pipeline, designed to process JSON and CSV files into a 3-layer medallion architecture (Bronze → Silver → Gold) and present final insights with Seaborn visualizations.

Built with enterprise-grade best practices, the pipeline supports data quality, governance, testing, and maintainability standards aligned with  data engineering expectations.

---

## Architecture

```
/data-pipeline/
│
├── configs/
│   └── pipeline_config.yaml        # Configurable parameters and paths
│
├── data/
│   ├── raw/                       # Raw input JSON and CSV files
│   ├── bronze/                    # Landing zone (raw ingested data)
│   ├── silver/                    # Cleaned and conformed datasets
│   └── gold/                      # Aggregated, KPI-ready data
│
├── src/
│   ├── __init__.py                # Makes 'src' a package
│   ├── ingestion.py               # Handles file ingestion and raw data validation
│   ├── bronze_to_silver.py        # Cleans and standardizes raw data
│   ├── silver_to_gold.py          # Aggregates and enriches data for analysis
│   ├── visualization.py           # Generates Seaborn visualizations
│   ├── utils.py                   # Utility functions (logging, config parsing)
|
├── tests/                         # Pytest test cases for each module
│   ├── __init__.py                # Makes 'tests' a package
│   ├── test_ingest.py
│   ├── test_bronze_to_silver.py
│   ├── test_silver_to_gold.py
│   ├── test_visualization.py
|
├── requirements.txt               # Python dependencies
├── run_pipeline.py                # Entry point for running the entire pipeline
├── Dockerfile
├── .github/
│   └── workflows/
│       └── python-pipeline.yml
├── pyproject.toml
└── .flake8
├── README.md                     # This file
└── .gitignore                    # Standard gitignore rules
```
---

## Features and Best Practices

### Modular, Reusable Code

* Each pipeline layer and functional area is encapsulated in its own module for clarity and reuse.
* Utilities (logging, config parsing) centralized for consistent behavior.

### Configuration-Driven

* Uses `pipeline_config.yaml` to avoid hardcoded paths or parameters.
* Enables environment-specific overrides (dev/test/prod).

### Robust Data Ingestion

* Supports JSON and CSV files with validation, schema checks, and error handling.
* Uses Python typing and pydantic models (optional) for schema enforcement.

### Data Quality and Transformations

* Bronze layer ingests raw data with minimal changes.
* Silver layer cleans, standardizes, and removes duplicates.
* Gold layer aggregates KPIs and prepares data for analysis.

### Logging and Error Handling

* Centralized Python `logging` with structured log messages.
* Exceptions caught with informative error logs to facilitate debugging.

### Testing with Pytest

* Comprehensive unit and integration tests cover all layers.
* Tests include edge cases: missing fields, corrupt files, empty datasets.
* Fixtures and mocks isolate external dependencies.

### Python Best Practices

* PEP8 and PEP257 compliant with clear docstrings.
* Type annotations for functions.
* Context managers for file and resource handling.
* Use of f-strings for clean formatting.
* Dependency management via `requirements.txt`.

### Visualization & Reporting

* Use Seaborn for clear, customizable visual insights.
* Visualizations saved as images for sharing and audit.

### Version Control and CI/CD Ready

* `.gitignore` for typical artifacts.
* Easily extendable for GitHub Actions or Azure Pipelines integration.

---

## Setup Instructions

### Prerequisites

* Python 3.9+
* `pip` package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Update `configs/pipeline_config.yaml` with your environment specifics, e.g.:

```yaml
input_path: "./data/raw/"
bronze_path: "./data/bronze/"
silver_path: "./data/silver/"
gold_path: "./data/gold/"
log_level: "INFO"
```

---

## Usage

Run the entire pipeline:

```bash
python run_pipeline.py --config configs/pipeline_config.yaml
```

---

## Example Python Snippet: Ingestion Module

```python
from typing import List
import os
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

def ingest_files(input_dir: str, supported_formats: List[str] = ['csv', 'json']) -> pd.DataFrame:
    """
    Reads and concatenates all supported files from input_dir into a single DataFrame.
    Handles errors gracefully and logs progress.
    """
    all_data = []
    path = Path(input_dir)
    if not path.exists():
        logger.error(f"Input directory {input_dir} does not exist.")
        return pd.DataFrame()

    for ext in supported_formats:
        files = list(path.glob(f'*.{ext}'))
        logger.info(f"Found {len(files)} {ext} files.")
        for file in files:
            try:
                if ext == 'csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_json(file, lines=True)
                all_data.append(df)
                logger.info(f"Successfully ingested {file.name}")
            except Exception as e:
                logger.error(f"Failed to ingest {file.name}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        logger.warning("No data ingested.")
        return pd.DataFrame()
```

---

## Testing

Run all tests:

```bash
pytest --maxfail=3 --disable-warnings -q
```

Example of a simple test in `src/tests/test_ingestion.py`:

```python
import pytest
from src.ingestion import ingest_files
import pandas as pd

def test_ingest_empty_dir(tmp_path):
    df = ingest_files(str(tmp_path))
    assert df.empty

def test_ingest_csv(tmp_path):
    test_csv = tmp_path / "test.csv"
    test_csv.write_text("id,name\n1,Alice\n2,Bob")
    df = ingest_files(str(tmp_path))
    assert len(df) == 2
    assert list(df.columns) == ['id', 'name']
```

---

## Logging

Logging is configured in `run_pipeline.py` with levels set in the config file. Logs provide traceability and support root cause analysis for issues.

---

## License

