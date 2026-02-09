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
Weighted Scoring System for Ash-NLP Ensemble Service
---
FILE VERSION: v5.1-4.5-4.5.3-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 4.5 - BART Label Optimization (scoring update)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Implement weighted ensemble scoring algorithm
- Combine model outputs using configured weights
- Apply irony dampening to reduce false positives
- Calculate final crisis score and confidence
- Map scores to severity levels

ALGORITHM:
1. Extract crisis signals from each model
2. Apply model weights to signals
3. Calculate base weighted score
4. Apply irony dampening factor
5. Calculate confidence from model agreement
6. Map final score to severity level
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from src.models import ModelResult, ModelRole

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.1-4.5-4.5.3-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Severity Levels
# =============================================================================


class CrisisSeverity(Enum):
    """Crisis severity levels for classification."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SAFE = "safe"

    @classmethod
    def from_score(cls, score: float, thresholds: Dict[str, float]) -> "CrisisSeverity":
        """
        Map score to severity using thresholds.

        Args:
            score: Crisis score (0.0 - 1.0)
            thresholds: Dictionary with critical, high, medium, low thresholds

        Returns:
            CrisisSeverity enum value
        """
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


# =============================================================================
# Scoring Data Classes
# =============================================================================


@dataclass
class ModelSignal:
    """
    Extracted signal from a single model.

    Attributes:
        model_name: Name of the source model
        raw_score: Original model confidence score
        crisis_signal: Extracted crisis-relevant signal (0.0 - 1.0)
        weight: Model weight in ensemble
        weighted_score: crisis_signal * weight
        label: Primary predicted label
        metadata: Additional model-specific data
    """

    model_name: str
    raw_score: float
    crisis_signal: float
    weight: float
    weighted_score: float
    label: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "model_name": self.model_name,
            "raw_score": self.raw_score,
            "crisis_signal": self.crisis_signal,
            "weight": self.weight,
            "weighted_score": self.weighted_score,
            "label": self.label,
            "metadata": self.metadata,
        }


@dataclass
class EnsembleScore:
    """
    Final ensemble scoring result.

    Attributes:
        crisis_score: Final weighted crisis score (0.0 - 1.0)
        confidence: Confidence in the assessment (0.0 - 1.0)
        severity: Mapped severity level
        signals: Individual model signals
        irony_dampening: Irony dampening factor applied
        base_score: Score before irony dampening
        crisis_detected: Whether crisis threshold was met
        requires_intervention: Whether immediate action needed
    """

    crisis_score: float
    confidence: float
    severity: CrisisSeverity
    signals: Dict[str, ModelSignal]
    irony_dampening: float
    base_score: float
    crisis_detected: bool
    requires_intervention: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "crisis_score": self.crisis_score,
            "confidence": self.confidence,
            "severity": self.severity.value,
            "crisis_detected": self.crisis_detected,
            "requires_intervention": self.requires_intervention,
            "irony_dampening": self.irony_dampening,
            "base_score": self.base_score,
            "signals": {
                name: signal.to_dict() for name, signal in self.signals.items()
            },
        }


# =============================================================================
# Weighted Scoring Calculator
# =============================================================================


class WeightedScorer:
    """
    Weighted Ensemble Scoring Calculator.

    Combines outputs from all ensemble models using configured weights
    to produce a final crisis assessment.

    Algorithm:
    1. Extract crisis signal from each model
    2. Apply model weights
    3. Calculate weighted base score
    4. Apply irony dampening
    5. Calculate confidence from agreement
    6. Map to severity level

    Clean Architecture v5.1 Compliance:
    - Factory function: create_weighted_scorer()
    - Configuration via ConfigManager
    """

    # Default weights (must sum to ~1.0, irony is modifier not additive)
    DEFAULT_WEIGHTS = {
        "bart": 0.50,
        "sentiment": 0.25,
        "irony": 0.15,  # Used as modifier weight, not additive
        "emotions": 0.10,
    }

    # Default thresholds
    DEFAULT_THRESHOLDS = {
        "critical": 0.85,
        "high": 0.70,
        "medium": 0.50,
        "low": 0.30,
    }

    # Phase 4.5: Critical signal threshold for crisis override
    # Labels with signal >= this threshold trigger critical severity override
    CRITICAL_SIGNAL_THRESHOLD = 0.90

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        thresholds: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize WeightedScorer.

        Args:
            weights: Model weights (bart, sentiment, irony, emotions)
            thresholds: Severity thresholds (critical, high, medium, low)
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self.thresholds = thresholds or self.DEFAULT_THRESHOLDS.copy()

        # Validate weights
        self._validate_weights()

        logger.info(f"📊 WeightedScorer initialized (weights: {self.weights})")

    def _validate_weights(self) -> None:
        """Validate that weights are sensible."""
        # Additive weights (excluding irony which is a modifier)
        additive_weights = (
            self.weights.get("bart", 0)
            + self.weights.get("sentiment", 0)
            + self.weights.get("emotions", 0)
        )

        if abs(additive_weights - 0.85) > 0.1:
            logger.warning(
                f"⚠️ Additive weights sum to {additive_weights:.2f}, "
                f"expected ~0.85 (bart + sentiment + emotions)"
            )

    # =========================================================================
    # Signal Extraction
    # =========================================================================

    def extract_bart_signal(self, result: ModelResult) -> ModelSignal:
        """
        Extract crisis signal from BART result.

        v5.1 Phase 4.5: Reads pre-computed crisis_signal from ModelResult.metadata.
        The BARTCrisisClassifier computes this during _process_output() using its
        label-to-signal mapping — same pattern as sentiment.

        Backward compatibility: Falls back to legacy tier-boosting heuristic
        if metadata["crisis_signal"] is not present (e.g., during rollback to
        v5.0 BART classifier).

        Args:
            result: ModelResult from BART classifier

        Returns:
            ModelSignal with extracted crisis information
        """
        if not result.success:
            return ModelSignal(
                model_name="bart",
                raw_score=0.0,
                crisis_signal=0.0,
                weight=self.weights.get("bart", 0.50),
                weighted_score=0.0,
                label="error",
                metadata={"error": result.error},
            )

        # v5.1 Phase 4.5: Read pre-computed crisis signal from zero-shot model
        if "crisis_signal" in result.metadata:
            crisis_signal = result.metadata["crisis_signal"]
            crisis_signal = max(0.0, min(1.0, crisis_signal))

            weight = self.weights.get("bart", 0.50)

            return ModelSignal(
                model_name="bart",
                raw_score=result.score,
                crisis_signal=crisis_signal,
                weight=weight,
                weighted_score=crisis_signal * weight,
                label=result.label,
                metadata=result.all_scores,
            )

        # v5.0 fallback: Legacy tier-boosting heuristic
        # Supports rollback to v5.0 BART classifier extending BaseModelWrapper
        logger.debug("BART result missing crisis_signal metadata, using legacy fallback")

        crisis_signal = result.score
        label_lower = result.label.lower()

        # Legacy hardcoded label sets for backward compatibility only
        legacy_critical = {"suicide ideation", "self-harm", "domestic violence"}
        legacy_high = {"panic attack", "severe depression", "substance abuse crisis"}
        legacy_safe = {"casual conversation", "positive sharing", "seeking information", "general discussion"}

        if label_lower in legacy_critical:
            crisis_signal = max(crisis_signal, 0.90)
        elif label_lower in legacy_high:
            crisis_signal = max(crisis_signal, 0.75)
        elif label_lower in legacy_safe:
            crisis_signal = 1.0 - result.score

        weight = self.weights.get("bart", 0.50)

        return ModelSignal(
            model_name="bart",
            raw_score=result.score,
            crisis_signal=crisis_signal,
            weight=weight,
            weighted_score=crisis_signal * weight,
            label=result.label,
            metadata={"all_scores": result.all_scores, "legacy_fallback": True},
        )

    def extract_sentiment_signal(self, result: ModelResult) -> ModelSignal:
        """
        Extract crisis signal from sentiment result.

        v5.1: Reads pre-computed crisis_signal from ModelResult.metadata.
        The SentimentZeroShotAnalyzer computes this during _process_output()
        using its label-to-signal mapping.

        Backward compatibility: Falls back to legacy pos/neg/neutral heuristic
        if metadata["crisis_signal"] is not present (e.g., during rollback to
        v5.0 Cardiff model).

        Args:
            result: ModelResult from sentiment analyzer

        Returns:
            ModelSignal with extracted crisis information
        """
        if not result.success:
            return ModelSignal(
                model_name="sentiment",
                raw_score=0.0,
                crisis_signal=0.0,
                weight=self.weights.get("sentiment", 0.25),
                weighted_score=0.0,
                label="error",
                metadata={"error": result.error},
            )

        # v5.1: Read pre-computed crisis signal from zero-shot model
        if "crisis_signal" in result.metadata:
            crisis_signal = result.metadata["crisis_signal"]
            crisis_signal = max(0.0, min(1.0, crisis_signal))

            weight = self.weights.get("sentiment", 0.25)

            return ModelSignal(
                model_name="sentiment",
                raw_score=result.score,
                crisis_signal=crisis_signal,
                weight=weight,
                weighted_score=crisis_signal * weight,
                label=result.label,
                metadata=result.all_scores,
            )

        # v5.0 fallback: Legacy pos/neg/neutral heuristic
        # Supports rollback to Cardiff text-classification model
        negative_score = result.all_scores.get("negative", 0.0)
        neutral_score = result.all_scores.get("neutral", 0.0)
        positive_score = result.all_scores.get("positive", 0.0)

        crisis_signal = (
            negative_score * 1.0 + neutral_score * 0.2 - positive_score * 0.3
        )
        crisis_signal = max(0.0, min(1.0, crisis_signal))

        weight = self.weights.get("sentiment", 0.25)

        return ModelSignal(
            model_name="sentiment",
            raw_score=result.score,
            crisis_signal=crisis_signal,
            weight=weight,
            weighted_score=crisis_signal * weight,
            label=result.label,
            metadata={
                "negative": negative_score,
                "neutral": neutral_score,
                "positive": positive_score,
                "legacy_fallback": True,
            },
        )

    def extract_irony_signal(self, result: ModelResult) -> ModelSignal:
        """
        Extract dampening factor from irony result.

        Irony REDUCES crisis signals to prevent false positives
        from sarcastic messages.

        Args:
            result: ModelResult from irony detector

        Returns:
            ModelSignal with dampening factor
        """
        if not result.success:
            # No dampening if model fails
            return ModelSignal(
                model_name="irony",
                raw_score=1.0,
                crisis_signal=1.0,  # 1.0 = no dampening
                weight=self.weights.get("irony", 0.15),
                weighted_score=1.0,
                label="error",
                metadata={"error": result.error, "dampening": 1.0},
            )

        irony_score = result.all_scores.get("irony", 0.0)

        # Calculate dampening factor
        # High irony → low dampening factor → reduced crisis score
        # irony_score = 0.0 → dampening = 1.0 (no reduction)
        # irony_score = 1.0 → dampening = 0.1 (90% reduction)
        dampening = 1.0 - (irony_score * 0.9)
        dampening = max(0.1, dampening)  # Never fully eliminate

        return ModelSignal(
            model_name="irony",
            raw_score=result.score,
            crisis_signal=dampening,  # Used as multiplier
            weight=self.weights.get("irony", 0.15),
            weighted_score=dampening,
            label=result.label,
            metadata={
                "irony_score": irony_score,
                "dampening_factor": dampening,
            },
        )

    def extract_emotions_signal(self, result: ModelResult) -> ModelSignal:
        """
        Extract crisis signal from emotions result.

        Certain emotions (grief, fear, sadness) indicate crisis.

        Args:
            result: ModelResult from emotions classifier

        Returns:
            ModelSignal with extracted crisis information
        """
        if not result.success:
            return ModelSignal(
                model_name="emotions",
                raw_score=0.0,
                crisis_signal=0.0,
                weight=self.weights.get("emotions", 0.10),
                weighted_score=0.0,
                label="error",
                metadata={"error": result.error},
            )

        scores = result.all_scores

        # Crisis-indicating emotions
        crisis_emotions = {
            "grief": 1.0,
            "sadness": 0.9,
            "fear": 0.9,
            "nervousness": 0.7,
            "remorse": 0.8,
            "anger": 0.6,
            "disappointment": 0.5,
            "disgust": 0.5,
        }

        # Positive emotions (reduce signal)
        positive_emotions = {
            "joy": -0.8,
            "love": -0.7,
            "gratitude": -0.6,
            "relief": -0.5,
            "optimism": -0.6,
            "amusement": -0.5,
        }

        # Calculate weighted emotion signal
        crisis_signal = 0.0

        for emotion, multiplier in crisis_emotions.items():
            crisis_signal += scores.get(emotion, 0.0) * multiplier

        for emotion, multiplier in positive_emotions.items():
            crisis_signal += scores.get(emotion, 0.0) * multiplier

        crisis_signal = max(0.0, min(1.0, crisis_signal))

        weight = self.weights.get("emotions", 0.10)

        # Get top emotions for metadata
        top_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

        return ModelSignal(
            model_name="emotions",
            raw_score=result.score,
            crisis_signal=crisis_signal,
            weight=weight,
            weighted_score=crisis_signal * weight,
            label=result.label,
            metadata={"top_emotions": dict(top_emotions)},
        )

    # =========================================================================
    # Main Scoring Methods
    # =========================================================================

    def calculate_score(
        self,
        bart_result: Optional[ModelResult] = None,
        sentiment_result: Optional[ModelResult] = None,
        irony_result: Optional[ModelResult] = None,
        emotions_result: Optional[ModelResult] = None,
    ) -> EnsembleScore:
        """
        Calculate final ensemble crisis score.

        Args:
            bart_result: Result from BART classifier
            sentiment_result: Result from sentiment analyzer
            irony_result: Result from irony detector
            emotions_result: Result from emotions classifier

        Returns:
            EnsembleScore with final assessment
        """
        signals: Dict[str, ModelSignal] = {}

        # Extract signals from available models
        if bart_result:
            signals["bart"] = self.extract_bart_signal(bart_result)

        if sentiment_result:
            signals["sentiment"] = self.extract_sentiment_signal(sentiment_result)

        if irony_result:
            signals["irony"] = self.extract_irony_signal(irony_result)

        if emotions_result:
            signals["emotions"] = self.extract_emotions_signal(emotions_result)

        # Calculate base weighted score (without irony)
        base_score = 0.0
        total_weight = 0.0

        for name, signal in signals.items():
            if name != "irony":  # Irony is a modifier, not additive
                base_score += signal.weighted_score
                total_weight += signal.weight

        # Normalize if not all models available
        if total_weight > 0 and total_weight < 0.85:
            base_score = base_score / total_weight * 0.85

        # Apply irony dampening
        irony_dampening = 1.0
        if "irony" in signals:
            irony_dampening = signals["irony"].crisis_signal

        final_score = base_score * irony_dampening
        final_score = max(0.0, min(1.0, final_score))

        # Calculate confidence based on model agreement
        confidence = self._calculate_confidence(signals)

        # Determine severity
        severity = CrisisSeverity.from_score(final_score, self.thresholds)

        # Check for critical signal override
        # Phase 4.5: Uses signal threshold instead of label membership
        if "bart" in signals:
            bart_signal = signals["bart"].crisis_signal
            if bart_signal >= self.CRITICAL_SIGNAL_THRESHOLD and final_score >= 0.5:
                severity = CrisisSeverity.CRITICAL

        # Determine if crisis detected and intervention needed
        crisis_detected = severity in (
            CrisisSeverity.CRITICAL,
            CrisisSeverity.HIGH,
            CrisisSeverity.MEDIUM,
        )

        requires_intervention = severity in (
            CrisisSeverity.CRITICAL,
            CrisisSeverity.HIGH,
        )

        return EnsembleScore(
            crisis_score=final_score,
            confidence=confidence,
            severity=severity,
            signals=signals,
            irony_dampening=irony_dampening,
            base_score=base_score,
            crisis_detected=crisis_detected,
            requires_intervention=requires_intervention,
        )

    def _calculate_confidence(self, signals: Dict[str, ModelSignal]) -> float:
        """
        Calculate confidence based on model agreement.

        Higher confidence when models agree on direction.

        Args:
            signals: Dictionary of model signals

        Returns:
            Confidence score (0.0 - 1.0)
        """
        if not signals:
            return 0.0

        # Get crisis signals (excluding irony which is different)
        crisis_signals = [
            s.crisis_signal for name, s in signals.items() if name != "irony"
        ]

        if not crisis_signals:
            return 0.0

        # Calculate agreement (inverse of variance)
        mean_signal = sum(crisis_signals) / len(crisis_signals)
        variance = sum((s - mean_signal) ** 2 for s in crisis_signals) / len(
            crisis_signals
        )

        # Low variance = high agreement = high confidence
        # Max variance for 0-1 range is 0.25
        agreement = 1.0 - (variance / 0.25)
        agreement = max(0.0, min(1.0, agreement))

        # Weight by number of models available
        model_coverage = len(crisis_signals) / 3  # 3 additive models expected

        confidence = agreement * model_coverage

        return max(0.0, min(1.0, confidence))

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Update model weights."""
        self.weights.update(weights)
        self._validate_weights()
        logger.info(f"Updated weights: {self.weights}")

    def set_thresholds(self, thresholds: Dict[str, float]) -> None:
        """Update severity thresholds."""
        self.thresholds.update(thresholds)
        logger.info(f"Updated thresholds: {self.thresholds}")

    def get_weights(self) -> Dict[str, float]:
        """Get current weights."""
        return self.weights.copy()

    def get_thresholds(self) -> Dict[str, float]:
        """Get current thresholds."""
        return self.thresholds.copy()


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_weighted_scorer(
    config_manager: Optional["ConfigManager"] = None,
    weights: Optional[Dict[str, float]] = None,
    thresholds: Optional[Dict[str, float]] = None,
) -> WeightedScorer:
    """
    Factory function for WeightedScorer.

    Creates a configured scorer using ConfigManager settings.

    Args:
        config_manager: Configuration manager instance
        weights: Override weights (optional)
        thresholds: Override thresholds (optional)

    Returns:
        Configured WeightedScorer instance

    Example:
        >>> scorer = create_weighted_scorer(config_manager=config)
        >>> score = scorer.calculate_score(bart_result, sentiment_result, ...)
    """
    final_weights = WeightedScorer.DEFAULT_WEIGHTS.copy()
    final_thresholds = WeightedScorer.DEFAULT_THRESHOLDS.copy()

    # Load from config manager
    if config_manager is not None:
        # Get model weights
        config_weights = config_manager.get_model_weights()
        if config_weights:
            final_weights.update(config_weights)

        # Get thresholds
        config_thresholds = config_manager.get_thresholds()
        if config_thresholds:
            final_thresholds.update(config_thresholds)

    # Apply explicit overrides
    if weights:
        final_weights.update(weights)

    if thresholds:
        final_thresholds.update(thresholds)

    return WeightedScorer(
        weights=final_weights,
        thresholds=final_thresholds,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "WeightedScorer",
    "create_weighted_scorer",
    "CrisisSeverity",
    "ModelSignal",
    "EnsembleScore",
]
