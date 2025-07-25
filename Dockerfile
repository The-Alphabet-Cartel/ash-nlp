# Multi-stage Dockerfile for Ash NLP Service - Production Ready
# Build stage
FROM python:3.11-slim AS builder

# Install build dependencies for GPU libraries and ML packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies in virtual environment
# Optimized for RTX 3050 and PyTorch/Transformers
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim AS production

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Create non-root user for security (matching main bot UID)
RUN useradd -m -u 1001 nlpuser

# Create necessary directories with proper ownership
RUN mkdir -p /app/data /app/models/cache /app/logs /app/learning_data && \
    chown -R nlpuser:nlpuser /app

# Copy service code
COPY --chown=nlpuser:nlpuser . .

# Switch to non-root user
USER nlpuser

# Set default environment variables optimized for your hardware
## Core Python settings
ENV PYTHONUNBUFFERED=1

## Hugging Face Configuration
ENV HUGGINGFACE_HUB_TOKEN=
ENV HUGGINGFACE_CACHE_DIR=./models/cache

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

## Hardware Configuration - Optimized for RTX 3050
ENV DEVICE=auto
ENV MODEL_PRECISION=float16

## Performance Tuning - Tuned for Ryzen 7 7700x + 64GB RAM
ENV MAX_BATCH_SIZE=32
ENV INFERENCE_THREADS=8
ENV MAX_CONCURRENT_REQUESTS=12
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

## Health Check Configuration
ENV HEALTH_CHECK_INTERVAL=60
ENV HEALTH_CHECK_TIMEOUT=30
ENV HEALTH_CHECK_START_PERIOD=300

## Crisis Detection Thresholds
ENV HIGH_CRISIS_THRESHOLD=0.55
ENV MEDIUM_CRISIS_THRESHOLD=0.28
ENV LOW_CRISIS_THRESHOLD=0.16

## Rate Limiting
ENV MAX_REQUESTS_PER_MINUTE=60
ENV MAX_REQUESTS_PER_HOUR=1000

## Security
ENV ALLOWED_IPS=10.20.30.0/24,127.0.0.1,::1
ENV ENABLE_CORS=true

# Expose port
EXPOSE 8881

# Health check - optimized for model loading time
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8881/health || exit 1

# Start the service
CMD ["python", "nlp_main.py"]