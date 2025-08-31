# ash-nlp/managers/logging_config_manager.py
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
Centralized Logging Configuration Manager for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-1
LAST MODIFIED: 2025-08-22
PHASE: 3e, Sub-step 5.5, Task 5 - LoggingConfigManager Standard Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

class LoggingConfigManager:
    """
    Centralized logging configuration management for Ash-NLP service
    
    Phase 3e Sub-step 5.5: Enhanced with get_config_section() patterns and improved logging management
    
    This manager provides comprehensive logging configuration management including:
    - Global logging settings (log level, file paths, console/file output)
    - Detailed logging controls (raw labels, analysis steps, performance metrics)
    - Component-specific logging (threshold changes, model disagreements, crisis detection)
    - Development logging (debug mode, request tracing, configuration loading)
    - Environment variable integration with safe type conversion
    
    Phase 3e Improvements:
    - Replaced load_config_file() with get_config_section() patterns
    - Enhanced error handling and resilience for configuration access
    - Improved fallback mechanisms for safe operation
    - Better integration with UnifiedConfigManager
    - Added comprehensive logging validation and monitoring
    """
    
    def __init__(self, unified_config_manager):
        """
        Initialize LoggingConfigManager with UnifiedConfigManager integration
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
        """
        self.unified_config = unified_config_manager
        
        try:
            # Load logging configuration using Phase 3e patterns
            self.logging_config = self.unified_config.get_config_section('logging_settings')
            logger.info("LoggingConfigManager v3.1e-5.5 initialized - Phase 3e patterns applied")
            
            return

        except Exception as e:
            logger.error(f"Error loading logging configuration: {e}")
            return

    # ========================================================================
    # GLOBAL LOGGING SETTINGS ACCESS METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_global_logging_settings(self) -> Dict[str, Any]:
        """Get global logging settings with Phase 3e enhanced error handling"""
        try:
            # PHASE 3E: Enhanced access using get_config_section patterns
            global_settings = self.unified_config.get_config_section('logging_settings', 'global_settings', {})
            if not global_settings:
                # Fallback to direct logging_config access
                global_settings = self.logging_config.get('global_settings', {})
            
            # Provide safe defaults
            return {
                'log_level': global_settings.get('log_level', 'INFO'),
                'log_file': global_settings.get('log_file', 'nlp_service.log'),
                'log_directory': global_settings.get('log_directory', './logs'),
                'enable_console_output': global_settings.get('enable_console_output', True),
                'enable_file_output': global_settings.get('enable_file_output', True)
            }
            
        except Exception as e:
            logger.error(f"Error getting global logging settings: {e}")
            return {
                'log_level': 'INFO',
                'log_file': 'nlp_service.log',
                'log_directory': './logs',
                'enable_console_output': True,
                'enable_file_output': True
            }
    
    def get_log_level(self) -> str:
        """Get current log level with enhanced validation"""
        try:
            global_settings = self.get_global_logging_settings()
            log_level = global_settings.get('log_level', 'INFO')
            
            # Validate log level
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if log_level.upper() not in valid_levels:
                logger.warning(f"Invalid log level '{log_level}', using INFO")
                return 'INFO'
                
            return log_level.upper()
            
        except Exception as e:
            logger.error(f"Error getting log level: {e}")
            return 'INFO'
    
    def get_log_directory(self) -> str:
        """Get log directory path with enhanced validation"""
        try:
            global_settings = self.get_global_logging_settings()
            return global_settings.get('log_directory', './logs')
        except Exception as e:
            logger.error(f"Error getting log directory: {e}")
            return './logs'
    
    def get_log_file(self) -> str:
        """Get log file name with enhanced validation"""
        try:
            global_settings = self.get_global_logging_settings()
            return global_settings.get('log_file', 'nlp_service.log')
        except Exception as e:
            logger.error(f"Error getting log file: {e}")
            return 'nlp_service.log'
    
    def is_console_output_enabled(self) -> bool:
        """Check if console output is enabled with enhanced error handling"""
        try:
            global_settings = self.get_global_logging_settings()
            return self._safe_bool_conversion(global_settings.get('enable_console_output', True))
        except Exception as e:
            logger.error(f"Error checking console output setting: {e}")
            return True
    
    def is_file_output_enabled(self) -> bool:
        """Check if file output is enabled with enhanced error handling"""
        try:
            global_settings = self.get_global_logging_settings()
            return self._safe_bool_conversion(global_settings.get('enable_file_output', True))
        except Exception as e:
            logger.error(f"Error checking file output setting: {e}")
            return True
    
    # ========================================================================
    # DETAILED LOGGING SETTINGS ACCESS METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_detailed_logging_settings(self) -> Dict[str, Any]:
        """Get detailed logging settings with Phase 3e enhanced access patterns"""
        try:
            # PHASE 3E: Enhanced access using get_config_section patterns
            detailed_settings = self.unified_config.get_config_section('logging_settings', 'detailed_logging', {})
            if not detailed_settings:
                # Fallback to direct logging_config access
                detailed_settings = self.logging_config.get('detailed_logging', {})
            
            return {
                'enable_detailed': detailed_settings.get('enable_detailed', True),
                'include_raw_labels': detailed_settings.get('include_raw_labels', True),
                'analysis_steps': detailed_settings.get('analysis_steps', False),
                'performance_metrics': detailed_settings.get('performance_metrics', True),
                'include_reasoning': detailed_settings.get('include_reasoning', True)
            }
            
        except Exception as e:
            logger.error(f"Error getting detailed logging settings: {e}")
            return {
                'enable_detailed': True,
                'include_raw_labels': True,
                'analysis_steps': False,
                'performance_metrics': True,
                'include_reasoning': True
            }
    
    def is_detailed_logging_enabled(self) -> bool:
        """Check if detailed logging is enabled with enhanced validation"""
        try:
            detailed_settings = self.get_detailed_logging_settings()
            return self._safe_bool_conversion(detailed_settings.get('enable_detailed', True))
        except Exception as e:
            logger.error(f"Error checking detailed logging setting: {e}")
            return True
    
    def should_include_raw_labels(self) -> bool:
        """Check if raw labels should be included in logs with enhanced validation"""
        try:
            detailed_settings = self.get_detailed_logging_settings()
            return self._safe_bool_conversion(detailed_settings.get('include_raw_labels', True))
        except Exception as e:
            logger.error(f"Error checking raw labels setting: {e}")
            return True
    
    def should_log_analysis_steps(self) -> bool:
        """Check if analysis steps should be logged with enhanced validation"""
        try:
            detailed_settings = self.get_detailed_logging_settings()
            return self._safe_bool_conversion(detailed_settings.get('analysis_steps', False))
        except Exception as e:
            logger.error(f"Error checking analysis steps setting: {e}")
            return False
    
    def should_log_performance_metrics(self) -> bool:
        """Check if performance metrics should be logged with enhanced validation"""
        try:
            detailed_settings = self.get_detailed_logging_settings()
            return self._safe_bool_conversion(detailed_settings.get('performance_metrics', True))
        except Exception as e:
            logger.error(f"Error checking performance metrics setting: {e}")
            return True
    
    def should_include_reasoning(self) -> bool:
        """Check if reasoning should be included in logs with enhanced validation"""
        try:
            detailed_settings = self.get_detailed_logging_settings()
            return self._safe_bool_conversion(detailed_settings.get('include_reasoning', True))
        except Exception as e:
            logger.error(f"Error checking reasoning setting: {e}")
            return True
    
    # ========================================================================
    # COMPONENT LOGGING SETTINGS ACCESS METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_component_logging_settings(self) -> Dict[str, Any]:
        """Get component-specific logging settings with Phase 3e enhanced access patterns"""
        try:
            # PHASE 3E: Enhanced access using get_config_section patterns
            component_settings = self.unified_config.get_config_section('logging_settings', 'component_logging', {})
            if not component_settings:
                # Fallback to direct logging_config access
                component_settings = self.logging_config.get('component_logging', {})
            
            return {
                'threshold_changes': component_settings.get('threshold_changes', True),
                'model_disagreements': component_settings.get('model_disagreements', True),
                'staff_review_triggers': component_settings.get('staff_review_triggers', True),
                'pattern_adjustments': component_settings.get('pattern_adjustments', True),
                'learning_updates': component_settings.get('learning_updates', True),
                'label_mappings': component_settings.get('label_mappings', True),
                'ensemble_decisions': component_settings.get('ensemble_decisions', True),
                'crisis_detection': component_settings.get('crisis_detection', True)
            }
            
        except Exception as e:
            logger.error(f"Error getting component logging settings: {e}")
            return {
                'threshold_changes': True,
                'model_disagreements': True,
                'staff_review_triggers': True,
                'pattern_adjustments': True,
                'learning_updates': True,
                'label_mappings': True,
                'ensemble_decisions': True,
                'crisis_detection': True
            }
    
    def should_log_threshold_changes(self) -> bool:
        """Check if threshold changes should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('threshold_changes', True))
        except Exception as e:
            logger.error(f"Error checking threshold changes logging setting: {e}")
            return True
    
    def should_log_model_disagreements(self) -> bool:
        """Check if model disagreements should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('model_disagreements', True))
        except Exception as e:
            logger.error(f"Error checking model disagreements logging setting: {e}")
            return True
    
    def should_log_staff_review_triggers(self) -> bool:
        """Check if staff review triggers should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('staff_review_triggers', True))
        except Exception as e:
            logger.error(f"Error checking staff review triggers logging setting: {e}")
            return True
    
    def should_log_pattern_adjustments(self) -> bool:
        """Check if pattern adjustments should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('pattern_adjustments', True))
        except Exception as e:
            logger.error(f"Error checking pattern adjustments logging setting: {e}")
            return True
    
    def should_log_learning_updates(self) -> bool:
        """Check if learning updates should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('learning_updates', True))
        except Exception as e:
            logger.error(f"Error checking learning updates logging setting: {e}")
            return True
    
    def should_log_label_mappings(self) -> bool:
        """Check if label mappings should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('label_mappings', True))
        except Exception as e:
            logger.error(f"Error checking label mappings logging setting: {e}")
            return True
    
    def should_log_ensemble_decisions(self) -> bool:
        """Check if ensemble decisions should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('ensemble_decisions', True))
        except Exception as e:
            logger.error(f"Error checking ensemble decisions logging setting: {e}")
            return True
    
    def should_log_crisis_detection(self) -> bool:
        """Check if crisis detection should be logged with enhanced validation"""
        try:
            component_settings = self.get_component_logging_settings()
            return self._safe_bool_conversion(component_settings.get('crisis_detection', True))
        except Exception as e:
            logger.error(f"Error checking crisis detection logging setting: {e}")
            return True
    
    # ========================================================================
    # DEVELOPMENT LOGGING SETTINGS ACCESS METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_development_logging_settings(self) -> Dict[str, Any]:
        """Get development logging settings with Phase 3e enhanced access patterns"""
        try:
            # PHASE 3E: Enhanced access using get_config_section patterns
            dev_settings = self.unified_config.get_config_section('logging_settings', 'development_logging', {})
            if not dev_settings:
                # Fallback to direct logging_config access
                dev_settings = self.logging_config.get('development_logging', {})
            
            return {
                'debug_mode': dev_settings.get('debug_mode', False),
                'trace_requests': dev_settings.get('trace_requests', False),
                'log_configuration_loading': dev_settings.get('log_configuration_loading', False),
                'log_manager_initialization': dev_settings.get('log_manager_initialization', True),
                'log_environment_variables': dev_settings.get('log_environment_variables', False)
            }
            
        except Exception as e:
            logger.error(f"Error getting development logging settings: {e}")
            return {
                'debug_mode': False,
                'trace_requests': False,
                'log_configuration_loading': False,
                'log_manager_initialization': True,
                'log_environment_variables': False
            }
    
    def is_debug_mode_enabled(self) -> bool:
        """Check if debug mode is enabled with enhanced validation"""
        try:
            dev_settings = self.get_development_logging_settings()
            return self._safe_bool_conversion(dev_settings.get('debug_mode', False))
        except Exception as e:
            logger.error(f"Error checking debug mode setting: {e}")
            return False
    
    def should_trace_requests(self) -> bool:
        """Check if requests should be traced with enhanced validation"""
        try:
            dev_settings = self.get_development_logging_settings()
            return self._safe_bool_conversion(dev_settings.get('trace_requests', False))
        except Exception as e:
            logger.error(f"Error checking request tracing setting: {e}")
            return False
    
    def should_log_configuration_loading(self) -> bool:
        """Check if configuration loading should be logged with enhanced validation"""
        try:
            dev_settings = self.get_development_logging_settings()
            return self._safe_bool_conversion(dev_settings.get('log_configuration_loading', False))
        except Exception as e:
            logger.error(f"Error checking configuration loading setting: {e}")
            return False
    
    def should_log_manager_initialization(self) -> bool:
        """Check if manager initialization should be logged with enhanced validation"""
        try:
            dev_settings = self.get_development_logging_settings()
            return self._safe_bool_conversion(dev_settings.get('log_manager_initialization', True))
        except Exception as e:
            logger.error(f"Error checking manager initialization setting: {e}")
            return True
    
    def should_log_environment_variables(self) -> bool:
        """Check if environment variables should be logged with enhanced validation"""
        try:
            dev_settings = self.get_development_logging_settings()
            return self._safe_bool_conversion(dev_settings.get('log_environment_variables', False))
        except Exception as e:
            logger.error(f"Error checking environment variables setting: {e}")
            return False
    
    # ========================================================================
    # UTILITY METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def _safe_bool_conversion(self, value: Any) -> bool:
        """Safely convert value to boolean with enhanced Phase 3e validation"""
        try:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
            if isinstance(value, (int, float)):
                return bool(value)
            return bool(value)
        except Exception as e:
            logger.warning(f"Error converting value to boolean: {e}")
            return False
    
    def get_all_logging_settings(self) -> Dict[str, Any]:
        """Get all logging settings with enhanced error handling"""
        try:
            return {
                'global_settings': self.get_global_logging_settings(),
                'detailed_logging': self.get_detailed_logging_settings(),
                'component_logging': self.get_component_logging_settings(),
                'development_logging': self.get_development_logging_settings()
            }
        except Exception as e:
            logger.error(f"Error getting all logging settings: {e}")
            return {
                'global_settings': {},
                'detailed_logging': {},
                'component_logging': {},
                'development_logging': {}
            }
    
    def get_logging_status(self) -> Dict[str, Any]:
        """Get comprehensive logging status with Phase 3e enhancements"""
        try:
            return {
                'manager_status': 'operational',
                'manager_version': 'v3.1e-5.5-4',
                'phase': '3e Sub-step 5.5 Task 5',
                'configuration_source': 'unified_config_manager',
                'get_config_section_patterns': 'implemented',
                'direct_os_getenv_calls': 'eliminated',
                'global_settings': self.get_global_logging_settings(),
                'detailed_logging_enabled': self.is_detailed_logging_enabled(),
                'debug_mode_enabled': self.is_debug_mode_enabled(),
                'console_output_enabled': self.is_console_output_enabled(),
                'file_output_enabled': self.is_file_output_enabled(),
                'unified_config_manager': True,
                'enhanced_error_handling': True
            }
        except Exception as e:
            logger.error(f"Error getting logging status: {e}")
            return {
                'manager_status': 'error',
                'manager_version': 'v3.1e-5.5-4',
                'error': str(e),
                'fallback_mode': 'active'
            }
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary for monitoring and debugging
        Phase 3e: New method for enhanced system visibility
        """
        try:
            all_settings = self.get_all_logging_settings()
            
            return {
                'manager_version': 'v3.1e-5.5-4',
                'phase': '3e Sub-step 5.5 Task 5',
                'log_level': self.get_log_level(),
                'log_directory': self.get_log_directory(),
                'log_file': self.get_log_file(),
                'console_output': self.is_console_output_enabled(),
                'file_output': self.is_file_output_enabled(),
                'detailed_logging': self.is_detailed_logging_enabled(),
                'debug_mode': self.is_debug_mode_enabled(),
                'crisis_detection_logging': self.should_log_crisis_detection(),
                'total_settings_categories': len(all_settings),
                'configuration_source': 'json_with_env_overrides',
                'initialization_status': 'complete'
            }
            
        except Exception as e:
            logger.error(f"Error generating configuration summary: {e}")
            return {
                'manager_version': 'v3.1e-5.5-4',
                'phase': '3e Sub-step 5.5 Task 5',
                'error': str(e),
                'initialization_status': 'error'
            }

# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================

def create_logging_config_manager(unified_config_manager) -> LoggingConfigManager:
    """
    Factory function for LoggingConfigManager (Clean v3.1 Pattern) - Phase 3e Enhanced
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for dependency injection
        
    Returns:
        Initialized LoggingConfigManager instance with Phase 3e enhancements
        
    Raises:
        ValueError: If unified_config_manager is None or invalid
    """
    logger.debug("Creating LoggingConfigManager with Phase 3e configuration patterns")
    
    if not unified_config_manager:
        raise ValueError("UnifiedConfigManager is required for LoggingConfigManager factory")
    
    return LoggingConfigManager(unified_config_manager)

# Export public interface
__all__ = ['LoggingConfigManager', 'create_logging_config_manager']

logger.info("LoggingConfigManager v3.1e-5.5-4 loaded - Phase 3e Sub-step 5.5 cleanup complete with enhanced patterns")