"""
Unified Configuration Manager for Ash-NLP v3.1d Step 9
Combines ConfigManager and EnvConfigManager into a single, comprehensive system
Eliminates all direct os.getenv() calls system-wide

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
    Unified Configuration Manager for Ash-NLP v3.1d Step 9
    
    Consolidates JSON configuration with environment variable overrides
    Includes comprehensive schema validation and type checking
    Eliminates all direct os.getenv() usage throughout the system
    
    Clean v3.1 Architecture:
    - Factory function pattern
    - Dependency injection support
    - Fail-fast validation
    - JSON + ENV pattern
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
        
        # Initialize schema definitions
        self.variable_schemas = self._initialize_schemas()
        
        # Configuration file mappings
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json',
            'analysis_parameters': 'analysis_parameters.json',
            'threshold_mapping': 'threshold_mapping.json',
            'server_settings': 'server_settings.json',
            'logging_settings': 'logging_settings.json',
            'feature_flags': 'feature_flags.json',
            'performance_settings': 'performance_settings.json',
            'storage_settings': 'storage_settings.json'
        }
        
        # Load and validate all environment variables
        self.env_config = self._load_all_environment_variables()
        
        logger.info("🎉 UnifiedConfigManager v3.1d Step 9 initialized - Complete environment variable unification")
    
    def _initialize_schemas(self) -> Dict[str, VariableSchema]:
        """Initialize comprehensive variable schemas for validation"""
        schemas = {}
        
        # ===== GLOBAL ECOSYSTEM VARIABLES (PRESERVE EXACTLY) =====
        global_vars = {
            'GLOBAL_HUGGINGFACE_TOKEN': VariableSchema('str', '', description="HuggingFace API token"),
            'GLOBAL_NLP_API_PORT': VariableSchema('int', 8881, min_value=1000, max_value=65535, description="NLP API server port"),
            'GLOBAL_ALLOWED_IPS': VariableSchema('str', '*', description="Allowed IP addresses for API access"),
            'GLOBAL_ENABLE_CORS': VariableSchema('bool', True, description="Enable CORS for API"),
            'GLOBAL_LOG_LEVEL': VariableSchema('str', 'INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], description="Global logging level"),
            'GLOBAL_ENABLE_LEARNING_SYSTEM': VariableSchema('bool', True, description="Enable learning system")
        }
        schemas.update(global_vars)
        
        # ===== MODEL CONFIGURATION VARIABLES =====
        model_vars = {
            'NLP_MODEL_DEPRESSION': VariableSchema('str', 'SamLowe/roberta-base-go_emotions', description="Depression detection model"),
            'NLP_MODEL_SENTIMENT': VariableSchema('str', 'cardiffnlp/twitter-roberta-base-sentiment-latest', description="Sentiment analysis model"),
            'NLP_MODEL_EMOTIONAL_DISTRESS': VariableSchema('str', 'j-hartmann/emotion-english-distilroberta-base', description="Emotional distress model"),
            'NLP_MODEL_WEIGHT_DEPRESSION': VariableSchema('float', 0.4, min_value=0.0, max_value=1.0, description="Depression model weight"),
            'NLP_MODEL_WEIGHT_SENTIMENT': VariableSchema('float', 0.3, min_value=0.0, max_value=1.0, description="Sentiment model weight"),
            'NLP_MODEL_WEIGHT_EMOTIONAL_DISTRESS': VariableSchema('float', 0.3, min_value=0.0, max_value=1.0, description="Emotional distress model weight"),
            'NLP_MODEL_DEVICE': VariableSchema('str', 'auto', choices=['auto', 'cpu', 'cuda'], description="Model computation device"),
            'NLP_MODEL_PRECISION': VariableSchema('str', 'float16', choices=['float16', 'float32'], description="Model precision"),
            'NLP_MODEL_MAX_BATCH_SIZE': VariableSchema('int', 32, min_value=1, max_value=256, description="Maximum batch size"),
            'NLP_MODEL_INFERENCE_THREADS': VariableSchema('int', 16, min_value=1, max_value=64, description="Inference thread count")
        }
        schemas.update(model_vars)
        
        # ===== STORAGE DIRECTORY VARIABLES =====
        storage_vars = {
            'NLP_STORAGE_MODELS_DIR': VariableSchema('str', '/app/models', description="Models storage directory"),
            'NLP_STORAGE_CACHE_DIR': VariableSchema('str', '/app/models/cache', description="Model cache directory"),
            'NLP_STORAGE_DATA_DIR': VariableSchema('str', '/app/data', description="Data storage directory"),
            'NLP_STORAGE_LOGS_DIR': VariableSchema('str', '/app/logs', description="Logs storage directory"),
            'NLP_STORAGE_LEARNING_DATA_DIR': VariableSchema('str', '/app/learning_data', description="Learning data directory"),
            'NLP_STORAGE_CONFIG_DIR': VariableSchema('str', '/app/config', description="Configuration directory"),
            'NLP_STORAGE_TEMP_DIR': VariableSchema('str', '/tmp', description="Temporary files directory"),
            'NLP_STORAGE_BACKUP_DIR': VariableSchema('str', '/app/backups', description="Backup directory")
        }
        schemas.update(storage_vars)
        
        # ===== SERVER CONFIGURATION VARIABLES =====
        server_vars = {
            'NLP_SERVER_HOST': VariableSchema('str', '0.0.0.0', description="Server bind address"),
            'NLP_SERVER_PORT': VariableSchema('int', 8881, min_value=1000, max_value=65535, description="Server port"),
            'NLP_SERVER_WORKERS': VariableSchema('int', 4, min_value=1, max_value=32, description="Server worker processes"),
            'NLP_SERVER_TIMEOUT': VariableSchema('int', 300, min_value=30, max_value=3600, description="Server timeout seconds"),
            'NLP_SERVER_MAX_CONNECTIONS': VariableSchema('int', 100, min_value=10, max_value=1000, description="Maximum connections")
        }
        schemas.update(server_vars)
        
        # ===== LOGGING CONFIGURATION VARIABLES =====
        logging_vars = {
            'NLP_LOGGING_ENABLE_DETAILED': VariableSchema('bool', True, description="Enable detailed logging"),
            'NLP_LOGGING_INCLUDE_RAW_LABELS': VariableSchema('bool', True, description="Include raw labels in logs"),
            'NLP_LOGGING_ANALYSIS_STEPS': VariableSchema('bool', False, description="Log analysis steps"),
            'NLP_LOGGING_PERFORMANCE_METRICS': VariableSchema('bool', True, description="Log performance metrics"),
            'NLP_LOGGING_INCLUDE_REASONING': VariableSchema('bool', True, description="Include reasoning in logs"),
            'NLP_LOGGING_THRESHOLD_CHANGES': VariableSchema('bool', True, description="Log threshold changes"),
            'NLP_LOGGING_MODEL_DISAGREEMENTS': VariableSchema('bool', True, description="Log model disagreements"),
            'NLP_LOGGING_STAFF_REVIEW_TRIGGERS': VariableSchema('bool', True, description="Log staff review triggers"),
            'NLP_LOGGING_PATTERN_ADJUSTMENTS': VariableSchema('bool', True, description="Log pattern adjustments"),
            'NLP_LOGGING_LEARNING_UPDATES': VariableSchema('bool', True, description="Log learning updates"),
            'NLP_LOGGING_LABEL_MAPPINGS': VariableSchema('bool', True, description="Log label mappings"),
            'NLP_LOGGING_ENSEMBLE_DECISIONS': VariableSchema('bool', True, description="Log ensemble decisions"),
            'NLP_LOGGING_CRISIS_DETECTION': VariableSchema('bool', True, description="Log crisis detection"),
            'NLP_LOGGING_DEBUG_MODE': VariableSchema('bool', False, description="Enable debug mode"),
            'NLP_LOGGING_TRACE_REQUESTS': VariableSchema('bool', False, description="Trace API requests"),
            'NLP_LOGGING_CONFIG_LOADING': VariableSchema('bool', False, description="Log configuration loading"),
            'NLP_LOGGING_MANAGER_INIT': VariableSchema('bool', True, description="Log manager initialization"),
            'NLP_LOGGING_ENV_VARS': VariableSchema('bool', False, description="Log environment variables")
        }
        schemas.update(logging_vars)
        
        # ===== FEATURE FLAGS =====
        feature_vars = {
            'NLP_FEATURE_ENABLE_ENHANCED_PATTERNS': VariableSchema('bool', True, description="Enable enhanced pattern matching"),
            'NLP_FEATURE_ENABLE_COMMUNITY_VOCAB': VariableSchema('bool', True, description="Enable community vocabulary"),
            'NLP_FEATURE_ENABLE_TEMPORAL_PATTERNS': VariableSchema('bool', True, description="Enable temporal pattern analysis"),
            'NLP_FEATURE_ENABLE_CONTEXT_WEIGHTS': VariableSchema('bool', True, description="Enable context weight patterns"),
            'NLP_FEATURE_ENABLE_CRISIS_BURDEN': VariableSchema('bool', True, description="Enable crisis burden detection"),
            'NLP_FEATURE_ENABLE_LGBTQIA_PATTERNS': VariableSchema('bool', True, description="Enable LGBTQIA+ specific patterns"),
            'NLP_FEATURE_ENABLE_CRISIS_IDIOMS': VariableSchema('bool', True, description="Enable crisis idiom detection"),
            'NLP_FEATURE_ENABLE_ADAPTIVE_THRESHOLDS': VariableSchema('bool', True, description="Enable adaptive thresholds"),
            'NLP_FEATURE_ENABLE_PATTERN_LEARNING': VariableSchema('bool', True, description="Enable pattern learning"),
            'NLP_FEATURE_ENABLE_ENSEMBLE_OPTIMIZATION': VariableSchema('bool', True, description="Enable ensemble optimization"),
            'NLP_FEATURE_ENABLE_REAL_TIME_ADAPTATION': VariableSchema('bool', False, description="Enable real-time adaptation"),
            'NLP_FEATURE_ENABLE_EXPERIMENTAL_MODELS': VariableSchema('bool', False, description="Enable experimental models")
        }
        schemas.update(feature_vars)
        
        # ===== PERFORMANCE SETTINGS =====
        performance_vars = {
            'NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS': VariableSchema('int', 10, min_value=1, max_value=100, description="Max concurrent requests"),
            'NLP_PERFORMANCE_REQUEST_TIMEOUT': VariableSchema('int', 30, min_value=5, max_value=300, description="Request timeout seconds"),
            'NLP_PERFORMANCE_ENABLE_CACHING': VariableSchema('bool', True, description="Enable result caching"),
            'NLP_PERFORMANCE_CACHE_TTL': VariableSchema('int', 300, min_value=60, max_value=3600, description="Cache TTL seconds"),
            'NLP_PERFORMANCE_ENABLE_COMPRESSION': VariableSchema('bool', True, description="Enable response compression"),
            'NLP_PERFORMANCE_COMPRESSION_LEVEL': VariableSchema('int', 6, min_value=1, max_value=9, description="Compression level"),
            'NLP_PERFORMANCE_ENABLE_RATE_LIMITING': VariableSchema('bool', True, description="Enable rate limiting"),
            'NLP_PERFORMANCE_RATE_LIMIT_PER_MINUTE': VariableSchema('int', 60, min_value=10, max_value=1000, description="Rate limit per minute"),
            'NLP_PERFORMANCE_ENABLE_METRICS': VariableSchema('bool', True, description="Enable performance metrics"),
            'NLP_PERFORMANCE_METRICS_INTERVAL': VariableSchema('int', 60, min_value=10, max_value=600, description="Metrics collection interval"),
            'NLP_PERFORMANCE_MEMORY_LIMIT_MB': VariableSchema('int', 4096, min_value=512, max_value=32768, description="Memory limit in MB"),
            'NLP_PERFORMANCE_ENABLE_PROFILING': VariableSchema('bool', False, description="Enable performance profiling")
        }
        schemas.update(performance_vars)
        
        return schemas
    
    def _load_all_environment_variables(self) -> Dict[str, Any]:
        """Load and validate all environment variables using schemas"""
        env_config = {}
        validation_errors = []
        
        logger.info("🔍 Loading and validating all environment variables...")
        
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
                        logger.debug(f"✅ {var_name}: Using default '{schema.default}'")
                        continue
                
                # Validate and convert the environment value
                validated_value = self._validate_and_convert(var_name, env_value, schema)
                env_config[var_name] = validated_value
                
                logger.debug(f"✅ {var_name}: '{env_value}' → {validated_value}")
                
            except Exception as e:
                validation_errors.append(f"Validation error for {var_name}: {e}")
                logger.error(f"❌ {var_name}: {e}")
        
        # Fail-fast on validation errors
        if validation_errors:
            error_msg = f"Environment variable validation failed:\n" + "\n".join(validation_errors)
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        logger.info(f"✅ Successfully loaded and validated {len(env_config)} environment variables")
        return env_config
    
    def _validate_and_convert(self, var_name: str, value: str, schema: VariableSchema) -> Any:
        """Validate and convert environment variable value according to schema"""
        try:
            # Type conversion
            if schema.var_type == 'bool':
                converted = self._parse_bool(value)
            elif schema.var_type == 'int':
                converted = int(value)
            elif schema.var_type == 'float':
                converted = float(value)
            elif schema.var_type == 'list':
                converted = [item.strip() for item in value.split(',')]
            else:  # str
                converted = value
            
            # Choices validation
            if schema.choices and converted not in schema.choices:
                raise ValueError(f"Value '{converted}' not in allowed choices: {schema.choices}")
            
            # Range validation
            if schema.var_type in ('int', 'float'):
                if schema.min_value is not None and converted < schema.min_value:
                    raise ValueError(f"Value {converted} below minimum {schema.min_value}")
                if schema.max_value is not None and converted > schema.max_value:
                    raise ValueError(f"Value {converted} above maximum {schema.max_value}")
            
            return converted
            
        except ValueError as e:
            raise ValueError(f"Invalid value '{value}' for {var_name}: {e}")
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean value from string"""
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
        
        return bool(value)
    
    # ========================================================================
    # UNIFIED ENVIRONMENT VARIABLE ACCESS METHODS
    # ========================================================================
    
    def get_env(self, var_name: str, default: Any = None) -> Any:
        """
        Get environment variable value (replaces all os.getenv() calls)
        
        Args:
            var_name: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return self.env_config.get(var_name, default)
    
    def get_env_bool(self, var_name: str, default: bool = False) -> bool:
        """Get boolean environment variable"""
        value = self.get_env(var_name, default)
        return self._parse_bool(value)
    
    def get_env_int(self, var_name: str, default: int = 0) -> int:
        """Get integer environment variable"""
        value = self.get_env(var_name, default)
        return int(value) if value is not None else default
    
    def get_env_float(self, var_name: str, default: float = 0.0) -> float:
        """Get float environment variable"""
        value = self.get_env(var_name, default)
        return float(value) if value is not None else default
    
    def get_env_list(self, var_name: str, default: List[str] = None) -> List[str]:
        """Get list environment variable (comma-separated)"""
        if default is None:
            default = []
        value = self.get_env(var_name)
        if value is None:
            return default
        if isinstance(value, list):
            return value
        return [item.strip() for item in str(value).split(',')]
    
    # ========================================================================
    # JSON CONFIGURATION METHODS (PRESERVED FROM EXISTING CONFIGMANAGER)
    # ========================================================================
    
    def substitute_environment_variables(self, value: Any) -> Any:
        """
        Substitute environment variables in configuration values
        Enhanced to use unified environment variable access - NO MORE os.getenv()
        """
        if isinstance(value, str):
            def replace_env_var(match):
                env_var = match.group(1)
                env_value = self.get_env(env_var)
                
                logger.debug(f"🔄 Substituting ${{{env_var}}} = {env_value}")
                
                if env_value is not None:
                    # Type conversion for substituted values
                    if isinstance(env_value, bool):
                        result = str(env_value).lower()
                    elif isinstance(env_value, (int, float)):
                        result = str(env_value)
                    else:
                        result = str(env_value)
                    
                    logger.debug(f"   → Substituted: {result}")
                    return result
                else:
                    logger.warning(f"⚠️ Environment variable {env_var} not found, keeping placeholder")
                    return match.group(0)  # Return original placeholder
            
            return self.env_override_pattern.sub(replace_env_var, value)
            
        elif isinstance(value, dict):
            return {k: self.substitute_environment_variables(v) for k, v in value.items()}
            
        elif isinstance(value, list):
            return [self.substitute_environment_variables(item) for item in value]
            
        else:
            return value
    
    def load_config_file(self, config_name: str) -> Dict[str, Any]:
        """Load and parse a configuration file with environment variable substitution"""
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
            return {}
        
        try:
            logger.debug(f"📁 Loading config file: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.debug("✅ JSON loaded successfully")
            
            # Substitute environment variables
            logger.debug("🔄 Starting environment variable substitution...")
            processed_config = self.substitute_environment_variables(raw_config)
            
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
    # SPECIALIZED CONFIGURATION METHODS (PRESERVED & ENHANCED)
    # ========================================================================
    
    def get_model_configuration(self) -> Dict[str, Any]:
        """Get model ensemble configuration with unified environment access"""
        logger.debug("🔍 Getting model configuration...")
        
        config = self.load_config_file('model_ensemble')
        
        if not config:
            logger.warning("⚠️ Model ensemble configuration not found, using environment fallback")
            return self._get_fallback_model_config()
        
        return config
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Fallback model configuration using unified environment access"""
        return {
            'model_ensemble': {
                'model_definitions': {
                    'depression': {
                        'model_name': self.get_env('NLP_MODEL_DEPRESSION', 'SamLowe/roberta-base-go_emotions'),
                        'weight': self.get_env_float('NLP_MODEL_WEIGHT_DEPRESSION', 0.4)
                    },
                    'sentiment': {
                        'model_name': self.get_env('NLP_MODEL_SENTIMENT', 'cardiffnlp/twitter-roberta-base-sentiment-latest'),
                        'weight': self.get_env_float('NLP_MODEL_WEIGHT_SENTIMENT', 0.3)
                    },
                    'emotional_distress': {
                        'model_name': self.get_env('NLP_MODEL_EMOTIONAL_DISTRESS', 'j-hartmann/emotion-english-distilroberta-base'),
                        'weight': self.get_env_float('NLP_MODEL_WEIGHT_EMOTIONAL_DISTRESS', 0.3)
                    }
                },
                'device_settings': {
                    'device': self.get_env('NLP_MODEL_DEVICE', 'auto'),
                    'precision': self.get_env('NLP_MODEL_PRECISION', 'float16'),
                    'max_batch_size': self.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
                    'inference_threads': self.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16)
                }
            }
        }
    
    def get_storage_configuration(self) -> Dict[str, Any]:
        """Get storage configuration with unified environment access"""
        return {
            'storage': {
                'models_dir': self.get_env('NLP_STORAGE_MODELS_DIR', '/app/models'),
                'cache_dir': self.get_env('NLP_STORAGE_CACHE_DIR', '/app/models/cache'),
                'data_dir': self.get_env('NLP_STORAGE_DATA_DIR', '/app/data'),
                'logs_dir': self.get_env('NLP_STORAGE_LOGS_DIR', '/app/logs'),
                'learning_data_dir': self.get_env('NLP_STORAGE_LEARNING_DATA_DIR', '/app/learning_data'),
                'config_dir': self.get_env('NLP_STORAGE_CONFIG_DIR', '/app/config'),
                'temp_dir': self.get_env('NLP_STORAGE_TEMP_DIR', '/tmp'),
                'backup_dir': self.get_env('NLP_STORAGE_BACKUP_DIR', '/app/backups')
            }
        }
    
    def get_server_configuration(self) -> Dict[str, Any]:
        """Get server configuration with unified environment access"""
        return {
            'server': {
                'host': self.get_env('NLP_SERVER_HOST', '0.0.0.0'),
                'port': self.get_env_int('NLP_SERVER_PORT', 8881),
                'workers': self.get_env_int('NLP_SERVER_WORKERS', 4),
                'timeout': self.get_env_int('NLP_SERVER_TIMEOUT', 300),
                'max_connections': self.get_env_int('NLP_SERVER_MAX_CONNECTIONS', 100)
            }
        }
    
    def get_logging_configuration(self) -> Dict[str, Any]:
        """Get logging configuration with unified environment access"""
        return {
            'global_logging': {
                'level': self.get_env('GLOBAL_LOG_LEVEL', 'INFO'),
                'logs_dir': self.get_env('NLP_STORAGE_LOGS_DIR', './logs')
            },
            'detailed_logging': {
                'enable_detailed': self.get_env_bool('NLP_LOGGING_ENABLE_DETAILED', True),
                'include_raw_labels': self.get_env_bool('NLP_LOGGING_INCLUDE_RAW_LABELS', True),
                'analysis_steps': self.get_env_bool('NLP_LOGGING_ANALYSIS_STEPS', False),
                'performance_metrics': self.get_env_bool('NLP_LOGGING_PERFORMANCE_METRICS', True),
                'include_reasoning': self.get_env_bool('NLP_LOGGING_INCLUDE_REASONING', True)
            },
            'component_logging': {
                'threshold_changes': self.get_env_bool('NLP_LOGGING_THRESHOLD_CHANGES', True),
                'model_disagreements': self.get_env_bool('NLP_LOGGING_MODEL_DISAGREEMENTS', True),
                'staff_review_triggers': self.get_env_bool('NLP_LOGGING_STAFF_REVIEW_TRIGGERS', True),
                'pattern_adjustments': self.get_env_bool('NLP_LOGGING_PATTERN_ADJUSTMENTS', True),
                'learning_updates': self.get_env_bool('NLP_LOGGING_LEARNING_UPDATES', True),
                'label_mappings': self.get_env_bool('NLP_LOGGING_LABEL_MAPPINGS', True),
                'ensemble_decisions': self.get_env_bool('NLP_LOGGING_ENSEMBLE_DECISIONS', True),
                'crisis_detection': self.get_env_bool('NLP_LOGGING_CRISIS_DETECTION', True)
            },
            'development_logging': {
                'debug_mode': self.get_env_bool('NLP_LOGGING_DEBUG_MODE', False),
                'trace_requests': self.get_env_bool('NLP_LOGGING_TRACE_REQUESTS', False),
                'log_configuration_loading': self.get_env_bool('NLP_LOGGING_CONFIG_LOADING', False),
                'manager_initialization': self.get_env_bool('NLP_LOGGING_MANAGER_INIT', True),
                'environment_variables': self.get_env_bool('NLP_LOGGING_ENV_VARS', False)
            }
        }
    
    def get_feature_configuration(self) -> Dict[str, Any]:
        """Get feature flags configuration with unified environment access"""
        return {
            'enhanced_patterns': {
                'enable_enhanced_patterns': self.get_env_bool('NLP_FEATURE_ENABLE_ENHANCED_PATTERNS', True),
                'enable_community_vocab': self.get_env_bool('NLP_FEATURE_ENABLE_COMMUNITY_VOCAB', True),
                'enable_temporal_patterns': self.get_env_bool('NLP_FEATURE_ENABLE_TEMPORAL_PATTERNS', True),
                'enable_context_weights': self.get_env_bool('NLP_FEATURE_ENABLE_CONTEXT_WEIGHTS', True),
                'enable_crisis_burden': self.get_env_bool('NLP_FEATURE_ENABLE_CRISIS_BURDEN', True),
                'enable_lgbtqia_patterns': self.get_env_bool('NLP_FEATURE_ENABLE_LGBTQIA_PATTERNS', True),
                'enable_crisis_idioms': self.get_env_bool('NLP_FEATURE_ENABLE_CRISIS_IDIOMS', True)
            },
            'system_features': {
                'enable_adaptive_thresholds': self.get_env_bool('NLP_FEATURE_ENABLE_ADAPTIVE_THRESHOLDS', True),
                'enable_pattern_learning': self.get_env_bool('NLP_FEATURE_ENABLE_PATTERN_LEARNING', True),
                'enable_ensemble_optimization': self.get_env_bool('NLP_FEATURE_ENABLE_ENSEMBLE_OPTIMIZATION', True),
                'enable_real_time_adaptation': self.get_env_bool('NLP_FEATURE_ENABLE_REAL_TIME_ADAPTATION', False),
                'enable_experimental_models': self.get_env_bool('NLP_FEATURE_ENABLE_EXPERIMENTAL_MODELS', False)
            }
        }
    
    def get_performance_configuration(self) -> Dict[str, Any]:
        """Get performance settings configuration with unified environment access"""
        return {
            'concurrency': {
                'max_concurrent_requests': self.get_env_int('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 10),
                'request_timeout': self.get_env_int('NLP_PERFORMANCE_REQUEST_TIMEOUT', 30)
            },
            'caching': {
                'enable_caching': self.get_env_bool('NLP_PERFORMANCE_ENABLE_CACHING', True),
                'cache_ttl': self.get_env_int('NLP_PERFORMANCE_CACHE_TTL', 300)
            },
            'compression': {
                'enable_compression': self.get_env_bool('NLP_PERFORMANCE_ENABLE_COMPRESSION', True),
                'compression_level': self.get_env_int('NLP_PERFORMANCE_COMPRESSION_LEVEL', 6)
            },
            'rate_limiting': {
                'enable_rate_limiting': self.get_env_bool('NLP_PERFORMANCE_ENABLE_RATE_LIMITING', True),
                'rate_limit_per_minute': self.get_env_int('NLP_PERFORMANCE_RATE_LIMIT_PER_MINUTE', 60)
            },
            'monitoring': {
                'enable_metrics': self.get_env_bool('NLP_PERFORMANCE_ENABLE_METRICS', True),
                'metrics_interval': self.get_env_int('NLP_PERFORMANCE_METRICS_INTERVAL', 60),
                'memory_limit_mb': self.get_env_int('NLP_PERFORMANCE_MEMORY_LIMIT_MB', 4096),
                'enable_profiling': self.get_env_bool('NLP_PERFORMANCE_ENABLE_PROFILING', False)
            }
        }
    
    # ========================================================================
    # DEPRECATED METHODS FOR BACKWARD COMPATIBILITY
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
            
            # Load the specific pattern configuration file
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

logger.info("✅ UnifiedConfigManager v3.1d Step 9 loaded - Complete environment variable unification achieved")