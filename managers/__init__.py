"""
Managers Package for Ash NLP Service v3.1
Centralized configuration management with JSON and environment variable support

This package contains all configuration managers and loaders organized by functionality:
- model_ensemble_manager.py: Three-model ensemble configuration (✅ Implemented)
- config_manager.py: Environment and secrets management (✅ Renamed from config/nlp_config_manager.py)
- settings_manager.py: Static patterns and settings (✅ Renamed from config/nlp_settings.py) 
- crisis_patterns_manager.py: LGBTQIA+ and crisis detection patterns (⏳ Planned)
- analysis_parameters_manager.py: Analysis and scoring parameters (⏳ Planned)
- performance_settings_manager.py: Hardware and performance tuning (⏳ Planned)

All managers follow the same pattern:
- JSON configuration with environment variable substitution
- Validation and consistency checking  
- Hot-reload capability
- Backward compatibility with environment variables
- Centralized access via convenience functions
"""

import logging

logger = logging.getLogger(__name__)

# Import the model ensemble manager (main JSON configuration)
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

# Import existing configuration managers (now in managers/ directory)
try:
    from .config_manager import (
        NLPConfigManager,
        get_nlp_config,
        get_env_config,
        get_crisis_thresholds as get_enhanced_crisis_thresholds,
        get_server_config as get_enhanced_server_config,
        get_api_keys_status
    )
    CONFIG_MANAGER_AVAILABLE = True
    logger.info("✅ NLP config manager available (managers/config_manager.py)")
except ImportError as e:
    CONFIG_MANAGER_AVAILABLE = False
    logger.warning(f"⚠️ NLP config manager not available: {e}")
    
    # Provide fallback functions
    def get_env_config():
        """Fallback function when config_manager is not available"""
        logger.warning("config_manager not available, returning empty config")
        return {}
    
    def get_nlp_config():
        """Fallback function when config_manager is not available"""
        logger.warning("config_manager not available, returning None")
        return None
    
    def get_api_keys_status():
        """Fallback function when config_manager is not available"""
        logger.warning("config_manager not available, returning empty status")
        return {}
    
    def get_enhanced_crisis_thresholds():
        """Fallback function when config_manager is not available"""
        logger.warning("config_manager not available, returning empty thresholds")
        return {}
    
    def get_enhanced_server_config():
        """Fallback function when config_manager is not available"""
        logger.warning("config_manager not available, returning empty server config")
        return {}

# Import static settings and patterns (now in managers/ directory)
try:
    from .settings_manager import (
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
        NEGATION_PATTERNS,
        
        # Service capabilities
        SERVICE_CAPABILITIES
    )
    SETTINGS_MANAGER_AVAILABLE = True
    logger.info("✅ Settings manager available (managers/settings_manager.py)")
except ImportError as e:
    SETTINGS_MANAGER_AVAILABLE = False
    logger.warning(f"⚠️ Settings manager not available: {e}")
    
    # Provide fallback empty configurations
    SERVER_CONFIG = {}
    CRISIS_THRESHOLDS = {}
    DEFAULT_PARAMS = {}
    POSITIVE_CONTEXT_PATTERNS = []
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
    SERVICE_CAPABILITIES = {}

# Configuration manager status
MANAGERS_STATUS = {
    "model_ensemble": True,  # Always available (JSON configuration)
    "config_manager": CONFIG_MANAGER_AVAILABLE,  # Environment and secrets
    "settings_manager": SETTINGS_MANAGER_AVAILABLE,  # Static patterns and settings
    # Future managers will be added here
    "crisis_patterns": False,  # Planned (JSON configuration)
    "analysis_parameters": False,  # Planned (JSON configuration)
    "performance_settings": False  # Planned (JSON configuration)
}

# Configuration utilities (existing) - using settings_manager
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
    if config_manager:
        return bool(config_manager.get(key_name.upper()))
    return False

def get_service_capabilities():
    """Get detailed service capabilities"""
    return SERVICE_CAPABILITIES

# Enhanced service info with secrets support
def get_enhanced_service_info():
    """Get comprehensive service information including secrets status"""
    api_keys_status = get_api_keys_status()
    
    return {
        "service_name": "Ash NLP Service",
        "version": "3.1.0",  # Updated for JSON configuration
        "configuration": {
            "managers_status": MANAGERS_STATUS,
            "secrets_enabled": any(api_keys_status.values()),
            "api_keys_available": api_keys_status,
            "using_environment_fallback": not any(api_keys_status.values()),
            "json_ensemble_config": MANAGERS_STATUS["model_ensemble"],
            "crisis_thresholds": get_enhanced_thresholds(),
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

def get_managers_status() -> dict:
    """Get status of all configuration managers"""
    return MANAGERS_STATUS.copy()

def get_all_config_summary() -> dict:
    """Get a summary of all configuration managers"""
    summary = {
        "managers_status": get_managers_status(),
        "model_ensemble": get_model_ensemble_manager().get_summary()
    }
    
    # Add config manager summary if available
    if CONFIG_MANAGER_AVAILABLE:
        try:
            nlp_config = get_nlp_config()
            if nlp_config:
                summary["nlp_config"] = {
                    "device": nlp_config._config.get('NLP_DEVICE', 'unknown') if hasattr(nlp_config, '_config') else 'unknown',
                    "ensemble_mode": nlp_config._config.get('NLP_ENSEMBLE_MODE', 'unknown') if hasattr(nlp_config, '_config') else 'unknown',
                    "learning_enabled": nlp_config._config.get('GLOBAL_ENABLE_LEARNING_SYSTEM', False) if hasattr(nlp_config, '_config') else False
                }
        except Exception as e:
            logger.debug(f"Could not get NLP config summary: {e}")
    
    # Add settings manager summary
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

def reload_all_configs() -> None:
    """Reload all configuration managers"""
    logger.info("🔄 Reloading all configuration managers...")
    
    # Reload model ensemble config
    try:
        reload_model_ensemble_config()
        logger.info("✅ Model ensemble config reloaded")
    except Exception as e:
        logger.error(f"❌ Failed to reload model ensemble config: {e}")
    
    # Future: Add other config reloads here
    
    logger.info("✅ Configuration reload complete")

def validate_all_configs() -> dict:
    """Validate all configuration managers and return validation results"""
    validation_results = {}
    
    # Validate model ensemble config
    try:
        ensemble_manager = get_model_ensemble_manager()
        ensemble_manager._validate_config()  # Call internal validation
        validation_results["model_ensemble"] = {"status": "valid", "errors": []}
    except Exception as e:
        validation_results["model_ensemble"] = {"status": "invalid", "errors": [str(e)]}
    
    # Future: Add other config validations here
    
    return validation_results

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
    
    # Environment and NLP Config (renamed from config/ directory)
    "get_env_config",
    "get_nlp_config", 
    "get_api_keys_status",
    "get_enhanced_crisis_thresholds",  # From environment config
    "get_enhanced_server_config",
    
    # Static Settings and Patterns (from settings_manager)
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