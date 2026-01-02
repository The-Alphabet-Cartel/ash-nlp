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
Conflict Detection for Ash-NLP Ensemble Service
---
FILE VERSION: v5.0-4-2.1-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 Step 2 - Conflict Detection
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Detect disagreements between ensemble models
- Identify conflict types:
  - Score Disagreement: Max-min score > threshold
  - Irony-Sentiment Conflict: Positive sentiment + irony detected
  - Emotion-Crisis Mismatch: High crisis but no crisis emotions
  - Label Disagreement: Models predict different crisis types
- Provide severity classification for conflicts
- Support Discord alerting for high-severity conflicts

DESIGN PHILOSOPHY:
Conflict detection enables:
- Better understanding of model agreement
- Flagging ambiguous cases for human review
- Identifying potential false positives/negatives
- Improving model calibration over time
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-4-2.1-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Conflict Types and Severity
# =============================================================================


class ConflictType(Enum):
    """Types of conflicts that can be detected between models."""

    SCORE_DISAGREEMENT = "score_disagreement"
    IRONY_SENTIMENT_CONFLICT = "irony_sentiment_conflict"
    EMOTION_CRISIS_MISMATCH = "emotion_crisis_mismatch"
    LABEL_DISAGREEMENT = "label_disagreement"


class ConflictSeverity(Enum):
    """Severity levels for detected conflicts."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# =============================================================================
# Conflict Data Classes
# =============================================================================


@dataclass
class DetectedConflict:
    """
    A single detected conflict between models.

    Attributes:
        conflict_type: Type of conflict detected
        severity: Severity level of the conflict
        description: Human-readable description
        involved_models: Models involved in the conflict
        details: Additional conflict-specific details
    """

    conflict_type: ConflictType
    severity: ConflictSeverity
    description: str
    involved_models: List[str]
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "conflict_type": self.conflict_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "involved_models": self.involved_models,
            "details": self.details,
        }


@dataclass
class ConflictReport:
    """
    Complete conflict analysis report.

    Attributes:
        has_conflicts: Whether any conflicts were detected
        conflict_count: Total number of conflicts
        conflicts: List of detected conflicts
        highest_severity: Most severe conflict level
        requires_review: Whether human review is recommended
        summary: Brief summary of conflict analysis
    """

    has_conflicts: bool
    conflict_count: int
    conflicts: List[DetectedConflict]
    highest_severity: Optional[ConflictSeverity]
    requires_review: bool
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "has_conflicts": self.has_conflicts,
            "conflict_count": self.conflict_count,
            "conflicts": [c.to_dict() for c in self.conflicts],
            "highest_severity": self.highest_severity.value if self.highest_severity else None,
            "requires_review": self.requires_review,
            "summary": self.summary,
        }


# =============================================================================
# Model Signal Container
# =============================================================================


@dataclass
class ModelSignals:
    """
    Container for all model signals used in conflict detection.

    Attributes:
        bart_score: BART crisis signal (0.0-1.0)
        bart_label: BART primary label
        bart_all_scores: All BART label scores
        sentiment_score: Sentiment crisis signal
        sentiment_label: Sentiment label (positive/negative/neutral)
        sentiment_all_scores: All sentiment scores
        irony_score: Irony dampening factor
        irony_detected: Whether irony was detected
        irony_confidence: Irony detection confidence
        emotions_score: Emotions crisis signal
        emotions_top: Top detected emotions
        emotions_all_scores: All emotion scores
    """

    # BART signals
    bart_score: float = 0.0
    bart_label: str = ""
    bart_all_scores: Dict[str, float] = field(default_factory=dict)

    # Sentiment signals
    sentiment_score: float = 0.0
    sentiment_label: str = ""
    sentiment_all_scores: Dict[str, float] = field(default_factory=dict)

    # Irony signals
    irony_score: float = 1.0  # 1.0 = no irony (dampening factor)
    irony_detected: bool = False
    irony_confidence: float = 0.0

    # Emotions signals
    emotions_score: float = 0.0
    emotions_top: Dict[str, float] = field(default_factory=dict)
    emotions_all_scores: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_ensemble_signals(
        cls, signals: Dict[str, Any]
    ) -> "ModelSignals":
        """
        Create ModelSignals from ensemble signal dictionary.

        Args:
            signals: Dictionary with model signals from EnsembleScore

        Returns:
            ModelSignals instance
        """
        instance = cls()

        # Extract BART
        if "bart" in signals:
            bart = signals["bart"]
            instance.bart_score = bart.get("crisis_signal", 0.0)
            instance.bart_label = bart.get("label", "")
            instance.bart_all_scores = bart.get("metadata", {}).get("all_scores", {})

        # Extract sentiment
        if "sentiment" in signals:
            sentiment = signals["sentiment"]
            instance.sentiment_score = sentiment.get("crisis_signal", 0.0)
            instance.sentiment_label = sentiment.get("label", "")
            instance.sentiment_all_scores = sentiment.get("metadata", {})

        # Extract irony
        if "irony" in signals:
            irony = signals["irony"]
            instance.irony_score = irony.get("crisis_signal", 1.0)
            instance.irony_detected = irony.get("metadata", {}).get("irony_score", 0.0) > 0.5
            instance.irony_confidence = irony.get("metadata", {}).get("irony_score", 0.0)

        # Extract emotions
        if "emotions" in signals:
            emotions = signals["emotions"]
            instance.emotions_score = emotions.get("crisis_signal", 0.0)
            instance.emotions_top = emotions.get("metadata", {}).get("top_emotions", {})
            instance.emotions_all_scores = emotions.get("metadata", {})

        return instance


# =============================================================================
# Conflict Detector
# =============================================================================


class ConflictDetector:
    """
    Conflict Detector for Ensemble Model Disagreements.

    Analyzes model outputs to detect various types of conflicts
    that may indicate ambiguous or challenging cases.

    Conflict Types:
    1. Score Disagreement: Large variance in crisis scores
    2. Irony-Sentiment Conflict: Positive sentiment + irony detected
    3. Emotion-Crisis Mismatch: High crisis but no crisis emotions
    4. Label Disagreement: Different crisis type predictions

    Clean Architecture v5.1 Compliance:
    - Factory function: create_conflict_detector()
    - Configuration via ConfigManager
    """

    # Crisis-indicating emotions
    CRISIS_EMOTIONS: Set[str] = {
        "grief",
        "sadness",
        "fear",
        "nervousness",
        "remorse",
        "anger",
        "disappointment",
        "disgust",
    }

    # Primary crisis labels from BART
    PRIMARY_CRISIS_LABELS: Set[str] = {
        "suicide ideation",
        "self-harm",
        "domestic violence",
        "panic attack",
        "severe depression",
        "substance abuse crisis",
    }

    def __init__(
        self,
        score_disagreement_threshold: float = 0.4,
        irony_detection_threshold: float = 0.5,
        emotion_crisis_threshold: float = 0.3,
        enabled_conflict_types: Optional[Set[ConflictType]] = None,
    ):
        """
        Initialize ConflictDetector.

        Args:
            score_disagreement_threshold: Max-min score difference for conflict
            irony_detection_threshold: Irony confidence for conflict
            emotion_crisis_threshold: Min crisis emotion score expected
            enabled_conflict_types: Which conflict types to check (None = all)
        """
        self.score_disagreement_threshold = score_disagreement_threshold
        self.irony_detection_threshold = irony_detection_threshold
        self.emotion_crisis_threshold = emotion_crisis_threshold

        self.enabled_conflict_types = enabled_conflict_types or set(ConflictType)

        logger.info(
            f"🔍 ConflictDetector initialized "
            f"(score_threshold={score_disagreement_threshold}, "
            f"irony_threshold={irony_detection_threshold})"
        )

    def detect_conflicts(
        self,
        model_signals: ModelSignals,
        crisis_scores: Dict[str, float],
    ) -> ConflictReport:
        """
        Detect all conflicts in model outputs.

        Args:
            model_signals: Complete model signals
            crisis_scores: Dict of model_name -> crisis_signal

        Returns:
            ConflictReport with all detected conflicts
        """
        conflicts: List[DetectedConflict] = []

        # Check each enabled conflict type
        if ConflictType.SCORE_DISAGREEMENT in self.enabled_conflict_types:
            conflict = self._detect_score_disagreement(crisis_scores)
            if conflict:
                conflicts.append(conflict)

        if ConflictType.IRONY_SENTIMENT_CONFLICT in self.enabled_conflict_types:
            conflict = self._detect_irony_sentiment_conflict(model_signals)
            if conflict:
                conflicts.append(conflict)

        if ConflictType.EMOTION_CRISIS_MISMATCH in self.enabled_conflict_types:
            conflict = self._detect_emotion_crisis_mismatch(
                model_signals, crisis_scores
            )
            if conflict:
                conflicts.append(conflict)

        if ConflictType.LABEL_DISAGREEMENT in self.enabled_conflict_types:
            conflict = self._detect_label_disagreement(model_signals)
            if conflict:
                conflicts.append(conflict)

        # Build report
        has_conflicts = len(conflicts) > 0

        # Determine highest severity
        highest_severity = None
        if conflicts:
            severity_order = {
                ConflictSeverity.HIGH: 3,
                ConflictSeverity.MEDIUM: 2,
                ConflictSeverity.LOW: 1,
            }
            highest_severity = max(
                conflicts, key=lambda c: severity_order.get(c.severity, 0)
            ).severity

        # Requires review if any high severity or multiple conflicts
        requires_review = (
            highest_severity == ConflictSeverity.HIGH or len(conflicts) >= 2
        )

        # Build summary
        if not has_conflicts:
            summary = "No conflicts detected - models are in agreement"
        elif len(conflicts) == 1:
            summary = f"1 conflict detected: {conflicts[0].conflict_type.value}"
        else:
            types = ", ".join(c.conflict_type.value for c in conflicts)
            summary = f"{len(conflicts)} conflicts detected: {types}"

        return ConflictReport(
            has_conflicts=has_conflicts,
            conflict_count=len(conflicts),
            conflicts=conflicts,
            highest_severity=highest_severity,
            requires_review=requires_review,
            summary=summary,
        )

    def _detect_score_disagreement(
        self, crisis_scores: Dict[str, float]
    ) -> Optional[DetectedConflict]:
        """
        Detect significant score disagreement between models.

        Conflict if: max(scores) - min(scores) > threshold

        Args:
            crisis_scores: Dict of model_name -> crisis_signal

        Returns:
            DetectedConflict if found, None otherwise
        """
        if len(crisis_scores) < 2:
            return None

        scores = list(crisis_scores.values())
        score_range = max(scores) - min(scores)

        if score_range <= self.score_disagreement_threshold:
            return None

        # Find the disagreeing models
        max_model = max(crisis_scores, key=crisis_scores.get)
        min_model = min(crisis_scores, key=crisis_scores.get)

        return DetectedConflict(
            conflict_type=ConflictType.SCORE_DISAGREEMENT,
            severity=ConflictSeverity.HIGH,
            description=(
                f"Significant score disagreement: {max_model} ({crisis_scores[max_model]:.2f}) "
                f"vs {min_model} ({crisis_scores[min_model]:.2f})"
            ),
            involved_models=[max_model, min_model],
            details={
                "max_score": crisis_scores[max_model],
                "min_score": crisis_scores[min_model],
                "score_range": score_range,
                "threshold": self.score_disagreement_threshold,
                "all_scores": crisis_scores,
            },
        )

    def _detect_irony_sentiment_conflict(
        self, signals: ModelSignals
    ) -> Optional[DetectedConflict]:
        """
        Detect irony-sentiment conflict.

        Conflict if: Positive sentiment detected BUT irony also detected.
        This suggests sarcastic positive language that may mask distress.

        Args:
            signals: Model signals

        Returns:
            DetectedConflict if found, None otherwise
        """
        # Check if sentiment is positive
        positive_score = signals.sentiment_all_scores.get("positive", 0.0)
        is_positive = positive_score > 0.5 or signals.sentiment_label.lower() == "positive"

        # Check if irony detected
        irony_detected = signals.irony_confidence > self.irony_detection_threshold

        if not (is_positive and irony_detected):
            return None

        return DetectedConflict(
            conflict_type=ConflictType.IRONY_SENTIMENT_CONFLICT,
            severity=ConflictSeverity.MEDIUM,
            description=(
                f"Positive sentiment ({positive_score:.2f}) detected with irony "
                f"({signals.irony_confidence:.2f}) - possible sarcasm masking distress"
            ),
            involved_models=["sentiment", "irony"],
            details={
                "positive_score": positive_score,
                "irony_confidence": signals.irony_confidence,
                "sentiment_label": signals.sentiment_label,
                "irony_detected": irony_detected,
            },
        )

    def _detect_emotion_crisis_mismatch(
        self,
        signals: ModelSignals,
        crisis_scores: Dict[str, float],
    ) -> Optional[DetectedConflict]:
        """
        Detect emotion-crisis mismatch.

        Conflict if: High crisis score BUT no crisis-indicating emotions.
        This may indicate false positive or unusual expression pattern.

        Args:
            signals: Model signals
            crisis_scores: Crisis scores from models

        Returns:
            DetectedConflict if found, None otherwise
        """
        # Calculate average crisis score (excluding irony)
        relevant_scores = [
            s for name, s in crisis_scores.items() if name != "irony"
        ]
        if not relevant_scores:
            return None

        avg_crisis = sum(relevant_scores) / len(relevant_scores)

        # Check if crisis is high
        if avg_crisis < 0.5:
            return None

        # Check for crisis emotions
        crisis_emotion_total = 0.0
        detected_crisis_emotions = []

        for emotion in self.CRISIS_EMOTIONS:
            score = signals.emotions_top.get(emotion, 0.0)
            if score > self.emotion_crisis_threshold:
                crisis_emotion_total += score
                detected_crisis_emotions.append((emotion, score))

        # Mismatch if high crisis but low crisis emotions
        if crisis_emotion_total > 0.3:
            return None  # Has crisis emotions, no mismatch

        return DetectedConflict(
            conflict_type=ConflictType.EMOTION_CRISIS_MISMATCH,
            severity=ConflictSeverity.MEDIUM,
            description=(
                f"High crisis score ({avg_crisis:.2f}) but low crisis emotions "
                f"({crisis_emotion_total:.2f}) - possible false positive"
            ),
            involved_models=["bart", "emotions"],
            details={
                "average_crisis_score": avg_crisis,
                "crisis_emotion_total": crisis_emotion_total,
                "detected_crisis_emotions": detected_crisis_emotions,
                "top_emotions": signals.emotions_top,
            },
        )

    def _detect_label_disagreement(
        self, signals: ModelSignals
    ) -> Optional[DetectedConflict]:
        """
        Detect label disagreement.

        Conflict if: BART predicts crisis label BUT sentiment is positive
        AND no irony detected. Unusual combination.

        Args:
            signals: Model signals

        Returns:
            DetectedConflict if found, None otherwise
        """
        # Check if BART predicts a primary crisis label
        bart_label_lower = signals.bart_label.lower()
        is_crisis_label = bart_label_lower in self.PRIMARY_CRISIS_LABELS

        if not is_crisis_label:
            return None

        # Check if sentiment contradicts
        positive_score = signals.sentiment_all_scores.get("positive", 0.0)
        is_very_positive = positive_score > 0.7

        # Check irony (if ironic, contradiction makes sense)
        irony_detected = signals.irony_confidence > self.irony_detection_threshold

        if not (is_very_positive and not irony_detected):
            return None

        return DetectedConflict(
            conflict_type=ConflictType.LABEL_DISAGREEMENT,
            severity=ConflictSeverity.MEDIUM,
            description=(
                f"Crisis label '{signals.bart_label}' conflicts with "
                f"highly positive sentiment ({positive_score:.2f}) without irony"
            ),
            involved_models=["bart", "sentiment"],
            details={
                "bart_label": signals.bart_label,
                "bart_score": signals.bart_score,
                "positive_score": positive_score,
                "irony_detected": irony_detected,
            },
        )

    # =========================================================================
    # Configuration Methods
    # =========================================================================

    def set_thresholds(
        self,
        score_disagreement: Optional[float] = None,
        irony_detection: Optional[float] = None,
        emotion_crisis: Optional[float] = None,
    ) -> None:
        """Update detection thresholds."""
        if score_disagreement is not None:
            self.score_disagreement_threshold = score_disagreement
        if irony_detection is not None:
            self.irony_detection_threshold = irony_detection
        if emotion_crisis is not None:
            self.emotion_crisis_threshold = emotion_crisis

        logger.info(f"Updated thresholds: score={self.score_disagreement_threshold}, "
                    f"irony={self.irony_detection_threshold}, "
                    f"emotion={self.emotion_crisis_threshold}")

    def enable_conflict_type(self, conflict_type: ConflictType) -> None:
        """Enable a conflict type."""
        self.enabled_conflict_types.add(conflict_type)

    def disable_conflict_type(self, conflict_type: ConflictType) -> None:
        """Disable a conflict type."""
        self.enabled_conflict_types.discard(conflict_type)

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "score_disagreement_threshold": self.score_disagreement_threshold,
            "irony_detection_threshold": self.irony_detection_threshold,
            "emotion_crisis_threshold": self.emotion_crisis_threshold,
            "enabled_conflict_types": [ct.value for ct in self.enabled_conflict_types],
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_conflict_detector(
    config_manager: Optional["ConfigManager"] = None,
    score_disagreement_threshold: Optional[float] = None,
    irony_detection_threshold: Optional[float] = None,
    emotion_crisis_threshold: Optional[float] = None,
) -> ConflictDetector:
    """
    Factory function for ConflictDetector.

    Creates a configured conflict detector.

    Args:
        config_manager: Configuration manager instance
        score_disagreement_threshold: Override threshold
        irony_detection_threshold: Override threshold
        emotion_crisis_threshold: Override threshold

    Returns:
        Configured ConflictDetector instance

    Example:
        >>> detector = create_conflict_detector(config_manager=config)
        >>> report = detector.detect_conflicts(signals, scores)
    """
    # Default values
    final_score_threshold = 0.4
    final_irony_threshold = 0.5
    final_emotion_threshold = 0.3

    # Load from config manager
    if config_manager is not None:
        conflict_config = config_manager.get_conflict_detection_config()
        if conflict_config:
            final_score_threshold = conflict_config.get(
                "score_threshold", final_score_threshold
            )
            # Add more config loading as needed

    # Apply explicit overrides
    if score_disagreement_threshold is not None:
        final_score_threshold = score_disagreement_threshold
    if irony_detection_threshold is not None:
        final_irony_threshold = irony_detection_threshold
    if emotion_crisis_threshold is not None:
        final_emotion_threshold = emotion_crisis_threshold

    return ConflictDetector(
        score_disagreement_threshold=final_score_threshold,
        irony_detection_threshold=final_irony_threshold,
        emotion_crisis_threshold=final_emotion_threshold,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "ConflictType",
    "ConflictSeverity",
    # Data classes
    "DetectedConflict",
    "ConflictReport",
    "ModelSignals",
    # Detector class
    "ConflictDetector",
    "create_conflict_detector",
]
