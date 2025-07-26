# Use official lightweight Python image (slim for smaller size)
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir inside container
WORKDIR /app

# Install system dependencies required for pandas, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for Docker layer caching
COPY requirements.txt .

# Upgrade pip and install python dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port if your pipeline serves anything (optional)
# EXPOSE 8080

# Default command: run pipeline with config
CMD ["python", "run_pipeline.py", "--config", "configs/pipeline_config.yaml"]
