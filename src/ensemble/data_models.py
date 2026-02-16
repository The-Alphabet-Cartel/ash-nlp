"""
============================================================================
Ash-NLP: Crisis Detection NLP Server
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Analyze  → Process messages through multi-model ensemble classification
    Detect   → Identify crisis signals with weighted consensus algorithms
    Explain  → Provide human-readable explanations for all decisions
    Protect  → Safeguard our LGBTQIA+ community through accurate detection

============================================================================
Data Models for Ensemble Decision Engine

Shared dataclasses and result types used across the ensemble pipeline:
- WarmupResult: Engine warmup tracking (FE-004)
- VigilResponse: Vigil integration response details
- CrisisAssessment: Primary analysis output
- RecommendedAction: Severity-to-action mapping
- IronyGateResult: Irony gatekeeper result
- IronyGate: Irony gatekeeper implementation + factory
----------------------------------------------------------------------------
FILE VERSION: v5.1-6-6.4.3-1
LAST MODIFIED: 2026-02-15
PHASE: Phase 6 - Step 6.4.3 Decision Engine Decomposition
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from src.clients.vigil_client import VigilStatus

from .scoring import CrisisSeverity, ModelSignal
from .aggregator import AggregatedResult

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager
    from src.context import ContextAnalysisResult

# Module version
__version__ = "v5.1-6-6.4.3-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# FE-004: Warmup Result Dataclass
# =============================================================================


@dataclass
class WarmupResult:
    """
    Result of engine warmup operation (FE-004).

    Tracks warmup success, timing, and per-model latencies.

    Attributes:
        success: Whether warmup completed successfully
        total_latency_ms: Total warmup time in milliseconds
        per_model_latency_ms: Per-model latency breakdown
        models_warmed: List of models that were warmed up
        error: Error message if warmup failed
        timestamp: When warmup was performed
    """

    success: bool
    total_latency_ms: float
    per_model_latency_ms: Dict[str, float] = field(default_factory=dict)
    models_warmed: List[str] = field(default_factory=list)
    error: Optional[str] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "total_latency_ms": round(self.total_latency_ms, 2),
            "per_model_latency_ms": {
                k: round(v, 2) for k, v in self.per_model_latency_ms.items()
            },
            "models_warmed": self.models_warmed,
            "error": self.error,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


# =============================================================================
# Phase 3 Vigil: Vigil Response Dataclass
# =============================================================================


@dataclass
class VigilResponse:
    """
    Vigil integration details in analysis response.

    Tracks what happened with Vigil for each analysis request.

    Attributes:
        status: Vigil call status (used, skipped, unavailable, etc.)
        risk_score: Risk score from Vigil if available (0.0-1.0)
        risk_label: Risk classification label from Vigil if available
        amplification_applied: Whether Vigil amplification was applied
        base_score: Pre-amplification base score (for debugging)
        amplified_score: Post-amplification score before irony dampening
    """

    status: VigilStatus
    risk_score: Optional[float] = None
    risk_label: Optional[str] = None
    amplification_applied: bool = False
    base_score: Optional[float] = None
    amplified_score: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        result = {
            "status": self.status.value,
            "amplification_applied": self.amplification_applied,
        }

        if self.risk_score is not None:
            result["risk_score"] = round(self.risk_score, 4)
        if self.risk_label is not None:
            result["risk_label"] = self.risk_label
        if self.base_score is not None:
            result["base_score"] = round(self.base_score, 4)
        if self.amplified_score is not None:
            result["amplified_score"] = round(self.amplified_score, 4)

        return result


# =============================================================================
# Phase 6: Irony Gatekeeper Result
# =============================================================================


@dataclass
class IronyGateResult:
    """
    Result of irony gatekeeper application.

    Attributes:
        triggered: Whether the gate fired (irony confidence >= threshold)
        original_score: Score before gate application
        gated_score: Score after gate application
        irony_confidence: Irony model confidence (0.0-1.0)
        threshold: Threshold that was used
        reduction_factor: Reduction factor that was applied
    """

    triggered: bool
    original_score: float
    gated_score: float
    irony_confidence: float
    threshold: float
    reduction_factor: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "triggered": self.triggered,
            "original_score": round(self.original_score, 4),
            "gated_score": round(self.gated_score, 4),
            "irony_confidence": round(self.irony_confidence, 4),
            "threshold": self.threshold,
            "reduction_factor": self.reduction_factor,
        }


# =============================================================================
# Crisis Assessment Result (Phase 3 Vigil Enhanced)
# =============================================================================


@dataclass
class CrisisAssessment:
    """
    Complete crisis assessment result.

    This is the primary output from the Decision Engine,
    containing all information needed for API response.

    Attributes:
        crisis_detected: Whether a crisis was detected
        severity: Crisis severity level
        confidence: Confidence in assessment (0.0 - 1.0)
        crisis_score: Final weighted crisis score (0.0 - 1.0)
        requires_intervention: Whether immediate action is recommended
        recommended_action: Suggested response action
        signals: Individual model signals
        processing_time_ms: Total processing time
        models_used: Which models contributed
        is_degraded: Whether ensemble is operating in degraded mode
        message: Original message analyzed
        cached: Whether result was from cache

        # Phase 3 Vigil Fields
        vigil: Vigil integration details
        requires_review: True if CRT review recommended

        # Phase 4 Enhanced Fields
        explanation: Human-readable explanation (Phase 4)
        conflict_report: Conflict detection report (Phase 4)
        consensus_result: Consensus algorithm result (Phase 4)
        aggregated_result: Full aggregated result (Phase 4)

        # Phase 5 Enhanced Fields
        context_analysis: Context history analysis result (Phase 5)

        # Phase 6 Enhanced Fields
        irony_gate_result: Irony gatekeeper result (Phase 6)
    """

    crisis_detected: bool
    severity: CrisisSeverity
    confidence: float
    crisis_score: float
    requires_intervention: bool
    recommended_action: str
    signals: Dict[str, Any]
    processing_time_ms: float
    models_used: List[str]
    is_degraded: bool = False
    degradation_reason: str = ""
    message: str = ""
    cached: bool = False

    # Phase 3 Vigil Fields
    vigil: Optional[VigilResponse] = None
    requires_review: bool = False

    # Phase 4 Enhanced Fields
    explanation: Optional[Dict[str, Any]] = None
    conflict_report: Optional[Dict[str, Any]] = None
    consensus_result: Optional[Dict[str, Any]] = None
    aggregated_result: Optional[AggregatedResult] = None

    # Phase 5 Enhanced Fields
    context_analysis: Optional["ContextAnalysisResult"] = None

    # Phase 6 Enhanced Fields
    irony_gate_result: Optional[IronyGateResult] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        result = {
            "crisis_detected": self.crisis_detected,
            "severity": self.severity.value,
            "confidence": round(self.confidence, 4),
            "crisis_score": round(self.crisis_score, 4),
            "requires_intervention": self.requires_intervention,
            "requires_review": self.requires_review,
            "recommended_action": self.recommended_action,
            "signals": self.signals,
            "processing_time_ms": round(self.processing_time_ms, 2),
            "models_used": self.models_used,
            "is_degraded": self.is_degraded,
            "cached": self.cached,
        }

        # Include Phase 3 Vigil fields
        if self.vigil:
            result["vigil"] = self.vigil.to_dict()

        # Include Phase 4 fields if present
        if self.explanation:
            result["explanation"] = self.explanation
        if self.conflict_report:
            result["conflict_analysis"] = self.conflict_report
        if self.consensus_result:
            result["consensus"] = self.consensus_result

        # Include Phase 5 fields if present
        if self.context_analysis:
            result["context_analysis"] = self.context_analysis.to_dict()

        # Include Phase 6 fields if present
        if self.irony_gate_result:
            result["irony_gate"] = self.irony_gate_result.to_dict()

        return result

    def to_enhanced_dict(self) -> Dict[str, Any]:
        """Convert to full enhanced dictionary with all Phase 4 data.

        v5.1-6-6.4-2: Always use to_dict() as the base response. The
        aggregated_result is included as a nested field by to_dict() but
        no longer overrides the top-level crisis_score/severity, which
        must come from the ensemble → Vigil → irony gate pipeline.
        """
        return self.to_dict()

    @staticmethod
    def create_error(
        error: str,
        message: str = "",
        processing_time_ms: float = 0.0,
    ) -> "CrisisAssessment":
        """Create an error assessment."""
        return CrisisAssessment(
            crisis_detected=False,
            severity=CrisisSeverity.SAFE,
            confidence=0.0,
            crisis_score=0.0,
            requires_intervention=False,
            requires_review=False,
            recommended_action="error",
            signals={"error": error},
            processing_time_ms=processing_time_ms,
            models_used=[],
            is_degraded=True,
            degradation_reason=error,
            message=message,
            vigil=VigilResponse(status=VigilStatus.DISABLED),
        )


# =============================================================================
# Recommended Actions
# =============================================================================


class RecommendedAction:
    """Recommended actions based on severity."""

    IMMEDIATE_OUTREACH = "immediate_outreach"
    PRIORITY_RESPONSE = "priority_response"
    STANDARD_MONITORING = "standard_monitoring"
    PASSIVE_MONITORING = "passive_monitoring"
    NONE = "none"
    ERROR = "error"

    @classmethod
    def from_severity(cls, severity: CrisisSeverity) -> str:
        """Map severity to recommended action."""
        mapping = {
            CrisisSeverity.CRITICAL: cls.IMMEDIATE_OUTREACH,
            CrisisSeverity.HIGH: cls.PRIORITY_RESPONSE,
            CrisisSeverity.MEDIUM: cls.STANDARD_MONITORING,
            CrisisSeverity.LOW: cls.PASSIVE_MONITORING,
            CrisisSeverity.SAFE: cls.NONE,
        }
        return mapping.get(severity, cls.NONE)


# =============================================================================
# Phase 6: Irony Gatekeeper
# =============================================================================


class IronyGate:
    """
    Irony Gatekeeper - Post-Scoring Score Reducer.

    Phase 6 refactor: Replaces the v5.0 irony dampening (continuous
    multiplicative factor) with a threshold-gated reducer.

    Key behavioral differences from v5.0:
    - Only fires when irony confidence EXCEEDS a configurable threshold
    - When NOT triggered: ZERO effect on scoring (true pass-through)
    - When triggered: score multiplied by configurable reduction_factor
    - Applied AFTER Vigil amplification, BEFORE final severity mapping

    This fixes the critical v5.0 issue where genuine crisis statements
    (e.g., "I want to jump off this bridge") were being dampened by
    low-confidence irony scores (e.g., irony=0.15 → dampening=0.865),
    pulling them below the HIGH severity threshold.

    Configuration: classification_config.json → irony_gate section
    Environment: NLP_IRONY_GATE_ENABLED, NLP_IRONY_GATE_THRESHOLD,
                 NLP_IRONY_GATE_REDUCTION

    Clean Architecture v5.2.3 Compliance:
    - Factory function: create_irony_gate()
    - Configuration via ConfigManager
    - Resilient error handling (Rule #5)
    """

    DEFAULT_THRESHOLD = 0.80
    DEFAULT_REDUCTION_FACTOR = 0.70

    def __init__(
        self,
        enabled: bool = True,
        threshold: float = 0.80,
        reduction_factor: float = 0.70,
    ):
        """
        Initialize IronyGate.

        Args:
            enabled: Whether the gate is active
            threshold: Irony confidence threshold to trigger (0.0-1.0)
            reduction_factor: Score multiplier when triggered (0.0-1.0)
        """
        self.enabled = enabled
        self.threshold = max(0.0, min(1.0, threshold))
        self.reduction_factor = max(0.1, min(1.0, reduction_factor))

        logger.info(
            f"🚪 IronyGate initialized "
            f"(enabled={enabled}, threshold={self.threshold}, "
            f"reduction_factor={self.reduction_factor})"
        )

    def apply(
        self,
        score: float,
        irony_signal: Optional[ModelSignal] = None,
    ) -> IronyGateResult:
        """
        Apply irony gatekeeper to a crisis score.

        Args:
            score: Pre-gate crisis score (after Vigil amplification)
            irony_signal: ModelSignal from irony detector (from scorer)

        Returns:
            IronyGateResult with gated score and metadata
        """
        # Gate disabled - pass through
        if not self.enabled:
            return IronyGateResult(
                triggered=False,
                original_score=score,
                gated_score=score,
                irony_confidence=0.0,
                threshold=self.threshold,
                reduction_factor=self.reduction_factor,
            )

        # No irony signal available - pass through
        if irony_signal is None:
            return IronyGateResult(
                triggered=False,
                original_score=score,
                gated_score=score,
                irony_confidence=0.0,
                threshold=self.threshold,
                reduction_factor=self.reduction_factor,
            )

        # Extract irony confidence from the signal metadata
        irony_confidence = irony_signal.metadata.get("irony_score", 0.0)

        # Gate check: does irony confidence meet or exceed threshold?
        if irony_confidence >= self.threshold:
            # Triggered: reduce score
            gated_score = score * self.reduction_factor
            gated_score = max(0.0, min(1.0, gated_score))

            logger.info(
                f"🚪 IronyGate TRIGGERED: score {score:.3f} → {gated_score:.3f} "
                f"(irony={irony_confidence:.3f} >= threshold={self.threshold})"
            )

            return IronyGateResult(
                triggered=True,
                original_score=score,
                gated_score=gated_score,
                irony_confidence=irony_confidence,
                threshold=self.threshold,
                reduction_factor=self.reduction_factor,
            )
        else:
            # Not triggered: pass through unchanged
            logger.debug(
                f"🚪 IronyGate pass-through: irony={irony_confidence:.3f} "
                f"< threshold={self.threshold}"
            )

            return IronyGateResult(
                triggered=False,
                original_score=score,
                gated_score=score,
                irony_confidence=irony_confidence,
                threshold=self.threshold,
                reduction_factor=self.reduction_factor,
            )


def create_irony_gate(
    config_manager: Optional["ConfigManager"] = None,
    enabled: Optional[bool] = None,
    threshold: Optional[float] = None,
    reduction_factor: Optional[float] = None,
) -> IronyGate:
    """
    Factory function for IronyGate.

    Creates a configured IronyGate using ConfigManager settings.

    Args:
        config_manager: Configuration manager instance
        enabled: Override enabled flag (optional)
        threshold: Override threshold (optional)
        reduction_factor: Override reduction factor (optional)

    Returns:
        Configured IronyGate instance

    Example:
        >>> gate = create_irony_gate(config_manager=config)
        >>> result = gate.apply(score=0.75, irony_signal=irony_signal)
    """
    gate_enabled = True
    gate_threshold = IronyGate.DEFAULT_THRESHOLD
    gate_reduction = IronyGate.DEFAULT_REDUCTION_FACTOR

    # Load from config manager
    if config_manager is not None:
        try:
            gate_config = config_manager.get_irony_gate_config()
            if gate_config:
                gate_enabled = bool(gate_config.get("enabled", True))
                gate_threshold = float(
                    gate_config.get("confidence_threshold", IronyGate.DEFAULT_THRESHOLD)
                )
                gate_reduction = float(
                    gate_config.get("reduction_factor", IronyGate.DEFAULT_REDUCTION_FACTOR)
                )
        except Exception as e:
            logger.warning(f"⚠️ Error loading irony gate config, using defaults: {e}")

    # Apply explicit overrides
    if enabled is not None:
        gate_enabled = enabled
    if threshold is not None:
        gate_threshold = threshold
    if reduction_factor is not None:
        gate_reduction = reduction_factor

    return IronyGate(
        enabled=gate_enabled,
        threshold=gate_threshold,
        reduction_factor=gate_reduction,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "WarmupResult",
    "VigilResponse",
    "CrisisAssessment",
    "RecommendedAction",
    "IronyGateResult",
    "IronyGate",
    "create_irony_gate",
]
