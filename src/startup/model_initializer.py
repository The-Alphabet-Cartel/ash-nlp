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
Model Initializer for Ash-NLP Service
---
FILE VERSION: v5.1-5-5.5-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 5 - Emotions Zero-Shot Migration (startup label update)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

DESCRIPTION:
    Downloads and caches HuggingFace models at container startup.
    This enables lightweight Docker images with runtime model fetching.

    HuggingFace's caching system automatically:
    - Skips download if model already cached
    - Checks for newer versions (lightweight HEAD request)
    - Downloads only changed files when updates exist

USAGE:
    # As a module (from entrypoint)
    python -m src.startup.model_initializer

    # Programmatically
    from src.startup.model_initializer import initialize_models_sync
    success = initialize_models_sync()

ENVIRONMENT VARIABLES (reuses existing):
    HF_HOME                  - Cache directory (default: ./models-cache)
    NLP_MODEL_BART_ID        - BART model ID
    NLP_MODEL_BART_ENABLED   - Enable BART (default: true)
    NLP_MODEL_SENTIMENT_ID   - Sentiment model ID
    NLP_MODEL_SENTIMENT_ENABLED - Enable Sentiment (default: true)
    NLP_MODEL_IRONY_ID       - Irony model ID
    NLP_MODEL_IRONY_ENABLED  - Enable Irony (default: true)
    NLP_MODEL_EMOTIONS_ID    - Emotions model ID
    NLP_MODEL_EMOTIONS_ENABLED - Enable Emotions (default: true)
"""

import logging
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Module version
__version__ = "v5.0-7-1.2-1"

# Get logger - inherits configuration from entrypoint when imported,
# or uses fallback for standalone execution
logger = logging.getLogger(__name__)

# Only configure if running standalone (not imported by entrypoint)
if not logging.getLogger().handlers:
    # Fallback for standalone execution: python -m src.startup.model_initializer
    # When imported by entrypoint.py, root logger is already configured with colors
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class ModelConfig:
    """Configuration for a single model."""
    name: str
    env_id: str
    env_enabled: str
    default_id: str
    pipeline_task: str
    description: str


# Model configurations - reuses existing environment variables (Rule #7)
MODEL_CONFIGS: List[ModelConfig] = [
    ModelConfig(
        name="bart",
        env_id="NLP_MODEL_BART_ID",
        env_enabled="NLP_MODEL_BART_ENABLED",
        default_id="facebook/bart-large-mnli",
        pipeline_task="zero-shot-classification",
        description="BART Zero-Shot Crisis Classifier (PRIMARY)",
    ),
    ModelConfig(
        name="sentiment",
        env_id="NLP_MODEL_SENTIMENT_ID",
        env_enabled="NLP_MODEL_SENTIMENT_ENABLED",
        default_id="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
        pipeline_task="zero-shot-classification",
        description="DeBERTa Zero-Shot Sentiment Analyzer (SECONDARY)",
    ),
    ModelConfig(
        name="emotions",
        env_id="NLP_MODEL_EMOTIONS_ID",
        env_enabled="NLP_MODEL_EMOTIONS_ENABLED",
        default_id="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
        pipeline_task="zero-shot-classification",
        description="DeBERTa Zero-Shot Emotions Analyzer (SUPPLEMENTARY)",
    ),
    ModelConfig(
        name="irony",
        env_id="NLP_MODEL_IRONY_ID",
        env_enabled="NLP_MODEL_IRONY_ENABLED",
        default_id="cardiffnlp/twitter-roberta-base-irony",
        pipeline_task="text-classification",
        description="Cardiff Irony Detector (GATEKEEPER)",
    ),
]


# =============================================================================
# Model Initializer Class
# =============================================================================

class ModelInitializer:
    """
    Initializes HuggingFace models at runtime.

    Downloads and caches models to the configured HF_HOME directory.
    Leverages HuggingFace's built-in caching to skip downloads when
    models are already cached and up-to-date.

    Clean Architecture v5.1 Compliance:
    - Factory function: create_model_initializer()
    - Environment variable reuse (Rule #7)
    - Resilient error handling (Rule #5)
    """

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the ModelInitializer.

        Args:
            cache_dir: Override for HF_HOME cache directory
        """
        self.cache_dir = cache_dir or os.environ.get("HF_HOME", "./models-cache")
        self._results: Dict[str, bool] = {}
        self._timing: Dict[str, float] = {}

        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)

        logger.info(f"🗂️  Model cache directory: {self.cache_dir}")

    def _is_model_enabled(self, config: ModelConfig) -> bool:
        """Check if a model is enabled via environment variable."""
        enabled_str = os.environ.get(config.env_enabled, "true").lower()
        return enabled_str in ("true", "1", "yes", "on")

    def _get_model_id(self, config: ModelConfig) -> str:
        """Get model ID from environment or default."""
        return os.environ.get(config.env_id, config.default_id)

    def initialize_model(self, config: ModelConfig) -> Tuple[bool, float]:
        """
        Initialize a single model.

        Downloads the model if not cached, or verifies cache is current.

        Args:
            config: Model configuration

        Returns:
            Tuple of (success: bool, time_seconds: float)
        """
        model_id = self._get_model_id(config)

        if not self._is_model_enabled(config):
            logger.info(f"⏭️  {config.name}: SKIPPED (disabled)")
            return True, 0.0

        logger.info(f"📥 {config.name}: Initializing {model_id}...")
        logger.info(f"   └─ {config.description}")

        start_time = time.perf_counter()

        try:
            # Import here to avoid loading transformers if not needed
            from transformers import pipeline

            # Create pipeline - this triggers download/cache verification
            # HuggingFace automatically:
            # - Uses cached model if available and current
            # - Downloads if missing or outdated
            # - Performs lightweight version check
            _pipe = pipeline(
                task=config.pipeline_task,
                model=model_id,
                device=-1,  # CPU for initialization (GPU assigned at runtime)
            )

            # Release memory - we just needed to cache the model
            del _pipe

            elapsed = time.perf_counter() - start_time
            logger.info(f"✅ {config.name}: Ready ({elapsed:.1f}s)")

            return True, elapsed

        except Exception as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"❌ {config.name}: FAILED after {elapsed:.1f}s")
            logger.error(f"   └─ Error: {e}")

            # Resilient behavior (Rule #5): Log but don't crash
            # Lazy loading will retry at runtime
            return False, elapsed

    def initialize_all(self) -> Dict[str, bool]:
        """
        Initialize all configured models.

        Returns:
            Dictionary of model_name -> success status
        """
        logger.info("=" * 60)
        logger.info("  Ash-NLP Model Initializer")
        logger.info(f"  Version: {__version__}")
        logger.info("=" * 60)
        logger.info("")

        total_start = time.perf_counter()

        for config in MODEL_CONFIGS:
            success, elapsed = self.initialize_model(config)
            self._results[config.name] = success
            self._timing[config.name] = elapsed

        total_elapsed = time.perf_counter() - total_start

        # Summary
        logger.info("")
        logger.info("=" * 60)
        logger.info("  Initialization Summary")
        logger.info("=" * 60)

        success_count = sum(1 for s in self._results.values() if s)
        total_count = len(self._results)

        for name, success in self._results.items():
            status = "✅ Ready" if success else "❌ Failed"
            time_str = f"{self._timing[name]:.1f}s" if self._timing[name] > 0 else "skipped"
            logger.info(f"  {name:12} : {status} ({time_str})")

        logger.info("-" * 60)
        logger.info(f"  Total: {success_count}/{total_count} models ready")
        logger.info(f"  Time:  {total_elapsed:.1f}s")
        logger.info("=" * 60)

        return self._results

    def is_ready(self) -> bool:
        """
        Check if initialization was successful.

        At minimum, BART (primary model) must be ready.

        Returns:
            True if system is ready for inference
        """
        return self._results.get("bart", False)

    def get_results(self) -> Dict[str, bool]:
        """Get initialization results."""
        return self._results.copy()


# =============================================================================
# Factory Function - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================

def create_model_initializer(
    cache_dir: Optional[str] = None,
) -> ModelInitializer:
    """
    Factory function for ModelInitializer.

    Args:
        cache_dir: Override for HF_HOME cache directory

    Returns:
        Configured ModelInitializer instance

    Example:
        >>> initializer = create_model_initializer()
        >>> results = initializer.initialize_all()
        >>> if initializer.is_ready():
        ...     print("Models ready!")
    """
    return ModelInitializer(cache_dir=cache_dir)


# =============================================================================
# Convenience Functions
# =============================================================================

def initialize_models_sync(cache_dir: Optional[str] = None) -> bool:
    """
    Synchronously initialize all models.

    Convenience function for simple use cases.

    Args:
        cache_dir: Override for HF_HOME cache directory

    Returns:
        True if initialization successful (at least BART ready)

    Example:
        >>> if initialize_models_sync():
        ...     print("Ready to start server!")
    """
    initializer = create_model_initializer(cache_dir=cache_dir)
    initializer.initialize_all()
    return initializer.is_ready()


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> int:
    """
    Main entry point for command-line execution.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    logger.info("")
    logger.info("🚀 Starting Ash-NLP Model Initialization...")
    logger.info("")

    success = initialize_models_sync()

    if success:
        logger.info("")
        logger.info("✅ Model initialization complete - ready to start server")
        logger.info("")
        return 0
    else:
        logger.warning("")
        logger.warning("⚠️  Model initialization incomplete - BART not ready")
        logger.warning("   Server will attempt lazy loading at runtime")
        logger.warning("")
        # Return 0 anyway - resilient behavior allows lazy loading fallback
        # Only return 1 if we want to prevent server startup entirely
        return 0


if __name__ == "__main__":
    sys.exit(main())
