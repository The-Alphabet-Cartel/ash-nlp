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
ENV GLOBAL_PYTHONUNBUFFERED="1"

## Hugging Face Configuration
ENV NLP_HUGGINGFACE_CACHE_DIR="./models/cache"

## Learning System Configuration
ENV GLOBAL_ENABLE_LEARNING_SYSTEM="true"
ENV NLP_LEARNING_RATE="0.1"
ENV NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY="50"
ENV NLP_LEARNING_PERSISTENCE_FILE="./learning_data/adjustments.json"
ENV NLP_MIN_CONFIDENCE_ADJUSTMENT="0.05"
ENV NLP_MAX_CONFIDENCE_ADJUSTMENT="0.30"

## Model Configuration
ENV NLP_DEPRESSION_MODEL="rafalposwiata/deproberta-large-depression"
ENV NLP_SENTIMENT_MODEL="cardiffnlp/twitter-roberta-base-sentiment-latest"
ENV NLP_MODEL_CACHE_DIR="./models/cache"

## Hardware Configuration - Optimized for RTX 3050
ENV NLP_DEVICE="auto"
ENV NLP_MODEL_PRECISION="float16"

## Performance Tuning - Tuned for Ryzen 7 7700x + 64GB RAM
ENV NLP_MAX_BATCH_SIZE="32"
ENV NLP_INFERENCE_THREADS="8"
ENV NLP_MAX_CONCURRENT_REQUESTS="12"
ENV NLP_REQUEST_TIMEOUT="30"

## Server Configuration
ENV NLP_SERVICE_HOST="0.0.0.0"
ENV NLP_SERVICE_PORT="8881"
ENV NLP_UVICORN_WORKERS="1"
ENV NLP_RELOAD_ON_CHANGES="false"

## Logging Configuration
ENV GLOBAL_LOG_LEVEL="INFO"
ENV NLP_LOG_FILE="nlp_service.log"
ENV GLOBAL_ENABLE_DEBUG_LOGGING="false"

## Storage Paths
ENV NLP_DATA_DIR="./data"
ENV NLP_MODELS_DIR="./models/cache"
ENV NLP_LOGS_DIR="./logs"
ENV NLP_LEARNING_DATA_DIR="./learning_data"

## Health Check Configuration
ENV NLP_HEALTH_CHECK_INTERVAL="60"
ENV NLP_HEALTH_CHECK_INTERVAL="30"
ENV NLP_HEALTH_CHECK_START_PERIOD="300"

## Crisis Detection Thresholds
ENV NLP_HIGH_CRISIS_THRESHOLD="0.55"
ENV NLP_MEDIUM_CRISIS_THRESHOLD="0.28"
ENV NLP_LOW_CRISIS_THRESHOLD="0.16"

## Rate Limiting
ENV NLP_MAX_REQUESTS_PER_MINUTE="60"
ENV NLP_MAX_REQUESTS_PER_HOUR="1000"

## Security
ENV GLOBAL_ALLOWED_IPS="10.20.30.0/24,127.0.0.1,::1"
ENV GLOBAL_ENABLE_CORS="true"

# Expose port
EXPOSE 8881

# Health check - optimized for model loading time
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8881/health || exit 1

# Start the service
CMD ["python", "nlp_main.py"]