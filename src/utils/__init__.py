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
FILE VERSION: v5.0-6-4.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 4 (FE-002, FE-004, FE-008)
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
- text_truncation.py: Smart text truncation for long inputs (FE-003)
- history_debug.py: History validation and debugging utilities (FE-007)
"""

__version__ = "v5.0-6-4.0-1"

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
    # FE-002: Discord limits and truncation
    DISCORD_LIMITS,
    truncate_text,
    truncate_at_boundary,
    calculate_embed_size,
    validate_embed_size,
    # FE-008: Conflict alert enhancements
    DEFAULT_CONFLICT_ALERT_THRESHOLD,
    generate_disagreement_chart,
    format_conflict_summary,
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

# Text Truncation (FE-003)
from src.utils.text_truncation import (
    TruncationStrategy,
    TruncationResult,
    TextTruncator,
    create_text_truncator,
    truncate_text,
    estimate_tokens,
)

# History Debug (FE-007)
from src.utils.history_debug import (
    HistoryIssue,
    HistoryValidationIssue,
    HistoryValidationResult,
    HistoryDebugInfo,
    HistoryValidator,
    HistoryDebugLogger,
    create_history_validator,
    create_history_debug_logger,
    validate_history,
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
    # FE-002: Discord limits and truncation
    "DISCORD_LIMITS",
    "truncate_text",
    "truncate_at_boundary",
    "calculate_embed_size",
    "validate_embed_size",
    # FE-008: Conflict alert enhancements
    "DEFAULT_CONFLICT_ALERT_THRESHOLD",
    "generate_disagreement_chart",
    "format_conflict_summary",
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
    # Text Truncation (FE-003)
    "TruncationStrategy",
    "TruncationResult",
    "TextTruncator",
    "create_text_truncator",
    "truncate_text",
    "estimate_tokens",
    # History Debug (FE-007)
    "HistoryIssue",
    "HistoryValidationIssue",
    "HistoryValidationResult",
    "HistoryDebugInfo",
    "HistoryValidator",
    "HistoryDebugLogger",
    "create_history_validator",
    "create_history_debug_logger",
    "validate_history",
]
