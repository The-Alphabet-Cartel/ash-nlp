"""
============================================================================
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Monitor  → Receive messages from Ash-Bot for crisis classification
    Analyze  → Run multi-model ensemble for comprehensive assessment
    Detect   → Identify crisis signals through weighted decision engine
    Respond  → Return actionable crisis assessments to protect our community

============================================================================
Ash-Vigil HTTP Client - Mental Health Risk Detection Integration
----------------------------------------------------------------------------
FILE VERSION: v5.0-3-1.0-2
LAST MODIFIED: 2026-01-31
PHASE: Phase 3 - Ash-Vigil Integration
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================

This module provides the HTTP client for communicating with Ash-Vigil,
the specialized mental health risk detection service running on Bacchus.

Features:
- Async HTTP client with configurable timeout
- Circuit breaker pattern for fault tolerance
- Retry logic with exponential backoff
- Comprehensive logging with Charter-compliant colorization

The client is designed to fail gracefully - if Vigil is unavailable,
Ash-NLP continues with base ensemble scoring while flagging the message
for CRT review.

Usage:
    from src.clients.vigil_client import create_vigil_client
    
    client = create_vigil_client(config_manager)
    result = await client.analyze("I feel so alone")
    
    if result:
        print(f"Risk: {result.risk_score}, Label: {result.risk_label}")
    else:
        print(f"Vigil unavailable: {client.status}")
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-3-1.0-2"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================


class VigilStatus(str, Enum):
    """
    Status of Vigil integration for a given request.
    
    These values are returned in API responses to indicate what happened
    with the Vigil integration for each analysis request.
    
    Attributes:
        USED: Vigil was called successfully and result was incorporated
        SKIPPED: Base score already high enough, Vigil call not needed
        UNAVAILABLE: Network error or Vigil returned an error
        TIMEOUT: Vigil call exceeded the configured timeout
        CIRCUIT_OPEN: Circuit breaker tripped due to repeated failures
        DISABLED: Vigil integration is disabled in configuration
    """
    USED = "used"
    SKIPPED = "skipped"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    CIRCUIT_OPEN = "circuit_open"
    DISABLED = "disabled"


class CircuitState(str, Enum):
    """
    Circuit breaker states.
    
    Attributes:
        CLOSED: Normal operation, calls are allowed
        OPEN: Too many failures, calls are blocked
        HALF_OPEN: Testing if service has recovered
    """
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class VigilResult:
    """
    Result from Ash-Vigil analysis.
    
    Contains the risk assessment returned by Vigil for a given message.
    
    Attributes:
        risk_score: Risk score from 0.0 (safe) to 1.0 (critical risk)
        risk_label: Human-readable risk classification label
        confidence: Model confidence in the prediction (0.0-1.0)
        inference_time_ms: How long Vigil took to process the request
        model_version: Version of the Vigil model that produced this result
        timestamp: When the analysis was performed
    """
    risk_score: float
    risk_label: str
    confidence: float
    inference_time_ms: float
    model_version: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "risk_score": round(self.risk_score, 4),
            "risk_label": self.risk_label,
            "confidence": round(self.confidence, 4),
            "inference_time_ms": round(self.inference_time_ms, 2),
            "model_version": self.model_version,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_vigil_response(cls, response: Dict[str, Any], inference_time_ms: float) -> "VigilResult":
        """
        Create VigilResult from Vigil API response.
        
        Args:
            response: JSON response from Vigil /analyze endpoint
            inference_time_ms: Measured inference time
            
        Returns:
            VigilResult instance
        """
        return cls(
            risk_score=response.get("risk_score", 0.0),
            risk_label=response.get("risk_label", "unknown"),
            confidence=response.get("confidence", 0.0),
            inference_time_ms=inference_time_ms,
            model_version=response.get("model_version"),
        )


# =============================================================================
# Circuit Breaker
# =============================================================================


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for fault tolerance.
    
    Prevents cascade failures when Ash-Vigil is unavailable by tracking
    failures and temporarily blocking calls after too many failures.
    
    States:
    - CLOSED: Normal operation, all calls allowed
    - OPEN: Too many failures, calls blocked until recovery timeout
    - HALF_OPEN: Recovery timeout passed, allowing one test call
    
    Clean Architecture v5.2.3 Compliant:
    - Factory function: create_circuit_breaker()
    - Resilient error handling
    - Comprehensive logging
    
    Attributes:
        failure_threshold: Number of failures before circuit opens
        recovery_timeout_seconds: Seconds to wait before attempting recovery
        state: Current circuit state
        failures: Current failure count
        last_failure_time: Timestamp of most recent failure
    """
    
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout_seconds: int = 30
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of consecutive failures to trigger open state
            recovery_timeout_seconds: Seconds to wait before recovery attempt
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._last_failure_time: Optional[float] = None
        self._total_failures = 0
        self._total_successes = 0
        
        logger.debug(
            f"CircuitBreaker initialized: threshold={failure_threshold}, "
            f"recovery={recovery_timeout_seconds}s"
        )
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self._state
    
    @property
    def failures(self) -> int:
        """Get current consecutive failure count."""
        return self._failures
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is currently open (blocking calls)."""
        return self._state == CircuitState.OPEN
    
    def should_allow_call(self) -> bool:
        """
        Check if a call should be allowed based on circuit state.
        
        Returns:
            True if call should proceed, False if blocked
        """
        if self._state == CircuitState.CLOSED:
            return True
        
        if self._state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self._last_failure_time is None:
                # Shouldn't happen, but allow call
                logger.warning("Circuit OPEN but no last_failure_time - allowing call")
                return True
            
            elapsed = time.time() - self._last_failure_time
            if elapsed >= self.recovery_timeout_seconds:
                # Transition to half-open for test call
                self._state = CircuitState.HALF_OPEN
                logger.info(
                    f"⚡ Circuit transitioning OPEN → HALF_OPEN "
                    f"(recovery timeout {self.recovery_timeout_seconds}s elapsed)"
                )
                return True
            
            # Still in recovery period
            remaining = self.recovery_timeout_seconds - elapsed
            logger.debug(f"Circuit OPEN: blocking call ({remaining:.1f}s until recovery)")
            return False
        
        if self._state == CircuitState.HALF_OPEN:
            # Allow one test call
            return True
        
        # Unknown state - allow call but log warning
        logger.warning(f"Unknown circuit state: {self._state} - allowing call")
        return True
    
    def record_success(self) -> None:
        """
        Record a successful call - resets circuit to closed state.
        
        Called when a Vigil request completes successfully.
        """
        previous_state = self._state
        self._failures = 0
        self._state = CircuitState.CLOSED
        self._last_failure_time = None
        self._total_successes += 1
        
        if previous_state != CircuitState.CLOSED:
            logger.info(
                f"✅ Circuit recovered: {previous_state.value} → CLOSED "
                f"(total successes: {self._total_successes})"
            )
    
    def record_failure(self) -> None:
        """
        Record a failed call - may trigger circuit open.
        
        Called when a Vigil request fails (timeout, error, etc).
        """
        self._failures += 1
        self._last_failure_time = time.time()
        self._total_failures += 1
        
        if self._state == CircuitState.HALF_OPEN:
            # Test call failed - back to open
            self._state = CircuitState.OPEN
            logger.warning(
                f"⚡ Circuit test failed: HALF_OPEN → OPEN "
                f"(failures: {self._failures}, total: {self._total_failures})"
            )
        elif self._failures >= self.failure_threshold:
            # Threshold exceeded - open circuit
            self._state = CircuitState.OPEN
            logger.warning(
                f"🚨 Circuit opened: {self._failures} consecutive failures "
                f"(threshold: {self.failure_threshold}, total: {self._total_failures})"
            )
        else:
            logger.debug(
                f"Circuit failure recorded: {self._failures}/{self.failure_threshold}"
            )
    
    def get_status(self) -> VigilStatus:
        """
        Get appropriate VigilStatus based on circuit state.
        
        Returns:
            VigilStatus.CIRCUIT_OPEN if circuit is open, else UNAVAILABLE
        """
        if self._state == CircuitState.OPEN:
            return VigilStatus.CIRCUIT_OPEN
        return VigilStatus.UNAVAILABLE
    
    def get_health(self) -> Dict[str, Any]:
        """
        Get circuit breaker health information.
        
        Returns:
            Dictionary with circuit state and statistics
        """
        return {
            "state": self._state.value,
            "consecutive_failures": self._failures,
            "failure_threshold": self.failure_threshold,
            "recovery_timeout_seconds": self.recovery_timeout_seconds,
            "total_failures": self._total_failures,
            "total_successes": self._total_successes,
            "last_failure_time": self._last_failure_time,
        }
    
    def reset(self) -> None:
        """
        Manually reset circuit to closed state.
        
        Useful for testing or administrative recovery.
        """
        previous_state = self._state
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._last_failure_time = None
        
        logger.info(f"Circuit manually reset: {previous_state.value} → CLOSED")


def create_circuit_breaker(
    failure_threshold: int = 3,
    recovery_timeout_seconds: int = 30
) -> CircuitBreaker:
    """
    Factory function for CircuitBreaker - MANDATORY.
    
    Args:
        failure_threshold: Number of failures before circuit opens
        recovery_timeout_seconds: Seconds to wait before recovery attempt
        
    Returns:
        Configured CircuitBreaker instance
    """
    return CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout_seconds=recovery_timeout_seconds,
    )


# =============================================================================
# Vigil Client
# =============================================================================


class VigilClient:
    """
    HTTP client for Ash-Vigil mental health risk detection service.
    
    Provides async communication with Ash-Vigil running on Bacchus (10.20.30.14).
    Includes circuit breaker for fault tolerance and retry logic for transient
    failures.
    
    The client is designed to fail gracefully - when Vigil is unavailable,
    it returns None and sets an appropriate status, allowing Ash-NLP to
    continue with base ensemble scoring.
    
    Clean Architecture v5.2.3 Compliant:
    - Factory function: create_vigil_client()
    - Dependency injection via constructor
    - Resilient error handling (Rule #5)
    - Comprehensive logging (Rule #9)
    
    Usage:
        client = create_vigil_client(config_manager)
        
        result = await client.analyze("I feel so alone")
        if result:
            print(f"Risk: {result.risk_score}")
        else:
            print(f"Vigil unavailable: {client.status}")
    
    Attributes:
        host: Vigil server hostname/IP
        port: Vigil server port
        timeout_ms: Request timeout in milliseconds
        retry_attempts: Number of retry attempts on failure
        enabled: Whether the client is enabled
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        timeout_ms: int = 500,
        retry_attempts: int = 1,
        circuit_breaker: Optional[CircuitBreaker] = None,
        enabled: bool = True
    ):
        """
        Initialize Vigil client.
        
        Args:
            host: Vigil server hostname or IP address
            port: Vigil server port number
            timeout_ms: Request timeout in milliseconds (default: 500)
            retry_attempts: Number of retry attempts on transient failure (default: 1)
            circuit_breaker: Pre-configured circuit breaker (creates default if None)
            enabled: Whether the client is enabled (default: True)
        """
        self.host = host
        self.port = port
        self.timeout_ms = timeout_ms
        self.retry_attempts = retry_attempts
        self.enabled = enabled
        
        self._base_url = f"http://{host}:{port}"
        self._circuit_breaker = circuit_breaker or create_circuit_breaker()
        self._last_status: Optional[VigilStatus] = VigilStatus.DISABLED if not enabled else None
        
        # Statistics
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._total_latency_ms = 0.0
        
        # HTTP client configuration
        self._timeout = httpx.Timeout(
            timeout=timeout_ms / 1000.0,  # Convert to seconds
            connect=min(timeout_ms / 1000.0, 5.0),  # Connect timeout
        )
        
        if enabled:
            logger.info(
                f"🔌 VigilClient initialized: {self._base_url} "
                f"(timeout={timeout_ms}ms, retries={retry_attempts})"
            )
        else:
            logger.info("🔌 VigilClient initialized but DISABLED")
    
    @property
    def status(self) -> VigilStatus:
        """
        Get the status from the most recent operation.
        
        Returns:
            Most recent VigilStatus, or DISABLED if client is disabled
        """
        if not self.enabled:
            return VigilStatus.DISABLED
        if self._last_status is not None:
            return self._last_status
        if self._circuit_breaker.is_open:
            return VigilStatus.CIRCUIT_OPEN
        return VigilStatus.UNAVAILABLE
    
    async def analyze(self, text: str) -> Optional[VigilResult]:
        """
        Analyze text for mental health risk.
        
        Sends the text to Ash-Vigil for specialized risk detection.
        Handles timeouts, network errors, and circuit breaker states gracefully.
        
        Args:
            text: Message text to analyze
            
        Returns:
            VigilResult if successful, None if unavailable
            
        Note:
            Check self.status after a None return to determine the reason
            for failure (timeout, circuit open, network error, etc).
        """
        self._total_requests += 1
        
        # Gate 1: Is client enabled?
        if not self.enabled:
            self._last_status = VigilStatus.DISABLED
            return None
        
        # Gate 2: Is circuit breaker allowing calls?
        if not self._circuit_breaker.should_allow_call():
            self._last_status = VigilStatus.CIRCUIT_OPEN
            self._failed_requests += 1
            logger.debug(f"Vigil call blocked by circuit breaker")
            return None
        
        # Attempt call with retries
        last_error: Optional[Exception] = None
        
        for attempt in range(self.retry_attempts + 1):
            try:
                result = await self._make_request(text)
                
                # Success!
                self._circuit_breaker.record_success()
                self._last_status = VigilStatus.USED
                self._successful_requests += 1
                self._total_latency_ms += result.inference_time_ms
                
                return result
                
            except httpx.TimeoutException as e:
                last_error = e
                self._last_status = VigilStatus.TIMEOUT
                logger.warning(
                    f"Vigil timeout (attempt {attempt + 1}/{self.retry_attempts + 1}): {e}"
                )
                
            except httpx.ConnectError as e:
                last_error = e
                self._last_status = VigilStatus.UNAVAILABLE
                logger.warning(
                    f"Vigil connection error (attempt {attempt + 1}/{self.retry_attempts + 1}): {e}"
                )
                
            except httpx.HTTPStatusError as e:
                last_error = e
                self._last_status = VigilStatus.UNAVAILABLE
                logger.warning(
                    f"Vigil HTTP error {e.response.status_code} "
                    f"(attempt {attempt + 1}/{self.retry_attempts + 1})"
                )
                
            except Exception as e:
                last_error = e
                self._last_status = VigilStatus.UNAVAILABLE
                logger.error(
                    f"Vigil unexpected error (attempt {attempt + 1}/{self.retry_attempts + 1}): {e}"
                )
            
            # Wait before retry (exponential backoff)
            if attempt < self.retry_attempts:
                backoff = 0.1 * (2 ** attempt)  # 100ms, 200ms, 400ms...
                await asyncio.sleep(backoff)
        
        # All attempts failed
        self._circuit_breaker.record_failure()
        self._failed_requests += 1
        
        # Update status based on circuit state after failure
        if self._circuit_breaker.is_open:
            self._last_status = VigilStatus.CIRCUIT_OPEN
        
        logger.warning(
            f"❌ Vigil call failed after {self.retry_attempts + 1} attempts: "
            f"{type(last_error).__name__ if last_error else 'Unknown'}"
        )
        
        return None
    
    async def _make_request(self, text: str) -> VigilResult:
        """
        Make HTTP request to Vigil analyze endpoint.
        
        Args:
            text: Message text to analyze
            
        Returns:
            VigilResult from Vigil response
            
        Raises:
            httpx.TimeoutException: Request timed out
            httpx.ConnectError: Could not connect to Vigil
            httpx.HTTPStatusError: Vigil returned error status
        """
        start_time = time.perf_counter()
        
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/analyze",
                json={"text": text},
                headers={"Content-Type": "application/json"},
            )
            
            # Raise for 4xx/5xx status codes
            response.raise_for_status()
            
            inference_time_ms = (time.perf_counter() - start_time) * 1000
            
            data = response.json()
            
            return VigilResult.from_vigil_response(data, inference_time_ms)
    
    async def health_check(self) -> bool:
        """
        Check if Vigil service is healthy.
        
        Returns:
            True if Vigil is reachable and healthy, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(f"{self._base_url}/health")
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("status") == "healthy"
                    
                return False
                
        except Exception as e:
            logger.debug(f"Vigil health check failed: {e}")
            return False
    
    def get_health(self) -> Dict[str, Any]:
        """
        Get comprehensive client health information.
        
        Returns:
            Dictionary with client configuration and statistics
        """
        avg_latency = (
            self._total_latency_ms / self._successful_requests
            if self._successful_requests > 0
            else 0.0
        )
        
        success_rate = (
            self._successful_requests / self._total_requests
            if self._total_requests > 0
            else 0.0
        )
        
        return {
            "enabled": self.enabled,
            "host": self.host,
            "port": self.port,
            "base_url": self._base_url,
            "timeout_ms": self.timeout_ms,
            "retry_attempts": self.retry_attempts,
            "last_status": self._last_status.value if self._last_status else None,
            "circuit_breaker": self._circuit_breaker.get_health(),
            "statistics": {
                "total_requests": self._total_requests,
                "successful_requests": self._successful_requests,
                "failed_requests": self._failed_requests,
                "success_rate": round(success_rate, 4),
                "average_latency_ms": round(avg_latency, 2),
                "total_latency_ms": round(self._total_latency_ms, 2),
            },
        }
    
    def reset_circuit(self) -> None:
        """
        Manually reset the circuit breaker.
        
        Useful for administrative recovery after fixing Vigil issues.
        """
        self._circuit_breaker.reset()
        self._last_status = None
        logger.info("Vigil client circuit breaker reset")
    
    def reset_statistics(self) -> None:
        """
        Reset client statistics counters.
        
        Useful for monitoring/reporting windows.
        """
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._total_latency_ms = 0.0
        logger.debug("Vigil client statistics reset")


# =============================================================================
# Factory Function - Clean Architecture v5.2.3 Compliance (Rule #1)
# =============================================================================


def create_vigil_client(
    config_manager: Optional["ConfigManager"] = None,
    circuit_breaker: Optional[CircuitBreaker] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    timeout_ms: Optional[int] = None,
    retry_attempts: Optional[int] = None,
    enabled: Optional[bool] = None,
) -> VigilClient:
    """
    Factory function for VigilClient - MANDATORY.
    
    Creates a configured VigilClient instance. Configuration is loaded from
    the config_manager if provided, with explicit parameters taking precedence.
    
    Args:
        config_manager: Configuration manager for loading settings
        circuit_breaker: Pre-configured circuit breaker (creates default if None)
        host: Override Vigil host (default from config or "10.20.30.14")
        port: Override Vigil port (default from config or 30882)
        timeout_ms: Override timeout in ms (default from config or 500)
        retry_attempts: Override retry attempts (default from config or 1)
        enabled: Override enabled flag (default from config or True)
        
    Returns:
        Configured VigilClient instance
        
    Example:
        # From config
        client = create_vigil_client(config_manager=config)
        
        # With overrides
        client = create_vigil_client(
            config_manager=config,
            timeout_ms=1000,  # Override timeout
        )
        
        # Fully manual
        client = create_vigil_client(
            host="10.20.30.14",
            port=30882,
            timeout_ms=500,
        )
    """
    # Default values
    defaults = {
        "host": "10.20.30.14",
        "port": 30882,
        "timeout_ms": 500,
        "retry_attempts": 1,
        "enabled": True,
        "circuit_breaker": {
            "failure_threshold": 3,
            "recovery_timeout_seconds": 30,
        },
    }
    
    # Load from config manager if provided
    vigil_config: Dict[str, Any] = {}
    if config_manager is not None:
        try:
            # Use get_section() to get the entire vigil config section
            vigil_config = config_manager.get_section("vigil") or {}
            config_defaults = vigil_config.get("defaults", {})
            
            # Merge config defaults
            for key in ["host", "port", "timeout_ms", "retry_attempts", "enabled"]:
                if key in vigil_config:
                    defaults[key] = vigil_config[key]
                elif key in config_defaults:
                    defaults[key] = config_defaults[key]
            
            # Circuit breaker config
            cb_config = vigil_config.get("circuit_breaker", {})
            cb_defaults = config_defaults.get("circuit_breaker", {})
            
            if "failure_threshold" in cb_config:
                defaults["circuit_breaker"]["failure_threshold"] = cb_config["failure_threshold"]
            elif "failure_threshold" in cb_defaults:
                defaults["circuit_breaker"]["failure_threshold"] = cb_defaults["failure_threshold"]
            
            if "recovery_timeout_seconds" in cb_config:
                defaults["circuit_breaker"]["recovery_timeout_seconds"] = cb_config["recovery_timeout_seconds"]
            elif "recovery_timeout_seconds" in cb_defaults:
                defaults["circuit_breaker"]["recovery_timeout_seconds"] = cb_defaults["recovery_timeout_seconds"]
                
        except Exception as e:
            logger.warning(f"Error loading Vigil config, using defaults: {e}")
    
    # Apply explicit overrides
    final_host = host if host is not None else defaults["host"]
    final_port = port if port is not None else defaults["port"]
    final_timeout = timeout_ms if timeout_ms is not None else defaults["timeout_ms"]
    final_retries = retry_attempts if retry_attempts is not None else defaults["retry_attempts"]
    final_enabled = enabled if enabled is not None else defaults["enabled"]
    
    # Create circuit breaker if not provided
    if circuit_breaker is None:
        circuit_breaker = create_circuit_breaker(
            failure_threshold=defaults["circuit_breaker"]["failure_threshold"],
            recovery_timeout_seconds=defaults["circuit_breaker"]["recovery_timeout_seconds"],
        )
    
    return VigilClient(
        host=final_host,
        port=final_port,
        timeout_ms=final_timeout,
        retry_attempts=final_retries,
        circuit_breaker=circuit_breaker,
        enabled=final_enabled,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "VigilStatus",
    "CircuitState",
    
    # Data classes
    "VigilResult",
    
    # Classes
    "CircuitBreaker",
    "VigilClient",
    
    # Factory functions
    "create_vigil_client",
    "create_circuit_breaker",
]
