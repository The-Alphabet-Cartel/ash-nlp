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
Cardiff Irony Detector for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.2-4
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.2 - Model Wrapper Implementation
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Wrap cardiffnlp/twitter-roberta-base-irony for irony/sarcasm detection
- Detect ironic vs non-ironic messages
- Provide dampening signal to reduce false positives
- Handle sarcastic crisis-sounding messages

MODEL DETAILS:
- HuggingFace ID: cardiffnlp/twitter-roberta-base-irony
- Task: text-classification
- Role: TERTIARY (weight: 0.15)
- Labels: irony, non_irony
- Phase 2 Crisis Accuracy: 94.55%

IMPORTANT:
Irony detection is used to REDUCE false positives. When irony is detected,
the ensemble should dampen crisis signals because sarcastic messages like
"I'm SO happy today 🙄" should not trigger crisis alerts.
"""

import logging
from typing import Any, Dict, Optional

from .base import (
    BaseModelWrapper,
    ModelResult,
    ModelRole,
    ModelTask,
)

# Module version
__version__ = "v5.0-3-4.2-4"

# Initialize logger
logger = logging.getLogger(__name__)

# Irony labels (fixed by model)
IRONY_LABELS = ["irony", "non_irony"]

# Label mapping (model may output different formats)
LABEL_MAPPING = {
    "LABEL_0": "non_irony",
    "LABEL_1": "irony",
    # Direct labels
    "irony": "irony",
    "non_irony": "non_irony",
    "not_irony": "non_irony",  # Alternative format
    "non-irony": "non_irony",  # Alternative format
    "not-irony": "non_irony",  # Alternative format
}


class IronyDetector(BaseModelWrapper):
    """
    Cardiff Irony Detector - TERTIARY MODEL.

    Uses cardiffnlp/twitter-roberta-base-irony for detecting
    sarcasm and irony in text messages.

    CRITICAL FUNCTION: This model helps REDUCE false positives.
    When irony is detected, crisis signals should be dampened
    because sarcastic messages shouldn't trigger alerts.

    Features:
    - Twitter-trained model (good for casual/sarcastic text)
    - Binary classification (irony/non_irony)
    - Crisis dampening signal
    - Label normalization

    Clean Architecture v5.1 Compliance:
    - Factory function: create_irony_detector()
    - Configuration via ConfigManager
    - Standardized ModelResult output
    """

    # Default model configuration
    DEFAULT_MODEL_ID = "cardiffnlp/twitter-roberta-base-irony"
    DEFAULT_WEIGHT = 0.0  # Phase 6.3: Gatekeeper — not in additive scoring

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        weight: float = DEFAULT_WEIGHT,
        device: str = "auto",
        enabled: bool = True,
    ):
        """
        Initialize Irony Detector.

        Args:
            model_id: HuggingFace model identifier
            weight: Weight (0.0 — gatekeeper, not used in additive scoring)
            device: Device to run on (auto, cuda, cpu)
            enabled: Whether this model is enabled
        """
        super().__init__(
            model_id=model_id,
            name="irony",
            task=ModelTask.TEXT_CLASSIFICATION,
            role=ModelRole.GATEKEEPER,
            weight=weight,
            device=device,
            enabled=enabled,
        )

        logger.info(f"🙄 Irony Detector initialized (weight: {self.weight})")

    def _load_model(self) -> Any:
        """
        Load irony classification pipeline.

        Returns:
            HuggingFace pipeline for text-classification

        Raises:
            RuntimeError: If loading fails
        """
        try:
            from transformers import pipeline

            device_id = self._determine_device()

            logger.debug(
                f"Loading irony pipeline: {self.model_id} (device: {device_id})"
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
            raise RuntimeError(f"Failed to load irony model: {e}") from e

    def _run_inference(self, text: str, **kwargs) -> Any:
        """
        Run irony classification.

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
        Process irony output into standardized ModelResult.

        Irony pipeline returns:
        [
            {'label': 'LABEL_1', 'score': 0.85},  # irony
            {'label': 'LABEL_0', 'score': 0.15},  # non_irony
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
                primary_label = "non_irony"
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
            logger.error(f"Error processing irony output: {e}")
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Output processing failed: {e}",
                latency_ms=latency_ms,
            )

    # =========================================================================
    # Irony-Specific Methods
    # =========================================================================

    def _normalize_label(self, label: str) -> str:
        """
        Normalize model label to standard format.

        Args:
            label: Raw label from model

        Returns:
            Normalized label (irony or non_irony)
        """
        normalized = LABEL_MAPPING.get(label, label.lower())
        # Ensure we always return valid label
        if normalized not in IRONY_LABELS:
            normalized = "non_irony"
        return normalized

    def is_ironic(self, result: ModelResult) -> bool:
        """
        Check if message is detected as ironic.

        Args:
            result: ModelResult from analyze()

        Returns:
            True if irony detected
        """
        return result.success and result.label == "irony"

    def is_sincere(self, result: ModelResult) -> bool:
        """
        Check if message is detected as sincere (non-ironic).

        Args:
            result: ModelResult from analyze()

        Returns:
            True if message appears sincere
        """
        return result.success and result.label == "non_irony"

    def get_irony_score(self, result: ModelResult) -> float:
        """
        Get the irony score.

        Args:
            result: ModelResult from analyze()

        Returns:
            Irony score (0.0 - 1.0)
        """
        if not result.success:
            return 0.0
        return result.all_scores.get("irony", 0.0)

    def get_sincerity_score(self, result: ModelResult) -> float:
        """
        Get the sincerity (non-irony) score.

        Args:
            result: ModelResult from analyze()

        Returns:
            Sincerity score (0.0 - 1.0)
        """
        if not result.success:
            return 1.0  # Assume sincere if model fails
        return result.all_scores.get("non_irony", 1.0)

    def get_dampening_factor(self, result: ModelResult) -> float:
        """
        Calculate crisis dampening factor based on irony.

        IMPORTANT: This is the key contribution of the irony model.
        When irony is detected, we want to REDUCE crisis confidence.

        Returns:
        - 1.0 if sincere (no dampening)
        - 0.0-1.0 if ironic (proportional dampening)

        Args:
            result: ModelResult from analyze()

        Returns:
            Dampening factor (0.0 - 1.0)
            1.0 = no dampening (sincere message)
            0.5 = moderate dampening (possibly ironic)
            0.1 = strong dampening (very ironic)
        """
        if not result.success:
            return 1.0  # No dampening if model fails

        irony_score = result.all_scores.get("irony", 0.0)

        # Dampening formula:
        # If irony score is 0.0 → factor = 1.0 (no dampening)
        # If irony score is 0.5 → factor = 0.5 (moderate dampening)
        # If irony score is 1.0 → factor = 0.1 (strong dampening, not zero)

        # We never fully eliminate the signal (floor at 0.1)
        # because even ironic messages might have genuine distress underneath
        dampening = 1.0 - (irony_score * 0.9)

        return max(0.1, dampening)

    def should_dampen_crisis(self, result: ModelResult, threshold: float = 0.6) -> bool:
        """
        Check if crisis signals should be dampened.

        Args:
            result: ModelResult from analyze()
            threshold: Irony score threshold for dampening

        Returns:
            True if irony score exceeds threshold
        """
        return self.get_irony_score(result) >= threshold


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_irony_detector(
    config: Optional[Dict[str, Any]] = None,
    config_manager: Optional[Any] = None,
) -> IronyDetector:
    """
    Factory function for Irony Detector.

    Creates a configured irony detector using either:
    - Direct config dictionary
    - ConfigManager instance
    - Default values

    Args:
        config: Direct configuration dictionary
        config_manager: ConfigManager instance for loading config

    Returns:
        Configured IronyDetector instance

    Example:
        >>> detector = create_irony_detector()
        >>> detector = create_irony_detector(config_manager=config)
        >>> result = detector.analyze("Oh great, another Monday 🙄")
    """
    # Build configuration from various sources
    model_config = {}

    # Priority 1: ConfigManager
    if config_manager is not None:
        irony_config = config_manager.get_model_config("irony")
        if irony_config:
            model_config = {
                "model_id": irony_config.get(
                    "model_id", IronyDetector.DEFAULT_MODEL_ID
                ),
                "weight": irony_config.get("weight", IronyDetector.DEFAULT_WEIGHT),
                "enabled": irony_config.get("enabled", True),
            }

        # Get device from general model config
        models_config = config_manager.get_section("models")
        if models_config:
            model_config["device"] = models_config.get("device", "auto")

    # Priority 2: Direct config dict
    if config:
        model_config.update(config)

    # Create detector with merged config
    return IronyDetector(
        model_id=model_config.get("model_id", IronyDetector.DEFAULT_MODEL_ID),
        weight=model_config.get("weight", IronyDetector.DEFAULT_WEIGHT),
        device=model_config.get("device", "auto"),
        enabled=model_config.get("enabled", True),
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "IronyDetector",
    "create_irony_detector",
    "IRONY_LABELS",
]
