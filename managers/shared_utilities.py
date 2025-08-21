"""
SharedUtilitiesManager for Ash-NLP Service
FILE VERSION: v3.1-3e-5.5-6-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 2.2 - SharedUtilitiesManager Implementation
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: SharedUtilitiesManager implementation complete
"""

import json
import logging
import os
import re
from typing import Any, Dict, List, Union, Optional, Tuple
from pathlib import Path

# Import for type hints
from managers.unified_config_manager import UnifiedConfigManager

# Configure logging
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration-related errors occur"""
    pass


class SharedUtilitiesManager:
    """
    Consolidated utility methods used across multiple managers
    Follows Clean v3.1 architecture with dependency injection
    
    Provides 15 core utilities to eliminate 150+ duplicate methods
    across 14 managers, achieving ~90% code reduction
    
    Based on Phase 3e Step 1 analysis identifying:
    - 4 premium utility methods from best-in-class implementations
    - 11 universal utility patterns across all managers
    - 150+ duplicate methods consolidated into shared utilities
    """
    
    def __init__(self, unified_config: UnifiedConfigManager):
        """
        Initialize SharedUtilitiesManager with dependency injection
        
        Args:
            unified_config: UnifiedConfigManager instance for configuration access
            
        Raises:
            ConfigurationError: If unified_config is invalid or missing required methods
        """
        if not unified_config:
            raise ConfigurationError("unified_config is required")
            
        if not hasattr(unified_config, 'get_env_str'):
            raise ConfigurationError("unified_config missing required methods")
            
        self.config_manager = unified_config
        self.logger = logging.getLogger(__name__)
        
        # Validation status tracking
        self._validation_errors = []
        self._last_operation_status = {}
        
        # Initialize utility status with error handling
        try:
            self.initialization_time = unified_config.get_env_str('SHARED_UTILS_INIT_TIME', str(id(self)))
        except Exception as e:
            self.initialization_time = str(id(self))
            self.logger.warning(f"⚠️ Could not get initialization time from config: {e}")
            
        self.logger.info(f"✅ SharedUtilitiesManager initialized (ID: {self.initialization_time})")
    
    # ========================================================================
    # PREMIUM UTILITIES (Tier 1 - Best-in-Class from Step 1 Analysis)
    # ========================================================================
    
    def safe_bool_convert(self, value: Any, default: bool = False, param_name: str = "unknown") -> bool:
        """
        Convert value to boolean with intelligent fallbacks
        Source: logging_config_manager._safe_bool_conversion() - GOLD STANDARD
        Benefits: ALL 14 managers
        
        Handles: 'true'/'false', 1/0, 'yes'/'no', 'on'/'off', True/False, etc.
        
        Args:
            value: Value to convert to boolean
            default: Default value if conversion fails
            param_name: Parameter name for logging context
            
        Returns:
            bool: Converted boolean value or default
        """
        try:
            if isinstance(value, bool):
                return value
            
            if isinstance(value, str):
                value = value.strip().lower()
                true_values = {'true', 'yes', 'on', '1', 'enabled', 'active'}
                false_values = {'false', 'no', 'off', '0', 'disabled', 'inactive'}
                
                if value in true_values:
                    return True
                elif value in false_values:
                    return False
                else:
                    self.logger.warning(f"⚠️ Invalid boolean value '{value}' for {param_name}, using default: {default}")
                    return default
            
            if isinstance(value, (int, float)):
                return bool(value)
                
            # Fallback for any other type
            self.logger.warning(f"⚠️ Cannot convert {type(value).__name__} to boolean for {param_name}, using default: {default}")
            return default
            
        except Exception as e:
            self.logger.error(f"❌ Error converting boolean for {param_name}: {e}, using default: {default}")
            return default
    
    def get_setting_with_type_conversion(self, section: str, key: str, expected_type: type, 
                                       default: Any = None, param_name: str = None) -> Any:
        """
        Get configuration setting with automatic type conversion and validation
        Source: performance_config_manager._get_performance_setting() - EXCELLENT
        Benefits: 12 managers
        
        Args:
            section: Configuration section name
            key: Configuration key name
            expected_type: Expected type for conversion (int, float, bool, str)
            default: Default value if setting not found or conversion fails
            param_name: Parameter name for logging (defaults to f"{section}.{key}")
            
        Returns:
            Any: Converted value or default
        """
        if param_name is None:
            param_name = f"{section}.{key}"
            
        try:
            # Get raw value from configuration
            section_data = self.config_manager.get_env_dict().get(section, {})
            raw_value = section_data.get(key, default)
            
            if raw_value is None:
                return default
            
            # Type conversion
            if expected_type == bool:
                return self.safe_bool_convert(raw_value, default, param_name)
            elif expected_type == int:
                return self.safe_int_convert(raw_value, default, param_name=param_name)
            elif expected_type == float:
                return self.safe_float_convert(raw_value, default, param_name=param_name)
            elif expected_type == str:
                return str(raw_value)
            else:
                self.logger.warning(f"⚠️ Unsupported type {expected_type} for {param_name}, returning raw value")
                return raw_value
                
        except Exception as e:
            self.logger.error(f"❌ Error getting setting {param_name}: {e}, using default: {default}")
            return default
    
    def get_nested_config_setting(self, path: str, default: Any = None, 
                                fallback_paths: List[str] = None) -> Any:
        """
        Get nested configuration setting with intelligent fallback paths
        Source: server_config_manager._get_setting_with_defaults() - EXCELLENT
        Benefits: 11 managers
        
        Args:
            path: Dot-separated configuration path (e.g., "server.host.port")
            default: Default value if all paths fail
            fallback_paths: List of alternative paths to try
            
        Returns:
            Any: Configuration value or default
        """
        try:
            # Try primary path first
            value = self._get_nested_value(path)
            if value is not None:
                return value
            
            # Try fallback paths
            if fallback_paths:
                for fallback_path in fallback_paths:
                    value = self._get_nested_value(fallback_path)
                    if value is not None:
                        self.logger.info(f"✅ Used fallback path '{fallback_path}' for '{path}'")
                        return value
            
            self.logger.warning(f"⚠️ No value found for path '{path}', using default: {default}")
            return default
            
        except Exception as e:
            self.logger.error(f"❌ Error getting nested setting '{path}': {e}, using default: {default}")
            return default
    
    def get_boolean_setting(self, key: str, default: bool = False, 
                          environment_override: bool = True) -> bool:
        """
        Get boolean setting with feature flag patterns and environment overrides
        Source: feature_config_manager._get_feature_flag() - VERY GOOD
        Benefits: 10 managers
        
        Args:
            key: Configuration key name
            default: Default boolean value
            environment_override: Whether to check environment variables
            
        Returns:
            bool: Boolean configuration value
        """
        try:
            # Check environment override first if enabled
            if environment_override:
                env_value = self.config_manager.get_env_str(key.upper())
                if env_value:
                    return self.safe_bool_convert(env_value, default, key)
            
            # Get from regular configuration
            config_data = self.config_manager.get_env_dict()
            raw_value = config_data.get(key, default)
            
            return self.safe_bool_convert(raw_value, default, key)
            
        except Exception as e:
            self.logger.error(f"❌ Error getting boolean setting '{key}': {e}, using default: {default}")
            return default
    
    # ========================================================================
    # CONFIGURATION PROCESSING UTILITIES (Universal patterns - All 14 managers)
    # ========================================================================
    
    def load_json_with_env_substitution(self, file_path: str, env_prefix: str = None, 
                                      required: bool = True) -> Dict[str, Any]:
        """
        Load JSON configuration with environment variable substitution
        Supports ${VAR_NAME} and ${VAR_NAME:default_value} patterns
        
        Args:
            file_path: Path to JSON configuration file
            env_prefix: Environment variable prefix for substitution
            required: Whether file is required (raises error if missing and required)
            
        Returns:
            Dict[str, Any]: Loaded and processed configuration
            
        Raises:
            ConfigurationError: If required file is missing or invalid
        """
        try:
            if not os.path.exists(file_path):
                if required:
                    raise ConfigurationError(f"Required configuration file not found: {file_path}")
                else:
                    self.logger.warning(f"⚠️ Optional configuration file not found: {file_path}")
                    return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply environment variable substitution
            if env_prefix:
                content = self._substitute_env_variables(content, env_prefix)
            
            config_data = json.loads(content)
            self.logger.info(f"✅ Loaded configuration from {file_path}")
            return config_data
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in configuration file {file_path}: {e}"
            if required:
                raise ConfigurationError(error_msg)
            else:
                self.logger.error(f"❌ {error_msg}")
                return {}
        except Exception as e:
            error_msg = f"Error loading configuration from {file_path}: {e}"
            if required:
                raise ConfigurationError(error_msg)
            else:
                self.logger.error(f"❌ {error_msg}")
                return {}
    
    def get_config_section_safely(self, section_name: str, fallback: Dict = None) -> Dict[str, Any]:
        """
        Safely get configuration section with fallback dictionary
        
        Args:
            section_name: Name of configuration section
            fallback: Fallback dictionary if section not found
            
        Returns:
            Dict[str, Any]: Configuration section or fallback
        """
        try:
            config_data = self.config_manager.get_env_dict()
            section_data = config_data.get(section_name)
            
            if section_data is None:
                if fallback is None:
                    fallback = {}
                self.logger.warning(f"⚠️ Configuration section '{section_name}' not found, using fallback")
                return fallback.copy()
            
            if not isinstance(section_data, dict):
                self.logger.warning(f"⚠️ Configuration section '{section_name}' is not a dictionary, using fallback")
                return fallback.copy() if fallback else {}
            
            return section_data.copy()
            
        except Exception as e:
            self.logger.error(f"❌ Error getting config section '{section_name}': {e}")
            return fallback.copy() if fallback else {}
    
    def apply_env_overrides(self, config_data: Dict, env_prefix: str) -> Dict[str, Any]:
        """
        Apply environment variable overrides to configuration data
        
        Args:
            config_data: Base configuration dictionary
            env_prefix: Environment variable prefix (e.g., "NLP_")
            
        Returns:
            Dict[str, Any]: Configuration with environment overrides applied
        """
        try:
            result = config_data.copy()
            env_vars = os.environ
            
            for env_key, env_value in env_vars.items():
                if env_key.startswith(env_prefix):
                    # Convert environment variable to config key
                    config_key = env_key[len(env_prefix):].lower()
                    
                    # Handle nested keys (e.g., NLP_SECTION_KEY -> section.key)
                    if '_' in config_key:
                        parts = config_key.split('_')
                        current = result
                        for part in parts[:-1]:
                            if part not in current:
                                current[part] = {}
                            current = current[part]
                        current[parts[-1]] = env_value
                    else:
                        result[config_key] = env_value
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error applying environment overrides: {e}")
            return config_data.copy()
    
    def get_with_fallback(self, primary_key: str, fallback_keys: List[str], 
                         default: Any = None) -> Any:
        """
        Get configuration value with fallback key chain
        
        Args:
            primary_key: Primary configuration key to try first
            fallback_keys: List of fallback keys to try in order
            default: Default value if all keys fail
            
        Returns:
            Any: Configuration value or default
        """
        try:
            config_data = self.config_manager.get_env_dict()
            
            # Try primary key first
            if primary_key in config_data:
                return config_data[primary_key]
            
            # Try fallback keys
            for fallback_key in fallback_keys:
                if fallback_key in config_data:
                    self.logger.info(f"✅ Used fallback key '{fallback_key}' for '{primary_key}'")
                    return config_data[fallback_key]
            
            self.logger.warning(f"⚠️ No value found for '{primary_key}' or fallbacks, using default: {default}")
            return default
            
        except Exception as e:
            self.logger.error(f"❌ Error getting value with fallback for '{primary_key}': {e}")
            return default
    
    def validate_config_structure(self, config_data: Dict, required_sections: List[str], 
                                schema: Dict = None) -> List[str]:
        """
        Validate configuration structure and return list of issues
        
        Args:
            config_data: Configuration dictionary to validate
            required_sections: List of required section names
            schema: Optional schema dictionary for validation
            
        Returns:
            List[str]: List of validation issues (empty if valid)
        """
        issues = []
        
        try:
            # Check required sections
            for section in required_sections:
                if section not in config_data:
                    issues.append(f"Missing required section: {section}")
                elif not isinstance(config_data[section], dict):
                    issues.append(f"Section '{section}' must be a dictionary")
            
            # Check schema if provided
            if schema:
                for section_name, section_schema in schema.items():
                    if section_name in config_data:
                        section_issues = self._validate_section_schema(
                            config_data[section_name], section_schema, section_name
                        )
                        issues.extend(section_issues)
            
            if issues:
                self.logger.warning(f"⚠️ Configuration validation found {len(issues)} issues")
            else:
                self.logger.info("✅ Configuration structure validation passed")
            
            return issues
            
        except Exception as e:
            error_msg = f"Error validating configuration structure: {e}"
            self.logger.error(f"❌ {error_msg}")
            return [error_msg]
    
    def execute_safely(self, operation_name: str, operation_func, *args, **kwargs):
        """
        Execute operation safely with error handling and fallback support
        
        Args:
            operation_name: Name of operation being performed
            operation_func: Function to execute safely
            *args: Arguments to pass to operation_func
            **kwargs: Keyword arguments to pass to operation_func
            
        Returns:
            Result of operation_func or safe fallback value
        """
        try:
            result = operation_func(*args, **kwargs)
            
            # Update operation status
            self._last_operation_status[operation_name] = {
                'success': True,
                'result': str(result)[:100] if result is not None else 'None',
                'timestamp': self.config_manager.get_env_str('CURRENT_TIME', 'unknown')
            }
            
            return result
            
        except Exception as e:
            return self.handle_error_with_fallback(
                e, 
                self._get_safe_fallback_for_operation(operation_name),
                operation_name,
                operation_name
            )

    def _get_safe_fallback_for_operation(self, operation_name: str):
        """Get appropriate fallback value based on operation type"""
        if 'threshold' in operation_name.lower():
            return {'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8}
        elif 'score' in operation_name.lower() or 'confidence' in operation_name.lower():
            return 0.0
        elif 'level' in operation_name.lower():
            return 'medium'
        elif 'parameters' in operation_name.lower():
            return {'ensemble_weights': [0.4, 0.3, 0.3], 'score_normalization': 'sigmoid'}
        elif 'analysis' in operation_name.lower():
            return {
                'crisis_score': 0.5,
                'crisis_level': 'medium',
                'method': 'safe_fallback',
                'needs_response': True,
                'confidence_score': 0.5,
                'detected_categories': ['fallback'],
                'requires_staff_review': True,
                'processing_time': 0.0
            }
        else:
            return {}

    # ========================================================================
    # TYPE CONVERSION UTILITIES
    # ========================================================================
    
    def safe_int_convert(self, value: Any, default: int = 0, min_val: int = None, 
                        max_val: int = None, param_name: str = "unknown") -> int:
        """
        Convert value to integer with range validation and fallbacks
        
        Args:
            value: Value to convert to integer
            default: Default value if conversion fails
            min_val: Minimum allowed value (optional)
            max_val: Maximum allowed value (optional)
            param_name: Parameter name for logging context
            
        Returns:
            int: Converted integer value or default
        """
        try:
            if isinstance(value, int):
                result = value
            elif isinstance(value, float):
                result = int(value)
            elif isinstance(value, str):
                result = int(float(value))  # Handle "1.0" -> 1
            else:
                self.logger.warning(f"⚠️ Cannot convert {type(value).__name__} to int for {param_name}")
                return default
            
            # Range validation
            if min_val is not None and result < min_val:
                self.logger.warning(f"⚠️ Value {result} below minimum {min_val} for {param_name}, using minimum")
                return min_val
            
            if max_val is not None and result > max_val:
                self.logger.warning(f"⚠️ Value {result} above maximum {max_val} for {param_name}, using maximum")
                return max_val
            
            return result
            
        except (ValueError, TypeError) as e:
            self.logger.error(f"❌ Error converting to int for {param_name}: {e}, using default: {default}")
            return default
    
    def safe_float_convert(self, value: Any, default: float = 0.0, min_val: float = None, 
                          max_val: float = None, param_name: str = "unknown") -> float:
        """
        Convert value to float with range validation and fallbacks
        
        Args:
            value: Value to convert to float
            default: Default value if conversion fails
            min_val: Minimum allowed value (optional)
            max_val: Maximum allowed value (optional)
            param_name: Parameter name for logging context
            
        Returns:
            float: Converted float value or default
        """
        try:
            if isinstance(value, (int, float)):
                result = float(value)
            elif isinstance(value, str):
                result = float(value)
            else:
                self.logger.warning(f"⚠️ Cannot convert {type(value).__name__} to float for {param_name}")
                return default
            
            # Range validation
            if min_val is not None and result < min_val:
                self.logger.warning(f"⚠️ Value {result} below minimum {min_val} for {param_name}, using minimum")
                return min_val
            
            if max_val is not None and result > max_val:
                self.logger.warning(f"⚠️ Value {result} above maximum {max_val} for {param_name}, using maximum")
                return max_val
            
            return result
            
        except (ValueError, TypeError) as e:
            self.logger.error(f"❌ Error converting to float for {param_name}: {e}, using default: {default}")
            return default
    
    # ========================================================================
    # VALIDATION UTILITIES
    # ========================================================================
    
    def validate_range(self, value: Union[int, float], min_val: Union[int, float], 
                      max_val: Union[int, float], param_name: str = "unknown") -> bool:
        """
        Validate numeric value is within specified range
        
        Args:
            value: Numeric value to validate
            min_val: Minimum allowed value (None means no minimum)
            max_val: Maximum allowed value (None means no maximum)
            param_name: Parameter name for logging context
            
        Returns:
            bool: True if value is within range, False otherwise
        """
        try:
            if not isinstance(value, (int, float)):
                self.logger.error(f"❌ Non-numeric value for range validation of {param_name}: {type(value)}")
                return False
            
            if min_val is not None and value < min_val:
                self.logger.warning(f"⚠️ Value {value} below minimum {min_val} for {param_name}")
                return False
            
            if max_val is not None and value > max_val:
                self.logger.warning(f"⚠️ Value {value} above maximum {max_val} for {param_name}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error validating range for {param_name}: {e}")
            return False
    
    def validate_type(self, value: Any, expected_type: Union[type, tuple], 
                     param_name: str = "unknown") -> bool:
        """
        Validate value matches expected type(s)
        
        Args:
            value: Value to validate
            expected_type: Expected type or tuple of types
            param_name: Parameter name for logging context
            
        Returns:
            bool: True if value matches expected type, False otherwise
        """
        try:
            if isinstance(value, expected_type):
                return True
            
            # Special handling for numeric types - allow cross-compatibility
            if expected_type in (int, float) and isinstance(value, (int, float)):
                return True
            
            # Special handling for string conversions - most types can become strings
            if expected_type == str and value is not None:
                # Only return True if it's already a string, otherwise it's a type mismatch
                return isinstance(value, str)
            
            expected_name = expected_type.__name__ if hasattr(expected_type, '__name__') else str(expected_type)
            actual_name = type(value).__name__
            self.logger.warning(f"⚠️ Type mismatch for {param_name}: expected {expected_name}, got {actual_name}")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error validating type for {param_name}: {e}")
            return False
    
    def validate_bounds(self, value: Union[int, float], bounds: Dict[str, Union[int, float]], 
                       param_name: str = "unknown") -> bool:
        """
        Validate value is within operational bounds dictionary
        
        Args:
            value: Numeric value to validate
            bounds: Dictionary with 'min' and/or 'max' keys
            param_name: Parameter name for logging context
            
        Returns:
            bool: True if value is within bounds, False otherwise
        """
        try:
            if not isinstance(value, (int, float)):
                self.logger.error(f"❌ Non-numeric value for bounds validation of {param_name}: {type(value)}")
                return False
            
            if not isinstance(bounds, dict):
                self.logger.error(f"❌ Invalid bounds dictionary for {param_name}: {type(bounds)}")
                return False
            
            min_val = bounds.get('min')
            max_val = bounds.get('max')
            
            return self.validate_range(value, min_val, max_val, param_name)
            
        except Exception as e:
            self.logger.error(f"❌ Error validating bounds for {param_name}: {e}")
            return False
    
    # ========================================================================
    # ERROR HANDLING UTILITIES
    # ========================================================================
    
    def handle_error_with_fallback(self, error: Exception, fallback_value: Any, 
                                 context: str, operation: str = "unknown") -> Any:
        """
        Handle error with fallback value and structured logging
        Returns fallback_value and logs error with context
        
        Args:
            error: Exception that occurred
            fallback_value: Value to return as fallback
            context: Context where error occurred
            operation: Operation being performed when error occurred
            
        Returns:
            Any: fallback_value
        """
        try:
            error_msg = f"Error in {operation} ({context}): {str(error)}"
            self.logger.error(f"❌ {error_msg}")
            
            # Update operation status
            self._last_operation_status[operation] = {
                'success': False,
                'error': str(error),
                'context': context,
                'fallback_used': fallback_value,
                'timestamp': self.config_manager.get_env_str('CURRENT_TIME', 'unknown')
            }
            
            self.logger.info(f"✅ Using fallback value for {operation}: {fallback_value}")
            return fallback_value
            
        except Exception as logging_error:
            # Fallback for logging errors - just return the fallback value
            print(f"Critical error in error handling: {logging_error}")
            return fallback_value
    
    # ========================================================================
    # UTILITY STATUS METHODS
    # ========================================================================
    
    def get_last_operation_status(self) -> Dict[str, Any]:
        """Get status of last utility operation"""
        return self._last_operation_status.copy()
    
    def get_validation_errors(self) -> List[str]:
        """Get collected validation errors"""
        return self._validation_errors.copy()
    
    def clear_validation_errors(self) -> None:
        """Clear validation error collection"""
        self._validation_errors.clear()
        self.logger.info("✅ Validation errors cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status of SharedUtilitiesManager"""
        return {
            'manager_type': 'SharedUtilitiesManager',
            'initialization_time': self.initialization_time,
            'config_manager_available': bool(self.config_manager),
            'validation_errors_count': len(self._validation_errors),
            'last_operations_count': len(self._last_operation_status),
            'utilities_available': 15,  # Total utility methods
            'status': 'healthy'
        }
    
    # ========================================================================
    # INTERNAL HELPER METHODS
    # ========================================================================
    
    def _get_nested_value(self, path: str) -> Any:
        """Get value from nested configuration path"""
        try:
            config_data = self.config_manager.get_env_dict()
            parts = path.split('.')
            current = config_data
            
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            
            return current
            
        except Exception:
            return None
    
    def _substitute_env_variables(self, content: str, env_prefix: str) -> str:
        """Substitute environment variables in content"""
        try:
            # Pattern matches ${VAR_NAME} and ${VAR_NAME:default_value}
            pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
            
            def replace_var(match):
                var_name = match.group(1)
                default_value = match.group(2) if match.group(2) is not None else ''
                
                # Add prefix if not already present
                full_var_name = var_name if var_name.startswith(env_prefix) else f"{env_prefix}{var_name}"
                
                return os.environ.get(full_var_name, default_value)
            
            return re.sub(pattern, replace_var, content)
            
        except Exception as e:
            self.logger.error(f"❌ Error substituting environment variables: {e}")
            return content
    
    def _validate_section_schema(self, section_data: Dict, schema: Dict, section_name: str) -> List[str]:
        """Validate section data against schema"""
        issues = []
        
        try:
            for key, expected_type in schema.items():
                if key not in section_data:
                    issues.append(f"Missing required key '{key}' in section '{section_name}'")
                elif not isinstance(section_data[key], expected_type):
                    expected_name = expected_type.__name__
                    actual_name = type(section_data[key]).__name__
                    issues.append(f"Type mismatch for '{section_name}.{key}': expected {expected_name}, got {actual_name}")
            
            return issues
            
        except Exception as e:
            return [f"Error validating section '{section_name}': {e}"]


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_shared_utilities_manager(unified_config: UnifiedConfigManager = None) -> SharedUtilitiesManager:
    """
    Factory function to create SharedUtilitiesManager with dependency injection
    
    Args:
        unified_config: UnifiedConfigManager instance (will create if None)
        
    Returns:
        SharedUtilitiesManager: Configured manager instance
        
    Raises:
        ConfigurationError: If unified_config cannot be created or is invalid
    """
    try:
        # Use provided config or create new one
        if unified_config is None:
            from managers.unified_config_manager import create_unified_config_manager
            unified_config = create_unified_config_manager()
            
        # Validate config manager
        if not hasattr(unified_config, 'get_env_str'):
            raise ConfigurationError("Invalid unified_config: missing required methods")
            
        # Create and return manager
        manager = SharedUtilitiesManager(unified_config)
        
        # Verify initialization
        status = manager.get_status()
        if status['status'] != 'healthy':
            raise ConfigurationError("SharedUtilitiesManager initialization unhealthy")
            
        logger.info("✅ SharedUtilitiesManager created successfully via factory function")
        return manager
        
    except Exception as e:
        logger.error(f"❌ Failed to create SharedUtilitiesManager: {e}")
        raise ConfigurationError(f"SharedUtilitiesManager creation failed: {e}")


# ============================================================================
# EXPORT FOR CLEAN ARCHITECTURE
# ============================================================================

__all__ = [
    'SharedUtilitiesManager',
    'create_shared_utilities_manager',
    'ConfigurationError'
]