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
Ensemble Decision Engine for Ash-NLP Service
---
FILE VERSION: v5.1-6-6.2-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 6 - Irony Gatekeeper Refactor
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Orchestrate multi-model ensemble inference
- Coordinate model loading, scoring, and fallback
- Provide unified analyze() method for API
- Calculate final crisis assessment
- Handle async parallel inference with asyncio.gather()
- Cache responses for repeated messages
- Integrate Ash-Vigil for specialized risk detection (Phase 3 Vigil)

PHASE 3 VIGIL INTEGRATION:
- Ash-Vigil client integration for mental health risk detection
- Risk amplification for subtle crisis signals BART missed
- Configurable skip threshold and amplify_medium toggle
- Hard score cap at 1.0 to prevent exponential creep
- Graceful fallback when Vigil unavailable
- requires_review flag for HIGH/CRITICAL or Vigil unavailable

PROCESSING FLOW (Phase 3 Vigil):
1. Run 4-model ensemble → base score (no irony dampening yet)
2. Determine preliminary severity from base score
3. Decision Gate: Should we call Vigil?
   - If base_score >= skip_threshold → Skip Vigil
   - If MEDIUM severity and amplify_medium=false → Skip Vigil
   - Otherwise → Call Vigil
4. Apply Vigil amplification (cap at 1.0)
5. Apply irony dampening (FINAL step)
6. Determine final severity, set requires_review for HIGH/CRITICAL
7. Return response with vigil field

PHASE 4 ENHANCEMENTS:
- Consensus algorithm selection (weighted, majority, unanimous, conflict-aware)
- Conflict detection and resolution
- Comprehensive result aggregation
- Human-readable explainability

PHASE 5 ENHANCEMENTS:
- Context history analysis integration
- Escalation pattern detection (rapid, gradual, sudden)
- Temporal pattern detection (late night, rapid posting)
- Trend analysis (worsening, stable, improving)
- Intervention urgency recommendations

This is the PRIMARY INTERFACE for crisis detection.
API endpoints call this engine to analyze messages.

PERFORMANCE OPTIMIZATIONS (Phase 3.7):
- 3.7.1: Model warmup on startup with alerting
- 3.7.2: Async parallel inference with asyncio.gather()
- 3.7.4: Response caching for repeated messages
"""

import asyncio
import copy
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from src.models import ModelResult

from .model_loader import ModelLoader, create_model_loader
from .scoring import (
    WeightedScorer,
    create_weighted_scorer,
    EnsembleScore,
    CrisisSeverity,
)
from .fallback import (
    FallbackStrategy,
    create_fallback_strategy,
    CriticalModelFailure,
)

# Phase 4 imports
from .consensus import (
    ConsensusSelector,
    ConsensusAlgorithm,
    ConsensusResult,
    create_consensus_selector,
)
from .conflict_detector import (
    ConflictDetector,
    ConflictReport,
    ModelSignals,
    create_conflict_detector,
)
from .conflict_resolver import (
    ConflictResolver,
    ResolutionStrategy,
    ResolutionResult,
    create_conflict_resolver,
)
from .aggregator import (
    ResultAggregator,
    AggregatedResult,
    CrisisLevel,
    create_result_aggregator,
)
from .explainability import (
    ExplainabilityGenerator,
    VerbosityLevel,
    Explanation,
    create_explainability_generator,
)

# Phase 5 imports
from src.context import (
    ContextAnalyzer,
    create_context_analyzer,
    MessageHistoryItem,
    ContextAnalysisResult,
)

# Phase 3 Vigil imports
from src.clients.vigil_client import (
    VigilClient,
    VigilStatus,
    VigilResult,
    create_vigil_client,
)

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager
    from src.utils.cache import ResponseCache
    from src.utils.alerting import DiscordAlerter

# Module version
__version__ = "v5.1-6-6.2-1"

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
    context_analysis: Optional[ContextAnalysisResult] = None

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
        """Convert to full enhanced dictionary with all Phase 4 data."""
        if self.aggregated_result:
            return self.aggregated_result.to_dict()
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
        irony_signal: Optional["ModelSignal"] = None,
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
# Ensemble Decision Engine
# =============================================================================


class EnsembleDecisionEngine:
    """
    Ensemble Decision Engine - Primary Crisis Detection Interface.

    Orchestrates the multi-model ensemble:
    1. Loads and manages models via ModelLoader
    2. Runs inference on all models (parallel with asyncio.gather)
    3. Calculates weighted scores via WeightedScorer
    4. Handles failures via FallbackStrategy
    5. Caches responses for repeated messages
    6. Returns comprehensive CrisisAssessment

    Phase 3 Vigil Integration:
    - Calls Ash-Vigil for specialized mental health risk detection
    - Amplifies base scores when Vigil detects subtle crisis signals
    - Sets requires_review for HIGH/CRITICAL or Vigil unavailable

    Phase 4 Enhancements:
    - Consensus algorithm selection
    - Conflict detection and resolution
    - Comprehensive result aggregation
    - Human-readable explainability

    Phase 5 Enhancements:
    - Context history analysis integration
    - Escalation, temporal, and trend detection
    - Intervention urgency recommendations

    Phase 6 Enhancements:
    - Irony gatekeeper replaces continuous dampening
    - IronyGate applied AFTER Vigil amplification, BEFORE final severity
    - Only fires when irony confidence >= configurable threshold
    - Zero effect when irony not detected (true pass-through)

    This is the main interface for the API to call.

    Performance Optimizations (Phase 3.7):
    - Model warmup on startup (3.7.1)
    - Async parallel inference with asyncio.gather (3.7.2)
    - Response caching (3.7.4)

    Clean Architecture v5.2.3 Compliance:
    - Factory function: create_decision_engine()
    - Configuration via ConfigManager
    - Dependency injection pattern
    - Resilient error handling (Rule #5)
    """

    # =========================================================================
    # Default Vigil Amplification Configuration
    # =========================================================================

    DEFAULT_VIGIL_AMPLIFICATION = {
        "enabled": True,
        "score_cap": 1.0,
        "skip_threshold": 0.70,
        "amplify_medium": True,
        "vigil_thresholds": {
            "critical": 0.8,
            "high": 0.6,
            "moderate": 0.4,
        },
        "boosts": {
            "critical_boost": 0.35,
            "critical_minimum": 0.55,
            "high_multiplier": 0.3,
            "moderate_multiplier": 0.1,
        },
    }

    def __init__(
        self,
        config_manager: Optional["ConfigManager"] = None,
        model_loader: Optional[ModelLoader] = None,
        scorer: Optional[WeightedScorer] = None,
        fallback: Optional[FallbackStrategy] = None,
        cache: Optional["ResponseCache"] = None,
        alerter: Optional["DiscordAlerter"] = None,
        async_inference: bool = True,
        cache_enabled: bool = True,
        cache_ttl: float = 300.0,
        cache_max_size: int = 1000,
        # Phase 3 Vigil components
        vigil_client: Optional[VigilClient] = None,
        vigil_enabled: bool = True,
        # Phase 4 components
        consensus_selector: Optional[ConsensusSelector] = None,
        conflict_detector: Optional[ConflictDetector] = None,
        conflict_resolver: Optional[ConflictResolver] = None,
        result_aggregator: Optional[ResultAggregator] = None,
        explainability_generator: Optional[ExplainabilityGenerator] = None,
        phase4_enabled: bool = True,
        # Phase 5 components
        context_analyzer: Optional[ContextAnalyzer] = None,
        phase5_enabled: bool = True,
        # Phase 6 components
        irony_gate: Optional[IronyGate] = None,
    ):
        """
        Initialize Ensemble Decision Engine.

        Args:
            config_manager: Configuration manager instance
            model_loader: Pre-configured model loader (optional)
            scorer: Pre-configured scorer (optional)
            fallback: Pre-configured fallback strategy (optional)
            cache: Pre-configured response cache (optional)
            alerter: Discord alerter for notifications (optional)
            async_inference: Enable parallel model inference
            cache_enabled: Enable response caching
            cache_ttl: Cache time-to-live in seconds
            cache_max_size: Maximum cache entries

            # Phase 3 Vigil components
            vigil_client: Pre-configured Vigil client (optional)
            vigil_enabled: Enable Vigil integration (default: True)

            # Phase 4 components
            consensus_selector: Consensus algorithm selector
            conflict_detector: Conflict detection component
            conflict_resolver: Conflict resolution component
            result_aggregator: Result aggregation component
            explainability_generator: Explainability component
            phase4_enabled: Enable Phase 4 features (default: True)

            # Phase 5 components
            context_analyzer: Context history analyzer component
            phase5_enabled: Enable Phase 5 features (default: True)

            # Phase 6 components
            irony_gate: Pre-configured IronyGate (optional, auto-created from config)
        """
        self.config_manager = config_manager
        self.async_inference = async_inference
        self.cache_enabled = cache_enabled
        self.phase4_enabled = phase4_enabled

        # Initialize Phase 3 components
        self.model_loader = model_loader or create_model_loader(
            config_manager=config_manager,
            lazy_load=True,
            warmup_on_load=True,
        )

        self.scorer = scorer or create_weighted_scorer(config_manager=config_manager)

        self.fallback = fallback or create_fallback_strategy(
            config_manager=config_manager
        )

        # Initialize cache (Phase 3.7.4)
        if cache is not None:
            self._cache = cache
        elif cache_enabled:
            from src.utils.cache import create_response_cache

            self._cache = create_response_cache(
                max_size=cache_max_size,
                ttl_seconds=cache_ttl,
                config_manager=config_manager,
            )
        else:
            self._cache = None

        # Alerter for notifications (Phase 3.7.1)
        self._alerter = alerter

        # =====================================================================
        # Initialize Phase 3 Vigil components
        # =====================================================================

        self.vigil_enabled = vigil_enabled
        self._vigil_client: Optional[VigilClient] = None
        self._vigil_amplification_config = copy.deepcopy(self.DEFAULT_VIGIL_AMPLIFICATION)

        if vigil_enabled:
            # Load Vigil configuration
            self._load_vigil_config(config_manager)

            # Initialize Vigil client
            if vigil_client is not None:
                self._vigil_client = vigil_client
            else:
                self._vigil_client = create_vigil_client(
                    config_manager=config_manager,
                )

            logger.info(
                f"🔌 Phase 3 Vigil integration initialized "
                f"(skip_threshold={self._vigil_amplification_config['skip_threshold']}, "
                f"amplify_medium={self._vigil_amplification_config['amplify_medium']})"
            )
        else:
            logger.info("🔌 Phase 3 Vigil integration DISABLED")

        # =====================================================================
        # Initialize Phase 4 components
        # =====================================================================

        if phase4_enabled:
            self.consensus_selector = consensus_selector or create_consensus_selector(
                config_manager=config_manager
            )

            self.conflict_detector = conflict_detector or create_conflict_detector(
                config_manager=config_manager
            )

            self.conflict_resolver = conflict_resolver or create_conflict_resolver(
                config_manager=config_manager,
                alerter=alerter,
            )

            self.result_aggregator = result_aggregator or create_result_aggregator(
                config_manager=config_manager
            )

            self.explainability_generator = (
                explainability_generator
                or create_explainability_generator(config_manager=config_manager)
            )

            logger.info("✨ Phase 4 components initialized")
        else:
            self.consensus_selector = None
            self.conflict_detector = None
            self.conflict_resolver = None
            self.result_aggregator = None
            self.explainability_generator = None

        # =====================================================================
        # Initialize Phase 5 components
        # =====================================================================

        self.phase5_enabled = phase5_enabled

        if phase5_enabled:
            self.context_analyzer = context_analyzer or create_context_analyzer()
            logger.info("🌊 Phase 5 context analyzer initialized")
        else:
            self.context_analyzer = None

        # =====================================================================
        # Initialize Phase 6 components
        # =====================================================================

        self.irony_gate = irony_gate or create_irony_gate(
            config_manager=config_manager
        )

        # Performance tracking
        self._total_requests: int = 0
        self._total_latency_ms: float = 0.0
        self._crisis_detections: int = 0
        self._cache_hits: int = 0
        self._conflicts_detected: int = 0
        self._vigil_calls: int = 0
        self._vigil_amplifications: int = 0
        self._irony_gate_triggers: int = 0

        # Thread pool for parallel inference
        self._executor: Optional[ThreadPoolExecutor] = None
        if async_inference:
            self._executor = ThreadPoolExecutor(max_workers=4)

        logger.info(
            f"🧠 EnsembleDecisionEngine initialized "
            f"(async={async_inference}, cache={cache_enabled}, "
            f"vigil={vigil_enabled}, phase4={phase4_enabled}, phase5={phase5_enabled})"
        )

    def _load_vigil_config(self, config_manager: Optional["ConfigManager"]) -> None:
        """
        Load Vigil amplification configuration from ConfigManager.

        The resolved config from ConfigManager contains the final resolved values
        with environment variable overrides applied. Nested dicts like
        vigil_thresholds and boosts are fully resolved.

        Args:
            config_manager: Configuration manager instance
        """
        if config_manager is None:
            logger.debug("No config_manager provided, using Vigil defaults")
            return

        try:
            # Get the section - ensure we have a dict
            vigil_amp_config = config_manager.get_section("vigil_amplification")
            logger.debug(f"Raw vigil_amplification section: {vigil_amp_config}")
            
            if vigil_amp_config is None:
                logger.debug("vigil_amplification section is None, using defaults")
                return
            
            if not isinstance(vigil_amp_config, dict):
                logger.warning(f"vigil_amplification is not a dict: {type(vigil_amp_config)}")
                return
            
            if not vigil_amp_config:
                logger.debug("No vigil_amplification section found (empty), using defaults")
                return

            # Load top-level settings from resolved config
            if "enabled" in vigil_amp_config:
                val = vigil_amp_config.get("enabled")
                if val is not None:
                    self._vigil_amplification_config["enabled"] = bool(val)

            if "score_cap" in vigil_amp_config:
                val = vigil_amp_config.get("score_cap")
                if val is not None:
                    self._vigil_amplification_config["score_cap"] = float(val)

            if "skip_threshold" in vigil_amp_config:
                val = vigil_amp_config.get("skip_threshold")
                if val is not None:
                    self._vigil_amplification_config["skip_threshold"] = float(val)

            if "amplify_medium" in vigil_amp_config:
                val = vigil_amp_config.get("amplify_medium")
                if val is not None:
                    self._vigil_amplification_config["amplify_medium"] = bool(val)

            # Load nested thresholds - ConfigManager resolves these with env var overrides
            thresholds = vigil_amp_config.get("vigil_thresholds")
            logger.debug(f"vigil_thresholds from config: {thresholds}")
            if thresholds is not None and isinstance(thresholds, dict):
                self._vigil_amplification_config["vigil_thresholds"] = {
                    "critical": float(thresholds.get("critical") or 0.8),
                    "high": float(thresholds.get("high") or 0.6),
                    "moderate": float(thresholds.get("moderate") or 0.4),
                }

            # Load nested boosts - ConfigManager resolves these with env var overrides
            boosts = vigil_amp_config.get("boosts")
            logger.debug(f"boosts from config: {boosts}")
            if boosts is not None and isinstance(boosts, dict):
                self._vigil_amplification_config["boosts"] = {
                    "critical_boost": float(boosts.get("critical_boost") or 0.35),
                    "critical_minimum": float(boosts.get("critical_minimum") or 0.55),
                    "high_multiplier": float(boosts.get("high_multiplier") or 0.3),
                    "moderate_multiplier": float(boosts.get("moderate_multiplier") or 0.1),
                }

            logger.info(
                f"✅ Loaded Vigil amplification config: "
                f"skip_threshold={self._vigil_amplification_config['skip_threshold']}, "
                f"amplify_medium={self._vigil_amplification_config['amplify_medium']}"
            )

        except Exception as e:
            import traceback
            import sys
            error_tb = traceback.format_exc()
            logger.warning(f"Error loading Vigil config, using defaults: {e}")
            # Force print to stderr to ensure we see it
            print(f"VIGIL CONFIG ERROR TRACEBACK:\n{error_tb}", file=sys.stderr, flush=True)

    # =========================================================================
    # Phase 3 Vigil: Amplification Methods
    # =========================================================================

    async def _apply_vigil_amplification(
        self,
        base_score: float,
        base_severity: CrisisSeverity,
        text: str,
    ) -> Tuple[float, VigilResponse]:
        """
        Apply Ash-Vigil risk amplification to base ensemble score.

        Vigil acts as a SOFT amplifier:
        - Only called when base score is below skip_threshold
        - Boosts scores when Vigil detects risk that base models missed
        - Respects amplify_medium toggle for MEDIUM severity
        - Hard caps at score_cap (1.0)
        - Does NOT apply irony dampening (that comes after)

        Args:
            base_score: Pre-irony-dampening ensemble score
            base_severity: Preliminary severity from base score
            text: Original message text

        Returns:
            Tuple of (amplified_score, VigilResponse)
        """
        config = self._vigil_amplification_config

        # =====================================================================
        # Gate 1: Is amplification enabled?
        # =====================================================================
        if not config["enabled"]:
            logger.debug("Vigil amplification disabled in config")
            return base_score, VigilResponse(
                status=VigilStatus.DISABLED,
                base_score=base_score,
            )

        # =====================================================================
        # Gate 2: Is base score already above skip threshold?
        # =====================================================================
        if base_score >= config["skip_threshold"]:
            logger.debug(
                f"Skipping Vigil: base score {base_score:.3f} >= "
                f"skip threshold {config['skip_threshold']}"
            )
            return base_score, VigilResponse(
                status=VigilStatus.SKIPPED,
                base_score=base_score,
            )

        # =====================================================================
        # Gate 3: Is this MEDIUM severity and amplify_medium is disabled?
        # =====================================================================
        if base_severity == CrisisSeverity.MEDIUM and not config["amplify_medium"]:
            logger.debug("Skipping Vigil: MEDIUM severity and amplify_medium=false")
            return base_score, VigilResponse(
                status=VigilStatus.SKIPPED,
                base_score=base_score,
            )

        # =====================================================================
        # Gate 4: Is Vigil client available?
        # =====================================================================
        if not self._vigil_client or not self._vigil_client.enabled:
            logger.debug("Vigil client not available or disabled")
            return base_score, VigilResponse(
                status=VigilStatus.DISABLED,
                base_score=base_score,
            )

        # =====================================================================
        # Call Vigil
        # =====================================================================
        self._vigil_calls += 1
        vigil_result = await self._vigil_client.analyze(text)

        if vigil_result is None:
            # Vigil unavailable - return base score with appropriate status
            status = self._vigil_client.status
            logger.warning(f"Vigil call failed: {status.value}")
            return base_score, VigilResponse(
                status=status,
                base_score=base_score,
            )

        # =====================================================================
        # Apply amplification based on Vigil risk level
        # =====================================================================
        risk_signal = vigil_result.risk_score
        risk_label = vigil_result.risk_label
        thresholds = config["vigil_thresholds"]
        boosts = config["boosts"]

        amplification_applied = False

        if risk_signal >= thresholds["critical"]:
            # Critical risk Vigil caught that base models missed
            amplified = max(
                base_score + boosts["critical_boost"], boosts["critical_minimum"]
            )
            amplification_applied = True
            self._vigil_amplifications += 1
            logger.info(
                f"🚨 Vigil CRITICAL amplification: {base_score:.3f} → {amplified:.3f} "
                f"(vigil_risk={risk_signal:.3f}, label={risk_label})"
            )

        elif risk_signal >= thresholds["high"]:
            # Significant risk, boost with multiplier
            boost = risk_signal * boosts["high_multiplier"]
            amplified = base_score + boost
            amplification_applied = True
            self._vigil_amplifications += 1
            logger.info(
                f"⚠️ Vigil HIGH amplification: {base_score:.3f} → {amplified:.3f} "
                f"(vigil_risk={risk_signal:.3f}, boost={boost:.3f})"
            )

        elif risk_signal >= thresholds["moderate"]:
            # Modest risk signal
            boost = risk_signal * boosts["moderate_multiplier"]
            amplified = base_score + boost
            if boost > 0.01:  # Only count meaningful amplifications
                amplification_applied = True
                self._vigil_amplifications += 1
            logger.debug(
                f"ℹ️ Vigil MODERATE amplification: {base_score:.3f} → {amplified:.3f} "
                f"(vigil_risk={risk_signal:.3f}, boost={boost:.3f})"
            )

        else:
            # Vigil didn't detect significant risk
            amplified = base_score
            logger.debug(
                f"Vigil detected low risk ({risk_signal:.3f}), no amplification"
            )

        # =====================================================================
        # HARD CAP - Never exceed score_cap
        # =====================================================================
        if amplified > config["score_cap"]:
            logger.debug(f"Applying hard cap: {amplified:.3f} → {config['score_cap']}")
            amplified = config["score_cap"]

        return amplified, VigilResponse(
            status=VigilStatus.USED,
            risk_score=risk_signal,
            risk_label=risk_label,
            amplification_applied=amplification_applied,
            base_score=base_score,
            amplified_score=amplified,
        )

    def _apply_vigil_amplification_sync(
        self,
        base_score: float,
        base_severity: CrisisSeverity,
        text: str,
    ) -> Tuple[float, VigilResponse]:
        """
        Synchronous wrapper for Vigil amplification.

        Used by the sync analyze() method.

        Args:
            base_score: Pre-irony-dampening ensemble score
            base_severity: Preliminary severity from base score
            text: Original message text

        Returns:
            Tuple of (amplified_score, VigilResponse)
        """
        # Run async method in event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create a new task for nested async call
                import concurrent.futures

                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run,
                        self._apply_vigil_amplification(
                            base_score, base_severity, text
                        ),
                    )
                    return future.result(timeout=2.0)
            else:
                return loop.run_until_complete(
                    self._apply_vigil_amplification(base_score, base_severity, text)
                )
        except Exception as e:
            logger.warning(f"Sync Vigil amplification failed: {e}")
            return base_score, VigilResponse(
                status=VigilStatus.UNAVAILABLE,
                base_score=base_score,
            )

    def _determine_requires_review(
        self,
        final_severity: CrisisSeverity,
        vigil_response: VigilResponse,
    ) -> bool:
        """
        Determine if CRT review is required.

        Rules:
        - HIGH or CRITICAL severity → always requires review
        - Vigil unavailable/timeout/circuit_open → requires review (safety net)

        Args:
            final_severity: Final severity after all processing
            vigil_response: Vigil response with status

        Returns:
            True if CRT review is recommended
        """
        # HIGH and CRITICAL always need review
        if final_severity in (CrisisSeverity.HIGH, CrisisSeverity.CRITICAL):
            return True

        # If Vigil was supposed to run but couldn't, flag for review
        if vigil_response.status in (
            VigilStatus.UNAVAILABLE,
            VigilStatus.TIMEOUT,
            VigilStatus.CIRCUIT_OPEN,
        ):
            return True

        return False

    # =========================================================================
    # Main Analysis Methods
    # =========================================================================

    def analyze(
        self,
        message: str,
        use_cache: bool = True,
        include_explanation: bool = True,
        verbosity: Optional[str] = None,
        consensus_algorithm: Optional[str] = None,
        message_history: Optional[List[Dict]] = None,
        include_context_analysis: bool = True,
    ) -> CrisisAssessment:
        """
        Analyze a message for crisis signals.

        This is the PRIMARY method for crisis detection.
        Includes Phase 3 Vigil, Phase 4, and Phase 5 enhancements.

        Args:
            message: Text message to analyze
            use_cache: Whether to use response cache (default: True)
            include_explanation: Include human-readable explanation (Phase 4)
            verbosity: Explanation verbosity: minimal, standard, detailed (Phase 4)
            consensus_algorithm: Override consensus algorithm (Phase 4)
            message_history: List of prior messages with timestamps/scores (Phase 5)
            include_context_analysis: Include context analysis in response (Phase 5)

        Returns:
            CrisisAssessment with complete analysis
        """
        start_time = time.perf_counter()
        per_model_latency: Dict[str, float] = {}

        try:
            # Check cache first (Phase 3.7.4)
            if use_cache and self._cache is not None and self.cache_enabled:
                cached_result = self._cache.get(message)
                if cached_result is not None:
                    self._cache_hits += 1
                    self._total_requests += 1
                    # Update timing for cached response
                    cached_result.processing_time_ms = (
                        time.perf_counter() - start_time
                    ) * 1000
                    cached_result.cached = True
                    logger.debug(
                        f"Cache hit for message (hash: {hash(message) % 10000})"
                    )
                    return cached_result

            # Run inference on all models
            inference_start = time.perf_counter()
            if self.async_inference and self._executor:
                results, per_model_latency = self._run_parallel_inference_with_timing(
                    message
                )
            else:
                results, per_model_latency = self._run_sequential_inference_with_timing(
                    message
                )

            # Calculate ensemble score (Phase 3 scoring)
            # This gives us base_score (before irony) and irony_dampening factor
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # =================================================================
            # Phase 3 Vigil: Apply amplification BEFORE irony gate
            # =================================================================

            # Get base score (Phase 6: irony_dampening is always 1.0 from scorer)
            base_score = ensemble_score.base_score

            # Determine preliminary severity from base score
            preliminary_severity = CrisisSeverity.from_score(
                base_score, self.scorer.get_thresholds()
            )

            # Apply Vigil amplification (sync version)
            vigil_response: VigilResponse
            if self.vigil_enabled:
                amplified_score, vigil_response = self._apply_vigil_amplification_sync(
                    base_score=base_score,
                    base_severity=preliminary_severity,
                    text=message,
                )
            else:
                amplified_score = base_score
                vigil_response = VigilResponse(
                    status=VigilStatus.DISABLED,
                    base_score=base_score,
                )

            # =================================================================
            # Phase 6: Apply Irony Gatekeeper AFTER Vigil amplification
            # =================================================================

            irony_signal = ensemble_score.signals.get("irony")
            irony_gate_result = self.irony_gate.apply(
                score=amplified_score,
                irony_signal=irony_signal,
            )
            final_score = irony_gate_result.gated_score

            if irony_gate_result.triggered:
                self._irony_gate_triggers += 1

            # Recalculate final severity
            final_severity = CrisisSeverity.from_score(
                final_score, self.scorer.get_thresholds()
            )

            # Determine if review required
            requires_review = self._determine_requires_review(
                final_severity, vigil_response
            )

            # Update ensemble_score with our recalculated values
            # (We override the scorer's irony-dampened value with our Vigil-amplified one)
            ensemble_score.crisis_score = final_score
            ensemble_score.severity = final_severity
            ensemble_score.crisis_detected = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
                CrisisSeverity.MEDIUM,
            )
            ensemble_score.requires_intervention = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
            )

            # Calculate processing time
            processing_time_ms = (time.perf_counter() - start_time) * 1000

            # =========================================================
            # Phase 4: Enhanced Processing
            # =========================================================

            consensus_result: Optional[ConsensusResult] = None
            conflict_report: Optional[ConflictReport] = None
            resolution_result: Optional[ResolutionResult] = None
            aggregated_result: Optional[AggregatedResult] = None
            explanation: Optional[Explanation] = None

            if self.phase4_enabled:
                # Extract crisis signals for consensus
                crisis_scores = {
                    name: signal.crisis_signal
                    for name, signal in ensemble_score.signals.items()
                }

                # Build signals dict for conflict detection
                signals_dict = {
                    name: {
                        "crisis_signal": signal.crisis_signal,
                        "label": signal.label,
                        "raw_score": signal.raw_score,
                        "score": signal.raw_score,
                        "metadata": signal.metadata,
                    }
                    for name, signal in ensemble_score.signals.items()
                }

                # Run consensus algorithm
                if self.consensus_selector:
                    algo = None
                    if consensus_algorithm:
                        try:
                            algo = ConsensusAlgorithm(consensus_algorithm)
                        except ValueError:
                            logger.warning(
                                f"Invalid consensus algorithm: {consensus_algorithm}"
                            )

                    consensus_result = self.consensus_selector.select_and_run(
                        model_signals=crisis_scores,
                        algorithm=algo,
                    )

                # Run conflict detection
                if self.conflict_detector:
                    model_signals = ModelSignals.from_ensemble_signals(signals_dict)
                    conflict_report = self.conflict_detector.detect_conflicts(
                        model_signals=model_signals,
                        crisis_scores=crisis_scores,
                    )

                    if conflict_report.has_conflicts:
                        self._conflicts_detected += 1

                # Run conflict resolution if conflicts found
                if (
                    self.conflict_resolver
                    and conflict_report
                    and conflict_report.has_conflicts
                ):
                    resolution_result = self.conflict_resolver.resolve(
                        crisis_scores=crisis_scores,
                        conflict_report=conflict_report,
                        message_preview=message[:100],
                    )

                # Aggregate results
                if self.result_aggregator:
                    aggregated_result = self.result_aggregator.aggregate(
                        model_signals=signals_dict,
                        consensus_result=consensus_result,
                        conflict_report=conflict_report,
                        resolution_result=resolution_result,
                        processing_time_ms=processing_time_ms,
                        per_model_latency=per_model_latency,
                        is_degraded=self.fallback.is_degraded(),
                        degradation_reason=self.fallback.get_degradation_reason(),
                        message=message,
                        cached=False,
                    )

                # Generate explanation
                if (
                    include_explanation
                    and self.explainability_generator
                    and aggregated_result
                ):
                    verbosity_level = None
                    if verbosity:
                        try:
                            verbosity_level = VerbosityLevel(verbosity)
                        except ValueError:
                            pass

                    explanation = self.explainability_generator.generate(
                        result=aggregated_result,
                        verbosity=verbosity_level,
                    )

                    # Attach explanation to aggregated result
                    aggregated_result.explanation = explanation.to_dict()

            # =========================================================
            # Phase 5: Context History Analysis
            # =========================================================

            context_analysis_result: Optional[ContextAnalysisResult] = None

            if (
                self.phase5_enabled
                and include_context_analysis
                and self.context_analyzer
            ):
                try:
                    # Convert message history to MessageHistoryItem objects
                    history_items: List[MessageHistoryItem] = []
                    if message_history:
                        for item in message_history:
                            history_items.append(MessageHistoryItem.from_dict(item))

                    # Run context analysis with current message score
                    context_analysis_result = self.context_analyzer.analyze(
                        current_message=message,
                        current_score=final_score,
                        message_history=history_items,
                    )

                    logger.debug(
                        f"Context analysis: escalation={context_analysis_result.escalation.detected}, "
                        f"trend={context_analysis_result.trend.direction}, "
                        f"urgency={context_analysis_result.intervention.urgency}"
                    )

                except Exception as e:
                    logger.error(f"Context analysis failed: {e}")
                    # Continue without context analysis - non-critical failure

            # Build assessment
            assessment = self._build_assessment_enhanced(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
                vigil_response=vigil_response,
                requires_review=requires_review,
                consensus_result=consensus_result,
                conflict_report=conflict_report,
                resolution_result=resolution_result,
                aggregated_result=aggregated_result,
                explanation=explanation,
                context_analysis_result=context_analysis_result,
                irony_gate_result=irony_gate_result,
            )

            # Store in cache (Phase 3.7.4)
            if use_cache and self._cache is not None and self.cache_enabled:
                self._cache.set(message, assessment)

            # Update stats
            self._total_requests += 1
            self._total_latency_ms += processing_time_ms
            if assessment.crisis_detected:
                self._crisis_detections += 1

            return assessment

        except CriticalModelFailure as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.critical(f"🚨 Critical model failure during analysis: {e}")

            # Send alert if alerter configured
            if self._alerter:
                asyncio.create_task(
                    self._alerter.alert_model_failure("bart", str(e), is_critical=True)
                )

            return CrisisAssessment.create_error(
                error=str(e),
                message=message,
                processing_time_ms=processing_time_ms,
            )

        except Exception as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"❌ Analysis failed: {e}")
            return CrisisAssessment.create_error(
                error=str(e),
                message=message,
                processing_time_ms=processing_time_ms,
            )

    async def analyze_async(
        self,
        message: str,
        use_cache: bool = True,
        include_explanation: bool = True,
        verbosity: Optional[str] = None,
        consensus_algorithm: Optional[str] = None,
        message_history: Optional[List[Dict]] = None,
        include_context_analysis: bool = True,
    ) -> CrisisAssessment:
        """
        Async version of analyze using asyncio.gather for parallel inference.

        This is the optimized async implementation (Phase 3.7.2).
        Includes Phase 3 Vigil, Phase 4, and Phase 5 enhancements.

        Args:
            message: Text message to analyze
            use_cache: Whether to use response cache
            include_explanation: Include human-readable explanation (Phase 4)
            verbosity: Explanation verbosity level (Phase 4)
            consensus_algorithm: Override consensus algorithm (Phase 4)
            message_history: List of prior messages with timestamps/scores (Phase 5)
            include_context_analysis: Include context analysis in response (Phase 5)

        Returns:
            CrisisAssessment with complete analysis
        """
        start_time = time.perf_counter()
        per_model_latency: Dict[str, float] = {}

        try:
            # Check cache first (Phase 3.7.4)
            if use_cache and self._cache is not None and self.cache_enabled:
                cached_result = self._cache.get(message)
                if cached_result is not None:
                    self._cache_hits += 1
                    self._total_requests += 1
                    cached_result.processing_time_ms = (
                        time.perf_counter() - start_time
                    ) * 1000
                    cached_result.cached = True
                    return cached_result

            # Run parallel inference with asyncio.gather (Phase 3.7.2)
            (
                results,
                per_model_latency,
            ) = await self._run_async_parallel_inference_with_timing(message)

            # Calculate ensemble score
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # =================================================================
            # Phase 3 Vigil: Apply amplification BEFORE irony gate
            # =================================================================

            base_score = ensemble_score.base_score

            preliminary_severity = CrisisSeverity.from_score(
                base_score, self.scorer.get_thresholds()
            )

            # Apply Vigil amplification (async version)
            vigil_response: VigilResponse
            if self.vigil_enabled:
                amplified_score, vigil_response = await self._apply_vigil_amplification(
                    base_score=base_score,
                    base_severity=preliminary_severity,
                    text=message,
                )
            else:
                amplified_score = base_score
                vigil_response = VigilResponse(
                    status=VigilStatus.DISABLED,
                    base_score=base_score,
                )

            # =================================================================
            # Phase 6: Apply Irony Gatekeeper AFTER Vigil amplification
            # =================================================================

            irony_signal = ensemble_score.signals.get("irony")
            irony_gate_result = self.irony_gate.apply(
                score=amplified_score,
                irony_signal=irony_signal,
            )
            final_score = irony_gate_result.gated_score

            if irony_gate_result.triggered:
                self._irony_gate_triggers += 1

            # Recalculate final severity
            final_severity = CrisisSeverity.from_score(
                final_score, self.scorer.get_thresholds()
            )

            # Determine if review required
            requires_review = self._determine_requires_review(
                final_severity, vigil_response
            )

            # Update ensemble_score
            ensemble_score.crisis_score = final_score
            ensemble_score.severity = final_severity
            ensemble_score.crisis_detected = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
                CrisisSeverity.MEDIUM,
            )
            ensemble_score.requires_intervention = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
            )

            # Calculate processing time
            processing_time_ms = (time.perf_counter() - start_time) * 1000

            # =========================================================
            # Phase 4: Enhanced Processing (Async)
            # =========================================================

            consensus_result: Optional[ConsensusResult] = None
            conflict_report: Optional[ConflictReport] = None
            resolution_result: Optional[ResolutionResult] = None
            aggregated_result: Optional[AggregatedResult] = None
            explanation: Optional[Explanation] = None

            if self.phase4_enabled:
                # Extract crisis signals
                crisis_scores = {
                    name: signal.crisis_signal
                    for name, signal in ensemble_score.signals.items()
                }

                signals_dict = {
                    name: {
                        "crisis_signal": signal.crisis_signal,
                        "label": signal.label,
                        "raw_score": signal.raw_score,
                        "score": signal.raw_score,
                        "metadata": signal.metadata,
                    }
                    for name, signal in ensemble_score.signals.items()
                }

                # Run consensus
                if self.consensus_selector:
                    algo = None
                    if consensus_algorithm:
                        try:
                            algo = ConsensusAlgorithm(consensus_algorithm)
                        except ValueError:
                            pass

                    consensus_result = self.consensus_selector.select_and_run(
                        model_signals=crisis_scores,
                        algorithm=algo,
                    )

                # Run conflict detection
                if self.conflict_detector:
                    model_signals = ModelSignals.from_ensemble_signals(signals_dict)
                    conflict_report = self.conflict_detector.detect_conflicts(
                        model_signals=model_signals,
                        crisis_scores=crisis_scores,
                    )

                    if conflict_report.has_conflicts:
                        self._conflicts_detected += 1

                # Run conflict resolution (async)
                if (
                    self.conflict_resolver
                    and conflict_report
                    and conflict_report.has_conflicts
                ):
                    resolution_result = await self.conflict_resolver.resolve_async(
                        crisis_scores=crisis_scores,
                        conflict_report=conflict_report,
                        message_preview=message[:100],
                    )

                # Aggregate results
                if self.result_aggregator:
                    aggregated_result = self.result_aggregator.aggregate(
                        model_signals=signals_dict,
                        consensus_result=consensus_result,
                        conflict_report=conflict_report,
                        resolution_result=resolution_result,
                        processing_time_ms=processing_time_ms,
                        per_model_latency=per_model_latency,
                        is_degraded=self.fallback.is_degraded(),
                        degradation_reason=self.fallback.get_degradation_reason(),
                        message=message,
                        cached=False,
                    )

                # Generate explanation
                if (
                    include_explanation
                    and self.explainability_generator
                    and aggregated_result
                ):
                    verbosity_level = None
                    if verbosity:
                        try:
                            verbosity_level = VerbosityLevel(verbosity)
                        except ValueError:
                            pass

                    explanation = self.explainability_generator.generate(
                        result=aggregated_result,
                        verbosity=verbosity_level,
                    )

                    aggregated_result.explanation = explanation.to_dict()

            # =========================================================
            # Phase 5: Context History Analysis (Async)
            # =========================================================

            context_analysis_result: Optional[ContextAnalysisResult] = None

            if (
                self.phase5_enabled
                and include_context_analysis
                and self.context_analyzer
            ):
                try:
                    # Convert message history to MessageHistoryItem objects
                    history_items: List[MessageHistoryItem] = []
                    if message_history:
                        for item in message_history:
                            history_items.append(MessageHistoryItem.from_dict(item))

                    # Run context analysis with current message score
                    context_analysis_result = self.context_analyzer.analyze(
                        current_message=message,
                        current_score=final_score,
                        message_history=history_items,
                    )

                    logger.debug(
                        f"Context analysis (async): escalation={context_analysis_result.escalation.detected}, "
                        f"trend={context_analysis_result.trend.direction}, "
                        f"urgency={context_analysis_result.intervention.urgency}"
                    )

                except Exception as e:
                    logger.error(f"Context analysis failed (async): {e}")
                    # Continue without context analysis - non-critical failure

            # Build assessment
            assessment = self._build_assessment_enhanced(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
                vigil_response=vigil_response,
                requires_review=requires_review,
                consensus_result=consensus_result,
                conflict_report=conflict_report,
                resolution_result=resolution_result,
                aggregated_result=aggregated_result,
                explanation=explanation,
                context_analysis_result=context_analysis_result,
                irony_gate_result=irony_gate_result,
            )


            # Store in cache
            if use_cache and self._cache is not None and self.cache_enabled:
                self._cache.set(message, assessment)

            # Update stats
            self._total_requests += 1
            self._total_latency_ms += processing_time_ms
            if assessment.crisis_detected:
                self._crisis_detections += 1

            return assessment

        except CriticalModelFailure as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.critical(f"🚨 Critical model failure during analysis: {e}")

            if self._alerter:
                await self._alerter.alert_model_failure(
                    "bart", str(e), is_critical=True
                )

            return CrisisAssessment.create_error(
                error=str(e),
                message=message,
                processing_time_ms=processing_time_ms,
            )

        except Exception as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"❌ Analysis failed: {e}")
            return CrisisAssessment.create_error(
                error=str(e),
                message=message,
                processing_time_ms=processing_time_ms,
            )

    # =========================================================================
    # Inference Methods with Timing
    # =========================================================================

    def _run_sequential_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run sequential inference with per-model timing."""
        results: Dict[str, Optional[ModelResult]] = {}
        latencies: Dict[str, float] = {}
        model_names = ["bart", "sentiment", "irony", "emotions"]

        for model_name in model_names:
            if self.fallback.can_call_model(model_name):
                model_start = time.perf_counter()
                try:
                    model = self.model_loader.get_model(model_name)
                    if model:
                        results[model_name] = model.analyze(message)
                        self.fallback.handle_model_success(model_name)
                except Exception as e:
                    self.fallback.handle_model_failure(model_name, str(e))
                finally:
                    latencies[model_name] = (time.perf_counter() - model_start) * 1000

        return results, latencies

    def _run_parallel_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run parallel inference with per-model timing."""
        results: Dict[str, Optional[ModelResult]] = {}
        latencies: Dict[str, float] = {}

        def run_model(model_name: str) -> tuple:
            if not self.fallback.can_call_model(model_name):
                return (model_name, None, 0.0)

            model_start = time.perf_counter()
            try:
                model = self.model_loader.get_model(model_name)
                if model:
                    result = model.analyze(message)
                    self.fallback.handle_model_success(model_name)
                    latency = (time.perf_counter() - model_start) * 1000
                    return (model_name, result, latency)
                return (model_name, None, 0.0)
            except Exception as e:
                self.fallback.handle_model_failure(model_name, str(e))
                latency = (time.perf_counter() - model_start) * 1000
                return (model_name, None, latency)

        model_names = ["bart", "sentiment", "irony", "emotions"]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(run_model, name): name for name in model_names}

            for future in futures:
                model_name = futures[future]
                try:
                    name, result, latency = future.result(timeout=30)
                    if result:
                        results[name] = result
                    latencies[name] = latency
                except Exception as e:
                    logger.error(f"Parallel inference failed for {model_name}: {e}")

        return results, latencies

    async def _run_async_parallel_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run async parallel inference with per-model timing."""
        loop = asyncio.get_event_loop()

        async def run_model_async(model_name: str) -> tuple:
            if not self.fallback.can_call_model(model_name):
                return (model_name, None, 0.0)

            model_start = time.perf_counter()
            try:
                model = self.model_loader.get_model(model_name)
                if model:
                    result = await loop.run_in_executor(
                        self._executor,
                        model.analyze,
                        message,
                    )
                    self.fallback.handle_model_success(model_name)
                    latency = (time.perf_counter() - model_start) * 1000
                    return (model_name, result, latency)
                return (model_name, None, 0.0)
            except Exception as e:
                self.fallback.handle_model_failure(model_name, str(e))
                logger.warning(f"Model {model_name} failed: {e}")
                latency = (time.perf_counter() - model_start) * 1000
                return (model_name, None, latency)

        model_names = ["bart", "sentiment", "irony", "emotions"]
        tasks = [run_model_async(name) for name in model_names]

        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        results: Dict[str, Optional[ModelResult]] = {}
        latencies: Dict[str, float] = {}

        for item in results_list:
            if isinstance(item, Exception):
                logger.error(f"Async inference exception: {item}")
                continue
            if isinstance(item, tuple) and len(item) == 3:
                model_name, result, latency = item
                if result is not None:
                    results[model_name] = result
                latencies[model_name] = latency

        return results, latencies

    # =========================================================================
    # Assessment Building
    # =========================================================================

    def _build_assessment_enhanced(
        self,
        ensemble_score: EnsembleScore,
        results: Dict[str, Optional[ModelResult]],
        message: str,
        processing_time_ms: float,
        vigil_response: VigilResponse,
        requires_review: bool,
        consensus_result: Optional[ConsensusResult] = None,
        conflict_report: Optional[ConflictReport] = None,
        resolution_result: Optional[ResolutionResult] = None,
        aggregated_result: Optional[AggregatedResult] = None,
        explanation: Optional[Explanation] = None,
        context_analysis_result: Optional[ContextAnalysisResult] = None,
        irony_gate_result: Optional[IronyGateResult] = None,
    ) -> CrisisAssessment:
        """
        Build CrisisAssessment with Phase 3 Vigil, Phase 4, Phase 5, and Phase 6 enhancements.

        Args:
            ensemble_score: Calculated ensemble score (with Vigil-amplified crisis_score)
            results: Model results
            message: Original message
            processing_time_ms: Processing time
            vigil_response: Phase 3 Vigil response
            requires_review: Phase 3 Vigil requires_review flag
            consensus_result: Phase 4 consensus result
            conflict_report: Phase 4 conflict report
            resolution_result: Phase 4 resolution result
            aggregated_result: Phase 4 aggregated result
            explanation: Phase 4 explanation
            context_analysis_result: Phase 5 context analysis result
            irony_gate_result: Phase 6 irony gatekeeper result

        Returns:
            Complete CrisisAssessment with all phase data
        """
        # Use resolved score if available, otherwise ensemble score
        final_crisis_score = ensemble_score.crisis_score
        if resolution_result and resolution_result.was_modified:
            final_crisis_score = resolution_result.resolved_score

        # Determine recommended action
        recommended_action = RecommendedAction.from_severity(ensemble_score.severity)

        # Build signals dict for response
        signals = {}
        for name, signal in ensemble_score.signals.items():
            signals[name] = {
                "label": signal.label,
                "score": round(signal.raw_score, 4),
                "crisis_signal": round(signal.crisis_signal, 4),
            }

        # List models that contributed
        models_used = list(results.keys())

        # Check if review required (from Phase 4 as well)
        if resolution_result and resolution_result.requires_review:
            requires_review = True
        elif conflict_report and conflict_report.requires_review:
            requires_review = True

        # Build assessment
        assessment = CrisisAssessment(
            crisis_detected=ensemble_score.crisis_detected,
            severity=ensemble_score.severity,
            confidence=ensemble_score.confidence,
            crisis_score=final_crisis_score,
            requires_intervention=ensemble_score.requires_intervention
            or requires_review,
            requires_review=requires_review,
            recommended_action=recommended_action,
            signals=signals,
            processing_time_ms=processing_time_ms,
            models_used=models_used,
            is_degraded=self.fallback.is_degraded(),
            degradation_reason=self.fallback.get_degradation_reason(),
            message=message,
            # Phase 3 Vigil fields
            vigil=vigil_response,
            # Phase 4 fields
            explanation=explanation.to_dict() if explanation else None,
            conflict_report=conflict_report.to_dict() if conflict_report else None,
            consensus_result=consensus_result.to_dict() if consensus_result else None,
            aggregated_result=aggregated_result,
            # Phase 5 fields
            context_analysis=context_analysis_result,
            # Phase 6 fields
            irony_gate_result=irony_gate_result,
        )

        return assessment

    # =========================================================================
    # Initialization and Management
    # =========================================================================

    def initialize(self) -> bool:
        """
        Initialize the engine (load all models).

        Returns:
            True if initialization succeeded
        """
        logger.info("🚀 Initializing Decision Engine...")

        try:
            results = self.model_loader.load_all_models()

            success_count = sum(1 for r in results.values() if r)
            total_count = len(results)

            if results.get("bart", False):
                logger.info(
                    f"✅ Engine initialized ({success_count}/{total_count} models)"
                )
                return True
            else:
                logger.error("❌ BART model failed to load - engine not ready")
                return False

        except Exception as e:
            logger.error(f"❌ Engine initialization failed: {e}")
            return False

    def shutdown(self) -> None:
        """Shutdown the engine and release resources."""
        logger.info("🛑 Shutting down Decision Engine...")

        # Unload models
        self.model_loader.unload_all_models()

        # Shutdown thread pool
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None

        # Clear cache
        if self._cache:
            self._cache.clear()

        logger.info("✅ Decision Engine shutdown complete")

    def warmup(self, sample_text: str = "Hello, how are you today?") -> WarmupResult:
        """
        Warm up the engine with a sample analysis (FE-004 Enhanced).

        Phase 3.7.1: Model warmup on startup.
        Phase 6 FE-004: Enhanced with WarmupResult tracking.

        Note: Alerting and Vigil are disabled during warmup to prevent spurious notifications.

        Args:
            sample_text: Text to use for warmup

        Returns:
            WarmupResult with detailed timing and status information
        """
        logger.info("🔥 Warming up Decision Engine...")
        start_time = time.perf_counter()

        # Temporarily disable alerting during warmup
        original_alerter = None
        if self.conflict_resolver:
            original_alerter = self.conflict_resolver._alerter
            self.conflict_resolver._alerter = None

        # Temporarily disable Vigil during warmup
        original_vigil_enabled = self.vigil_enabled
        self.vigil_enabled = False

        try:
            # Run warmup analysis (bypass cache, no explanations)
            # Use sequential inference to get accurate per-model timing
            results, per_model_latency = self._run_sequential_inference_with_timing(
                sample_text
            )

            total_latency_ms = (time.perf_counter() - start_time) * 1000
            models_warmed = list(results.keys())

            if "bart" in results and results["bart"] is not None:
                warmup_result = WarmupResult(
                    success=True,
                    total_latency_ms=total_latency_ms,
                    per_model_latency_ms=per_model_latency,
                    models_warmed=models_warmed,
                )

                # Store warmup result for status reporting
                self._warmup_result = warmup_result

                logger.info(
                    f"✅ Engine warmed up (total: {total_latency_ms:.1f}ms, "
                    f"models: {len(models_warmed)})"
                )
                for model, latency in per_model_latency.items():
                    logger.debug(f"   {model}: {latency:.1f}ms")

                return warmup_result
            else:
                warmup_result = WarmupResult(
                    success=False,
                    total_latency_ms=total_latency_ms,
                    per_model_latency_ms=per_model_latency,
                    models_warmed=models_warmed,
                    error="BART model did not return valid result",
                )
                self._warmup_result = warmup_result
                logger.warning("⚠️ Warmup returned invalid result")
                return warmup_result

        except Exception as e:
            total_latency_ms = (time.perf_counter() - start_time) * 1000
            warmup_result = WarmupResult(
                success=False,
                total_latency_ms=total_latency_ms,
                error=str(e),
            )
            self._warmup_result = warmup_result
            logger.error(f"❌ Warmup failed: {e}")
            return warmup_result

        finally:
            # Restore alerter after warmup
            if self.conflict_resolver and original_alerter is not None:
                self.conflict_resolver._alerter = original_alerter

            # Restore Vigil after warmup
            self.vigil_enabled = original_vigil_enabled

    def get_warmup_result(self) -> Optional[WarmupResult]:
        """
        Get the last warmup result (FE-004).

        Returns:
            WarmupResult from last warmup, or None if never warmed up
        """
        return getattr(self, "_warmup_result", None)

    def set_alerter(self, alerter: "DiscordAlerter") -> None:
        """
        Set the Discord alerter for notifications.

        Args:
            alerter: DiscordAlerter instance
        """
        self._alerter = alerter

        # Also set on conflict resolver
        if self.conflict_resolver:
            self.conflict_resolver.set_alerter(alerter)

        logger.debug("Discord alerter configured")

    # =========================================================================
    # Phase 3 Vigil Configuration Methods
    # =========================================================================

    def get_vigil_config(self) -> Dict[str, Any]:
        """
        Get current Vigil configuration.

        Returns:
            Vigil configuration dictionary
        """
        return {
            "enabled": self.vigil_enabled,
            "client_enabled": self._vigil_client.enabled
            if self._vigil_client
            else False,
            "amplification": self._vigil_amplification_config,
            "client_health": self._vigil_client.get_health()
            if self._vigil_client
            else None,
        }

    def get_vigil_stats(self) -> Dict[str, Any]:
        """
        Get Vigil usage statistics.

        Returns:
            Vigil statistics dictionary
        """
        return {
            "calls": self._vigil_calls,
            "amplifications": self._vigil_amplifications,
            "amplification_rate": (
                self._vigil_amplifications / self._vigil_calls
                if self._vigil_calls > 0
                else 0.0
            ),
        }

    def reset_vigil_circuit(self) -> None:
        """
        Manually reset the Vigil circuit breaker.

        Useful for administrative recovery after fixing Vigil issues.
        """
        if self._vigil_client:
            self._vigil_client.reset_circuit()
            logger.info("Vigil circuit breaker reset via engine")

    # =========================================================================
    # Phase 4 Configuration Methods
    # =========================================================================

    def set_consensus_algorithm(self, algorithm: str) -> None:
        """Set the default consensus algorithm."""
        if self.consensus_selector:
            try:
                algo = ConsensusAlgorithm(algorithm)
                self.consensus_selector.set_algorithm(algo)
                logger.info(f"Consensus algorithm set to: {algorithm}")
            except ValueError:
                logger.warning(f"Invalid consensus algorithm: {algorithm}")

    def set_resolution_strategy(self, strategy: str) -> None:
        """Set the default conflict resolution strategy."""
        if self.conflict_resolver:
            try:
                strat = ResolutionStrategy(strategy)
                self.conflict_resolver.set_strategy(strat)
                logger.info(f"Resolution strategy set to: {strategy}")
            except ValueError:
                logger.warning(f"Invalid resolution strategy: {strategy}")

    def set_explainability_verbosity(self, verbosity: str) -> None:
        """Set the default explainability verbosity."""
        if self.explainability_generator:
            try:
                level = VerbosityLevel(verbosity)
                self.explainability_generator.set_verbosity(level)
                logger.info(f"Explainability verbosity set to: {verbosity}")
            except ValueError:
                logger.warning(f"Invalid verbosity level: {verbosity}")

    def get_consensus_config(self) -> Optional[Dict[str, Any]]:
        """Get current consensus configuration."""
        if self.consensus_selector:
            return self.consensus_selector.get_config()
        return None

    def get_conflict_config(self) -> Optional[Dict[str, Any]]:
        """Get current conflict detection configuration."""
        if self.conflict_detector:
            return self.conflict_detector.get_config()
        return None

    # =========================================================================
    # Phase 5 Configuration Methods
    # =========================================================================

    def get_context_config(self) -> Optional[Dict[str, Any]]:
        """
        Get current context analysis configuration.

        Returns:
            Context configuration dictionary or None if disabled
        """
        if self.context_analyzer and self.phase5_enabled:
            return {
                "enabled": self.context_analyzer.is_enabled(),
                "max_history_size": self.context_analyzer.get_max_history_size(),
            }
        return None

    def is_context_analysis_enabled(self) -> bool:
        """
        Check if context analysis is enabled.

        Returns:
            True if Phase 5 and context analyzer are enabled
        """
        if self.phase5_enabled and self.context_analyzer:
            return self.context_analyzer.is_enabled()
        return False

    # =========================================================================
    # Cache Management
    # =========================================================================

    def clear_cache(self) -> int:
        """
        Clear the response cache.

        Returns:
            Number of entries cleared
        """
        if self._cache:
            return self._cache.clear()
        return 0

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Cache stats dictionary
        """
        if self._cache:
            return self._cache.get_stats()
        return {"enabled": False}

    # =========================================================================
    # Status and Metrics
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive engine status.

        Returns:
            Status dictionary
        """
        avg_latency = (
            self._total_latency_ms / self._total_requests
            if self._total_requests > 0
            else 0.0
        )

        cache_hit_rate = (
            self._cache_hits / self._total_requests if self._total_requests > 0 else 0.0
        )

        status = {
            "is_ready": self.is_ready(),
            "is_degraded": self.fallback.is_degraded(),
            "degradation_reason": self.fallback.get_degradation_reason(),
            "async_inference": self.async_inference,
            "cache_enabled": self.cache_enabled,
            "vigil_enabled": self.vigil_enabled,
            "phase4_enabled": self.phase4_enabled,
            "phase5_enabled": self.phase5_enabled,
            "stats": {
                "total_requests": self._total_requests,
                "crisis_detections": self._crisis_detections,
                "conflicts_detected": self._conflicts_detected,
                "cache_hits": self._cache_hits,
                "cache_hit_rate": round(cache_hit_rate, 4),
                "average_latency_ms": round(avg_latency, 2),
                "vigil_calls": self._vigil_calls,
                "vigil_amplifications": self._vigil_amplifications,
            },
            "models": self.model_loader.get_status(),
            "weights": self.scorer.get_weights(),
            "thresholds": self.scorer.get_thresholds(),
            "fallback": self.fallback.get_status(),
            "cache": self.get_cache_stats(),
        }

        # Add Phase 3 Vigil component status
        if self.vigil_enabled:
            status["vigil"] = self.get_vigil_config()

        # Add Phase 4 component status
        if self.phase4_enabled:
            status["phase4"] = {
                "consensus": self.get_consensus_config(),
                "conflict_detection": self.get_conflict_config(),
                "conflict_resolution": (
                    self.conflict_resolver.get_config()
                    if self.conflict_resolver
                    else None
                ),
                "explainability": (
                    self.explainability_generator.get_config()
                    if self.explainability_generator
                    else None
                ),
            }

        # Add Phase 5 component status
        if self.phase5_enabled:
            status["phase5"] = {
                "context_analysis": self.get_context_config(),
            }

        return status

    def get_model_info(self) -> List[Dict[str, Any]]:
        """
        Get information about loaded models.

        Returns:
            List of model info dictionaries
        """
        return [info.to_dict() for info in self.model_loader.get_model_info()]

    def is_ready(self) -> bool:
        """
        Check if engine is ready for analysis.

        Returns:
            True if at least BART is loaded and operational
        """
        return self.model_loader.is_ready() and self.fallback.is_operational()

    def get_health(self) -> Dict[str, Any]:
        """
        Get health check information.

        Returns:
            Health status for API endpoint
        """
        vigil_healthy = False
        if self.vigil_enabled and self._vigil_client:
            vigil_healthy = self._vigil_client.status not in (
                VigilStatus.CIRCUIT_OPEN,
                VigilStatus.UNAVAILABLE,
            )

        return {
            "status": "healthy" if self.is_ready() else "unhealthy",
            "ready": self.is_ready(),
            "degraded": self.fallback.is_degraded(),
            "models_loaded": self.model_loader._models_loaded,
            "total_models": len(self.model_loader._models),
            "cache_enabled": self.cache_enabled,
            "vigil_enabled": self.vigil_enabled,
            "vigil_healthy": vigil_healthy,
            "phase4_enabled": self.phase4_enabled,
            "phase5_enabled": self.phase5_enabled,
            "context_analysis_enabled": self.is_context_analysis_enabled(),
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.2.3 Compliance (Rule #1)
# =============================================================================


def create_decision_engine(
    config_manager: Optional["ConfigManager"] = None,
    auto_initialize: bool = False,
    async_inference: bool = True,
    cache_enabled: bool = True,
    alerter: Optional["DiscordAlerter"] = None,
    vigil_enabled: bool = True,
    phase4_enabled: bool = True,
    phase5_enabled: bool = True,
) -> EnsembleDecisionEngine:
    """
    Factory function for EnsembleDecisionEngine.

    Creates a fully configured decision engine with Phase 3 Vigil,
    Phase 4, and Phase 5 enhancements.

    Args:
        config_manager: Configuration manager instance
        auto_initialize: If True, load models immediately
        async_inference: Enable parallel model inference
        cache_enabled: Enable response caching
        alerter: Discord alerter for notifications
        vigil_enabled: Enable Phase 3 Vigil integration (default: True)
        phase4_enabled: Enable Phase 4 features (default: True)
        phase5_enabled: Enable Phase 5 context analysis (default: True)

    Returns:
        Configured EnsembleDecisionEngine instance

    Example:
        >>> engine = create_decision_engine(config_manager=config)
        >>> engine.initialize()
        >>> assessment = engine.analyze(
        ...     "I'm feeling really down today",
        ...     message_history=[...],  # Phase 5 context
        ... )
        >>> print(assessment.vigil)  # Phase 3 Vigil response
        >>> print(assessment.explanation)  # Phase 4 explanation
        >>> print(assessment.context_analysis)  # Phase 5 analysis
    """
    # Get settings from config
    perf_config = {}
    if config_manager is not None:
        perf_config = config_manager.get_performance_config() or {}
        async_inference = perf_config.get("async_inference", async_inference)
        cache_enabled = perf_config.get("cache_enabled", cache_enabled)

        # Check if Vigil is enabled in config
        vigil_config = config_manager.get_section("vigil") or {}
        vigil_enabled = vigil_config.get("enabled", vigil_enabled)

    cache_ttl = perf_config.get("cache_ttl", 300.0)
    cache_max_size = perf_config.get("cache_max_size", 1000)

    engine = EnsembleDecisionEngine(
        config_manager=config_manager,
        async_inference=async_inference,
        cache_enabled=cache_enabled,
        cache_ttl=cache_ttl,
        cache_max_size=cache_max_size,
        alerter=alerter,
        vigil_enabled=vigil_enabled,
        phase4_enabled=phase4_enabled,
        phase5_enabled=phase5_enabled,
    )

    if auto_initialize:
        engine.initialize()

    return engine


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "EnsembleDecisionEngine",
    "create_decision_engine",
    "CrisisAssessment",
    "RecommendedAction",
    "WarmupResult",
    "VigilResponse",  # Phase 3 Vigil
]
