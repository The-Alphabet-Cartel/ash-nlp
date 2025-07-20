# Dockerfile for NLP Service
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
USER nlpuser

# Expose port
EXPOSE 8081

# Health check - give more time for model loading and use curl
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8081/health || exit 1

# Start the service with explicit host binding
CMD ["python", "-u", "main.py"]