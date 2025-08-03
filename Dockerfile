# Dockerfile for Ash NLP Service - Three Model Ensemble Architecture
# Enhanced for DistilBERT emotional distress detection

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Create non-root user with /app as home directory (no separate home dir)
RUN groupadd -g 1001 nlp && \
    useradd -g 1001 -u 1001 -d /app -M nlp

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies in virtual environment
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=nlp:nlp . .

# Create necessary directories with proper ownership
RUN mkdir -p ./models/cache ./data ./logs ./learning_data && \
    chown -R nlp:nlp /app && \
    chmod 755 /app

# Switch to non-root user
USER nlp

# Set working directory
WORKDIR /app

# Set default environment variables optimized for Three Zero-Shot Model Ensemble
ENV TZ="America/Los_Angeles"

## Core Python settings
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"
ENV PYTHONPATH="/app"

## Hugging Face Configuration
ENV NLP_HUGGINGFACE_CACHE_DIR="./models/cache"
ENV HF_HOME="/app/models/cache"
# ENV TRANSFORMERS_CACHE="/app/models/cache"
ENV HF_DATASETS_CACHE="/app/models/cache"
ENV TORCH_HOME="/app/models/cache"
ENV XDG_CACHE_HOME="/app/models/cache"

## Mode
ENV NLP_ENSEMBLE_MODE="consensus"

## Learning System Configuration
ENV GLOBAL_ENABLE_LEARNING_SYSTEM="true"
ENV NLP_LEARNING_RATE="0.1"
ENV NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY="50"
ENV NLP_LEARNING_PERSISTENCE_FILE="./learning_data/adjustments.json"
ENV NLP_MIN_CONFIDENCE_ADJUSTMENT="0.05"
ENV NLP_MAX_CONFIDENCE_ADJUSTMENT="0.30"

## Three-Model Configuration
ENV NLP_DEPRESSION_MODEL="MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
ENV NLP_SENTIMENT_MODEL="Lowerated/lm6-deberta-v3-topic-sentiment"
ENV NLP_EMOTIONAL_DISTRESS_MODEL="facebook/bart-large-mnli"
ENV NLP_MODEL_CACHE_DIR="./models/cache"

## Ensemble Configuration
ENV NLP_ENSEMBLE_MODE="consensus"
ENV NLP_GAP_DETECTION_THRESHOLD="0.4"
ENV NLP_DISAGREEMENT_THRESHOLD="0.5"
ENV NLP_AUTO_FLAG_DISAGREEMENTS="true"

## Hardware Configuration - Optimized for RTX 3060 (12GB VRAM) with three models
ENV NLP_DEVICE="auto"
ENV NLP_MODEL_PRECISION="float16"

## Performance Tuning - Optimized for Ryzen 7 5800X (8C/16T) + RTX 3060 (12GB) + 64GB RAM
ENV NLP_MAX_BATCH_SIZE="48"
ENV NLP_INFERENCE_THREADS="16"
ENV NLP_MAX_CONCURRENT_REQUESTS="20"
ENV NLP_REQUEST_TIMEOUT="35"

## Server Configuration
ENV GLOBAL_NLP_API_PORT="8881"
ENV NLP_UVICORN_WORKERS="1"
ENV NLP_RELOAD_ON_CHANGES="false"

## Logging Configuration
ENV GLOBAL_LOG_LEVEL="INFO"
ENV NLP_LOG_FILE="nlp_service.log"
ENV NLP_FLIP_SENTIMENT_LOGIC="false"

## Storage Paths
ENV NLP_DATA_DIR="./data"
ENV NLP_MODELS_DIR="./models/cache"
ENV NLP_LOGS_DIR="./logs"
ENV NLP_LEARNING_DATA_DIR="./learning_data"

## Zero-Shot Labels
ENV NLP_ZERO_SHOT_LABEL_SET="enhanced_crisis"
ENV NLP_ENABLE_LABEL_SET_SWITCHING="true"
ENV NLP_INCLUDE_RAW_LABELS="true"
ENV NLP_LOG_LABEL_MAPPINGS="true"
ENV NLP_TRACK_LABEL_PERFORMANCE="true"

## Crisis Detection Thresholds - Adjusted for ensemble
ENV NLP_HIGH_CRISIS_THRESHOLD="0.45"
ENV NLP_MEDIUM_CRISIS_THRESHOLD="0.25"
ENV NLP_LOW_CRISIS_THRESHOLD="0.15"

# UPDATED: Legacy thresholds (update values)
ENV NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD="0.45"
ENV NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD="0.25"
ENV NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD="0.12"

# Additional threshold controls (new)
ENV NLP_MILD_CRISIS_THRESHOLD="0.25"
ENV NLP_NEGATIVE_RESPONSE_THRESHOLD="0.65"
ENV NLP_UNKNOWN_RESPONSE_THRESHOLD="0.45"

# Safety controls (new)
ENV NLP_CONSENSUS_SAFETY_BIAS="0.05"
ENV NLP_ENABLE_SAFETY_OVERRIDE="true"

# UPDATED: Model weights
ENV NLP_DEPRESSION_MODEL_WEIGHT="0.6"
ENV NLP_SENTIMENT_MODEL_WEIGHT="0.15"
ENV NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT="0.25"

# UPDATED: Gap detection
ENV NLP_GAP_DETECTION_THRESHOLD="0.25"
ENV NLP_DISAGREEMENT_THRESHOLD="0.35"
ENV NLP_AUTO_FLAG_DISAGREEMENTS="true"

# NEW: Consensus mapping thresholds
ENV NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD="0.50"
ENV NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD="0.30"
ENV NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD="0.40"
ENV NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD="0.70"
ENV NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD="0.50"

# NEW: Staff review thresholds
ENV NLP_STAFF_REVIEW_HIGH_ALWAYS="true"
ENV NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD="0.45"
ENV NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD="0.75"
ENV NLP_STAFF_REVIEW_ON_MODEL_DISAGREEMENT="true"

# NEW: Safety controls
ENV NLP_CONSENSUS_SAFETY_BIAS="0.03"
ENV NLP_ENABLE_SAFETY_OVERRIDE="true"

## Rate Limiting - Optimized for RTX 3060 (12GB) + Ryzen 7 5800X performance
ENV NLP_MAX_REQUESTS_PER_MINUTE="120"
ENV NLP_MAX_REQUESTS_PER_HOUR="2000"

## Security
ENV GLOBAL_ALLOWED_IPS="10.20.30.0/24,127.0.0.1,::1"
ENV GLOBAL_ENABLE_CORS="true"

## Experimental Features
ENV NLP_ENABLE_ENSEMBLE_ANALYSIS="true"
ENV NLP_ENABLE_GAP_DETECTION="true"
ENV NLP_ENABLE_CONFIDENCE_SPREADING="true"
ENV NLP_LOG_MODEL_DISAGREEMENTS="true"

# Expose port
EXPOSE 8881

# Health check - optimized for RTX 3060 (12GB) model loading time
HEALTHCHECK --interval=60s --timeout=35s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8881/health || exit 1

# Start the service
CMD ["python", "main.py"]

# Updated labels for API server version
LABEL maintainer="The Alphabet Cartel" \
      version="3.0" \
      description="Ash NLP Server - Mental Health Support with Analytics" \
      org.opencontainers.image.source="https://github.com/The-Alphabet-Cartel/ash" \
      feature.conversation-isolation="enabled" \
      feature.api-server="enabled" \
      feature.analytics-dashboard="supported" \
      api.port="8881" \
      api.endpoints="/health,/stats,/analyze,/learning_statistics"