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
COPY --chown=1001:1001 . .

# Set proper permissions on working directories
RUN chmod -R 755 /app && \
    chmod -R 775 ./logs ./data ./learning_data ./cache ./tmp ./backups

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

# Expose port
EXPOSE 8881

# Health check - optimized for RTX 3060 (12GB) model loading time
HEALTHCHECK --interval=60s --timeout=35s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8881/health || exit 1

# Start the service
CMD ["python", "main.py"]

# Updated labels for API server version
LABEL maintainer="The Alphabet Cartel" \
      version="3.1" \
      description="Ash NLP Server - Mental Health Support with Analytics" \
      org.opencontainers.image.source="https://github.com/The-Alphabet-Cartel/ash" \
      feature.conversation-isolation="enabled" \
      feature.api-server="enabled" \
      feature.analytics-dashboard="supported" \
      api.port="8881" \
      api.endpoints="/analyze,/health,/admin/status,/admin/labels/status,/admin/labels/config,/admin/labels/current,/admin/labels/list,/admin/labels/validate,/admin/labels/details/safety_first,/admin/labels/export/safety_first,/admin/labels/simple-switch,/admin/labels/switch,/ensemble/config,/ensemble/health,/ensemble/status,/learning_statistics,/analyze_false_negative,/analyze_false_positive,/update_learning_model"