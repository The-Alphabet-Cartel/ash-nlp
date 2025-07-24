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
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV NLP_SERVICE_HOST=0.0.0.0
ENV NLP_SERVICE_PORT=8881
ENV DEVICE=auto
ENV MODEL_PRECISION=float16
ENV ENABLE_LEARNING_SYSTEM=true

# Expose port
EXPOSE 8881

# Health check - give more time for model loading and use curl
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8881/health || exit 1

# Start the service with explicit host binding
CMD ["python", "nlp_main.py"]