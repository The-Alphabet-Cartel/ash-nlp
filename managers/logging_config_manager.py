"""
Logging Configuration Manager for Ash-NLP v3.1d
Phase 3d Step 6: Storage & Logging Cleanup

Centralizes all logging configuration management following Clean v3.1 architecture.
Uses Python's built-in logging mechanism only - no custom logging implementations.

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Import ConfigManager for dependency injection
from managers.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class LoggingConfigManager:
    """
    Logging Configuration Manager - Phase 3d Step 6
    
    Manages all logging configuration following Clean v3.1 architecture:
    - Factory function pattern with dependency injection
    - JSON configuration with environment variable overrides  
    - Centralized logging settings management
    - Python logging integration only (no custom mechanisms)
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize LoggingConfigManager with dependency injection
        
        Args:
            config_manager: ConfigManager instance for accessing logging configuration
        """
        if not config_manager:
            raise ValueError("ConfigManager is required for LoggingConfigManager")
        
        self.config_manager = config_manager
        self._logging_config = None
        self._validation_errors = []
        
        logger.debug("🔧 LoggingConfigManager initialized with Clean v3.1 architecture")
        
        # Load and validate configuration on initialization
        self._load_configuration()
        self._validate_configuration()
        
        if self._validation_errors:
            error_msg = f"Logging configuration validation failed: {', '.join(self._validation_errors)}"
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        logger.info("✅ LoggingConfigManager initialized and validated successfully")
    
    def _load_configuration(self):
        """Load logging configuration from JSON with environment variable overrides"""
        try:
            logger.debug("📋 Loading logging configuration...")
            self._logging_config = self.config_manager.load_config_file('logging_settings')
            
            if not self._logging_config:
                logger.warning("⚠️ No logging_settings.json found, using environment fallback")
                self._logging_config = self._get_fallback_logging_config()
            else:
                logger.debug("✅ Logging configuration loaded from JSON")
                
        except Exception as e:
            logger.error(f"❌ Error loading logging configuration: {e}")
            logger.info("🔧 Using fallback environment-only configuration")
            self._logging_config = self._get_fallback_logging_config()
    
    def _get_fallback_logging_config(self) -> Dict[str, Any]:
        """
        Fallback logging configuration using environment variables directly
        Uses standardized Phase 3d Step 6 variable names
        """
        logger.info("🔧 Using Phase 3d standardized environment variables for logging configuration")
        
        return {
            'logging_configuration': {
                'global_settings': {
                    'log_level': os.getenv('GLOBAL_LOG_LEVEL', 'INFO'),  # PRESERVED GLOBAL
                    'log_file': os.getenv('NLP_STORAGE_LOG_FILE', 'nlp_service.log'),
                    'log_directory': os.getenv('NLP_STORAGE_LOGS_DIR', './logs'),
                    'enable_console_output': self._parse_bool(os.getenv('GLOBAL_LOGGING_ENABLE_CONSOLE', 'true')),
                    'enable_file_output': self._parse_bool(os.getenv('GLOBAL_LOGGING_ENABLE_FILE', 'true'))
                },
                'detailed_logging': {
                    'enable_detailed': self._parse_bool(os.getenv('NLP_LOGGING_ENABLE_DETAILED', 'true')),
                    'include_raw_labels': self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_RAW_LABELS', 'true')),
                    'analysis_steps': self._parse_bool(os.getenv('NLP_LOGGING_ANALYSIS_STEPS', 'false')),
                    'performance_metrics': self._parse_bool(os.getenv('NLP_LOGGING_PERFORMANCE_METRICS', 'true')),
                    'include_reasoning': self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_REASONING', 'true'))
                },
                'component_logging': {
                    'threshold_changes': self._parse_bool(os.getenv('NLP_LOGGING_THRESHOLD_CHANGES', 'true')),
                    'model_disagreements': self._parse_bool(os.getenv('NLP_LOGGING_MODEL_DISAGREEMENTS', 'true')),
                    'staff_review_triggers': self._parse_bool(os.getenv('NLP_LOGGING_STAFF_REVIEW_TRIGGERS', 'true')),
                    'pattern_adjustments': self._parse_bool(os.getenv('NLP_LOGGING_PATTERN_ADJUSTMENTS', 'true')),
                    'learning_updates': self._parse_bool(os.getenv('NLP_LOGGING_LEARNING_UPDATES', 'true')),
                    'label_mappings': self._parse_bool(os.getenv('NLP_LOGGING_LABEL_MAPPINGS', 'true')),
                    'ensemble_decisions': self._parse_bool(os.getenv('NLP_LOGGING_ENSEMBLE_DECISIONS', 'true')),
                    'crisis_detection': self._parse_bool(os.getenv('NLP_LOGGING_CRISIS_DETECTION', 'true'))
                },
                'development_logging': {
                    'debug_mode': self._parse_bool(os.getenv('NLP_LOGGING_DEBUG_MODE', 'false')),
                    'trace_requests': self._parse_bool(os.getenv('NLP_LOGGING_TRACE_REQUESTS', 'false')),
                    'log_configuration_loading': self._parse_bool(os.getenv('NLP_LOGGING_CONFIG_LOADING', 'false')),
                    'log_manager_initialization': self._parse_bool(os.getenv('NLP_LOGGING_MANAGER_INIT', 'true')),
                    'log_environment_variables': self._parse_bool(os.getenv('NLP_LOGGING_ENV_VARS', 'false'))
                }
            }
        }
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean values from environment variables"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    
    def _validate_configuration(self):
        """Validate logging configuration settings"""
        self._validation_errors = []
        
        if not self._logging_config:
            self._validation_errors.append("No logging configuration available")
            return
        
        logging_config = self._logging_config.get('logging_configuration', {})
        
        # Validate global settings
        global_settings = logging_config.get('global_settings', {})
        if global_settings:
            log_level = global_settings.get('log_level', 'INFO')
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if log_level not in valid_levels:
                self._validation_errors.append(f"Invalid log level: {log_level}. Must be one of {valid_levels}")
            
            log_file = global_settings.get('log_file', '')
            if not log_file or not isinstance(log_file, str):
                self._validation_errors.append("Log file must be a non-empty string")
        
        logger.debug(f"🔍 Logging configuration validation complete. Errors: {len(self._validation_errors)}")
    
    # ========================================================================
    # ENHANCED PUBLIC CONFIGURATION ACCESS METHODS - BETTER ERROR HANDLING
    # ========================================================================

    def get_global_logging_settings(self) -> Dict[str, Any]:
        """
        Get global logging settings including GLOBAL_LOG_LEVEL preservation
        
        Returns:
            Dictionary with global logging configuration
        """
        try:
            if not self._logging_config:
                logger.warning("⚠️ No logging configuration available, using defaults")
                return {
                    'log_level': os.getenv('GLOBAL_LOG_LEVEL', 'INFO'),
                    'log_file': os.getenv('NLP_STORAGE_LOG_FILE', 'nlp_service.log'),
                    'log_directory': os.getenv('NLP_STORAGE_LOGS_DIR', './logs'),
                    'enable_console_output': True,
                    'enable_file_output': True,
                    'log_format': '%(asctime)s %(levelname)s: %(name)s - %(message)s'
                }
            
            logging_config = self._logging_config.get('logging_configuration', {})
            global_settings = logging_config.get('global_settings', {})
            
            # Provide safe defaults for all settings
            result = {
                'log_level': global_settings.get('log_level', os.getenv('GLOBAL_LOG_LEVEL', 'INFO')),
                'log_file': global_settings.get('log_file', os.getenv('NLP_STORAGE_LOG_FILE', 'nlp_service.log')),
                'log_directory': global_settings.get('log_directory', os.getenv('NLP_STORAGE_LOGS_DIR', './logs')),
                'enable_console_output': global_settings.get('enable_console_output', True),
                'enable_file_output': global_settings.get('enable_file_output', True),
                'log_format': global_settings.get('log_format', '%(asctime)s %(levelname)s: %(name)s - %(message)s')
            }
            
            logger.debug(f"🔍 Global logging settings: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting global logging settings: {e}")
            # Return safe defaults
            return {
                'log_level': os.getenv('GLOBAL_LOG_LEVEL', 'INFO'),
                'log_file': 'nlp_service.log',
                'log_directory': './logs',
                'enable_console_output': True,
                'enable_file_output': True,
                'log_format': '%(asctime)s %(levelname)s: %(name)s - %(message)s'
            }

    def get_detailed_logging_settings(self) -> Dict[str, Any]:
        """
        Get detailed logging settings for enhanced system monitoring
        
        Returns:
            Dictionary with detailed logging configuration
        """
        try:
            if not self._logging_config:
                logger.warning("⚠️ No logging configuration available, using defaults")
                return {
                    'enable_detailed': self._parse_bool(os.getenv('NLP_LOGGING_ENABLE_DETAILED', 'true')),
                    'include_raw_labels': self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_RAW_LABELS', 'true')),
                    'analysis_steps': self._parse_bool(os.getenv('NLP_LOGGING_ANALYSIS_STEPS', 'false')),
                    'performance_metrics': self._parse_bool(os.getenv('NLP_LOGGING_PERFORMANCE_METRICS', 'true')),
                    'include_reasoning': self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_REASONING', 'true'))
                }
            
            logging_config = self._logging_config.get('logging_configuration', {})
            detailed_settings = logging_config.get('detailed_logging', {})
            
            result = {
                'enable_detailed': detailed_settings.get('enable_detailed', 
                                                       self._parse_bool(os.getenv('NLP_LOGGING_ENABLE_DETAILED', 'true'))),
                'include_raw_labels': detailed_settings.get('include_raw_labels', 
                                                           self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_RAW_LABELS', 'true'))),
                'analysis_steps': detailed_settings.get('analysis_steps', 
                                                       self._parse_bool(os.getenv('NLP_LOGGING_ANALYSIS_STEPS', 'false'))),
                'performance_metrics': detailed_settings.get('performance_metrics', 
                                                            self._parse_bool(os.getenv('NLP_LOGGING_PERFORMANCE_METRICS', 'true'))),
                'include_reasoning': detailed_settings.get('include_reasoning', 
                                                          self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_REASONING', 'true')))
            }
            
            logger.debug(f"🔍 Detailed logging settings: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting detailed logging settings: {e}")
            # Return safe defaults with environment fallbacks
            return {
                'enable_detailed': self._parse_bool(os.getenv('NLP_LOGGING_ENABLE_DETAILED', 'true')),
                'include_raw_labels': self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_RAW_LABELS', 'true')),
                'analysis_steps': self._parse_bool(os.getenv('NLP_LOGGING_ANALYSIS_STEPS', 'false')),
                'performance_metrics': self._parse_bool(os.getenv('NLP_LOGGING_PERFORMANCE_METRICS', 'true')),
                'include_reasoning': self._parse_bool(os.getenv('NLP_LOGGING_INCLUDE_REASONING', 'true'))
            }

    def get_component_logging_settings(self) -> Dict[str, Any]:
        """
        Get component-specific logging settings for different system parts
        
        Returns:
            Dictionary with component logging configuration
        """
        try:
            if not self._logging_config:
                logger.warning("⚠️ No logging configuration available, using defaults")
                return {
                    'threshold_changes': self._parse_bool(os.getenv('NLP_LOGGING_THRESHOLD_CHANGES', 'true')),
                    'model_disagreements': self._parse_bool(os.getenv('NLP_LOGGING_MODEL_DISAGREEMENTS', 'true')),
                    'staff_review_triggers': self._parse_bool(os.getenv('NLP_LOGGING_STAFF_REVIEW_TRIGGERS', 'true')),
                    'pattern_adjustments': self._parse_bool(os.getenv('NLP_LOGGING_PATTERN_ADJUSTMENTS', 'true')),
                    'learning_updates': self._parse_bool(os.getenv('NLP_LOGGING_LEARNING_UPDATES', 'true')),
                    'label_mappings': self._parse_bool(os.getenv('NLP_LOGGING_LABEL_MAPPINGS', 'true')),
                    'ensemble_decisions': self._parse_bool(os.getenv('NLP_LOGGING_ENSEMBLE_DECISIONS', 'true')),
                    'crisis_detection': self._parse_bool(os.getenv('NLP_LOGGING_CRISIS_DETECTION', 'true'))
                }
            
            logging_config = self._logging_config.get('logging_configuration', {})
            component_settings = logging_config.get('component_logging', {})
            
            result = {
                'threshold_changes': component_settings.get('threshold_changes', 
                                                           self._parse_bool(os.getenv('NLP_LOGGING_THRESHOLD_CHANGES', 'true'))),
                'model_disagreements': component_settings.get('model_disagreements', 
                                                             self._parse_bool(os.getenv('NLP_LOGGING_MODEL_DISAGREEMENTS', 'true'))),
                'staff_review_triggers': component_settings.get('staff_review_triggers', 
                                                               self._parse_bool(os.getenv('NLP_LOGGING_STAFF_REVIEW_TRIGGERS', 'true'))),
                'pattern_adjustments': component_settings.get('pattern_adjustments', 
                                                             self._parse_bool(os.getenv('NLP_LOGGING_PATTERN_ADJUSTMENTS', 'true'))),
                'learning_updates': component_settings.get('learning_updates', 
                                                          self._parse_bool(os.getenv('NLP_LOGGING_LEARNING_UPDATES', 'true'))),
                'label_mappings': component_settings.get('label_mappings', 
                                                        self._parse_bool(os.getenv('NLP_LOGGING_LABEL_MAPPINGS', 'true'))),
                'ensemble_decisions': component_settings.get('ensemble_decisions', 
                                                            self._parse_bool(os.getenv('NLP_LOGGING_ENSEMBLE_DECISIONS', 'true'))),
                'crisis_detection': component_settings.get('crisis_detection', 
                                                          self._parse_bool(os.getenv('NLP_LOGGING_CRISIS_DETECTION', 'true')))
            }
            
            logger.debug(f"🔍 Component logging settings: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting component logging settings: {e}")
            # Return safe defaults with environment fallbacks
            return {
                'threshold_changes': self._parse_bool(os.getenv('NLP_LOGGING_THRESHOLD_CHANGES', 'true')),
                'model_disagreements': self._parse_bool(os.getenv('NLP_LOGGING_MODEL_DISAGREEMENTS', 'true')),
                'staff_review_triggers': self._parse_bool(os.getenv('NLP_LOGGING_STAFF_REVIEW_TRIGGERS', 'true')),
                'pattern_adjustments': self._parse_bool(os.getenv('NLP_LOGGING_PATTERN_ADJUSTMENTS', 'true')),
                'learning_updates': self._parse_bool(os.getenv('NLP_LOGGING_LEARNING_UPDATES', 'true')),
                'label_mappings': self._parse_bool(os.getenv('NLP_LOGGING_LABEL_MAPPINGS', 'true')),
                'ensemble_decisions': self._parse_bool(os.getenv('NLP_LOGGING_ENSEMBLE_DECISIONS', 'true')),
                'crisis_detection': self._parse_bool(os.getenv('NLP_LOGGING_CRISIS_DETECTION', 'true'))
            }
    
    def get_development_logging_settings(self) -> Dict[str, Any]:
        """
        Get development and debugging logging settings
        
        Returns:
            Dictionary with development logging configuration
        """
        logging_config = self._logging_config.get('logging_configuration', {})
        dev_settings = logging_config.get('development_logging', {})
        
        return {
            'debug_mode': dev_settings.get('debug_mode', False),
            'trace_requests': dev_settings.get('trace_requests', False),
            'log_configuration_loading': dev_settings.get('log_configuration_loading', False),
            'log_manager_initialization': dev_settings.get('log_manager_initialization', True),
            'log_environment_variables': dev_settings.get('log_environment_variables', False)
        }
    
    def get_all_logging_settings(self) -> Dict[str, Any]:
        """
        Get complete logging configuration for system-wide access
        
        Returns:
            Dictionary with all logging settings
        """
        return {
            'global_settings': self.get_global_logging_settings(),
            'detailed_logging': self.get_detailed_logging_settings(),
            'component_logging': self.get_component_logging_settings(),
            'development_logging': self.get_development_logging_settings()
        }
    
    # ========================================================================
    # CONVENIENCE METHODS FOR COMPONENT INTEGRATION - ENHANCED ERROR HANDLING
    # ========================================================================

    def should_log_component(self, component_name: str) -> bool:
        """
        Check if logging is enabled for a specific component
        
        Args:
            component_name: Name of the component (e.g., 'threshold_changes', 'model_disagreements')
            
        Returns:
            Boolean indicating if component logging is enabled
        """
        try:
            component_settings = self.get_component_logging_settings()
            result = component_settings.get(component_name, True)  # Default to True
            logger.debug(f"🔍 Component logging check for '{component_name}': {result}")
            return result
        except Exception as e:
            logger.warning(f"⚠️ Error checking component logging for '{component_name}': {e}")
            return True  # Safe default - enable logging

    def should_log_detailed(self) -> bool:
        """
        Check if detailed logging is enabled
        
        Returns:
            Boolean indicating if detailed logging is enabled
        """
        try:
            detailed_settings = self.get_detailed_logging_settings()
            result = detailed_settings.get('enable_detailed', True)  # Default to True
            logger.debug(f"🔍 Detailed logging check: {result}")
            return result
        except Exception as e:
            logger.warning(f"⚠️ Error checking detailed logging: {e}")
            return True  # Safe default - enable detailed logging

    def should_include_reasoning(self) -> bool:
        """
        Check if reasoning should be included in logs
        
        Returns:
            Boolean indicating if reasoning should be logged
        """
        try:
            detailed_settings = self.get_detailed_logging_settings()
            result = detailed_settings.get('include_reasoning', True)  # Default to True
            logger.debug(f"🔍 Include reasoning check: {result}")
            return result
        except Exception as e:
            logger.warning(f"⚠️ Error checking include reasoning: {e}")
            return True  # Safe default - include reasoning

    def get_log_level(self) -> str:
        """
        Get the current log level (preserves GLOBAL_LOG_LEVEL)
        
        Returns:
            String log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        try:
            global_settings = self.get_global_logging_settings()
            log_level = global_settings.get('log_level', 'INFO')
            logger.debug(f"🔍 Current log level: {log_level}")
            
            # Validate log level
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if log_level not in valid_levels:
                logger.warning(f"⚠️ Invalid log level '{log_level}', using INFO")
                return 'INFO'
            
            return log_level
        except Exception as e:
            logger.warning(f"⚠️ Error getting log level: {e}")
            return 'INFO'  # Safe default

    def get_log_file_path(self) -> str:
        """
        Get the complete log file path
        
        Returns:
            String path to log file
        """
        try:
            global_settings = self.get_global_logging_settings()
            log_dir = global_settings.get('log_directory', './logs')
            log_file = global_settings.get('log_file', 'nlp_service.log')
            
            # Ensure we have valid values
            if not log_dir:
                log_dir = './logs'
            if not log_file:
                log_file = 'nlp_service.log'
            
            full_path = str(Path(log_dir) / log_file)
            logger.debug(f"🔍 Log file path: {full_path}")
            return full_path
        except Exception as e:
            logger.warning(f"⚠️ Error getting log file path: {e}")
            return './logs/nlp_service.log'  # Safe default
    
    # ========================================================================
    # CONFIGURATION STATUS AND HEALTH
    # ========================================================================
    
    def get_configuration_status(self) -> Dict[str, Any]:
        """
        Get configuration status for health checks and debugging
        
        Returns:
            Dictionary with configuration status information
        """
        return {
            'manager_type': 'LoggingConfigManager',
            'architecture': 'clean-v3.1',
            'phase': '3d-step-6',
            'config_loaded': self._logging_config is not None,
            'validation_errors': len(self._validation_errors),
            'global_log_level_preserved': True,  # Always preserved
            'python_logger_only': True,  # No custom logging mechanisms
            'configuration_source': 'JSON with ENV overrides' if self._logging_config else 'ENV fallback'
        }


# ========================================================================
# FACTORY FUNCTION - CLEAN V3.1 ARCHITECTURE REQUIREMENT
# ========================================================================

def create_logging_config_manager(config_manager: ConfigManager) -> LoggingConfigManager:
    """
    Factory function for creating LoggingConfigManager instance
    
    Args:
        config_manager: ConfigManager instance for dependency injection
        
    Returns:
        Initialized LoggingConfigManager instance
        
    Raises:
        ValueError: If config_manager is None or invalid
    """
    logger.debug("🏭 Creating LoggingConfigManager with factory function (Clean v3.1)")
    
    if not config_manager:
        raise ValueError("ConfigManager is required for LoggingConfigManager factory")
    
    return LoggingConfigManager(config_manager)


# ========================================================================
# MODULE EXPORTS - CLEAN V3.1 STANDARD
# ========================================================================

__all__ = ['LoggingConfigManager', 'create_logging_config_manager']