# ============================================================================
# Ash-NLP v5.0 Production Dockerfile
# ============================================================================
# FILE VERSION: v5.0-8-1.3-1
# LAST MODIFIED: 2026-01-25
# Repository: https://github.com/the-alphabet-cartel/ash-nlp
# Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
# ============================================================================
#
# USAGE:
#   # Build the image
#   docker build -t ash-nlp:v5.0 .
#
#   # Run with GPU support and custom PUID/PGID
#   docker run --gpus all -e PUID=1000 -e PGID=1000 -p 30880:30880 ash-nlp:v5.0
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
# PUID/PGID:
#   Container supports LinuxServer.io-style PUID/PGID environment variables
#   for runtime user configuration. The entrypoint creates the user and
#   fixes permissions before dropping privileges.
#
# ============================================================================

# =============================================================================
# Stage 1: Builder
# =============================================================================
FROM python:3.12-slim AS builder

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

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Note: Models are downloaded at runtime via entrypoint.py
# This keeps the Docker image small (~500MB vs ~4GB with models)


# =============================================================================
# Stage 2: Runtime (CUDA)
# =============================================================================
FROM python:3.12-slim AS runtime

# Default user/group IDs (can be overridden at runtime via PUID/PGID)
ARG DEFAULT_UID=1000
ARG DEFAULT_GID=1000

# Labels
LABEL maintainer="PapaBearDoes <github.com/PapaBearDoes>"
LABEL org.opencontainers.image.title="Ash-NLP"
LABEL org.opencontainers.image.description="Crisis Detection Backend for The Alphabet Cartel Discord Community"
LABEL org.opencontainers.image.version="5.0.0"
LABEL org.opencontainers.image.vendor="The Alphabet Cartel"
LABEL org.opencontainers.image.url="https://github.com/the-alphabet-cartel/ash-nlp"
LABEL org.opencontainers.image.source="https://github.com/the-alphabet-cartel/ash-nlp"

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    APP_HOME=/app \
    PATH="/opt/venv/bin:$PATH" \
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
    HF_HOME=${APP_HOME}/models-cache \
    # CUDA
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    # Default PUID/PGID (LinuxServer.io style)
    PUID=${DEFAULT_UID} \
    PGID=${DEFAULT_GID}

# Install runtime dependencies (Python 3.11 already provided by base image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tini \
    tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create app directories (owned by root initially, entrypoint fixes ownership)
RUN mkdir -p ${APP_HOME}/config ${APP_HOME}/models-cache ${APP_HOME}/logs

# Set working directory
WORKDIR ${APP_HOME}

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY . ${APP_HOME}/

# Make entrypoint executable
RUN chmod +x ${APP_HOME}/entrypoint.py 2>/dev/null || true

# NOTE: We do NOT switch to non-root user here.
# The entrypoint.py handles:
# 1. Creating user with PUID/PGID
# 2. Fixing ownership of /app directories
# 3. Dropping privileges before starting the server

# Expose port
EXPOSE 30880

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:30880/health || exit 1

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command - uses entrypoint for user setup and model initialization
CMD ["python", "/app/entrypoint.py"]
