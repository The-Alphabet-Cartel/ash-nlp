# Ash-NLP Utilities Reference

**FILE VERSION**: v5.0-3-6.4-1  
**LAST MODIFIED**: 2026-01-01  
**PHASE**: Phase 3 Complete  

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | https://alphabetcartel.org

---

## Overview

The `src/utils/` package provides production utilities for Ash-NLP:

| Module | Description |
|--------|-------------|
| `retry.py` | Retry decorator with exponential backoff |
| `timeout.py` | Timeout wrapper for model inference |
| `alerting.py` | Discord webhook alerting service |
| `logging.py` | Structured JSON logging |
| `metrics.py` | Prometheus metrics (optional) |

---

## Retry Utility

**File**: `src/utils/retry.py`

### Basic Usage

```python
from src.utils import retry

@retry(max_attempts=3, base_delay=1.0)
async def call_external_api():
    return await api.request()

@retry(max_attempts=5, retryable_exceptions=(ConnectionError,))
def connect_database():
    return db.connect()
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_attempts` | 3 | Maximum retry attempts |
| `base_delay` | 1.0 | Initial delay in seconds |
| `max_delay` | 30.0 | Maximum delay cap |
| `exponential_base` | 2.0 | Exponential backoff multiplier |
| `jitter` | True | Add random jitter to prevent thundering herd |
| `retryable_exceptions` | (Exception,) | Exceptions to retry on |

### Backoff Formula

```
delay = base_delay * (exponential_base ^ attempt)
delay = min(delay, max_delay)
delay += random(-25%, +25%)  # if jitter enabled
```

---

## Timeout Utility

**File**: `src/utils/timeout.py`

### Basic Usage

```python
from src.utils import timeout, inference_timeout

# Generic timeout
@timeout(seconds=30.0)
async def slow_operation():
    await asyncio.sleep(60)  # Will raise TimeoutError

# Model-specific timeout
@inference_timeout("bart_crisis", seconds=30.0)
async def run_bart(text: str):
    return await model.predict(text)  # Raises InferenceTimeoutError on timeout
```

### Recommended Timeouts by Model

| Model | Recommended Timeout |
|-------|---------------------|
| BART | 30s |
| Sentiment | 10s |
| Irony | 10s |
| Emotions | 15s |

```python
from src.utils import get_recommended_timeout

timeout_seconds = get_recommended_timeout("bart")  # Returns 30.0
```

---

## Discord Alerting

**File**: `src/utils/alerting.py`

### Setup

1. Create Discord webhook (Server Settings → Integrations → Webhooks)
2. Add to secrets:
   ```bash
   echo "https://discord.com/api/webhooks/..." > secrets/discord_alert_webhook
   chmod 600 secrets/discord_alert_webhook
   ```

### Basic Usage

```python
from src.utils import create_discord_alerter

# Create alerter (loads webhook from secrets)
alerter = create_discord_alerter(secrets_manager=secrets)

# Send alerts
await alerter.send_critical("BART Failed", "Primary model unavailable")
await alerter.send_error("Sentiment Failed", "Model timeout")
await alerter.send_warning("High Latency", "Response time degraded")
await alerter.send_info("System Started", "All models loaded")
await alerter.send_recovery("BART Recovered", "Model operational")
```

### Model-Specific Alerts

```python
# Alert on model failure
await alerter.alert_model_failure(
    model_name="bart",
    error="CUDA out of memory",
    is_critical=True,  # True for BART, False for secondary models
)

# Alert on recovery
await alerter.alert_model_recovery("bart")

# Alert on startup
await alerter.alert_system_startup(models_loaded=4, total_models=4)
```

### Throttling

Alerts are automatically throttled to prevent spam:

| Setting | Default | Description |
|---------|---------|-------------|
| `window_seconds` | 300 (5 min) | Throttle window |
| `max_alerts` | 5 | Max alerts per window |
| `cooldown_seconds` | 600 (10 min) | Cooldown after limit |

---

## Structured Logging

**File**: `src/utils/logging.py`

### Setup

```python
from src.utils import setup_logging

# JSON format (production)
setup_logging(level="INFO", json_format=True)

# Human format (development)
setup_logging(level="DEBUG", json_format=False)

# From environment variables
setup_logging_from_env()
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NLP_LOG_LEVEL` | INFO | Log level |
| `NLP_LOG_FORMAT` | human | `json` or `human` |
| `NLP_LOG_FILE` | None | Optional file path |
| `NLP_SERVICE_NAME` | ash-nlp | Service name in logs |

### JSON Log Format

```json
{
  "timestamp": "2026-01-01T12:00:00.000Z",
  "level": "INFO",
  "logger": "ash-nlp.api",
  "message": "Request processed",
  "service": "ash-nlp",
  "request_id": "req_abc123",
  "duration_ms": 45.2
}
```

### Usage

```python
from src.utils import get_logger, get_request_logger

# Standard logger
logger = get_logger(__name__)
logger.info("Processing message", extra={"message_id": "123"})

# Request-scoped logger
req_logger = get_request_logger("req_abc123")
req_logger.info("Analysis complete")  # Automatically includes request_id
```

---

## Prometheus Metrics (Optional)

**File**: `src/utils/metrics.py`

### Enable Metrics

1. Install prometheus_client:
   ```bash
   pip install prometheus-client
   ```

2. Setup in FastAPI:
   ```python
   from src.utils import setup_metrics
   
   app = FastAPI()
   setup_metrics(app)  # Adds /metrics endpoint
   ```

### Available Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `ash_nlp_requests_total` | Counter | Total API requests |
| `ash_nlp_request_duration_seconds` | Histogram | Request latency |
| `ash_nlp_crisis_detected_total` | Counter | Crisis detections by severity |
| `ash_nlp_model_inference_duration_seconds` | Histogram | Model latency |
| `ash_nlp_model_errors_total` | Counter | Model failures |
| `ash_nlp_models_loaded` | Gauge | Loaded models count |

### Recording Metrics

```python
from src.utils import record_request, record_crisis_detection, record_model_inference

# Request timing
with record_request("/analyze", "POST") as ctx:
    result = process()
    ctx["status"] = 200

# Crisis detection
record_crisis_detection(severity="critical", score=0.92, detected=True)

# Model inference
with record_model_inference("bart"):
    result = model.predict(text)
```

---

## Integration Example

Here's how all utilities work together:

```python
from src.utils import (
    retry,
    inference_timeout,
    get_logger,
    create_discord_alerter,
    record_model_inference,
)

logger = get_logger(__name__)
alerter = create_discord_alerter()

@retry(max_attempts=2, retryable_exceptions=(TimeoutError,))
@inference_timeout("bart", seconds=30.0)
async def run_bart_inference(text: str):
    with record_model_inference("bart"):
        return await bart_model.predict(text)

async def analyze_message(text: str):
    try:
        result = await run_bart_inference(text)
        logger.info("Inference complete", extra={"model": "bart"})
        return result
    except InferenceTimeoutError as e:
        logger.error(f"BART timeout: {e}")
        await alerter.alert_model_failure("bart", str(e), is_critical=True)
        raise
```

---

**Built with care for chosen family** 🏳️‍🌈
