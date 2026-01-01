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
Consensus Algorithms for Ash-NLP Ensemble Service
---
FILE VERSION: v5.0-4-1.1-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 Step 1 - Consensus Algorithms
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Provide multiple consensus algorithm options
- weighted_voting: Weight-based model contribution (default)
- majority_voting: Binary majority decision
- unanimous: All models must agree (conservative)
- conflict_aware: Detect disagreements and flag for review (Council-inspired)

DESIGN PHILOSOPHY:
Each algorithm serves different use cases:
- weighted_voting: Best for nuanced scoring with model expertise weights
- majority_voting: Best for clear binary crisis/no-crisis decisions
- unanimous: Most conservative, minimizes false positives
- conflict_aware: Best when human review is available
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-4-1.1-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Consensus Algorithm Types
# =============================================================================


class ConsensusAlgorithm(Enum):
    """Available consensus algorithms."""

    WEIGHTED_VOTING = "weighted_voting"
    MAJORITY_VOTING = "majority_voting"
    UNANIMOUS = "unanimous"
    CONFLICT_AWARE = "conflict_aware"


class AgreementLevel(Enum):
    """Level of agreement between models."""

    STRONG_AGREEMENT = "strong_agreement"  # Variance < 0.05
    MODERATE_AGREEMENT = "moderate_agreement"  # Variance < 0.15
    WEAK_AGREEMENT = "weak_agreement"  # Variance < 0.25
    SIGNIFICANT_DISAGREEMENT = "significant_disagreement"  # Variance >= 0.25


# =============================================================================
# Consensus Result Data Class
# =============================================================================


@dataclass
class ConsensusResult:
    """
    Result from consensus algorithm execution.

    Attributes:
        algorithm: Algorithm used for consensus
        crisis_score: Final consensus crisis score (0.0 - 1.0)
        confidence: Confidence in consensus (0.0 - 1.0)
        agreement_level: Level of model agreement
        is_crisis: Binary crisis determination
        requires_review: Flag for human review
        has_conflict: Whether significant conflict detected
        individual_scores: Per-model crisis signals
        vote_breakdown: For voting algorithms, vote counts
        metadata: Algorithm-specific additional data
    """

    algorithm: ConsensusAlgorithm
    crisis_score: float
    confidence: float
    agreement_level: AgreementLevel
    is_crisis: bool
    requires_review: bool
    has_conflict: bool
    individual_scores: Dict[str, float]
    vote_breakdown: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "algorithm": self.algorithm.value,
            "crisis_score": round(self.crisis_score, 4),
            "confidence": round(self.confidence, 4),
            "agreement_level": self.agreement_level.value,
            "is_crisis": self.is_crisis,
            "requires_review": self.requires_review,
            "has_conflict": self.has_conflict,
            "individual_scores": {
                k: round(v, 4) for k, v in self.individual_scores.items()
            },
            "vote_breakdown": self.vote_breakdown,
            "metadata": self.metadata,
        }


# =============================================================================
# Consensus Algorithm Implementations
# =============================================================================


def weighted_voting_consensus(
    model_signals: Dict[str, float],
    weights: Dict[str, float],
    crisis_threshold: float = 0.5,
) -> ConsensusResult:
    """
    Weighted Voting Consensus Algorithm (Default).

    Each model's crisis signal is weighted by its configured weight.
    Final score is the weighted sum normalized by total weight.

    Formula:
        crisis_score = Σ(signal_i * weight_i) / Σ(weight_i)

    Args:
        model_signals: Dict of model_name -> crisis_signal (0.0-1.0)
        weights: Dict of model_name -> weight
        crisis_threshold: Score above which crisis is detected

    Returns:
        ConsensusResult with weighted voting outcome
    """
    if not model_signals:
        return ConsensusResult(
            algorithm=ConsensusAlgorithm.WEIGHTED_VOTING,
            crisis_score=0.0,
            confidence=0.0,
            agreement_level=AgreementLevel.SIGNIFICANT_DISAGREEMENT,
            is_crisis=False,
            requires_review=False,
            has_conflict=False,
            individual_scores={},
            metadata={"error": "No model signals provided"},
        )

    # Calculate weighted score
    total_weighted_score = 0.0
    total_weight = 0.0
    contributions = {}

    for model_name, signal in model_signals.items():
        weight = weights.get(model_name, 0.0)
        contribution = signal * weight
        total_weighted_score += contribution
        total_weight += weight
        contributions[model_name] = {
            "signal": signal,
            "weight": weight,
            "contribution": contribution,
        }

    # Normalize
    if total_weight > 0:
        crisis_score = total_weighted_score / total_weight
    else:
        crisis_score = 0.0

    # Calculate agreement level
    agreement_level = _calculate_agreement_level(list(model_signals.values()))

    # Calculate confidence based on agreement
    confidence = _calculate_confidence_from_agreement(
        list(model_signals.values()), len(model_signals)
    )

    # Determine if crisis
    is_crisis = crisis_score >= crisis_threshold

    # Check for conflict (high variance)
    has_conflict = agreement_level == AgreementLevel.SIGNIFICANT_DISAGREEMENT

    return ConsensusResult(
        algorithm=ConsensusAlgorithm.WEIGHTED_VOTING,
        crisis_score=crisis_score,
        confidence=confidence,
        agreement_level=agreement_level,
        is_crisis=is_crisis,
        requires_review=has_conflict,
        has_conflict=has_conflict,
        individual_scores=model_signals.copy(),
        vote_breakdown={
            "total_weight": total_weight,
            "weighted_sum": total_weighted_score,
        },
        metadata={"contributions": contributions},
    )


def majority_voting_consensus(
    model_signals: Dict[str, float],
    crisis_threshold: float = 0.5,
    majority_threshold: float = 0.5,
) -> ConsensusResult:
    """
    Majority Voting Consensus Algorithm.

    Each model votes crisis/no-crisis based on its signal exceeding threshold.
    Final decision is based on majority of votes.

    Formula:
        vote = 1 if signal >= crisis_threshold else 0
        is_crisis = (Σvotes / total_models) > majority_threshold

    Args:
        model_signals: Dict of model_name -> crisis_signal (0.0-1.0)
        crisis_threshold: Signal threshold for a "crisis" vote
        majority_threshold: Fraction of votes needed for crisis decision

    Returns:
        ConsensusResult with majority voting outcome
    """
    if not model_signals:
        return ConsensusResult(
            algorithm=ConsensusAlgorithm.MAJORITY_VOTING,
            crisis_score=0.0,
            confidence=0.0,
            agreement_level=AgreementLevel.SIGNIFICANT_DISAGREEMENT,
            is_crisis=False,
            requires_review=False,
            has_conflict=False,
            individual_scores={},
            metadata={"error": "No model signals provided"},
        )

    # Count votes
    crisis_votes = 0
    safe_votes = 0
    vote_details = {}

    for model_name, signal in model_signals.items():
        if signal >= crisis_threshold:
            crisis_votes += 1
            vote_details[model_name] = {"vote": "crisis", "signal": signal}
        else:
            safe_votes += 1
            vote_details[model_name] = {"vote": "safe", "signal": signal}

    total_votes = len(model_signals)
    vote_ratio = crisis_votes / total_votes if total_votes > 0 else 0.0

    # Determine outcome
    is_crisis = vote_ratio > majority_threshold

    # Crisis score is the vote ratio (simple for majority voting)
    crisis_score = vote_ratio

    # Confidence based on margin
    # More decisive majority = higher confidence
    margin = abs(vote_ratio - 0.5) * 2  # 0 at tie, 1 at unanimous
    confidence = margin

    # Agreement level
    agreement_level = _calculate_agreement_level(list(model_signals.values()))

    # Conflict if close to 50/50 split
    has_conflict = margin < 0.3  # Less than 65-35 split

    return ConsensusResult(
        algorithm=ConsensusAlgorithm.MAJORITY_VOTING,
        crisis_score=crisis_score,
        confidence=confidence,
        agreement_level=agreement_level,
        is_crisis=is_crisis,
        requires_review=has_conflict,
        has_conflict=has_conflict,
        individual_scores=model_signals.copy(),
        vote_breakdown={
            "crisis_votes": crisis_votes,
            "safe_votes": safe_votes,
            "total_votes": total_votes,
            "vote_ratio": vote_ratio,
            "majority_threshold": majority_threshold,
        },
        metadata={"vote_details": vote_details},
    )


def unanimous_consensus(
    model_signals: Dict[str, float],
    crisis_threshold: float = 0.6,
) -> ConsensusResult:
    """
    Unanimous Consensus Algorithm (Conservative).

    ALL models must agree (signal >= threshold) for crisis classification.
    Most conservative approach - minimizes false positives.

    Formula:
        is_crisis = ALL(signal_i >= crisis_threshold)

    Args:
        model_signals: Dict of model_name -> crisis_signal (0.0-1.0)
        crisis_threshold: Signal threshold for crisis agreement

    Returns:
        ConsensusResult with unanimous consensus outcome
    """
    if not model_signals:
        return ConsensusResult(
            algorithm=ConsensusAlgorithm.UNANIMOUS,
            crisis_score=0.0,
            confidence=0.0,
            agreement_level=AgreementLevel.SIGNIFICANT_DISAGREEMENT,
            is_crisis=False,
            requires_review=False,
            has_conflict=False,
            individual_scores={},
            metadata={"error": "No model signals provided"},
        )

    # Check unanimity
    crisis_signals = []
    safe_signals = []
    agreement_details = {}

    for model_name, signal in model_signals.items():
        if signal >= crisis_threshold:
            crisis_signals.append(model_name)
            agreement_details[model_name] = {"agrees_crisis": True, "signal": signal}
        else:
            safe_signals.append(model_name)
            agreement_details[model_name] = {"agrees_crisis": False, "signal": signal}

    # Unanimous crisis only if ALL agree
    is_crisis = len(safe_signals) == 0 and len(crisis_signals) > 0

    # Unanimous safe only if ALL below threshold
    is_unanimous_safe = len(crisis_signals) == 0 and len(safe_signals) > 0

    # Calculate score as average (for reference)
    scores = list(model_signals.values())
    avg_score = sum(scores) / len(scores) if scores else 0.0

    # If unanimous crisis, use average. If not unanimous, score is 0 (conservative)
    if is_crisis:
        crisis_score = avg_score
    elif is_unanimous_safe:
        crisis_score = avg_score
    else:
        # Not unanimous - report average but don't classify as crisis
        crisis_score = avg_score

    # Confidence is 1.0 if unanimous, lower otherwise
    if is_crisis or is_unanimous_safe:
        confidence = 1.0
        agreement_level = AgreementLevel.STRONG_AGREEMENT
    else:
        # Partial agreement
        agreement_ratio = max(len(crisis_signals), len(safe_signals)) / len(
            model_signals
        )
        confidence = agreement_ratio
        agreement_level = _calculate_agreement_level(scores)

    # Has conflict if not unanimous
    has_conflict = not (is_crisis or is_unanimous_safe)

    return ConsensusResult(
        algorithm=ConsensusAlgorithm.UNANIMOUS,
        crisis_score=crisis_score,
        confidence=confidence,
        agreement_level=agreement_level,
        is_crisis=is_crisis,
        requires_review=has_conflict,
        has_conflict=has_conflict,
        individual_scores=model_signals.copy(),
        vote_breakdown={
            "crisis_agreeing": crisis_signals,
            "safe_agreeing": safe_signals,
            "unanimous_crisis": is_crisis,
            "unanimous_safe": is_unanimous_safe,
        },
        metadata={"agreement_details": agreement_details},
    )


def conflict_aware_consensus(
    model_signals: Dict[str, float],
    weights: Dict[str, float],
    disagreement_threshold: float = 0.15,
    crisis_threshold: float = 0.5,
) -> ConsensusResult:
    """
    Conflict-Aware Consensus Algorithm (Council-inspired).

    Detects significant disagreements between models and flags for review.
    Uses weighted voting as base but adds conflict detection layer.
    Inspired by LLM Council peer review concepts.

    Conflict Detection:
        variance = Σ(signal_i - mean)² / n
        has_conflict = variance > disagreement_threshold

    Args:
        model_signals: Dict of model_name -> crisis_signal (0.0-1.0)
        weights: Dict of model_name -> weight
        disagreement_threshold: Variance threshold for flagging conflict
        crisis_threshold: Score threshold for crisis detection

    Returns:
        ConsensusResult with conflict analysis
    """
    if not model_signals:
        return ConsensusResult(
            algorithm=ConsensusAlgorithm.CONFLICT_AWARE,
            crisis_score=0.0,
            confidence=0.0,
            agreement_level=AgreementLevel.SIGNIFICANT_DISAGREEMENT,
            is_crisis=False,
            requires_review=False,
            has_conflict=False,
            individual_scores={},
            metadata={"error": "No model signals provided"},
        )

    scores = list(model_signals.values())
    n = len(scores)

    # Calculate mean
    mean_score = sum(scores) / n

    # Calculate variance
    variance = sum((s - mean_score) ** 2 for s in scores) / n

    # Calculate score range
    score_range = max(scores) - min(scores)

    # Identify outliers (models that deviate significantly from mean)
    outliers = []
    std_dev = variance ** 0.5
    for model_name, signal in model_signals.items():
        deviation = abs(signal - mean_score)
        if deviation > std_dev * 1.5:  # 1.5 standard deviations
            outliers.append(
                {
                    "model": model_name,
                    "signal": signal,
                    "deviation": deviation,
                    "direction": "high" if signal > mean_score else "low",
                }
            )

    # Detect conflict
    has_conflict = variance > disagreement_threshold

    # Calculate weighted score (same as weighted_voting)
    total_weighted_score = 0.0
    total_weight = 0.0

    for model_name, signal in model_signals.items():
        weight = weights.get(model_name, 0.0)
        total_weighted_score += signal * weight
        total_weight += weight

    if total_weight > 0:
        crisis_score = total_weighted_score / total_weight
    else:
        crisis_score = mean_score

    # Determine agreement level
    if variance < 0.05:
        agreement_level = AgreementLevel.STRONG_AGREEMENT
    elif variance < 0.15:
        agreement_level = AgreementLevel.MODERATE_AGREEMENT
    elif variance < 0.25:
        agreement_level = AgreementLevel.WEAK_AGREEMENT
    else:
        agreement_level = AgreementLevel.SIGNIFICANT_DISAGREEMENT

    # Confidence inversely related to variance
    # Low variance = high confidence
    max_variance = 0.25  # Maximum expected variance for 0-1 signals
    confidence = max(0.0, 1.0 - (variance / max_variance))

    # Crisis detection
    is_crisis = crisis_score >= crisis_threshold

    # Requires review if conflict detected
    requires_review = has_conflict

    return ConsensusResult(
        algorithm=ConsensusAlgorithm.CONFLICT_AWARE,
        crisis_score=crisis_score,
        confidence=confidence,
        agreement_level=agreement_level,
        is_crisis=is_crisis,
        requires_review=requires_review,
        has_conflict=has_conflict,
        individual_scores=model_signals.copy(),
        vote_breakdown={
            "mean_score": mean_score,
            "variance": variance,
            "std_dev": std_dev,
            "score_range": score_range,
            "disagreement_threshold": disagreement_threshold,
        },
        metadata={
            "outliers": outliers,
            "conflict_detected": has_conflict,
            "outlier_count": len(outliers),
        },
    )


# =============================================================================
# Helper Functions
# =============================================================================


def _calculate_agreement_level(scores: List[float]) -> AgreementLevel:
    """
    Calculate agreement level based on score variance.

    Args:
        scores: List of crisis signals

    Returns:
        AgreementLevel enum value
    """
    if not scores:
        return AgreementLevel.SIGNIFICANT_DISAGREEMENT

    n = len(scores)
    if n < 2:
        return AgreementLevel.STRONG_AGREEMENT

    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / n

    if variance < 0.05:
        return AgreementLevel.STRONG_AGREEMENT
    elif variance < 0.15:
        return AgreementLevel.MODERATE_AGREEMENT
    elif variance < 0.25:
        return AgreementLevel.WEAK_AGREEMENT
    else:
        return AgreementLevel.SIGNIFICANT_DISAGREEMENT


def _calculate_confidence_from_agreement(
    scores: List[float], model_count: int
) -> float:
    """
    Calculate confidence based on model agreement and coverage.

    Args:
        scores: List of crisis signals
        model_count: Number of models that provided signals

    Returns:
        Confidence score (0.0 - 1.0)
    """
    if not scores:
        return 0.0

    # Agreement component (inverse of variance)
    n = len(scores)
    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / n

    # Max variance for 0-1 range is 0.25
    agreement = 1.0 - (variance / 0.25)
    agreement = max(0.0, min(1.0, agreement))

    # Coverage component (how many models provided signals)
    expected_models = 4  # bart, sentiment, irony, emotions
    coverage = min(1.0, model_count / expected_models)

    # Combined confidence
    confidence = agreement * coverage

    return max(0.0, min(1.0, confidence))


# =============================================================================
# Consensus Selector
# =============================================================================


class ConsensusSelector:
    """
    Consensus Algorithm Selector.

    Manages selection and execution of consensus algorithms.
    Allows runtime switching between algorithms.

    Clean Architecture v5.1 Compliance:
    - Factory function: create_consensus_selector()
    - Configuration via ConfigManager
    """

    def __init__(
        self,
        default_algorithm: ConsensusAlgorithm = ConsensusAlgorithm.WEIGHTED_VOTING,
        weights: Optional[Dict[str, float]] = None,
        thresholds: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize ConsensusSelector.

        Args:
            default_algorithm: Default algorithm to use
            weights: Model weights for weighted algorithms
            thresholds: Various threshold configurations
        """
        self.default_algorithm = default_algorithm
        self.weights = weights or {
            "bart": 0.50,
            "sentiment": 0.25,
            "irony": 0.15,
            "emotions": 0.10,
        }
        self.thresholds = thresholds or {
            "crisis": 0.5,
            "majority": 0.5,
            "unanimous": 0.6,
            "disagreement": 0.15,
        }

        # Algorithm implementations
        self._algorithms = {
            ConsensusAlgorithm.WEIGHTED_VOTING: self._run_weighted_voting,
            ConsensusAlgorithm.MAJORITY_VOTING: self._run_majority_voting,
            ConsensusAlgorithm.UNANIMOUS: self._run_unanimous,
            ConsensusAlgorithm.CONFLICT_AWARE: self._run_conflict_aware,
        }

        logger.info(
            f"📊 ConsensusSelector initialized "
            f"(default: {default_algorithm.value})"
        )

    def select_and_run(
        self,
        model_signals: Dict[str, float],
        algorithm: Optional[ConsensusAlgorithm] = None,
    ) -> ConsensusResult:
        """
        Run consensus algorithm on model signals.

        Args:
            model_signals: Dict of model_name -> crisis_signal
            algorithm: Algorithm to use (None = default)

        Returns:
            ConsensusResult from selected algorithm
        """
        algo = algorithm or self.default_algorithm

        if algo not in self._algorithms:
            logger.warning(
                f"Unknown algorithm {algo}, falling back to weighted_voting"
            )
            algo = ConsensusAlgorithm.WEIGHTED_VOTING

        logger.debug(f"Running consensus algorithm: {algo.value}")

        return self._algorithms[algo](model_signals)

    def _run_weighted_voting(
        self, model_signals: Dict[str, float]
    ) -> ConsensusResult:
        """Run weighted voting consensus."""
        return weighted_voting_consensus(
            model_signals=model_signals,
            weights=self.weights,
            crisis_threshold=self.thresholds.get("crisis", 0.5),
        )

    def _run_majority_voting(
        self, model_signals: Dict[str, float]
    ) -> ConsensusResult:
        """Run majority voting consensus."""
        return majority_voting_consensus(
            model_signals=model_signals,
            crisis_threshold=self.thresholds.get("crisis", 0.5),
            majority_threshold=self.thresholds.get("majority", 0.5),
        )

    def _run_unanimous(self, model_signals: Dict[str, float]) -> ConsensusResult:
        """Run unanimous consensus."""
        return unanimous_consensus(
            model_signals=model_signals,
            crisis_threshold=self.thresholds.get("unanimous", 0.6),
        )

    def _run_conflict_aware(
        self, model_signals: Dict[str, float]
    ) -> ConsensusResult:
        """Run conflict-aware consensus."""
        return conflict_aware_consensus(
            model_signals=model_signals,
            weights=self.weights,
            disagreement_threshold=self.thresholds.get("disagreement", 0.15),
            crisis_threshold=self.thresholds.get("crisis", 0.5),
        )

    def set_algorithm(self, algorithm: ConsensusAlgorithm) -> None:
        """Set the default algorithm."""
        self.default_algorithm = algorithm
        logger.info(f"Default algorithm set to: {algorithm.value}")

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Update model weights."""
        self.weights.update(weights)
        logger.info(f"Updated weights: {self.weights}")

    def set_thresholds(self, thresholds: Dict[str, float]) -> None:
        """Update threshold values."""
        self.thresholds.update(thresholds)
        logger.info(f"Updated thresholds: {self.thresholds}")

    def get_algorithm(self) -> ConsensusAlgorithm:
        """Get current default algorithm."""
        return self.default_algorithm

    def get_available_algorithms(self) -> List[str]:
        """Get list of available algorithm names."""
        return [algo.value for algo in ConsensusAlgorithm]

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "default_algorithm": self.default_algorithm.value,
            "weights": self.weights.copy(),
            "thresholds": self.thresholds.copy(),
            "available_algorithms": self.get_available_algorithms(),
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_consensus_selector(
    config_manager: Optional["ConfigManager"] = None,
    default_algorithm: Optional[str] = None,
    weights: Optional[Dict[str, float]] = None,
    thresholds: Optional[Dict[str, float]] = None,
) -> ConsensusSelector:
    """
    Factory function for ConsensusSelector.

    Creates a configured consensus selector.

    Args:
        config_manager: Configuration manager instance
        default_algorithm: Algorithm name string (optional)
        weights: Model weights (optional)
        thresholds: Threshold values (optional)

    Returns:
        Configured ConsensusSelector instance

    Example:
        >>> selector = create_consensus_selector(config_manager=config)
        >>> result = selector.select_and_run(model_signals)
    """
    # Default values
    final_algorithm = ConsensusAlgorithm.WEIGHTED_VOTING
    final_weights = {
        "bart": 0.50,
        "sentiment": 0.25,
        "irony": 0.15,
        "emotions": 0.10,
    }
    final_thresholds = {
        "crisis": 0.5,
        "majority": 0.5,
        "unanimous": 0.6,
        "disagreement": 0.15,
    }

    # Load from config manager if available
    if config_manager is not None:
        # Get consensus config
        consensus_config = config_manager.get_consensus_config()
        if consensus_config:
            algo_name = consensus_config.get("default_algorithm")
            if algo_name:
                try:
                    final_algorithm = ConsensusAlgorithm(algo_name)
                except ValueError:
                    logger.warning(
                        f"Invalid algorithm '{algo_name}', using weighted_voting"
                    )

            config_thresholds = consensus_config.get("thresholds", {})
            if config_thresholds:
                final_thresholds.update(config_thresholds)

        # Get model weights
        config_weights = config_manager.get_model_weights()
        if config_weights:
            final_weights.update(config_weights)

    # Apply explicit overrides
    if default_algorithm:
        try:
            final_algorithm = ConsensusAlgorithm(default_algorithm)
        except ValueError:
            logger.warning(
                f"Invalid algorithm '{default_algorithm}', using weighted_voting"
            )

    if weights:
        final_weights.update(weights)

    if thresholds:
        final_thresholds.update(thresholds)

    return ConsensusSelector(
        default_algorithm=final_algorithm,
        weights=final_weights,
        thresholds=final_thresholds,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "ConsensusAlgorithm",
    "AgreementLevel",
    # Data classes
    "ConsensusResult",
    # Algorithm functions
    "weighted_voting_consensus",
    "majority_voting_consensus",
    "unanimous_consensus",
    "conflict_aware_consensus",
    # Selector class
    "ConsensusSelector",
    "create_consensus_selector",
]
