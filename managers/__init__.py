"""
Managers Package for Ash NLP Service v3.1
FIXED: Now correctly imports from your actual moved files
"""

import logging
import os

logger = logging.getLogger(__name__)

# Import the model ensemble manager (main JSON configuration)
try:
    from .model_ensemble_manager import (
        ModelEnsembleManager,
        get_model_ensemble_manager,
        reload_model_ensemble_config,
        
        # Convenience functions for easy access
        get_model_definitions,
        get_ensemble_configuration,
        get_threshold_configuration,
        get_hardware_optimization,
        get_feature_flags,
        get_model_config,
        get_ensemble_mode_config,
        get_crisis_thresholds as get_ensemble_crisis_thresholds,
        get_gap_detection_config
    )
    MODEL_ENSEMBLE_AVAILABLE = True
    logger.info("✅ Model ensemble manager available")
except ImportError as e:
    MODEL_ENSEMBLE_AVAILABLE = False
    logger.warning(f"⚠️ Model ensemble manager not available: {e}")
    
    # Provide fallback functions
    class DummyModelEnsembleManager:
        def get_summary(self):
            return {"status": "not_available"}
        def get_config(self):
            return {}
    
    def get_model_ensemble_manager():
        return DummyModelEnsembleManager()
    
    def get_model_definitions():
        return {}
    
    def get_ensemble_configuration():
        return {}
    
    def get_threshold_configuration():
        return {}
    
    def get_hardware_optimization():
        return {}
    
    def get_feature_flags():
        return {}

# FIXED: Import from your actual moved config_manager.py file
try:
    from .config_manager import (
        get_nlp_config,
        get_env_config,
        get_crisis_thresholds as get_enhanced_crisis_thresholds,
        get_server_config as get_enhanced_server_config
    )
    CONFIG_MANAGER_AVAILABLE = True
    logger.info("✅ Config manager available (managers/config_manager.py)")
except ImportError as e:
    CONFIG_MANAGER_AVAILABLE = False
    logger.warning(f"⚠️ Config manager not available: {e}")
    
    def get_nlp_config():
        return None
    
    def get_env_config():
        return {}
    
    def get_enhanced_crisis_thresholds():
        return {}
    
    def get_enhanced_server_config():
        return {}

# FIXED: Import from your actual moved settings_manager.py file
try:
    from .settings_manager import (
        SERVER_CONFIG,
        CRISIS_THRESHOLDS,
        DEFAULT_PARAMS,
        POSITIVE_CONTEXT_PATTERNS,
        IDIOM_PATTERNS,
        LGBTQIA_PATTERNS,
        CRISIS_CONTEXTS,
        COMMUNITY_VOCABULARY,
        TEMPORAL_INDICATORS,
        CONTEXT_WEIGHTS,
        ENHANCED_IDIOM_PATTERNS,
        BURDEN_PATTERNS,
        HOPELESSNESS_PATTERNS,
        STRUGGLE_PATTERNS,
        NEGATION_PATTERNS
    )
    SETTINGS_MANAGER_AVAILABLE = True
    logger.info("✅ Settings manager available (managers/settings_manager.py)")
except ImportError as e:
    SETTINGS_MANAGER_AVAILABLE = False
    logger.warning(f"⚠️ Settings manager not available: {e}")
    
    # Provide empty fallbacks
    SERVER_CONFIG = {}
    CRISIS_THRESHOLDS = {'high': 0.55, 'medium': 0.28, 'low': 0.16}
    DEFAULT_PARAMS = {}
    POSITIVE_CONTEXT_PATTERNS = {}
    IDIOM_PATTERNS = []
    LGBTQIA_PATTERNS = {}
    CRISIS_CONTEXTS = {}
    COMMUNITY_VOCABULARY = {}
    TEMPORAL_INDICATORS = {}
    CONTEXT_WEIGHTS = {}
    ENHANCED_IDIOM_PATTERNS = []
    BURDEN_PATTERNS = []
    HOPELESSNESS_PATTERNS = []
    STRUGGLE_PATTERNS = []
    NEGATION_PATTERNS = []

# FIXED: Add missing get_api_keys_status function
def get_api_keys_status():
    """Get API keys status - function that was missing from config_manager.py"""
    if CONFIG_MANAGER_AVAILABLE:
        config = get_nlp_config()
        if config:
            return {
                'claude_api_key': bool(config.get('GLOBAL_CLAUDE_API_KEY')),
                'huggingface_token': bool(config.get('GLOBAL_HUGGINGFACE_TOKEN')),
                'openai_api_key': bool(config.get('OPENAI_API_KEY'))
            }
    
    # Fallback to direct environment check
    return {
        'claude_api_key': bool(os.getenv('GLOBAL_CLAUDE_API_KEY')),
        'huggingface_token': bool(os.getenv('GLOBAL_HUGGINGFACE_TOKEN')),
        'openai_api_key': bool(os.getenv('OPENAI_API_KEY'))
    }

# FIXED: Add missing SERVICE_CAPABILITIES (from your settings_manager.py it looks like this wasn't defined)
SERVICE_CAPABILITIES = {
    "crisis_analysis": {
        "description": "Multi-model crisis detection with safety-first approach",
        "models": ["depression", "sentiment", "emotional_distress"],
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

# Configuration manager status
MANAGERS_STATUS = {
    "model_ensemble": MODEL_ENSEMBLE_AVAILABLE,
    "config_manager": CONFIG_MANAGER_AVAILABLE,
    "settings_manager": SETTINGS_MANAGER_AVAILABLE,
    "crisis_patterns": False,  # Planned
    "analysis_parameters": False,  # Planned
    "performance_settings": False  # Planned
}

# Utility functions (backward compatibility)
def get_server_config():
    """Get complete server configuration"""
    return SERVER_CONFIG

def get_crisis_thresholds():
    """Get crisis level mapping thresholds (static from settings_manager)"""
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

def validate_crisis_level(level: str) -> bool:
    """Validate that crisis level is supported"""
    return level in ['none', 'low', 'medium', 'high']

def validate_confidence_score(score: float) -> bool:
    """Validate that confidence score is in valid range"""
    return 0.0 <= score <= 1.0

def get_threshold_for_level(level: str) -> float:
    """Get confidence threshold for crisis level"""
    return CRISIS_THRESHOLDS.get(level, 0.0)

def has_api_key(key_name: str) -> bool:
    """Check if API key is available (from secrets or environment)"""
    if CONFIG_MANAGER_AVAILABLE:
        config = get_nlp_config()
        if config:
            return bool(config.get(key_name.upper()))
    return bool(os.getenv(key_name.upper()))

def get_service_capabilities():
    """Get detailed service capabilities"""
    return SERVICE_CAPABILITIES

def get_managers_status():
    """Get status of all configuration managers"""
    return MANAGERS_STATUS.copy()

def get_all_config_summary():
    """Get a summary of all configuration managers"""
    summary = {
        "managers_status": get_managers_status(),
    }
    
    if MODEL_ENSEMBLE_AVAILABLE:
        try:
            summary["model_ensemble"] = get_model_ensemble_manager().get_summary()
        except Exception as e:
            logger.debug(f"Could not get model ensemble summary: {e}")
    
    if CONFIG_MANAGER_AVAILABLE:
        try:
            config = get_nlp_config()
            if config:
                summary["nlp_config"] = {
                    "device": config.get('NLP_DEVICE', 'unknown'),
                    "ensemble_mode": config.get('NLP_ENSEMBLE_MODE', 'unknown'),
                    "learning_enabled": config.get('GLOBAL_ENABLE_LEARNING_SYSTEM', False)
                }
        except Exception as e:
            logger.debug(f"Could not get NLP config summary: {e}")
    
    if SETTINGS_MANAGER_AVAILABLE:
        summary["settings_manager"] = {
            "patterns_loaded": {
                "lgbtqia_patterns": len(LGBTQIA_PATTERNS),
                "burden_patterns": len(BURDEN_PATTERNS),
                "hopelessness_patterns": len(HOPELESSNESS_PATTERNS),
                "enhanced_idiom_patterns": len(ENHANCED_IDIOM_PATTERNS)
            },
            "crisis_thresholds_available": bool(CRISIS_THRESHOLDS),
            "server_config_available": bool(SERVER_CONFIG)
        }
    
    return summary

def reload_all_configs():
    """Reload all configuration managers"""
    logger.info("🔄 Reloading all configuration managers...")
    
    # Reload model ensemble config
    if MODEL_ENSEMBLE_AVAILABLE:
        try:
            reload_model_ensemble_config()
            logger.info("✅ Model ensemble config reloaded")
        except Exception as e:
            logger.error(f"❌ Failed to reload model ensemble config: {e}")
    
    logger.info("✅ Configuration reload complete")

def validate_all_configs():
    """Validate all configuration managers and return validation results"""
    validation_results = {}
    
    # Validate model ensemble config
    try:
        if MODEL_ENSEMBLE_AVAILABLE:
            ensemble_manager = get_model_ensemble_manager()
            ensemble_manager._validate_config()  # Call internal validation
            validation_results["model_ensemble"] = {"status": "valid", "errors": []}
        else:
            validation_results["model_ensemble"] = {"status": "not_available", "errors": []}
    except Exception as e:
        validation_results["model_ensemble"] = {"status": "invalid", "errors": [str(e)]}
    
    # Validate config manager
    validation_results["config_manager"] = {
        "status": "valid" if CONFIG_MANAGER_AVAILABLE else "not_available", 
        "errors": []
    }
    
    # Validate settings manager
    validation_results["settings_manager"] = {
        "status": "valid" if SETTINGS_MANAGER_AVAILABLE else "not_available", 
        "errors": []
    }
    
    return validation_results

# Enhanced service info
def get_enhanced_service_info():
    """Get comprehensive service information including secrets status"""
    api_keys_status = get_api_keys_status()
    
    return {
        "service_name": "Ash NLP Service",
        "version": "3.1.0",
        "configuration": {
            "managers_status": MANAGERS_STATUS,
            "secrets_enabled": any(api_keys_status.values()),
            "api_keys_available": api_keys_status,
            "using_environment_fallback": not any(api_keys_status.values()),
            "json_ensemble_config": MANAGERS_STATUS["model_ensemble"],
            "crisis_thresholds": get_enhanced_crisis_thresholds() if CONFIG_MANAGER_AVAILABLE else CRISIS_THRESHOLDS,
            "hardware_optimized": True
        },
        "capabilities": SERVICE_CAPABILITIES,
        "patterns_loaded": {
            "lgbtqia_patterns": len(LGBTQIA_PATTERNS) if LGBTQIA_PATTERNS else 0,
            "idiom_patterns": len(IDIOM_PATTERNS) if IDIOM_PATTERNS else 0,
            "burden_patterns": len(BURDEN_PATTERNS) if BURDEN_PATTERNS else 0,
            "hopelessness_patterns": len(HOPELESSNESS_PATTERNS) if HOPELESSNESS_PATTERNS else 0
        }
    }

# Enhanced configuration functions (with secrets support)
def get_secrets_aware_config():
    """Get configuration manager with secrets support"""
    return get_nlp_config()

def get_enhanced_thresholds():
    """Get crisis thresholds with environment variable overrides"""
    return get_enhanced_crisis_thresholds()

def get_enhanced_server_config():
    """Get server config with secrets and environment variables"""
    return get_enhanced_server_config()

# Export all commonly used functions for easy importing
__all__ = [
    # Model Ensemble Manager (JSON Configuration)
    "ModelEnsembleManager",
    "get_model_ensemble_manager",
    "reload_model_ensemble_config",
    
    # Model Ensemble Convenience Functions
    "get_model_definitions",
    "get_ensemble_configuration", 
    "get_threshold_configuration",
    "get_hardware_optimization",
    "get_feature_flags",
    "get_model_config",
    "get_ensemble_mode_config",
    "get_ensemble_crisis_thresholds",  # From JSON config
    "get_gap_detection_config",
    
    # Environment and NLP Config (from your moved files)
    "get_env_config",
    "get_nlp_config", 
    "get_api_keys_status",
    "get_enhanced_crisis_thresholds",  # From environment config
    "get_enhanced_server_config",
    
    # Static Settings and Patterns (from your moved settings_manager)
    "SERVER_CONFIG",
    "CRISIS_THRESHOLDS", 
    "DEFAULT_PARAMS",
    "POSITIVE_CONTEXT_PATTERNS",
    "IDIOM_PATTERNS",
    "LGBTQIA_PATTERNS", 
    "CRISIS_CONTEXTS",
    "ENHANCED_IDIOM_PATTERNS",
    "BURDEN_PATTERNS",
    "HOPELESSNESS_PATTERNS",
    "STRUGGLE_PATTERNS",
    "NEGATION_PATTERNS",
    "COMMUNITY_VOCABULARY",
    "TEMPORAL_INDICATORS",
    "CONTEXT_WEIGHTS",
    "SERVICE_CAPABILITIES",
    
    # Utility Functions (backward compatibility)
    "get_server_config",
    "get_crisis_thresholds",  # Static thresholds from settings
    "get_default_parameters",
    "get_lgbtqia_patterns",
    "get_community_vocabulary",
    "get_safety_patterns",
    "get_idiom_patterns",
    "validate_crisis_level",
    "validate_confidence_score", 
    "get_threshold_for_level",
    "get_service_capabilities",
    
    # Enhanced Functions
    "get_secrets_aware_config",
    "get_enhanced_thresholds", 
    "has_api_key",
    "get_enhanced_service_info",
    
    # Manager Utilities
    "get_managers_status",
    "get_all_config_summary",
    "reload_all_configs",
    "validate_all_configs",
    
    # Status Flags
    "MANAGERS_STATUS",
    "CONFIG_MANAGER_AVAILABLE",
    "SETTINGS_MANAGER_AVAILABLE"
]

# Log managers initialization with detailed status
logger.info(f"📦 Managers package initialized with {sum(MANAGERS_STATUS.values())} available managers")
for manager_name, available in MANAGERS_STATUS.items():
    if available:
        if manager_name == "model_ensemble":
            status = "✅ Available (JSON configuration)"
        elif manager_name == "config_manager":
            status = "✅ Available (environment + secrets)"
        elif manager_name == "settings_manager":
            status = "✅ Available (static patterns)"
        else:
            status = "✅ Available"
    else:
        status = "⏳ Planned (JSON configuration)"
    
    logger.info(f"   {manager_name}: {status}")

# Log pattern loading status
if SETTINGS_MANAGER_AVAILABLE:
    logger.info("🎯 Pattern Loading Status:")
    logger.info(f"   LGBTQIA+ Patterns: {len(LGBTQIA_PATTERNS)} loaded")
    logger.info(f"   Burden Patterns: {len(BURDEN_PATTERNS)} loaded")
    logger.info(f"   Hopelessness Patterns: {len(HOPELESSNESS_PATTERNS)} loaded")
    logger.info(f"   Enhanced Idiom Patterns: {len(ENHANCED_IDIOM_PATTERNS)} loaded")
else:
    logger.warning("⚠️ Settings manager not available - patterns not loaded")

# Log configuration sources
logger.info("🔧 Configuration Sources:")
logger.info(f"   JSON Ensemble Config: {'✅ managers/model_ensemble_manager.py' if MANAGERS_STATUS['model_ensemble'] else '❌ Not available'}")
logger.info(f"   Environment Config: {'✅ managers/config_manager.py' if CONFIG_MANAGER_AVAILABLE else '❌ Not available'}")
logger.info(f"   Static Patterns: {'✅ managers/settings_manager.py' if SETTINGS_MANAGER_AVAILABLE else '❌ Not available'}")