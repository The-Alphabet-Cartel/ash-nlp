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
Models Package for Ash-NLP Service
---
FILE VERSION: v5.1-5-5.5-1
LAST MODIFIED: 2026-02-09
PHASE: Phase 5 - Emotions Zero-Shot Migration
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package contains all model wrappers for the Ash-NLP ensemble:

MODELS:
- BART Crisis Classifier (PRIMARY, weight 0.50) [Phase 4.5 - v5.1 ZeroShotModelWrapper]
- DeBERTa Sentiment Zero-Shot Analyzer (SECONDARY, weight 0.25) [Phase 4 - v5.1]
- Cardiff Irony Detector (TERTIARY, weight 0.15)
- DeBERTa Emotions Zero-Shot Analyzer (SUPPLEMENTARY, weight 0.10) [Phase 5 - v5.1]

USAGE:
    from src.models import (
        create_bart_classifier,
        create_sentiment_analyzer,
        create_irony_detector,
        create_emotions_classifier,
    )

    # Create models with factory functions
    bart = create_bart_classifier(config_manager=config)
    sentiment = create_sentiment_analyzer(config_manager=config)
    irony = create_irony_detector(config_manager=config)
    emotions = create_emotions_classifier(config_manager=config)

    # Analyze text
    result = bart.analyze("I'm feeling really down today")
"""

# Module version
__version__ = "v5.1-5-5.5-1"

# =============================================================================
# Base Classes and Data Types
# =============================================================================

from .base import (
    BaseModelWrapper,
    ModelResult,
    ModelInfo,
    ModelRole,
    ModelTask,
)

# =============================================================================
# Zero-Shot Abstraction Layer (Phase 3 - v5.1 Migration)
# =============================================================================

from .zero_shot_base import ZeroShotModelWrapper

# =============================================================================
# Model Wrappers and Factory Functions
# =============================================================================

# BART Crisis Classifier - PRIMARY (weight 0.50)
# Phase 4.5: Migrated to ZeroShotModelWrapper with descriptive NLI labels
from .bart_classifier import (
    BARTCrisisClassifier,
    create_bart_classifier,
    DEFAULT_CRISIS_LABELS,
    DEFAULT_LABEL_SIGNAL_MAPPING as BART_DEFAULT_LABEL_SIGNAL_MAPPING,
    CRITICAL_SIGNAL_THRESHOLD,
)

# DeBERTa Sentiment Zero-Shot Analyzer - SECONDARY (weight 0.25)
# Phase 4: Migrated from Cardiff text-classification to DeBERTa zero-shot
from .sentiment import (
    SentimentZeroShotAnalyzer,
    create_sentiment_analyzer,
    DEFAULT_CANDIDATE_LABELS,
    DEFAULT_LABEL_SIGNAL_MAPPING,
)

# Cardiff Irony Detector - TERTIARY (weight 0.15)
from .irony import (
    IronyDetector,
    create_irony_detector,
    IRONY_LABELS,
)

# DeBERTa Emotions Zero-Shot Analyzer - SUPPLEMENTARY (weight 0.10)
# Phase 5: Migrated from RoBERTa text-classification to DeBERTa zero-shot
from .emotions import (
    EmotionsZeroShotAnalyzer,
    create_emotions_classifier,
    DEFAULT_EMOTIONS_CANDIDATE_LABELS,
    DEFAULT_EMOTIONS_LABEL_SIGNAL_MAPPING,
)

# =============================================================================
# Convenience Mapping
# =============================================================================

# Map model names to factory functions
MODEL_FACTORIES = {
    "bart": create_bart_classifier,
    "bart_crisis": create_bart_classifier,
    "sentiment": create_sentiment_analyzer,
    "irony": create_irony_detector,
    "emotions": create_emotions_classifier,
}

# Map model names to classes
MODEL_CLASSES = {
    "bart": BARTCrisisClassifier,
    "bart_crisis": BARTCrisisClassifier,
    "sentiment": SentimentZeroShotAnalyzer,
    "irony": IronyDetector,
    "emotions": EmotionsZeroShotAnalyzer,
}

# Default model weights
DEFAULT_WEIGHTS = {
    "bart": 0.50,
    "sentiment": 0.25,
    "irony": 0.15,
    "emotions": 0.10,
}


def create_model(model_name: str, **kwargs):
    """
    Create a model by name using the appropriate factory function.

    Args:
        model_name: Name of the model (bart, sentiment, irony, emotions)
        **kwargs: Arguments passed to factory function

    Returns:
        Configured model wrapper instance

    Raises:
        ValueError: If model_name is not recognized

    Example:
        >>> model = create_model("bart", config_manager=config)
        >>> model = create_model("sentiment", device="cuda")
    """
    factory = MODEL_FACTORIES.get(model_name.lower())

    if factory is None:
        valid_names = list(MODEL_FACTORIES.keys())
        raise ValueError(f"Unknown model: '{model_name}'. Valid models: {valid_names}")

    return factory(**kwargs)


# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Version
    "__version__",
    # Base classes and types
    "BaseModelWrapper",
    "ZeroShotModelWrapper",
    "ModelResult",
    "ModelInfo",
    "ModelRole",
    "ModelTask",
    # BART Crisis Classifier (Phase 4.5)
    "BARTCrisisClassifier",
    "create_bart_classifier",
    "DEFAULT_CRISIS_LABELS",
    "BART_DEFAULT_LABEL_SIGNAL_MAPPING",
    "CRITICAL_SIGNAL_THRESHOLD",
    # Sentiment Zero-Shot Analyzer (Phase 4)
    "SentimentZeroShotAnalyzer",
    "create_sentiment_analyzer",
    "DEFAULT_CANDIDATE_LABELS",
    "DEFAULT_LABEL_SIGNAL_MAPPING",
    # Irony Detector
    "IronyDetector",
    "create_irony_detector",
    "IRONY_LABELS",
    # Emotions Zero-Shot Analyzer (Phase 5)
    "EmotionsZeroShotAnalyzer",
    "create_emotions_classifier",
    "DEFAULT_EMOTIONS_CANDIDATE_LABELS",
    "DEFAULT_EMOTIONS_LABEL_SIGNAL_MAPPING",
    # Convenience functions
    "create_model",
    "MODEL_FACTORIES",
    "MODEL_CLASSES",
    "DEFAULT_WEIGHTS",
]
