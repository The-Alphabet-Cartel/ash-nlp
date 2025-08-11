# ash-nlp/utils/__init__.py
"""
Utilities Package for Ash NLP Service v3.1
Clean v3.1 Architecture
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

# Scoring utilities  
from .scoring_helpers import (
    extract_depression_score,
    enhanced_depression_analysis,
    advanced_idiom_detection,
    enhanced_crisis_level_mapping,
    score_phrases_with_models,
    filter_and_rank_phrases
)

# Community pattern utilities
from .community_patterns import (
    extract_community_patterns,
    extract_crisis_context_phrases
)

# Utility metadata
UTILITY_FUNCTIONS = {
    "context_analysis": {
        "extract_context_signals": "Extract contextual signals from messages",
        "detect_negation_context": "Detect negation that affects crisis interpretation",
        "analyze_sentiment_context": "Analyze sentiment for additional context",
        "perform_enhanced_context_analysis": "Enhanced context analysis with community awareness",
        "score_term_in_context": "Score community term relevance in message context"
    },
    
    "scoring_and_analysis": {
        "extract_depression_score": "Extract depression score from model output",
        "enhanced_depression_analysis": "Enhanced depression analysis with safety-first approach",
        "advanced_idiom_detection": "Advanced idiom detection with context verification", 
        "enhanced_crisis_level_mapping": "Map confidence scores to crisis levels",
        "score_phrases_with_models": "Score extracted phrases using ML models",
        "filter_and_rank_phrases": "Filter and rank phrases by relevance and confidence"
    },
    
    "community_patterns": {
        "extract_community_patterns": "Extract LGBTQIA+ community-specific patterns",
        "extract_crisis_context_phrases": "Extract phrases with crisis context indicators"
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
    """Get scoring and analysis capabilities"""
    return {
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
    # Learning utilities
    'EnhancedLearningManager',
    'add_enhanced_learning_endpoints',

    # Context analysis
    "extract_context_signals",
    "detect_negation_context", 
    "analyze_sentiment_context",
    "perform_enhanced_context_analysis",
    "score_term_in_context",
    
    # Scoring utilities
    "extract_depression_score",
    "enhanced_depression_analysis",
    "advanced_idiom_detection",
    "enhanced_crisis_level_mapping",
    "score_phrases_with_models",
    "filter_and_rank_phrases",
    
    # Community patterns
    "extract_community_patterns",
    "extract_crisis_context_phrases",
    
    # Metadata functions
    "get_utility_functions",
    "get_context_analysis_capabilities",
    "get_scoring_capabilities", 
    "get_community_pattern_capabilities",
    
    # Validation functions
    "validate_message_input",
    "validate_context_input",
    "validate_model_result",
    
    # Metadata
    "UTILITY_FUNCTIONS"
]