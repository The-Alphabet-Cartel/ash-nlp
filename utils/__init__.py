"""
Utilities Package for Ash NLP Service
Helper functions and utilities for context analysis, scoring, and community patterns
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
    enhanced_crisis_level_mapping
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
        "enhanced_crisis_level_mapping": "Map confidence scores to crisis levels"
    },
    
    "community_patterns": {
        "extract_community_patterns": "Extract LGBTQIA+ community-specific patterns",
        "extract_crisis_context_phrases": "Extract crisis-context phrases from messages"
    }
}

def get_utility_capabilities():
    """Get information about available utility functions"""
    return UTILITY_FUNCTIONS

def get_context_analysis_functions():
    """Get list of available context analysis functions"""
    return list(UTILITY_FUNCTIONS["context_analysis"].keys())

def get_scoring_functions():
    """Get list of available scoring and analysis functions"""
    return list(UTILITY_FUNCTIONS["scoring_and_analysis"].keys())

def get_community_pattern_functions():
    """Get list of available community pattern functions"""
    return list(UTILITY_FUNCTIONS["community_patterns"].keys())

__all__ = [
    # Context analysis utilities
    "extract_context_signals",
    "detect_negation_context", 
    "analyze_sentiment_context",
    "perform_enhanced_context_analysis",
    "score_term_in_context",
    
    # Scoring utilities (cleaned - removed phrase-specific functions)
    "extract_depression_score",
    "enhanced_depression_analysis",
    "advanced_idiom_detection",
    "enhanced_crisis_level_mapping",
    
    # Community pattern utilities
    "extract_community_patterns",
    "extract_crisis_context_phrases",
    
    # Metadata functions
    "get_utility_capabilities",
    "get_context_analysis_functions", 
    "get_scoring_functions",
    "get_community_pattern_functions"
]