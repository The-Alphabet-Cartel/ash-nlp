"""
Configuration Package for Ash NLP Service
Centralized configuration management and settings
Enhanced with secrets support for secure API key management
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

# Import new secrets-aware configuration manager
from .nlp_config_manager import (
    NLPConfigManager,
    get_nlp_config,
    get_env_config,
    get_crisis_thresholds as get_enhanced_crisis_thresholds,
    get_server_config as get_enhanced_server_config
)

# Configuration utilities (existing)
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

# Validation functions (existing)
def validate_crisis_level(level: str) -> bool:
    """Validate that crisis level is supported"""
    return level in ['none', 'low', 'medium', 'high']

def validate_confidence_score(score: float) -> bool:
    """Validate that confidence score is in valid range"""
    return 0.0 <= score <= 1.0

def get_threshold_for_level(level: str) -> float:
    """Get confidence threshold for crisis level"""
    return CRISIS_THRESHOLDS.get(level, 0.0)

# Enhanced configuration functions (new - with secrets support)
def get_secrets_aware_config():
    """Get configuration manager with secrets support"""
    return get_nlp_config()

def get_enhanced_thresholds():
    """Get crisis thresholds with environment variable overrides"""
    return get_enhanced_crisis_thresholds()

def get_enhanced_server_config():
    """Get server config with secrets and environment variables"""
    return get_enhanced_server_config()

def has_api_key(key_name: str) -> bool:
    """Check if API key is available (from secrets or environment)"""
    config_manager = get_nlp_config()
    return bool(config_manager.get(key_name.upper()))

def get_api_keys_status():
    """Get status of all API keys"""
    config_manager = get_nlp_config()
    return {
        'claude_api_key': bool(config_manager.get('CLAUDE_API_KEY')),
        'huggingface_token': bool(config_manager.get('HUGGINGFACE_TOKEN')),
        'openai_api_key': bool(config_manager.get('OPENAI_API_KEY'))
    }

# Service capabilities (existing)
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
    },
    "secrets_management": {
        "description": "Secure API key management with file-based secrets",
        "features": ["windows_support", "environment_fallback", "automatic_detection"],
        "supported_keys": ["claude_api_key", "huggingface_token", "openai_api_key"]
    }
}

def get_service_capabilities():
    """Get detailed service capabilities"""
    return SERVICE_CAPABILITIES

# Enhanced service info with secrets support
def get_enhanced_service_info():
    """Get comprehensive service information including secrets status"""
    config_manager = get_nlp_config()
    api_keys_status = get_api_keys_status()
    
    return {
        "service_name": "Ash NLP Service",
        "version": "4.4.0",
        "configuration": {
            "secrets_enabled": any(api_keys_status.values()),
            "api_keys_available": api_keys_status,
            "using_environment_fallback": not any(api_keys_status.values()),
            "crisis_thresholds": get_enhanced_thresholds(),
            "hardware_optimized": True
        },
        "capabilities": SERVICE_CAPABILITIES,
        "patterns_loaded": {
            "lgbtqia_patterns": len(LGBTQIA_PATTERNS),
            "idiom_patterns": len(IDIOM_PATTERNS),
            "burden_patterns": len(BURDEN_PATTERNS),
            "hopelessness_patterns": len(HOPELESSNESS_PATTERNS)
        }
    }

__all__ = [
    # Core configuration (existing)
    "SERVER_CONFIG",
    "CRISIS_THRESHOLDS", 
    "DEFAULT_PARAMS",
    
    # Pattern configurations (existing)
    "POSITIVE_CONTEXT_PATTERNS",
    "IDIOM_PATTERNS",
    "LGBTQIA_PATTERNS", 
    "CRISIS_CONTEXTS",
    "ENHANCED_IDIOM_PATTERNS",
    
    # Safety patterns (existing)
    "BURDEN_PATTERNS",
    "HOPELESSNESS_PATTERNS",
    "STRUGGLE_PATTERNS",
    "NEGATION_PATTERNS",
    
    # Community data (existing)
    "COMMUNITY_VOCABULARY",
    "TEMPORAL_INDICATORS",
    "CONTEXT_WEIGHTS",
    
    # Utility functions (existing)
    "get_server_config",
    "get_crisis_thresholds",
    "get_default_parameters",
    "get_lgbtqia_patterns",
    "get_community_vocabulary",
    "get_safety_patterns",
    "get_idiom_patterns",
    
    # Validation functions (existing)
    "validate_crisis_level",
    "validate_confidence_score", 
    "get_threshold_for_level",
    
    # Service info (existing)
    "SERVICE_CAPABILITIES",
    "get_service_capabilities",
    
    # New secrets-aware configuration
    "NLPConfigManager",
    "get_nlp_config",
    "get_env_config",
    "get_enhanced_crisis_thresholds",
    "get_enhanced_server_config",
    
    # Enhanced configuration functions (new)
    "get_secrets_aware_config",
    "get_enhanced_thresholds", 
    "has_api_key",
    "get_api_keys_status",
    "get_enhanced_service_info"
]