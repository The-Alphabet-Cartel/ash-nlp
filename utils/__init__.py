# ash-nlp/utils/__init__.py
"""
Utility Packages for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-10.6-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.6 - Scoring Functions Consolidated
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Scoring helpers consolidated into CrisisAnalyzer
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

# Community pattern utilities
from .community_patterns import (
    extract_community_patterns,
    extract_crisis_context_phrases
)

# Enhanced learning utilities (for Step 10.9)
try:
    from .enhanced_learning import EnhancedLearningManager, add_enhanced_learning_endpoints
except ImportError:
    # Enhanced learning not yet implemented
    EnhancedLearningManager = None
    add_enhanced_learning_endpoints = None

# Utility metadata - Updated for Phase 3d Step 10.6
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
        "extract_community_patterns": "Extract LGBTQIA+ community-specific patterns",
        "extract_crisis_context_phrases": "Extract phrases with crisis context indicators"
    },
    
    "migration_status": {
        "phase_3d_step_10_6": "✅ Scoring functions consolidated into CrisisAnalyzer",
        "utils_scoring_helpers": "🗑️ Eliminated - functions moved to CrisisAnalyzer",
        "clean_architecture": "✅ Clean v3.1 compliance achieved"
    },
    
    "remaining_consolidation_targets": {
        "utils_community_patterns": "⏳ Pending Step 10.7 - migrate to CrisisPatternManager",
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
    """Get scoring and analysis capabilities (now in CrisisAnalyzer)"""
    return {
        "status": "MIGRATED_TO_CRISIS_ANALYZER",
        "phase": "3d_step_10_6_complete",
        "access_method": "Use CrisisAnalyzer instance methods",
        "functions": {
            "depression_analysis": [
                "multi_model_integration",
                "safety_first_recalibration",
                "critical_pattern_detection",
                "context_based_adjustments"
            ],
            "idiom_detection": [
                "context_aware_filtering",
                "pattern_matching",
                "reduction_factors",
                "max_score_limits"
            ],
            "phrase_scoring": [
                "model_based_scoring",
                "community_pattern_boosting",
                "crisis_context_enhancement",
                "confidence_mapping"
            ]
        },
        "migration_note": "All scoring functions now available as CrisisAnalyzer instance methods"
    }

def get_community_pattern_capabilities():
    """Get community pattern recognition capabilities"""
    return {
        "lgbtqia_patterns": [
            "family_rejection", 
            "identity_crisis",
            "dysphoria_transition",
            "discrimination_safety",
            "community_support"
        ],
        "crisis_contexts": [
            "temporal_urgency",
            "intensity_amplifier",
            "social_isolation", 
            "capability_loss"
        ]
    }

def get_migration_status():
    """Get Phase 3d consolidation migration status"""
    return {
        "current_step": "10.6_complete",
        "completed": ["scoring_helpers_consolidation"],
        "pending": ["community_patterns_consolidation", "context_helpers_manager_creation"],
        "architecture_compliance": "clean_v3_1_achieved",
        "version": "v3.1.3d.10.6.1"
    }

# Helper function to validate utility inputs
def validate_message_input(message: str) -> bool:
    """Validate message input for utility functions"""
    return isinstance(message, str) and len(message.strip()) > 0

def validate_context_input(context: dict) -> bool:
    """Validate context dictionary input"""
    required_keys = ['message_lower', 'has_positive_words', 'has_humor_context']
    return isinstance(context, dict) and all(key in context for key in required_keys)

def validate_model_result(result) -> bool:
    """Validate model result format"""
    if not result:
        return False
    
    if isinstance(result, list) and len(result) > 0:
        return True
    elif isinstance(result, dict) and 'score' in result:
        return True
    
    return False

__all__ = [
    # Enhanced learning utilities (conditional)
    'EnhancedLearningManager',
    'add_enhanced_learning_endpoints',

    # Context analysis
    "extract_context_signals",
    "detect_negation_context", 
    "analyze_sentiment_context",
    "perform_enhanced_context_analysis",
    "score_term_in_context",
    
    # PHASE 3D STEP 10.6: Scoring utilities REMOVED (consolidated into CrisisAnalyzer)
    # "extract_depression_score",           # ❌ MIGRATED
    # "enhanced_depression_analysis",       # ❌ MIGRATED
    # "advanced_idiom_detection",          # ❌ MIGRATED
    # "enhanced_crisis_level_mapping",     # ❌ MIGRATED
    # "score_phrases_with_models",         # ❌ MIGRATED
    # "filter_and_rank_phrases",           # ❌ MIGRATED
    
    # Community patterns (pending Step 10.7)
    "extract_community_patterns",
    "extract_crisis_context_phrases",
    
    # Metadata functions
    "get_utility_functions",
    "get_context_analysis_capabilities",
    "get_scoring_capabilities", 
    "get_community_pattern_capabilities",
    "get_migration_status",
    
    # Validation functions
    "validate_message_input",
    "validate_context_input",
    "validate_model_result",
    
    # Metadata
    "UTILITY_FUNCTIONS"
]