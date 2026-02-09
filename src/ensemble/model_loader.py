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
Model Loader for Ash-NLP Ensemble Service
---
FILE VERSION: v5.1-5-5.5-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 5 - Emotions Zero-Shot Migration (docstring update)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Load and initialize all ensemble models
- Manage model lifecycle (load, unload, warmup)
- Provide unified access to model instances
- Handle GPU memory efficiently
- Support lazy loading and parallel initialization
"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from src.models import (
    BaseModelWrapper,
    ModelInfo,
    create_bart_classifier,
    create_sentiment_analyzer,
    create_irony_detector,
    create_emotions_classifier,
)

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-3-4.3-1"

# Initialize logger
logger = logging.getLogger(__name__)

# Model names in load order (primary first)
MODEL_NAMES = ["bart", "sentiment", "irony", "emotions"]

# Factory function mapping
MODEL_FACTORIES = {
    "bart": create_bart_classifier,
    "sentiment": create_sentiment_analyzer,
    "irony": create_irony_detector,
    "emotions": create_emotions_classifier,
}


class ModelLoader:
    """
    Model Loader for Ash-NLP Ensemble.

    Manages the lifecycle of all models in the ensemble:
    - BART Zero-Shot Crisis Classifier (PRIMARY)
    - DeBERTa Zero-Shot Sentiment Analyzer (SECONDARY)
    - Cardiff Irony Detector (TERTIARY)
    - DeBERTa Zero-Shot Emotions Analyzer (SUPPLEMENTARY)

    Features:
    - Lazy loading (models load on first access)
    - Warmup support for consistent latency
    - Parallel loading for faster startup
    - Memory management (unload unused models)
    - Configuration-driven initialization

    Clean Architecture v5.1 Compliance:
    - Factory function: create_model_loader()
    - Configuration via ConfigManager
    - Dependency injection pattern
    """

    def __init__(
        self,
        config_manager: Optional["ConfigManager"] = None,
        lazy_load: bool = True,
        warmup_on_load: bool = True,
    ):
        """
        Initialize Model Loader.

        Args:
            config_manager: Configuration manager instance
            lazy_load: If True, models load on first access
            warmup_on_load: If True, run warmup after loading
        """
        self.config_manager = config_manager
        self.lazy_load = lazy_load
        self.warmup_on_load = warmup_on_load

        # Model storage
        self._models: Dict[str, BaseModelWrapper] = {}
        self._load_times: Dict[str, float] = {}
        self._is_initialized: bool = False

        # Track loading state
        self._loading_in_progress: bool = False
        self._models_loaded: int = 0

        logger.info(
            f"🔧 ModelLoader initialized "
            f"(lazy_load={lazy_load}, warmup={warmup_on_load})"
        )

        # If not lazy loading, load all models now
        if not lazy_load:
            self.load_all_models()

    # =========================================================================
    # Model Loading
    # =========================================================================

    def load_model(self, model_name: str) -> Optional[BaseModelWrapper]:
        """
        Load a single model by name.

        Args:
            model_name: Name of model to load (bart, sentiment, irony, emotions)

        Returns:
            Loaded model wrapper or None if loading fails
        """
        # Check if already loaded
        if model_name in self._models and self._models[model_name].is_loaded():
            logger.debug(f"{model_name} already loaded")
            return self._models[model_name]

        # Get factory function
        factory = MODEL_FACTORIES.get(model_name)
        if factory is None:
            logger.error(f"❌ Unknown model: {model_name}")
            return None

        logger.info(f"🔄 Loading {model_name}...")
        start_time = time.perf_counter()

        try:
            # Create model using factory function
            model = factory(config_manager=self.config_manager)

            # Check if enabled
            if not model.is_enabled():
                logger.info(f"⏭️ {model_name} is disabled, skipping")
                return None

            # Load the model (triggers HuggingFace download if needed)
            model.load()

            # Warmup if configured
            if self.warmup_on_load:
                model.warmup()

            # Store model and timing
            self._models[model_name] = model
            load_time = time.perf_counter() - start_time
            self._load_times[model_name] = load_time
            self._models_loaded += 1

            logger.info(
                f"✅ {model_name} loaded in {load_time:.2f}s "
                f"(device: {model._actual_device})"
            )

            return model

        except Exception as e:
            logger.error(f"❌ Failed to load {model_name}: {e}")
            return None

    def load_all_models(self) -> Dict[str, bool]:
        """
        Load all ensemble models.

        Returns:
            Dictionary of model_name -> success status
        """
        if self._loading_in_progress:
            logger.warning("⚠️ Model loading already in progress")
            return {}

        self._loading_in_progress = True
        logger.info("🚀 Loading all ensemble models...")

        results = {}
        total_start = time.perf_counter()

        for model_name in MODEL_NAMES:
            model = self.load_model(model_name)
            results[model_name] = model is not None

        total_time = time.perf_counter() - total_start
        loaded_count = sum(1 for success in results.values() if success)

        self._loading_in_progress = False
        self._is_initialized = True

        logger.info(
            f"✅ Loaded {loaded_count}/{len(MODEL_NAMES)} models in {total_time:.2f}s"
        )

        return results

    def load_models_parallel(self, max_workers: int = 2) -> Dict[str, bool]:
        """
        Load models in parallel using thread pool.

        Note: Limited parallelism recommended due to GPU memory constraints.

        Args:
            max_workers: Maximum concurrent model loads

        Returns:
            Dictionary of model_name -> success status
        """
        if self._loading_in_progress:
            logger.warning("⚠️ Model loading already in progress")
            return {}

        self._loading_in_progress = True
        logger.info(f"🚀 Loading models in parallel (workers={max_workers})...")

        results = {}
        total_start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.load_model, name): name for name in MODEL_NAMES
            }

            for future in futures:
                model_name = futures[future]
                try:
                    model = future.result()
                    results[model_name] = model is not None
                except Exception as e:
                    logger.error(f"❌ Parallel load failed for {model_name}: {e}")
                    results[model_name] = False

        total_time = time.perf_counter() - total_start
        loaded_count = sum(1 for success in results.values() if success)

        self._loading_in_progress = False
        self._is_initialized = True

        logger.info(
            f"✅ Parallel loaded {loaded_count}/{len(MODEL_NAMES)} models "
            f"in {total_time:.2f}s"
        )

        return results

    # =========================================================================
    # Model Access
    # =========================================================================

    def get_model(self, model_name: str) -> Optional[BaseModelWrapper]:
        """
        Get a model by name, loading if necessary.

        Args:
            model_name: Name of model to get

        Returns:
            Model wrapper or None if not available
        """
        # Check if already loaded
        if model_name in self._models:
            return self._models[model_name]

        # Lazy load if enabled
        if self.lazy_load:
            return self.load_model(model_name)

        logger.warning(f"⚠️ Model {model_name} not loaded")
        return None

    def get_bart(self):
        """Get BART crisis classifier."""
        return self.get_model("bart")

    def get_sentiment(self):
        """Get sentiment analyzer."""
        return self.get_model("sentiment")

    def get_irony(self):
        """Get irony detector."""
        return self.get_model("irony")

    def get_emotions(self):
        """Get emotions classifier."""
        return self.get_model("emotions")

    def get_all_models(self) -> Dict[str, BaseModelWrapper]:
        """
        Get all loaded models.

        Returns:
            Dictionary of model_name -> model wrapper
        """
        return self._models.copy()

    def get_enabled_models(self) -> Dict[str, BaseModelWrapper]:
        """
        Get all enabled and loaded models.

        Returns:
            Dictionary of model_name -> model wrapper for enabled models
        """
        return {
            name: model
            for name, model in self._models.items()
            if model.is_enabled() and model.is_loaded()
        }

    # =========================================================================
    # Model Lifecycle
    # =========================================================================

    def unload_model(self, model_name: str) -> bool:
        """
        Unload a model to free memory.

        Args:
            model_name: Name of model to unload

        Returns:
            True if unloaded successfully
        """
        if model_name not in self._models:
            logger.debug(f"{model_name} not loaded")
            return False

        try:
            self._models[model_name].unload()
            del self._models[model_name]
            self._models_loaded -= 1

            logger.info(f"🗑️ Unloaded {model_name}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to unload {model_name}: {e}")
            return False

    def unload_all_models(self) -> None:
        """Unload all models to free memory."""
        logger.info("🗑️ Unloading all models...")

        for model_name in list(self._models.keys()):
            self.unload_model(model_name)

        # Force garbage collection
        self._free_gpu_memory()

        self._is_initialized = False
        logger.info("✅ All models unloaded")

    def reload_model(self, model_name: str) -> Optional[BaseModelWrapper]:
        """
        Reload a model (unload then load).

        Args:
            model_name: Name of model to reload

        Returns:
            Reloaded model or None if failed
        """
        logger.info(f"🔄 Reloading {model_name}...")

        self.unload_model(model_name)
        return self.load_model(model_name)

    def warmup_all(self) -> Dict[str, bool]:
        """
        Warmup all loaded models.

        Returns:
            Dictionary of model_name -> warmup success
        """
        logger.info("🔥 Warming up all models...")

        results = {}
        for name, model in self._models.items():
            results[name] = model.warmup()

        return results

    # =========================================================================
    # Status and Info
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive loader status.

        Returns:
            Status dictionary with all model states
        """
        models_status = {}

        for name in MODEL_NAMES:
            if name in self._models:
                model = self._models[name]
                models_status[name] = {
                    "loaded": model.is_loaded(),
                    "enabled": model.is_enabled(),
                    "device": model._actual_device,
                    "load_time_s": self._load_times.get(name, 0),
                    "stats": model.get_stats(),
                }
            else:
                models_status[name] = {
                    "loaded": False,
                    "enabled": None,
                    "device": None,
                    "load_time_s": 0,
                }

        return {
            "is_initialized": self._is_initialized,
            "lazy_load": self.lazy_load,
            "warmup_on_load": self.warmup_on_load,
            "models_loaded": self._models_loaded,
            "total_models": len(MODEL_NAMES),
            "loading_in_progress": self._loading_in_progress,
            "models": models_status,
        }

    def get_model_info(self) -> List[ModelInfo]:
        """
        Get info for all loaded models.

        Returns:
            List of ModelInfo objects
        """
        return [model.get_info() for model in self._models.values()]

    def get_model_weights(self) -> Dict[str, float]:
        """
        Get weights for all loaded models.

        Returns:
            Dictionary of model_name -> weight
        """
        return {
            name: model.weight
            for name, model in self._models.items()
            if model.is_enabled()
        }

    def is_ready(self) -> bool:
        """
        Check if loader is ready for inference.

        At minimum, BART (primary model) must be loaded.

        Returns:
            True if ready for inference
        """
        bart = self._models.get("bart")
        return bart is not None and bart.is_loaded()

    def is_fully_loaded(self) -> bool:
        """
        Check if all models are loaded.

        Returns:
            True if all enabled models are loaded
        """
        for name in MODEL_NAMES:
            model = self._models.get(name)
            if model is None:
                # Check if it should be enabled via config
                if self.config_manager:
                    config = self.config_manager.get_model_config(name)
                    if config and config.get("enabled", True):
                        return False

        return self._is_initialized

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _free_gpu_memory(self) -> None:
        """Free GPU memory after unloading models."""
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                logger.debug("GPU memory cache cleared")
        except ImportError:
            pass

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ModelLoader("
            f"loaded={self._models_loaded}/{len(MODEL_NAMES)}, "
            f"ready={self.is_ready()})"
        )


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_model_loader(
    config_manager: Optional["ConfigManager"] = None,
    lazy_load: bool = True,
    warmup_on_load: bool = True,
) -> ModelLoader:
    """
    Factory function for ModelLoader.

    Creates a configured model loader using ConfigManager settings.

    Args:
        config_manager: Configuration manager instance
        lazy_load: If True, models load on first access (default: True)
        warmup_on_load: If True, run warmup after loading (default: True)

    Returns:
        Configured ModelLoader instance

    Example:
        >>> loader = create_model_loader(config_manager=config)
        >>> loader.load_all_models()
        >>> bart = loader.get_bart()
    """
    # Override settings from config if available
    if config_manager is not None:
        models_config = config_manager.get_section("models")
        if models_config:
            warmup_on_load = models_config.get("warmup_enabled", warmup_on_load)

    return ModelLoader(
        config_manager=config_manager,
        lazy_load=lazy_load,
        warmup_on_load=warmup_on_load,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "ModelLoader",
    "create_model_loader",
    "MODEL_NAMES",
]
