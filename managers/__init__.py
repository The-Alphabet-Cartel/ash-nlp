"""
Managers Package for Ash NLP Service v3.1 - Minimal Working Version
Centralized configuration management with JSON and environment variable support
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

# Try to import from the current structure for backward compatibility
try:
    # Try the managers/ directory first
    from .config_manager import (
        get_nlp_config,
        get_api_keys_status
    )
    CONFIG_MANAGER_AVAILABLE = True
    logger.info("✅ Config manager available (managers/config_manager.py)")
except ImportError:
    try:
        # Fall back to config/ directory
        from config.nlp_config_manager import (
            get_nlp_config,
            get_api_keys_status
        )
        CONFIG_MANAGER_AVAILABLE = True
        logger.info("✅ Config manager available (config/ directory)")
    except ImportError as e:
        CONFIG_MANAGER_AVAILABLE = False
        logger.warning(f"⚠️ Config manager not available: {e}")
        
        def get_nlp_config():
            return None
        
        def get_api_keys_status():
            return {
                'claude_api_key': bool(os.getenv('GLOBAL_CLAUDE_API_KEY')),
                'huggingface_token': bool(os.getenv('GLOBAL_HUGGINGFACE_TOKEN')),
                'openai_api_key': bool(os.getenv('OPENAI_API_KEY'))
            }

# Try to get env_config function
try:
    # Try managers first
    from .config_manager import get_config as get_env_config
except ImportError:
    try:
        # Fall back to config/ directory
        from config.env_manager import get_config as get_env_config
    except ImportError:
        def get_env_config():
            """Fallback function when config manager is not available"""
            return {
                'GLOBAL_LOG_LEVEL': os.getenv('GLOBAL_LOG_LEVEL', 'INFO'),
                'NLP_LOG_FILE': os.getenv('NLP_LOG_FILE', 'nlp_service.log'),
                'GLOBAL_ENABLE_DEBUG_MODE': os.getenv('GLOBAL_ENABLE_DEBUG_MODE', 'false').lower() == 'true',
                'NLP_DEVICE': os.getenv('NLP_DEVICE', 'auto'),
                'NLP_MODEL_PRECISION': os.getenv('NLP_MODEL_PRECISION', 'float16'),
                'NLP_MAX_BATCH_SIZE': int(os.getenv('NLP_MAX_BATCH_SIZE', '32')),
                'NLP_INFERENCE_THREADS': int(os.getenv('NLP_INFERENCE_THREADS', '16')),
                'GLOBAL_ENABLE_LEARNING_SYSTEM': os.getenv('GLOBAL_ENABLE_LEARNING_SYSTEM', 'true').lower() == 'true',
                'GLOBAL_ENABLE_CORS': os.getenv('GLOBAL_ENABLE_CORS', 'true').lower() == 'true'
            }

# Try to import static settings
try:
    # Try managers/ directory first
    from .settings_manager import (
        SERVER_CONFIG,
        CRISIS_THRESHOLDS,
        DEFAULT_PARAMS,
        LGBTQIA_PATTERNS,
        BURDEN_PATTERNS,
        HOPELESSNESS_PATTERNS,
        STRUGGLE_PATTERNS,
        ENHANCED_IDIOM_PATTERNS,
        SERVICE_CAPABILITIES
    )
    SETTINGS_MANAGER_AVAILABLE = True
    logger.info("✅ Settings available (managers/settings_manager.py)")
except ImportError:
    try:
        # Fall back to config/ directory
        from config.nlp_settings import (
            SERVER_CONFIG,
            CRISIS_THRESHOLDS,
            DEFAULT_PARAMS,
            LGBTQIA_PATTERNS,
            BURDEN_PATTERNS,
            HOPELESSNESS_PATTERNS,
            STRUGGLE_PATTERNS,
            ENHANCED_IDIOM_PATTERNS,
            SERVICE_CAPABILITIES
        )
        SETTINGS_MANAGER_AVAILABLE = True
        logger.info("✅ Settings available (config/ directory)")
    except ImportError as e:
        SETTINGS_MANAGER_AVAILABLE = False
        logger.warning(f"⚠️ Settings not available: {e}")
        
        # Provide empty fallbacks
        SERVER_CONFIG = {}
        CRISIS_THRESHOLDS = {'high': 0.55, 'medium': 0.28, 'low': 0.16}
        DEFAULT_PARAMS = {}
        LGBTQIA_PATTERNS = {}
        BURDEN_PATTERNS = []
        HOPELESSNESS_PATTERNS = []
        STRUGGLE_PATTERNS = []
        ENHANCED_IDIOM_PATTERNS = []
        SERVICE_CAPABILITIES = {}

# Configuration manager status
MANAGERS_STATUS = {
    "model_ensemble": MODEL_ENSEMBLE_AVAILABLE,
    "config_manager": CONFIG_MANAGER_AVAILABLE,
    "settings_manager": SETTINGS_MANAGER_AVAILABLE,
    "crisis_patterns": False,
    "analysis_parameters": False,
    "performance_settings": False
}

def get_managers_status():
    """Get status of all configuration managers"""
    return MANAGERS_STATUS.copy()

def get_all_config_summary():
    """Get a summary of all configuration managers"""
    summary = {
        "managers_status": get_managers_status()
    }
    
    if MODEL_ENSEMBLE_AVAILABLE:
        try:
            summary["model_ensemble"] = get_model_ensemble_manager().get_summary()
        except Exception as e:
            logger.debug(f"Could not get model ensemble summary: {e}")
    
    return summary

def reload_all_configs():
    """Reload all configuration managers"""
    logger.info("🔄 Reloading configurations...")
    # Add reload logic here when implemented

def validate_all_configs():
    """Validate all configuration managers"""
    return {
        "model_ensemble": {"status": "valid" if MODEL_ENSEMBLE_AVAILABLE else "not_available", "errors": []},
        "config_manager": {"status": "valid" if CONFIG_MANAGER_AVAILABLE else "not_available", "errors": []},
        "settings_manager": {"status": "valid" if SETTINGS_MANAGER_AVAILABLE else "not_available", "errors": []}
    }

# Backward compatibility functions
def get_crisis_thresholds():
    """Get crisis thresholds"""
    return CRISIS_THRESHOLDS

def get_server_config():
    """Get server configuration"""
    return SERVER_CONFIG

def get_lgbtqia_patterns():
    """Get LGBTQIA patterns"""
    return LGBTQIA_PATTERNS

def get_safety_patterns():
    """Get safety patterns"""
    return {
        "burden_patterns": BURDEN_PATTERNS,
        "hopelessness_patterns": HOPELESSNESS_PATTERNS,
        "struggle_patterns": STRUGGLE_PATTERNS
    }

def validate_crisis_level(level: str) -> bool:
    """Validate crisis level"""
    return level in ['none', 'low', 'medium', 'high']

def has_api_key(key_name: str) -> bool:
    """Check if API key is available"""
    return bool(os.getenv(key_name.upper()))

# Export commonly used functions
__all__ = [
    # Model Ensemble Manager
    "get_model_ensemble_manager",
    "get_model_definitions",
    "get_ensemble_configuration",
    "get_threshold_configuration",
    "get_hardware_optimization",
    "get_feature_flags",
    
    # Environment and Config
    "get_env_config",
    "get_nlp_config",
    "get_api_keys_status",
    
    # Static configurations
    "CRISIS_THRESHOLDS",
    "SERVER_CONFIG",
    "LGBTQIA_PATTERNS",
    "SERVICE_CAPABILITIES",
    
    # Utility functions
    "get_crisis_thresholds",
    "get_server_config",
    "get_lgbtqia_patterns",
    "get_safety_patterns",
    "validate_crisis_level",
    "has_api_key",
    
    # Manager utilities
    "get_managers_status",
    "get_all_config_summary",
    "validate_all_configs",
    "MANAGERS_STATUS",
    "CONFIG_MANAGER_AVAILABLE",
    "SETTINGS_MANAGER_AVAILABLE"
]

# Log initialization status
available_managers = sum(MANAGERS_STATUS.values())
logger.info(f"📦 Managers package initialized with {available_managers}/6 managers available")
for manager_name, available in MANAGERS_STATUS.items():
    status = "✅ Available" if available else "❌ Not available"
    logger.info(f"   {manager_name}: {status}")