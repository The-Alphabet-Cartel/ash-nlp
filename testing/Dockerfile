# syntax=docker/dockerfile:1.4
# Ash-NLP Testing Suite Container - FINAL FIX
# FILE VERSION: v5.0.5
# LAST MODIFIED: 2025-12-30
# CLEAN ARCHITECTURE: v5.0 Compliant
# Repository: https://github.com/the-alphabet-cartel/ash-nlp
#
# FIX: Uses python3.11 -m pip to ensure packages install to correct Python version

# Base image with CUDA support for GPU acceleration
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Metadata
LABEL maintainer="The Alphabet Cartel <https://alphabetcartel.org>"
LABEL description="Ash-NLP v5.0 Testing Suite - Crisis Detection Model Evaluation"
LABEL version="5.0.5"

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=0
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies (including bash and dos2unix)
RUN apt-get update && apt-get install -y \
    bash \
    python3.11 \
    python3-pip \
    python3.11-dev \
    git \
    curl \
    wget \
    ca-certificates \
    build-essential \
    dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# CRITICAL FIX: Upgrade pip using python3.11 explicitly
RUN --mount=type=cache,target=/root/.cache/pip \
    python3.11 -m pip install --upgrade pip setuptools wheel

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt /app/

# CRITICAL FIX: Install Python dependencies using python3.11 -m pip
# This ensures packages install to Python 3.11, not Python 3.10!
RUN --mount=type=cache,target=/root/.cache/pip \
    python3.11 -m pip install -r requirements.txt

# Copy testing framework code
COPY ./ /app/testing/
#COPY ../managers/ /app/managers/
#COPY ../config/ /app/config/

# Create necessary directories
RUN mkdir -p /app/testing/reports/output \
    /app/testing/cache/models \
    /app/logs

# Set permissions
RUN chmod -R 755 /app/testing \
    && chmod -R 777 /app/testing/reports/output \
    && chmod -R 777 /app/testing/cache \
    && chmod -R 777 /app/logs

# Copy entrypoint script and ensure proper format
COPY ./docker/testing-entrypoint.sh /usr/local/bin/testing-entrypoint.sh

# Fix line endings and make executable
RUN dos2unix /usr/local/bin/testing-entrypoint.sh 2>/dev/null || true \
    && chmod +x /usr/local/bin/testing-entrypoint.sh

# Verify bash exists
RUN bash --version

# Verify packages are installed correctly
RUN python3.11 -c "import transformers; print('Transformers:', transformers.__version__)"
RUN python3.11 -c "import torch; print('PyTorch:', torch.__version__)"

# Expose port for potential web interface (future)
EXPOSE 30880

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3.11 -c "import torch; print('CUDA:', torch.cuda.is_available())" || exit 1

# Default entrypoint
ENTRYPOINT ["/bin/bash", "/usr/local/bin/testing-entrypoint.sh"]

# Default command: run help
CMD ["--help"]
