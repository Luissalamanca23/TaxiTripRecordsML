# Airlines ML Docker Container
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for ML libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY conf/ conf/
COPY tests/ tests/

# Install the project
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data/{01_raw,02_intermediate,03_primary,04_feature,05_model_input,06_models,07_model_output,08_reporting} && \
    mkdir -p logs notebooks

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash airlines_user && \
    chown -R airlines_user:airlines_user /app

# Switch to non-root user
USER airlines_user

# Expose ports for Kedro Viz and Jupyter
EXPOSE 4141 8888

# Default command
CMD ["kedro", "run"]