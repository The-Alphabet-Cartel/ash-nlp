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
Timeout Utility for Ash-NLP Service
---
FILE VERSION: v5.0-3-5.4-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 5.4 - Timeout Handling
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Provide timeout wrapper for model inference
- Handle async timeout with asyncio
- Handle sync timeout with threading
- Prevent hung operations from blocking the system

USAGE:
    @timeout(seconds=30.0)
    async def analyze_message(text: str):
        return await model.predict(text)

    result = await with_timeout(model.predict(text), timeout=10.0)
"""

import asyncio
import concurrent.futures
import functools
import logging
import signal
import sys
import threading
from contextlib import contextmanager
from typing import Any, Callable, Optional, TypeVar, Union

# Module version
__version__ = "v5.0-3-5.4-1"

# Initialize logger
logger = logging.getLogger(__name__)

# Type variable for generic return types
T = TypeVar("T")


# =============================================================================
# Exceptions
# =============================================================================


class TimeoutError(Exception):
    """
    Raised when an operation exceeds its timeout.

    Attributes:
        operation: Name of the operation that timed out
        timeout: The timeout value in seconds
    """

    def __init__(
        self,
        message: str = "Operation timed out",
        operation: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.operation = operation
        self.timeout = timeout

        if operation and timeout:
            message = f"Operation '{operation}' timed out after {timeout}s"
        elif timeout:
            message = f"Operation timed out after {timeout}s"

        super().__init__(message)


class InferenceTimeoutError(TimeoutError):
    """
    Raised when model inference exceeds its timeout.

    This is a specific timeout for ML model operations.
    """

    def __init__(
        self,
        model_name: str,
        timeout: float,
        message: Optional[str] = None,
    ):
        self.model_name = model_name
        if message is None:
            message = f"Model '{model_name}' inference timed out after {timeout}s"
        super().__init__(message=message, operation=model_name, timeout=timeout)


# =============================================================================
# Async Timeout
# =============================================================================


async def with_timeout_async(
    coro,
    timeout: float,
    operation_name: Optional[str] = None,
) -> Any:
    """
    Execute an async coroutine with a timeout.

    Args:
        coro: Coroutine to execute
        timeout: Timeout in seconds
        operation_name: Name for error messages

    Returns:
        Result of the coroutine

    Raises:
        TimeoutError: If operation exceeds timeout
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(
            operation=operation_name or "async operation",
            timeout=timeout,
        )


async def with_inference_timeout(
    coro,
    model_name: str,
    timeout: float = 30.0,
) -> Any:
    """
    Execute model inference with a timeout.

    Specialized wrapper for ML model operations.

    Args:
        coro: Inference coroutine
        model_name: Name of the model (for logging)
        timeout: Timeout in seconds (default: 30s)

    Returns:
        Inference result

    Raises:
        InferenceTimeoutError: If inference exceeds timeout
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        logger.error(f"⏱️ Inference timeout: {model_name} exceeded {timeout}s")
        raise InferenceTimeoutError(model_name=model_name, timeout=timeout)


# =============================================================================
# Sync Timeout (Thread-based)
# =============================================================================


def with_timeout_sync(
    func: Callable[..., T],
    timeout: float,
    operation_name: Optional[str] = None,
    *args,
    **kwargs,
) -> T:
    """
    Execute a synchronous function with a timeout using threads.

    Note: This uses concurrent.futures which cannot forcibly terminate
    the function - it will continue running but the caller will receive
    a TimeoutError. Use with caution for long-running operations.

    Args:
        func: Function to execute
        timeout: Timeout in seconds
        operation_name: Name for error messages
        *args: Function positional arguments
        **kwargs: Function keyword arguments

    Returns:
        Result of the function

    Raises:
        TimeoutError: If operation exceeds timeout
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(
                operation=operation_name or func.__name__,
                timeout=timeout,
            )


# =============================================================================
# Timeout Context Manager
# =============================================================================


@contextmanager
def timeout_context(seconds: float, operation_name: Optional[str] = None):
    """
    Context manager for timeout (Unix only, uses SIGALRM).

    WARNING: This only works on Unix systems and in the main thread.
    For cross-platform support, use with_timeout_sync() instead.

    Args:
        seconds: Timeout in seconds
        operation_name: Name for error messages

    Example:
        with timeout_context(10.0, "database_query"):
            result = slow_database_query()

    Raises:
        TimeoutError: If operation exceeds timeout
    """
    if sys.platform == "win32":
        # Windows doesn't support SIGALRM
        logger.warning(
            "timeout_context not supported on Windows, "
            "operation will run without timeout"
        )
        yield
        return

    def timeout_handler(signum, frame):
        raise TimeoutError(operation=operation_name, timeout=seconds)

    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)

    # Set the alarm
    signal.setitimer(signal.ITIMER_REAL, seconds)

    try:
        yield
    finally:
        # Cancel the alarm
        signal.setitimer(signal.ITIMER_REAL, 0)
        # Restore the old handler
        signal.signal(signal.SIGALRM, old_handler)


# =============================================================================
# Timeout Decorator
# =============================================================================


def timeout(
    seconds: float,
    operation_name: Optional[str] = None,
    reraise: bool = True,
    default: Any = None,
) -> Callable:
    """
    Decorator to add timeout to a function.

    Supports both sync and async functions.

    Args:
        seconds: Timeout in seconds
        operation_name: Name for error messages (defaults to function name)
        reraise: Re-raise TimeoutError (default: True)
        default: Default value to return on timeout (if reraise=False)

    Returns:
        Decorated function

    Example:
        @timeout(seconds=30.0)
        async def slow_operation():
            await asyncio.sleep(60)

        @timeout(seconds=10.0, reraise=False, default=None)
        def maybe_slow():
            return compute_something()
    """

    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__

        if asyncio.iscoroutinefunction(func):
            # Async function
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await with_timeout_async(
                        func(*args, **kwargs),
                        timeout=seconds,
                        operation_name=op_name,
                    )
                except TimeoutError:
                    if reraise:
                        raise
                    logger.warning(f"Timeout in {op_name}, returning default")
                    return default

            return async_wrapper
        else:
            # Sync function
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    return with_timeout_sync(
                        func,
                        timeout=seconds,
                        operation_name=op_name,
                        *args,
                        **kwargs,
                    )
                except TimeoutError:
                    if reraise:
                        raise
                    logger.warning(f"Timeout in {op_name}, returning default")
                    return default

            return sync_wrapper

    return decorator


# =============================================================================
# Inference Timeout Decorator
# =============================================================================


def inference_timeout(
    model_name: str,
    seconds: float = 30.0,
) -> Callable:
    """
    Decorator specifically for model inference operations.

    Args:
        model_name: Name of the model (for logging and errors)
        seconds: Timeout in seconds (default: 30s)

    Returns:
        Decorated function

    Example:
        @inference_timeout("bart_crisis", seconds=30.0)
        async def run_bart(text: str):
            return await bart_model.predict(text)
    """

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await with_inference_timeout(
                    func(*args, **kwargs),
                    model_name=model_name,
                    timeout=seconds,
                )

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    return with_timeout_sync(
                        func,
                        timeout=seconds,
                        operation_name=model_name,
                        *args,
                        **kwargs,
                    )
                except TimeoutError:
                    raise InferenceTimeoutError(
                        model_name=model_name,
                        timeout=seconds,
                    )

            return sync_wrapper

    return decorator


# =============================================================================
# Utility Functions
# =============================================================================


def get_recommended_timeout(model_name: str) -> float:
    """
    Get recommended timeout for a specific model.

    Based on typical inference times observed during testing.

    Args:
        model_name: Name of the model

    Returns:
        Recommended timeout in seconds
    """
    # Recommended timeouts based on model complexity
    TIMEOUTS = {
        "bart": 30.0,  # BART is largest, needs more time
        "bart_crisis": 30.0,
        "sentiment": 10.0,  # Smaller models
        "irony": 10.0,
        "emotions": 15.0,  # Medium size
        "default": 30.0,
    }

    return TIMEOUTS.get(model_name, TIMEOUTS["default"])


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Exceptions
    "TimeoutError",
    "InferenceTimeoutError",
    # Async timeout
    "with_timeout_async",
    "with_inference_timeout",
    # Sync timeout
    "with_timeout_sync",
    "timeout_context",
    # Decorators
    "timeout",
    "inference_timeout",
    # Utilities
    "get_recommended_timeout",
]
