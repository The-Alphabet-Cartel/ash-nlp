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
Abstract Base Model Class for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.2-1
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.2 - Model Wrapper Foundation
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Define standard interface for all model wrappers
- Provide common functionality (lazy loading, performance tracking)
- Ensure consistent response format across all models
- Handle errors gracefully with logging
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum

# Module version
__version__ = "v5.0-3-4.2-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Data Classes for Standardized Responses
# =============================================================================


class ModelRole(Enum):
    """Model roles in the ensemble hierarchy."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    SUPPLEMENTARY = "supplementary"


class ModelTask(Enum):
    """Supported model task types."""

    ZERO_SHOT = "zero-shot-classification"
    TEXT_CLASSIFICATION = "text-classification"


@dataclass
class ModelResult:
    """
    Standardized result from any model wrapper.

    All model wrappers return this format to ensure
    the decision engine can process them uniformly.

    Attributes:
        label: Primary predicted label
        score: Confidence score for primary label (0.0 - 1.0)
        all_scores: Dictionary of all labels with their scores
        latency_ms: Processing time in milliseconds
        model_name: Name of the model that produced this result
        model_role: Role of this model in the ensemble
        success: Whether inference succeeded
        error: Error message if inference failed
        raw_output: Original model output (for debugging)
    """

    label: str
    score: float
    all_scores: Dict[str, float]
    latency_ms: float
    model_name: str
    model_role: ModelRole
    success: bool = True
    error: Optional[str] = None
    raw_output: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "label": self.label,
            "score": self.score,
            "all_scores": self.all_scores,
            "latency_ms": self.latency_ms,
            "model_name": self.model_name,
            "model_role": self.model_role.value,
            "success": self.success,
            "error": self.error,
        }

    @classmethod
    def create_error(
        cls, model_name: str, model_role: ModelRole, error: str, latency_ms: float = 0.0
    ) -> "ModelResult":
        """Create an error result when inference fails."""
        return cls(
            label="error",
            score=0.0,
            all_scores={},
            latency_ms=latency_ms,
            model_name=model_name,
            model_role=model_role,
            success=False,
            error=error,
        )


@dataclass
class ModelInfo:
    """
    Information about a loaded model.

    Attributes:
        name: Short name (e.g., "bart", "sentiment")
        model_id: HuggingFace model identifier
        task: Model task type
        role: Role in ensemble
        weight: Weight in ensemble scoring
        is_loaded: Whether model is currently loaded
        device: Device model is loaded on
    """

    name: str
    model_id: str
    task: ModelTask
    role: ModelRole
    weight: float
    is_loaded: bool = False
    device: str = "cpu"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "model_id": self.model_id,
            "task": self.task.value,
            "role": self.role.value,
            "weight": self.weight,
            "is_loaded": self.is_loaded,
            "device": self.device,
        }


# =============================================================================
# Abstract Base Model Class
# =============================================================================


class BaseModelWrapper(ABC):
    """
    Abstract base class for all Ash-NLP model wrappers.

    Provides:
    - Standard interface via analyze() method
    - Lazy loading (models load on first use)
    - Performance tracking (latency, VRAM)
    - Error handling with graceful fallbacks
    - Consistent logging

    Subclasses must implement:
    - _load_model(): Load the HuggingFace pipeline
    - _run_inference(): Run model-specific inference
    - _process_output(): Convert output to ModelResult

    Clean Architecture v5.1 Compliance:
    - Factory function pattern for each subclass
    - Configuration via ConfigManager
    - Resilient error handling (Rule #5)
    """

    def __init__(
        self,
        model_id: str,
        name: str,
        task: ModelTask,
        role: ModelRole,
        weight: float = 0.0,
        device: str = "auto",
        enabled: bool = True,
    ):
        """
        Initialize base model wrapper.

        Args:
            model_id: HuggingFace model identifier
            name: Short name for this model
            task: Model task type
            role: Role in ensemble hierarchy
            weight: Weight in ensemble scoring
            device: Device to load model on (auto, cuda, cpu)
            enabled: Whether this model is enabled
        """
        self.model_id = model_id
        self.name = name
        self.task = task
        self.role = role
        self.weight = weight
        self.device = device
        self.enabled = enabled

        # Pipeline will be loaded lazily
        self._pipeline: Optional[Any] = None
        self._is_loaded: bool = False
        self._actual_device: str = "cpu"

        # Performance tracking
        self._total_inferences: int = 0
        self._total_latency_ms: float = 0.0

        logger.debug(
            f"Initialized {self.name} wrapper "
            f"(model_id={self.model_id}, role={self.role.value})"
        )

    # =========================================================================
    # Abstract Methods (must be implemented by subclasses)
    # =========================================================================

    @abstractmethod
    def _load_model(self) -> Any:
        """
        Load the HuggingFace pipeline.

        Subclasses implement model-specific loading logic.

        Returns:
            Loaded pipeline object

        Raises:
            RuntimeError: If model loading fails
        """
        pass

    @abstractmethod
    def _run_inference(self, text: str, **kwargs) -> Any:
        """
        Run model-specific inference.

        Args:
            text: Input text to analyze
            **kwargs: Model-specific parameters

        Returns:
            Raw model output
        """
        pass

    @abstractmethod
    def _process_output(self, raw_output: Any, latency_ms: float) -> ModelResult:
        """
        Process raw model output into standardized ModelResult.

        Args:
            raw_output: Raw output from _run_inference
            latency_ms: Inference latency

        Returns:
            Standardized ModelResult
        """
        pass

    # =========================================================================
    # Public API
    # =========================================================================

    def analyze(self, text: str, **kwargs) -> ModelResult:
        """
        Analyze text and return standardized result.

        This is the main public interface for all model wrappers.
        Handles lazy loading, timing, and error handling.

        Args:
            text: Input text to analyze
            **kwargs: Model-specific parameters

        Returns:
            ModelResult with prediction and metadata
        """
        if not self.enabled:
            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error="Model is disabled",
            )

        # Ensure model is loaded
        if not self._is_loaded:
            try:
                self.load()
            except Exception as e:
                logger.error(f"❌ Failed to load {self.name}: {e}")
                return ModelResult.create_error(
                    model_name=self.name,
                    model_role=self.role,
                    error=f"Model loading failed: {str(e)}",
                )

        # Run inference with timing
        start_time = time.perf_counter()

        try:
            raw_output = self._run_inference(text, **kwargs)
            latency_ms = (time.perf_counter() - start_time) * 1000

            # Process output
            result = self._process_output(raw_output, latency_ms)

            # Update performance tracking
            self._total_inferences += 1
            self._total_latency_ms += latency_ms

            return result

        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"❌ Inference error in {self.name}: {e}")

            return ModelResult.create_error(
                model_name=self.name,
                model_role=self.role,
                error=f"Inference failed: {str(e)}",
                latency_ms=latency_ms,
            )

    def load(self) -> bool:
        """
        Load the model (called automatically on first analyze).

        Returns:
            True if loading succeeded

        Raises:
            RuntimeError: If loading fails
        """
        if self._is_loaded:
            logger.debug(f"{self.name} already loaded")
            return True

        logger.info(f"🔄 Loading {self.name} ({self.model_id})...")

        try:
            self._pipeline = self._load_model()
            self._is_loaded = True

            # Determine actual device
            self._actual_device = self._determine_actual_device()

            logger.info(
                f"✅ {self.name} loaded successfully (device: {self._actual_device})"
            )
            return True

        except Exception as e:
            logger.error(f"❌ Failed to load {self.name}: {e}")
            self._is_loaded = False
            raise RuntimeError(f"Model loading failed: {e}") from e

    def unload(self) -> None:
        """Unload model to free memory."""
        if not self._is_loaded:
            return

        logger.info(f"🗑️ Unloading {self.name}...")

        self._pipeline = None
        self._is_loaded = False

        # Try to free GPU memory
        self._free_gpu_memory()

        logger.info(f"✅ {self.name} unloaded")

    def warmup(self, sample_text: str = "This is a warmup message.") -> bool:
        """
        Warm up the model with a sample inference.

        This helps ensure consistent latency on first real inference.

        Args:
            sample_text: Text to use for warmup

        Returns:
            True if warmup succeeded
        """
        logger.info(f"🔥 Warming up {self.name}...")

        try:
            result = self.analyze(sample_text)

            if result.success:
                logger.info(
                    f"✅ {self.name} warmed up (latency: {result.latency_ms:.2f}ms)"
                )
                return True
            else:
                logger.warning(f"⚠️ {self.name} warmup returned error: {result.error}")
                return False

        except Exception as e:
            logger.error(f"❌ {self.name} warmup failed: {e}")
            return False

    # =========================================================================
    # Info and Status Methods
    # =========================================================================

    def get_info(self) -> ModelInfo:
        """Get model information."""
        return ModelInfo(
            name=self.name,
            model_id=self.model_id,
            task=self.task,
            role=self.role,
            weight=self.weight,
            is_loaded=self._is_loaded,
            device=self._actual_device,
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        avg_latency = (
            self._total_latency_ms / self._total_inferences
            if self._total_inferences > 0
            else 0.0
        )

        return {
            "model_name": self.name,
            "is_loaded": self._is_loaded,
            "device": self._actual_device,
            "total_inferences": self._total_inferences,
            "total_latency_ms": self._total_latency_ms,
            "average_latency_ms": avg_latency,
        }

    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._is_loaded

    def is_enabled(self) -> bool:
        """Check if model is enabled."""
        return self.enabled

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _determine_device(self) -> int:
        """
        Determine device ID for pipeline.

        Returns:
            Device ID (0 for CUDA, -1 for CPU)
        """
        if self.device == "cpu":
            return -1

        if self.device == "cuda":
            return 0

        # Auto-detect
        try:
            import torch

            if torch.cuda.is_available():
                return 0
        except ImportError:
            pass

        return -1

    def _determine_actual_device(self) -> str:
        """Determine actual device model is running on."""
        try:
            import torch

            if torch.cuda.is_available() and self._determine_device() >= 0:
                return f"cuda:{torch.cuda.current_device()}"
        except ImportError:
            pass

        return "cpu"

    def _free_gpu_memory(self) -> None:
        """Free GPU memory if using CUDA."""
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

    def __repr__(self) -> str:
        """String representation."""
        status = "loaded" if self._is_loaded else "not loaded"
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"role={self.role.value}, "
            f"status={status})"
        )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "BaseModelWrapper",
    "ModelResult",
    "ModelInfo",
    "ModelRole",
    "ModelTask",
]
