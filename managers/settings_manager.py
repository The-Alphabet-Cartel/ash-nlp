# ash/ash-nlp/managers/settings_manager.py
"""
Settings Manager for Ash NLP Service v3.1 - Phase 3b Complete
Handles runtime settings and configuration overrides

Phase 3a: Crisis patterns migrated to CrisisPatternManager and JSON configuration
Phase 3b: Analysis parameters migrated to AnalysisParametersManager and JSON configuration
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# CORE CONFIGURATION CONSTANTS (Non-migratable server info)
# ============================================================================

# Server configuration - Core system info, not migrated
SERVER_CONFIG = {
    "version": "3.1",
    "architecture": "modular_v3.1_phase_3b_complete",
    "hardware_info": {
        "cpu": "Ryzen 7 5800x",
        "gpu": "RTX 3060 (12GB VRAM)",
        "ram": "64GB",
        "inference_device": "GPU",
        "models_loaded": 3
    },
    "capabilities": {
        "crisis_analysis": "Enhanced ensemble + pattern analysis",
        "phrase_extraction": "Extract crisis keywords using model scoring",
        "pattern_learning": "Learn distinctive crisis patterns from community messages", 
        "semantic_analysis": "Enhanced crisis detection with community context",
        "community_awareness": "LGBTQIA+ specific pattern recognition via CrisisPatternManager",
        "json_configuration": "All configuration managed via JSON files with environment overrides",
        "analysis_parameters": "Analysis algorithm parameters managed via AnalysisParametersManager"
    }
}

# ============================================================================
# SETTINGS MANAGER CLASS - v3.1 Clean Architecture (Phase 3b Updated)
# ============================================================================

class SettingsManager:
    """
    Manages runtime settings and configuration overrides
    Phase 3a: Crisis patterns now managed by CrisisPatternManager
    Phase 3b: Analysis parameters now managed by AnalysisParametersManager
    """
    
    def __init__(self, config_manager, crisis_pattern_manager=None, analysis_parameters_manager=None, threshold_mapping_manager=None):
        """
        Initialize SettingsManager with ConfigManager and all Phase 3c managers
        
        Args:
            config_manager: ConfigManager instance for dependency injection
            crisis_pattern_manager: CrisisPatternManager instance (Phase 3a)
            analysis_parameters_manager: AnalysisParametersManager instance (Phase 3b)
            threshold_mapping_manager: ThresholdMappingManager instance (Phase 3c)
        """
        self.config_manager = config_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.analysis_parameters_manager = analysis_parameters_manager
        self.threshold_mapping_manager = threshold_mapping_manager  # Phase 3c

        self.setting_overrides = {}
        self.runtime_settings = {}
        
        # Load runtime settings
        self._load_runtime_settings()
        
        # Validate analysis parameters manager integration
        if self.analysis_parameters_manager is None:
            logger.warning("⚠️ AnalysisParametersManager not provided - analysis parameter methods will use fallbacks")
        
        logger.info("SettingsManager v3.1 initialized (Phase 3b - Analysis parameters externalized)")
    
    def _load_runtime_settings(self):
        """Load runtime settings from environment variables and config"""
        try:
            # Load basic runtime settings (non-migratable)
            self.runtime_settings = {
                'server': SERVER_CONFIG,
                'phase_status': {
                    'phase_2a': 'complete',
                    'phase_2b': 'complete', 
                    'phase_2c': 'complete',
                    'phase_3a': 'complete',
                    'phase_3b': 'complete',
                    'crisis_patterns': 'externalized_to_json',
                    'analysis_parameters': 'externalized_to_json'
                }
            }
            
            # Load environment overrides for non-migratable settings
            self._load_environment_overrides()
            
        except Exception as e:
            logger.error(f"Error loading runtime settings: {e}")
    
    def _load_environment_overrides(self):
        """Load setting overrides from environment variables for non-migratable settings only"""
        try:
            # NOTE: Analysis parameter overrides now handled by AnalysisParametersManager
            # Only load overrides for non-migratable settings here
            
            # Device and performance settings (non-migratable)
            if os.getenv('NLP_DEVICE'):
                self.setting_overrides['device'] = os.getenv('NLP_DEVICE')
            if os.getenv('NLP_PRECISION'):
                self.setting_overrides['precision'] = os.getenv('NLP_PRECISION')
            
            logger.debug("✅ Environment overrides loaded for non-migratable settings")
            
        except Exception as e:
            logger.error(f"Error loading environment overrides: {e}")
    
    # ========================================================================
    # DEVICE AND PERFORMANCE SETTINGS (Non-migratable)
    # ========================================================================
    
    def get_device_setting(self) -> str:
        """Get device setting (cpu/cuda/auto)"""
        return self.setting_overrides.get('device', os.getenv('NLP_DEVICE', 'auto'))
    
    def get_precision_setting(self) -> str:
        """Get precision setting (float16/float32/auto)"""
        return self.setting_overrides.get('precision', os.getenv('NLP_PRECISION', 'auto'))
    
    def get_cache_dir_setting(self) -> str:
        """Get model cache directory setting"""
        return os.getenv('NLP_CACHE_DIR', '/app/models/cache')
    
    def get_max_memory_setting(self) -> Optional[str]:
        """Get maximum memory setting"""
        return os.getenv('NLP_MAX_MEMORY')
    
    def get_offload_folder_setting(self) -> Optional[str]:
        """Get model offload folder setting"""
        return os.getenv('NLP_OFFLOAD_FOLDER')
    
    # ========================================================================
    # ANALYSIS SETTINGS - Now delegated to AnalysisParametersManager
    # ========================================================================
    
    def get_ensemble_analysis_enabled_setting(self) -> bool:
        """Get ensemble analysis enabled setting"""
        return os.getenv('NLP_ENSEMBLE_ANALYSIS_ENABLED', 'true').lower() == 'true'
    
    def get_crisis_threshold_settings(self) -> Dict[str, float]:
        """
        Get crisis threshold settings - MIGRATED to AnalysisParametersManager
        
        Returns:
            Dictionary with crisis thresholds from AnalysisParametersManager or fallback
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_crisis_thresholds()
        else:
            # Fallback to environment variables if manager not available
            logger.warning("⚠️ Using fallback crisis thresholds - AnalysisParametersManager not available")
            return {
                'high': float(os.getenv('NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH', '0.55')),
                'medium': float(os.getenv('NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM', '0.28')),
                'low': float(os.getenv('NLP_ANALYSIS_CRISIS_THRESHOLD_LOW', '0.16'))
            }
    
    def get_phrase_extraction_settings(self) -> Dict[str, Any]:
        """
        Get phrase extraction settings - MIGRATED to AnalysisParametersManager
        
        Returns:
            Dictionary with phrase extraction parameters from AnalysisParametersManager or fallback
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_phrase_extraction_parameters()
        else:
            # Fallback to environment variables if manager not available
            logger.warning("⚠️ Using fallback phrase extraction settings - AnalysisParametersManager not available")
            return {
                'min_phrase_length': int(os.getenv('NLP_ANALYSIS_MIN_PHRASE_LENGTH', '2')),
                'max_phrase_length': int(os.getenv('NLP_ANALYSIS_MAX_PHRASE_LENGTH', '6')),
                'crisis_focus': os.getenv('NLP_ANALYSIS_PHRASE_CRISIS_FOCUS', 'true').lower() == 'true',
                'community_specific': os.getenv('NLP_ANALYSIS_PHRASE_COMMUNITY_SPECIFIC', 'true').lower() == 'true',
                'min_confidence': float(os.getenv('NLP_ANALYSIS_PHRASE_MIN_CONFIDENCE', '0.3')),
                'max_results': int(os.getenv('NLP_ANALYSIS_PHRASE_MAX_RESULTS', '20'))
            }
    
    def get_pattern_learning_settings(self) -> Dict[str, Any]:
        """
        Get pattern learning settings - MIGRATED to AnalysisParametersManager
        
        Returns:
            Dictionary with pattern learning parameters from AnalysisParametersManager or fallback
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_pattern_learning_parameters()
        else:
            # Fallback to environment variables if manager not available
            logger.warning("⚠️ Using fallback pattern learning settings - AnalysisParametersManager not available")
            return {
                'min_crisis_messages': int(os.getenv('NLP_ANALYSIS_PATTERN_MIN_CRISIS_MESSAGES', '10')),
                'max_phrases_to_analyze': int(os.getenv('NLP_ANALYSIS_PATTERN_MAX_PHRASES_TO_ANALYZE', '200')),
                'min_distinctiveness_ratio': float(os.getenv('NLP_ANALYSIS_PATTERN_MIN_DISTINCTIVENESS_RATIO', '2.0')),
                'min_frequency': int(os.getenv('NLP_ANALYSIS_PATTERN_MIN_FREQUENCY', '3')),
                'confidence_thresholds': {
                    'high_confidence': float(os.getenv('NLP_ANALYSIS_PATTERN_HIGH_CONFIDENCE', '0.7')),
                    'medium_confidence': float(os.getenv('NLP_ANALYSIS_PATTERN_MEDIUM_CONFIDENCE', '0.4')),
                    'low_confidence': float(os.getenv('NLP_ANALYSIS_PATTERN_LOW_CONFIDENCE', '0.1'))
                }
            }
    
    def get_semantic_analysis_settings(self) -> Dict[str, Any]:
        """
        Get semantic analysis settings - MIGRATED to AnalysisParametersManager
        
        Returns:
            Dictionary with semantic analysis parameters from AnalysisParametersManager or fallback
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_semantic_analysis_parameters()
        else:
            # Fallback to environment variables if manager not available
            logger.warning("⚠️ Using fallback semantic analysis settings - AnalysisParametersManager not available")
            return {
                'context_window': int(os.getenv('NLP_ANALYSIS_SEMANTIC_CONTEXT_WINDOW', '3')),
                'boost_weights': {
                    'high_relevance': float(os.getenv('NLP_ANALYSIS_SEMANTIC_HIGH_RELEVANCE_BOOST', '0.1')),
                    'medium_relevance': float(os.getenv('NLP_ANALYSIS_SEMANTIC_MEDIUM_RELEVANCE_BOOST', '0.05')),
                    'family_rejection': float(os.getenv('NLP_ANALYSIS_SEMANTIC_FAMILY_REJECTION_BOOST', '0.15')),
                    'discrimination_fear': float(os.getenv('NLP_ANALYSIS_SEMANTIC_DISCRIMINATION_FEAR_BOOST', '0.15')),
                    'support_seeking': float(os.getenv('NLP_ANALYSIS_SEMANTIC_SUPPORT_SEEKING_BOOST', '-0.05'))
                }
            }
    
    # ========================================================================
    # NEW ANALYSIS PARAMETER ACCESS METHODS (Phase 3b)
    # ========================================================================
    
    def get_advanced_analysis_parameters(self) -> Dict[str, Any]:
        """
        Get advanced analysis parameters - NEW in Phase 3b
        
        Returns:
            Dictionary with advanced analysis parameters
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_advanced_parameters()
        else:
            logger.warning("⚠️ Using fallback advanced parameters - AnalysisParametersManager not available")
            return {
                'pattern_confidence_boost': float(os.getenv('NLP_ANALYSIS_PATTERN_CONFIDENCE_BOOST', '0.05')),
                'model_confidence_boost': float(os.getenv('NLP_ANALYSIS_MODEL_CONFIDENCE_BOOST', '0.0')),
                'context_signal_weight': float(os.getenv('NLP_ANALYSIS_CONTEXT_SIGNAL_WEIGHT', '1.0')),
                'temporal_urgency_multiplier': float(os.getenv('NLP_ANALYSIS_TEMPORAL_URGENCY_MULTIPLIER', '1.2')),
                'community_awareness_boost': float(os.getenv('NLP_ANALYSIS_COMMUNITY_AWARENESS_BOOST', '0.1'))
            }
    
    def get_integration_settings(self) -> Dict[str, Any]:
        """
        Get integration settings for analysis components - NEW in Phase 3b
        
        Returns:
            Dictionary with integration settings
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_integration_settings()
        else:
            logger.warning("⚠️ Using fallback integration settings - AnalysisParametersManager not available")
            return {
                'enable_pattern_analysis': os.getenv('NLP_ANALYSIS_ENABLE_PATTERN_ANALYSIS', 'true').lower() == 'true',
                'enable_semantic_analysis': os.getenv('NLP_ANALYSIS_ENABLE_SEMANTIC_ANALYSIS', 'true').lower() == 'true',
                'enable_phrase_extraction': os.getenv('NLP_ANALYSIS_ENABLE_PHRASE_EXTRACTION', 'true').lower() == 'true',
                'enable_pattern_learning': os.getenv('NLP_ANALYSIS_ENABLE_PATTERN_LEARNING', 'true').lower() == 'true',
                'integration_mode': os.getenv('NLP_ANALYSIS_INTEGRATION_MODE', 'full')
            }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """
        Get performance settings for analysis - NEW in Phase 3b
        
        Returns:
            Dictionary with performance settings
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_performance_settings()
        else:
            logger.warning("⚠️ Using fallback performance settings - AnalysisParametersManager not available")
            return {
                'analysis_timeout_ms': int(os.getenv('NLP_ANALYSIS_TIMEOUT_MS', '5000')),
                'max_concurrent_analyses': int(os.getenv('NLP_ANALYSIS_MAX_CONCURRENT', '10')),
                'cache_analysis_results': os.getenv('NLP_ANALYSIS_ENABLE_CACHING', 'true').lower() == 'true',
                'cache_ttl_seconds': int(os.getenv('NLP_ANALYSIS_CACHE_TTL_SECONDS', '300')),
                'enable_parallel_processing': os.getenv('NLP_ANALYSIS_ENABLE_PARALLEL_PROCESSING', 'true').lower() == 'true'
            }
    
    def get_debugging_settings(self) -> Dict[str, Any]:
        """
        Get debugging settings for analysis - NEW in Phase 3b
        
        Returns:
            Dictionary with debugging settings
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_debugging_settings()
        else:
            logger.warning("⚠️ Using fallback debugging settings - AnalysisParametersManager not available")
            return {
                'enable_detailed_logging': os.getenv('NLP_ANALYSIS_ENABLE_DETAILED_LOGGING', 'false').lower() == 'true',
                'log_analysis_steps': os.getenv('NLP_ANALYSIS_LOG_ANALYSIS_STEPS', 'false').lower() == 'true',
                'include_reasoning_in_response': os.getenv('NLP_ANALYSIS_INCLUDE_REASONING', 'true').lower() == 'true',
                'enable_performance_metrics': os.getenv('NLP_ANALYSIS_ENABLE_PERFORMANCE_METRICS', 'true').lower() == 'true'
            }
    
    def get_experimental_features(self) -> Dict[str, Any]:
        """
        Get experimental feature flags - NEW in Phase 3b
        
        Returns:
            Dictionary with experimental feature flags
        """
        if self.analysis_parameters_manager:
            return self.analysis_parameters_manager.get_experimental_features()
        else:
            logger.warning("⚠️ Using fallback experimental features - AnalysisParametersManager not available")
            return {
                'enable_advanced_context_analysis': os.getenv('NLP_ANALYSIS_EXPERIMENTAL_ADVANCED_CONTEXT', 'false').lower() == 'true',
                'enable_community_vocabulary_boost': os.getenv('NLP_ANALYSIS_EXPERIMENTAL_COMMUNITY_VOCAB', 'false').lower() == 'true',
                'enable_temporal_pattern_detection': os.getenv('NLP_ANALYSIS_EXPERIMENTAL_TEMPORAL_PATTERNS', 'false').lower() == 'true',
                'enable_multi_language_support': os.getenv('NLP_ANALYSIS_EXPERIMENTAL_MULTI_LANGUAGE', 'false').lower() == 'true'
            }
    
    # ========================================================================
    # MIGRATION NOTIFICATION METHODS (Phase 3a & 3b)
    # ========================================================================
    
    def get_crisis_patterns_migration_notice(self) -> Dict[str, str]:
        """
        Get migration notice for crisis patterns (Phase 3a)
        
        Returns:
            Dictionary with migration information
        """
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3a_complete',
            'new_location': 'CrisisPatternManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'CrisisPatternManager',
            'access_method': 'Use create_crisis_pattern_manager(config_manager)',
            'migration_date': '2025-08-04',
            'note': 'Crisis patterns are no longer available from SettingsManager. Use CrisisPatternManager for pattern access.'
        }
    
    def get_analysis_parameters_migration_notice(self) -> Dict[str, str]:
        """
        Get migration notice for analysis parameters (Phase 3b)
        
        Returns:
            Dictionary with migration information
        """
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3b_complete',
            'new_location': 'AnalysisParametersManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'AnalysisParametersManager',
            'access_method': 'Use create_analysis_parameters_manager(config_manager)',
            'migration_date': '2025-08-05',
            'note': 'Analysis parameters (DEFAULT_PARAMS, CRISIS_THRESHOLDS) are no longer available from SettingsManager. Use AnalysisParametersManager for parameter access.'
        }
    
    # ========================================================================
    # VALIDATION
    # ========================================================================
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate settings configuration"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Validate device setting
            device = self.get_device_setting()
            valid_devices = ['auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1']
            if device not in valid_devices:
                validation_result['warnings'].append(f"Unusual device setting: {device}")
            
            # Validate precision setting
            precision = self.get_precision_setting()
            if precision not in ['float16', 'float32', 'auto']:
                validation_result['warnings'].append(f"Unusual precision setting: {precision}")
            
            # Validate cache directory exists
            cache_dir = self.get_cache_dir_setting()
            if not Path(cache_dir).exists():
                validation_result['warnings'].append(f"Cache directory does not exist: {cache_dir}")
            
            # Validate crisis thresholds via AnalysisParametersManager
            if self.analysis_parameters_manager:
                param_validation = self.analysis_parameters_manager.validate_parameters()
                if not param_validation['valid']:
                    validation_result['errors'].extend(param_validation['errors'])
                    validation_result['warnings'].extend(param_validation['warnings'])
                    validation_result['valid'] = False
            else:
                # Fallback validation if manager not available
                thresholds = self.get_crisis_threshold_settings()
                if thresholds['high'] <= thresholds['medium'] or thresholds['medium'] <= thresholds['low']:
                    validation_result['errors'].append("Crisis thresholds must be: high > medium > low")
                    validation_result['valid'] = False
            
        except Exception as e:
            validation_result['errors'].append(f"Settings validation error: {e}")
            validation_result['valid'] = False
        
        return validation_result
    
    # ========================================================================
    # LEGACY METHOD STUBS FOR BACKWARD COMPATIBILITY WARNINGS
    # ========================================================================
    
    # Crisis patterns (Phase 3a migration)
    def get_lgbtqia_patterns(self):
        """DEPRECATED: Crisis patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_lgbtqia_patterns() is deprecated. Use CrisisPatternManager.get_lgbtqia_patterns() instead.")
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
# FACTORY FUNCTION
# ============================================================================

def create_settings_manager(config_manager, analysis_parameters_manager=None) -> SettingsManager:
    """
    Factory function to create SettingsManager instance
    
    Args:
        config_manager: ConfigManager instance for dependency injection
        analysis_parameters_manager: AnalysisParametersManager instance for analysis parameters
        
    Returns:
        SettingsManager instance
    """
    return SettingsManager(config_manager, analysis_parameters_manager)


# ============================================================================
# CLEAN ARCHITECTURE EXPORTS (Phase 3b Complete)
# ============================================================================

__all__ = [
    'SettingsManager',
    'create_settings_manager',
    # Core constants (non-migratable server information)
    'SERVER_CONFIG'
    # NOTE: 
    # - Crisis pattern constants removed in Phase 3a - now available via CrisisPatternManager
    # - Analysis parameter constants (DEFAULT_PARAMS, CRISIS_THRESHOLDS) removed in Phase 3b - now available via AnalysisParametersManager
    # To access crisis patterns, use: create_crisis_pattern_manager(config_manager)
    # To access analysis parameters, use: create_analysis_parameters_manager(config_manager)
]

# ============================================================================
# PHASE 3B MIGRATION COMPLETE
# ============================================================================

logger.info("✅ SettingsManager v3.1 - Phase 3b Migration Complete")
logger.info("🔄 Analysis parameters migrated from hardcoded constants to AnalysisParametersManager with JSON configuration")
logger.debug("📋 Remaining constants: SERVER_CONFIG (non-migratable server information)")
logger.debug("🎯 For crisis patterns, use CrisisPatternManager")
logger.debug("🎯 For analysis parameters, use AnalysisParametersManager")
logger.debug("✨ Phase 3b: All analysis algorithm parameters now externalized to JSON configuration")