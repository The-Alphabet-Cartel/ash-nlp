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
BART Zero-Shot Crisis Classifier - PRIMARY Model (weight 0.50)
----------------------------------------------------------------------------
Uses facebook/bart-large-mnli for semantic crisis detection through zero-shot
classification with descriptive NLI-optimized candidate labels. Each label
describes a behavior or state, forming coherent NLI hypotheses that produce
richer semantic signal than short categorical terms.

Model: facebook/bart-large-mnli
Role: PRIMARY (weight: 0.50)
Task: zero-shot-classification
Migration: Phase 4.5 (v5.1) - Short categorical labels → Descriptive NLI labels
Previous: 16 short categorical labels with hardcoded tier boosting in scorer
Current:  16 descriptive labels with configurable label_signal_mapping
----------------------------------------------------------------------------
FILE VERSION: v5.1-4.5-4.5.2-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 4.5 - BART Label Optimization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import logging
from typing import Any, Dict, List, Optional

from .base import (
    ModelResult,
    ModelRole,
)
from .zero_shot_base import ZeroShotModelWrapper

# Module version
__version__ = "v5.1-4.5-4.5.2-1"

# Initialize logger
logger = logging.getLogger(__name__)

# =============================================================================
# Default Labels and Mapping
# =============================================================================

# Descriptive NLI-optimized crisis labels - Phase 4.5
# These form coherent hypotheses: "This text entails {label}"
DEFAULT_CRISIS_LABELS = [
    # Critical crisis indicators (signal >= 0.95)
    "person expressing suicidal thoughts or intent to end their life",
    "person describing self-harm or intent to hurt themselves",
    "person experiencing or describing domestic violence or abuse",
    # High severity indicators (signal 0.85)
    "person having a panic attack or acute mental health emergency",
    "person experiencing severe depression with loss of functioning",
    "person in a substance abuse crisis or dangerous intoxication",
    # Medium severity indicators (signal 0.50-0.65)
    "person in significant emotional distress needing support",
    "person experiencing overwhelming anxiety or fear",
    "person processing intense grief or devastating loss",
    "person going through a painful relationship breakdown or betrayal",
    "person struggling with identity, belonging, or self-acceptance",
    "person experiencing deep loneliness or social isolation",
    # Safe indicators (signal 0.00)
    "person having a casual everyday conversation with no distress",
    "person sharing good news, achievements, or positive experiences",
    "person asking a factual question or seeking information",
    "person discussing a topic, opinion, or interest casually",
]

# Maps each label to a crisis signal strength (0.0-1.0)
DEFAULT_LABEL_SIGNAL_MAPPING = {
    "person expressing suicidal thoughts or intent to end their life": 1.00,
    "person describing self-harm or intent to hurt themselves": 0.95,
    "person experiencing or describing domestic violence or abuse": 0.95,
    "person having a panic attack or acute mental health emergency": 0.85,
    "person experiencing severe depression with loss of functioning": 0.85,
    "person in a substance abuse crisis or dangerous intoxication": 0.85,
    "person in significant emotional distress needing support": 0.65,
    "person experiencing overwhelming anxiety or fear": 0.55,
    "person processing intense grief or devastating loss": 0.55,
    "person going through a painful relationship breakdown or betrayal": 0.50,
    "person struggling with identity, belonging, or self-acceptance": 0.50,
    "person experiencing deep loneliness or social isolation": 0.50,
    "person having a casual everyday conversation with no distress": 0.00,
    "person sharing good news, achievements, or positive experiences": 0.00,
    "person asking a factual question or seeking information": 0.00,
    "person discussing a topic, opinion, or interest casually": 0.00,
}

# Critical signal threshold — labels at or above this are considered critical
CRITICAL_SIGNAL_THRESHOLD = 0.90


class BARTCrisisClassifier(ZeroShotModelWrapper):
    """
    BART Zero-Shot Crisis Classifier — PRIMARY MODEL.

    Uses facebook/bart-large-mnli for semantic crisis detection through
    zero-shot classification with descriptive NLI-optimized labels.

    This is the most important model in the ensemble (weight: 0.50).
    Phase 4.5 migrates from short categorical labels to descriptive
    natural-language labels and configurable signal mapping.

    Key difference from v5.0 BARTCrisisClassifier:
    - v5.0: Extends BaseModelWrapper, short categorical labels, hardcoded
            tier boosting in scorer (CRITICAL_LABELS, HIGH_SEVERITY_LABELS)
    - v5.1: Extends ZeroShotModelWrapper, descriptive NLI labels,
            label_signal_mapping produces crisis_signal in ModelResult.metadata

    The crisis_signal is pre-computed during _process_output() and stored in
    ModelResult.metadata["crisis_signal"] for the WeightedScorer to consume.

    Clean Architecture Compliance:
    - Factory function: create_bart_classifier() (Rule #1)
    - Configuration via ConfigManager (Rule #4)
    - Resilient error handling with graceful fallbacks (Rule #5)
    - Labels configurable via labels_config.json + env overrides (Rule #4)
    """

    DEFAULT_MODEL_ID = "facebook/bart-large-mnli"
    DEFAULT_WEIGHT = 0.50

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        weight: float = DEFAULT_WEIGHT,
        device: str = "auto",
        enabled: bool = True,
        candidate_labels: Optional[List[str]] = None,
        hypothesis_template: Optional[str] = None,
        label_signal_mapping: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize BART Crisis Classifier.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight in ensemble scoring (default: 0.50)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
            candidate_labels: Descriptive NLI crisis labels for zero-shot classification.
                              Falls back to DEFAULT_CRISIS_LABELS if not provided.
            hypothesis_template: Optional NLI hypothesis template.
                                 If None, HuggingFace default is used.
            label_signal_mapping: Maps label strings to crisis signal values (0.0-1.0).
                                  Falls back to DEFAULT_LABEL_SIGNAL_MAPPING if not provided.
        """
        # Use defaults if not provided (None means "use defaults", [] is an explicit error)
        labels = candidate_labels if candidate_labels is not None else DEFAULT_CRISIS_LABELS.copy()
        mapping = label_signal_mapping if label_signal_mapping is not None else DEFAULT_LABEL_SIGNAL_MAPPING.copy()

        super().__init__(
            model_id=model_id,
            name="bart_crisis",
            role=ModelRole.PRIMARY,
            candidate_labels=labels,
            weight=weight,
            device=device,
            enabled=enabled,
            hypothesis_template=hypothesis_template,
            label_signal_mapping=mapping,
        )

        logger.info(
            f"🎯 BART Crisis Classifier initialized "
            f"(model: {self.model_id}, weight: {self.weight}, "
            f"labels: {len(self._candidate_labels)})"
        )

    # =========================================================================
    # Abstract Method Implementation
    # =========================================================================

    def _process_output(self, raw_output: Any, latency_ms: float) -> ModelResult:
        """
        Process zero-shot output into standardized ModelResult.

        Zero-shot pipeline returns:
        {
            'sequence': 'input text',
            'labels': ['label1', 'label2', ...],  # Sorted by score descending
            'scores': [0.78, 0.15, ...]            # Corresponding scores
        }

        This method:
        1. Builds all_scores dict from labels + scores
        2. Identifies the top-scoring label
        3. Computes a weighted crisis_signal using label_signal_mapping
        4. Stores crisis_signal in metadata for the WeightedScorer

        Args:
            raw_output: Raw pipeline output (labels + scores)
            latency_ms: Inference latency in milliseconds

        Returns:
            Standardized ModelResult with crisis_signal in metadata
        """
        try:
            labels = raw_output.get("labels", [])
            scores = raw_output.get("scores", [])

            # Build all_scores dictionary
            all_scores = {}
            for label, score in zip(labels, scores):
                all_scores[label] = float(score)

            # Primary prediction (highest scoring label)
            if labels and scores:
                primary_label = labels[0]  # Already sorted descending
                primary_score = float(scores[0])
            else:
                primary_label = "unknown"
                primary_score = 0.0

            # Compute crisis signal from label-to-signal mapping
            crisis_signal = self._compute_crisis_signal(all_scores)

            return ModelResult(
                label=primary_label,
                score=float(primary_score),
                all_scores=all_scores,
                latency_ms=latency_ms,
                model_name=self.name,
                model_role=self.role,
                success=True,
                raw_output=raw_output,
                metadata={
                    "crisis_signal": crisis_signal,
                    "model_type": "zero-shot-crisis",
                    "label_count": len(labels),
                },
            )

        except Exception as e:
            logger.error(f"Error processing BART zero-shot output: {e}")
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Output processing failed: {e}",
                latency_ms=latency_ms,
            )

    # =========================================================================
    # Crisis Signal Computation
    # =========================================================================

    def _compute_crisis_signal(self, all_scores: Dict[str, float]) -> float:
        """
        Compute a weighted crisis signal from zero-shot label scores.

        For each label, multiplies the model's confidence score by the
        configured signal weight from label_signal_mapping, then sums.
        This produces a single 0.0-1.0 value representing crisis severity.

        Example:
            scores = {"suicidal thoughts...": 0.78, "casual conversation...": 0.15, ...}
            mapping = {"suicidal thoughts...": 1.00, "casual conversation...": 0.00, ...}
            signal = (0.78 * 1.00) + (0.15 * 0.00) + ... = 0.78

        Args:
            all_scores: Dictionary of label → model confidence score

        Returns:
            Crisis signal strength (0.0 - 1.0)
        """
        if not all_scores or self._label_signal_mapping is None:
            return 0.0

        crisis_signal = 0.0
        for label, confidence in all_scores.items():
            signal_weight = self._label_signal_mapping.get(label, 0.0)
            crisis_signal += confidence * signal_weight

        # Clamp to valid range
        return max(0.0, min(1.0, crisis_signal))

    # =========================================================================
    # BART-Specific Convenience Methods
    # =========================================================================

    def get_crisis_signal(self, result: ModelResult) -> float:
        """
        Get the pre-computed crisis signal from a ModelResult.

        The crisis signal is computed during _process_output() and stored
        in result.metadata["crisis_signal"]. This method provides a clean
        interface for external consumers (e.g., WeightedScorer).

        Args:
            result: ModelResult from analyze()

        Returns:
            Crisis signal strength (0.0 - 1.0)
        """
        if not result.success:
            return 0.0
        return result.metadata.get("crisis_signal", 0.0)

    def is_critical(self, result: ModelResult) -> bool:
        """
        Check if the crisis signal indicates a critical-level crisis.

        Uses the signal threshold rather than label membership, enabling
        the threshold to be tuned without code changes.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if crisis signal is at or above the critical threshold
        """
        return self.get_crisis_signal(result) >= CRITICAL_SIGNAL_THRESHOLD

    def get_top_crisis_label(self, result: ModelResult) -> str:
        """
        Get the highest-scoring label from the result.

        Args:
            result: ModelResult from analyze()

        Returns:
            The primary (highest confidence) label string
        """
        if not result.success:
            return "unknown"
        return result.label

    def is_safe(self, result: ModelResult, threshold: float = 0.10) -> bool:
        """
        Check if the crisis signal indicates a safe message.

        Args:
            result: ModelResult from analyze()
            threshold: Signal threshold below which message is considered safe

        Returns:
            True if crisis signal is below threshold
        """
        return self.get_crisis_signal(result) < threshold


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_bart_classifier(
    config: Optional[Dict[str, Any]] = None,
    config_manager: Optional[Any] = None,
) -> BARTCrisisClassifier:
    """
    Factory function for BART Crisis Classifier.

    Creates a configured BART classifier using either:
    - ConfigManager instance (loads from default.json + labels_config.json)
    - Direct config dictionary
    - Default values

    Same external signature as v5.0 factory function — drop-in replacement.

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured BARTCrisisClassifier instance

    Example:
        >>> classifier = create_bart_classifier()
        >>> classifier = create_bart_classifier(config_manager=config)
        >>> result = classifier.analyze("I'm feeling really down today")
        >>> signal = classifier.get_crisis_signal(result)
    """
    # Build configuration from various sources
    model_config = {}
    labels = None
    hypothesis_template = None
    label_signal_mapping = None

    # Priority 1: ConfigManager
    if config_manager is not None:
        # Model identity config from default.json
        bart_config = config_manager.get_model_config("bart")
        if bart_config:
            model_config = {
                "model_id": bart_config.get(
                    "model_id", BARTCrisisClassifier.DEFAULT_MODEL_ID
                ),
                "weight": bart_config.get(
                    "weight", BARTCrisisClassifier.DEFAULT_WEIGHT
                ),
                "enabled": bart_config.get("enabled", True),
            }

        # Device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

        # Label config from labels_config.json (Phase 4.5)
        crisis_labels_config = config_manager.get_crisis_labels()
        if crisis_labels_config:
            raw_labels = crisis_labels_config.get("candidate_labels")
            if raw_labels and isinstance(raw_labels, list):
                labels = raw_labels

            raw_template = crisis_labels_config.get("hypothesis_template")
            if raw_template and isinstance(raw_template, str):
                hypothesis_template = raw_template

            raw_mapping = crisis_labels_config.get("label_signal_mapping")
            if raw_mapping and isinstance(raw_mapping, dict):
                label_signal_mapping = raw_mapping

    # Priority 2: Direct config dict
    if config:
        model_config.update(config)
        # Allow labels/mapping in direct config too
        if "candidate_labels" in config:
            labels = config["candidate_labels"]
        if "hypothesis_template" in config:
            hypothesis_template = config["hypothesis_template"]
        if "label_signal_mapping" in config:
            label_signal_mapping = config["label_signal_mapping"]

    # Create classifier with merged config
    return BARTCrisisClassifier(
        model_id=model_config.get("model_id", BARTCrisisClassifier.DEFAULT_MODEL_ID),
        weight=model_config.get("weight", BARTCrisisClassifier.DEFAULT_WEIGHT),
        device=model_config.get("device", "auto"),
        enabled=model_config.get("enabled", True),
        candidate_labels=labels,
        hypothesis_template=hypothesis_template,
        label_signal_mapping=label_signal_mapping,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "BARTCrisisClassifier",
    "create_bart_classifier",
    "DEFAULT_CRISIS_LABELS",
    "DEFAULT_LABEL_SIGNAL_MAPPING",
    "CRITICAL_SIGNAL_THRESHOLD",
]
