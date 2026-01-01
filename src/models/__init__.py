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
FILE VERSION: v5.0-3-4.2-6
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.2 - Model Wrapper Package
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package contains all model wrappers for the Ash-NLP ensemble:

MODELS:
- BART Crisis Classifier (PRIMARY, weight 0.50)
- Cardiff Sentiment Analyzer (SECONDARY, weight 0.25)
- Cardiff Irony Detector (TERTIARY, weight 0.15)
- RoBERTa Emotions Classifier (SUPPLEMENTARY, weight 0.10)

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
__version__ = "v5.0-3-4.2-6"

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
# Model Wrappers and Factory Functions
# =============================================================================

# BART Crisis Classifier - PRIMARY (weight 0.50)
from .bart_classifier import (
    BARTCrisisClassifier,
    create_bart_classifier,
    DEFAULT_CRISIS_LABELS,
)

# Cardiff Sentiment Analyzer - SECONDARY (weight 0.25)
from .sentiment import (
    SentimentAnalyzer,
    create_sentiment_analyzer,
    SENTIMENT_LABELS,
)

# Cardiff Irony Detector - TERTIARY (weight 0.15)
from .irony import (
    IronyDetector,
    create_irony_detector,
    IRONY_LABELS,
)

# RoBERTa Emotions Classifier - SUPPLEMENTARY (weight 0.10)
from .emotions import (
    EmotionsClassifier,
    create_emotions_classifier,
    GOEMOTION_LABELS,
    CRISIS_EMOTIONS,
    POSITIVE_EMOTIONS,
    NEUTRAL_EMOTIONS,
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
    "sentiment": SentimentAnalyzer,
    "irony": IronyDetector,
    "emotions": EmotionsClassifier,
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
    "ModelResult",
    "ModelInfo",
    "ModelRole",
    "ModelTask",
    # BART Crisis Classifier
    "BARTCrisisClassifier",
    "create_bart_classifier",
    "DEFAULT_CRISIS_LABELS",
    # Sentiment Analyzer
    "SentimentAnalyzer",
    "create_sentiment_analyzer",
    "SENTIMENT_LABELS",
    # Irony Detector
    "IronyDetector",
    "create_irony_detector",
    "IRONY_LABELS",
    # Emotions Classifier
    "EmotionsClassifier",
    "create_emotions_classifier",
    "GOEMOTION_LABELS",
    "CRISIS_EMOTIONS",
    "POSITIVE_EMOTIONS",
    "NEUTRAL_EMOTIONS",
    # Convenience functions
    "create_model",
    "MODEL_FACTORIES",
    "MODEL_CLASSES",
    "DEFAULT_WEIGHTS",
]
