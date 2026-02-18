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
- FigurativeGateResult: Figurative language gate result (Phase 7)
- FigurativeGate: Figurative language gate implementation + factory (Phase 7)
----------------------------------------------------------------------------
FILE VERSION: v5.1-7-7.3-1
LAST MODIFIED: 2026-02-18
PHASE: Phase 7 - Step 7.3 Figurative Language Gate
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from src.clients.vigil_client import VigilStatus

from .scoring import CrisisSeverity
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
# Phase 7: Figurative Language Gate Result
# =============================================================================


@dataclass
class FigurativeGateResult:
    """
    Result of figurative language gate application.

    Phase 7: Replaces IronyGateResult. Contains richer metadata about
    what type of figurative language was detected and the gate decision.

    Attributes:
        triggered: Whether the gate fired (figurative confidence >= threshold)
        skipped: Whether the gate was skipped (score below skip_below)
        original_score: Score before gate application
        gated_score: Score after gate application
        figurative_confidence: Combined figurative confidence (1.0 - literal) (0.0-1.0)
        top_figurative_label: Highest-scoring figurative label (or None if literal)
        top_figurative_score: Score of the top figurative label
        literal_confidence: Confidence in literal classification
        threshold: Threshold that was used
        reduction_factor: Reduction factor that was applied
    """

    triggered: bool
    skipped: bool
    original_score: float
    gated_score: float
    figurative_confidence: float
    top_figurative_label: Optional[str]
    top_figurative_score: float
    literal_confidence: float
    threshold: float
    reduction_factor: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        result = {
            "triggered": self.triggered,
            "skipped": self.skipped,
            "original_score": round(self.original_score, 4),
            "gated_score": round(self.gated_score, 4),
            "figurative_confidence": round(self.figurative_confidence, 4),
            "literal_confidence": round(self.literal_confidence, 4),
            "threshold": self.threshold,
            "reduction_factor": self.reduction_factor,
        }
        if self.top_figurative_label:
            result["top_figurative_label"] = self.top_figurative_label
            result["top_figurative_score"] = round(self.top_figurative_score, 4)
        return result


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

        # Phase 7 Enhanced Fields
        figurative_gate_result: Figurative language gate result (Phase 7)
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

    # Phase 7 Enhanced Fields (replaces Phase 6 irony_gate_result)
    figurative_gate_result: Optional[FigurativeGateResult] = None

    # Step 6.4.3 Enhanced Fields
    consensus_escalation_result: Optional[Any] = None  # ConsensusEscalationResult

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

        # Include Phase 7 fields if present
        if self.figurative_gate_result:
            result["figurative_gate"] = self.figurative_gate_result.to_dict()

        # Include Step 6.4.3 fields if present
        if self.consensus_escalation_result:
            result["consensus_escalation"] = self.consensus_escalation_result.to_dict()

        return result

    def to_enhanced_dict(self) -> Dict[str, Any]:
        """Convert to full enhanced dictionary with all Phase 4+ data.

        v5.1-7-7.3: Always use to_dict() as the base response. The
        aggregated_result is included as a nested field by to_dict() but
        no longer overrides the top-level crisis_score/severity, which
        must come from the ensemble → Vigil → figurative gate pipeline.
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
# Phase 7: Figurative Language Gate
# =============================================================================


class FigurativeGate:
    """
    Figurative Language Gate - Post-Scoring Score Reducer.

    Phase 7: Replaces the Phase 6 IronyGate with a broader figurative
    language gate that uses zero-shot classification to detect non-literal
    speech patterns (hyperbole, sarcasm, irony, gaming death metaphors).

    Key behavioral differences from Phase 6 IronyGate:
    - Uses DeBERTa zero-shot classification instead of Cardiff binary irony
    - Detects multiple figurative language types, not just irony
    - Runs the figurative classifier directly (not a pre-computed signal)
    - Includes skip_below threshold to avoid running on low-scoring messages
    - When NOT triggered: ZERO effect on scoring (true pass-through)
    - When triggered: score multiplied by configurable reduction_factor
    - Applied AFTER Vigil amplification, BEFORE final severity mapping

    Configuration: classification_config.json → figurative_gate section
    Environment: NLP_FIGURATIVE_GATE_ENABLED, NLP_FIGURATIVE_GATE_THRESHOLD,
                 NLP_FIGURATIVE_GATE_REDUCTION, NLP_FIGURATIVE_GATE_SKIP_BELOW

    Clean Architecture v5.2.3 Compliance:
    - Factory function: create_figurative_gate()
    - Configuration via ConfigManager
    - Resilient error handling (Rule #5)
    """

    DEFAULT_THRESHOLD = 0.75
    DEFAULT_REDUCTION_FACTOR = 0.60
    DEFAULT_SKIP_BELOW = 0.30

    def __init__(
        self,
        enabled: bool = True,
        threshold: float = DEFAULT_THRESHOLD,
        reduction_factor: float = DEFAULT_REDUCTION_FACTOR,
        skip_below: float = DEFAULT_SKIP_BELOW,
    ):
        self.enabled = enabled
        self.threshold = max(0.0, min(1.0, threshold))
        self.reduction_factor = max(0.1, min(1.0, reduction_factor))
        self.skip_below = max(0.0, min(1.0, skip_below))

        logger.info(
            f"🎭 FigurativeGate initialized "
            f"(enabled={enabled}, threshold={self.threshold}, "
            f"reduction={self.reduction_factor}, skip_below={self.skip_below})"
        )

    def apply(
        self,
        score: float,
        figurative_result: Optional[Any] = None,
    ) -> FigurativeGateResult:
        """
        Apply figurative language gate to a crisis score.

        Args:
            score: Pre-gate crisis score (after Vigil amplification)
            figurative_result: ModelResult from FigurativeLanguageClassifier

        Returns:
            FigurativeGateResult with gated score and metadata
        """
        _pass_through = FigurativeGateResult(
            triggered=False,
            skipped=False,
            original_score=score,
            gated_score=score,
            figurative_confidence=0.0,
            top_figurative_label=None,
            top_figurative_score=0.0,
            literal_confidence=1.0,
            threshold=self.threshold,
            reduction_factor=self.reduction_factor,
        )

        # Gate disabled — pass through
        if not self.enabled:
            _pass_through.skipped = True
            return _pass_through

        # Score below skip threshold — don't waste inference
        if score < self.skip_below:
            _pass_through.skipped = True
            logger.debug(
                f"🎭 FigurativeGate skipped: score {score:.3f} "
                f"< skip_below {self.skip_below}"
            )
            return _pass_through

        # No figurative result available — pass through
        if figurative_result is None or not figurative_result.success:
            logger.debug("🎭 FigurativeGate pass-through: no figurative result")
            return _pass_through

        # Extract figurative metadata from the classifier result
        metadata = figurative_result.metadata or {}
        figurative_confidence = metadata.get("figurative_confidence", 0.0)
        literal_confidence = metadata.get("literal_confidence", 1.0)
        top_figurative_label = metadata.get("top_figurative_label")
        top_figurative_score = metadata.get("top_figurative_score", 0.0)

        # Gate check: does figurative confidence meet or exceed threshold?
        if figurative_confidence >= self.threshold:
            # Triggered: reduce score
            gated_score = score * self.reduction_factor
            gated_score = max(0.0, min(1.0, gated_score))

            logger.info(
                f"🎭 FigurativeGate TRIGGERED: score {score:.3f} → {gated_score:.3f} "
                f"(figurative={figurative_confidence:.3f} >= threshold={self.threshold}, "
                f"label='{top_figurative_label}')"
            )

            return FigurativeGateResult(
                triggered=True,
                skipped=False,
                original_score=score,
                gated_score=gated_score,
                figurative_confidence=figurative_confidence,
                top_figurative_label=top_figurative_label,
                top_figurative_score=top_figurative_score,
                literal_confidence=literal_confidence,
                threshold=self.threshold,
                reduction_factor=self.reduction_factor,
            )
        else:
            # Not triggered: pass through unchanged
            logger.debug(
                f"🎭 FigurativeGate pass-through: figurative={figurative_confidence:.3f} "
                f"< threshold={self.threshold}"
            )

            return FigurativeGateResult(
                triggered=False,
                skipped=False,
                original_score=score,
                gated_score=score,
                figurative_confidence=figurative_confidence,
                top_figurative_label=top_figurative_label,
                top_figurative_score=top_figurative_score,
                literal_confidence=literal_confidence,
                threshold=self.threshold,
                reduction_factor=self.reduction_factor,
            )


def create_figurative_gate(
    config_manager: Optional["ConfigManager"] = None,
    enabled: Optional[bool] = None,
    threshold: Optional[float] = None,
    reduction_factor: Optional[float] = None,
    skip_below: Optional[float] = None,
) -> FigurativeGate:
    """
    Factory function for FigurativeGate.

    Creates a configured FigurativeGate using ConfigManager settings.

    Args:
        config_manager: Configuration manager instance
        enabled: Override enabled flag (optional)
        threshold: Override threshold (optional)
        reduction_factor: Override reduction factor (optional)
        skip_below: Override skip_below threshold (optional)

    Returns:
        Configured FigurativeGate instance

    Example:
        >>> gate = create_figurative_gate(config_manager=config)
        >>> result = gate.apply(score=0.75, figurative_result=fig_result)
    """
    gate_enabled = True
    gate_threshold = FigurativeGate.DEFAULT_THRESHOLD
    gate_reduction = FigurativeGate.DEFAULT_REDUCTION_FACTOR
    gate_skip_below = FigurativeGate.DEFAULT_SKIP_BELOW

    # Load from config manager
    if config_manager is not None:
        try:
            gate_config = config_manager.get_figurative_gate_config()
            if gate_config:
                gate_enabled = bool(gate_config.get("enabled", True))
                gate_threshold = float(
                    gate_config.get("confidence_threshold", FigurativeGate.DEFAULT_THRESHOLD)
                )
                gate_reduction = float(
                    gate_config.get("reduction_factor", FigurativeGate.DEFAULT_REDUCTION_FACTOR)
                )
                gate_skip_below = float(
                    gate_config.get("skip_below", FigurativeGate.DEFAULT_SKIP_BELOW)
                )
        except Exception as e:
            logger.warning(f"⚠️ Error loading figurative gate config, using defaults: {e}")

    # Apply explicit overrides
    if enabled is not None:
        gate_enabled = enabled
    if threshold is not None:
        gate_threshold = threshold
    if reduction_factor is not None:
        gate_reduction = reduction_factor
    if skip_below is not None:
        gate_skip_below = skip_below

    return FigurativeGate(
        enabled=gate_enabled,
        threshold=gate_threshold,
        reduction_factor=gate_reduction,
        skip_below=gate_skip_below,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "WarmupResult",
    "VigilResponse",
    "CrisisAssessment",
    "RecommendedAction",
    "FigurativeGateResult",
    "FigurativeGate",
    "create_figurative_gate",
]
