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
Result Aggregator for Ash-NLP Ensemble Service
---
FILE VERSION: v5.0-4-3.1-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 Step 3 - Result Aggregation
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Aggregate all ensemble analysis results into comprehensive output
- Include: crisis_assessment, model_results, consensus, explanation, performance
- Provide structured output for API responses
- Support backward compatibility with Phase 3 response format
- Calculate crisis levels, agreement levels, intervention requirements

DESIGN PHILOSOPHY:
Comprehensive output that enables:
- Clear crisis status determination
- Full audit trail of model contributions
- Human-readable explanations
- Performance monitoring
"""

import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .consensus import ConsensusResult, AgreementLevel
from .conflict_detector import ConflictReport
from .conflict_resolver import ResolutionResult

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-4-3.1-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Crisis Levels
# =============================================================================


class CrisisLevel(Enum):
    """Crisis severity levels for final assessment."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SAFE = "safe"

    @classmethod
    def from_score(cls, score: float, thresholds: Dict[str, float]) -> "CrisisLevel":
        """Map score to crisis level using thresholds."""
        if score >= thresholds.get("critical", 0.85):
            return cls.CRITICAL
        elif score >= thresholds.get("high", 0.70):
            return cls.HIGH
        elif score >= thresholds.get("medium", 0.50):
            return cls.MEDIUM
        elif score >= thresholds.get("low", 0.30):
            return cls.LOW
        else:
            return cls.SAFE


class InterventionPriority(Enum):
    """Priority levels for intervention recommendations."""

    IMMEDIATE = "immediate"  # Critical - needs immediate attention
    HIGH = "high"  # High priority - respond soon
    STANDARD = "standard"  # Medium priority - standard monitoring
    LOW = "low"  # Low priority - passive monitoring
    NONE = "none"  # Safe - no intervention needed


# =============================================================================
# Model Result Container
# =============================================================================


@dataclass
class ModelResultSummary:
    """Summary of a single model's contribution."""

    model_name: str
    label: str
    score: float
    confidence: float
    weight: float
    contribution: float
    crisis_signal: float
    top_labels: List[Dict[str, float]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "model_name": self.model_name,
            "label": self.label,
            "score": round(self.score, 4),
            "confidence": round(self.confidence, 4),
            "weight": round(self.weight, 4),
            "contribution": round(self.contribution, 4),
            "crisis_signal": round(self.crisis_signal, 4),
            "top_labels": self.top_labels,
            "metadata": self.metadata,
        }


# =============================================================================
# Aggregated Result
# =============================================================================


@dataclass
class AggregatedResult:
    """
    Complete aggregated analysis result.

    This is the comprehensive output from the ensemble system,
    containing all information needed for API response and audit.

    Attributes:
        ensemble_version: Version of the ensemble system
        timestamp: ISO-8601 timestamp
        request_id: Unique request identifier
        
        # Crisis Assessment
        crisis_score: Final crisis score (0.0-1.0)
        crisis_level: Severity level
        confidence: Confidence in assessment
        requires_intervention: Whether action is needed
        intervention_priority: Priority level for response
        
        # Model Results
        model_results: Individual model summaries
        models_used: List of models that contributed
        
        # Consensus Analysis
        consensus: Consensus algorithm result
        
        # Conflict Analysis
        conflict_report: Conflict detection result
        resolution: Conflict resolution result
        
        # Explanation (populated by ExplainabilityGenerator)
        explanation: Human-readable explanation dict
        
        # Performance
        processing_time_ms: Total processing time
        per_model_latency: Latency per model
        cached: Whether result was from cache
        
        # System State
        is_degraded: Whether system is degraded
        degradation_reason: Why system is degraded
    """

    # Identifiers
    ensemble_version: str = "v5.0"
    timestamp: str = ""
    request_id: str = ""

    # Crisis Assessment
    crisis_score: float = 0.0
    crisis_level: CrisisLevel = CrisisLevel.SAFE
    confidence: float = 0.0
    requires_intervention: bool = False
    intervention_priority: InterventionPriority = InterventionPriority.NONE

    # Model Results
    model_results: Dict[str, ModelResultSummary] = field(default_factory=dict)
    models_used: List[str] = field(default_factory=list)

    # Consensus
    consensus: Optional[ConsensusResult] = None

    # Conflict Analysis
    conflict_report: Optional[ConflictReport] = None
    resolution: Optional[ResolutionResult] = None

    # Explanation
    explanation: Dict[str, Any] = field(default_factory=dict)

    # Performance
    processing_time_ms: float = 0.0
    per_model_latency: Dict[str, float] = field(default_factory=dict)
    cached: bool = False

    # System State
    is_degraded: bool = False
    degradation_reason: str = ""

    # Original message (for internal use)
    message: str = ""

    def __post_init__(self):
        """Set defaults for timestamp and request_id."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"
        if not self.request_id:
            self.request_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to complete dictionary for API response."""
        return {
            "ensemble_version": self.ensemble_version,
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "crisis_assessment": {
                "crisis_score": round(self.crisis_score, 4),
                "crisis_level": self.crisis_level.value,
                "confidence": round(self.confidence, 4),
                "requires_intervention": self.requires_intervention,
                "intervention_priority": self.intervention_priority.value,
            },
            "model_results": {
                name: result.to_dict()
                for name, result in self.model_results.items()
            },
            "models_used": self.models_used,
            "consensus": self.consensus.to_dict() if self.consensus else None,
            "conflict_analysis": {
                "report": self.conflict_report.to_dict() if self.conflict_report else None,
                "resolution": self.resolution.to_dict() if self.resolution else None,
            },
            "explanation": self.explanation,
            "performance": {
                "total_latency_ms": round(self.processing_time_ms, 2),
                "per_model_latency": {
                    k: round(v, 2) for k, v in self.per_model_latency.items()
                },
                "cached": self.cached,
            },
            "system_state": {
                "is_degraded": self.is_degraded,
                "degradation_reason": self.degradation_reason,
            },
        }

    def to_legacy_dict(self) -> Dict[str, Any]:
        """
        Convert to Phase 3 compatible format for backward compatibility.

        Returns simplified format matching CrisisAssessment.to_dict()
        """
        return {
            "crisis_detected": self.requires_intervention or self.crisis_level in (
                CrisisLevel.CRITICAL, CrisisLevel.HIGH, CrisisLevel.MEDIUM
            ),
            "severity": self.crisis_level.value,
            "confidence": round(self.confidence, 4),
            "crisis_score": round(self.crisis_score, 4),
            "requires_intervention": self.requires_intervention,
            "recommended_action": self._get_recommended_action(),
            "signals": {
                name: {
                    "label": r.label,
                    "score": round(r.score, 4),
                    "crisis_signal": round(r.crisis_signal, 4),
                }
                for name, r in self.model_results.items()
            },
            "processing_time_ms": round(self.processing_time_ms, 2),
            "models_used": self.models_used,
            "is_degraded": self.is_degraded,
            "cached": self.cached,
        }

    def _get_recommended_action(self) -> str:
        """Get recommended action string for legacy format."""
        mapping = {
            InterventionPriority.IMMEDIATE: "immediate_outreach",
            InterventionPriority.HIGH: "priority_response",
            InterventionPriority.STANDARD: "standard_monitoring",
            InterventionPriority.LOW: "passive_monitoring",
            InterventionPriority.NONE: "none",
        }
        return mapping.get(self.intervention_priority, "none")


# =============================================================================
# Result Aggregator
# =============================================================================


class ResultAggregator:
    """
    Result Aggregator for Ensemble Analysis.

    Combines outputs from all ensemble components into
    a comprehensive, structured result.

    Components Aggregated:
    - Model results (from ModelWrappers)
    - Consensus analysis (from ConsensusSelector)
    - Conflict detection (from ConflictDetector)
    - Conflict resolution (from ConflictResolver)
    - Explanation (from ExplainabilityGenerator)
    - Performance metrics

    Clean Architecture v5.1 Compliance:
    - Factory function: create_result_aggregator()
    - Configuration via ConfigManager
    """

    # Default thresholds
    DEFAULT_THRESHOLDS = {
        "critical": 0.85,
        "high": 0.70,
        "medium": 0.50,
        "low": 0.30,
    }

    def __init__(
        self,
        thresholds: Optional[Dict[str, float]] = None,
        weights: Optional[Dict[str, float]] = None,
        include_legacy_format: bool = True,
    ):
        """
        Initialize ResultAggregator.

        Args:
            thresholds: Crisis level thresholds
            weights: Model weights for contribution calculation
            include_legacy_format: Include backward-compatible fields
        """
        self.thresholds = thresholds or self.DEFAULT_THRESHOLDS.copy()
        self.weights = weights or {
            "bart": 0.50,
            "sentiment": 0.25,
            "irony": 0.15,
            "emotions": 0.10,
        }
        self.include_legacy_format = include_legacy_format

        logger.info("📊 ResultAggregator initialized")

    def aggregate(
        self,
        model_signals: Dict[str, Any],
        consensus_result: Optional[ConsensusResult] = None,
        conflict_report: Optional[ConflictReport] = None,
        resolution_result: Optional[ResolutionResult] = None,
        processing_time_ms: float = 0.0,
        per_model_latency: Optional[Dict[str, float]] = None,
        is_degraded: bool = False,
        degradation_reason: str = "",
        message: str = "",
        cached: bool = False,
    ) -> AggregatedResult:
        """
        Aggregate all analysis components into final result.

        Args:
            model_signals: Raw signals from each model
            consensus_result: Result from consensus algorithm
            conflict_report: Result from conflict detection
            resolution_result: Result from conflict resolution
            processing_time_ms: Total processing time
            per_model_latency: Per-model latency dict
            is_degraded: Whether system is degraded
            degradation_reason: Degradation reason
            message: Original message analyzed
            cached: Whether result was cached

        Returns:
            AggregatedResult with complete analysis
        """
        # Build model result summaries
        model_results = self._build_model_results(model_signals)
        models_used = list(model_results.keys())

        # Determine final crisis score
        if resolution_result:
            crisis_score = resolution_result.resolved_score
        elif consensus_result:
            crisis_score = consensus_result.crisis_score
        else:
            # Fallback to simple average
            scores = [r.crisis_signal for r in model_results.values()]
            crisis_score = sum(scores) / len(scores) if scores else 0.0

        # Determine crisis level
        crisis_level = CrisisLevel.from_score(crisis_score, self.thresholds)

        # Determine confidence
        if consensus_result:
            confidence = consensus_result.confidence
        else:
            confidence = self._calculate_confidence(model_results)

        # Determine intervention requirements
        requires_intervention = crisis_level in (
            CrisisLevel.CRITICAL,
            CrisisLevel.HIGH,
        )

        # Determine intervention priority
        intervention_priority = self._determine_priority(
            crisis_level, conflict_report, resolution_result
        )

        # Build aggregated result
        result = AggregatedResult(
            ensemble_version="v5.0",
            crisis_score=crisis_score,
            crisis_level=crisis_level,
            confidence=confidence,
            requires_intervention=requires_intervention,
            intervention_priority=intervention_priority,
            model_results=model_results,
            models_used=models_used,
            consensus=consensus_result,
            conflict_report=conflict_report,
            resolution=resolution_result,
            processing_time_ms=processing_time_ms,
            per_model_latency=per_model_latency or {},
            cached=cached,
            is_degraded=is_degraded,
            degradation_reason=degradation_reason,
            message=message,
        )

        return result

    def _build_model_results(
        self, model_signals: Dict[str, Any]
    ) -> Dict[str, ModelResultSummary]:
        """
        Build ModelResultSummary for each model.

        Args:
            model_signals: Raw signals dict from EnsembleScore

        Returns:
            Dict of model_name -> ModelResultSummary
        """
        results = {}

        for model_name, signal in model_signals.items():
            weight = self.weights.get(model_name, 0.0)
            crisis_signal = signal.get("crisis_signal", 0.0)

            # Calculate contribution
            contribution = crisis_signal * weight

            # Extract top labels if available
            top_labels = []
            if "metadata" in signal:
                metadata = signal["metadata"]
                if "all_scores" in metadata:
                    # Sort scores and take top 3
                    sorted_scores = sorted(
                        metadata["all_scores"].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:3]
                    top_labels = [
                        {"label": label, "score": score}
                        for label, score in sorted_scores
                    ]
                elif "top_emotions" in metadata:
                    sorted_emotions = sorted(
                        metadata["top_emotions"].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:3]
                    top_labels = [
                        {"label": emotion, "score": score}
                        for emotion, score in sorted_emotions
                    ]

            results[model_name] = ModelResultSummary(
                model_name=model_name,
                label=signal.get("label", ""),
                score=signal.get("raw_score", signal.get("score", 0.0)),
                confidence=signal.get("confidence", signal.get("score", 0.0)),
                weight=weight,
                contribution=contribution,
                crisis_signal=crisis_signal,
                top_labels=top_labels,
                metadata=signal.get("metadata", {}),
            )

        return results

    def _calculate_confidence(
        self, model_results: Dict[str, ModelResultSummary]
    ) -> float:
        """Calculate confidence from model agreement."""
        if not model_results:
            return 0.0

        signals = [r.crisis_signal for r in model_results.values()]
        if len(signals) < 2:
            return 0.5

        mean = sum(signals) / len(signals)
        variance = sum((s - mean) ** 2 for s in signals) / len(signals)

        # Low variance = high confidence
        max_variance = 0.25
        confidence = 1.0 - (variance / max_variance)

        return max(0.0, min(1.0, confidence))

    def _determine_priority(
        self,
        crisis_level: CrisisLevel,
        conflict_report: Optional[ConflictReport],
        resolution_result: Optional[ResolutionResult],
    ) -> InterventionPriority:
        """Determine intervention priority."""
        # Base priority on crisis level
        base_priorities = {
            CrisisLevel.CRITICAL: InterventionPriority.IMMEDIATE,
            CrisisLevel.HIGH: InterventionPriority.HIGH,
            CrisisLevel.MEDIUM: InterventionPriority.STANDARD,
            CrisisLevel.LOW: InterventionPriority.LOW,
            CrisisLevel.SAFE: InterventionPriority.NONE,
        }

        priority = base_priorities.get(crisis_level, InterventionPriority.NONE)

        # Upgrade priority if review required
        if resolution_result and resolution_result.requires_review:
            if priority == InterventionPriority.STANDARD:
                priority = InterventionPriority.HIGH
            elif priority == InterventionPriority.LOW:
                priority = InterventionPriority.STANDARD

        return priority

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def identify_primary_indicators(
        self, model_results: Dict[str, ModelResultSummary]
    ) -> List[str]:
        """
        Identify primary crisis indicators from model results.

        Args:
            model_results: Model result summaries

        Returns:
            List of primary indicator strings
        """
        indicators = []

        for model_name, result in model_results.items():
            if result.crisis_signal > 0.5:
                # Add primary label
                if result.label:
                    indicators.append(result.label)

                # Add top labels with high scores
                for label_info in result.top_labels[:2]:
                    if label_info.get("score", 0) > 0.5:
                        label = label_info.get("label", "")
                        if label and label not in indicators:
                            indicators.append(label)

        return indicators[:6]  # Limit to 6 indicators

    def set_thresholds(self, thresholds: Dict[str, float]) -> None:
        """Update crisis level thresholds."""
        self.thresholds.update(thresholds)
        logger.info(f"Updated thresholds: {self.thresholds}")

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Update model weights."""
        self.weights.update(weights)
        logger.info(f"Updated weights: {self.weights}")


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_result_aggregator(
    config_manager: Optional["ConfigManager"] = None,
    thresholds: Optional[Dict[str, float]] = None,
    weights: Optional[Dict[str, float]] = None,
) -> ResultAggregator:
    """
    Factory function for ResultAggregator.

    Creates a configured result aggregator.

    Args:
        config_manager: Configuration manager instance
        thresholds: Override thresholds
        weights: Override weights

    Returns:
        Configured ResultAggregator instance

    Example:
        >>> aggregator = create_result_aggregator(config_manager=config)
        >>> result = aggregator.aggregate(signals, consensus, conflicts, ...)
    """
    final_thresholds = ResultAggregator.DEFAULT_THRESHOLDS.copy()
    final_weights = {
        "bart": 0.50,
        "sentiment": 0.25,
        "irony": 0.15,
        "emotions": 0.10,
    }

    # Load from config manager
    if config_manager is not None:
        config_thresholds = config_manager.get_thresholds()
        if config_thresholds:
            final_thresholds.update(config_thresholds)

        config_weights = config_manager.get_model_weights()
        if config_weights:
            final_weights.update(config_weights)

    # Apply explicit overrides
    if thresholds:
        final_thresholds.update(thresholds)
    if weights:
        final_weights.update(weights)

    return ResultAggregator(
        thresholds=final_thresholds,
        weights=final_weights,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "CrisisLevel",
    "InterventionPriority",
    # Data classes
    "ModelResultSummary",
    "AggregatedResult",
    # Aggregator class
    "ResultAggregator",
    "create_result_aggregator",
]
