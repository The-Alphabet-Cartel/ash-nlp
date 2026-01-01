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
Ensemble Package for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.3-5
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.3 - Ensemble Package
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package contains the ensemble decision engine and supporting components:

COMPONENTS:
- EnsembleDecisionEngine: Main orchestrator for crisis detection
- ModelLoader: Loads and manages all ensemble models
- WeightedScorer: Calculates weighted crisis scores
- FallbackStrategy: Handles errors and graceful degradation

USAGE:
    from src.ensemble import create_decision_engine

    # Create and initialize the engine
    engine = create_decision_engine(config_manager=config)
    engine.initialize()

    # Analyze a message
    assessment = engine.analyze("I'm feeling really down today")

    if assessment.crisis_detected:
        print(f"Crisis detected: {assessment.severity.value}")
        print(f"Recommended action: {assessment.recommended_action}")
"""

# Module version
__version__ = "v5.0-3-4.3-5"

# =============================================================================
# Decision Engine (Main Interface)
# =============================================================================

from .decision_engine import (
    EnsembleDecisionEngine,
    create_decision_engine,
    CrisisAssessment,
    RecommendedAction,
)

# =============================================================================
# Model Loading
# =============================================================================

from .model_loader import (
    ModelLoader,
    create_model_loader,
    MODEL_NAMES,
)

# =============================================================================
# Scoring System
# =============================================================================

from .scoring import (
    WeightedScorer,
    create_weighted_scorer,
    CrisisSeverity,
    ModelSignal,
    EnsembleScore,
)

# =============================================================================
# Fallback and Error Handling
# =============================================================================

from .fallback import (
    FallbackStrategy,
    create_fallback_strategy,
    CircuitBreaker,
    CircuitState,
    ModelFailureInfo,
    CriticalModelFailure,
    EnsembleDegradedError,
)

# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Version
    "__version__",
    # Decision Engine (Primary Interface)
    "EnsembleDecisionEngine",
    "create_decision_engine",
    "CrisisAssessment",
    "RecommendedAction",
    # Model Loading
    "ModelLoader",
    "create_model_loader",
    "MODEL_NAMES",
    # Scoring
    "WeightedScorer",
    "create_weighted_scorer",
    "CrisisSeverity",
    "ModelSignal",
    "EnsembleScore",
    # Fallback
    "FallbackStrategy",
    "create_fallback_strategy",
    "CircuitBreaker",
    "CircuitState",
    "ModelFailureInfo",
    "CriticalModelFailure",
    "EnsembleDegradedError",
]
