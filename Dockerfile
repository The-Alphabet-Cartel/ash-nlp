# ============================================================================
# Ash-NLP v5.0 Production Dockerfile
# ============================================================================
# FILE VERSION: v5.0-3-4.5-1
# LAST MODIFIED: 2025-12-31
# Repository: https://github.com/the-alphabet-cartel/ash-nlp
# Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
# ============================================================================
#
# USAGE:
#   # Build the image
#   docker build -t ash-nlp:v5.0 .
#
#   # Run with GPU support
#   docker run --gpus all -p 30880:30880 ash-nlp:v5.0
#
#   # Run with docker-compose (recommended)
#   docker-compose up -d
#
# MULTI-STAGE BUILD:
#   Stage 1 (builder): Install dependencies, download models
#   Stage 2 (runtime): Minimal production image
#
# ============================================================================

# =============================================================================
# Stage 1: Builder
# =============================================================================
FROM python:3.11-slim-bookworm AS builder

# Build arguments
ARG HUGGINGFACE_HUB_CACHE=/app/models-cache
ARG PIP_NO_CACHE_DIR=1
ARG PIP_DISABLE_PIP_VERSION_CHECK=1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=${HUGGINGFACE_HUB_CACHE}

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy model download script
COPY --chmod=755 <<'EOF' /app/download_models.py
#!/usr/bin/env python3
"""Download HuggingFace models for offline use."""
import os
import sys

# Set cache directory
cache_dir = os.environ.get("HUGGINGFACE_HUB_CACHE", "/app/models-cache")
os.makedirs(cache_dir, exist_ok=True)

print(f"Downloading models to {cache_dir}...")

try:
    from transformers import pipeline

    # Download BART (Primary model)
    print("📥 Downloading facebook/bart-large-mnli...")
    pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=-1,  # CPU for download
    )

    # Download Sentiment (Secondary model)
    print("📥 Downloading cardiffnlp/twitter-roberta-base-sentiment-latest...")
    pipeline(
        "text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=-1,
    )

    # Download Irony (Tertiary model)
    print("📥 Downloading cardiffnlp/twitter-roberta-base-irony...")
    pipeline(
        "text-classification",
        model="cardiffnlp/twitter-roberta-base-irony",
        device=-1,
    )

    # Download Emotions (Supplementary model)
    print("📥 Downloading SamLowe/roberta-base-go_emotions...")
    pipeline(
        "text-classification",
        model="SamLowe/roberta-base-go_emotions",
        device=-1,
    )

    print("✅ All models downloaded successfully!")

except Exception as e:
    print(f"❌ Error downloading models: {e}")
    sys.exit(1)
EOF

# Download models during build (optional - can be skipped for smaller images)
# Uncomment to pre-download models:
# RUN python /app/download_models.py


# =============================================================================
# Stage 2: Runtime (CUDA)
# =============================================================================
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04 AS runtime

# Labels
LABEL maintainer="The Alphabet Cartel <dev@alphabetcartel.org>"
LABEL org.opencontainers.image.title="Ash-NLP"
LABEL org.opencontainers.image.description="Crisis Detection Backend for The Alphabet Cartel Discord Community"
LABEL org.opencontainers.image.version="5.0.0"
LABEL org.opencontainers.image.vendor="The Alphabet Cartel"
LABEL org.opencontainers.image.url="https://github.com/the-alphabet-cartel/ash-nlp"
LABEL org.opencontainers.image.source="https://github.com/the-alphabet-cartel/ash-nlp"

# Build arguments
ARG APP_USER=nlp
ARG APP_UID=1001
ARG APP_GID=1001

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    # Application
    NLP_ENVIRONMENT=production \
    NLP_API_HOST=0.0.0.0 \
    NLP_API_PORT=30880 \
    NLP_API_WORKERS=1 \
    NLP_LOG_LEVEL=INFO \
    # Model settings
    NLP_MODELS_DEVICE=auto \
    NLP_MODELS_WARMUP_ENABLED=true \
    # HuggingFace cache
    HF_HOME=/app/models-cache \
    # CUDA
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3-pip \
    curl \
    tini \
    tzdata \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd --gid ${APP_GID} ${APP_USER} \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --shell /bin/bash --create-home ${APP_USER}

# Create app directories
RUN mkdir -p /app/config /app/models-cache /app/logs \
    && chown -R ${APP_USER}:${APP_USER} /app

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/dist-packages

# Copy pre-downloaded models from builder (if downloaded)
COPY --from=builder --chown=${APP_USER}:${APP_USER} /app/models-cache /app/models-cache

# Copy application code
COPY --chown=${APP_USER}:${APP_USER} . /app/

# Make entrypoint executable
RUN chmod +x /app/main.py 2>/dev/null || true

# Switch to non-root user
USER ${APP_USER}

# Expose port
EXPOSE 30880

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:30880/health || exit 1

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command
CMD ["python", "-m", "uvicorn", "src.api.app:app", \
     "--host", "0.0.0.0", \
     "--port", "30880", \
     "--workers", "1", \
     "--log-level", "info"]


# =============================================================================
# Stage 2 Alternative: CPU-only Runtime (smaller image)
# =============================================================================
FROM python:3.11-slim-bookworm AS runtime-cpu

# Labels
LABEL maintainer="The Alphabet Cartel <dev@alphabetcartel.org>"
LABEL org.opencontainers.image.title="Ash-NLP (CPU)"
LABEL org.opencontainers.image.description="Crisis Detection Backend - CPU Only"

# Build arguments
ARG APP_USER=nlp
ARG APP_UID=1001
ARG APP_GID=1001

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    NLP_ENVIRONMENT=production \
    NLP_API_HOST=0.0.0.0 \
    NLP_API_PORT=30880 \
    NLP_API_WORKERS=1 \
    NLP_LOG_LEVEL=INFO \
    NLP_MODELS_DEVICE=cpu \
    NLP_MODELS_WARMUP_ENABLED=true \
    HF_HOME=/app/models-cache

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid ${APP_GID} ${APP_USER} \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --shell /bin/bash --create-home ${APP_USER}

# Create app directories
RUN mkdir -p /app/config /app/models-cache /app/logs \
    && chown -R ${APP_USER}:${APP_USER} /app

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY --chown=${APP_USER}:${APP_USER} . /app/

USER ${APP_USER}

EXPOSE 30880

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:30880/health || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["python", "-m", "uvicorn", "src.api.app:app", \
     "--host", "0.0.0.0", \
     "--port", "30880", \
     "--workers", "1", \
     "--log-level", "info"]
