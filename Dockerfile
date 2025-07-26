# Use official Python image as base
FROM python:3.9-slim

# Metadata labels
LABEL maintainer="Your Name <you@example.com>"
LABEL description="Modular Data Pipeline for CSV/JSON Ingestion and Visualization"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Default command (can override in docker run)
CMD ["python", "run_pipeline.py", "--config", "configs/pipeline_config.yaml"]
