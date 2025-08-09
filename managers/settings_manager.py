# ash/ash-nlp/managers/settings_manager.py
"""
Settings Manager for Ash NLP Service v3.1 - Phase 3d Step 7 Complete
Handles runtime settings and configuration overrides

Phase 3a: Crisis patterns migrated to CrisisPatternManager and JSON configuration
Phase 3b: Analysis parameters migrated to AnalysisParametersManager and JSON configuration
Phase 3c: Threshold mappings migrated to ThresholdMappingManager and JSON configuration
Phase 3d Step 5: Server configuration migrated to ServerConfigManager
Phase 3d Step 6: Logging configuration migrated to LoggingConfigManager
Phase 3d Step 7: Feature flags migrated to FeatureConfigManager, Performance settings migrated to PerformanceConfigManager

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
    "version": "3d.7",
    "architecture": "modular_v3.1_phase_3d_step_7_complete",
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
        "analysis_parameters": "Analysis algorithm parameters managed via AnalysisParametersManager",
        "threshold_mapping": "Mode-aware threshold mappings via ThresholdMappingManager",
        "feature_flags": "Feature toggle management via FeatureConfigManager",
        "performance_optimization": "Performance settings management via PerformanceConfigManager"
    }
}

# ============================================================================
# SETTINGS MANAGER CLASS - v3.1 Clean Architecture (Phase 3d Step 7 Complete)
# ============================================================================

class SettingsManager:
    """
    Manages runtime settings and configuration overrides
    Phase 3a: Crisis patterns now managed by CrisisPatternManager
    Phase 3b: Analysis parameters now managed by AnalysisParametersManager
    Phase 3c: Threshold mappings now managed by ThresholdMappingManager
    Phase 3d Step 5: Server configuration now managed by ServerConfigManager
    Phase 3d Step 6: Logging configuration now managed by LoggingConfigManager  
    Phase 3d Step 7: Feature flags now managed by FeatureConfigManager, Performance settings now managed by PerformanceConfigManager
    """
    
    def __init__(self, config_manager, crisis_pattern_manager=None, analysis_parameters_manager=None, 
                 threshold_mapping_manager=None, server_config_manager=None, logging_config_manager=None,
                 feature_config_manager=None, performance_config_manager=None):
        """
        Initialize SettingsManager with ConfigManager and all Phase 3d Step 7 managers
        
        Args:
            config_manager: ConfigManager instance for dependency injection
            crisis_pattern_manager: CrisisPatternManager instance (Phase 3a)
            analysis_parameters_manager: AnalysisParametersManager instance (Phase 3b)
            threshold_mapping_manager: ThresholdMappingManager instance (Phase 3c)
            server_config_manager: ServerConfigManager instance (Phase 3d Step 5)
            logging_config_manager: LoggingConfigManager instance (Phase 3d Step 6)
            feature_config_manager: FeatureConfigManager instance (Phase 3d Step 7)
            performance_config_manager: PerformanceConfigManager instance (Phase 3d Step 7)
        """
        self.config_manager = config_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.analysis_parameters_manager = analysis_parameters_manager
        self.threshold_mapping_manager = threshold_mapping_manager
        self.server_config_manager = server_config_manager  # Phase 3d Step 5
        self.logging_config_manager = logging_config_manager  # Phase 3d Step 6
        self.feature_config_manager = feature_config_manager  # Phase 3d Step 7
        self.performance_config_manager = performance_config_manager  # Phase 3d Step 7

        self.setting_overrides = {}
        self.runtime_settings = {}
        
        # Load runtime settings
        self._load_runtime_settings()
        
        # Validate manager integration
        self._validate_manager_integration()
        
        logger.info("SettingsManager v3.1 initialized (Phase 3d Step 7 - Feature flags & Performance settings externalized)")
    
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
                    'phase_3c': 'complete',
                    'phase_3d_step_5': 'complete',
                    'phase_3d_step_6': 'complete', 
                    'phase_3d_step_7': 'complete',
                    'crisis_patterns': 'externalized_to_json',
                    'analysis_parameters': 'externalized_to_json',
                    'threshold_mappings': 'externalized_to_json',
                    'server_configuration': 'externalized_to_json',
                    'logging_configuration': 'externalized_to_json',
                    'feature_flags': 'externalized_to_json',
                    'performance_settings': 'externalized_to_json'
                }
            }
            
            # Load environment overrides for non-migratable settings
            self._load_environment_overrides()
            
        except Exception as e:
            logger.error(f"Error loading runtime settings: {e}")
    
    def _load_environment_overrides(self):
        """Load setting overrides from environment variables for non-migratable settings only"""
        try:
            # NOTE: Most overrides now handled by specialized managers
            # Only load overrides for truly non-migratable settings here
            
            # Legacy device and precision settings (maintained for backward compatibility)
            # These are now primarily handled by PerformanceConfigManager
            if os.getenv('NLP_DEVICE'):  # Legacy variable
                self.setting_overrides['device'] = os.getenv('NLP_DEVICE')
            if os.getenv('NLP_PRECISION'):  # Legacy variable
                self.setting_overrides['precision'] = os.getenv('NLP_PRECISION')
            
            logger.debug("✅ Environment overrides loaded for non-migratable settings")
            
        except Exception as e:
            logger.error(f"Error loading environment overrides: {e}")
    
    def _validate_manager_integration(self):
        """Validate manager integration for Phase 3d Step 7"""
        managers = {
            'AnalysisParametersManager': self.analysis_parameters_manager,
            'ThresholdMappingManager': self.threshold_mapping_manager,
            'FeatureConfigManager': self.feature_config_manager,
            'PerformanceConfigManager': self.performance_config_manager
        }
        
        missing_managers = [name for name, manager in managers.items() if manager is None]
        
        if missing_managers:
            logger.warning(f"⚠️ Missing managers (will use fallbacks): {', '.join(missing_managers)}")
        
        available_managers = [name for name, manager in managers.items() if manager is not None]
        if available_managers:
            logger.debug(f"✅ Available managers: {', '.join(available_managers)}")
    
    # ========================================================================
    # FEATURE FLAGS ACCESS - NEW Phase 3d Step 7
    # ========================================================================
    
    def get_feature_flags(self) -> Dict[str, Any]:
        """
        Get all feature flags using FeatureConfigManager
        
        Returns:
            Dictionary with all feature flag categories
        """
        if self.feature_config_manager:
            return self.feature_config_manager.get_all_features()
        else:
            logger.warning("⚠️ Using fallback feature flags - FeatureConfigManager not available")
            return {
                'core_system_features': {
                    'ensemble_analysis': os.getenv('NLP_FEATURE_ENSEMBLE_ANALYSIS', 'true').lower() == 'true',
                    'pattern_integration': os.getenv('NLP_FEATURE_PATTERN_INTEGRATION', 'true').lower() == 'true',
                    'threshold_learning': os.getenv('NLP_FEATURE_THRESHOLD_LEARNING', 'true').lower() == 'true',
                    'staff_review_logic': os.getenv('NLP_FEATURE_STAFF_REVIEW_LOGIC', 'true').lower() == 'true',
                    'safety_controls': os.getenv('NLP_FEATURE_SAFETY_CONTROLS', 'true').lower() == 'true'
                },
                'analysis_component_features': {
                    'pattern_analysis': os.getenv('NLP_FEATURE_PATTERN_ANALYSIS', 'true').lower() == 'true',
                    'semantic_analysis': os.getenv('NLP_FEATURE_SEMANTIC_ANALYSIS', 'true').lower() == 'true',
                    'phrase_extraction': os.getenv('NLP_FEATURE_PHRASE_EXTRACTION', 'true').lower() == 'true',
                    'pattern_learning': os.getenv('NLP_FEATURE_PATTERN_LEARNING', 'true').lower() == 'true',
                    'analysis_caching': os.getenv('NLP_FEATURE_ANALYSIS_CACHING', 'true').lower() == 'true',
                    'parallel_processing': os.getenv('NLP_FEATURE_PARALLEL_PROCESSING', 'true').lower() == 'true'
                }
            }
    
    def get_core_system_features(self) -> Dict[str, bool]:
        """Get core system feature flags"""
        if self.feature_config_manager:
            return self.feature_config_manager.get_core_system_features()
        else:
            logger.warning("⚠️ Using fallback core system features - FeatureConfigManager not available")
            return {
                'ensemble_analysis': os.getenv('NLP_FEATURE_ENSEMBLE_ANALYSIS', 'true').lower() == 'true',
                'pattern_integration': os.getenv('NLP_FEATURE_PATTERN_INTEGRATION', 'true').lower() == 'true',
                'threshold_learning': os.getenv('NLP_FEATURE_THRESHOLD_LEARNING', 'true').lower() == 'true',
                'staff_review_logic': os.getenv('NLP_FEATURE_STAFF_REVIEW_LOGIC', 'true').lower() == 'true',
                'safety_controls': os.getenv('NLP_FEATURE_SAFETY_CONTROLS', 'true').lower() == 'true'
            }
    
    def get_experimental_features(self) -> Dict[str, bool]:
        """Get experimental feature flags"""
        if self.feature_config_manager:
            return self.feature_config_manager.get_experimental_features()
        else:
            logger.warning("⚠️ Using fallback experimental features - FeatureConfigManager not available")
            return {
                'advanced_context': os.getenv('NLP_FEATURE_EXPERIMENTAL_ADVANCED_CONTEXT', 'false').lower() == 'true',
                'community_vocab': os.getenv('NLP_FEATURE_EXPERIMENTAL_COMMUNITY_VOCAB', 'true').lower() == 'true',
                'temporal_patterns': os.getenv('NLP_FEATURE_EXPERIMENTAL_TEMPORAL_PATTERNS', 'true').lower() == 'true',
                'multi_language': os.getenv('NLP_FEATURE_EXPERIMENTAL_MULTI_LANGUAGE', 'false').lower() == 'true'
            }
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a specific feature is enabled"""
        if self.feature_config_manager:
            return self.feature_config_manager.is_feature_enabled(feature_name)
        else:
            logger.warning(f"⚠️ Using fallback for feature check: {feature_name}")
            # Map feature names to environment variables for fallback
            feature_env_map = {
                'ensemble_analysis': 'NLP_FEATURE_ENSEMBLE_ANALYSIS',
                'pattern_integration': 'NLP_FEATURE_PATTERN_INTEGRATION',
                'threshold_learning': 'NLP_FEATURE_THRESHOLD_LEARNING',
                'staff_review_logic': 'NLP_FEATURE_STAFF_REVIEW_LOGIC',
                'safety_controls': 'NLP_FEATURE_SAFETY_CONTROLS',
                'pattern_analysis': 'NLP_FEATURE_PATTERN_ANALYSIS',
                'semantic_analysis': 'NLP_FEATURE_SEMANTIC_ANALYSIS',
                'phrase_extraction': 'NLP_FEATURE_PHRASE_EXTRACTION',
                'pattern_learning': 'NLP_FEATURE_PATTERN_LEARNING',
                'analysis_caching': 'NLP_FEATURE_ANALYSIS_CACHING',
                'parallel_processing': 'NLP_FEATURE_PARALLEL_PROCESSING'
            }
            env_var = feature_env_map.get(feature_name)
            if env_var:
                return os.getenv(env_var, 'true').lower() == 'true'
            return False
    
    # ========================================================================
    # PERFORMANCE SETTINGS ACCESS - NEW Phase 3d Step 7
    # ========================================================================
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """
        Get all performance settings using PerformanceConfigManager
        
        Returns:
            Dictionary with all performance setting categories
        """
        if self.performance_config_manager:
            return self.performance_config_manager.get_all_performance_settings()
        else:
            logger.warning("⚠️ Using fallback performance settings - PerformanceConfigManager not available")
            return {
                'analysis_performance': {
                    'analysis_timeout_ms': int(os.getenv('NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS', '5000')),
                    'analysis_max_concurrent': int(os.getenv('NLP_PERFORMANCE_ANALYSIS_MAX_CONCURRENT', '10')),
                    'analysis_cache_ttl': int(os.getenv('NLP_PERFORMANCE_ANALYSIS_CACHE_TTL', '300')),
                    'request_timeout': int(os.getenv('NLP_PERFORMANCE_REQUEST_TIMEOUT', '40'))
                },
                'model_performance': {
                    'max_batch_size': int(os.getenv('NLP_PERFORMANCE_MAX_BATCH_SIZE', '32')),
                    'inference_threads': int(os.getenv('NLP_PERFORMANCE_INFERENCE_THREADS', '16')),
                    'model_precision': os.getenv('NLP_PERFORMANCE_MODEL_PRECISION', 'float16'),
                    'device': os.getenv('NLP_PERFORMANCE_DEVICE', 'auto')
                }
            }
    
    def get_analysis_performance_settings(self) -> Dict[str, Any]:
        """Get analysis performance settings"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_analysis_performance_settings()
        else:
            logger.warning("⚠️ Using fallback analysis performance settings")
            return {
                'analysis_timeout_ms': int(os.getenv('NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS', '5000')),
                'analysis_max_concurrent': int(os.getenv('NLP_PERFORMANCE_ANALYSIS_MAX_CONCURRENT', '10')),
                'analysis_cache_ttl': int(os.getenv('NLP_PERFORMANCE_ANALYSIS_CACHE_TTL', '300')),
                'request_timeout': int(os.getenv('NLP_PERFORMANCE_REQUEST_TIMEOUT', '40'))
            }
    
    def get_model_performance_settings(self) -> Dict[str, Any]:
        """Get model performance settings"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_model_performance_settings()
        else:
            logger.warning("⚠️ Using fallback model performance settings")
            return {
                'max_batch_size': int(os.getenv('NLP_PERFORMANCE_MAX_BATCH_SIZE', '32')),
                'inference_threads': int(os.getenv('NLP_PERFORMANCE_INFERENCE_THREADS', '16')),
                'model_precision': os.getenv('NLP_PERFORMANCE_MODEL_PRECISION', 'float16'),
                'device': os.getenv('NLP_PERFORMANCE_DEVICE', 'auto'),
                'max_memory': os.getenv('NLP_PERFORMANCE_MAX_MEMORY'),
                'offload_folder': os.getenv('NLP_PERFORMANCE_OFFLOAD_FOLDER')
            }
    
    # ========================================================================
    # DEVICE AND PERFORMANCE SETTINGS (Updated to use PerformanceConfigManager)
    # ========================================================================
    
    def get_device_setting(self) -> str:
        """Get device setting using PerformanceConfigManager (with legacy fallback)"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_device()
        else:
            # Legacy fallback order: override -> NLP_PERFORMANCE_DEVICE -> NLP_DEVICE -> default
            return self.setting_overrides.get('device', 
                   os.getenv('NLP_PERFORMANCE_DEVICE', 
                   os.getenv('NLP_DEVICE', 'auto')))
    
    def get_precision_setting(self) -> str:
        """Get precision setting using PerformanceConfigManager (with legacy fallback)"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_model_precision()
        else:
            # Legacy fallback order: override -> NLP_PERFORMANCE_MODEL_PRECISION -> NLP_PRECISION -> default
            return self.setting_overrides.get('precision', 
                   os.getenv('NLP_PERFORMANCE_MODEL_PRECISION', 
                   os.getenv('NLP_PRECISION', 'auto')))
    
    def get_max_batch_size_setting(self) -> int:
        """Get max batch size using PerformanceConfigManager"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_max_batch_size()
        else:
            return int(os.getenv('NLP_PERFORMANCE_MAX_BATCH_SIZE', '32'))
    
    def get_inference_threads_setting(self) -> int:
        """Get inference threads using PerformanceConfigManager"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_inference_threads()
        else:
            return int(os.getenv('NLP_PERFORMANCE_INFERENCE_THREADS', '16'))
    
    def get_cache_dir_setting(self) -> str:
        """Get model cache directory setting"""
        if self.performance_config_manager:
            # Use performance manager's cache settings if available
            cache_perf = self.performance_config_manager.get_cache_performance_settings()
            return cache_perf.get('model_cache_directory', '/app/models/cache')
        else:
            return os.getenv('NLP_CACHE_DIR', '/app/models/cache')
    
    def get_max_memory_setting(self) -> Optional[str]:
        """Get maximum memory setting using PerformanceConfigManager"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_max_memory()
        else:
            return os.getenv('NLP_PERFORMANCE_MAX_MEMORY')
    
    def get_offload_folder_setting(self) -> Optional[str]:
        """Get model offload folder setting using PerformanceConfigManager"""
        if self.performance_config_manager:
            return self.performance_config_manager.get_offload_folder()
        else:
            return os.getenv('NLP_PERFORMANCE_OFFLOAD_FOLDER')
    
    # ========================================================================
    # ANALYSIS SETTINGS - Now delegated to AnalysisParametersManager
    # ========================================================================
    
    def get_ensemble_analysis_enabled_setting(self) -> bool:
        """Get ensemble analysis enabled setting using FeatureConfigManager"""
        if self.feature_config_manager:
            return self.feature_config_manager.is_ensemble_analysis_enabled()
        else:
            return os.getenv('NLP_FEATURE_ENSEMBLE_ANALYSIS', 'true').lower() == 'true'
    
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
                'crisis_focus': os.getenv('NLP_FEATURE_PHRASE_EXTRACTION', 'true').lower() == 'true',
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
    # ANALYSIS PARAMETER ACCESS METHODS (Updated for Phase 3d Step 7)
    # ========================================================================
    
    def get_advanced_analysis_parameters(self) -> Dict[str, Any]:
        """
        Get advanced analysis parameters - Updated in Phase 3d Step 7
        
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
        Get integration settings for analysis components - Updated in Phase 3d Step 7
        Uses FeatureConfigManager for feature flag access
        
        Returns:
            Dictionary with integration settings
        """
        if self.feature_config_manager:
            # Use FeatureConfigManager for integration settings
            analysis_features = self.feature_config_manager.get_analysis_component_features()
            return {
                'enable_pattern_analysis': analysis_features.get('pattern_analysis', True),
                'enable_semantic_analysis': analysis_features.get('semantic_analysis', True),
                'enable_phrase_extraction': analysis_features.get('phrase_extraction', True),
                'enable_pattern_learning': analysis_features.get('pattern_learning', True),
                'integration_mode': os.getenv('NLP_ANALYSIS_INTEGRATION_MODE', 'full')
            }
        elif self.analysis_parameters_manager:
            # Fallback to AnalysisParametersManager
            return self.analysis_parameters_manager.get_integration_settings()
        else:
            logger.warning("⚠️ Using fallback integration settings - No managers available")
            return {
                'enable_pattern_analysis': os.getenv('NLP_FEATURE_PATTERN_ANALYSIS', 'true').lower() == 'true',
                'enable_semantic_analysis': os.getenv('NLP_FEATURE_SEMANTIC_ANALYSIS', 'true').lower() == 'true',
                'enable_phrase_extraction': os.getenv('NLP_FEATURE_PHRASE_EXTRACTION', 'true').lower() == 'true',
                'enable_pattern_learning': os.getenv('NLP_FEATURE_PATTERN_LEARNING', 'true').lower() == 'true',
                'integration_mode': os.getenv('NLP_ANALYSIS_INTEGRATION_MODE', 'full')
            }
    
    def get_debugging_settings(self) -> Dict[str, Any]:
        """
        Get debugging settings for analysis - Updated in Phase 3d Step 7
        Uses FeatureConfigManager for debug feature flags
        
        Returns:
            Dictionary with debugging settings
        """
        if self.feature_config_manager:
            # Use FeatureConfigManager for debug features
            dev_features = self.feature_config_manager.get_development_debug_features()
            return {
                'enable_detailed_logging': dev_features.get('detailed_logging', True),
                'log_analysis_steps': os.getenv('NLP_ANALYSIS_LOG_ANALYSIS_STEPS', 'false').lower() == 'true',
                'include_reasoning_in_response': os.getenv('NLP_ANALYSIS_INCLUDE_REASONING', 'true').lower() == 'true',
                'enable_performance_metrics': dev_features.get('performance_metrics', True)
            }
        elif self.analysis_parameters_manager:
            # Fallback to AnalysisParametersManager
            return self.analysis_parameters_manager.get_debugging_settings()
        else:
            logger.warning("⚠️ Using fallback debugging settings - No managers available")
            return {
                'enable_detailed_logging': os.getenv('NLP_FEATURE_DETAILED_LOGGING', 'false').lower() == 'true',
                'log_analysis_steps': os.getenv('NLP_ANALYSIS_LOG_ANALYSIS_STEPS', 'false').lower() == 'true',
                'include_reasoning_in_response': os.getenv('NLP_ANALYSIS_INCLUDE_REASONING', 'true').lower() == 'true',
                'enable_performance_metrics': os.getenv('NLP_FEATURE_PERFORMANCE_METRICS', 'true').lower() == 'true'
            }
    
    # ========================================================================
    # VALIDATION - Enhanced for Phase 3d Step 7
    # ========================================================================
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate settings configuration - Enhanced for Phase 3d Step 7"""
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
            
            # Validate feature flags via FeatureConfigManager - NEW Phase 3d Step 7
            if self.feature_config_manager:
                feature_validation_errors = self.feature_config_manager.get_validation_errors()
                if feature_validation_errors:
                    validation_result['warnings'].extend(feature_validation_errors)
            
            # Validate performance settings via PerformanceConfigManager - NEW Phase 3d Step 7
            if self.performance_config_manager:
                perf_validation_errors = self.performance_config_manager.get_validation_errors()
                if perf_validation_errors:
                    validation_result['warnings'].extend(perf_validation_errors)
            
            # Fallback threshold validation if no managers available
            if not self.analysis_parameters_manager:
                thresholds = self.get_crisis_threshold_settings()
                if thresholds['high'] <= thresholds['medium'] or thresholds['medium'] <= thresholds['low']:
                    validation_result['errors'].append("Crisis thresholds must be: high > medium > low")
                    validation_result['valid'] = False
            
        except Exception as e:
            validation_result['errors'].append(f"Settings validation error: {e}")
            validation_result['valid'] = False
        
        return validation_result
    
    # ========================================================================
    # MIGRATION NOTIFICATION METHODS (All Phases)
    # ========================================================================
    
    def get_crisis_patterns_migration_notice(self) -> Dict[str, str]:
        """Get migration notice for crisis patterns (Phase 3a)"""
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3a_complete',
            'new_location': 'CrisisPatternManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'CrisisPatternManager',
            'access_method': 'Use create_crisis_pattern_manager(config_manager)',
            'migration_date': '2025-08-04'
        }
    
    def get_analysis_parameters_migration_notice(self) -> Dict[str, str]:
        """Get migration notice for analysis parameters (Phase 3b)"""
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3b_complete',
            'new_location': 'AnalysisParametersManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'AnalysisParametersManager',
            'access_method': 'Use create_analysis_parameters_manager(config_manager)',
            'migration_date': '2025-08-05'
        }
    
    def get_feature_flags_migration_notice(self) -> Dict[str, str]:
        """Get migration notice for feature flags (Phase 3d Step 7) - NEW"""
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3d_step_7_complete',
            'new_location': 'FeatureConfigManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'FeatureConfigManager',
            'access_method': 'Use create_feature_config_manager(config_manager)',
            'migration_date': '2025-08-08'
        }
    
    def get_performance_settings_migration_notice(self) -> Dict[str, str]:
        """Get migration notice for performance settings (Phase 3d Step 7) - NEW"""
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3d_step_7_complete',
            'new_location': 'PerformanceConfigManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'PerformanceConfigManager',
            'access_method': 'Use create_performance_config_manager(config_manager)',
            'migration_date': '2025-08-08'
        }
    
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
# FACTORY FUNCTION - Updated for Phase 3d Step 7
# ============================================================================
def create_settings_manager(config_manager, crisis_pattern_manager=None, analysis_parameters_manager=None,
                           threshold_mapping_manager=None, server_config_manager=None, logging_config_manager=None,
                           feature_config_manager=None, performance_config_manager=None) -> SettingsManager:
    """
    Factory function to create SettingsManager instance - Phase 3d Step 7 Complete
    
    Args:
        config_manager: ConfigManager instance for dependency injection
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
        config_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        server_config_manager=server_config_manager,
        logging_config_manager=logging_config_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager
    )

# ============================================================================
# CLEAN ARCHITECTURE EXPORTS (Phase 3d Step 7 Complete)
# ============================================================================

__all__ = [
    'SettingsManager',
    'create_settings_manager',
    'SERVER_CONFIG'  # Non-migratable server information
]

# ============================================================================
# PHASE 3D STEP 7 MIGRATION COMPLETE
# ============================================================================

logger.info("✅ SettingsManager v3.1 - Phase 3d Step 7 Migration Complete")
logger.info("🚩 Feature flags migrated from scattered environment variables to FeatureConfigManager with JSON configuration")
logger.info("⚡ Performance settings migrated from scattered environment variables to PerformanceConfigManager with JSON configuration")
logger.debug("📋 Remaining constants: SERVER_CONFIG (non-migratable server information)")
logger.debug("🎯 For crisis patterns, use CrisisPatternManager")
logger.debug("🎯 For analysis parameters, use AnalysisParametersManager")
logger.debug("🎯 For threshold mappings, use ThresholdMappingManager")
logger.debug("🎯 For feature flags, use FeatureConfigManager")
logger.debug("🎯 For performance settings, use PerformanceConfigManager")
logger.debug("✨ Phase 3d Step 7: All feature flags and performance settings now externalized to JSON configuration")