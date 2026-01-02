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
Structured JSON Logging for Ash-NLP Service
---
FILE VERSION: v5.0-3-6.1-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 6.1 - Structured Logging
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Provide JSON-formatted log output for log aggregation
- Support structured fields for filtering and searching
- Compatible with ELK Stack, Loki, CloudWatch, etc.
- Maintain human-readable fallback for development

LOG FORMAT (JSON):
{
    "timestamp": "2026-01-01T12:00:00.000Z",
    "level": "INFO",
    "logger": "ash-nlp.api",
    "message": "Request processed",
    "service": "ash-nlp",
    "request_id": "req_abc123",
    "duration_ms": 45.2,
    ...extra_fields
}

USAGE:
    from src.utils.logging import setup_logging, get_logger

    # Setup at application start
    setup_logging(json_format=True, level="INFO")

    # Get logger
    logger = get_logger(__name__)
    logger.info("Processing request", extra={"request_id": "abc123"})
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Module version
__version__ = "v5.0-3-6.1-1"

# Service identifier
SERVICE_NAME = "ash-nlp"


# =============================================================================
# JSON Formatter
# =============================================================================


class JSONFormatter(logging.Formatter):
    """
    JSON log formatter for structured logging.

    Outputs logs as single-line JSON objects suitable for
    log aggregation systems.

    Attributes:
        service_name: Name of the service
        include_extra: Whether to include extra fields
        exclude_fields: Fields to exclude from output
    """

    # Fields to always exclude from extra
    EXCLUDE_FIELDS = {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
        "taskName",
    }

    def __init__(
        self,
        service_name: str = SERVICE_NAME,
        include_extra: bool = True,
        exclude_fields: Optional[set] = None,
    ):
        super().__init__()
        self.service_name = service_name
        self.include_extra = include_extra
        self.exclude_fields = exclude_fields or set()

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON string
        """
        # Base log structure
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
        }

        # Add location info for errors/warnings
        if record.levelno >= logging.WARNING:
            log_data["location"] = {
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
            }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if self.include_extra:
            extras = self._extract_extras(record)
            if extras:
                log_data.update(extras)

        return json.dumps(log_data, default=str, ensure_ascii=False)

    def _extract_extras(self, record: logging.LogRecord) -> Dict[str, Any]:
        """
        Extract extra fields from log record.

        Args:
            record: Log record

        Returns:
            Dictionary of extra fields
        """
        extras = {}
        exclude = self.EXCLUDE_FIELDS | self.exclude_fields

        for key, value in record.__dict__.items():
            if key not in exclude and not key.startswith("_"):
                extras[key] = value

        return extras


# =============================================================================
# Human-Readable Formatter
# =============================================================================


class HumanFormatter(logging.Formatter):
    """
    Human-readable colored log formatter for development.

    Uses ANSI colors for different log levels.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, use_colors: bool = True):
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.use_colors = use_colors and sys.stdout.isatty()

    def format(self, record: logging.LogRecord) -> str:
        """Format with optional colors."""
        message = super().format(record)

        if self.use_colors:
            color = self.COLORS.get(record.levelname, "")
            if color:
                # Color the level name
                message = message.replace(
                    record.levelname,
                    f"{color}{record.levelname}{self.RESET}",
                    1,
                )

        # Add extras if present
        extras = self._format_extras(record)
        if extras:
            message += f" | {extras}"

        return message

    def _format_extras(self, record: logging.LogRecord) -> str:
        """Format extra fields for display."""
        extras = []
        exclude = JSONFormatter.EXCLUDE_FIELDS

        for key, value in record.__dict__.items():
            if key not in exclude and not key.startswith("_"):
                extras.append(f"{key}={value}")

        return " ".join(extras)


# =============================================================================
# Log Filter
# =============================================================================


class ServiceFilter(logging.Filter):
    """
    Filter that adds service context to all records.

    Attributes:
        service_name: Name of the service
        extra_context: Additional context to add
    """

    def __init__(
        self,
        service_name: str = SERVICE_NAME,
        extra_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        self.service_name = service_name
        self.extra_context = extra_context or {}

    def filter(self, record: logging.LogRecord) -> bool:
        """Add service context to record."""
        record.service = self.service_name

        for key, value in self.extra_context.items():
            if not hasattr(record, key):
                setattr(record, key, value)

        return True


# =============================================================================
# Setup Functions
# =============================================================================


def setup_logging(
    level: str = "INFO",
    json_format: bool = False,
    service_name: str = SERVICE_NAME,
    log_file: Optional[str] = None,
) -> None:
    """
    Configure logging for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON format (True) or human-readable (False)
        service_name: Service name for logs
        log_file: Optional file path for logging
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Choose formatter
    if json_format:
        formatter = JSONFormatter(service_name=service_name)
    else:
        formatter = HumanFormatter()

    # Add service filter
    service_filter = ServiceFilter(service_name=service_name)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(service_filter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        # Always use JSON for file output
        file_handler.setFormatter(JSONFormatter(service_name=service_name))
        file_handler.addFilter(service_filter)
        root_logger.addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("transformers").setLevel(logging.WARNING)

    root_logger.info(
        f"Logging configured",
        extra={
            "level": level,
            "format": "json" if json_format else "human",
            "service": service_name,
        },
    )


def setup_logging_from_env() -> None:
    """
    Configure logging from environment variables.

    Environment variables:
        NLP_LOG_LEVEL: Log level (default: INFO)
        NLP_LOG_FORMAT: json or human (default: human)
        NLP_LOG_FILE: Optional log file path
        NLP_SERVICE_NAME: Service name (default: ash-nlp)
    """
    level = os.environ.get("NLP_LOG_LEVEL", "INFO")
    format_type = os.environ.get("NLP_LOG_FORMAT", "human")
    log_file = os.environ.get("NLP_LOG_FILE")
    service_name = os.environ.get("NLP_SERVICE_NAME", SERVICE_NAME)

    setup_logging(
        level=level,
        json_format=format_type.lower() == "json",
        service_name=service_name,
        log_file=log_file,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger
    """
    return logging.getLogger(name)


# =============================================================================
# Context Logging
# =============================================================================


class LogContext:
    """
    Context manager for adding fields to all logs within a block.

    Example:
        with LogContext(request_id="abc123", user_id="user1"):
            logger.info("Processing")  # Includes request_id and user_id
    """

    _context: Dict[str, Any] = {}

    def __init__(self, **kwargs):
        self.fields = kwargs
        self._old_context = {}

    def __enter__(self):
        self._old_context = LogContext._context.copy()
        LogContext._context.update(self.fields)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LogContext._context = self._old_context

    @classmethod
    def get_context(cls) -> Dict[str, Any]:
        """Get current context fields."""
        return cls._context.copy()

    @classmethod
    def add_field(cls, key: str, value: Any) -> None:
        """Add a field to current context."""
        cls._context[key] = value

    @classmethod
    def clear(cls) -> None:
        """Clear context."""
        cls._context.clear()


class ContextFilter(logging.Filter):
    """Filter that adds LogContext fields to records."""

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in LogContext.get_context().items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True


# =============================================================================
# Specialized Loggers
# =============================================================================


def get_request_logger(request_id: str) -> logging.LoggerAdapter:
    """
    Get a logger adapter that includes request_id in all logs.

    Args:
        request_id: Request ID to include

    Returns:
        Logger adapter with request_id context
    """
    logger = logging.getLogger("ash-nlp.request")
    return logging.LoggerAdapter(logger, {"request_id": request_id})


def get_model_logger(model_name: str) -> logging.LoggerAdapter:
    """
    Get a logger adapter for model operations.

    Args:
        model_name: Model name to include

    Returns:
        Logger adapter with model context
    """
    logger = logging.getLogger(f"ash-nlp.model.{model_name}")
    return logging.LoggerAdapter(logger, {"model": model_name})


# =============================================================================
# Log Event Helpers
# =============================================================================


def log_crisis_detection(
    logger: logging.Logger,
    request_id: str,
    severity: str,
    confidence: float,
    processing_time_ms: float,
) -> None:
    """Log a crisis detection event."""
    logger.info(
        f"Crisis detected: severity={severity}, confidence={confidence:.2f}",
        extra={
            "event": "crisis_detection",
            "request_id": request_id,
            "severity": severity,
            "confidence": confidence,
            "processing_time_ms": processing_time_ms,
        },
    )


def log_model_inference(
    logger: logging.Logger,
    model_name: str,
    duration_ms: float,
    success: bool,
    error: Optional[str] = None,
) -> None:
    """Log a model inference event."""
    if success:
        logger.debug(
            f"Model inference: {model_name} ({duration_ms:.1f}ms)",
            extra={
                "event": "model_inference",
                "model": model_name,
                "duration_ms": duration_ms,
                "success": True,
            },
        )
    else:
        logger.error(
            f"Model inference failed: {model_name}",
            extra={
                "event": "model_inference",
                "model": model_name,
                "duration_ms": duration_ms,
                "success": False,
                "error": error,
            },
        )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Formatters
    "JSONFormatter",
    "HumanFormatter",
    # Filters
    "ServiceFilter",
    "ContextFilter",
    # Setup
    "setup_logging",
    "setup_logging_from_env",
    "get_logger",
    # Context
    "LogContext",
    # Specialized loggers
    "get_request_logger",
    "get_model_logger",
    # Event helpers
    "log_crisis_detection",
    "log_model_inference",
    # Constants
    "SERVICE_NAME",
]
