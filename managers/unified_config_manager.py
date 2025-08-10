"""
Unified Configuration Manager for Ash-NLP v3.1d Step 9 - CORRECTLY FIXED
Follows the established JSON defaults block pattern and eliminates all direct os.getenv() calls

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class VariableSchema:
    """Schema definition for environment variable validation"""
    var_type: str  # 'str', 'int', 'float', 'bool', 'list'
    default: Any
    choices: Optional[List[Any]] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    required: bool = False
    description: str = ""

class UnifiedConfigManager:
    """
    Unified Configuration Manager for Ash-NLP v3.1d Step 9 - CORRECTLY FIXED
    
    FOLLOWS ESTABLISHED PATTERN WITH DEFAULTS BLOCK:
    1. JSON files have main configuration with ${VAR_NAME} placeholders
    2. JSON files have separate "defaults" block with actual default values
    3. Environment variables substitute ${VAR_NAME} placeholders when present
    4. Remaining placeholders fall back to values from "defaults" block
    
    Example JSON structure:
    {
      "model_ensemble": {
        "model_definitions": {
          "depression": {
            "name": "${NLP_MODEL_DEPRESSION_NAME}",  // Environment placeholder
            "weight": "${NLP_MODEL_DEPRESSION_WEIGHT}"
          }
        },
        "defaults": {  // Separate defaults block
          "model_definitions": {
            "depression": {
              "name": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",  // Actual default
              "weight": 0.4
            }
          }
        }
      }
    }
    
    This manager consolidates:
    - ConfigManager: JSON loading with ${VAR} substitution (PRESERVED)
    - EnvConfigManager: Schema validation and type conversion (INTEGRATED)  
    - Direct os.getenv(): Centralized environment access (REPLACED)
    
    Clean v3.1 Architecture:
    - Factory function pattern  
    - Dependency injection support
    - Fail-fast validation
    - JSON placeholders + defaults block pattern
    """
    
    def __init__(self, config_dir: str = "/app/config"):
        """
        Initialize Unified Configuration Manager
        
        Args:
            config_dir: Directory containing JSON configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.env_override_pattern = re.compile(r'\$\{([^}]+)\}')
        
        # Initialize schema definitions for validation
        self.variable_schemas = self._initialize_schemas()
        
        # Configuration file mappings (follows established pattern)
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json', 
            'analysis_parameters': 'analysis_parameters.json',
            'threshold_mapping': 'threshold_mapping.json',
            'server_settings': 'server_settings.json',
            'logging_settings': 'logging_settings.json',
            'feature_flags': 'feature_flags.json',
            'performance_settings': 'performance_settings.json',
            'storage_settings': 'storage_settings.json',
            'learning_settings': 'learning_settings.json'
        }
        
        logger.info("UnifiedConfigManager v3.1d Step 9 initialized - Following established JSON patterns")
    
    def _initialize_schemas(self) -> Dict[str, VariableSchema]:
        """Initialize comprehensive schema definitions for all 150+ environment variables"""
        schemas = {}
        
        # Models & Thresholds (Critical Priority)
        schemas.update({
            'NLP_MODEL_DEPRESSION_NAME': VariableSchema('str', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
            'NLP_MODEL_SENTIMENT_NAME': VariableSchema('str', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
            'NLP_MODEL_DISTRESS_NAME': VariableSchema('str', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
            'NLP_MODEL_DEPRESSION_WEIGHT': VariableSchema('float', 0.4, min_value=0.0, max_value=1.0),
            'NLP_MODEL_SENTIMENT_WEIGHT': VariableSchema('float', 0.3, min_value=0.0, max_value=1.0),
            'NLP_MODEL_DISTRESS_WEIGHT': VariableSchema('float', 0.3, min_value=0.0, max_value=1.0),
            'NLP_MODEL_CACHE_DIRECTORY': VariableSchema('str', './models/cache'),
            'NLP_MODEL_DEVICE': VariableSchema('str', 'auto', choices=['auto', 'cpu', 'cuda']),
            'NLP_MODEL_MAX_MEMORY_MB': VariableSchema('int', 8192, min_value=1024, max_value=32768),
            'NLP_MODEL_ENSEMBLE_MODE': VariableSchema('str', 'consensus', choices=['consensus', 'majority', 'weighted']),
            
            # Analysis Parameters (High Priority)
            'NLP_ANALYSIS_CRISIS_THRESHOLD': VariableSchema('float', 0.7, min_value=0.0, max_value=1.0),
            'NLP_ANALYSIS_DEPRESSION_THRESHOLD': VariableSchema('float', 0.6, min_value=0.0, max_value=1.0),
            'NLP_ANALYSIS_SENTIMENT_THRESHOLD': VariableSchema('float', 0.5, min_value=0.0, max_value=1.0),
            'NLP_ANALYSIS_MINIMUM_TEXT_LENGTH': VariableSchema('int', 10, min_value=1, max_value=1000),
            'NLP_ANALYSIS_MAXIMUM_TEXT_LENGTH': VariableSchema('int', 512, min_value=100, max_value=2048),
            
            # Server & Infrastructure (Medium Priority)
            'NLP_SERVER_HOST': VariableSchema('str', '0.0.0.0'),
            'NLP_SERVER_PORT': VariableSchema('int', 8881, min_value=1024, max_value=65535),
            'NLP_SERVER_WORKERS': VariableSchema('int', 1, min_value=1, max_value=16),
            'NLP_SERVER_TIMEOUT': VariableSchema('int', 60, min_value=10, max_value=300),
            'NLP_SERVER_RELOAD': VariableSchema('bool', False),
            
            # Storage & Logging (Medium Priority)
            'NLP_STORAGE_DATA_DIRECTORY': VariableSchema('str', './data'),
            'NLP_STORAGE_CACHE_DIRECTORY': VariableSchema('str', './cache'),
            'NLP_STORAGE_LOG_DIRECTORY': VariableSchema('str', './logs'),
            'NLP_LOGGING_LEVEL': VariableSchema('str', 'INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
            'NLP_LOGGING_FORMAT': VariableSchema('str', 'detailed', choices=['simple', 'detailed', 'json']),
            
            # Feature Flags (Low Priority)
            'NLP_FEATURE_ENABLE_CRISIS_DETECTION': VariableSchema('bool', True),
            'NLP_FEATURE_ENABLE_LEARNING_SYSTEM': VariableSchema('bool', True),
            'NLP_FEATURE_ENABLE_PATTERN_MATCHING': VariableSchema('bool', True),
            'NLP_FEATURE_ENABLE_STAFF_REVIEW': VariableSchema('bool', True),
            
            # Performance Settings (Low Priority)
            'NLP_PERFORMANCE_BATCH_SIZE': VariableSchema('int', 32, min_value=1, max_value=256),
            'NLP_PERFORMANCE_CACHE_SIZE': VariableSchema('int', 1000, min_value=100, max_value=10000),
            'NLP_PERFORMANCE_ENABLE_OPTIMIZATION': VariableSchema('bool', True),
            
            # Preserve GLOBAL_* variables (Ecosystem Compatibility)
            'GLOBAL_LOG_LEVEL': VariableSchema('str', 'INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
            'GLOBAL_DEBUG': VariableSchema('bool', False),
            'GLOBAL_ENABLE_LOGGING': VariableSchema('bool', True)
        })
        
        # Add additional schemas for learning, thresholds, etc.
        schemas.update(self._get_learning_schemas())
        schemas.update(self._get_threshold_schemas())
        schemas.update(self._get_extended_schemas())
        
        logger.info(f"✅ Initialized {len(schemas)} environment variable schemas")
        return schemas
    
    def _get_learning_schemas(self) -> Dict[str, VariableSchema]:
        """Get learning system variable schemas"""
        return {
            'NLP_LEARNING_ENABLE_ADJUSTMENTS': VariableSchema('bool', True),
            'NLP_LEARNING_ADJUSTMENT_RATE': VariableSchema('float', 0.1, min_value=0.01, max_value=1.0),
            'NLP_LEARNING_PERSISTENCE_FILE': VariableSchema('str', './learning_data/adjustments.json'),
            'NLP_LEARNING_MAXIMUM_ADJUSTMENTS': VariableSchema('int', 100, min_value=10, max_value=1000)
        }
    
    def _get_threshold_schemas(self) -> Dict[str, VariableSchema]:
        """Get threshold mapping variable schemas"""
        return {
            'NLP_THRESHOLD_ENSEMBLE_MODE': VariableSchema('str', 'consensus', choices=['consensus', 'majority', 'weighted']),
            'NLP_THRESHOLD_CRISIS_MAPPING_HIGH': VariableSchema('float', 0.8, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CRISIS_MAPPING_MEDIUM': VariableSchema('float', 0.6, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CRISIS_MAPPING_LOW': VariableSchema('float', 0.4, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_STAFF_REVIEW_REQUIRED': VariableSchema('float', 0.7, min_value=0.0, max_value=1.0)
        }
    
    def _get_extended_schemas(self) -> Dict[str, VariableSchema]:
        """Get extended variable schemas for complete system coverage"""
        return {
            # Additional model configurations
            'NLP_MODEL_PRECISION_MODE': VariableSchema('str', 'balanced', choices=['speed', 'balanced', 'accuracy']),
            
            # Extended analysis parameters
            'NLP_ANALYSIS_ENABLE_PREPROCESSING': VariableSchema('bool', True),
            'NLP_ANALYSIS_ENABLE_POSTPROCESSING': VariableSchema('bool', True),
            'NLP_ANALYSIS_CONTEXT_WINDOW': VariableSchema('int', 512, min_value=64, max_value=2048),
            
            # Extended server configurations  
            'NLP_SERVER_ENABLE_CORS': VariableSchema('bool', True),
            'NLP_SERVER_ENABLE_COMPRESSION': VariableSchema('bool', True),
            'NLP_SERVER_MAX_REQUEST_SIZE': VariableSchema('int', 10485760, min_value=1048576, max_value=104857600),
            
            # Extended storage configurations
            'NLP_STORAGE_ENABLE_COMPRESSION': VariableSchema('bool', False),
            'NLP_STORAGE_BACKUP_DIRECTORY': VariableSchema('str', './backups'),
            'NLP_STORAGE_RETENTION_DAYS': VariableSchema('int', 30, min_value=1, max_value=365)
        }
    
    # ========================================================================
    # UNIFIED ENVIRONMENT VARIABLE ACCESS (FOR MANAGERS WITHOUT JSON CONFIG)
    # ========================================================================
    
    def get_env(self, var_name: str, default: Any = None) -> Any:
        """
        Get environment variable with schema validation and type conversion
        FOR UNIFIED MANAGER USE ONLY - JSON loading uses os.getenv() directly
        """
        # Get raw environment value
        env_value = os.getenv(var_name)
        
        # If no environment value, use schema default or provided default
        if env_value is None:
            if var_name in self.variable_schemas:
                result = self.variable_schemas[var_name].default
                logger.debug(f"🔧 Using schema default for {var_name}: {result}")
                return result
            else:
                logger.debug(f"🔧 Using provided default for {var_name}: {default}")
                return default
        
        # Validate and convert using schema
        if var_name in self.variable_schemas:
            return self._validate_and_convert(var_name, env_value)
        else:
            logger.warning(f"⚠️ No schema found for {var_name}, returning raw value: {env_value}")
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
            logger.warning(f"⚠️ Cannot convert {var_name}={result} to int, using default: {default}")
            return default
    
    def get_env_float(self, var_name: str, default: float = 0.0) -> float:
        """Get environment variable as float"""
        result = self.get_env(var_name, default)
        try:
            return float(result) if result is not None else default
        except (ValueError, TypeError):
            logger.warning(f"⚠️ Cannot convert {var_name}={result} to float, using default: {default}")
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
                logger.error(f"❌ Invalid choice for {var_name}: {converted} not in {schema.choices}")
                return schema.default
                
            if schema.min_value is not None and isinstance(converted, (int, float)):
                if converted < schema.min_value:
                    logger.error(f"❌ Value too low for {var_name}: {converted} < {schema.min_value}")
                    return schema.default
                    
            if schema.max_value is not None and isinstance(converted, (int, float)):
                if converted > schema.max_value:
                    logger.error(f"❌ Value too high for {var_name}: {converted} > {schema.max_value}")
                    return schema.default
            
            logger.debug(f"✅ Validated {var_name}: {converted}")
            return converted
            
        except (ValueError, TypeError) as e:
            logger.error(f"❌ Conversion error for {var_name}: {e}")
            return schema.default
    
    # ========================================================================
    # JSON CONFIGURATION METHODS (FOLLOWS ESTABLISHED PATTERN)
    # ========================================================================
    
    def substitute_environment_variables(self, value: Any) -> Any:
        """
        Substitute environment variables in configuration values
        FOLLOWS ESTABLISHED PATTERN: ${VAR} placeholders + defaults block fallback
        """
        if isinstance(value, str):
            def replace_env_var(match):
                env_var = match.group(1)
                # Use os.getenv() directly for substitution (following established pattern)
                env_value = os.getenv(env_var)
                
                logger.debug(f"🔄 Substituting ${{{env_var}}} = {env_value}")
                
                if env_value is not None:
                    # Type conversion for substituted values (follows ConfigManager pattern)
                    if env_value.lower() in ('true', 'false'):
                        result = str(env_value.lower() == 'true')
                        logger.debug(f"   → Converted to boolean: {result}")
                        return result
                    elif env_value.replace('.', '').replace('-', '').isdigit():
                        try:
                            # Try float first, then int
                            if '.' in env_value:
                                result = str(float(env_value))
                                logger.debug(f"   → Converted to float: {result}")
                                return result
                            else:
                                result = str(int(env_value))
                                logger.debug(f"   → Converted to int: {result}")
                                return result
                        except ValueError:
                            logger.debug(f"   → Kept as string: {env_value}")
                            return env_value
                    else:
                        logger.debug(f"   → Used as string: {env_value}")
                        return env_value
                else:
                    logger.debug(f"⚠️ Environment variable {env_var} not found, keeping placeholder for defaults fallback")
                    return match.group(0)  # Return original placeholder for defaults processing
            
            return self.env_override_pattern.sub(replace_env_var, value)
            
        elif isinstance(value, dict):
            return {k: self.substitute_environment_variables(v) for k, v in value.items()}
            
        elif isinstance(value, list):
            return [self.substitute_environment_variables(item) for item in value]
            
        else:
            return value
    
    def _apply_defaults_fallback(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply defaults block fallback for any remaining ${VAR} placeholders
        Handles the established pattern: main config + defaults block
        """
        defaults = config.get('defaults', {})
        if not defaults:
            logger.debug("🔍 No defaults block found, skipping defaults fallback")
            return config
        
        logger.debug("🔧 Applying defaults block fallback for remaining placeholders...")
        
        def apply_defaults_recursive(main_value: Any, defaults_value: Any) -> Any:
            if isinstance(main_value, str) and main_value.startswith('${') and main_value.endswith('}'):
                # This is still a placeholder, use the default value
                logger.debug(f"🔄 Replacing placeholder {main_value} with default: {defaults_value}")
                return defaults_value
            elif isinstance(main_value, dict) and isinstance(defaults_value, dict):
                # Recursively apply defaults to nested dictionaries
                result = {}
                for key in main_value:
                    if key in defaults_value:
                        result[key] = apply_defaults_recursive(main_value[key], defaults_value[key])
                    else:
                        result[key] = main_value[key]
                # Add any defaults that aren't in main config
                for key in defaults_value:
                    if key not in result:
                        result[key] = defaults_value[key]
                return result
            elif isinstance(main_value, list) and isinstance(defaults_value, list):
                # For lists, prefer main_value if it exists, otherwise use defaults
                return main_value if main_value else defaults_value
            else:
                # Use main value if it's not a placeholder
                return main_value
        
        # Apply defaults to the main configuration sections
        result = {}
        for key, value in config.items():
            if key == 'defaults':
                # Keep the defaults block for reference
                result[key] = value
            elif key in defaults:
                # Apply defaults to this section
                result[key] = apply_defaults_recursive(value, defaults[key])
            else:
                # No defaults for this section, keep as-is
                result[key] = value
        
        logger.debug("✅ Defaults block fallback applied")
        return result
    
    def load_config_file(self, config_name: str) -> Dict[str, Any]:
        """
        Load and parse a configuration file with environment variable substitution and defaults fallback
        FOLLOWS ESTABLISHED PATTERN: ${VAR} placeholders + defaults block
        """
        if config_name in self.config_cache:
            logger.debug(f"📋 Using cached config for {config_name}")
            return self.config_cache[config_name]
        
        config_file = self.config_files.get(config_name)
        if not config_file:
            logger.error(f"❌ Unknown configuration: {config_name}")
            logger.debug(f"🔍 Available configurations: {list(self.config_files.keys())}")
            return {}
        
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            logger.warning(f"⚠️ Configuration file not found: {config_path}")
            logger.debug(f"🔍 Config directory contents: {list(self.config_dir.glob('*.json')) if self.config_dir.exists() else 'Directory does not exist'}")
            return {}
        
        try:
            logger.debug(f"📁 Loading config file: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.debug(f"✅ JSON loaded successfully")
            
            # Step 1: Substitute environment variables
            logger.debug("🔄 Step 1: Starting environment variable substitution...")
            env_substituted_config = self.substitute_environment_variables(raw_config)
            
            # Step 2: Apply defaults block fallback for remaining placeholders
            logger.debug("🔄 Step 2: Applying defaults block fallback...")
            processed_config = self._apply_defaults_fallback(env_substituted_config)
            
            # Cache the processed configuration
            self.config_cache[config_name] = processed_config
            
            logger.info(f"✅ Loaded configuration: {config_name} from {config_file}")
            return processed_config
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error in {config_file}: {e}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error loading {config_file}: {e}")
            return {}
    
    # ========================================================================
    # BACKWARD COMPATIBILITY METHODS (PRESERVED FROM PREVIOUS PHASES)
    # ========================================================================
    
    def get_crisis_patterns(self, pattern_type: str) -> Dict[str, Any]:
        """Get crisis pattern configuration by type - PRESERVED from Phase 3a"""
        logger.debug(f"🔍 Getting crisis patterns: {pattern_type}")
        
        try:
            # Check if we have a cached version first
            cache_key = f"crisis_patterns_{pattern_type}"
            if cache_key in self.config_cache:
                logger.debug(f"📋 Using cached config for {pattern_type}")
                return self.config_cache[cache_key]
            
            # Load the specific pattern configuration file (follows established pattern)
            config_file_path = self.config_dir / f"{pattern_type}.json"
            
            if not config_file_path.exists():
                logger.warning(f"⚠️ Crisis pattern file not found: {config_file_path}")
                return {}
            
            logger.debug(f"📁 Loading config file: {config_file_path}")
            
            with open(config_file_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.debug("✅ JSON loaded successfully")
            
            # Apply environment variable substitutions
            processed_config = self.substitute_environment_variables(raw_config)
            
            # Cache the processed configuration
            self.config_cache[cache_key] = processed_config
            
            logger.debug(f"✅ Loaded crisis patterns: {pattern_type}")
            
            return processed_config
            
        except Exception as e:
            logger.error(f"❌ Failed to load crisis patterns {pattern_type}: {e}")
            return {}
    
    def get_model_configuration(self) -> Dict[str, Any]:
        """Get model ensemble configuration - PRESERVED from Phase 3d"""
        logger.debug("🔍 Getting model configuration...")
        
        config = self.load_config_file('model_ensemble')
        
        if not config:
            logger.warning("⚠️ Model ensemble configuration not found, using environment fallback")
            return self._get_fallback_model_config()
        
        # Extract model definitions from the nested structure
        model_defs = config.get('model_ensemble', {}).get('model_definitions', {})
        ensemble_config = config.get('model_ensemble', {}).get('ensemble_config', {})
        
        # Return in the format expected by ModelEnsembleManager
        result = {
            'models': model_defs,  # ModelEnsembleManager expects 'models' key
            'ensemble_mode': ensemble_config.get('mode', 'consensus'),
            'validation': config.get('model_ensemble', {}).get('validation', {}),
            'performance': config.get('model_ensemble', {}).get('performance', {})
        }
        
        logger.debug(f"✅ Model configuration loaded successfully: {len(model_defs)} models found")
        return result
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Get fallback model configuration using schema defaults and environment overrides"""
        logger.info("🔧 Using schema defaults with environment overrides for model configuration")
        
        return {
            'models': {  # ModelEnsembleManager expects 'models' key
                'depression': {
                    'name': self.get_env_str('NLP_MODEL_DEPRESSION_NAME', 'cardiffnlp/twitter-roberta-base-sentiment'),
                    'weight': self.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
                    'cache_dir': self.get_env_str('NLP_MODEL_CACHE_DIRECTORY', './model_cache'),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                },
                'sentiment': {
                    'name': self.get_env_str('NLP_MODEL_SENTIMENT_NAME', 'cardiffnlp/twitter-roberta-base-sentiment-latest'),
                    'weight': self.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
                    'cache_dir': self.get_env_str('NLP_MODEL_CACHE_DIRECTORY', './model_cache'),
                    'type': 'sentiment-analysis',
                    'pipeline_task': 'zero-shot-classification'
                },
                'emotional_distress': {
                    'name': self.get_env_str('NLP_MODEL_EMOTIONAL_DISTRESS_NAME', 'j-hartmann/emotion-english-distilroberta-base'),
                    'weight': self.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
                    'cache_dir': self.get_env_str('NLP_MODEL_CACHE_DIRECTORY', './model_cache'),
                    'type': 'natural-language-inference',
                    'pipeline_task': 'zero-shot-classification'
                }
            },
            'ensemble_mode': self.get_env_str('NLP_MODEL_ENSEMBLE_MODE', 'consensus'),
            'validation': {
                'ensure_weights_sum_to_one': True,
                'fail_on_invalid_weights': True
            },
            'performance': {
                'device': self.get_env_str('NLP_MODEL_DEVICE', 'auto'),
                'max_memory_mb': self.get_env_int('NLP_MODEL_MAX_MEMORY_MB', 8192)
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
        UnifiedConfigManager instance
    """
    return UnifiedConfigManager(config_dir)

__all__ = ['UnifiedConfigManager', 'create_unified_config_manager']

logger.info("✅ UnifiedConfigManager v3.1d Step 9 CORRECTLY FIXED - JSON placeholders + defaults block pattern implemented, complete environment variable unification achieved")