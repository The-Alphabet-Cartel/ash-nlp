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
Cardiff Sentiment Analyzer for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.2-3
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.2 - Model Wrapper Implementation
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Wrap cardiffnlp/twitter-roberta-base-sentiment-latest for sentiment analysis
- Detect positive, negative, or neutral sentiment
- Provide emotional context signal for ensemble decision
- Support crisis detection through negative sentiment correlation

MODEL DETAILS:
- HuggingFace ID: cardiffnlp/twitter-roberta-base-sentiment-latest
- Task: text-classification
- Role: SECONDARY (weight: 0.25)
- Labels: positive, negative, neutral
- Phase 2 Crisis Accuracy: 89.09%
"""

import logging
from typing import Any, Dict, List, Optional

from .base import (
    BaseModelWrapper,
    ModelResult,
    ModelRole,
    ModelTask,
)

# Module version
__version__ = "v5.0-3-4.2-3"

# Initialize logger
logger = logging.getLogger(__name__)

# Sentiment labels (fixed by model)
SENTIMENT_LABELS = ["positive", "negative", "neutral"]

# Label mapping (model outputs may use different formats)
LABEL_MAPPING = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
    # Direct labels (some model versions)
    "negative": "negative",
    "neutral": "neutral",
    "positive": "positive",
}


class SentimentAnalyzer(BaseModelWrapper):
    """
    Cardiff Sentiment Analyzer - SECONDARY MODEL.

    Uses cardiffnlp/twitter-roberta-base-sentiment-latest for
    sentiment classification (positive, negative, neutral).

    In the crisis detection context, negative sentiment often
    correlates with distress, but is not definitive on its own.

    Features:
    - Twitter-trained model (good for casual text)
    - Three-class sentiment (pos/neg/neutral)
    - Crisis correlation scoring
    - Label normalization

    Clean Architecture v5.1 Compliance:
    - Factory function: create_sentiment_analyzer()
    - Configuration via ConfigManager
    - Standardized ModelResult output
    """

    # Default model configuration
    DEFAULT_MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    DEFAULT_WEIGHT = 0.25

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        weight: float = DEFAULT_WEIGHT,
        device: str = "auto",
        enabled: bool = True,
    ):
        """
        Initialize Sentiment Analyzer.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight in ensemble scoring (default: 0.25)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
        """
        super().__init__(
            model_id=model_id,
            name="sentiment",
            task=ModelTask.TEXT_CLASSIFICATION,
            role=ModelRole.SECONDARY,
            weight=weight,
            device=device,
            enabled=enabled,
        )

        logger.info(f"😊 Sentiment Analyzer initialized (weight: {self.weight})")

    def _load_model(self) -> Any:
        """
        Load sentiment classification pipeline.

        Returns:
            HuggingFace pipeline for text-classification

        Raises:
            RuntimeError: If loading fails
        """
        try:
            from transformers import pipeline

            device_id = self._determine_device()

            logger.debug(
                f"Loading sentiment pipeline: {self.model_id} (device: {device_id})"
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
            raise RuntimeError(f"Failed to load sentiment model: {e}") from e

    def _run_inference(self, text: str, **kwargs) -> Any:
        """
        Run sentiment classification.

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
        Process sentiment output into standardized ModelResult.

        Sentiment pipeline returns:
        [
            {'label': 'LABEL_2', 'score': 0.95},  # positive
            {'label': 'LABEL_1', 'score': 0.03},  # neutral
            {'label': 'LABEL_0', 'score': 0.02},  # negative
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

            # Build all_scores with normalized labels
            all_scores = {}
            for item in scores_list:
                raw_label = item.get("label", "unknown")
                normalized_label = self._normalize_label(raw_label)
                all_scores[normalized_label] = float(item.get("score", 0.0))

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
            logger.error(f"Error processing sentiment output: {e}")
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Output processing failed: {e}",
                latency_ms=latency_ms,
            )

    # =========================================================================
    # Sentiment-Specific Methods
    # =========================================================================

    def _normalize_label(self, label: str) -> str:
        """
        Normalize model label to standard format.

        Args:
            label: Raw label from model

        Returns:
            Normalized label (positive, negative, neutral)
        """
        return LABEL_MAPPING.get(label, label.lower())

    def is_negative(self, result: ModelResult) -> bool:
        """
        Check if sentiment is negative.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if primary sentiment is negative
        """
        return result.success and result.label == "negative"

    def is_positive(self, result: ModelResult) -> bool:
        """
        Check if sentiment is positive.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if primary sentiment is positive
        """
        return result.success and result.label == "positive"

    def is_neutral(self, result: ModelResult) -> bool:
        """
        Check if sentiment is neutral.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if primary sentiment is neutral
        """
        return result.success and result.label == "neutral"

    def get_negative_score(self, result: ModelResult) -> float:
        """
        Get the negative sentiment score.

        Useful for crisis correlation - higher negative
        score may indicate distress.

        Args:
            result: ModelResult from analyze()

        Returns:
            Negative sentiment score (0.0 - 1.0)
        """
        if not result.success:
            return 0.0
        return result.all_scores.get("negative", 0.0)

    def get_crisis_signal(self, result: ModelResult) -> float:
        """
        Calculate crisis signal from sentiment.

        Maps sentiment to crisis correlation:
        - Negative sentiment → higher crisis signal
        - Neutral sentiment → moderate signal
        - Positive sentiment → lower signal

        Args:
            result: ModelResult from analyze()

        Returns:
            Crisis signal strength (0.0 - 1.0)
        """
        if not result.success:
            return 0.0

        # Weight negative heavily, neutral moderately, positive low
        negative = result.all_scores.get("negative", 0.0)
        neutral = result.all_scores.get("neutral", 0.0)
        positive = result.all_scores.get("positive", 0.0)

        # Crisis signal formula:
        # High negative = high signal
        # Neutral has some weight (could mask distress)
        # Positive reduces signal
        signal = (negative * 1.0) + (neutral * 0.3) - (positive * 0.5)

        # Clamp to 0.0 - 1.0
        return max(0.0, min(1.0, signal))


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_sentiment_analyzer(
    config: Optional[Dict[str, Any]] = None,
    config_manager: Optional[Any] = None,
) -> SentimentAnalyzer:
    """
    Factory function for Sentiment Analyzer.

    Creates a configured sentiment analyzer using either:
    - Direct config dictionary
    - ConfigManager instance
    - Default values

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured SentimentAnalyzer instance

    Example:
        >>> analyzer = create_sentiment_analyzer()
        >>> analyzer = create_sentiment_analyzer(config_manager=config)
        >>> result = analyzer.analyze("I'm feeling really down today")
    """
    # Build configuration from various sources
    model_config = {}

    # Priority 1: ConfigManager
    if config_manager is not None:
        sentiment_config = config_manager.get_model_config("sentiment")
        if sentiment_config:
            model_config = {
                "model_id": sentiment_config.get(
                    "model_id", SentimentAnalyzer.DEFAULT_MODEL_ID
                ),
                "weight": sentiment_config.get(
                    "weight", SentimentAnalyzer.DEFAULT_WEIGHT
                ),
                "enabled": sentiment_config.get("enabled", True),
            }

        # Get device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

    # Priority 2: Direct config dict
    if config:
        model_config.update(config)

    # Create analyzer with merged config
    return SentimentAnalyzer(
        model_id=model_config.get("model_id", SentimentAnalyzer.DEFAULT_MODEL_ID),
        weight=model_config.get("weight", SentimentAnalyzer.DEFAULT_WEIGHT),
        device=model_config.get("device", "auto"),
        enabled=model_config.get("enabled", True),
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "SentimentAnalyzer",
    "create_sentiment_analyzer",
    "SENTIMENT_LABELS",
]
