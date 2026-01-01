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
Utilities Package for Ash-NLP Service
---
FILE VERSION: v5.0-3-7.4-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 7 - Performance Optimization
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PACKAGE CONTENTS:
- retry.py: Retry decorator with exponential backoff
- timeout.py: Timeout wrapper for model inference
- alerting.py: Discord webhook alerting service
- logging.py: Structured JSON logging
- metrics.py: Prometheus metrics (optional)
- cache.py: Response caching layer
"""

__version__ = "v5.0-3-7.4-1"

# Retry utilities
from src.utils.retry import (
    RetryConfig,
    RetryResult,
    retry,
    retry_sync,
    retry_async,
    with_retry,
    with_retry_async,
)

# Timeout utilities
from src.utils.timeout import (
    TimeoutError,
    InferenceTimeoutError,
    timeout,
    inference_timeout,
    with_timeout_async,
    with_timeout_sync,
    with_inference_timeout,
    get_recommended_timeout,
)

# Alerting
from src.utils.alerting import (
    DiscordAlerter,
    Alert,
    AlertSeverity,
    ThrottleConfig,
    create_discord_alerter,
    get_alerter,
    set_alerter,
)

# Logging
from src.utils.logging import (
    JSONFormatter,
    HumanFormatter,
    setup_logging,
    setup_logging_from_env,
    get_logger,
    LogContext,
    get_request_logger,
    get_model_logger,
    log_crisis_detection,
    log_model_inference,
)

# Metrics (optional - may be no-op if prometheus_client not installed)
from src.utils.metrics import (
    PROMETHEUS_AVAILABLE,
    record_request,
    record_crisis_detection,
    record_model_inference,
    record_model_error,
    set_models_loaded,
    setup_metrics,
    get_metrics_status,
)

# Cache
from src.utils.cache import (
    ResponseCache,
    CacheEntry,
    create_response_cache,
    cached_response,
    cached_response_async,
)

__all__ = [
    # Retry
    "RetryConfig",
    "RetryResult",
    "retry",
    "retry_sync",
    "retry_async",
    "with_retry",
    "with_retry_async",
    # Timeout
    "TimeoutError",
    "InferenceTimeoutError",
    "timeout",
    "inference_timeout",
    "with_timeout_async",
    "with_timeout_sync",
    "with_inference_timeout",
    "get_recommended_timeout",
    # Alerting
    "DiscordAlerter",
    "Alert",
    "AlertSeverity",
    "ThrottleConfig",
    "create_discord_alerter",
    "get_alerter",
    "set_alerter",
    # Logging
    "JSONFormatter",
    "HumanFormatter",
    "setup_logging",
    "setup_logging_from_env",
    "get_logger",
    "LogContext",
    "get_request_logger",
    "get_model_logger",
    "log_crisis_detection",
    "log_model_inference",
    # Metrics
    "PROMETHEUS_AVAILABLE",
    "record_request",
    "record_crisis_detection",
    "record_model_inference",
    "record_model_error",
    "set_models_loaded",
    "setup_metrics",
    "get_metrics_status",
    # Cache
    "ResponseCache",
    "CacheEntry",
    "create_response_cache",
    "cached_response",
    "cached_response_async",
]
