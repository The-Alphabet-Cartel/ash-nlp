# ash-nlp/managers/settings_manager.py
"""
Runtime Settings and Configuration Overrides for Ash NLP Service
FILE VERSION: v3.1-3ed-4.3-1
LAST MODIFIED: 2025-08-13
PHASE: 3d, Step 10.11-3
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# SERVER CONFIGURATION (NON-MIGRATABLE LEGACY CONSTANTS)
# ============================================================================

SERVER_CONFIG = {
    "description": "Phase 3d: Server configuration managed by UnifiedConfigManager",
    "note": "These legacy constants preserved for backward compatibility only",
    "version": "3.1d",
    "unified_config": True
}

class SettingsManager:
    """
    Manages runtime settings and configuration overrides
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    
    All configuration now accessed through specialized managers:
    - Analysis parameters: AnalysisParametersManager
    - Crisis patterns: CrisisPatternManager
    - Feature flags: FeatureConfigManager
    - Learning system settings: LearningSystemManager
    - Logging settings: LoggingConfigManager
    - Model Ensemble settings: ModelEnsembleManager
    - Performance settings: PerformanceConfigManager
    - Pydantic settings: PydanticManager
    - Server settings: ServerConfigManager
    - Shared utilities: SharedUtilitiesManager
    - Storage settings: StorageConfigManager
    - Threshold mappings: ThresholdMappingManager
    - Zero Shot settings: ZeroShotManager
    """
    
    def __init__(self, unified_config_manager,
        analysis_parameters_manager=None, crisis_pattern_manager=None,
        feature_config_manager=None, learning_systsem_manager=None,
        logging_config_manager=None, model_ensemble_manager=None,
        performance_config_manager=None, pydantic_manager=None,
        server_config_manager=None, shared_utilities_manager=None,
        storage_config_manager=None, threshold_mapping_manager=None,
        zero_shot_manager=None):
        """
        Initialize SettingsManager with UnifiedConfigManager and all Phase 3d managers
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
            analysis_parameters_manager: AnalysisParametersManager instance
            crisis_pattern_manager: CrisisPatternManager instance
            analysis_parameters_manager: AnalysisParametersManager instance
            logging_config_manager: LoggingConfigManager instance
            model_ensemble_manager: ModelEnsembleManager instance
            performance_config_manager: PerformanceConfigManager instance
            pydantic_manager: PydanticManager instance
            server_config_manager: ServerConfigManager instance
            storage_config_manager: StorageConfigManager instance
            threshold_mapping_manager: ThresholdMappingManager instance
            zero_shot_manager: ZeroShotManager instance
        """
        # STEP 9 CHANGE: Use UnifiedConfigManager instead of ConfigManager
        self.unified_config = unified_config_manager
        self.analysis_parameters_manager = analysis_parameters_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.feature_config_manager = feature_config_manager
        self.learning_system_manager = learning_system_manager
        self.logging_config_manager = logging_config_manager
        self.model_ensemble_manager = model_ensemble_manager
        self.performance_config_manager = performance_config_manager
        self.pydantic_manager = pydantic_manager
        self.server_config_manager = server_config_manager
        self.shared_utilities_manager = shared_utilities_manager
        self.storage_config_manager = storage_config_manager
        self.threshold_mapping_manager = threshold_mapping_manager
        self.zero_shot_manager = zero_shot_manager

        self.setting_overrides = {}
        self.runtime_settings = {}
        
        # Load runtime settings using unified configuration
        self._load_runtime_settings()
        
        # Validate manager integration
        self._validate_manager_integration()
        
        logger.info("SettingsManager v3.1d Step 9 initialized - UnifiedConfigManager integration complete")
    
    def _load_runtime_settings(self):
        """Load runtime settings using UnifiedConfigManager (NO MORE os.getenv())"""
        try:
            # STEP 9 CHANGE: Use unified configuration instead of os.getenv()
            self.runtime_settings = {
                'server': SERVER_CONFIG,
                'phase_status': {
                    'unified_config_manager': 'operational',  # NEW
                    'phase_2a': 'complete',
                    'phase_2b': 'complete', 
                    'phase_2c': 'complete',
                    'phase_3a': 'complete',
                    'phase_3b': 'complete',
                    'phase_3c': 'complete',
                    'phase_3d_step_5': 'complete',
                    'phase_3d_step_6': 'complete', 
                    'phase_3d_step_7': 'complete',
                    'phase_3d_step_8': 'complete',
                    'phase_3d_step_9': 'complete',  # NEW
                    'crisis_patterns': 'externalized_to_json',
                    'analysis_parameters': 'externalized_to_json',
                    'threshold_mappings': 'externalized_to_json',
                    'server_configuration': 'externalized_to_json',
                    'logging_configuration': 'externalized_to_json',
                    'feature_flags': 'externalized_to_json',
                    'performance_settings': 'externalized_to_json',
                    'direct_os_getenv_calls': 'eliminated'    # NEW
                }
            }
            
            # Load environment overrides using unified configuration
            self._load_environment_overrides()
            
        except Exception as e:
            logger.error(f"Error loading runtime settings: {e}")
    
    def _load_environment_overrides(self):
        """Load setting overrides using UnifiedConfigManager (NO MORE os.getenv())"""
        try:
            # STEP 9 CHANGE: Use unified configuration instead of os.getenv()
            
            # Legacy device and precision settings (maintained for backward compatibility)
            # Now accessed through UnifiedConfigManager instead of direct os.getenv()
            legacy_device = self.unified_config.get_env('NLP_DEVICE')
            if legacy_device:
                self.setting_overrides['device'] = legacy_device
                
            legacy_precision = self.unified_config.get_env('NLP_PRECISION')
            if legacy_precision:
                self.setting_overrides['precision'] = legacy_precision
            
            logger.debug("✅ Environment overrides loaded using UnifiedConfigManager")
            
        except Exception as e:
            logger.error(f"Error loading environment overrides: {e}")
    
    def _validate_manager_integration(self):
        """Validate manager integration for Phase 3d Step 9"""
        managers = {
            'UnifiedConfigManager': self.unified_config,
            'AnalysisParametersManager': self.analysis_parameters_manager,
            'CrisisPatternManager': self.crisis_pattern_manager,
            'FeatureConfigManager': self.feature_config_manager,
            'LearningSystemManager': self.learning_system_manager,
            'LoggingConfigManager': self.logging_config_manager,
            'ModelEnsembleManager': self.model_ensemble_manager,
            'PerformanceConfigManager': self.performance_config_manager,
            'PydanticManager': self.pydantic_manager,
            'ServerConfigManager': self.server_config_manager,
            'SharedUtilitiesManager': self.shared_utilities_manager,
            'StorageConfigManager': self.storage_config_manager,
            'ThresholdMappingManager': self.threshold_mapping_manager,
            'ZeroShotManager': self.zero_shot_manager,
        }
        
        available_managers = [name for name, mgr in managers.items() if mgr is not None]
        missing_managers = [name for name, mgr in managers.items() if mgr is None]
        
        logger.info(f"✅ Available managers: {available_managers}")
        if missing_managers:
            logger.warning(f"⚠️ Missing managers: {missing_managers}")
        
        # Validate that UnifiedConfigManager is available (critical for Step 9)
        if not self.unified_config:
            raise ValueError("UnifiedConfigManager is required for SettingsManager in Phase 3d Step 9")
    
    # ========================================================================
    # UNIFIED CONFIGURATION ACCESS METHODS (NEW IN STEP 9)
    # ========================================================================
    
    def get_environment_variable(self, var_name: str, default: Any = None) -> Any:
        """
        Get environment variable through UnifiedConfigManager
        REPLACES all direct os.getenv() calls throughout the system
        
        Args:
            var_name: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return self.unified_config.get_env(var_name, default)
    
    def get_environment_bool(self, var_name: str, default: bool = False) -> bool:
        """Get boolean environment variable through UnifiedConfigManager"""
        return self.unified_config.get_env_bool(var_name, default)
    
    def get_environment_int(self, var_name: str, default: int = 0) -> int:
        """Get integer environment variable through UnifiedConfigManager"""
        return self.unified_config.get_env_int(var_name, default)
    
    def get_environment_float(self, var_name: str, default: float = 0.0) -> float:
        """Get float environment variable through UnifiedConfigManager"""
        return self.unified_config.get_env_float(var_name, default)
    
    def get_storage_configuration(self) -> Dict[str, Any]:
        """
        Get comprehensive storage configuration settings
        Uses StorageConfigManager if available, otherwise falls back to UnifiedConfigManager
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_complete_configuration()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Fallback to UnifiedConfigManager storage configuration
        try:
            return self.unified_config.get_storage_configuration()
        except Exception as e:
            logger.warning(f"⚠️ Could not get storage configuration: {e}")
            # Return basic fallback configuration
            return {
                'directories': {
                    'data_directory': './data',
                    'cache_directory': './cache',
                    'logs_directory': './logs',
                    'backup_directory': './backups',
                    'models_directory': './models/cache'
                },
                'cache_settings': {
                    'enable_model_cache': True,
                    'enable_analysis_cache': True
                },
                'status': 'fallback_configuration'
            }

    def get_storage_directories(self) -> Dict[str, str]:
        """
        Get storage directory configuration
        Uses StorageConfigManager if available, otherwise falls back to basic directories
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_directories()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Fallback to basic directories from environment or defaults
        return {
            'data_directory': self.unified_config.get_env('NLP_STORAGE_DATA_DIRECTORY', './data'),
            'cache_directory': self.unified_config.get_env('NLP_STORAGE_CACHE_DIRECTORY', './cache'),
            'logs_directory': self.unified_config.get_env('NLP_STORAGE_LOG_DIRECTORY', './logs'),
            'backup_directory': self.unified_config.get_env('NLP_STORAGE_BACKUP_DIRECTORY', './backups'),
            'models_directory': self.unified_config.get_env('NLP_STORAGE_MODELS_DIR', './models/cache'),
            'learning_directory': self.unified_config.get_env('NLP_STORAGE_LEARNING_DIRECTORY', './learning_data')
        }

    def get_cache_settings(self) -> Dict[str, Any]:
        """
        Get cache configuration settings
        Uses StorageConfigManager if available, otherwise falls back to environment variables
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_cache_settings()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Fallback to individual environment variables
        return {
            'enable_model_cache': self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_MODEL_CACHE', True),
            'enable_analysis_cache': self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_ANALYSIS_CACHE', True),
            'cache_cleanup_on_startup': self.unified_config.get_env_bool('NLP_STORAGE_CACHE_CLEANUP_ON_STARTUP', False),
            'model_cache_size_limit': self.unified_config.get_env('NLP_STORAGE_MODEL_CACHE_SIZE_LIMIT', 1000),
            'analysis_cache_size_limit': self.unified_config.get_env('NLP_STORAGE_ANALYSIS_CACHE_SIZE_LIMIT', 500),
            'cache_expiry_hours': self.unified_config.get_env('NLP_STORAGE_CACHE_EXPIRY_HOURS', 24)
        }

    def is_storage_cache_enabled(self) -> bool:
        """
        Check if storage caching is enabled
        Uses StorageConfigManager if available, otherwise checks environment
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.is_model_cache_enabled()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        return self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_MODEL_CACHE', True)

    def get_backup_settings(self) -> Dict[str, Any]:
        """
        Get backup configuration settings
        Uses StorageConfigManager if available, otherwise falls back to environment variables
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_backup_settings()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Fallback to individual environment variables
        return {
            'enable_automatic_backup': self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_AUTO_BACKUP', False),
            'backup_interval_hours': self.unified_config.get_env('NLP_STORAGE_BACKUP_INTERVAL_HOURS', 24),
            'backup_retention_days': self.unified_config.get_env('NLP_STORAGE_BACKUP_RETENTION_DAYS', 30),
            'compress_backups': self.unified_config.get_env_bool('NLP_STORAGE_COMPRESS_BACKUPS', True),
            'backup_learning_data': self.unified_config.get_env_bool('NLP_STORAGE_BACKUP_LEARNING_DATA', True),
            'backup_configuration': self.unified_config.get_env_bool('NLP_STORAGE_BACKUP_CONFIG', True)
        }

    # ========================================================================
    # MANAGER-DELEGATED METHODS (PRESERVED FROM PREVIOUS PHASES)
    # ========================================================================

    def get_crisis_patterns_migration_notice(self):
        """Provides migration notice for deprecated crisis pattern methods"""
        return {
            'status': 'migrated',
            'message': 'Crisis patterns have been migrated to CrisisPatternManager in Phase 3a',
            'access_method': 'Use CrisisPatternManager methods directly',
            'documentation': 'See Phase 3a migration guide for details'
        }
    
    def get_analysis_parameters_migration_notice(self):
        """Provides migration notice for deprecated analysis parameter methods"""
        return {
            'status': 'migrated',
            'message': 'Analysis parameters have been migrated to AnalysisParametersManager in Phase 3b',
            'access_method': 'Use AnalysisParametersManager methods directly',
            'documentation': 'See Phase 3b migration guide for details'
        }
    
    def get_threshold_mapping_migration_notice(self):
        """Provides migration notice for deprecated threshold mapping methods"""
        return {
            'status': 'migrated',
            'message': 'Threshold mappings have been migrated to ThresholdMappingManager in Phase 3c',
            'access_method': 'Use ThresholdMappingManager methods directly',
            'documentation': 'See Phase 3c migration guide for details'
        }
    
    # ========================================================================
    # RUNTIME SETTINGS ACCESS
    # ========================================================================
    
    def get_runtime_setting(self, key: str, default: Any = None) -> Any:
        """Get runtime setting with override support"""
        # Check overrides first
        if key in self.setting_overrides:
            return self.setting_overrides[key]
        
        # Then check runtime settings
        return self.runtime_settings.get(key, default)
    
    def set_runtime_override(self, key: str, value: Any):
        """Set runtime setting override"""
        logger.info(f"Setting runtime override: {key} = {value}")
        self.setting_overrides[key] = value
    
    def clear_runtime_override(self, key: str):
        """Clear runtime setting override"""
        if key in self.setting_overrides:
            logger.info(f"Clearing runtime override: {key}")
            del self.setting_overrides[key]
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all runtime settings with overrides applied"""
        combined_settings = self.runtime_settings.copy()
        combined_settings.update(self.setting_overrides)
        return combined_settings
    
    # ========================================================================
    # DEPRECATED METHODS WITH MIGRATION NOTICES (PRESERVED FOR COMPATIBILITY)
    # ========================================================================
    
    def get_crisis_patterns(self):
        """DEPRECATED: Crisis patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_crisis_patterns() is deprecated. Use CrisisPatternManager.get_crisis_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_enhanced_crisis_patterns(self):
        """DEPRECATED: Enhanced crisis patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_enhanced_crisis_patterns() is deprecated. Use CrisisPatternManager.get_enhanced_crisis_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_community_vocabulary_patterns(self):
        """DEPRECATED: Community vocabulary patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_community_vocabulary_patterns() is deprecated. Use CrisisPatternManager.get_community_vocabulary_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_lgbtqia_crisis_patterns(self):
        """DEPRECATED: LGBTQIA+ crisis patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_lgbtqia_crisis_patterns() is deprecated. Use CrisisPatternManager.get_lgbtqia_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_crisis_contexts(self):
        """DEPRECATED: Crisis contexts migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_crisis_contexts() is deprecated. Use CrisisPatternManager.get_crisis_context_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_positive_context_patterns(self):
        """DEPRECATED: Positive context patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_positive_context_patterns() is deprecated. Use CrisisPatternManager.get_positive_context_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()


# ============================================================================
# FACTORY FUNCTION - Updated for Phase 3d Step 9
# ============================================================================
def create_settings_manager(unified_config_manager,
    analysis_parameters_manager=None, crisis_pattern_manager=None,
    feature_config_manager=None, learning_system_manager=None,
    logging_config_manager=None, model_ensemble_manager=None,
    performance_config_manager=None, pydantic_manager=None,
    server_config_manager=None, shared_utilities_manager=None,
    storage_config_manager=None, threshold_mapping_manager=None,
    zero_shot_manager=None) -> SettingsManager:
    """
    Factory function to create SettingsManager instance - Phase 3d Step 9 Complete
    
    Args:
        unified_config_manager: UnifiedConfigManager instance
        analysis_parameters_manager: AnalysisParametersManager instance
        crisis_pattern_manager: CrisisPatternManager instance
        feature_config_manager: FeatureConfigManager instance
        learning_system_manager: LearningSystemManager instance
        logging_config_manager: LoggingConfigManager instance
        model_ensemble_manager: ModelEnsembleManager instance
        performance_config_manager: PerformanceConfigManager instance
        pydantic_manager: PydanticManager instance
        server_config_manager: ServerConfigManager instance
        shared_utilities_manager: SharedUtilitiesManager instance
        storage_config_manager: StorageConfigManager instance
        threshold_mapping_manager: ThresholdMappingManager instance
        zero_shot_manager: ZeroShotManager instance

    Returns:
        SettingsManager instance
    """
    return SettingsManager(
        unified_config_manager=unified_config_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        feature_config_manager=feature_config_manager,
        learning_system_manager=learning_system_manager,
        logging_config_manager=logging_config_manager,
        model_ensemble_manager=model_ensemble_manager,
        performance_config_manager=performance_config_manager,
        pydantic_manager=pydantic_manager,
        server_config_manager=server_config_manager,
        shared_utilities_manager=shared_utilities_manager,
        storage_config_manager=storage_config_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        zero_shot_manager=zero_shot_manager,
    )

# ============================================================================
# CLEAN ARCHITECTURE EXPORTS (Phase 3d Step 9 Complete)
# ============================================================================

__all__ = [
    'SettingsManager',
    'create_settings_manager',
    'SERVER_CONFIG'  # Non-migratable server info
]

logger.info("✅ SettingsManager v3.1d Step 9 loaded - UnifiedConfigManager integration complete, direct os.getenv() calls eliminated")