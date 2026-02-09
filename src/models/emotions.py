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
DeBERTa Zero-Shot Emotions Analyzer - Emotional State Classification
----------------------------------------------------------------------------
Replaces the RoBERTa text-classification emotions model with a DeBERTa
zero-shot classifier using emotional-state candidate labels. Instead of
28 GoEmotions labels with heuristic crisis mapping, this model answers:
"What is the person's emotional state?" using natural language labels.

Model: MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
Role: SUPPLEMENTARY (weight: 0.10)
Task: zero-shot-classification
Migration: Phase 5 (v5.1) - RoBERTa text-classification → DeBERTa zero-shot
Previous: SamLowe/roberta-base-go_emotions (28 GoEmotions labels)
Current:  MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli (emotional state labels)

NOTE: Uses the SAME base model as SentimentZeroShotAnalyzer but with
DIFFERENT candidate labels. These are independent pipeline instances
answering different questions:
  - Sentiment: "What is the distress severity level?"
  - Emotions:  "What is the person's emotional state?"
----------------------------------------------------------------------------
FILE VERSION: v5.1-5-5.1-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 5 - Emotions Zero-Shot Migration
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
__version__ = "v5.1-5-5.1-1"

# Initialize logger
logger = logging.getLogger(__name__)

# =============================================================================
# Default Labels and Mapping
# =============================================================================

# Emotional state labels - answer: "What is the person's emotional state?"
DEFAULT_EMOTIONS_CANDIDATE_LABELS = [
    "person feeling trapped or helpless with no way out",
    "person experiencing grief or devastating loss",
    "person feeling rejected or abandoned by loved ones",
    "person experiencing fear or panic",
    "person feeling anger without crisis intent",
    "person expressing joy or excitement",
    "person in calm or neutral emotional state",
    "person using humor to cope with difficulty",
]

# Maps each label to a crisis signal strength (0.0-1.0)
DEFAULT_EMOTIONS_LABEL_SIGNAL_MAPPING = {
    "person feeling trapped or helpless with no way out": 0.95,
    "person experiencing grief or devastating loss": 0.85,
    "person experiencing fear or panic": 0.80,
    "person feeling rejected or abandoned by loved ones": 0.75,
    "person feeling anger without crisis intent": 0.20,
    "person using humor to cope with difficulty": 0.10,
    "person expressing joy or excitement": 0.0,
    "person in calm or neutral emotional state": 0.0,
}


class EmotionsZeroShotAnalyzer(ZeroShotModelWrapper):
    """
    DeBERTa Zero-Shot Emotions Analyzer — SUPPLEMENTARY MODEL.

    Uses MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli for emotional
    state classification using natural language labels. Each label
    describes an emotional state rather than a generic emotion category,
    giving the ensemble a complementary signal to the Sentiment model's
    distress-severity assessment.

    Role: SUPPLEMENTARY (weight: 0.10)
    Task: zero-shot-classification
    Question answered: "What is the person's emotional state?"

    Key difference from v5.0 EmotionsClassifier:
    - v5.0: RoBERTa outputs 28 GoEmotions labels → heuristic aggregation
    - v5.1: DeBERTa outputs emotional-state scores → direct label-to-signal mapping

    Key difference from SentimentZeroShotAnalyzer:
    - Sentiment: "How severe is the distress?" (severity gradient)
    - Emotions:  "What emotional state are they in?" (type/nature of experience)

    The crisis_signal is pre-computed during _process_output() and stored in
    ModelResult.metadata["crisis_signal"] for the WeightedScorer to consume.

    Clean Architecture Compliance:
    - Factory function: create_emotions_classifier() (Rule #1)
    - Configuration via ConfigManager (Rule #4)
    - Resilient error handling with graceful fallbacks (Rule #5)
    - Labels configurable via labels_config.json + env overrides (Rule #4)
    """

    DEFAULT_MODEL_ID = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    DEFAULT_WEIGHT = 0.10

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
        Initialize DeBERTa Zero-Shot Emotions Analyzer.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight in ensemble scoring (default: 0.10)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
            candidate_labels: Emotional state labels for zero-shot classification.
                              Falls back to DEFAULT_EMOTIONS_CANDIDATE_LABELS if not provided.
            hypothesis_template: Optional NLI hypothesis template.
                                 If None, HuggingFace default is used.
            label_signal_mapping: Maps label strings to crisis signal values (0.0-1.0).
                                  Falls back to DEFAULT_EMOTIONS_LABEL_SIGNAL_MAPPING if not provided.
        """
        # Use defaults if not provided (None means "use defaults", [] is an explicit error)
        labels = (
            candidate_labels
            if candidate_labels is not None
            else DEFAULT_EMOTIONS_CANDIDATE_LABELS.copy()
        )
        mapping = (
            label_signal_mapping
            if label_signal_mapping is not None
            else DEFAULT_EMOTIONS_LABEL_SIGNAL_MAPPING.copy()
        )

        super().__init__(
            model_id=model_id,
            name="emotions",
            role=ModelRole.SUPPLEMENTARY,
            candidate_labels=labels,
            weight=weight,
            device=device,
            enabled=enabled,
            hypothesis_template=hypothesis_template,
            label_signal_mapping=mapping,
        )

        logger.info(
            f"💭 Emotions Zero-Shot Analyzer initialized "
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
                    "model_type": "zero-shot-emotions",
                    "label_count": len(labels),
                },
            )

        except Exception as e:
            logger.error(f"Error processing emotions zero-shot output: {e}")
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
        This produces a single 0.0-1.0 value representing emotional crisis risk.

        Example:
            scores = {"trapped or helpless": 0.72, "calm or neutral": 0.18, ...}
            mapping = {"trapped or helpless": 0.95, "calm or neutral": 0.0, ...}
            signal = (0.72 * 0.95) + (0.18 * 0.0) + ... = 0.684

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

    # =========================================================================
    # Emotions-Specific Convenience Methods
    # =========================================================================

    def get_top_emotional_state(self, result: ModelResult) -> str:
        """
        Get the highest-scoring emotional state label from the result.

        Args:
            result: ModelResult from analyze()

        Returns:
            The primary (highest confidence) label string
        """
        if not result.success:
            return "unknown"
        return result.label

    def is_crisis_emotion(self, result: ModelResult, threshold: float = 0.60) -> bool:
        """
        Check if the crisis signal indicates a crisis-level emotional state.

        Args:
            result: ModelResult from analyze()
            threshold: Signal threshold for "crisis emotion" (default: 0.60)

        Returns:
            True if crisis signal exceeds threshold
        """
        return self.get_crisis_signal(result) >= threshold

    def is_safe_emotion(self, result: ModelResult, threshold: float = 0.20) -> bool:
        """
        Check if the crisis signal indicates a safe/neutral emotional state.

        Args:
            result: ModelResult from analyze()
            threshold: Signal threshold below which emotion is considered safe

        Returns:
            True if crisis signal is below threshold
        """
        return self.get_crisis_signal(result) < threshold


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_emotions_classifier(
    config: Optional[Dict[str, Any]] = None,
    config_manager: Optional[Any] = None,
) -> EmotionsZeroShotAnalyzer:
    """
    Factory function for Emotions Zero-Shot Analyzer.

    Creates a configured DeBERTa zero-shot emotions analyzer using either:
    - ConfigManager instance (loads from default.json + labels_config.json)
    - Direct config dictionary
    - Default values

    Same external signature as v5.0 factory function — drop-in replacement.

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured EmotionsZeroShotAnalyzer instance

    Example:
        >>> analyzer = create_emotions_classifier()
        >>> analyzer = create_emotions_classifier(config_manager=config)
        >>> result = analyzer.analyze("I feel completely trapped")
        >>> signal = analyzer.get_crisis_signal(result)
    """
    # Build configuration from various sources
    model_config = {}
    labels = None
    hypothesis_template = None
    label_signal_mapping = None

    # Priority 1: ConfigManager
    if config_manager is not None:
        # Model identity config from default.json
        emotions_config = config_manager.get_model_config("emotions")
        if emotions_config:
            model_config = {
                "model_id": emotions_config.get(
                    "model_id", EmotionsZeroShotAnalyzer.DEFAULT_MODEL_ID
                ),
                "weight": emotions_config.get(
                    "weight", EmotionsZeroShotAnalyzer.DEFAULT_WEIGHT
                ),
                "enabled": emotions_config.get("enabled", True),
            }

        # Device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

        # Label config from labels_config.json (Phase 3.5)
        emotions_labels = config_manager.get_emotions_labels()
        if emotions_labels:
            raw_labels = emotions_labels.get("candidate_labels")
            if raw_labels and isinstance(raw_labels, list):
                labels = raw_labels

            raw_template = emotions_labels.get("hypothesis_template")
            if raw_template and isinstance(raw_template, str):
                hypothesis_template = raw_template

            raw_mapping = emotions_labels.get("label_signal_mapping")
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

    # Create analyzer with merged config
    return EmotionsZeroShotAnalyzer(
        model_id=model_config.get(
            "model_id", EmotionsZeroShotAnalyzer.DEFAULT_MODEL_ID
        ),
        weight=model_config.get("weight", EmotionsZeroShotAnalyzer.DEFAULT_WEIGHT),
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
    "EmotionsZeroShotAnalyzer",
    "create_emotions_classifier",
    "DEFAULT_EMOTIONS_CANDIDATE_LABELS",
    "DEFAULT_EMOTIONS_LABEL_SIGNAL_MAPPING",
]
