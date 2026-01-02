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
RoBERTa Emotions Classifier for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.2-5
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.2 - Model Wrapper Implementation
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Wrap SamLowe/roberta-base-go_emotions for emotion classification
- Detect fine-grained emotions using 28 GoEmotions labels
- Provide supplementary emotional signals for ensemble decision
- Map emotions to crisis relevance scoring

MODEL DETAILS:
- HuggingFace ID: SamLowe/roberta-base-go_emotions
- Task: text-classification
- Role: SUPPLEMENTARY (weight: 0.10)
- Labels: 28 GoEmotions labels
- Phase 2 Crisis Accuracy: 49.09% (emotions are nuanced/overlapping)

GOEMOTION LABELS (28 total):
Positive: admiration, amusement, approval, caring, desire, excitement,
          gratitude, joy, love, optimism, pride, relief
Negative: anger, annoyance, disappointment, disapproval, disgust,
          embarrassment, fear, grief, nervousness, remorse, sadness
Ambiguous: confusion, curiosity, realization, surprise
Neutral: neutral
"""

import logging
from typing import Any, Dict, List, Optional, Set

from .base import (
    BaseModelWrapper,
    ModelResult,
    ModelRole,
    ModelTask,
)

# Module version
__version__ = "v5.0-3-4.2-5"

# Initialize logger
logger = logging.getLogger(__name__)

# GoEmotions 28 labels
GOEMOTION_LABELS = [
    # Positive emotions
    "admiration",
    "amusement",
    "approval",
    "caring",
    "desire",
    "excitement",
    "gratitude",
    "joy",
    "love",
    "optimism",
    "pride",
    "relief",
    # Negative emotions
    "anger",
    "annoyance",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "fear",
    "grief",
    "nervousness",
    "remorse",
    "sadness",
    # Ambiguous emotions
    "confusion",
    "curiosity",
    "realization",
    "surprise",
    # Neutral
    "neutral",
]

# Emotion categories for crisis assessment
CRISIS_EMOTIONS: Set[str] = {
    "grief",
    "sadness",
    "fear",
    "nervousness",
    "remorse",
    "anger",
    "disappointment",
    "disgust",
    "embarrassment",
}

POSITIVE_EMOTIONS: Set[str] = {
    "joy",
    "love",
    "gratitude",
    "relief",
    "optimism",
    "admiration",
    "amusement",
    "approval",
    "caring",
    "excitement",
    "pride",
    "desire",
}

NEUTRAL_EMOTIONS: Set[str] = {
    "neutral",
    "confusion",
    "curiosity",
    "realization",
    "surprise",
}


class EmotionsClassifier(BaseModelWrapper):
    """
    RoBERTa Emotions Classifier - SUPPLEMENTARY MODEL.

    Uses SamLowe/roberta-base-go_emotions for fine-grained
    emotion classification using 28 GoEmotions labels.

    This model provides supplementary signals about emotional state.
    While it has lower accuracy than other models (emotions overlap),
    it adds valuable nuance to the ensemble decision.

    Features:
    - 28 fine-grained emotion labels
    - Crisis-relevant emotion scoring
    - Multi-label support (multiple emotions possible)
    - Emotion category aggregation

    Clean Architecture v5.1 Compliance:
    - Factory function: create_emotions_classifier()
    - Configuration via ConfigManager
    - Standardized ModelResult output
    """

    # Default model configuration
    DEFAULT_MODEL_ID = "SamLowe/roberta-base-go_emotions"
    DEFAULT_WEIGHT = 0.10

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        weight: float = DEFAULT_WEIGHT,
        device: str = "auto",
        enabled: bool = True,
    ):
        """
        Initialize Emotions Classifier.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight in ensemble scoring (default: 0.10)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
        """
        super().__init__(
            model_id=model_id,
            name="emotions",
            task=ModelTask.TEXT_CLASSIFICATION,
            role=ModelRole.SUPPLEMENTARY,
            weight=weight,
            device=device,
            enabled=enabled,
        )

        logger.info(f"💭 Emotions Classifier initialized (weight: {self.weight})")

    def _load_model(self) -> Any:
        """
        Load emotions classification pipeline.

        Returns:
            HuggingFace pipeline for text-classification

        Raises:
            RuntimeError: If loading fails
        """
        try:
            from transformers import pipeline

            device_id = self._determine_device()

            logger.debug(
                f"Loading emotions pipeline: {self.model_id} (device: {device_id})"
            )

            model = pipeline(
                task="text-classification",
                model=self.model_id,
                device=device_id,
                top_k=None,  # Return all label scores
            )

            return model

        except ImportError as e:
            raise RuntimeError(
                "transformers library not installed. "
                "Install with: pip install transformers torch"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Failed to load emotions model: {e}") from e

    def _run_inference(self, text: str, **kwargs) -> Any:
        """
        Run emotions classification.

        Args:
            text: Input text to analyze
            **kwargs: Additional arguments (unused)

        Returns:
            Raw pipeline output with label scores
        """
        if self._pipeline is None:
            raise RuntimeError("Model not loaded")

        # Run inference
        result = self._pipeline(text)

        return result

    def _process_output(self, raw_output: Any, latency_ms: float) -> ModelResult:
        """
        Process emotions output into standardized ModelResult.

        Emotions pipeline returns all 28 labels with scores:
        [
            {'label': 'neutral', 'score': 0.45},
            {'label': 'sadness', 'score': 0.25},
            {'label': 'grief', 'score': 0.15},
            ...
        ]

        Args:
            raw_output: Raw pipeline output
            latency_ms: Inference latency

        Returns:
            Standardized ModelResult
        """
        try:
            # Handle list output (top_k=None returns list)
            if isinstance(raw_output, list) and len(raw_output) > 0:
                # Could be list of dicts or list of lists
                if isinstance(raw_output[0], list):
                    # Nested list - take first
                    scores_list = raw_output[0]
                else:
                    scores_list = raw_output
            else:
                scores_list = []

            # Build all_scores dictionary
            all_scores = {}
            for item in scores_list:
                label = item.get("label", "unknown").lower()
                score = float(item.get("score", 0.0))
                all_scores[label] = score

            # Get primary prediction (highest score)
            if all_scores:
                primary_label = max(all_scores, key=all_scores.get)
                primary_score = all_scores[primary_label]
            else:
                primary_label = "neutral"
                primary_score = 0.0

            return ModelResult(
                label=primary_label,
                score=float(primary_score),
                all_scores=all_scores,
                latency_ms=latency_ms,
                model_name=self.name,
                model_role=self.role,
                success=True,
                raw_output=raw_output,
            )

        except Exception as e:
            logger.error(f"Error processing emotions output: {e}")
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Output processing failed: {e}",
                latency_ms=latency_ms,
            )

    # =========================================================================
    # Emotions-Specific Methods
    # =========================================================================

    def is_crisis_emotion(self, emotion: str) -> bool:
        """
        Check if an emotion indicates potential crisis.

        Args:
            emotion: Emotion label to check

        Returns:
            True if emotion is crisis-relevant
        """
        return emotion.lower() in CRISIS_EMOTIONS

    def is_positive_emotion(self, emotion: str) -> bool:
        """
        Check if an emotion is positive.

        Args:
            emotion: Emotion label to check

        Returns:
            True if emotion is positive
        """
        return emotion.lower() in POSITIVE_EMOTIONS

    def get_top_emotions(
        self, result: ModelResult, n: int = 3, threshold: float = 0.1
    ) -> List[tuple[str, float]]:
        """
        Get top N emotions above threshold.

        Args:
            result: ModelResult from analyze()
            n: Number of top emotions to return
            threshold: Minimum score threshold

        Returns:
            List of (emotion, score) tuples sorted by score
        """
        if not result.success or not result.all_scores:
            return []

        # Filter and sort
        filtered = [
            (emotion, score)
            for emotion, score in result.all_scores.items()
            if score >= threshold
        ]
        sorted_emotions = sorted(filtered, key=lambda x: x[1], reverse=True)

        return sorted_emotions[:n]

    def get_crisis_emotion_score(self, result: ModelResult) -> float:
        """
        Calculate aggregate score for crisis-relevant emotions.

        Args:
            result: ModelResult from analyze()

        Returns:
            Sum of crisis emotion scores (0.0 - 1.0+)
        """
        if not result.success or not result.all_scores:
            return 0.0

        return sum(
            score
            for emotion, score in result.all_scores.items()
            if emotion in CRISIS_EMOTIONS
        )

    def get_positive_emotion_score(self, result: ModelResult) -> float:
        """
        Calculate aggregate score for positive emotions.

        Args:
            result: ModelResult from analyze()

        Returns:
            Sum of positive emotion scores (0.0 - 1.0+)
        """
        if not result.success or not result.all_scores:
            return 0.0

        return sum(
            score
            for emotion, score in result.all_scores.items()
            if emotion in POSITIVE_EMOTIONS
        )

    def get_emotion_balance(self, result: ModelResult) -> float:
        """
        Calculate emotional balance score.

        Returns:
        - Negative values = crisis emotions dominant
        - Positive values = positive emotions dominant
        - Zero = balanced/neutral

        Args:
            result: ModelResult from analyze()

        Returns:
            Balance score (-1.0 to 1.0)
        """
        if not result.success:
            return 0.0

        crisis_score = self.get_crisis_emotion_score(result)
        positive_score = self.get_positive_emotion_score(result)

        total = crisis_score + positive_score
        if total == 0:
            return 0.0

        # Normalize to -1.0 to 1.0 range
        # negative = crisis dominant, positive = positive dominant
        balance = (positive_score - crisis_score) / total

        return balance

    def get_crisis_signal(self, result: ModelResult) -> float:
        """
        Calculate crisis signal strength from emotions.

        Maps emotional state to crisis relevance:
        - High crisis emotions → higher signal
        - High positive emotions → lower signal
        - Specific severe emotions (grief, fear) boosted

        Args:
            result: ModelResult from analyze()

        Returns:
            Crisis signal strength (0.0 - 1.0)
        """
        if not result.success or not result.all_scores:
            return 0.0

        scores = result.all_scores

        # Base crisis signal from crisis emotions
        crisis_base = sum(scores.get(emotion, 0.0) for emotion in CRISIS_EMOTIONS)

        # Boost for severe emotions
        severe_boost = (
            scores.get("grief", 0.0) * 0.3
            + scores.get("fear", 0.0) * 0.2
            + scores.get("sadness", 0.0) * 0.2
            + scores.get("remorse", 0.0) * 0.1
        )

        # Reduction from positive emotions
        positive_reduction = sum(
            scores.get(emotion, 0.0) * 0.3 for emotion in POSITIVE_EMOTIONS
        )

        # Calculate final signal
        signal = crisis_base + severe_boost - positive_reduction

        # Clamp to 0.0 - 1.0
        return max(0.0, min(1.0, signal))

    def detect_grief(self, result: ModelResult, threshold: float = 0.3) -> bool:
        """
        Detect if grief emotion is significant.

        Args:
            result: ModelResult from analyze()
            threshold: Score threshold for detection

        Returns:
            True if grief score exceeds threshold
        """
        if not result.success:
            return False
        return result.all_scores.get("grief", 0.0) >= threshold

    def detect_fear(self, result: ModelResult, threshold: float = 0.3) -> bool:
        """
        Detect if fear emotion is significant.

        Args:
            result: ModelResult from analyze()
            threshold: Score threshold for detection

        Returns:
            True if fear score exceeds threshold
        """
        if not result.success:
            return False
        return result.all_scores.get("fear", 0.0) >= threshold


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_emotions_classifier(
    config: Optional[Dict[str, Any]] = None,
    config_manager: Optional[Any] = None,
) -> EmotionsClassifier:
    """
    Factory function for Emotions Classifier.

    Creates a configured emotions classifier using either:
    - Direct config dictionary
    - ConfigManager instance
    - Default values

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured EmotionsClassifier instance

    Example:
        >>> classifier = create_emotions_classifier()
        >>> classifier = create_emotions_classifier(config_manager=config)
        >>> result = classifier.analyze("I miss them so much")
    """
    # Build configuration from various sources
    model_config = {}

    # Priority 1: ConfigManager
    if config_manager is not None:
        emotions_config = config_manager.get_model_config("emotions")
        if emotions_config:
            model_config = {
                "model_id": emotions_config.get(
                    "model_id", EmotionsClassifier.DEFAULT_MODEL_ID
                ),
                "weight": emotions_config.get(
                    "weight", EmotionsClassifier.DEFAULT_WEIGHT
                ),
                "enabled": emotions_config.get("enabled", True),
            }

        # Get device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

    # Priority 2: Direct config dict
    if config:
        model_config.update(config)

    # Create classifier with merged config
    return EmotionsClassifier(
        model_id=model_config.get("model_id", EmotionsClassifier.DEFAULT_MODEL_ID),
        weight=model_config.get("weight", EmotionsClassifier.DEFAULT_WEIGHT),
        device=model_config.get("device", "auto"),
        enabled=model_config.get("enabled", True),
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "EmotionsClassifier",
    "create_emotions_classifier",
    "GOEMOTION_LABELS",
    "CRISIS_EMOTIONS",
    "POSITIVE_EMOTIONS",
    "NEUTRAL_EMOTIONS",
]
