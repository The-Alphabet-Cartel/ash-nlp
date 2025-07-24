# Enhanced Dockerfile for Ash NLP Service
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Create non-root user (same UID as main bot)
RUN useradd -m -u 1001 nlpuser && chown -R nlpuser:nlpuser /app

# Create directories for data, models, logs, and learning data
RUN mkdir -p /app/data /app/models/cache /app/logs /app/learning_data && \
    chown -R nlpuser:nlpuser /app/data /app/models /app/logs /app/learning_data

USER nlpuser

# Set default environment variables (can be overridden by docker-compose or .env)
## Core Python settings
ENV PYTHONUNBUFFERED=1

## Hugging Face Configuration
ENV HUGGINGFACE_HUB_TOKEN=
ENV HUGGINGFACE_CACHE_DIR=/models/cache

## Learning System Configuration
ENV ENABLE_LEARNING_SYSTEM=true
ENV LEARNING_RATE=0.1
ENV MAX_LEARNING_ADJUSTMENTS_PER_DAY=50
ENV LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json
ENV MIN_CONFIDENCE_ADJUSTMENT=0.05
ENV MAX_CONFIDENCE_ADJUSTMENT=0.30

## Model Configuration
ENV DEPRESSION_MODEL=rafalposwiata/deproberta-large-depression
ENV SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
ENV MODEL_CACHE_DIR=./models/cache

## Hardware Configuration
ENV DEVICE=auto
ENV MODEL_PRECISION=float16

## Performance Tuning
ENV MAX_BATCH_SIZE=32
ENV INFERENCE_THREADS=4
ENV MAX_CONCURRENT_REQUESTS=10
ENV REQUEST_TIMEOUT=30

## Server Configuration
ENV NLP_SERVICE_HOST=0.0.0.0
ENV NLP_SERVICE_PORT=8881
ENV UVICORN_WORKERS=1
ENV RELOAD_ON_CHANGES=false

## Logging Configuration
ENV LOG_LEVEL=INFO
ENV LOG_FILE=nlp_service.log
ENV ENABLE_DEBUG_LOGGING=false

## Storage Paths
ENV DATA_DIR=./data
ENV MODELS_DIR=./models/cache
ENV LOGS_DIR=./logs
ENV LEARNING_DATA_DIR=./learning_data

## Crisis Detection Thresholds
ENV HIGH_CRISIS_THRESHOLD=0.7
ENV MEDIUM_CRISIS_THRESHOLD=0.4
ENV LOW_CRISIS_THRESHOLD=0.2

## Rate Limiting
ENV MAX_REQUESTS_PER_MINUTE=60
ENV MAX_REQUESTS_PER_HOUR=1000

## Security
ENV ALLOWED_IPS=10.20.30.0/24,127.0.0.1,::1
ENV ENABLE_CORS=true

# Expose port
EXPOSE 8881

# Health check - give more time for model loading and use curl
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8881/health || exit 1

# Start the service with explicit host binding
CMD ["python", "nlp_main.py"]