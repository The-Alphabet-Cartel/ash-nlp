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
API Middleware for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.4-2
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.4 - API Layer
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Generate unique request IDs for tracking
- Log all requests and responses
- Handle exceptions with consistent error format
- Track request timing and performance
- Implement rate limiting (optional)
"""

import logging
import time
import uuid
from datetime import datetime
from typing import Callable, Dict, Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Module version
__version__ = "v5.0-3-4.4-2"

# Initialize logger
logger = logging.getLogger(__name__)

# Request ID header name
REQUEST_ID_HEADER = "X-Request-ID"


# =============================================================================
# Request Context
# =============================================================================


class RequestContext:
    """
    Context holder for request-scoped data.

    Stores request ID, timing, and other metadata
    accessible throughout request lifecycle.
    """

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start_time = time.perf_counter()
        self.metadata: Dict[str, any] = {}

    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        return (time.perf_counter() - self.start_time) * 1000

    def set(self, key: str, value: any) -> None:
        """Set metadata value."""
        self.metadata[key] = value

    def get(self, key: str, default: any = None) -> any:
        """Get metadata value."""
        return self.metadata.get(key, default)


# Store for request contexts (request-scoped)
_request_contexts: Dict[str, RequestContext] = {}


def get_request_context(request: Request) -> Optional[RequestContext]:
    """Get request context for current request."""
    request_id = getattr(request.state, "request_id", None)
    if request_id:
        return _request_contexts.get(request_id)
    return None


def get_request_id(request: Request) -> Optional[str]:
    """Get request ID from current request."""
    return getattr(request.state, "request_id", None)


# =============================================================================
# Request ID Middleware
# =============================================================================


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and track request IDs.

    - Generates unique request ID for each request
    - Accepts client-provided request ID (if valid)
    - Adds request ID to response headers
    - Creates request context for tracking
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get or generate request ID
        request_id = request.headers.get(REQUEST_ID_HEADER)

        if not request_id or not self._is_valid_request_id(request_id):
            request_id = self._generate_request_id()

        # Store in request state
        request.state.request_id = request_id

        # Create request context
        context = RequestContext(request_id)
        _request_contexts[request_id] = context

        try:
            # Process request
            response = await call_next(request)

            # Add request ID to response headers
            response.headers[REQUEST_ID_HEADER] = request_id

            return response

        finally:
            # Cleanup context
            _request_contexts.pop(request_id, None)

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return f"req_{uuid.uuid4().hex[:12]}"

    def _is_valid_request_id(self, request_id: str) -> bool:
        """Validate request ID format."""
        if not request_id:
            return False
        if len(request_id) > 64:
            return False
        # Allow alphanumeric, hyphens, underscores
        return all(c.isalnum() or c in "-_" for c in request_id)


# =============================================================================
# Logging Middleware
# =============================================================================


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for request/response logging.

    Logs:
    - Request method, path, client IP
    - Response status code
    - Processing time
    - Request ID for correlation
    """

    # Paths to skip logging (health checks, etc.)
    SKIP_PATHS = {"/health", "/healthz", "/ready", "/metrics"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip logging for certain paths
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        # Get request info
        request_id = getattr(request.state, "request_id", "unknown")
        method = request.method
        path = request.url.path
        client_ip = self._get_client_ip(request)

        # Log request
        logger.info(
            f"📥 {method} {path}",
            extra={
                "request_id": request_id,
                "client_ip": client_ip,
                "method": method,
                "path": path,
            },
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log response
            log_level = logging.INFO if response.status_code < 400 else logging.WARNING
            logger.log(
                log_level,
                f"📤 {method} {path} → {response.status_code} ({duration_ms:.1f}ms)",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )

            return response

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"❌ {method} {path} → ERROR ({duration_ms:.1f}ms): {e}",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "duration_ms": duration_ms,
                },
                exc_info=True,
            )
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check forwarded headers (for reverse proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to direct client
        if request.client:
            return request.client.host

        return "unknown"


# =============================================================================
# Error Handling Middleware
# =============================================================================


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for consistent error handling.

    Catches unhandled exceptions and returns
    consistent JSON error responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)

        except Exception as e:
            request_id = getattr(request.state, "request_id", None)

            logger.error(
                f"Unhandled exception: {e}",
                extra={"request_id": request_id},
                exc_info=True,
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_error",
                    "message": "An unexpected error occurred",
                    "request_id": request_id,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                },
                headers={REQUEST_ID_HEADER: request_id} if request_id else {},
            )


# =============================================================================
# Rate Limiting Middleware (Simple Implementation)
# =============================================================================


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware.

    Note: For production, use Redis-based rate limiting
    for distributed deployments.

    Attributes:
        requests_per_minute: Max requests per minute per client
        enabled: Whether rate limiting is active
        bypass_key: Optional secret key to bypass rate limiting (for internal tools)
    """

    # Header name for internal bypass key
    BYPASS_HEADER = "X-Ash-Internal-Key"

    def __init__(
        self,
        app: FastAPI,
        requests_per_minute: int = 60,
        enabled: bool = True,
        bypass_key: Optional[str] = None,
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.enabled = enabled
        self.bypass_key = bypass_key
        self._request_counts: Dict[str, list] = {}

        # Log bypass key status (without revealing the key)
        if self.bypass_key:
            logger.info("🔑 Rate limit bypass key configured for internal tools")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.enabled:
            return await call_next(request)

        # Skip rate limiting for health checks
        if request.url.path in {"/health", "/healthz", "/ready"}:
            return await call_next(request)

        # Skip rate limiting for internal tools with valid bypass key
        if self.bypass_key:
            provided_key = request.headers.get(self.BYPASS_HEADER)
            if provided_key and provided_key == self.bypass_key:
                logger.debug("🔓 Rate limit bypassed for internal tool")
                return await call_next(request)

        client_id = self._get_client_id(request)

        if self._is_rate_limited(client_id):
            request_id = getattr(request.state, "request_id", None)

            logger.warning(
                f"Rate limit exceeded for {client_id}",
                extra={"request_id": request_id, "client_id": client_id},
            )

            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": f"Rate limit exceeded. Max {self.requests_per_minute} requests per minute.",
                    "request_id": request_id,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                },
                headers={
                    "Retry-After": "60",
                    REQUEST_ID_HEADER: request_id or "",
                },
            )

        # Record request
        self._record_request(client_id)

        return await call_next(request)

    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier."""
        # Use API key if provided
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"key:{api_key[:8]}"

        # Fall back to IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0].strip()}"

        if request.client:
            return f"ip:{request.client.host}"

        return "unknown"

    def _is_rate_limited(self, client_id: str) -> bool:
        """Check if client is rate limited."""
        now = time.time()
        window_start = now - 60  # 1 minute window

        if client_id not in self._request_counts:
            return False

        # Count requests in window
        recent_requests = [
            ts for ts in self._request_counts[client_id] if ts > window_start
        ]

        return len(recent_requests) >= self.requests_per_minute

    def _record_request(self, client_id: str) -> None:
        """Record a request for rate limiting."""
        now = time.time()

        if client_id not in self._request_counts:
            self._request_counts[client_id] = []

        self._request_counts[client_id].append(now)

        # Cleanup old entries (older than 2 minutes)
        cutoff = now - 120
        self._request_counts[client_id] = [
            ts for ts in self._request_counts[client_id] if ts > cutoff
        ]


# =============================================================================
# Middleware Setup Function
# =============================================================================


def setup_middleware(
    app: FastAPI,
    enable_rate_limiting: bool = True,
    requests_per_minute: int = 60,
    rate_limit_bypass_key: Optional[str] = None,
) -> None:
    """
    Setup all middleware for the FastAPI application.

    Order matters! Middleware is executed in reverse order of addition.

    Args:
        app: FastAPI application instance
        enable_rate_limiting: Whether to enable rate limiting
        requests_per_minute: Rate limit threshold
        rate_limit_bypass_key: Optional secret key to bypass rate limiting (for internal tools)
    """
    # Add middleware in reverse execution order
    # (last added = first executed)

    # 1. Error handling (outermost - catches all errors)
    app.add_middleware(ErrorHandlingMiddleware)

    # 2. Logging (logs all requests/responses)
    app.add_middleware(LoggingMiddleware)

    # 3. Rate limiting (before processing)
    if enable_rate_limiting:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=requests_per_minute,
            enabled=True,
            bypass_key=rate_limit_bypass_key,
        )

    # 4. Request ID (innermost - generates ID first)
    app.add_middleware(RequestIDMiddleware)

    logger.info(
        f"🔧 Middleware configured "
        f"(rate_limiting={enable_rate_limiting}, "
        f"rpm={requests_per_minute}, "
        f"bypass_key={'configured' if rate_limit_bypass_key else 'none'})"
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "RequestIDMiddleware",
    "LoggingMiddleware",
    "ErrorHandlingMiddleware",
    "RateLimitMiddleware",
    "RequestContext",
    "setup_middleware",
    "get_request_context",
    "get_request_id",
    "REQUEST_ID_HEADER",
]
