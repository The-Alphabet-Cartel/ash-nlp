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
Retry Utility with Exponential Backoff for Ash-NLP Service
---
FILE VERSION: v5.0-3-5.3-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 5.3 - Error Handling Completion
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Provide retry decorator with exponential backoff
- Handle transient failures gracefully
- Support both sync and async functions
- Configurable retry parameters

USAGE:
    @retry(max_attempts=3, base_delay=1.0, max_delay=30.0)
    async def call_model(text: str):
        return await model.predict(text)
"""

import asyncio
import functools
import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple, Type, Union

# Module version
__version__ = "v5.0-3-5.3-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Retry Configuration
# =============================================================================


@dataclass
class RetryConfig:
    """
    Configuration for retry behavior.

    Attributes:
        max_attempts: Maximum number of attempts (including initial)
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        jitter: Add random jitter to prevent thundering herd
        retryable_exceptions: Tuple of exceptions to retry on
    """

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)

    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for a given attempt number.

        Uses exponential backoff: delay = base_delay * (exponential_base ^ attempt)

        Args:
            attempt: Current attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        delay = self.base_delay * (self.exponential_base**attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            # Add ±25% jitter
            jitter_range = delay * 0.25
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.1, delay)  # Minimum 100ms

        return delay


# Default configuration
DEFAULT_RETRY_CONFIG = RetryConfig()


# =============================================================================
# Retry Result
# =============================================================================


@dataclass
class RetryResult:
    """
    Result of a retry operation.

    Attributes:
        success: Whether the operation succeeded
        result: The return value (if successful)
        attempts: Number of attempts made
        total_time: Total time spent (including delays)
        last_error: The last error encountered (if failed)
    """

    success: bool
    result: Any = None
    attempts: int = 0
    total_time: float = 0.0
    last_error: Optional[Exception] = None


# =============================================================================
# Sync Retry Implementation
# =============================================================================


def retry_sync(
    func: Callable,
    config: Optional[RetryConfig] = None,
    *args,
    **kwargs,
) -> RetryResult:
    """
    Execute a synchronous function with retry logic.

    Args:
        func: Function to execute
        config: Retry configuration
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        RetryResult with outcome details
    """
    config = config or DEFAULT_RETRY_CONFIG
    start_time = time.perf_counter()
    last_error = None

    for attempt in range(config.max_attempts):
        try:
            result = func(*args, **kwargs)
            return RetryResult(
                success=True,
                result=result,
                attempts=attempt + 1,
                total_time=time.perf_counter() - start_time,
            )
        except config.retryable_exceptions as e:
            last_error = e
            remaining = config.max_attempts - attempt - 1

            if remaining > 0:
                delay = config.calculate_delay(attempt)
                logger.warning(
                    f"Retry {attempt + 1}/{config.max_attempts} for {func.__name__} "
                    f"failed: {e}. Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)
            else:
                logger.error(
                    f"All {config.max_attempts} attempts failed for {func.__name__}: {e}"
                )

    return RetryResult(
        success=False,
        attempts=config.max_attempts,
        total_time=time.perf_counter() - start_time,
        last_error=last_error,
    )


# =============================================================================
# Async Retry Implementation
# =============================================================================


async def retry_async(
    func: Callable,
    config: Optional[RetryConfig] = None,
    *args,
    **kwargs,
) -> RetryResult:
    """
    Execute an asynchronous function with retry logic.

    Args:
        func: Async function to execute
        config: Retry configuration
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        RetryResult with outcome details
    """
    config = config or DEFAULT_RETRY_CONFIG
    start_time = time.perf_counter()
    last_error = None

    for attempt in range(config.max_attempts):
        try:
            result = await func(*args, **kwargs)
            return RetryResult(
                success=True,
                result=result,
                attempts=attempt + 1,
                total_time=time.perf_counter() - start_time,
            )
        except config.retryable_exceptions as e:
            last_error = e
            remaining = config.max_attempts - attempt - 1

            if remaining > 0:
                delay = config.calculate_delay(attempt)
                logger.warning(
                    f"Retry {attempt + 1}/{config.max_attempts} for {func.__name__} "
                    f"failed: {e}. Retrying in {delay:.2f}s..."
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"All {config.max_attempts} attempts failed for {func.__name__}: {e}"
                )

    return RetryResult(
        success=False,
        attempts=config.max_attempts,
        total_time=time.perf_counter() - start_time,
        last_error=last_error,
    )


# =============================================================================
# Retry Decorator
# =============================================================================


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    reraise: bool = True,
) -> Callable:
    """
    Decorator for adding retry logic to functions.

    Supports both synchronous and asynchronous functions.

    Args:
        max_attempts: Maximum number of attempts
        base_delay: Initial delay between retries
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff
        jitter: Add random jitter to delays
        retryable_exceptions: Exceptions to retry on
        reraise: Re-raise the last exception if all retries fail

    Returns:
        Decorated function

    Example:
        @retry(max_attempts=3, base_delay=1.0)
        async def fetch_data():
            return await api.get_data()

        @retry(max_attempts=5, retryable_exceptions=(ConnectionError, TimeoutError))
        def connect():
            return database.connect()
    """
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        retryable_exceptions=retryable_exceptions,
    )

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            # Async function
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                result = await retry_async(func, config, *args, **kwargs)
                if result.success:
                    return result.result
                if reraise and result.last_error:
                    raise result.last_error
                return None

            return async_wrapper
        else:
            # Sync function
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                result = retry_sync(func, config, *args, **kwargs)
                if result.success:
                    return result.result
                if reraise and result.last_error:
                    raise result.last_error
                return None

            return sync_wrapper

    return decorator


# =============================================================================
# Convenience Functions
# =============================================================================


def with_retry(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    *args,
    **kwargs,
) -> Any:
    """
    Execute a function with retry logic (convenience wrapper).

    Args:
        func: Function to execute
        max_attempts: Maximum attempts
        base_delay: Initial delay
        *args: Function arguments
        **kwargs: Function keyword arguments

    Returns:
        Function result

    Raises:
        Last exception if all retries fail
    """
    config = RetryConfig(max_attempts=max_attempts, base_delay=base_delay)
    result = retry_sync(func, config, *args, **kwargs)

    if result.success:
        return result.result
    if result.last_error:
        raise result.last_error
    raise RuntimeError(f"All {max_attempts} retry attempts failed")


async def with_retry_async(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    *args,
    **kwargs,
) -> Any:
    """
    Execute an async function with retry logic (convenience wrapper).

    Args:
        func: Async function to execute
        max_attempts: Maximum attempts
        base_delay: Initial delay
        *args: Function arguments
        **kwargs: Function keyword arguments

    Returns:
        Function result

    Raises:
        Last exception if all retries fail
    """
    config = RetryConfig(max_attempts=max_attempts, base_delay=base_delay)
    result = await retry_async(func, config, *args, **kwargs)

    if result.success:
        return result.result
    if result.last_error:
        raise result.last_error
    raise RuntimeError(f"All {max_attempts} retry attempts failed")


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "RetryConfig",
    "RetryResult",
    "retry",
    "retry_sync",
    "retry_async",
    "with_retry",
    "with_retry_async",
    "DEFAULT_RETRY_CONFIG",
]
