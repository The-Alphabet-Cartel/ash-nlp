# Dockerfile for NLP Service
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Create non-root user (same UID as main bot)
RUN useradd -m -u 1001 nlpuser && chown -R nlpuser:nlpuser /app
USER nlpuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8081/health')" || exit 1

# Expose port
EXPOSE 8081

# Start the service
CMD ["python", "main.py"]