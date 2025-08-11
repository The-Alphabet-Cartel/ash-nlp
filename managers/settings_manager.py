"""
SettingsManager - Runtime Settings and Configuration Overrides
Phase 3d Step 9: Updated for UnifiedConfigManager - NO MORE os.getenv() calls

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
    "description": "Phase 3d Step 9: Server configuration managed by UnifiedConfigManager",
    "note": "These legacy constants preserved for backward compatibility only",
    "version": "3.1d-step9",
    "unified_config": True
}

class SettingsManager:
    """
    Manages runtime settings and configuration overrides
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    
    All configuration now accessed through specialized managers:
    - Crisis patterns: CrisisPatternManager (Phase 3a)
    - Analysis parameters: AnalysisParametersManager (Phase 3b) 
    - Threshold mappings: ThresholdMappingManager (Phase 3c)
    - Server settings: ServerConfigManager + UnifiedConfigManager (Phase 3d Step 5+9)
    - Logging settings: LoggingConfigManager + UnifiedConfigManager (Phase 3d Step 6+9)
    - Feature flags: FeatureConfigManager + UnifiedConfigManager (Phase 3d Step 7+9)
    - Performance settings: PerformanceConfigManager + UnifiedConfigManager (Phase 3d Step 7+9)
    """
    
    def __init__(self, unified_config_manager, crisis_pattern_manager=None, analysis_parameters_manager=None, 
                 threshold_mapping_manager=None, server_config_manager=None, logging_config_manager=None,
                 feature_config_manager=None, performance_config_manager=None):
        """
        Initialize SettingsManager with UnifiedConfigManager and all Phase 3d managers
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection (NEW IN STEP 9)
            crisis_pattern_manager: CrisisPatternManager instance (Phase 3a)
            analysis_parameters_manager: AnalysisParametersManager instance (Phase 3b)
            threshold_mapping_manager: ThresholdMappingManager instance (Phase 3c)
            server_config_manager: ServerConfigManager instance (Phase 3d Step 5)
            logging_config_manager: LoggingConfigManager instance (Phase 3d Step 6)
            feature_config_manager: FeatureConfigManager instance (Phase 3d Step 7)
            performance_config_manager: PerformanceConfigManager instance (Phase 3d Step 7)
        """
        # STEP 9 CHANGE: Use UnifiedConfigManager instead of ConfigManager
        self.unified_config = unified_config_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.analysis_parameters_manager = analysis_parameters_manager
        self.threshold_mapping_manager = threshold_mapping_manager
        self.server_config_manager = server_config_manager
        self.logging_config_manager = logging_config_manager
        self.feature_config_manager = feature_config_manager
        self.performance_config_manager = performance_config_manager

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
                    'unified_config_manager': 'operational',  # NEW
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
            'UnifiedConfigManager': self.unified_config,  # NEW IN STEP 9
            'AnalysisParametersManager': self.analysis_parameters_manager,
            'CrisisPatternManager': self.crisis_pattern_manager,
            'ThresholdMappingManager': self.threshold_mapping_manager,
            'ServerConfigManager': self.server_config_manager,
            'LoggingConfigManager': self.logging_config_manager,
            'FeatureConfigManager': self.feature_config_manager,
            'PerformanceConfigManager': self.performance_config_manager
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
def create_settings_manager(unified_config_manager, crisis_pattern_manager=None, analysis_parameters_manager=None,
                           threshold_mapping_manager=None, server_config_manager=None, logging_config_manager=None,
                           feature_config_manager=None, performance_config_manager=None) -> SettingsManager:
    """
    Factory function to create SettingsManager instance - Phase 3d Step 9 Complete
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (NEW IN STEP 9 - REQUIRED)
        crisis_pattern_manager: CrisisPatternManager instance (Phase 3a)
        analysis_parameters_manager: AnalysisParametersManager instance (Phase 3b)
        threshold_mapping_manager: ThresholdMappingManager instance (Phase 3c)
        server_config_manager: ServerConfigManager instance (Phase 3d Step 5)
        logging_config_manager: LoggingConfigManager instance (Phase 3d Step 6)
        feature_config_manager: FeatureConfigManager instance (Phase 3d Step 7)
        performance_config_manager: PerformanceConfigManager instance (Phase 3d Step 7)
        
    Returns:
        SettingsManager instance
    """
    return SettingsManager(
        unified_config_manager,  # STEP 9 CHANGE: First parameter is now UnifiedConfigManager
        crisis_pattern_manager=crisis_pattern_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        server_config_manager=server_config_manager,
        logging_config_manager=logging_config_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager
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