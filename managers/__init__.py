# ash-nlp/managers/__init__.py
"""
Managers Module for Ash NLP Service
FILE VERSION: v3.1-3d-10.8-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.8 - Added ContextPatternManager support
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This module provides centralized manager imports and factory functions
following Clean v3.1 architecture principles with proper dependency injection.
"""

import logging

logger = logging.getLogger(__name__)

# ============================================================================
# MANAGER IMPORTS WITH RESILIENT ERROR HANDLING
# ============================================================================

logger.info("🏭 Loading managers v3.1 with Clean Architecture patterns...")

# Analysis Parameter Manager (Phase 3B)
try:
    from .analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager
    ANALYSIS_PARAMETERS_MANAGER_AVAILABLE = True
    logger.debug("  ✅ AnalysisParametersManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ AnalysisParametersManager v3.1 import failed: {e}")
    AnalysisParametersManager = None
    create_analysis_parameters_manager = None
    ANALYSIS_PARAMETERS_MANAGER_AVAILABLE = False

# Context Pattern Manager (Phase 3D Step 10.8) - NEW
try:
    from .context_pattern_manager import ContextPatternManager, create_context_pattern_manager
    CONTEXT_PATTERN_MANAGER_AVAILABLE = True
    logger.debug("  ✅ ContextPatternManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ ContextPatternManager v3.1 import failed: {e}")
    ContextPatternManager = None
    create_context_pattern_manager = None
    CONTEXT_PATTERN_MANAGER_AVAILABLE = False

# Crisis Pattern Manager (Phase 3A)
try:
    from .crisis_pattern_manager import CrisisPatternManager, create_crisis_pattern_manager
    CRISIS_PATTERN_MANAGER_AVAILABLE = True
    logger.debug("  ✅ CrisisPatternManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ CrisisPatternManager v3.1 import failed: {e}")
    CrisisPatternManager = None
    create_crisis_pattern_manager = None
    CRISIS_PATTERN_MANAGER_AVAILABLE = False

# Feature Configuration Manager
try:
    from .feature_config_manager import FeatureConfigManager, create_feature_config_manager
    FEATURE_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("  ✅ FeatureConfigManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ FeatureConfigManager v3.1 import failed: {e}")
    FeatureConfigManager = None
    create_feature_config_manager = None
    FEATURE_CONFIG_MANAGER_AVAILABLE = False

# Logging Configuration Manager
try:
    from .logging_config_manager import LoggingConfigManager, create_logging_config_manager
    LOGGING_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("  ✅ LoggingConfigManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ LoggingConfigManager v3.1 import failed: {e}")
    LoggingConfigManager = None
    create_logging_config_manager = None
    LOGGING_CONFIG_MANAGER_AVAILABLE = False

# Model Ensemble Manager
try:
    from .model_ensemble_manager import ModelEnsembleManager, create_model_ensemble_manager
    MODEL_ENSEMBLE_MANAGER_AVAILABLE = True
    logger.debug("  ✅ ModelEnsembleManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ ModelEnsembleManager v3.1 import failed: {e}")
    ModelEnsembleManager = None
    create_model_ensemble_manager = None
    MODEL_ENSEMBLE_MANAGER_AVAILABLE = False

# Models Manager
try:
    from .models_manager import ModelsManager, create_models_manager
    MODELS_MANAGER_AVAILABLE = True
    logger.debug("  ✅ ModelsManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ ModelsManager v3.1 import failed: {e}")
    ModelsManager = None
    create_models_manager = None
    MODELS_MANAGER_AVAILABLE = False

# Performance Configuration Manager
try:
    from .performance_config_manager import PerformanceConfigManager, create_performance_config_manager
    PERFORMANCE_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("  ✅ PerformanceConfigManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ PerformanceConfigManager v3.1 import failed: {e}")
    PerformanceConfigManager = None
    create_performance_config_manager = None
    PERFORMANCE_CONFIG_MANAGER_AVAILABLE = False

# Pydantic Model Managers (Phase 2B)
try:
    from .pydantic_manager import PydanticManager, create_pydantic_manager
    PYDANTIC_MANAGER_AVAILABLE = True
    logger.debug("  ✅ PydanticManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ PydanticManager v3.1 import failed: {e}")
    PydanticManager = None
    create_pydantic_manager = None
    PYDANTIC_MANAGER_AVAILABLE = False

# Server Configuration Manager
try:
    from .server_config_manager import ServerConfigManager, create_server_config_manager
    SERVER_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("  ✅ ServerConfigManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ ServerConfigManager v3.1 import failed: {e}")
    ServerConfigManager = None
    create_server_config_manager = None
    SERVER_CONFIG_MANAGER_AVAILABLE = False

# Settings Manager
try:
    from .settings_manager import SettingsManager, create_settings_manager
    SETTINGS_MANAGER_AVAILABLE = True
    logger.debug("  ✅ SettingsManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ SettingsManager v3.1 import failed: {e}")
    SettingsManager = None
    create_settings_manager = None
    SETTINGS_MANAGER_AVAILABLE = False

# Storage Configuration Manager
try:
    from .storage_config_manager import StorageConfigManager, create_storage_config_manager
    STORAGE_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("  ✅ StorageConfigManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ StorageConfigManager v3.1 import failed: {e}")
    StorageConfigManager = None
    create_storage_config_manager = None
    STORAGE_CONFIG_MANAGER_AVAILABLE = False

# Threshold Mapping Manager (Phase 3C)
try:
    from .threshold_mapping_manager import ThresholdMappingManager, create_threshold_mapping_manager
    THRESHOLD_MAPPING_MANAGER_AVAILABLE = True
    logger.debug("  ✅ ThresholdMappingManager v3.1 imported")
except ImportError as e:
    logger.error(f"  ❌ ThresholdMappingManager v3.1 import failed: {e}")
    ThresholdMappingManager = None
    create_threshold_mapping_manager = None
    THRESHOLD_MAPPING_MANAGER_AVAILABLE = False

# Unified Configuration Manager (Core)
try:
    from .unified_config_manager import UnifiedConfigManager, create_unified_config_manager
    UNIFIED_CONFIG_MANAGER_AVAILABLE = True
    logger.debug("  ✅ Unified configuration managers imported")
except ImportError as e:
    logger.error(f"  ❌ Unified configuration manager imports failed: {e}")
    UnifiedConfigManager = None
    create_unified_config_manager = None
    UNIFIED_CONFIG_MANAGER_AVAILABLE = False

# Zero Shot Manager
try:
    from .zero_shot_manager import ZeroShotManager, create_zero_shot_manager
    ZERO_SHOT_MANAGER_AVAILABLE = True
    logger.debug("  ✅ ZeroShotManager imported")
except ImportError as e:
    logger.error(f"  ❌ ZeroShotManager import failed: {e}")
    ZeroShotManager = None
    create_zero_shot_manager = None
    ZERO_SHOT_MANAGER_AVAILABLE = False

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
        'analysis_parameters_manager': ANALYSIS_PARAMETERS_MANAGER_AVAILABLE,
        'context_pattern_manager': CONTEXT_PATTERN_MANAGER_AVAILABLE,  # NEW
        'crisis_pattern_manager': CRISIS_PATTERN_MANAGER_AVAILABLE,
        'feature_config_manager': FEATURE_CONFIG_MANAGER_AVAILABLE,
        'logging_config_manager': LOGGING_CONFIG_MANAGER_AVAILABLE,
        'model_ensemble_manager': MODEL_ENSEMBLE_MANAGER_AVAILABLE,
        'models_manager': MODELS_MANAGER_AVAILABLE,
        'performance_config_manager': PERFORMANCE_CONFIG_MANAGER_AVAILABLE,
        'pydantic_manager': PYDANTIC_MANAGER_AVAILABLE,
        'server_config_manager': SERVER_CONFIG_MANAGER_AVAILABLE,
        'settings_manager': SETTINGS_MANAGER_AVAILABLE,
        'storage_config_manager': STORAGE_CONFIG_MANAGER_AVAILABLE,
        'threshold_mapping_manager': THRESHOLD_MAPPING_MANAGER_AVAILABLE,
        'unified_config_managers': UNIFIED_CONFIG_MANAGER_AVAILABLE,
        'zero_shot_manager': ZERO_SHOT_MANAGER_AVAILABLE,
    }

# ============================================================================
# STEP 10.8: UNIFIED CONFIGURATION EXPORTS WITH CONTEXT PATTERN MANAGER
# ============================================================================

__all__ = [
    'AnalysisParametersManager',
    'create_analysis_parameters_manager',
    'ContextPatternManager',  # NEW
    'create_context_pattern_manager',  # NEW
    'CrisisPatternManager',
    'create_crisis_pattern_manager',
    'FeatureConfigManager',
    'create_feature_config_manager',
    'LoggingConfigManager',
    'create_logging_config_manager',
    'ModelEnsembleManager',
    'create_model_ensemble_manager',
    'ModelsManager',
    'create_models_manager',
    'PerformanceConfigManager',
    'create_performance_config_manager',
    'PydanticManager', 
    'create_pydantic_manager',
    'ServerConfigManager',
    'create_server_config_manager',
    'SettingsManager',
    'create_settings_manager',
    'StorageConfigManager',
    'create_storage_config_manager',
    'ThresholdMappingManager',
    'create_threshold_mapping_manager',
    'UnifiedConfigManager',
    'create_unified_config_manager',
    'ZeroShotManager',
    'create_zero_shot_manager',

    'get_manager_status'
]

# ============================================================================
# STEP 10.8 COMPLETION LOG
# ============================================================================

logger.info("✅ Managers __init__.py Step 10.8 complete - ContextPatternManager added")
logger.info(f"📊 Manager status: {sum(get_manager_status().values())}/{len(get_manager_status())} managers available")