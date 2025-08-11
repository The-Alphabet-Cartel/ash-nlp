# ash/ash-nlp/managers/__init__.py (Clean v3.1 Architecture - Step 9.8 Complete)
"""
Ash NLP Service Managers - Clean v3.1 Architecture
Step 9.8: Complete ConfigManager Elimination - UnifiedConfigManager Only

Provides centralized access to all manager components following clean v3.1 patterns.
All managers use dependency injection and fail-fast design.
"""

import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CLEAN V3.1 MANAGER IMPORTS - Step 9.8 Complete
# ============================================================================

# STEP 9.8: Unified Configuration Managers Only
try:
    from .unified_config_manager import UnifiedConfigManager, create_unified_config_manager
    from .settings_manager import SettingsManager, create_settings_manager
    from .zero_shot_manager import ZeroShotManager
    UNIFIED_CONFIG_MANAGERS_AVAILABLE = True
    logger.debug("✅ Unified configuration managers imported (Step 9.8)")
except ImportError as e:
    logger.error(f"❌ Unified configuration manager imports failed: {e}")
    UnifiedConfigManager = None
    create_unified_config_manager = None
    SettingsManager = None
    create_settings_manager = None
    ZeroShotManager = None
    UNIFIED_CONFIG_MANAGERS_AVAILABLE = False

# ML Model Managers (Phase 2A)
try:
    from .models_manager import ModelsManager, create_models_manager
    MODELS_MANAGER_AVAILABLE = True
    logger.debug("✅ ModelsManager v3.1 imported (Phase 2A)")
except ImportError as e:
    logger.error(f"❌ ModelsManager v3.1 import failed: {e}")
    ModelsManager = None
    create_models_manager = None
    MODELS_MANAGER_AVAILABLE = False

# Pydantic Model Managers (Phase 2B)
try:
    from .pydantic_manager import PydanticManager, create_pydantic_manager
    PYDANTIC_MANAGER_AVAILABLE = True
    logger.debug("✅ PydanticManager v3.1 imported (Phase 2B)")
except ImportError as e:
    logger.error(f"❌ PydanticManager v3.1 import failed: {e}")
    PydanticManager = None
    create_pydantic_manager = None
    PYDANTIC_MANAGER_AVAILABLE = False

# Crisis Pattern Manager (Phase 3a - Step 9.8 Updated) 
try:
    from .crisis_pattern_manager import CrisisPatternManager, create_crisis_pattern_manager
    CRISIS_PATTERN_MANAGER_AVAILABLE = True
    logger.debug("✅ CrisisPatternManager v3.1 Step 9.8 imported (UnifiedConfigManager only)")
except ImportError as e:
    logger.error(f"❌ CrisisPatternManager v3.1 Step 9.8 import failed: {e}")
    CrisisPatternManager = None
    create_crisis_pattern_manager = None
    CRISIS_PATTERN_MANAGER_AVAILABLE = False

# Analysis Parameters Manager (Phase 3b)
try:
    from .analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager
    ANALYSIS_PARAMETERS_MANAGER_AVAILABLE = True
    logger.debug("✅ AnalysisParametersManager v3.1 imported (Phase 3b)")
except ImportError as e:
    logger.error(f"❌ AnalysisParametersManager v3.1 import failed: {e}")
    AnalysisParametersManager = None
    create_analysis_parameters_manager = None
    ANALYSIS_PARAMETERS_MANAGER_AVAILABLE = False

# Threshold Mapping Manager (Phase 3c)
try:
    from .threshold_mapping_manager import ThresholdMappingManager, create_threshold_mapping_manager
    THRESHOLD_MAPPING_MANAGER_AVAILABLE = True
    logger.debug("✅ ThresholdMappingManager v3.1 imported (Phase 3c)")
except ImportError as e:
    logger.error(f"❌ ThresholdMappingManager v3.1 import failed: {e}")
    ThresholdMappingManager = None
    create_threshold_mapping_manager = None
    THRESHOLD_MAPPING_MANAGER_AVAILABLE = False

# Model Ensemble Manager (Phase 3d)
try:
    from .model_ensemble_manager import ModelEnsembleManager, create_model_ensemble_manager
    MODEL_ENSEMBLE_MANAGER_AVAILABLE = True
    logger.debug("✅ ModelEnsembleManager v3.1 imported (Phase 3d)")
except ImportError as e:
    logger.error(f"❌ ModelEnsembleManager v3.1 import failed: {e}")
    ModelEnsembleManager = None
    create_model_ensemble_manager = None
    MODEL_ENSEMBLE_MANAGER_AVAILABLE = False

# Phase 3d Step 6-7-8 Managers  
try:
    from .logging_config_manager import LoggingConfigManager, create_logging_config_manager
    LOGGING_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("✅ LoggingConfigManager v3.1 imported (Phase 3d Step 6)")
except ImportError as e:
    logger.error(f"❌ LoggingConfigManager v3.1 import failed: {e}")
    LoggingConfigManager = None
    create_logging_config_manager = None
    LOGGING_CONFIG_MANAGER_AVAILABLE = False

try:
    from .feature_config_manager import FeatureConfigManager, create_feature_config_manager
    FEATURE_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("✅ FeatureConfigManager v3.1 imported (Phase 3d Step 7)")
except ImportError as e:
    logger.error(f"❌ FeatureConfigManager v3.1 import failed: {e}")
    FeatureConfigManager = None
    create_feature_config_manager = None
    FEATURE_CONFIG_MANAGER_AVAILABLE = False

try:
    from .performance_config_manager import PerformanceConfigManager, create_performance_config_manager
    PERFORMANCE_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("✅ PerformanceConfigManager v3.1 imported (Phase 3d Step 7)")
except ImportError as e:
    logger.error(f"❌ PerformanceConfigManager v3.1 import failed: {e}")
    PerformanceConfigManager = None
    create_performance_config_manager = None
    PERFORMANCE_CONFIG_MANAGER_AVAILABLE = False

try:
    from .server_config_manager import ServerConfigManager, create_server_config_manager
    SERVER_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("✅ ServerConfigManager v3.1 imported (Phase 3d Step 5)")
except ImportError as e:
    logger.error(f"❌ ServerConfigManager v3.1 import failed: {e}")
    ServerConfigManager = None
    create_server_config_manager = None
    SERVER_CONFIG_MANAGER_AVAILABLE = False

# ============================================================================
# MANAGER AVAILABILITY SUMMARY
# ============================================================================

def get_manager_status() -> dict:
    """
    Get status of all available managers
    
    Returns:
        Dictionary showing availability of all manager types
    """
    return {
        'unified_config_managers': UNIFIED_CONFIG_MANAGERS_AVAILABLE,
        'models_manager': MODELS_MANAGER_AVAILABLE,
        'pydantic_manager': PYDANTIC_MANAGER_AVAILABLE,
        'crisis_pattern_manager': CRISIS_PATTERN_MANAGER_AVAILABLE,
        'analysis_parameters_manager': ANALYSIS_PARAMETERS_MANAGER_AVAILABLE,
        'threshold_mapping_manager': THRESHOLD_MAPPING_MANAGER_AVAILABLE,
        'model_ensemble_manager': MODEL_ENSEMBLE_MANAGER_AVAILABLE,
        'logging_config_manager': LOGGING_CONFIG_MANAGER_AVAILABLE,
        'feature_config_manager': FEATURE_CONFIG_MANAGER_AVAILABLE,
        'performance_config_manager': PERFORMANCE_CONFIG_MANAGER_AVAILABLE,
        'server_config_manager': SERVER_CONFIG_MANAGER_AVAILABLE
    }

# ============================================================================
# STEP 9.8: UNIFIED CONFIGURATION EXPORTS ONLY
# ============================================================================

__all__ = [
    # Unified Configuration Managers (Step 9.8)
    'UnifiedConfigManager',
    'create_unified_config_manager',
    'SettingsManager',
    'create_settings_manager',
    'ZeroShotManager',
    
    # Model Managers
    'ModelsManager',
    'create_models_manager',
    'PydanticManager', 
    'create_pydantic_manager',
    
    # Pattern and Analysis Managers
    'CrisisPatternManager',
    'create_crisis_pattern_manager',
    'AnalysisParametersManager',
    'create_analysis_parameters_manager',
    'ThresholdMappingManager',
    'create_threshold_mapping_manager',
    'ModelEnsembleManager',
    'create_model_ensemble_manager',
    
    # Configuration Managers
    'LoggingConfigManager',
    'create_logging_config_manager',
    'FeatureConfigManager',
    'create_feature_config_manager',
    'PerformanceConfigManager',
    'create_performance_config_manager',
    'ServerConfigManager',
    'create_server_config_manager',
    
    # Utility Functions
    'get_manager_status'
]

# ============================================================================
# STEP 9.8 COMPLETION LOG
# ============================================================================

logger.info("✅ Managers __init__.py Step 9.8 complete - ConfigManager eliminated, UnifiedConfigManager only")
logger.info(f"📊 Manager status: {sum(get_manager_status().values())}/{len(get_manager_status())} managers available")

# Log specific achievement
if UNIFIED_CONFIG_MANAGERS_AVAILABLE and CRISIS_PATTERN_MANAGER_AVAILABLE:
    logger.info("🎉 Step 9.8 SUCCESS: Complete transition to UnifiedConfigManager architecture achieved!")
else:
    logger.warning("⚠️ Step 9.8 INCOMPLETE: UnifiedConfigManager or CrisisPatternManager not available")