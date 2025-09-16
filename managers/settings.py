# ash-nlp/managers/settings_manager.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Runtime Settings and Configuration Overrides for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-3
LAST MODIFIED: 2025-08-22
PHASE: 3e, Sub-step 5.5, Task 5 - SettingsManager Standard Cleanup
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
    "description": "Phase 3e: Server configuration managed by UnifiedConfigManager",
    "note": "These legacy constants preserved for backward compatibility only",
    "version": "3.1e-5.5",
    "unified_config": True
}

class SettingsManager:
    """
    Manages runtime settings and configuration overrides for Ash NLP Service
    
    Phase 3e Sub-step 5.5: Enhanced with get_config_section() patterns and improved coordination
    
    This manager serves as the central coordination point for all configuration across the system.
    All configuration now accessed through specialized managers with fallback support:
    - Analysis config: AnalysisConfigManager
    - Crisis patterns: PatternDetectionManager
    - Feature flags: FeatureConfigManager
    - Learning system settings: LearningSystemManager
    - Logging settings: LoggingConfigManager
    - Model Ensemble settings: ModelCoordinationManager
    - Performance settings: PerformanceConfigManager
    - Pydantic settings: PydanticManager
    - Server settings: ServerConfigManager
    - Shared utilities: SharedUtilitiesManager
    - Storage settings: StorageConfigManager
    - Threshold mappings: CrisisThresholdManager
    - Zero Shot settings: ZeroShotManager
    
    Phase 3e Improvements:
    - Enhanced configuration access patterns
    - Improved error handling and resilience
    - Better integration with specialized managers
    """
    
    def __init__(self, unified_config,
        analysis_config_manager=None, pattern_detection_manager=None,
        feature_config_manager=None, learning_system_manager=None,
        logging_config_manager=None, model_coordination_manager=None,
        performance_config_manager=None, pydantic_manager=None,
        server_config_manager=None, shared_utilities_manager=None,
        storage_config_manager=None, crisis_threshold_manager=None,
        zero_shot_manager=None):
        """
        Initialize SettingsManager with dependency injection for all managers
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
            analysis_config_manager: AnalysisConfigManager instance
            pattern_detection_manager: PatternDetectionManager instance
            feature_config_manager: FeatureConfigManager instance
            learning_system_manager: LearningSystemManager instance
            logging_config_manager: LoggingConfigManager instance
            model_coordination_manager: ModelCoordinationManager instance
            performance_config_manager: PerformanceConfigManager instance
            pydantic_manager: PydanticManager instance
            server_config_manager: ServerConfigManager instance
            shared_utilities_manager: SharedUtilitiesManager instance
            storage_config_manager: StorageConfigManager instance
            crisis_threshold_manager: CrisisThresholdManager instance
            zero_shot_manager: ZeroShotManager instance
        """
        # Core configuration manager (required)
        self.unified_config = unified_config
        
        # All specialized managers (optional dependencies)
        self.analysis_config_manager = analysis_config_manager
        self.pattern_detection_manager = pattern_detection_manager
        self.feature_config_manager = feature_config_manager
        self.learning_system_manager = learning_system_manager
        self.logging_config_manager = logging_config_manager
        self.model_coordination_manager = model_coordination_manager
        self.performance_config_manager = performance_config_manager
        self.pydantic_manager = pydantic_manager
        self.server_config_manager = server_config_manager
        self.shared_utilities_manager = shared_utilities_manager
        self.storage_config_manager = storage_config_manager
        self.crisis_threshold_manager = crisis_threshold_manager
        self.zero_shot_manager = zero_shot_manager

        # Runtime state
        self.setting_overrides = {}
        self.runtime_settings = {}
        
        # Initialize using Phase 3e patterns
        self._load_runtime_settings()
        self._validate_manager_integration()
        
        logger.info("✅ SettingsManager v3.1e-5.5 initialized - Phase 3e cleanup complete")
    
    def _load_runtime_settings(self):
        """Load runtime settings using enhanced Phase 3e configuration patterns"""
        try:
            # PHASE 3E: Enhanced configuration loading using get_config_section patterns
            phase_status = self.unified_config.get_config_section(
                'settings_config',
                'system_status.phase_status', {
                    'unified_config_manager': 'operational',
                    'manager_cleanup': 'active'
                }
            )
            
            self.runtime_settings = {
                'server': SERVER_CONFIG
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading runtime settings: {e}")
            # Provide safe defaults for resilient operation
            self._initialize_safe_runtime_defaults()
    
    def _initialize_safe_runtime_defaults(self):
        """Initialize safe runtime defaults for resilient operation"""
        self.runtime_settings = {
            'server': SERVER_CONFIG,
            'phase_status': {
                'unified_config_manager': 'operational',
                'fallback_mode': 'active',
                'safe_defaults': 'enabled'
            }
        }
        logger.info("✅ Safe runtime defaults initialized")
    
    def _validate_manager_integration(self):
        """Validate manager integration for Phase 3e"""
        managers = {
            'UnifiedConfigManager': self.unified_config,
            'AnalysisConfigManager': self.analysis_config_manager,
            'PatternDetectionManager': self.pattern_detection_manager,
            'FeatureConfigManager': self.feature_config_manager,
            'LearningSystemManager': self.learning_system_manager,
            'LoggingConfigManager': self.logging_config_manager,
            'ModelCoordinationManager': self.model_coordination_manager,
            'PerformanceConfigManager': self.performance_config_manager,
            'PydanticManager': self.pydantic_manager,
            'ServerConfigManager': self.server_config_manager,
            'SharedUtilitiesManager': self.shared_utilities_manager,
            'StorageConfigManager': self.storage_config_manager,
            'CrisisThresholdManager': self.crisis_threshold_manager,
            'ZeroShotManager': self.zero_shot_manager,
        }
        
        available_managers = [name for name, mgr in managers.items() if mgr is not None]
        missing_managers = [name for name, mgr in managers.items() if mgr is None]
        
        logger.info(f"✅ Available managers ({len(available_managers)}): {available_managers}")
        if missing_managers:
            logger.warning(f"⚠️ Missing managers ({len(missing_managers)}): {missing_managers}")
        
        # Validate that UnifiedConfigManager is available (critical for operation)
        if not self.unified_config:
            raise ValueError("UnifiedConfigManager is required for SettingsManager operation")
    
    # ========================================================================
    # UNIFIED CONFIGURATION ACCESS METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_environment_variable(self, var_name: str, default: Any = None) -> Any:
        """
        Get environment variable through UnifiedConfigManager
        REPLACES all direct os.getenv() calls throughout the system
        
        Phase 3e: Enhanced with better error handling and logging
        
        Args:
            var_name: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        try:
            return self.unified_config.get_env(var_name, default)
        except Exception as e:
            logger.warning(f"⚠️ Error getting environment variable {var_name}: {e}")
            return default
    
    def get_environment_bool(self, var_name: str, default: bool = False) -> bool:
        """Get boolean environment variable through UnifiedConfigManager"""
        try:
            return self.unified_config.get_env_bool(var_name, default)
        except Exception as e:
            logger.warning(f"⚠️ Error getting boolean environment variable {var_name}: {e}")
            return default
    
    def get_environment_int(self, var_name: str, default: int = 0) -> int:
        """Get integer environment variable through UnifiedConfigManager"""
        try:
            return self.unified_config.get_env_int(var_name, default)
        except Exception as e:
            logger.warning(f"⚠️ Error getting integer environment variable {var_name}: {e}")
            return default
    
    def get_environment_float(self, var_name: str, default: float = 0.0) -> float:
        """Get float environment variable through UnifiedConfigManager"""
        try:
            return self.unified_config.get_env_float(var_name, default)
        except Exception as e:
            logger.warning(f"⚠️ Error getting float environment variable {var_name}: {e}")
            return default
    
    def get_storage_configuration(self) -> Dict[str, Any]:
        """
        Get comprehensive storage configuration settings
        Phase 3e: Enhanced with improved manager delegation and fallback patterns
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_complete_configuration()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Fallback to UnifiedConfigManager with enhanced patterns
        try:
            # PHASE 3E: Use get_config_section pattern
            storage_config = self.unified_config.get_config_section('storage_settings')
            if storage_config:
                return storage_config
                
            # Secondary fallback to environment variables
            return self._get_storage_fallback_configuration()
            
        except Exception as e:
            logger.warning(f"⚠️ Could not get storage configuration: {e}")
            return self._get_storage_fallback_configuration()
    
    def _get_storage_fallback_configuration(self) -> Dict[str, Any]:
        """Get fallback storage configuration for resilient operation"""
        return {
            'directories': {
                'data_directory': './data',
                'cache_directory': './cache',
                'logs_directory': './logs',
                'backup_directory': './backups',
                'models_directory': './cache/models'
            },
            'cache_settings': {
                'enable_model_cache': True,
                'enable_analysis_cache': False
            },
            'status': 'fallback_configuration',
            'fallback_reason': 'resilient_operation'
        }

    def get_storage_directories(self) -> Dict[str, str]:
        """
        Get storage directory configuration
        Phase 3e: Enhanced with improved delegation patterns
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_directories()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Enhanced fallback using get_config_section pattern
        try:
            directories = self.unified_config.get_config_section('storage_settings', 'storage_configuration.directories', {})
            if directories:
                return directories
        except Exception as e:
            logger.debug(f"Configuration section not found, using environment fallback: {e}")
        
        # Final fallback to environment variables with enhanced defaults
        return {
            'data_directory': self.unified_config.get_env('NLP_STORAGE_DATA_DIRECTORY', './data'),
            'cache_directory': self.unified_config.get_env('NLP_STORAGE_CACHE_DIRECTORY', './cache'),
            'logs_directory': self.unified_config.get_env('NLP_STORAGE_LOG_DIRECTORY', './logs'),
            'backup_directory': self.unified_config.get_env('NLP_STORAGE_BACKUP_DIRECTORY', './backups'),
            'models_directory': self.unified_config.get_env('NLP_STORAGE_MODELS_DIR', './cache/models'),
            'learning_directory': self.unified_config.get_env('NLP_STORAGE_LEARNING_DIRECTORY', './data/learning')
        }

    def get_cache_settings(self) -> Dict[str, Any]:
        """
        Get cache configuration settings
        Phase 3e: Enhanced with improved delegation and configuration patterns
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_cache_settings()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Enhanced fallback using get_config_section pattern
        try:
            cache_config = self.unified_config.get_config_section('storage_settings', 'storage_configuration.cache_settings', {})
            if cache_config:
                return cache_config
        except Exception as e:
            logger.debug(f"Cache configuration section not found, using environment fallback: {e}")
        
        # Fallback to individual environment variables
        return {
            'enable_model_cache': self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_MODEL_CACHE', True),
            'enable_analysis_cache': self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_ANALYSIS_CACHE', False),
            'cache_cleanup_on_startup': self.unified_config.get_env_bool('NLP_STORAGE_CACHE_CLEANUP_ON_STARTUP', False),
            'model_cache_size_limit': self.unified_config.get_env_int('NLP_STORAGE_MODEL_CACHE_SIZE_LIMIT', 1000),
            'analysis_cache_size_limit': self.unified_config.get_env_int('NLP_STORAGE_ANALYSIS_CACHE_SIZE_LIMIT', 500),
            'cache_expiry_hours': self.unified_config.get_env_int('NLP_STORAGE_CACHE_EXPIRY_HOURS', 24)
        }

    def is_storage_cache_enabled(self) -> bool:
        """
        Check if storage caching is enabled
        Phase 3e: Enhanced with improved delegation and error handling
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.is_model_cache_enabled()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        try:
            cache_enabled = self.unified_config.get_config_section('storage_settings', 'storage_configuration.cache_settings.enable_model_cache', None)
            if cache_enabled is not None:
                return bool(cache_enabled)
        except Exception as e:
            logger.debug(f"Cache setting not found in configuration, using environment fallback: {e}")
        
        return self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_MODEL_CACHE', True)

    def get_backup_settings(self) -> Dict[str, Any]:
        """
        Get backup configuration settings
        Phase 3e: Enhanced with improved delegation and configuration patterns
        """
        if self.storage_config_manager:
            try:
                return self.storage_config_manager.get_backup_settings()
            except Exception as e:
                logger.warning(f"⚠️ StorageConfigManager error, using fallback: {e}")
        
        # Enhanced fallback using get_config_section pattern
        try:
            backup_config = self.unified_config.get_config_section('storage_settings', 'storage_configuration.backup_settings', {})
            if backup_config:
                return backup_config
        except Exception as e:
            logger.debug(f"Backup configuration section not found, using environment fallback: {e}")
        
        # Fallback to individual environment variables
        return {
            'enable_automatic_backup': self.unified_config.get_env_bool('NLP_STORAGE_ENABLE_AUTO_BACKUP', False),
            'backup_interval_hours': self.unified_config.get_env_int('NLP_STORAGE_BACKUP_INTERVAL_HOURS', 24),
            'backup_retention_days': self.unified_config.get_env_int('NLP_STORAGE_BACKUP_RETENTION_DAYS', 30),
            'compress_backups': self.unified_config.get_env_bool('NLP_STORAGE_COMPRESS_BACKUPS', True),
            'backup_learning_data': self.unified_config.get_env_bool('NLP_STORAGE_BACKUP_LEARNING_DATA', True),
            'backup_configuration': self.unified_config.get_env_bool('NLP_STORAGE_BACKUP_CONFIG', True)
        }

    # ========================================================================
    # RUNTIME SETTINGS ACCESS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_runtime_setting(self, key: str, default: Any = None) -> Any:
        """Get runtime setting with enhanced override support"""
        # Check overrides first
        if key in self.setting_overrides:
            return self.setting_overrides[key]
        
        # Then check runtime settings with dot notation support
        if '.' in key:
            try:
                keys = key.split('.')
                value = self.runtime_settings
                for k in keys:
                    value = value[k]
                return value
            except (KeyError, TypeError):
                return default
        
        return self.runtime_settings.get(key, default)
    
    def set_runtime_override(self, key: str, value: Any):
        """Set runtime setting override with enhanced logging"""
        logger.info(f"🔧 Setting runtime override: {key} = {value}")
        self.setting_overrides[key] = value
    
    def clear_runtime_override(self, key: str):
        """Clear runtime setting override with enhanced validation"""
        if key in self.setting_overrides:
            logger.info(f"🧹 Clearing runtime override: {key}")
            del self.setting_overrides[key]
        else:
            logger.debug(f"⚠️ Runtime override {key} not found, no action taken")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all runtime settings with overrides applied"""
        combined_settings = self.runtime_settings.copy()
        combined_settings.update(self.setting_overrides)
        return combined_settings
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary for monitoring and debugging
        Phase 3e: New method for enhanced system visibility
        """
        return {
            'manager_version': 'v3.1e-5.5-1',
            'total_managers_available': len([m for m in [
                self.analysis_config_manager, self.pattern_detection_manager,
                self.feature_config_manager, self.learning_system_manager,
                self.logging_config_manager, self.model_coordination_manager,
                self.performance_config_manager, self.pydantic_manager,
                self.server_config_manager, self.shared_utilities_manager,
                self.storage_config_manager, self.crisis_threshold_manager,
                self.zero_shot_manager
            ] if m is not None]),
            'runtime_overrides_count': len(self.setting_overrides),
            'runtime_settings_sections': len(self.runtime_settings),
            'unified_config_available': self.unified_config is not None,
            'initialization_status': 'complete'
        }
    
# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_settings_manager(unified_config,
    analysis_config_manager=None, pattern_detection_manager=None,
    feature_config_manager=None, learning_system_manager=None,
    logging_config_manager=None, model_coordination_manager=None,
    performance_config_manager=None, pydantic_manager=None,
    server_config_manager=None, shared_utilities_manager=None,
    storage_config_manager=None, crisis_threshold_manager=None,
    zero_shot_manager=None) -> SettingsManager:
    """
    Factory function for SettingsManager (Clean v3.1 Pattern) - Phase 3e Enhanced
    
    Args:
        unified_config_manager: UnifiedConfigManager instance
        analysis_config_manager: AnalysisConfigManager instance
        pattern_detection_manager: PatternDetectionManager instance
        feature_config_manager: FeatureConfigManager instance
        learning_system_manager: LearningSystemManager instance
        logging_config_manager: LoggingConfigManager instance
        model_coordination_manager: ModelCoordinationManager instance
        performance_config_manager: PerformanceConfigManager instance
        pydantic_manager: PydanticManager instance
        server_config_manager: ServerConfigManager instance
        shared_utilities_manager: SharedUtilitiesManager instance
        storage_config_manager: StorageConfigManager instance
        crisis_threshold_manager: CrisisThresholdManager instance
        zero_shot_manager: ZeroShotManager instance

    Returns:
        SettingsManager instance with Phase 3e enhancements
    """
    return SettingsManager(
        unified_config,
        analysis_config_manager=analysis_config_manager,
        pattern_detection_manager=pattern_detection_manager,
        feature_config_manager=feature_config_manager,
        learning_system_manager=learning_system_manager,
        logging_config_manager=logging_config_manager,
        model_coordination_manager=model_coordination_manager,
        performance_config_manager=performance_config_manager,
        pydantic_manager=pydantic_manager,
        server_config_manager=server_config_manager,
        shared_utilities_manager=shared_utilities_manager,
        storage_config_manager=storage_config_manager,
        crisis_threshold_manager=crisis_threshold_manager,
        zero_shot_manager=zero_shot_manager,
    )

# Export public interface
__all__ = [
    'SettingsManager',
    'create_settings_manager',
    'SERVER_CONFIG'  # Non-migratable server info
]

logger.info("✅ SettingsManager v3.1e-5.5-1 loaded - Phase 3e Sub-step 5.5 cleanup complete with enhanced patterns")