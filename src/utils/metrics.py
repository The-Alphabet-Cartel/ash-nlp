"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Prometheus Metrics for Ash-NLP Service (Optional)
---
FILE VERSION: v5.0-3-6.3-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 6.3 - Performance Profiling
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Provide Prometheus metrics endpoint (/metrics)
- Track request counts, latencies, and errors
- Monitor model inference performance
- Support Grafana dashboards

METRICS:
- ash_nlp_requests_total: Total API requests
- ash_nlp_request_duration_seconds: Request latency histogram
- ash_nlp_crisis_detected_total: Crisis detections by severity
- ash_nlp_model_inference_duration_seconds: Model inference latency
- ash_nlp_model_errors_total: Model failures
- ash_nlp_models_loaded: Number of loaded models
- ash_nlp_gpu_memory_bytes: GPU memory usage (if available)

USAGE:
    from src.utils.metrics import (
        setup_metrics,
        record_request,
        record_crisis_detection,
    )

    # Setup at application start
    setup_metrics(app)

    # Record metrics
    with record_request("/analyze"):
        result = process_request()

NOTE: This module is OPTIONAL. If prometheus_client is not installed,
a no-op implementation is used and metrics are simply logged.
"""

import logging
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional

# Module version
__version__ = "v5.0-3-6.3-1"

# Initialize logger
logger = logging.getLogger(__name__)

# Flag for prometheus availability
PROMETHEUS_AVAILABLE = False

try:
    from prometheus_client import (
        CollectorRegistry,
        Counter,
        Gauge,
        Histogram,
        generate_latest,
        CONTENT_TYPE_LATEST,
    )

    PROMETHEUS_AVAILABLE = True
    logger.debug("prometheus_client available")
except ImportError:
    logger.info("prometheus_client not installed, metrics disabled")


# =============================================================================
# Metric Definitions (when Prometheus is available)
# =============================================================================

if PROMETHEUS_AVAILABLE:
    # Custom registry (don't pollute default)
    REGISTRY = CollectorRegistry()

    # Request metrics
    REQUEST_COUNT = Counter(
        "ash_nlp_requests_total",
        "Total number of API requests",
        ["endpoint", "method", "status"],
        registry=REGISTRY,
    )

    REQUEST_DURATION = Histogram(
        "ash_nlp_request_duration_seconds",
        "Request duration in seconds",
        ["endpoint"],
        buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
        registry=REGISTRY,
    )

    # Crisis detection metrics
    CRISIS_DETECTED = Counter(
        "ash_nlp_crisis_detected_total",
        "Total crisis detections",
        ["severity"],
        registry=REGISTRY,
    )

    CRISIS_SCORE = Histogram(
        "ash_nlp_crisis_score",
        "Distribution of crisis scores",
        buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        registry=REGISTRY,
    )

    # Model metrics
    MODEL_INFERENCE_DURATION = Histogram(
        "ash_nlp_model_inference_duration_seconds",
        "Model inference duration in seconds",
        ["model"],
        buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
        registry=REGISTRY,
    )

    MODEL_ERRORS = Counter(
        "ash_nlp_model_errors_total",
        "Total model errors",
        ["model", "error_type"],
        registry=REGISTRY,
    )

    MODELS_LOADED = Gauge(
        "ash_nlp_models_loaded",
        "Number of models currently loaded",
        registry=REGISTRY,
    )

    # System metrics
    GPU_MEMORY = Gauge(
        "ash_nlp_gpu_memory_bytes",
        "GPU memory usage in bytes",
        ["type"],  # allocated, reserved
        registry=REGISTRY,
    )

    UPTIME = Gauge(
        "ash_nlp_uptime_seconds",
        "Service uptime in seconds",
        registry=REGISTRY,
    )


# =============================================================================
# No-Op Implementations (when Prometheus not available)
# =============================================================================


class NoOpMetric:
    """No-op metric for when prometheus_client is not available."""

    def inc(self, *args, **kwargs):
        pass

    def dec(self, *args, **kwargs):
        pass

    def set(self, *args, **kwargs):
        pass

    def observe(self, *args, **kwargs):
        pass

    def labels(self, *args, **kwargs):
        return self

    def time(self):
        return self._time_context()

    @contextmanager
    def _time_context(self):
        yield


class NoOpRegistry:
    """No-op registry."""

    pass


if not PROMETHEUS_AVAILABLE:
    REGISTRY = NoOpRegistry()
    REQUEST_COUNT = NoOpMetric()
    REQUEST_DURATION = NoOpMetric()
    CRISIS_DETECTED = NoOpMetric()
    CRISIS_SCORE = NoOpMetric()
    MODEL_INFERENCE_DURATION = NoOpMetric()
    MODEL_ERRORS = NoOpMetric()
    MODELS_LOADED = NoOpMetric()
    GPU_MEMORY = NoOpMetric()
    UPTIME = NoOpMetric()


# =============================================================================
# Recording Functions
# =============================================================================


@contextmanager
def record_request(endpoint: str, method: str = "POST"):
    """
    Context manager to record request metrics.

    Args:
        endpoint: API endpoint path
        method: HTTP method

    Example:
        with record_request("/analyze", "POST") as ctx:
            result = process()
            ctx["status"] = 200
    """
    start_time = time.perf_counter()
    context = {"status": 200}

    try:
        yield context
    except Exception:
        context["status"] = 500
        raise
    finally:
        duration = time.perf_counter() - start_time

        REQUEST_COUNT.labels(
            endpoint=endpoint,
            method=method,
            status=str(context["status"]),
        ).inc()

        REQUEST_DURATION.labels(endpoint=endpoint).observe(duration)


def record_crisis_detection(
    severity: str,
    score: float,
    detected: bool = True,
) -> None:
    """
    Record a crisis detection event.

    Args:
        severity: Severity level (safe, low, medium, high, critical)
        score: Crisis score (0.0 - 1.0)
        detected: Whether crisis was detected
    """
    if detected:
        CRISIS_DETECTED.labels(severity=severity).inc()

    CRISIS_SCORE.observe(score)

    logger.debug(f"Metric: crisis_detection severity={severity} score={score:.2f}")


@contextmanager
def record_model_inference(model_name: str):
    """
    Context manager to record model inference metrics.

    Args:
        model_name: Name of the model

    Example:
        with record_model_inference("bart"):
            result = model.predict(text)
    """
    start_time = time.perf_counter()

    try:
        yield
    except Exception as e:
        MODEL_ERRORS.labels(
            model=model_name,
            error_type=type(e).__name__,
        ).inc()
        raise
    finally:
        duration = time.perf_counter() - start_time
        MODEL_INFERENCE_DURATION.labels(model=model_name).observe(duration)


def record_model_error(model_name: str, error_type: str) -> None:
    """
    Record a model error.

    Args:
        model_name: Name of the model
        error_type: Type of error
    """
    MODEL_ERRORS.labels(model=model_name, error_type=error_type).inc()


def set_models_loaded(count: int) -> None:
    """
    Set the number of loaded models.

    Args:
        count: Number of models loaded
    """
    MODELS_LOADED.set(count)


def update_gpu_memory() -> None:
    """Update GPU memory metrics (if GPU available)."""
    try:
        import torch

        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated()
            reserved = torch.cuda.memory_reserved()

            GPU_MEMORY.labels(type="allocated").set(allocated)
            GPU_MEMORY.labels(type="reserved").set(reserved)
    except ImportError:
        pass
    except Exception as e:
        logger.debug(f"Could not update GPU metrics: {e}")


def set_uptime(seconds: float) -> None:
    """
    Set the uptime metric.

    Args:
        seconds: Uptime in seconds
    """
    UPTIME.set(seconds)


# =============================================================================
# FastAPI Integration
# =============================================================================


def setup_metrics(app) -> None:
    """
    Setup Prometheus metrics endpoint for FastAPI.

    Adds /metrics endpoint to the application.

    Args:
        app: FastAPI application instance
    """
    if not PROMETHEUS_AVAILABLE:
        logger.info("Prometheus not available, /metrics endpoint disabled")
        return

    from fastapi import Response

    @app.get("/metrics")
    async def metrics_endpoint():
        """Prometheus metrics endpoint."""
        return Response(
            content=generate_latest(REGISTRY),
            media_type=CONTENT_TYPE_LATEST,
        )

    logger.info("Prometheus metrics endpoint enabled at /metrics")


def get_metrics_middleware():
    """
    Get middleware for automatic request metrics.

    Returns:
        Middleware class or None if Prometheus unavailable
    """
    if not PROMETHEUS_AVAILABLE:
        return None

    from starlette.middleware.base import BaseHTTPMiddleware
    from fastapi import Request

    class MetricsMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Skip metrics endpoint itself
            if request.url.path == "/metrics":
                return await call_next(request)

            start_time = time.perf_counter()

            try:
                response = await call_next(request)
                status = response.status_code
            except Exception:
                status = 500
                raise
            finally:
                duration = time.perf_counter() - start_time

                REQUEST_COUNT.labels(
                    endpoint=request.url.path,
                    method=request.method,
                    status=str(status),
                ).inc()

                REQUEST_DURATION.labels(endpoint=request.url.path).observe(duration)

            return response

    return MetricsMiddleware


# =============================================================================
# Health Check Integration
# =============================================================================


def get_metrics_status() -> Dict[str, Any]:
    """
    Get metrics status for health checks.

    Returns:
        Dictionary with metrics status
    """
    return {
        "prometheus_available": PROMETHEUS_AVAILABLE,
        "metrics_endpoint": "/metrics" if PROMETHEUS_AVAILABLE else None,
    }


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Availability flag
    "PROMETHEUS_AVAILABLE",
    # Recording functions
    "record_request",
    "record_crisis_detection",
    "record_model_inference",
    "record_model_error",
    "set_models_loaded",
    "update_gpu_memory",
    "set_uptime",
    # FastAPI integration
    "setup_metrics",
    "get_metrics_middleware",
    # Status
    "get_metrics_status",
    # Registry (for custom metrics)
    "REGISTRY",
]
