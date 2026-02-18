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
DeBERTa Zero-Shot Figurative Language Classifier - Non-Literal Speech Detection
----------------------------------------------------------------------------
Post-scoring gatekeeper that detects non-literal speech patterns (hyperbole,
sarcasm, irony, gaming death metaphors) using zero-shot classification. When
figurative language is detected with high confidence, the FigurativeGate in
the decision engine reduces the crisis score to prevent false positives.

Replaces the Cardiff binary irony detector (Phase 6) with a broader
figurative language classifier that covers irony as a subset while also
detecting hyperbole, sarcasm, gaming death metaphors, and other non-literal
speech patterns.

Model: MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli (same as Sentiment-ZS
       and Emotions-ZS — shares cached model weights, separate pipeline)
Role: GATEKEEPER (weight: 0.0 — not in additive scoring)
Task: zero-shot-classification
Phase: Phase 7 (v5.1) - Figurative Language Gate
Previous: cardiffnlp/twitter-roberta-base-irony (binary ironic/not-ironic)
Current:  MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli (figurative labels)
----------------------------------------------------------------------------
FILE VERSION: v5.1-7-7.2-1
LAST MODIFIED: 2026-02-18
PHASE: Phase 7 - Step 7.2 Figurative Language Classifier
CLEAN ARCHITECTURE: v5.2.3 Compliant
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
__version__ = "v5.1-7-7.2-1"

# Initialize logger
logger = logging.getLogger(__name__)

# =============================================================================
# Default Labels
# =============================================================================

# Figurative language labels — answer: "Is this text literal or figurative?"
# The first label is the LITERAL anchor; all others are FIGURATIVE categories.
DEFAULT_FIGURATIVE_CANDIDATE_LABELS = [
    "this text uses literal language to describe a real situation",
    "this text uses exaggeration or hyperbole for emphasis or humor",
    "this text uses sarcasm or irony to express the opposite of what is meant",
    "this text uses violent or death-related metaphors in a casual or playful context",
]

# The literal anchor label — used to identify the "not figurative" classification
LITERAL_LABEL = "this text uses literal language to describe a real situation"


class FigurativeLanguageClassifier(ZeroShotModelWrapper):
    """
    DeBERTa Zero-Shot Figurative Language Classifier — GATEKEEPER MODEL.

    Uses MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli for detecting
    non-literal speech patterns using natural language labels. Each label
    describes a type of figurative language use, with one anchor label for
    literal/genuine content.

    Role: GATEKEEPER (weight: 0.0 — not in additive ensemble scoring)
    Task: zero-shot-classification
    Question answered: "Is this text using language literally or figuratively?"

    This classifier does NOT contribute to the ensemble crisis score. Instead,
    its output is consumed by the FigurativeGate in the decision engine, which
    applies a score reduction when figurative language is detected with high
    confidence.

    Key difference from Phase 6 IronyDetector:
    - Phase 6: Cardiff binary ironic/not-ironic → irony confidence → gate
    - Phase 7: DeBERTa figurative labels → top figurative label + confidence → gate

    The output stores top_figurative_label and figurative_confidence in
    ModelResult.metadata for the FigurativeGate to consume.

    Clean Architecture Compliance:
    - Factory function: create_figurative_classifier() (Rule #1)
    - Configuration via ConfigManager (Rule #4)
    - Resilient error handling with graceful fallbacks (Rule #5)
    - Labels configurable via labels_config.json + env overrides (Rule #4)
    """

    DEFAULT_MODEL_ID = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    DEFAULT_WEIGHT = 0.0  # Gatekeeper — not in additive scoring

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        weight: float = DEFAULT_WEIGHT,
        device: str = "auto",
        enabled: bool = True,
        candidate_labels: Optional[List[str]] = None,
        hypothesis_template: Optional[str] = None,
        literal_label: Optional[str] = None,
    ):
        """
        Initialize DeBERTa Zero-Shot Figurative Language Classifier.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight in ensemble scoring (0.0 — gatekeeper)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
            candidate_labels: Figurative language labels for zero-shot classification.
                              Falls back to DEFAULT_FIGURATIVE_CANDIDATE_LABELS if not provided.
            hypothesis_template: Optional NLI hypothesis template.
                                 If None, HuggingFace default is used.
            literal_label: The label that represents literal/genuine language.
                           Falls back to LITERAL_LABEL constant if not provided.
        """
        labels = (
            candidate_labels
            if candidate_labels is not None
            else DEFAULT_FIGURATIVE_CANDIDATE_LABELS.copy()
        )

        # No label_signal_mapping — gate uses top-label detection, not signal mapping
        super().__init__(
            model_id=model_id,
            name="figurative",
            role=ModelRole.GATEKEEPER,
            candidate_labels=labels,
            weight=weight,
            device=device,
            enabled=enabled,
            hypothesis_template=hypothesis_template,
            label_signal_mapping=None,
        )

        self._literal_label = literal_label or LITERAL_LABEL

        logger.info(
            f"🎭 Figurative Language Classifier initialized "
            f"(model: {self.model_id}, labels: {len(self._candidate_labels)}, "
            f"literal_anchor: '{self._literal_label[:50]}...')"
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
        3. Determines if the top label is figurative (any label except literal)
        4. Computes figurative_confidence (1.0 - literal_confidence)
        5. Stores figurative metadata for the FigurativeGate

        Args:
            raw_output: Raw pipeline output (labels + scores)
            latency_ms: Inference latency in milliseconds

        Returns:
            Standardized ModelResult with figurative detection metadata
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
                primary_label = labels[0]
                primary_score = float(scores[0])
            else:
                primary_label = "unknown"
                primary_score = 0.0

            # Determine if figurative
            is_literal = primary_label == self._literal_label
            literal_confidence = all_scores.get(self._literal_label, 0.0)

            # Figurative confidence = total confidence across all figurative labels
            figurative_confidence = 1.0 - literal_confidence

            # Top figurative label (highest scoring non-literal label)
            top_figurative_label = None
            top_figurative_score = 0.0
            for label, score in all_scores.items():
                if label != self._literal_label and score > top_figurative_score:
                    top_figurative_label = label
                    top_figurative_score = score

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
                    "is_figurative": not is_literal,
                    "figurative_confidence": figurative_confidence,
                    "literal_confidence": literal_confidence,
                    "top_figurative_label": top_figurative_label,
                    "top_figurative_score": top_figurative_score,
                    "model_type": "zero-shot-figurative",
                    "label_count": len(labels),
                },
            )

        except Exception as e:
            logger.error(f"Error processing figurative zero-shot output: {e}")
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Output processing failed: {e}",
                latency_ms=latency_ms,
            )

    # =========================================================================
    # Figurative-Specific Convenience Methods
    # =========================================================================

    def is_figurative(self, result: ModelResult) -> bool:
        """
        Check if the message was classified as figurative language.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if top label is any figurative category (not literal)
        """
        if not result.success:
            return False
        return result.metadata.get("is_figurative", False)

    def is_literal(self, result: ModelResult) -> bool:
        """
        Check if the message was classified as literal language.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if top label is the literal anchor
        """
        if not result.success:
            return True  # Assume literal if model fails (safe default)
        return not result.metadata.get("is_figurative", False)

    def get_figurative_confidence(self, result: ModelResult) -> float:
        """
        Get the combined figurative confidence score.

        This is 1.0 - literal_confidence, representing the total confidence
        the model places on any figurative label.

        Args:
            result: ModelResult from analyze()

        Returns:
            Figurative confidence (0.0 - 1.0)
        """
        if not result.success:
            return 0.0
        return result.metadata.get("figurative_confidence", 0.0)

    def get_top_figurative_label(self, result: ModelResult) -> Optional[str]:
        """
        Get the highest-scoring figurative label (excluding literal).

        Args:
            result: ModelResult from analyze()

        Returns:
            Top figurative label string, or None if literal was top
        """
        if not result.success:
            return None
        return result.metadata.get("top_figurative_label")

    def get_literal_confidence(self, result: ModelResult) -> float:
        """
        Get the literal anchor label's confidence score.

        Args:
            result: ModelResult from analyze()

        Returns:
            Literal confidence (0.0 - 1.0)
        """
        if not result.success:
            return 1.0  # Assume literal if model fails
        return result.metadata.get("literal_confidence", 1.0)


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.2.3 Compliance (Rule #1)
# =============================================================================


def create_figurative_classifier(
    config: Optional[Dict[str, Any]] = None,
    config_manager: Optional[Any] = None,
) -> FigurativeLanguageClassifier:
    """
    Factory function for Figurative Language Classifier.

    Creates a configured DeBERTa zero-shot figurative language classifier
    using either:
    - ConfigManager instance (loads from default.json + labels_config.json)
    - Direct config dictionary
    - Default values

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured FigurativeLanguageClassifier instance

    Example:
        >>> classifier = create_figurative_classifier()
        >>> classifier = create_figurative_classifier(config_manager=config)
        >>> result = classifier.analyze("I died to that boss again, kill me")
        >>> classifier.is_figurative(result)  # True
    """
    model_config = {}
    labels = None
    hypothesis_template = None

    # Priority 1: ConfigManager
    if config_manager is not None:
        # Model identity config from default.json
        figurative_config = config_manager.get_model_config("figurative")
        if figurative_config:
            model_config = {
                "model_id": figurative_config.get(
                    "model_id", FigurativeLanguageClassifier.DEFAULT_MODEL_ID
                ),
                "enabled": figurative_config.get("enabled", True),
            }

        # Device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

        # Label config from labels_config.json (Phase 7)
        figurative_labels = config_manager.get_figurative_labels()
        if figurative_labels:
            raw_labels = figurative_labels.get("candidate_labels")
            if raw_labels and isinstance(raw_labels, list):
                labels = raw_labels

            raw_template = figurative_labels.get("hypothesis_template")
            if raw_template and isinstance(raw_template, str):
                hypothesis_template = raw_template

    # Priority 2: Direct config dict
    if config:
        model_config.update(config)
        if "candidate_labels" in config:
            labels = config["candidate_labels"]
        if "hypothesis_template" in config:
            hypothesis_template = config["hypothesis_template"]

    # Create classifier with merged config
    return FigurativeLanguageClassifier(
        model_id=model_config.get(
            "model_id", FigurativeLanguageClassifier.DEFAULT_MODEL_ID
        ),
        weight=FigurativeLanguageClassifier.DEFAULT_WEIGHT,  # Always 0.0 (gatekeeper)
        device=model_config.get("device", "auto"),
        enabled=model_config.get("enabled", True),
        candidate_labels=labels,
        hypothesis_template=hypothesis_template,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "FigurativeLanguageClassifier",
    "create_figurative_classifier",
    "DEFAULT_FIGURATIVE_CANDIDATE_LABELS",
    "LITERAL_LABEL",
]
