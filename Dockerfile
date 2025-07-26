# Use official lightweight Python image (slim variant for smaller size)
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for pandas and other libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Optional: expose port if pipeline serves a web service
# EXPOSE 8080

# Default command to run the pipeline with the config file
CMD ["python", "run_pipeline.py", "--config", "configs/pipeline_config.yaml"]
