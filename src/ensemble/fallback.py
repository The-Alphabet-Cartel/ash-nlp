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
Fallback Strategy for Ash-NLP Ensemble Service
---
FILE VERSION: v5.0-3-4.3-3
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.3 - Ensemble Error Handling
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Handle model failures gracefully
- Redistribute weights when models fail
- Implement circuit breaker pattern
- Ensure operational continuity (Rule #5)
- Alert on critical model failures

DESIGN PHILOSOPHY (Rule #5 - Production Resilience):
This system serves LIFE-SAVING crisis detection. Therefore:
- System availability is paramount
- Graceful degradation over system crash
- Continue with reduced accuracy rather than fail completely
- Comprehensive logging for post-incident analysis
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

# Module version
__version__ = "v5.0-3-4.3-3"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Exceptions
# =============================================================================


class CriticalModelFailure(Exception):
    """
    Exception raised when the primary (BART) model fails.

    This is a critical error because BART is essential for
    crisis detection. The system may need to alert operators.
    """

    pass


class EnsembleDegradedError(Exception):
    """
    Exception raised when ensemble is too degraded to function.

    This occurs when multiple models fail and accuracy would
    be too low for safe operation.
    """

    pass


# =============================================================================
# Circuit Breaker States
# =============================================================================


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, skip calls
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class CircuitBreaker:
    """
    Circuit breaker for individual models.

    Prevents repeated calls to failing models,
    allowing time for recovery.

    Attributes:
        model_name: Name of the model
        failure_threshold: Failures before opening
        recovery_timeout: Seconds before trying again
        state: Current circuit state
        failure_count: Consecutive failures
        last_failure_time: Time of last failure
    """

    model_name: str
    failure_threshold: int = 3
    recovery_timeout: float = 60.0
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: float = 0.0
    success_count: int = 0

    def record_success(self) -> None:
        """Record successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 2:  # Two successes to close
                self._close()
        else:
            self.failure_count = 0
            self.success_count = 0

    def record_failure(self) -> None:
        """Record failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0

        if self.failure_count >= self.failure_threshold:
            self._open()

    def can_call(self) -> bool:
        """Check if model can be called."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if recovery timeout elapsed
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.recovery_timeout:
                self._half_open()
                return True
            return False

        # HALF_OPEN - allow call for testing
        return True

    def _open(self) -> None:
        """Open the circuit (stop calling)."""
        self.state = CircuitState.OPEN
        logger.warning(
            f"🔴 Circuit OPEN for {self.model_name} ({self.failure_count} failures)"
        )

    def _half_open(self) -> None:
        """Half-open the circuit (test recovery)."""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        logger.info(f"🟡 Circuit HALF_OPEN for {self.model_name} (testing)")

    def _close(self) -> None:
        """Close the circuit (normal operation)."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        logger.info(f"🟢 Circuit CLOSED for {self.model_name} (recovered)")

    def reset(self) -> None:
        """Reset circuit to initial state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0


# =============================================================================
# Fallback Strategy
# =============================================================================


@dataclass
class ModelFailureInfo:
    """Information about a model failure."""

    model_name: str
    error: str
    timestamp: float
    is_critical: bool
    weight_lost: float


class FallbackStrategy:
    """
    Fallback Strategy for Ensemble Resilience.

    Handles model failures gracefully:
    - Redistributes weights when models fail
    - Tracks failures with circuit breakers
    - Alerts on critical (BART) failures
    - Maintains operational continuity

    Design Philosophy:
    - BART failure is CRITICAL (raises exception)
    - Secondary model failures trigger weight redistribution
    - System continues with degraded accuracy
    - All failures logged for analysis

    Clean Architecture v5.1 Compliance:
    - Factory function: create_fallback_strategy()
    - Resilient error handling (Rule #5)
    """

    # Primary model (failure is critical)
    PRIMARY_MODEL = "bart"

    # Models that contribute to scoring
    SCORING_MODELS = {"bart", "sentiment", "emotions"}

    # Minimum models required for safe operation
    MIN_MODELS_REQUIRED = 1  # At minimum, BART must work

    def __init__(
        self,
        base_weights: Dict[str, float],
        failure_threshold: int = 3,
        recovery_timeout: float = 60.0,
    ):
        """
        Initialize FallbackStrategy.

        Args:
            base_weights: Original model weights
            failure_threshold: Failures before circuit opens
            recovery_timeout: Seconds before retrying failed model
        """
        self.base_weights = base_weights.copy()
        self.current_weights = base_weights.copy()
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        # Circuit breakers for each model
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            name: CircuitBreaker(
                model_name=name,
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
            )
            for name in base_weights.keys()
        }

        # Track failed models
        self.failed_models: Set[str] = set()
        self.failure_history: List[ModelFailureInfo] = []

        # Degradation tracking
        self._is_degraded: bool = False
        self._degradation_reason: str = ""

        logger.info(
            f"🛡️ FallbackStrategy initialized "
            f"(threshold={failure_threshold}, timeout={recovery_timeout}s)"
        )

    # =========================================================================
    # Failure Handling
    # =========================================================================

    def handle_model_failure(
        self,
        model_name: str,
        error: str,
    ) -> Dict[str, float]:
        """
        Handle a model failure.

        Args:
            model_name: Name of failed model
            error: Error message

        Returns:
            Updated weights after redistribution

        Raises:
            CriticalModelFailure: If BART (primary) fails
        """
        is_critical = model_name == self.PRIMARY_MODEL
        weight_lost = self.current_weights.get(model_name, 0.0)

        # Record failure info
        failure_info = ModelFailureInfo(
            model_name=model_name,
            error=error,
            timestamp=time.time(),
            is_critical=is_critical,
            weight_lost=weight_lost,
        )
        self.failure_history.append(failure_info)

        # Update circuit breaker
        if model_name in self.circuit_breakers:
            self.circuit_breakers[model_name].record_failure()

        # Log the failure
        if is_critical:
            logger.critical(
                f"🚨 CRITICAL: Primary model '{model_name}' failed: {error}"
            )
        else:
            logger.error(f"❌ Model '{model_name}' failed: {error}")

        # Check if primary model failed
        if is_critical:
            raise CriticalModelFailure(
                f"Primary model ({model_name}) unavailable: {error}"
            )

        # Mark as failed and redistribute weights
        self.failed_models.add(model_name)
        self._redistribute_weights(model_name)

        return self.current_weights.copy()

    def handle_model_success(self, model_name: str) -> None:
        """
        Handle a model success (for circuit breaker).

        Args:
            model_name: Name of successful model
        """
        if model_name in self.circuit_breakers:
            self.circuit_breakers[model_name].record_success()

        # If model was failed, check if it recovered
        if model_name in self.failed_models:
            cb = self.circuit_breakers.get(model_name)
            if cb and cb.state == CircuitState.CLOSED:
                self._recover_model(model_name)

    def _redistribute_weights(self, failed_model: str) -> None:
        """
        Redistribute weight from failed model to remaining models.

        Args:
            failed_model: Name of failed model
        """
        if failed_model not in self.current_weights:
            return

        lost_weight = self.current_weights[failed_model]
        self.current_weights[failed_model] = 0.0

        # Get active models that can receive weight
        active_models = [
            name
            for name in self.SCORING_MODELS
            if name != failed_model and name not in self.failed_models
        ]

        if not active_models:
            self._is_degraded = True
            self._degradation_reason = "No active scoring models"
            logger.warning("⚠️ No active models to redistribute weight to")
            return

        # Redistribute proportionally
        redistribution = lost_weight / len(active_models)

        for model in active_models:
            self.current_weights[model] += redistribution

        self._is_degraded = True
        self._degradation_reason = f"Model '{failed_model}' unavailable"

        logger.info(
            f"⚖️ Redistributed {lost_weight:.2f} weight from {failed_model} "
            f"to {active_models}"
        )
        logger.info(f"New weights: {self.current_weights}")

    def _recover_model(self, model_name: str) -> None:
        """
        Handle model recovery.

        Args:
            model_name: Name of recovered model
        """
        if model_name not in self.failed_models:
            return

        self.failed_models.remove(model_name)

        # Restore original weights
        self._restore_weights()

        logger.info(f"✅ Model '{model_name}' recovered")

        # Check if no longer degraded
        if not self.failed_models:
            self._is_degraded = False
            self._degradation_reason = ""

    def _restore_weights(self) -> None:
        """Restore weights accounting for currently failed models."""
        # Start with base weights
        self.current_weights = self.base_weights.copy()

        # Zero out failed models and redistribute
        for failed in self.failed_models:
            if failed in self.current_weights:
                lost_weight = self.current_weights[failed]
                self.current_weights[failed] = 0.0

                # Redistribute to active models
                active = [n for n in self.SCORING_MODELS if n not in self.failed_models]
                if active:
                    redistribution = lost_weight / len(active)
                    for model in active:
                        self.current_weights[model] += redistribution

    # =========================================================================
    # Circuit Breaker Checks
    # =========================================================================

    def can_call_model(self, model_name: str) -> bool:
        """
        Check if model can be called (circuit breaker check).

        Args:
            model_name: Name of model to check

        Returns:
            True if model should be called
        """
        cb = self.circuit_breakers.get(model_name)
        if cb is None:
            return True
        return cb.can_call()

    def get_callable_models(self) -> List[str]:
        """
        Get list of models that can be called.

        Returns:
            List of model names with closed/half-open circuits
        """
        return [name for name, cb in self.circuit_breakers.items() if cb.can_call()]

    # =========================================================================
    # Status and Info
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive fallback status.

        Returns:
            Status dictionary
        """
        circuit_status = {
            name: {
                "state": cb.state.value,
                "failure_count": cb.failure_count,
                "can_call": cb.can_call(),
            }
            for name, cb in self.circuit_breakers.items()
        }

        return {
            "is_degraded": self._is_degraded,
            "degradation_reason": self._degradation_reason,
            "failed_models": list(self.failed_models),
            "base_weights": self.base_weights,
            "current_weights": self.current_weights,
            "circuit_breakers": circuit_status,
            "total_failures": len(self.failure_history),
            "recent_failures": [
                {
                    "model": f.model_name,
                    "error": f.error,
                    "critical": f.is_critical,
                }
                for f in self.failure_history[-5:]  # Last 5 failures
            ],
        }

    def get_current_weights(self) -> Dict[str, float]:
        """Get current adjusted weights."""
        return self.current_weights.copy()

    def is_degraded(self) -> bool:
        """Check if ensemble is in degraded state."""
        return self._is_degraded

    def get_degradation_reason(self) -> str:
        """Get reason for degradation."""
        return self._degradation_reason

    def is_operational(self) -> bool:
        """
        Check if ensemble is operational.

        At minimum, BART must be available.

        Returns:
            True if system can process requests
        """
        return self.PRIMARY_MODEL not in self.failed_models

    # =========================================================================
    # Reset and Recovery
    # =========================================================================

    def reset(self) -> None:
        """Reset all state to initial."""
        self.current_weights = self.base_weights.copy()
        self.failed_models.clear()
        self.failure_history.clear()
        self._is_degraded = False
        self._degradation_reason = ""

        for cb in self.circuit_breakers.values():
            cb.reset()

        logger.info("🔄 FallbackStrategy reset to initial state")

    def clear_failure_history(self) -> None:
        """Clear failure history (keep other state)."""
        self.failure_history.clear()
        logger.info("📋 Failure history cleared")


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_fallback_strategy(
    base_weights: Optional[Dict[str, float]] = None,
    config_manager: Optional[Any] = None,
    failure_threshold: int = 3,
    recovery_timeout: float = 60.0,
) -> FallbackStrategy:
    """
    Factory function for FallbackStrategy.

    Creates a configured fallback strategy.

    Args:
        base_weights: Model weights (optional, loaded from config)
        config_manager: Configuration manager instance
        failure_threshold: Failures before circuit opens
        recovery_timeout: Seconds before retrying failed model

    Returns:
        Configured FallbackStrategy instance

    Example:
        >>> fallback = create_fallback_strategy(config_manager=config)
        >>> try:
        ...     result = model.analyze(text)
        ...     fallback.handle_model_success("bart")
        ... except Exception as e:
        ...     fallback.handle_model_failure("bart", str(e))
    """
    # Get weights from config or use defaults
    if base_weights is None:
        if config_manager is not None:
            base_weights = config_manager.get_model_weights()

        if not base_weights:
            base_weights = {
                "bart": 0.50,
                "sentiment": 0.25,
                "irony": 0.15,
                "emotions": 0.10,
            }

    return FallbackStrategy(
        base_weights=base_weights,
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "FallbackStrategy",
    "create_fallback_strategy",
    "CircuitBreaker",
    "CircuitState",
    "ModelFailureInfo",
    "CriticalModelFailure",
    "EnsembleDegradedError",
]
