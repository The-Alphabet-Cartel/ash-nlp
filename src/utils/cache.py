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
Response Cache for Ash-NLP Service
---
FILE VERSION: v5.0-3-7.4-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 7.4 - Response Caching
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Cache analysis results for repeated messages
- Reduce redundant model inference
- Provide TTL-based cache expiration
- Thread-safe cache operations
- Memory-bounded cache with LRU eviction

CACHE STRATEGY:
- Key: Hash of normalized message text
- Value: CrisisAssessment result
- TTL: Configurable (default 5 minutes)
- Max Size: Configurable (default 1000 entries)

USAGE:
    from src.utils import ResponseCache, create_response_cache

    cache = create_response_cache(max_size=1000, ttl_seconds=300)

    # Check cache before inference
    cached = cache.get(message)
    if cached:
        return cached

    # Run inference
    result = engine.analyze(message)

    # Cache result
    cache.set(message, result)
"""

import hashlib
import logging
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Optional, TypeVar

# Module version
__version__ = "v5.0-3-7.4-1"

# Initialize logger
logger = logging.getLogger(__name__)

# Type variable for cached values
T = TypeVar("T")


# =============================================================================
# Cache Entry
# =============================================================================


@dataclass
class CacheEntry(Generic[T]):
    """
    A cache entry with value and metadata.

    Attributes:
        value: The cached value
        created_at: Timestamp when entry was created
        expires_at: Timestamp when entry expires
        hits: Number of times entry was accessed
    """

    value: T
    created_at: float
    expires_at: float
    hits: int = 0

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return time.time() > self.expires_at

    def touch(self) -> None:
        """Record a cache hit."""
        self.hits += 1


# =============================================================================
# Response Cache
# =============================================================================


class ResponseCache(Generic[T]):
    """
    Thread-safe LRU cache with TTL expiration.

    Features:
    - Time-based expiration (TTL)
    - Size-based eviction (LRU)
    - Thread-safe operations
    - Cache statistics

    Clean Architecture v5.1 Compliance:
    - Factory function: create_response_cache()
    """

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: float = 300.0,
        normalize_keys: bool = True,
    ):
        """
        Initialize the response cache.

        Args:
            max_size: Maximum number of entries
            ttl_seconds: Time-to-live in seconds
            normalize_keys: Normalize text keys (lowercase, strip)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.normalize_keys = normalize_keys

        # Cache storage (OrderedDict for LRU)
        self._cache: OrderedDict[str, CacheEntry[T]] = OrderedDict()

        # Lock for thread safety
        self._lock = threading.RLock()

        # Statistics
        self._hits: int = 0
        self._misses: int = 0
        self._evictions: int = 0

        logger.debug(
            f"ResponseCache initialized (max_size={max_size}, ttl={ttl_seconds}s)"
        )

    # =========================================================================
    # Core Operations
    # =========================================================================

    def get(self, key: str) -> Optional[T]:
        """
        Get a value from the cache.

        Args:
            key: Cache key (message text)

        Returns:
            Cached value or None if not found/expired
        """
        cache_key = self._make_key(key)

        with self._lock:
            entry = self._cache.get(cache_key)

            if entry is None:
                self._misses += 1
                return None

            # Check expiration
            if entry.is_expired():
                self._remove_entry(cache_key)
                self._misses += 1
                return None

            # Move to end (LRU update)
            self._cache.move_to_end(cache_key)
            entry.touch()
            self._hits += 1

            return entry.value

    def set(self, key: str, value: T, ttl_override: Optional[float] = None) -> None:
        """
        Store a value in the cache.

        Args:
            key: Cache key (message text)
            value: Value to cache
            ttl_override: Override default TTL for this entry
        """
        cache_key = self._make_key(key)
        ttl = ttl_override if ttl_override is not None else self.ttl_seconds
        now = time.time()

        entry = CacheEntry(
            value=value,
            created_at=now,
            expires_at=now + ttl,
        )

        with self._lock:
            # Remove existing entry if present
            if cache_key in self._cache:
                del self._cache[cache_key]

            # Evict oldest entries if at capacity
            while len(self._cache) >= self.max_size:
                self._evict_oldest()

            # Add new entry
            self._cache[cache_key] = entry

    def delete(self, key: str) -> bool:
        """
        Delete an entry from the cache.

        Args:
            key: Cache key

        Returns:
            True if entry was deleted
        """
        cache_key = self._make_key(key)

        with self._lock:
            if cache_key in self._cache:
                del self._cache[cache_key]
                return True
            return False

    def clear(self) -> int:
        """
        Clear all entries from the cache.

        Returns:
            Number of entries cleared
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            logger.info(f"Cache cleared ({count} entries)")
            return count

    def contains(self, key: str) -> bool:
        """
        Check if key exists and is not expired.

        Args:
            key: Cache key

        Returns:
            True if key exists and is valid
        """
        return self.get(key) is not None

    # =========================================================================
    # Maintenance
    # =========================================================================

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns:
            Number of entries removed
        """
        removed = 0

        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items() if entry.is_expired()
            ]

            for key in expired_keys:
                del self._cache[key]
                removed += 1

        if removed > 0:
            logger.debug(f"Cleaned up {removed} expired cache entries")

        return removed

    def _evict_oldest(self) -> None:
        """Evict the oldest (least recently used) entry."""
        if self._cache:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            self._evictions += 1

    def _remove_entry(self, cache_key: str) -> None:
        """Remove a specific entry."""
        if cache_key in self._cache:
            del self._cache[cache_key]

    # =========================================================================
    # Key Management
    # =========================================================================

    def _make_key(self, text: str) -> str:
        """
        Create a cache key from text.

        Uses MD5 hash for fixed-length keys.

        Args:
            text: Original text

        Returns:
            Cache key string
        """
        if self.normalize_keys:
            text = text.lower().strip()

        # Use hash for consistent key length
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    # =========================================================================
    # Statistics
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "ttl_seconds": self.ttl_seconds,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": round(hit_rate, 4),
                "evictions": self._evictions,
            }

    def reset_stats(self) -> None:
        """Reset statistics counters."""
        with self._lock:
            self._hits = 0
            self._misses = 0
            self._evictions = 0

    # =========================================================================
    # Context Manager
    # =========================================================================

    def __len__(self) -> int:
        """Return number of entries."""
        with self._lock:
            return len(self._cache)

    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return self.contains(key)

    def __repr__(self) -> str:
        """String representation."""
        stats = self.get_stats()
        return (
            f"ResponseCache("
            f"size={stats['size']}/{stats['max_size']}, "
            f"hit_rate={stats['hit_rate']:.1%})"
        )


# =============================================================================
# Cached Response Decorator
# =============================================================================


def cached_response(
    cache: ResponseCache,
    key_func: Optional[callable] = None,
    ttl_override: Optional[float] = None,
):
    """
    Decorator to cache function responses.

    Args:
        cache: ResponseCache instance
        key_func: Function to extract cache key from args (default: first arg)
        ttl_override: Override cache TTL for this function

    Example:
        @cached_response(cache, key_func=lambda msg: msg.text)
        def analyze(message):
            return expensive_analysis(message)
    """
    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            elif args:
                cache_key = str(args[0])
            else:
                # Can't cache without a key
                return func(*args, **kwargs)

            # Check cache
            cached = cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit for key: {cache_key[:16]}...")
                return cached

            # Execute function
            result = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl_override)

            return result

        return wrapper

    return decorator


def cached_response_async(
    cache: ResponseCache,
    key_func: Optional[callable] = None,
    ttl_override: Optional[float] = None,
):
    """
    Async version of cached_response decorator.

    Args:
        cache: ResponseCache instance
        key_func: Function to extract cache key from args
        ttl_override: Override cache TTL
    """
    import functools

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            elif args:
                cache_key = str(args[0])
            else:
                return await func(*args, **kwargs)

            # Check cache
            cached = cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit (async) for key: {cache_key[:16]}...")
                return cached

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl_override)

            return result

        return wrapper

    return decorator


# =============================================================================
# Factory Function
# =============================================================================


def create_response_cache(
    max_size: int = 1000,
    ttl_seconds: float = 300.0,
    normalize_keys: bool = True,
    config_manager=None,
) -> ResponseCache:
    """
    Factory function for ResponseCache.

    Args:
        max_size: Maximum cache entries
        ttl_seconds: Time-to-live in seconds
        normalize_keys: Normalize message text before hashing
        config_manager: Optional ConfigManager for settings

    Returns:
        Configured ResponseCache instance
    """
    # Override from config if available
    if config_manager is not None:
        perf_config = config_manager.get_performance_config()
        if perf_config:
            if perf_config.get("cache_enabled", True):
                max_size = perf_config.get("cache_max_size", max_size)
                ttl_seconds = perf_config.get("cache_ttl", ttl_seconds)
            else:
                # Cache disabled - use minimal cache
                max_size = 0
                ttl_seconds = 0

    return ResponseCache(
        max_size=max_size,
        ttl_seconds=ttl_seconds,
        normalize_keys=normalize_keys,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "ResponseCache",
    "CacheEntry",
    "create_response_cache",
    "cached_response",
    "cached_response_async",
]
