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
Zero-Shot Model Wrapper Abstract Base Class
----------------------------------------------------------------------------
Provides a reusable abstraction for secondary/supplementary models that use
zero-shot classification with configurable candidate labels and hypothesis
templates. Extends BaseModelWrapper with zero-shot pipeline loading and
inference, leaving _process_output() abstract for role-specific subclasses.

Reference implementation: BARTCrisisClassifier (src/models/bart_classifier.py)
Note: BART is NOT refactored to use this class — it predates this abstraction
and has unique crisis-label boosting logic that would add risk without benefit.
----------------------------------------------------------------------------
FILE VERSION: v5.1-4-4.0-1
LAST MODIFIED: 2026-02-08
PHASE: Phase 4 - Sentiment Zero-Shot Migration (truncation fix)
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import logging
from abc import abstractmethod
from typing import Any, Dict, List, Optional

from .base import (
    BaseModelWrapper,
    ModelResult,
    ModelRole,
    ModelTask,
)

# Module version
__version__ = "v5.1-4-4.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


class ZeroShotModelWrapper(BaseModelWrapper):
    """
    Abstract base class for zero-shot classification secondary/supplementary models.

    Extends BaseModelWrapper to provide:
    - Zero-shot classification pipeline loading via _load_model()
    - Candidate label management with runtime reconfiguration
    - Optional hypothesis template for custom NLI formatting
    - Inference that passes candidate_labels to the pipeline

    Subclasses MUST implement:
    - _process_output(): Convert raw zero-shot output to ModelResult
      (each model role maps label scores to crisis signals differently)

    Class Hierarchy:
        BaseModelWrapper (abstract)
        └── ZeroShotModelWrapper (partially abstract)  ← THIS CLASS
                ├── SentimentZeroShotAnalyzer  (Phase 4)
                └── EmotionsZeroShotAnalyzer   (Phase 5)

    Clean Architecture Compliance:
    - Factory functions in each subclass (Rule #1)
    - Configuration via ConfigManager (Rule #4)
    - Resilient error handling with graceful fallbacks (Rule #5)
    """

    def __init__(
        self,
        model_id: str,
        name: str,
        role: ModelRole,
        candidate_labels: List[str],
        weight: float = 0.0,
        device: str = "auto",
        enabled: bool = True,
        hypothesis_template: Optional[str] = None,
        label_signal_mapping: Optional[Dict[str, float]] = None,
        max_tokens: int = 512,
        truncation_strategy: str = "smart",
    ):
        """
        Initialize zero-shot model wrapper.

        Args:
            model_id: HuggingFace model identifier (e.g., MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli)
            name: Short name for this model (e.g., "sentiment_zs", "emotions_zs")
            role: Role in ensemble hierarchy (SECONDARY, SUPPLEMENTARY, etc.)
            candidate_labels: REQUIRED list of natural language labels for zero-shot classification.
                              Each label describes a category this model should detect.
            weight: Weight in ensemble scoring (default: 0.0)
            device: Device to load model on (auto, cuda, cpu)
            enabled: Whether this model is enabled
            hypothesis_template: Optional NLI hypothesis template (e.g., "This text expresses {}.")
                                 If None, HuggingFace default is used: "This example is {}."
            label_signal_mapping: Optional dict mapping label strings to crisis signal values (0.0-1.0).
                                  Used by subclasses in _process_output() to convert label scores
                                  to crisis-relevant signals.
            max_tokens: Maximum tokens for input (FE-003)
            truncation_strategy: How to truncate long inputs (FE-003)

        Raises:
            ValueError: If candidate_labels is empty or not a list
        """
        # Validate candidate_labels before anything else
        if not candidate_labels or not isinstance(candidate_labels, list):
            raise ValueError(
                f"{name}: candidate_labels must be a non-empty list of strings. "
                f"Received: {type(candidate_labels).__name__}"
            )

        if not all(isinstance(label, str) for label in candidate_labels):
            raise ValueError(
                f"{name}: All candidate_labels must be strings."
            )

        # Initialize parent with ZERO_SHOT task type
        super().__init__(
            model_id=model_id,
            name=name,
            task=ModelTask.ZERO_SHOT,
            role=role,
            weight=weight,
            device=device,
            enabled=enabled,
            max_tokens=max_tokens,
            truncation_strategy=truncation_strategy,
        )

        # Store candidate labels as a private copy to prevent external mutation
        self._candidate_labels: List[str] = candidate_labels.copy()

        # Optional hypothesis template
        self._hypothesis_template: Optional[str] = hypothesis_template

        # Optional label-to-signal mapping for crisis score conversion
        self._label_signal_mapping: Optional[Dict[str, float]] = (
            label_signal_mapping.copy() if label_signal_mapping else None
        )

        logger.info(
            f"🎯 {self.name} zero-shot wrapper initialized "
            f"(labels: {len(self._candidate_labels)}, "
            f"template: {'custom' if self._hypothesis_template else 'default'}, "
            f"signal_mapping: {'yes' if self._label_signal_mapping else 'no'})"
        )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def candidate_labels(self) -> List[str]:
        """
        Get current candidate labels (returns a copy to prevent external mutation).

        Returns:
            Copy of the current candidate label list
        """
        return self._candidate_labels.copy()

    @property
    def hypothesis_template(self) -> Optional[str]:
        """
        Get the hypothesis template string.

        Returns:
            Hypothesis template or None if using HuggingFace default
        """
        return self._hypothesis_template

    @property
    def label_signal_mapping(self) -> Optional[Dict[str, float]]:
        """
        Get the label-to-signal mapping (returns a copy to prevent external mutation).

        Returns:
            Copy of the label signal mapping dict, or None if not configured
        """
        if self._label_signal_mapping is None:
            return None
        return self._label_signal_mapping.copy()

    # =========================================================================
    # Implemented Methods (shared across all zero-shot models)
    # =========================================================================

    def _load_model(self) -> Any:
        """
        Load zero-shot classification pipeline from HuggingFace.

        This implementation is shared across all zero-shot secondary models.
        The pipeline task is always "zero-shot-classification".

        Returns:
            HuggingFace pipeline for zero-shot-classification

        Raises:
            RuntimeError: If loading fails (transformers not installed, model not found, etc.)
        """
        try:
            from transformers import pipeline

            device_id = self._determine_device()

            logger.debug(
                f"Loading zero-shot pipeline: {self.model_id} "
                f"(device: {device_id})"
            )

            model = pipeline(
                task="zero-shot-classification",
                model=self.model_id,
                device=device_id,
                truncation=True,
                max_length=self.max_tokens,
            )

            # Ensure tokenizer has an explicit max_length to suppress
            # "no predefined maximum length" warnings during inference
            if hasattr(model, "tokenizer") and model.tokenizer is not None:
                if not hasattr(model.tokenizer, "model_max_length") or model.tokenizer.model_max_length > 1e9:
                    model.tokenizer.model_max_length = self.max_tokens

            return model

        except ImportError as e:
            raise RuntimeError(
                "transformers library not installed. "
                "Install with: pip install transformers torch"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to load zero-shot model '{self.model_id}': {e}"
            ) from e

    def _run_inference(self, text: str, **kwargs) -> Any:
        """
        Run zero-shot classification with candidate labels.

        Passes candidate_labels and optional hypothesis_template to the
        HuggingFace zero-shot-classification pipeline.

        Args:
            text: Input text to classify
            **kwargs: Additional arguments passed to pipeline
                      (e.g., multi_label=True for multi-label classification)

        Returns:
            Raw pipeline output: {
                'sequence': 'input text',
                'labels': ['label1', 'label2', ...],
                'scores': [0.95, 0.03, ...]
            }

        Raises:
            RuntimeError: If model is not loaded
        """
        if self._pipeline is None:
            raise RuntimeError(f"{self.name}: Model not loaded")

        # Build inference kwargs
        inference_kwargs = {
            "candidate_labels": self._candidate_labels,
            "truncation": True,
            "max_length": self.max_tokens,
        }

        # Add hypothesis template if configured
        if self._hypothesis_template is not None:
            inference_kwargs["hypothesis_template"] = self._hypothesis_template

        # Merge any additional kwargs (e.g., multi_label)
        inference_kwargs.update(kwargs)

        # Run inference
        result = self._pipeline(text, **inference_kwargs)

        return result

    # =========================================================================
    # Abstract Method (must be implemented by subclasses)
    # =========================================================================

    @abstractmethod
    def _process_output(self, raw_output: Any, latency_ms: float) -> ModelResult:
        """
        Process raw zero-shot output into standardized ModelResult.

        Each subclass implements this differently based on its analytical role:
        - SentimentZeroShotAnalyzer maps distress-severity labels to crisis signals
        - EmotionsZeroShotAnalyzer maps emotional-state labels to crisis signals

        The raw_output format from zero-shot-classification is:
        {
            'sequence': 'input text',
            'labels': ['label1', 'label2', ...],  # Sorted by score descending
            'scores': [0.95, 0.03, ...]            # Corresponding scores
        }

        Args:
            raw_output: Raw pipeline output (labels + scores)
            latency_ms: Inference latency in milliseconds

        Returns:
            Standardized ModelResult for the decision engine
        """
        pass

    # =========================================================================
    # Label Management Methods
    # =========================================================================

    def update_labels(self, new_labels: List[str]) -> None:
        """
        Update candidate labels at runtime without reloading the model.

        Labels are inference input, not model weights — the model itself does
        not change. This allows dynamic label reconfiguration for A/B testing
        or iterative tuning (Phase 6).

        Args:
            new_labels: New list of candidate label strings

        Raises:
            ValueError: If new_labels is empty or not a list of strings
        """
        if not new_labels or not isinstance(new_labels, list):
            raise ValueError(
                f"{self.name}: new_labels must be a non-empty list of strings. "
                f"Received: {type(new_labels).__name__}"
            )

        if not all(isinstance(label, str) for label in new_labels):
            raise ValueError(
                f"{self.name}: All labels must be strings."
            )

        old_count = len(self._candidate_labels)
        self._candidate_labels = new_labels.copy()

        logger.info(
            f"🔄 {self.name}: Updated candidate labels "
            f"({old_count} → {len(self._candidate_labels)} labels)"
        )

    def update_hypothesis_template(self, template: Optional[str]) -> None:
        """
        Update the hypothesis template at runtime.

        Args:
            template: New hypothesis template string, or None to use HuggingFace default
        """
        old_template = self._hypothesis_template
        self._hypothesis_template = template

        logger.info(
            f"🔄 {self.name}: Updated hypothesis template "
            f"({'custom' if old_template else 'default'} → "
            f"{'custom' if template else 'default'})"
        )

    def update_label_signal_mapping(self, mapping: Optional[Dict[str, float]]) -> None:
        """
        Update the label-to-signal mapping at runtime.

        Args:
            mapping: New mapping dict (label → crisis signal 0.0-1.0), or None to clear
        """
        self._label_signal_mapping = mapping.copy() if mapping else None

        logger.info(
            f"🔄 {self.name}: Updated label signal mapping "
            f"({'set' if mapping else 'cleared'})"
        )

    def get_signal_for_label(self, label: str) -> Optional[float]:
        """
        Get the crisis signal value for a specific label.

        Convenience method for subclasses to use in _process_output().

        Args:
            label: The label string to look up

        Returns:
            Crisis signal value (0.0-1.0) or None if not mapped
        """
        if self._label_signal_mapping is None:
            return None
        return self._label_signal_mapping.get(label)

    # =========================================================================
    # Info Methods
    # =========================================================================

    def get_info(self) -> Dict[str, Any]:
        """
        Get model information including zero-shot-specific details.

        Returns:
            ModelInfo with additional zero-shot metadata
        """
        base_info = super().get_info()
        info_dict = base_info.to_dict()

        # Add zero-shot-specific info
        info_dict["candidate_labels"] = self._candidate_labels.copy()
        info_dict["label_count"] = len(self._candidate_labels)
        info_dict["hypothesis_template"] = self._hypothesis_template
        info_dict["has_signal_mapping"] = self._label_signal_mapping is not None

        return info_dict

    def __repr__(self) -> str:
        """String representation with label count."""
        status = "loaded" if self._is_loaded else "not loaded"
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"role={self.role.value}, "
            f"labels={len(self._candidate_labels)}, "
            f"status={status})"
        )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "ZeroShotModelWrapper",
]