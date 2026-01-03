# ============================================================================
# Ash-NLP v5.0 Production Dockerfile
# ============================================================================
# FILE VERSION: v5.0-7-1.3-1
# LAST MODIFIED: 2025-01-02
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
#   Stage 1 (builder): Install dependencies
#   Stage 2 (runtime): Minimal production image with runtime model init
#
# MODEL CACHING:
#   Models are downloaded at container startup (not build time).
#   This keeps the Docker image small and enables version checking.
#   Models cache to /app/models-cache (mount as volume for persistence).
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

# Note: Models are downloaded at runtime via entrypoint.py
# This keeps the Docker image small (~500MB vs ~4GB with models)


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

# Create models-cache directory (models download at runtime)
RUN mkdir -p /app/models-cache && chown ${APP_USER}:${APP_USER} /app/models-cache

# Copy application code
COPY --chown=${APP_USER}:${APP_USER} . /app/

# Make entrypoint executable
RUN chmod +x /app/entrypoint.py 2>/dev/null || true

# Switch to non-root user
USER ${APP_USER}

# Expose port
EXPOSE 30880

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:30880/health || exit 1

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command - uses entrypoint for model initialization
CMD ["python", "/app/entrypoint.py"]
