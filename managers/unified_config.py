# ash-nlp/managers/unified_config.py
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
Unified Configuration Manager for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-2
LAST MODIFIED: 2025-08-22
PHASE: 3e Step 5.5 - UnifiedConfigManager Optimization with Helper Files
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

OPTIMIZATION NOTES:
- Extracted schema management to helpers/unified_config_schema_helper.py (~200 lines)
- Extracted value conversion to helpers/unified_config_value_helper.py (~150 lines)
- Removed duplicate documentation and usage examples (~100 lines)
- Maintained 100% API compatibility with existing managers
- Reduced main file from ~1089 lines to ~650 lines (40% reduction)
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

# Import helper classes for reduced complexity
from managers.helpers.unified_config_schema_helper import (
    VariableSchema, 
    UnifiedConfigSchemaHelper, 
    create_schema_helper
)
from managers.helpers.unified_config_value_helper import (
    UnifiedConfigValueHelper,
    create_value_helper
)

logger = logging.getLogger(__name__)

class UnifiedConfigManager:
    """
    Unified Configuration Manager for Ash-NLP v3.1 with Helper File Optimization
    
    This manager consolidates:
    - JSON loading with ${VAR} substitution and enhanced defaults resolution
    - Schema validation and type conversion
    - Centralized environment variable access
    
    Clean v3.1 Architecture:
    - Factory function pattern  
    - Dependency injection support
    - Fail-fast validation
    - Helper file optimization for maintainability
    
    FOUNDATION LAYER: This manager provides configuration services to ALL other managers.
    No methods should be extracted to other managers to avoid circular dependencies.
    """
    
    def __init__(self, config_dir: str = "/app/config"):
        """
        Initialize Unified Configuration Manager
        
        Args:
            config_dir: Directory containing JSON configuration files
        """
        self.config_dir = Path(config_dir)
        
        # Configuration file mappings - UPDATED for v3.1 consolidation
        self.config_files = {
            # Core algorithm configuration
            'analysis_config': 'analysis_config.json',
            'crisis_threshold': 'crisis_threshold.json',
            
            # Pattern files
            'patterns_community': 'patterns_community.json',
            'patterns_context': 'patterns_context.json',
            'patterns_temporal': 'patterns_temporal.json',
            'patterns_crisis': 'patterns_crisis.json',
            'patterns_idiom': 'patterns_idiom.json',
            'patterns_burden': 'patterns_burden.json',
            
            # Core system configuration
            'feature_flags': 'feature_flags.json',
            'label_config': 'label_config.json',
            'learning_system': 'learning_system.json',
            'logging_settings': 'logging_settings.json',
            'model_coordination': 'model_coordination.json',
            'performance_settings': 'performance_settings.json',
            'server_config': 'server_config.json',
            'settings_config': 'settings_config.json',
            'storage_settings': 'storage_settings.json',
        }
        
        # Initialize helper classes for reduced complexity
        self.schema_helper = create_schema_helper(self.config_dir, self.config_files)
        self.variable_schemas = self.schema_helper.initialize_schemas()
        self.value_helper = create_value_helper(self.variable_schemas)
        
        # Load and validate all environment variables
        self.env_config = self._load_all_environment_variables()
        
        logger.info("UnifiedConfigManager v3.1e optimized initialized - Helper file architecture with enhanced performance")
    
    # ========================================================================
    # ENVIRONMENT VARIABLE VALIDATION AND LOADING
    # ========================================================================
    
    def _load_all_environment_variables(self) -> Dict[str, Any]:
        """Load and validate all environment variables using schemas"""
        env_config = {}
        validation_errors = []
        
        logger.info("Loading and validating all environment variables...")
        
        for var_name, schema in self.variable_schemas.items():
            try:
                # Get environment value or use default
                env_value = os.getenv(var_name)
                
                if env_value is None:
                    if schema.required:
                        validation_errors.append(f"Required variable {var_name} not found")
                        continue
                    else:
                        env_config[var_name] = schema.default
                        logger.debug(f"{var_name}: Using default '{schema.default}'")
                        continue
                
                # Validate and convert the environment value
                validated_value = self._validate_and_convert(var_name, env_value)
                env_config[var_name] = validated_value
                
                logger.debug(f"{var_name}: '{env_value}' -> {validated_value}")
                
            except Exception as e:
                validation_errors.append(f"Validation error for {var_name}: {e}")
                logger.error(f"{var_name}: {e}")
        
        # Fail-fast on validation errors
        if validation_errors:
            error_msg = f"Environment variable validation failed:\n" + "\n".join(validation_errors)
            logger.error(f"{error_msg}")
            raise ValueError(error_msg)
        
        logger.info(f"Successfully loaded and validated {len(env_config)} environment variables")
        return env_config
    
    def _validate_and_convert(self, var_name: str, value: str) -> Any:
        """Validate and convert environment variable using schema"""
        schema = self.variable_schemas[var_name]
        
        try:
            # Type conversion
            if schema.var_type == 'bool':
                converted = value.lower() in ('true', '1', 'yes', 'on', 'enabled')
            elif schema.var_type == 'int':
                converted = int(value)
            elif schema.var_type == 'float':
                converted = float(value)
            elif schema.var_type == 'list':
                converted = [item.strip() for item in value.split(',')]
            else:  # str
                converted = value
            
            # Validation
            if schema.choices and converted not in schema.choices:
                logger.error(f"Invalid choice for {var_name}: {converted} not in {schema.choices}")
                return schema.default
                
            if schema.min_value is not None and isinstance(converted, (int, float)):
                if converted < schema.min_value:
                    logger.error(f"Value too low for {var_name}: {converted} < {schema.min_value}")
                    return schema.default
                    
            if schema.max_value is not None and isinstance(converted, (int, float)):
                if converted > schema.max_value:
                    logger.error(f"Value too high for {var_name}: {converted} > {schema.max_value}")
                    return schema.default
            
            logger.debug(f"Validated {var_name}: {converted}")
            return converted
            
        except (ValueError, TypeError) as e:
            logger.error(f"Conversion error for {var_name}: {e}")
            return schema.default
    
    # ========================================================================
    # UNIFIED ENVIRONMENT VARIABLE ACCESS (CRITICAL METHODS)
    # ========================================================================
    
    def get_env(self, var_name: str, default: Any = None) -> Any:
        """
        Get environment variable with schema validation and type conversion
        CRITICAL METHOD - Used by all managers
        """
        # Get raw environment value
        env_value = os.getenv(var_name)
        
        # If no environment value, use schema default or provided default
        if env_value is None:
            if var_name in self.variable_schemas:
                result = self.variable_schemas[var_name].default
                logger.debug(f"Using schema default for {var_name}: {result}")
                return result
            else:
                logger.debug(f"Using provided default for {var_name}: {default}")
                return default
        
        # Validate and convert using schema
        if var_name in self.variable_schemas:
            return self._validate_and_convert(var_name, env_value)
        else:
            logger.warning(f"No schema found for {var_name}, returning raw value: {env_value}")
            return env_value
    
    def get_env_str(self, var_name: str, default: str = '') -> str:
        """Get environment variable as string"""
        result = self.get_env(var_name, default)
        return str(result) if result is not None else default
    
    def get_env_int(self, var_name: str, default: int = 0) -> int:
        """Get environment variable as integer"""
        result = self.get_env(var_name, default)
        try:
            return int(result) if result is not None else default
        except (ValueError, TypeError):
            logger.warning(f"Cannot convert {var_name}={result} to int, using default: {default}")
            return default
    
    def get_env_float(self, var_name: str, default: float = 0.0) -> float:
        """Get environment variable as float"""
        result = self.get_env(var_name, default)
        try:
            return float(result) if result is not None else default
        except (ValueError, TypeError):
            logger.warning(f"Cannot convert {var_name}={result} to float, using default: {default}")
            return default
    
    def get_env_bool(self, var_name: str, default: bool = False) -> bool:
        """Get environment variable as boolean"""
        result = self.get_env(var_name, default)
        if isinstance(result, bool):
            return result
        if isinstance(result, str):
            return result.lower() in ('true', '1', 'yes', 'on', 'enabled')
        return bool(result) if result is not None else default
    
    def get_env_list(self, var_name: str, default: List[str] = None) -> List[str]:
        """Get environment variable as list (comma-separated)"""
        if default is None:
            default = []
        result = self.get_env(var_name, ','.join(default) if default else '')
        if isinstance(result, str) and result:
            return [item.strip() for item in result.split(',')]
        return default
    
    # ========================================================================
    # JSON CONFIGURATION METHODS WITH HELPER DELEGATION
    # ========================================================================
    
    def load_config_file(self, config_name: str) -> Dict[str, Any]:
        """
        Load and parse configuration file with enhanced placeholder resolution
        
        Args:
            config_name: Name of configuration to load
            
        Returns:
            Processed configuration dictionary
        """
        config_file = self.config_files.get(config_name)
        if not config_file:
            logger.error(f"Unknown configuration: {config_name}")
            return {}
        
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            logger.warning(f"Configuration file not found: {config_path}")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            # Use helper for enhanced placeholder resolution
            processed_config = self.value_helper.substitute_environment_variables(raw_config)
            
            # Apply legacy fallback for any remaining placeholders
            processed_config = self.value_helper.apply_defaults_fallback(processed_config)
            
            logger.info(f"Loaded configuration: {config_name}")
            return processed_config
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {config_file}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading {config_file}: {e}")
            return {}
    
    # ========================================================================
    # ENHANCED CONFIGURATION SECTION ACCESS - CLEAN API
    # ========================================================================
    
    def get_config_section(self, config_file: str, section_path: str = None, default: Any = None) -> Any:
        """
        Get a specific section from a configuration file with support for nested paths
        
        Args:
            config_file: Name of the configuration file (e.g., 'analysis_config')
            section_path: Dot-separated path to the section (e.g., 'learning_system.thresholds')
            default: Default value to return if section not found
            
        Returns:
            The requested configuration section or default value
        """
        try:
            # Load the configuration file
            config_data = self.load_config_file(config_file)
            
            if not config_data:
                logger.warning(f"Configuration file '{config_file}' not found or empty")
                return default if default is not None else {}
            
            # If no section path specified, return entire config
            if section_path is None:
                return config_data
            
            # Navigate through the nested path
            result = config_data
            path_parts = section_path.split('.')
            
            for part in path_parts:
                if isinstance(result, dict) and part in result:
                    result = result[part]
                else:
                    logger.debug(f"Section path '{section_path}' not found in '{config_file}', using default")
                    return default if default is not None else {}
            
            logger.debug(f"Retrieved section '{section_path}' from '{config_file}'")
            return result
            
        except Exception as e:
            logger.error(f"Error getting config section '{section_path}' from '{config_file}': {e}")
            return default if default is not None else {}
    
    def get_config_section_with_env_fallback(self, config_file: str, section_path: str, 
                                           env_prefix: str = None, default: Any = None) -> Any:
        """
        Get configuration section with environment variable fallback support
        
        Args:
            config_file: Name of the configuration file
            section_path: Dot-separated path to the section
            env_prefix: Environment variable prefix (e.g., 'NLP_LEARNING_')
            default: Default value if neither config nor env vars found
            
        Returns:
            Configuration section with environment variable overrides applied
        """
        try:
            # First try to get from JSON config
            result = self.get_config_section(config_file, section_path, {})
            
            # If we got something from JSON and no env prefix specified, return it
            if result and env_prefix is None:
                return result
            
            # Apply environment variable overrides if prefix specified
            if env_prefix:
                result = dict(result) if result else {}  # Ensure we have a mutable dict
                
                # Look for environment variables with the specified prefix
                for env_var, env_value in os.environ.items():
                    if env_var.startswith(env_prefix):
                        # Convert env var name to config key
                        config_key = env_var[len(env_prefix):].lower()
                        
                        # Convert environment value to appropriate type
                        converted_value = self.value_helper.convert_value_type(env_var, env_value)
                        result[config_key] = converted_value
                        
                        logger.debug(f"Environment override: {env_var} -> {config_key} = {converted_value}")
            
            return result if result else (default if default is not None else {})
            
        except Exception as e:
            logger.error(f"Error getting config section with env fallback: {e}")
            return default if default is not None else {}
    
    def get_all_config_sections(self, config_file: str) -> Dict[str, Any]:
        """Get all top-level sections from a configuration file"""
        try:
            config_data = self.load_config_file(config_file)
            
            if not isinstance(config_data, dict):
                logger.warning(f"Config file '{config_file}' is not a dictionary")
                return {}
            
            return {
                section_name: section_data 
                for section_name, section_data in config_data.items()
                if not section_name.startswith('_')  # Skip metadata sections
            }
            
        except Exception as e:
            logger.error(f"Error getting all config sections from '{config_file}': {e}")
            return {}
    
    def has_config_section(self, config_file: str, section_path: str) -> bool:
        """Check if a configuration section exists without loading it"""
        try:
            result = self.get_config_section(config_file, section_path, None)
            return result is not None
        except Exception:
            return False
    
    def list_config_files(self) -> List[str]:
        """Get a list of all available configuration files"""
        return list(self.config_files.keys())
    
    def list_config_sections(self, config_file: str) -> List[str]:
        """Get a list of all top-level sections in a configuration file"""
        try:
            config_data = self.load_config_file(config_file)
            
            if isinstance(config_data, dict):
                return [
                    section_name 
                    for section_name in config_data.keys() 
                    if not section_name.startswith('_')
                ]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error listing sections in '{config_file}': {e}")
            return []
    
    # ========================================================================
    # CONFIGURATION CONVENIENCE METHODS FOR OTHER MANAGERS
    # ========================================================================
    
    def get_hardware_configuration(self) -> Dict[str, Any]:
        """Get hardware configuration for models"""
        try:
            return {
                'device': self.get_env('NLP_MODEL_DEVICE', 'auto'),
                'precision': self.get_env('NLP_MODEL_PRECISION', 'float16'),
                'max_batch_size': self.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
                'inference_threads': self.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16),
                'max_memory': self.get_env('NLP_MODEL_MAX_MEMORY', None),
                'offload_folder': self.get_env('NLP_MODEL_OFFLOAD_FOLDER', './models/offload'),
                'cache_directory': self.get_env('NLP_STORAGE_MODELS_DIR', './models/cache')
            }
        except Exception as e:
            logger.error(f"Error getting hardware configuration: {e}")
            return {
                'device': 'auto', 'precision': 'float16', 'max_batch_size': 32,
                'inference_threads': 16, 'max_memory': None,
                'offload_folder': './models/offload', 'cache_directory': './models/cache'
            }
    
    def get_model_configuration(self) -> Dict[str, Any]:
        """Get model configuration settings"""
        try:
            return {
                'depression_model': self.get_env('NLP_MODEL_DEPRESSION_NAME', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                'depression_weight': self.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
                'sentiment_model': self.get_env('NLP_MODEL_SENTIMENT_NAME', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                'sentiment_weight': self.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
                'emotional_distress_model': self.get_env('NLP_MODEL_DISTRESS_NAME', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                'emotional_distress_weight': self.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
                'ensemble_mode': self.get_env('NLP_ENSEMBLE_MODE', 'majority'),
                'gap_detection_enabled': self.get_env_bool('NLP_ENSEMBLE_GAP_DETECTION_ENABLED', True),
                'disagreement_threshold': self.get_env_int('NLP_ENSEMBLE_DISAGREEMENT_THRESHOLD', 2),
                'cache_directory': self.get_env('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'huggingface_token': self.get_env('GLOBAL_HUGGINGFACE_TOKEN', None)
            }
        except Exception as e:
            logger.error(f"Error getting model configuration: {e}")
            return {
                'depression_model': 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0', 'depression_weight': 0.4,
                'sentiment_model': 'Lowerated/lm6-deberta-v3-topic-sentiment', 'sentiment_weight': 0.3,
                'emotional_distress_model': 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli', 'emotional_distress_weight': 0.3,
                'ensemble_mode': 'consensus', 'gap_detection_enabled': True, 'disagreement_threshold': 2,
                'cache_directory': './models/cache', 'huggingface_token': None
            }
    
    def get_performance_configuration(self) -> Dict[str, Any]:
        """Get performance configuration settings"""
        try:
            return {
                'max_concurrent_requests': self.get_env_int('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 20),
                'request_timeout': self.get_env_int('GLOBAL_REQUEST_TIMEOUT', 30),
                'worker_timeout': self.get_env_int('NLP_PERFORMANCE_WORKER_TIMEOUT', 60),
                'analysis_timeout_ms': self.get_env_int('NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS', 5000),
                'analysis_cache_ttl': self.get_env_int('NLP_PERFORMANCE_ANALYSIS_CACHE_TTL', 300),
                'enable_optimization': self.get_env_bool('NLP_PERFORMANCE_ENABLE_OPTIMIZATION', True),
                'batch_size': self.get_env_int('NLP_PERFORMANCE_BATCH_SIZE', 32),
                'cache_size': self.get_env_int('NLP_PERFORMANCE_CACHE_SIZE', 1000)
            }
        except Exception as e:
            logger.error(f"Error getting performance configuration: {e}")
            return {
                'max_concurrent_requests': 20, 'request_timeout': 40, 'worker_timeout': 60,
                'analysis_timeout_ms': 5000, 'analysis_cache_ttl': 300, 'enable_optimization': True,
                'batch_size': 32, 'cache_size': 1000
            }
    
    def get_storage_configuration(self) -> Dict[str, Any]:
        """Get storage configuration settings"""
        try:
            return {
                'data_directory': self.get_env('NLP_STORAGE_DATA_DIR', './data'),
                'cache_directory': self.get_env('NLP_STORAGE_CACHE_DIR', './cache'),
                'log_directory': self.get_env('NLP_STORAGE_LOG_DIR', './logs'),
                'backup_directory': self.get_env('NLP_STORAGE_BACKUP_DIR', './backups'),
                'models_directory': self.get_env('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'enable_compression': self.get_env_bool('NLP_STORAGE_ENABLE_COMPRESSION', False),
                'retention_days': self.get_env_int('NLP_STORAGE_RETENTION_DAYS', 30),
                'log_file': self.get_env('NLP_STORAGE_LOG_FILE', 'nlp_service.log')
            }
        except Exception as e:
            logger.error(f"Error getting storage configuration: {e}")
            return {
                'data_directory': './data', 'cache_directory': './cache', 'log_directory': './logs',
                'backup_directory': './backups', 'models_directory': './models/cache',
                'enable_compression': False, 'retention_days': 30, 'log_file': 'nlp_service.log'
            }
    
    # ========================================================================
    # BACKWARD COMPATIBILITY METHODS
    # ========================================================================
    
    def get_patterns_crisis(self, pattern_type: str) -> Dict[str, Any]:
        """Get crisis pattern configuration by type - UPDATED for consolidation support"""
        logger.debug(f"Getting crisis patterns: {pattern_type}")
        
        try:
            # Load the specific pattern configuration file
            config_file_path = self.config_dir / f"{pattern_type}.json"
            
            if not config_file_path.exists():
                logger.warning(f"Crisis pattern file not found: {config_file_path}")
                return {}
            
            with open(config_file_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            # Use helper for enhanced environment variable substitutions
            processed_config = self.value_helper.substitute_environment_variables(raw_config)
            processed_config = self.value_helper.apply_defaults_fallback(processed_config)
            
            logger.debug(f"Loaded crisis patterns: {pattern_type}")
            return processed_config
            
        except Exception as e:
            logger.error(f"Failed to load crisis patterns {pattern_type}: {e}")
            return {}
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of UnifiedConfigManager with optimization info"""
        return {
            'status': 'operational',
            'version': 'v3.1e_optimized_with_helpers',
            'enhancement': 'Helper File Architecture with Enhanced Performance',
            'config_files': len(self.config_files),
            'variables_managed': len([k for k in os.environ.keys() if k.startswith('NLP_') or k.startswith('GLOBAL_')]),
            'config_directory': str(self.config_dir),
            'architecture': 'Clean v3.1 with Helper File Optimization',
            'optimization_status': {
                'helper_files_used': True,
                'schema_helper': 'managers/helpers/unified_config_schema_helper.py',
                'value_helper': 'managers/helpers/unified_config_value_helper.py',
                'main_file_reduction': '40% (1089 -> ~650 lines)',
                'extracted_functionality': ['Schema management', 'Value conversion', 'Documentation']
            },
            'schema_system': {
                'total_schemas': len(self.variable_schemas),
                'core_python_schemas': self.schema_helper.count_core_schemas(),
                'json_driven_schemas': len(self.variable_schemas) - self.schema_helper.count_core_schemas(),
                'helper_managed': True,
                'validation_source': 'JSON configuration files + essential core'
            }
        }

# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_unified_config_manager(config_dir: str = "/app/config") -> UnifiedConfigManager:
    """
    Factory function to create UnifiedConfigManager instance
    
    Args:
        config_dir: Directory containing JSON configuration files
        
    Returns:
        UnifiedConfigManager instance with helper file optimization
    """
    return UnifiedConfigManager(config_dir)

__all__ = ['UnifiedConfigManager', 'create_unified_config_manager']

logger.info("UnifiedConfigManager v3.1e optimized loaded - Helper file architecture with 40% size reduction")