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
BART Zero-Shot Crisis Classifier for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.2-2
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.2 - Model Wrapper Implementation
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Wrap facebook/bart-large-mnli for zero-shot crisis classification
- Provide candidate labels for crisis detection
- Return standardized ModelResult for ensemble processing
- Handle multi-label scoring for crisis severity assessment

MODEL DETAILS:
- HuggingFace ID: facebook/bart-large-mnli
- Task: zero-shot-classification
- Role: PRIMARY (weight: 0.50)
- Phase 2 Accuracy: 100% across 207 test cases
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
__version__ = "v5.0-3-4.2-2"

# Initialize logger
logger = logging.getLogger(__name__)

# Default crisis labels (can be overridden via config)
DEFAULT_CRISIS_LABELS = [
    # Primary crisis indicators (critical/high severity)
    "suicide ideation",
    "self-harm",
    "domestic violence",
    "panic attack",
    "severe depression",
    "substance abuse crisis",
    # Secondary crisis indicators (medium severity)
    "emotional distress",
    "anxiety",
    "grief",
    "relationship crisis",
    "identity crisis",
    "isolation",
    # Safe indicators (low/no severity)
    "casual conversation",
    "positive sharing",
    "seeking information",
    "general discussion",
]


class BARTCrisisClassifier(BaseModelWrapper):
    """
    BART Zero-Shot Crisis Classifier - PRIMARY MODEL.

    Uses facebook/bart-large-mnli for semantic crisis detection
    through zero-shot classification with candidate labels.

    This is the most important model in the ensemble (weight: 0.50)
    and achieved 100% accuracy in Phase 2 testing.

    Features:
    - Zero-shot classification (no fine-tuning needed)
    - Configurable candidate labels
    - Multi-label hypothesis scoring
    - Graceful fallback on errors

    Clean Architecture v5.1 Compliance:
    - Factory function: create_bart_classifier()
    - Configuration via ConfigManager
    - Standardized ModelResult output
    """

    # Default model configuration
    DEFAULT_MODEL_ID = "facebook/bart-large-mnli"
    DEFAULT_WEIGHT = 0.50

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        weight: float = DEFAULT_WEIGHT,
        device: str = "auto",
        enabled: bool = True,
        crisis_labels: Optional[List[str]] = None,
    ):
        """
        Initialize BART Crisis Classifier.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight in ensemble scoring (default: 0.50)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
            crisis_labels: Candidate labels for classification
        """
        super().__init__(
            model_id=model_id,
            name="bart_crisis",
            task=ModelTask.ZERO_SHOT,
            role=ModelRole.PRIMARY,
            weight=weight,
            device=device,
            enabled=enabled,
        )

        # Set crisis labels
        self.crisis_labels = crisis_labels or DEFAULT_CRISIS_LABELS.copy()

        logger.info(
            f"🎯 BART Crisis Classifier initialized "
            f"(labels: {len(self.crisis_labels)}, weight: {self.weight})"
        )

    def _load_model(self) -> Any:
        """
        Load BART zero-shot classification pipeline.

        Returns:
            HuggingFace pipeline for zero-shot-classification

        Raises:
            RuntimeError: If loading fails
        """
        try:
            from transformers import pipeline

            device_id = self._determine_device()

            logger.debug(
                f"Loading BART pipeline: {self.model_id} (device: {device_id})"
            )

            model = pipeline(
                task="zero-shot-classification",
                model=self.model_id,
                device=device_id,
            )

            return model

        except ImportError as e:
            raise RuntimeError(
                "transformers library not installed. "
                "Install with: pip install transformers torch"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Failed to load BART model: {e}") from e

    def _run_inference(
        self,
        text: str,
        labels: Optional[List[str]] = None,
        multi_label: bool = False,
        **kwargs,
    ) -> Any:
        """
        Run BART zero-shot classification.

        Args:
            text: Input text to classify
            labels: Candidate labels (uses self.crisis_labels if not provided)
            multi_label: Whether to allow multiple labels per text
            **kwargs: Additional arguments passed to pipeline

        Returns:
            Raw pipeline output with labels and scores
        """
        if self._pipeline is None:
            raise RuntimeError("Model not loaded")

        # Use provided labels or default crisis labels
        candidate_labels = labels or self.crisis_labels

        # Run inference
        result = self._pipeline(
            text, candidate_labels=candidate_labels, multi_label=multi_label, **kwargs
        )

        return result

    def _process_output(self, raw_output: Any, latency_ms: float) -> ModelResult:
        """
        Process BART output into standardized ModelResult.

        BART zero-shot returns:
        {
            'sequence': 'input text',
            'labels': ['label1', 'label2', ...],
            'scores': [0.95, 0.03, ...]
        }

        Args:
            raw_output: Raw pipeline output
            latency_ms: Inference latency

        Returns:
            Standardized ModelResult
        """
        try:
            # Extract labels and scores
            labels = raw_output.get("labels", [])
            scores = raw_output.get("scores", [])

            # Primary prediction (highest score)
            primary_label = labels[0] if labels else "unknown"
            primary_score = scores[0] if scores else 0.0

            # Build all_scores dictionary
            all_scores = {}
            for label, score in zip(labels, scores):
                all_scores[label] = float(score)

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
            logger.error(f"Error processing BART output: {e}")
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Output processing failed: {e}",
                latency_ms=latency_ms,
            )

    # =========================================================================
    # BART-Specific Methods
    # =========================================================================

    def analyze_with_labels(
        self, text: str, labels: List[str], multi_label: bool = False
    ) -> ModelResult:
        """
        Analyze text with custom candidate labels.

        Useful for testing specific hypotheses or
        using different label sets for different contexts.

        Args:
            text: Input text to classify
            labels: Custom candidate labels
            multi_label: Allow multiple labels

        Returns:
            ModelResult with classification
        """
        return self.analyze(text, labels=labels, multi_label=multi_label)

    def get_crisis_score(self, result: ModelResult) -> float:
        """
        Calculate aggregate crisis score from result.

        Weights crisis-related labels higher than safe labels.

        Args:
            result: ModelResult from analyze()

        Returns:
            Aggregate crisis score (0.0 - 1.0)
        """
        if not result.success or not result.all_scores:
            return 0.0

        # Crisis-indicating labels (sum their scores)
        crisis_labels = {
            "suicide ideation",
            "self-harm",
            "domestic violence",
            "panic attack",
            "severe depression",
            "substance abuse crisis",
            "emotional distress",
            "anxiety",
            "grief",
            "relationship crisis",
            "identity crisis",
            "isolation",
        }

        crisis_score_sum = sum(
            score
            for label, score in result.all_scores.items()
            if label in crisis_labels
        )

        # Normalize (scores may not sum to 1.0 in multi-label mode)
        total_score = sum(result.all_scores.values())
        if total_score > 0:
            return crisis_score_sum / total_score

        return 0.0

    def is_crisis_label(self, label: str) -> bool:
        """
        Check if a label indicates crisis.

        Args:
            label: Label to check

        Returns:
            True if label indicates crisis
        """
        safe_labels = {
            "casual conversation",
            "positive sharing",
            "seeking information",
            "general discussion",
        }
        return label.lower() not in safe_labels

    def set_crisis_labels(self, labels: List[str]) -> None:
        """
        Update the candidate labels for classification.

        Args:
            labels: New list of candidate labels
        """
        self.crisis_labels = labels.copy()
        logger.info(f"Updated crisis labels: {len(self.crisis_labels)} labels")

    def get_crisis_labels(self) -> List[str]:
        """Get current crisis labels."""
        return self.crisis_labels.copy()


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
    - Direct config dictionary
    - ConfigManager instance
    - Default values

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured BARTCrisisClassifier instance

    Example:
        >>> classifier = create_bart_classifier()
        >>> classifier = create_bart_classifier(config_manager=config)
        >>> result = classifier.analyze("I'm feeling really down today")
    """
    # Build configuration from various sources
    model_config = {}
    crisis_labels = None

    # Priority 1: ConfigManager
    if config_manager is not None:
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

        # Get device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

        # Get crisis labels
        labels_config = config_manager.get_crisis_labels()
        if labels_config:
            crisis_labels = (
                labels_config.get("primary_labels", [])
                + labels_config.get("secondary_labels", [])
                + labels_config.get("safe_labels", [])
            )

    # Priority 2: Direct config dict
    if config:
        model_config.update(config)
        if "crisis_labels" in config:
            crisis_labels = config["crisis_labels"]

    # Create classifier with merged config
    return BARTCrisisClassifier(
        model_id=model_config.get("model_id", BARTCrisisClassifier.DEFAULT_MODEL_ID),
        weight=model_config.get("weight", BARTCrisisClassifier.DEFAULT_WEIGHT),
        device=model_config.get("device", "auto"),
        enabled=model_config.get("enabled", True),
        crisis_labels=crisis_labels,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "BARTCrisisClassifier",
    "create_bart_classifier",
    "DEFAULT_CRISIS_LABELS",
]
