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
Context Analysis Package for Ash-NLP Service - Phase 5
---
FILE VERSION: v5.0-5-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package provides context-aware crisis analysis by examining message history:

PHASE 5 COMPONENTS:
- ContextAnalyzer: Main orchestrator for context-aware analysis
- EscalationDetector: Detects escalation patterns across message sequences
- TemporalDetector: Detects time-based patterns (late night, rapid posting)
- TrendAnalyzer: Analyzes trend direction and velocity

KEY ARCHITECTURAL DECISION:
Ash-NLP remains STATELESS. Message history is provided by Ash-Bot in each request.
This enables horizontal scaling and maintains clean separation of concerns.

USAGE:
    from src.context import create_context_analyzer, MessageHistoryItem

    # Create the analyzer
    analyzer = create_context_analyzer()

    # Analyze message with history
    result = analyzer.analyze(
        current_message="I can't do this anymore",
        current_score=0.85,
        message_history=[
            MessageHistoryItem(
                message="Not having the best day", 
                timestamp=datetime(2026, 1, 1, 16, 0),
                crisis_score=0.25,
            ),
            MessageHistoryItem(
                message="Things are getting harder", 
                timestamp=datetime(2026, 1, 1, 18, 0),
                crisis_score=0.45,
            ),
        ],
    )

    if result.escalation.detected:
        print(f"Escalation: {result.escalation.rate}")
        print(f"Pattern: {result.escalation.pattern}")
        print(f"Urgency: {result.intervention.urgency}")
"""

# Module version
__version__ = "v5.0-5-1.0-1"

# =============================================================================
# Context Analyzer (Main Interface)
# =============================================================================

from .context_analyzer import (
    # Urgency enum
    InterventionUrgency,
    # Input data classes
    MessageHistoryItem,
    MessageSequence,
    # Output data classes
    EscalationResult,
    TemporalResult,
    TrendResult,
    TrajectoryInfo,
    InterventionInfo,
    HistoryMetadata,
    ContextAnalysisResult,
    # Main analyzer
    ContextAnalyzer,
    create_context_analyzer,
)

# =============================================================================
# Escalation Detection
# =============================================================================

from .escalation_detector import (
    # Enums
    EscalationType,
    # Data classes
    EscalationAnalysis,
    # Detector class
    EscalationDetector,
    create_escalation_detector,
)

# =============================================================================
# Temporal Detection
# =============================================================================

from .temporal_detector import (
    # Enums
    TimeOfDayRisk,
    PostingFrequency,
    # Data classes
    TemporalAnalysis,
    # Detector class
    TemporalDetector,
    create_temporal_detector,
)

# =============================================================================
# Trend Analysis
# =============================================================================

from .trend_analyzer import (
    # Enums
    TrendDirection,
    TrendVelocity,
    # Data classes
    TrendAnalysis,
    # Analyzer class
    TrendAnalyzer,
    create_trend_analyzer,
)

# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Version
    "__version__",
    
    # =========================================================================
    # INPUT DATA CLASSES
    # =========================================================================
    "MessageHistoryItem",
    "MessageSequence",
    
    # =========================================================================
    # OUTPUT DATA CLASSES
    # =========================================================================
    "EscalationResult",
    "TemporalResult",
    "TrendResult",
    "TrajectoryInfo",
    "InterventionInfo",
    "HistoryMetadata",
    "ContextAnalysisResult",
    
    # =========================================================================
    # CONTEXT ANALYZER (Main Interface)
    # =========================================================================
    "InterventionUrgency",
    "ContextAnalyzer",
    "create_context_analyzer",
    
    # =========================================================================
    # ESCALATION DETECTION
    # =========================================================================
    "EscalationType",
    "EscalationAnalysis",
    "EscalationDetector",
    "create_escalation_detector",
    
    # =========================================================================
    # TEMPORAL DETECTION
    # =========================================================================
    "TimeOfDayRisk",
    "PostingFrequency",
    "TemporalAnalysis",
    "TemporalDetector",
    "create_temporal_detector",
    
    # =========================================================================
    # TREND ANALYSIS
    # =========================================================================
    "TrendDirection",
    "TrendVelocity",
    "TrendAnalysis",
    "TrendAnalyzer",
    "create_trend_analyzer",
]
