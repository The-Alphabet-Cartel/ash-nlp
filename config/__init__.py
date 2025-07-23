"""
Configuration Package for Ash NLP Service
Centralized configuration management and settings
"""

from .nlp_settings import (
    # Core configuration
    SERVER_CONFIG,
    CRISIS_THRESHOLDS,
    DEFAULT_PARAMS,
    
    # Pattern configurations
    POSITIVE_CONTEXT_PATTERNS,
    IDIOM_PATTERNS,
    LGBTQIA_PATTERNS,
    CRISIS_CONTEXTS,
    
    # Analysis configurations
    COMMUNITY_VOCABULARY,
    TEMPORAL_INDICATORS,
    CONTEXT_WEIGHTS,
    
    # Enhanced patterns
    ENHANCED_IDIOM_PATTERNS,
    BURDEN_PATTERNS,
    HOPELESSNESS_PATTERNS,
    STRUGGLE_PATTERNS,
    NEGATION_PATTERNS
)

# Configuration utilities
def get_server_config():
    """Get complete server configuration"""
    return SERVER_CONFIG

def get_crisis_thresholds():
    """Get crisis level mapping thresholds"""
    return CRISIS_THRESHOLDS

def get_default_parameters():
    """Get default parameters for all analysis types"""
    return DEFAULT_PARAMS

def get_lgbtqia_patterns():
    """Get LGBTQIA+ specific pattern configurations"""
    return LGBTQIA_PATTERNS

def get_community_vocabulary():
    """Get community-specific vocabulary for semantic analysis"""
    return COMMUNITY_VOCABULARY

def get_safety_patterns():
    """Get safety-critical patterns that must be detected"""
    return {
        "burden_patterns": BURDEN_PATTERNS,
        "hopelessness_patterns": HOPELESSNESS_PATTERNS, 
        "struggle_patterns": STRUGGLE_PATTERNS
    }

def get_idiom_patterns():
    """Get enhanced idiom patterns for false positive reduction"""
    return {
        "basic_patterns": IDIOM_PATTERNS,
        "enhanced_patterns": ENHANCED_IDIOM_PATTERNS
    }

# Validation functions
def validate_crisis_level(level: str) -> bool:
    """Validate that crisis level is supported"""
    return level in ['none', 'low', 'medium', 'high']

def validate_confidence_score(score: float) -> bool:
    """Validate that confidence score is in valid range"""
    return 0.0 <= score <= 1.0

def get_threshold_for_level(level: str) -> float:
    """Get confidence threshold for crisis level"""
    return CRISIS_THRESHOLDS.get(level, 0.0)

# Service capabilities
SERVICE_CAPABILITIES = {
    "crisis_analysis": {
        "description": "Multi-model crisis detection with safety-first approach",
        "models": ["depression", "sentiment"],
        "features": ["context_analysis", "idiom_filtering", "pattern_boosting"]
    },
    "phrase_extraction": {
        "description": "Extract crisis keywords using model scoring",
        "methods": ["ngram_extraction", "community_patterns", "crisis_context"],
        "output": "scored_phrase_candidates"
    },
    "pattern_learning": {
        "description": "Learn patterns from community message history", 
        "input": "message_batches",
        "output": "keyword_recommendations"
    },
    "semantic_analysis": {
        "description": "Enhanced context analysis with community awareness",
        "features": ["community_vocabulary", "context_hints", "lgbtqia_patterns"]
    }
}

def get_service_capabilities():
    """Get detailed service capabilities"""
    return SERVICE_CAPABILITIES

__all__ = [
    # Core configuration
    "SERVER_CONFIG",
    "CRISIS_THRESHOLDS", 
    "DEFAULT_PARAMS",
    
    # Pattern configurations
    "POSITIVE_CONTEXT_PATTERNS",
    "IDIOM_PATTERNS",
    "LGBTQIA_PATTERNS", 
    "CRISIS_CONTEXTS",
    "ENHANCED_IDIOM_PATTERNS",
    
    # Safety patterns
    "BURDEN_PATTERNS",
    "HOPELESSNESS_PATTERNS",
    "STRUGGLE_PATTERNS",
    "NEGATION_PATTERNS",
    
    # Community data
    "COMMUNITY_VOCABULARY",
    "TEMPORAL_INDICATORS",
    "CONTEXT_WEIGHTS",
    
    # Utility functions
    "get_server_config",
    "get_crisis_thresholds",
    "get_default_parameters",
    "get_lgbtqia_patterns",
    "get_community_vocabulary",
    "get_safety_patterns",
    "get_idiom_patterns",
    
    # Validation functions
    "validate_crisis_level",
    "validate_confidence_score", 
    "get_threshold_for_level",
    
    # Service info
    "SERVICE_CAPABILITIES",
    "get_service_capabilities"
]