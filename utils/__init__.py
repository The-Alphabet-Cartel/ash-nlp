# ash-nlp/utils/__init__.py
"""
Utility Packages for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-10.7-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.7 - Community Pattern Consolidation
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Community patterns consolidated into CrisisPatternManager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

# Context analysis utilities
from .context_helpers import (
    extract_context_signals,
    detect_negation_context,
    analyze_sentiment_context,
    perform_enhanced_context_analysis,
    score_term_in_context
)

# PHASE 3D STEP 10.6: Scoring functions migrated to CrisisAnalyzer
# scoring_helpers imports removed - functions now available as CrisisAnalyzer methods

# PHASE 3D STEP 10.7: Community pattern functions migrated to CrisisPatternManager
# community_patterns imports removed - functions now available as CrisisPatternManager methods

# Enhanced learning utilities (for Step 10.9)
try:
    from .enhanced_learning import EnhancedLearningManager, add_enhanced_learning_endpoints
except ImportError:
    # Enhanced learning not yet implemented
    EnhancedLearningManager = None
    add_enhanced_learning_endpoints = None

# Utility metadata - Updated for Phase 3d Step 10.7
UTILITY_FUNCTIONS = {
    "context_analysis": {
        "extract_context_signals": "Extract contextual signals from messages",
        "detect_negation_context": "Detect negation that affects crisis interpretation",
        "analyze_sentiment_context": "Analyze sentiment for additional context",
        "perform_enhanced_context_analysis": "Enhanced context analysis with community awareness",
        "score_term_in_context": "Score community term relevance in message context"
    },
    
    "scoring_and_analysis": {
        # PHASE 3D STEP 10.6: These functions are now CrisisAnalyzer instance methods
        "extract_depression_score": "Consolidated into CrisisAnalyzer.extract_depression_score()",
        "enhanced_depression_analysis": "Consolidated into CrisisAnalyzer.enhanced_depression_analysis()",
        "advanced_idiom_detection": "Consolidated into CrisisAnalyzer.advanced_idiom_detection()", 
        "enhanced_crisis_level_mapping": "Consolidated into CrisisAnalyzer.enhanced_crisis_level_mapping()",
        "score_phrases_with_models": "Consolidated into CrisisAnalyzer.score_phrases_with_models()",
        "filter_and_rank_phrases": "Consolidated into CrisisAnalyzer.filter_and_rank_phrases()"
    },
    
    "community_patterns": {
        # PHASE 3D STEP 10.7: These functions are now CrisisPatternManager instance methods
        "extract_community_patterns": "Consolidated into CrisisPatternManager.extract_community_patterns()",
        "extract_crisis_context_phrases": "Consolidated into CrisisPatternManager.extract_crisis_context_phrases()",
        "analyze_temporal_indicators": "Consolidated into CrisisPatternManager.analyze_temporal_indicators()",
        "apply_context_weights": "Consolidated into CrisisPatternManager.apply_context_weights()",
        "check_enhanced_crisis_patterns": "Consolidated into CrisisPatternManager.check_enhanced_crisis_patterns()"
    },
    
    "migration_status": {
        "phase_3d_step_10_6": "✅ Scoring functions consolidated into CrisisAnalyzer",
        "phase_3d_step_10_7": "✅ Community pattern functions consolidated into CrisisPatternManager",
        "utils_scoring_helpers": "🗑️ Eliminated - functions moved to CrisisAnalyzer",
        "utils_community_patterns": "🗑️ Eliminated - functions moved to CrisisPatternManager",
        "clean_architecture": "✅ Clean v3.1 compliance achieved"
    },
    
    "remaining_consolidation_targets": {
        "utils_context_helpers": "⏳ Pending Step 10.8 - create ContextPatternManager"
    }
}

def get_utility_functions():
    """Get information about available utility functions"""
    return UTILITY_FUNCTIONS

def get_context_analysis_capabilities():
    """Get context analysis capabilities"""
    return {
        "signal_types": [
            "positive_words",
            "humor_context", 
            "work_context",
            "idiom_detection",
            "negation_context",
            "temporal_indicators"
        ],
        "community_signals": [
            "temporal_urgency",
            "social_isolation",
            "identity_crisis", 
            "family_rejection",
            "discrimination_fear",
            "support_seeking"
        ]
    }

def get_scoring_capabilities():
    """
    Get scoring capabilities (UPDATED for Step 10.7)
    
    Returns:
        Dictionary describing available scoring methods and their locations
    """
    return {
        "crisis_analysis": {
            "location": "CrisisAnalyzer class methods",
            "scoring_functions": [
                "extract_depression_score", "enhanced_depression_analysis",
                "advanced_idiom_detection", "enhanced_crisis_level_mapping",
                "score_phrases_with_models", "filter_and_rank_phrases"
            ]
        },
        "community_patterns": {
            "location": "CrisisPatternManager class methods", 
            "pattern_functions": [
                "extract_community_patterns", "extract_crisis_context_phrases",
                "analyze_temporal_indicators", "apply_context_weights",
                "check_enhanced_crisis_patterns"
            ]
        },
        "context_analysis": {
            "location": "utils.context_helpers module",
            "context_functions": [
                "extract_context_signals", "detect_negation_context",
                "analyze_sentiment_context", "perform_enhanced_context_analysis",
                "score_term_in_context"
            ]
        }
    }

def get_migration_status():
    """Get current migration status for utility consolidation"""
    return {
        "completed_phases": [
            "Phase 3d Step 10.6: Scoring function consolidation",
            "Phase 3d Step 10.7: Community pattern consolidation"
        ],
        "eliminated_files": [
            "utils/scoring_helpers.py",
            "utils/community_patterns.py"
        ],
        "consolidated_into": {
            "CrisisAnalyzer": "Scoring and analysis functions",
            "CrisisPatternManager": "Community pattern and crisis pattern functions"
        },
        "next_phase": "Step 10.8: Context helper consolidation"
    }

# Deprecation warnings for removed imports
def __getattr__(name):
    """Handle deprecated imports with helpful error messages"""
    if name in ['extract_community_patterns', 'extract_crisis_context_phrases']:
        raise ImportError(
            f"'{name}' has been consolidated into CrisisPatternManager in Step 10.7. "
            f"Use: crisis_pattern_manager.{name}(message) instead of utils.{name}(message)"
        )
    elif name in ['extract_depression_score', 'enhanced_depression_analysis', 
                  'advanced_idiom_detection', 'enhanced_crisis_level_mapping']:
        raise ImportError(
            f"'{name}' has been consolidated into CrisisAnalyzer in Step 10.6. "
            f"Use: crisis_analyzer.{name}(message) instead of utils.{name}(message)"
        )
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")