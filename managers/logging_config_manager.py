# ash-nlp/managers/logging_config_manager.py
"""
Centralized Logging Configuration Manager for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

class LoggingConfigManager:
    """
    Centralized logging configuration management for Ash-NLP
    Phase 3d Step 6: Consolidates all logging-related environment variables
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    """
    
    def __init__(self, unified_config_manager):
        """
        Initialize LoggingConfigManager with UnifiedConfigManager integration
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
        """
        # STEP 9 CHANGE: Use UnifiedConfigManager instead of ConfigManager
        self.unified_config = unified_config_manager
        
        # Load logging configuration using unified manager
        self.logging_config = self._load_logging_configuration()
        
        logger.info("LoggingConfigManager v3.1d Step 9 initialized - UnifiedConfigManager integration complete")
    
    def _load_logging_configuration(self) -> Dict[str, Any]:
        """Load logging configuration using UnifiedConfigManager (NO MORE os.getenv())"""
        try:
            # Load logging configuration from JSON through unified manager
            config = self.unified_config.load_config_file('logging_settings')
            
            if config and 'logging_configuration' in config:
                logger.info("✅ Logging configuration loaded from JSON with environment overrides")
                return config['logging_configuration']
            else:
                logger.warning("⚠️ JSON logging configuration not found, using environment fallback")
                return self._get_fallback_logging_config()
                
        except Exception as e:
            logger.error(f"❌ Error loading logging configuration: {e}")
            return self._get_fallback_logging_config()
    
    def _get_fallback_logging_config(self) -> Dict[str, Any]:
        """Get fallback logging configuration using UnifiedConfigManager (NO MORE os.getenv())"""
        logger.info("🔧 Using UnifiedConfigManager for fallback logging configuration")
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv() for ALL variables
        return {
            'global_settings': {
                'log_level': self.unified_config.get_env('GLOBAL_LOG_LEVEL', 'INFO'),  # PRESERVED GLOBAL
                'log_file': self.unified_config.get_env('NLP_STORAGE_LOG_FILE', 'nlp_service.log'),
                'log_directory': self.unified_config.get_env('NLP_STORAGE_LOGS_DIR', './logs'),
                'enable_console_output': self.unified_config.get_env_bool('GLOBAL_LOGGING_ENABLE_CONSOLE', True),
                'enable_file_output': self.unified_config.get_env_bool('GLOBAL_LOGGING_ENABLE_FILE', True)
            },
            'detailed_logging': {
                'enable_detailed': self.unified_config.get_env_bool('NLP_LOGGING_ENABLE_DETAILED', True),
                'include_raw_labels': self.unified_config.get_env_bool('NLP_LOGGING_INCLUDE_RAW_LABELS', True),
                'analysis_steps': self.unified_config.get_env_bool('NLP_LOGGING_ANALYSIS_STEPS', False),
                'performance_metrics': self.unified_config.get_env_bool('NLP_LOGGING_PERFORMANCE_METRICS', True),
                'include_reasoning': self.unified_config.get_env_bool('NLP_LOGGING_INCLUDE_REASONING', True)
            },
            'component_logging': {
                'threshold_changes': self.unified_config.get_env_bool('NLP_LOGGING_THRESHOLD_CHANGES', True),
                'model_disagreements': self.unified_config.get_env_bool('NLP_LOGGING_MODEL_DISAGREEMENTS', True),
                'staff_review_triggers': self.unified_config.get_env_bool('NLP_LOGGING_STAFF_REVIEW_TRIGGERS', True),
                'pattern_adjustments': self.unified_config.get_env_bool('NLP_LOGGING_PATTERN_ADJUSTMENTS', True),
                'learning_updates': self.unified_config.get_env_bool('NLP_LOGGING_LEARNING_UPDATES', True),
                'label_mappings': self.unified_config.get_env_bool('NLP_LOGGING_LABEL_MAPPINGS', True),
                'ensemble_decisions': self.unified_config.get_env_bool('NLP_LOGGING_ENSEMBLE_DECISIONS', True),
                'crisis_detection': self.unified_config.get_env_bool('NLP_LOGGING_CRISIS_DETECTION', True)
            },
            'development_logging': {
                'debug_mode': self.unified_config.get_env_bool('NLP_LOGGING_DEBUG_MODE', False),
                'trace_requests': self.unified_config.get_env_bool('NLP_LOGGING_TRACE_REQUESTS', False),
                'log_configuration_loading': self.unified_config.get_env_bool('NLP_LOGGING_CONFIG_LOADING', False),
                'log_manager_initialization': self.unified_config.get_env_bool('NLP_LOGGING_MANAGER_INIT', True),
                'log_environment_variables': self.unified_config.get_env_bool('NLP_LOGGING_ENV_VARS', False)
            }
        }
    
    # ========================================================================
    # GLOBAL LOGGING SETTINGS ACCESS METHODS
    # ========================================================================
    
    def get_global_logging_settings(self) -> Dict[str, Any]:
        """Get global logging settings (GLOBAL_* variables preserved)"""
        return self.logging_config.get('global_settings', {
            'log_level': 'INFO',
            'log_file': 'nlp_service.log',
            'log_directory': './logs',
            'enable_console_output': True,
            'enable_file_output': True
        })
    
    def get_log_level(self) -> str:
        """Get current log level (GLOBAL_LOG_LEVEL preserved)"""
        global_settings = self.get_global_logging_settings()
        return global_settings.get('log_level', 'INFO')
    
    def get_log_directory(self) -> str:
        """Get log directory path"""
        global_settings = self.get_global_logging_settings()
        return global_settings.get('log_directory', './logs')
    
    def get_log_file(self) -> str:
        """Get log file name"""
        global_settings = self.get_global_logging_settings()
        return global_settings.get('log_file', 'nlp_service.log')
    
    def is_console_output_enabled(self) -> bool:
        """Check if console output is enabled (GLOBAL_LOGGING_ENABLE_CONSOLE preserved)"""
        global_settings = self.get_global_logging_settings()
        return global_settings.get('enable_console_output', True)
    
    def is_file_output_enabled(self) -> bool:
        """Check if file output is enabled (GLOBAL_LOGGING_ENABLE_FILE preserved)"""
        global_settings = self.get_global_logging_settings()
        return global_settings.get('enable_file_output', True)
    
    # ========================================================================
    # DETAILED LOGGING SETTINGS ACCESS METHODS
    # ========================================================================
    
    def get_detailed_logging_settings(self) -> Dict[str, Any]:
        """Get detailed logging settings"""
        return self.logging_config.get('detailed_logging', {
            'enable_detailed': True,
            'include_raw_labels': True,
            'analysis_steps': False,
            'performance_metrics': True,
            'include_reasoning': True
        })
    
    def is_detailed_logging_enabled(self) -> bool:
        """Check if detailed logging is enabled"""
        detailed_settings = self.get_detailed_logging_settings()
        enable_detailed = detailed_settings.get('enable_detailed', True)
        
        # Ensure boolean type safety
        if isinstance(enable_detailed, str):
            return enable_detailed.lower() in ('true', '1', 'yes', 'on')
        return bool(enable_detailed)
    
    def should_include_raw_labels(self) -> bool:
        """Check if raw labels should be included in logs"""
        detailed_settings = self.get_detailed_logging_settings()
        include_raw = detailed_settings.get('include_raw_labels', True)
        
        if isinstance(include_raw, str):
            return include_raw.lower() in ('true', '1', 'yes', 'on')
        return bool(include_raw)
    
    def should_log_analysis_steps(self) -> bool:
        """Check if analysis steps should be logged"""
        detailed_settings = self.get_detailed_logging_settings()
        log_steps = detailed_settings.get('analysis_steps', False)
        
        if isinstance(log_steps, str):
            return log_steps.lower() in ('true', '1', 'yes', 'on')
        return bool(log_steps)
    
    def should_log_performance_metrics(self) -> bool:
        """Check if performance metrics should be logged"""
        detailed_settings = self.get_detailed_logging_settings()
        log_metrics = detailed_settings.get('performance_metrics', True)
        
        if isinstance(log_metrics, str):
            return log_metrics.lower() in ('true', '1', 'yes', 'on')
        return bool(log_metrics)
    
    def should_include_reasoning(self) -> bool:
        """Check if reasoning should be included in logs"""
        detailed_settings = self.get_detailed_logging_settings()
        include_reasoning = detailed_settings.get('include_reasoning', True)
        
        if isinstance(include_reasoning, str):
            return include_reasoning.lower() in ('true', '1', 'yes', 'on')
        return bool(include_reasoning)
    
    # ========================================================================
    # COMPONENT LOGGING SETTINGS ACCESS METHODS
    # ========================================================================
    
    def get_component_logging_settings(self) -> Dict[str, Any]:
        """Get component-specific logging settings"""
        return self.logging_config.get('component_logging', {
            'threshold_changes': True,
            'model_disagreements': True,
            'staff_review_triggers': True,
            'pattern_adjustments': True,
            'learning_updates': True,
            'label_mappings': True,
            'ensemble_decisions': True,
            'crisis_detection': True
        })
    
    def should_log_threshold_changes(self) -> bool:
        """Check if threshold changes should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('threshold_changes', True))
    
    def should_log_model_disagreements(self) -> bool:
        """Check if model disagreements should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('model_disagreements', True))
    
    def should_log_staff_review_triggers(self) -> bool:
        """Check if staff review triggers should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('staff_review_triggers', True))
    
    def should_log_pattern_adjustments(self) -> bool:
        """Check if pattern adjustments should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('pattern_adjustments', True))
    
    def should_log_learning_updates(self) -> bool:
        """Check if learning updates should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('learning_updates', True))
    
    def should_log_label_mappings(self) -> bool:
        """Check if label mappings should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('label_mappings', True))
    
    def should_log_ensemble_decisions(self) -> bool:
        """Check if ensemble decisions should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('ensemble_decisions', True))
    
    def should_log_crisis_detection(self) -> bool:
        """Check if crisis detection should be logged"""
        component_settings = self.get_component_logging_settings()
        return self._safe_bool_conversion(component_settings.get('crisis_detection', True))
    
    # ========================================================================
    # DEVELOPMENT LOGGING SETTINGS ACCESS METHODS
    # ========================================================================
    
    def get_development_logging_settings(self) -> Dict[str, Any]:
        """Get development logging settings"""
        return self.logging_config.get('development_logging', {
            'debug_mode': False,
            'trace_requests': False,
            'log_configuration_loading': False,
            'log_manager_initialization': True,
            'log_environment_variables': False
        })
    
    def is_debug_mode_enabled(self) -> bool:
        """Check if debug mode is enabled"""
        dev_settings = self.get_development_logging_settings()
        return self._safe_bool_conversion(dev_settings.get('debug_mode', False))
    
    def should_trace_requests(self) -> bool:
        """Check if requests should be traced"""
        dev_settings = self.get_development_logging_settings()
        return self._safe_bool_conversion(dev_settings.get('trace_requests', False))
    
    def should_log_configuration_loading(self) -> bool:
        """Check if configuration loading should be logged"""
        dev_settings = self.get_development_logging_settings()
        return self._safe_bool_conversion(dev_settings.get('log_configuration_loading', False))
    
    def should_log_manager_initialization(self) -> bool:
        """Check if manager initialization should be logged"""
        dev_settings = self.get_development_logging_settings()
        return self._safe_bool_conversion(dev_settings.get('log_manager_initialization', True))
    
    def should_log_environment_variables(self) -> bool:
        """Check if environment variables should be logged"""
        dev_settings = self.get_development_logging_settings()
        return self._safe_bool_conversion(dev_settings.get('log_environment_variables', False))
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _safe_bool_conversion(self, value: Any) -> bool:
        """Safely convert value to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    
    def get_all_logging_settings(self) -> Dict[str, Any]:
        """Get all logging settings"""
        return {
            'global_settings': self.get_global_logging_settings(),
            'detailed_logging': self.get_detailed_logging_settings(),
            'component_logging': self.get_component_logging_settings(),
            'development_logging': self.get_development_logging_settings()
        }
    
    def get_logging_status(self) -> Dict[str, Any]:
        """Get comprehensive logging status"""
        return {
            'manager_status': 'operational',
            'configuration_source': 'unified_config_manager',
            'direct_os_getenv_calls': 'eliminated',
            'global_settings': self.get_global_logging_settings(),
            'detailed_logging_enabled': self.is_detailed_logging_enabled(),
            'debug_mode_enabled': self.is_debug_mode_enabled(),
            'console_output_enabled': self.is_console_output_enabled(),
            'file_output_enabled': self.is_file_output_enabled(),
            'unified_config_manager': True
        }

# ========================================================================
# FACTORY FUNCTION - Updated for Phase 3d Step 9
# ========================================================================

def create_logging_config_manager(unified_config_manager) -> LoggingConfigManager:
    """
    Factory function for creating LoggingConfigManager instance - Phase 3d Step 9
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for dependency injection
        
    Returns:
        Initialized LoggingConfigManager instance
        
    Raises:
        ValueError: If unified_config_manager is None or invalid
    """
    logger.debug("🏭 Creating LoggingConfigManager with UnifiedConfigManager (Phase 3d Step 9)")
    
    if not unified_config_manager:
        raise ValueError("UnifiedConfigManager is required for LoggingConfigManager factory")
    
    return LoggingConfigManager(unified_config_manager)

# ========================================================================
# MODULE EXPORTS - CLEAN V3.1 STANDARD
# ========================================================================

__all__ = ['LoggingConfigManager', 'create_logging_config_manager']

logger.info("✅ LoggingConfigManager v3.1d Step 9 loaded - UnifiedConfigManager integration complete, direct os.getenv() calls eliminated")