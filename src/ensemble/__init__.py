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
FILE VERSION: v5.0-4-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 - Ensemble Coordinator Enhancement
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package contains the ensemble decision engine and supporting components:

PHASE 3 COMPONENTS:
- EnsembleDecisionEngine: Main orchestrator for crisis detection
- ModelLoader: Loads and manages all ensemble models
- WeightedScorer: Calculates weighted crisis scores
- FallbackStrategy: Handles errors and graceful degradation

PHASE 4 COMPONENTS:
- ConsensusSelector: Multiple consensus algorithms
- ConflictDetector: Detects model disagreements
- ConflictResolver: Resolves conflicts with strategies
- ResultAggregator: Comprehensive result aggregation
- ExplainabilityGenerator: Human-readable explanations

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

PHASE 4 USAGE (Enhanced):
    from src.ensemble import (
        create_consensus_selector,
        create_conflict_detector,
        create_conflict_resolver,
        create_result_aggregator,
        create_explainability_generator,
    )

    # Create Phase 4 components
    consensus = create_consensus_selector(config_manager=config)
    detector = create_conflict_detector(config_manager=config)
    resolver = create_conflict_resolver(config_manager=config)
    aggregator = create_result_aggregator(config_manager=config)
    explainer = create_explainability_generator(config_manager=config)
"""

# Module version
__version__ = "v5.0-4-1.0-1"

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
# Phase 4: Consensus Algorithms
# =============================================================================

from .consensus import (
    # Enums
    ConsensusAlgorithm,
    AgreementLevel,
    # Data classes
    ConsensusResult,
    # Algorithm functions
    weighted_voting_consensus,
    majority_voting_consensus,
    unanimous_consensus,
    conflict_aware_consensus,
    # Selector class
    ConsensusSelector,
    create_consensus_selector,
)

# =============================================================================
# Phase 4: Conflict Detection
# =============================================================================

from .conflict_detector import (
    # Enums
    ConflictType,
    ConflictSeverity,
    # Data classes
    DetectedConflict,
    ConflictReport,
    ModelSignals,
    # Detector class
    ConflictDetector,
    create_conflict_detector,
)

# =============================================================================
# Phase 4: Conflict Resolution
# =============================================================================

from .conflict_resolver import (
    # Enums
    ResolutionStrategy,
    # Data classes
    ResolutionResult,
    # Resolver class
    ConflictResolver,
    create_conflict_resolver,
)

# =============================================================================
# Phase 4: Result Aggregation
# =============================================================================

from .aggregator import (
    # Enums
    CrisisLevel,
    InterventionPriority,
    # Data classes
    ModelResultSummary,
    AggregatedResult,
    # Aggregator class
    ResultAggregator,
    create_result_aggregator,
)

# =============================================================================
# Phase 4: Explainability
# =============================================================================

from .explainability import (
    # Enums
    VerbosityLevel,
    # Data classes
    ModelContribution,
    RecommendedAction as ExplainabilityRecommendedAction,
    Explanation,
    # Generator class
    ExplainabilityGenerator,
    create_explainability_generator,
)

# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Version
    "__version__",
    
    # =========================================================================
    # PHASE 3 COMPONENTS
    # =========================================================================
    
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
    
    # =========================================================================
    # PHASE 4 COMPONENTS
    # =========================================================================
    
    # Consensus Algorithms
    "ConsensusAlgorithm",
    "AgreementLevel",
    "ConsensusResult",
    "weighted_voting_consensus",
    "majority_voting_consensus",
    "unanimous_consensus",
    "conflict_aware_consensus",
    "ConsensusSelector",
    "create_consensus_selector",
    
    # Conflict Detection
    "ConflictType",
    "ConflictSeverity",
    "DetectedConflict",
    "ConflictReport",
    "ModelSignals",
    "ConflictDetector",
    "create_conflict_detector",
    
    # Conflict Resolution
    "ResolutionStrategy",
    "ResolutionResult",
    "ConflictResolver",
    "create_conflict_resolver",
    
    # Result Aggregation
    "CrisisLevel",
    "InterventionPriority",
    "ModelResultSummary",
    "AggregatedResult",
    "ResultAggregator",
    "create_result_aggregator",
    
    # Explainability
    "VerbosityLevel",
    "ModelContribution",
    "ExplainabilityRecommendedAction",
    "Explanation",
    "ExplainabilityGenerator",
    "create_explainability_generator",
]
