# ash/ash-nlp/managers/config_manager.py - Phase 3d Enhanced
"""
Enhanced Configuration Manager for Ash NLP Service v3.1d
Handles JSON configuration with environment variable overrides
Phase 3d: Unified configuration with standardized variable naming

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
"""

import os
import json
import logging
import re
from typing import Dict, Any, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigManager:
    """Enhanced configuration manager with unified variable support - Phase 3d"""
    
    def __init__(self, config_dir: str = "/app/config"):
        """
        Initialize configuration manager with Phase 3d enhancements
        
        Args:
            config_dir: Directory containing JSON configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.env_override_pattern = re.compile(r'\$\{([^}]+)\}')
        
        # Enhanced configuration files mapping - Phase 3d
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json',
            'analysis_parameters': 'analysis_parameters.json',
            'threshold_mapping': 'threshold_mapping.json',
            'performance_settings': 'performance_settings.json',
            'server_settings': 'server_settings.json',
            'storage_settings': 'storage_settings.json',
            'learning_parameters': 'learning_parameters.json',
            'logging_settings': 'logging_settings.json',   # NEW - Phase 3d Step 6
        }
        
        logger.info(f"✅ ConfigManager v3.1d initialized with config directory: {config_dir}")
        
        # DEBUG: Log standardized environment variables
        logger.debug("🔍 Phase 3d Standardized Environment Variables:")
        standardized_vars = [
            'NLP_MODEL_DEPRESSION_NAME',
            'NLP_MODEL_DEPRESSION_WEIGHT',
            'NLP_MODEL_SENTIMENT_NAME', 
            'NLP_MODEL_SENTIMENT_WEIGHT',
            'NLP_MODEL_DISTRESS_NAME',
            'NLP_MODEL_DISTRESS_WEIGHT',
            'NLP_STORAGE_MODELS_DIR',
            'NLP_ENSEMBLE_MODE'
        ]
        
        for env_var in standardized_vars:
            value = os.getenv(env_var)
            logger.debug(f"   {env_var}: {value}")
    
    def get_logging_configuration(self) -> Dict[str, Any]:
        """
        Get logging configuration with Phase 3d unified variables
        NEW in Phase 3d Step 6: Consolidates multiple logging variables
        """
        logger.debug("📝 Getting logging configuration (Phase 3d Step 6)...")
        
        config = self.load_config_file('logging_settings')
        
        if not config:
            logger.warning("⚠️ Logging configuration not found, using environment fallback")
            return self._get_fallback_logging_config()
        
        logging_config = config.get('logging_configuration', {})
        
        processed_logging = {
            'global_settings': logging_config.get('global_settings', {}),
            'detailed_logging': logging_config.get('detailed_logging', {}),
            'component_logging': logging_config.get('component_logging', {}),
            'development_logging': logging_config.get('development_logging', {}),
            'validation': logging_config.get('validation', {})
        }
        
        logger.debug(f"✅ Logging configuration loaded")
        return processed_logging

    def _get_fallback_logging_config(self) -> Dict[str, Any]:
        """
        Fallback logging configuration using Phase 3d standardized environment variables
        """
        logger.info("🔧 Using Phase 3d standardized environment variables for logging configuration")
        
        return {
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

    def get_server_configuration(self) -> Dict[str, Any]:
        """
        Get server configuration settings (NEW in Phase 3d Step 5)
        Consolidates duplicate server variables into standardized configuration
        """
        logger.debug("🖥️ Getting server configuration (Phase 3d Step 5)...")
        
        config = self.load_config_file('server_settings')
        
        if config:
            server_config = config.get('server_configuration', {})
            defaults = config.get('defaults', {})
        else:
            logger.warning("⚠️ No server_settings.json found, using environment fallbacks")
            server_config = {}
            defaults = {}
        
        # Return consolidated server configuration with environment overrides
        return {
            'network_settings': {
                'host': os.getenv('NLP_SERVER_HOST', 
                                 server_config.get('network_settings', {}).get('host', 
                                 defaults.get('network_settings', {}).get('host', '0.0.0.0'))),
                'port': int(os.getenv('GLOBAL_NLP_API_PORT', '8881')),  # PRESERVED GLOBAL
                'workers': int(os.getenv('NLP_SERVER_WORKERS', 
                                       server_config.get('network_settings', {}).get('workers', 
                                       defaults.get('network_settings', {}).get('workers', 1)))),
                'reload_on_changes': self._parse_bool(os.getenv('NLP_SERVER_RELOAD_ON_CHANGES', 
                                                              server_config.get('network_settings', {}).get('reload_on_changes', 
                                                              defaults.get('network_settings', {}).get('reload_on_changes', False))))
            },
            'performance_settings': {
                'max_concurrent_requests': int(os.getenv('NLP_SERVER_MAX_CONCURRENT_REQUESTS', 
                                                       server_config.get('performance_settings', {}).get('max_concurrent_requests', 
                                                       defaults.get('performance_settings', {}).get('max_concurrent_requests', 20)))),
                'request_timeout': int(os.getenv('NLP_SERVER_REQUEST_TIMEOUT', 
                                               server_config.get('performance_settings', {}).get('request_timeout', 
                                               defaults.get('performance_settings', {}).get('request_timeout', 40)))),
                'worker_timeout': int(os.getenv('NLP_SERVER_WORKER_TIMEOUT', 
                                              server_config.get('performance_settings', {}).get('worker_timeout', 
                                              defaults.get('performance_settings', {}).get('worker_timeout', 60))))
            },
            'security_settings': {
                'rate_limiting': {
                    'requests_per_minute': int(os.getenv('NLP_SECURITY_REQUESTS_PER_MINUTE', 
                                                       server_config.get('security_settings', {}).get('rate_limiting', {}).get('requests_per_minute', 
                                                       defaults.get('security_settings', {}).get('rate_limiting', {}).get('requests_per_minute', 120)))),
                    'requests_per_hour': int(os.getenv('NLP_SECURITY_REQUESTS_PER_HOUR', 
                                                     server_config.get('security_settings', {}).get('rate_limiting', {}).get('requests_per_hour', 
                                                     defaults.get('security_settings', {}).get('rate_limiting', {}).get('requests_per_hour', 2000)))),
                    'burst_limit': int(os.getenv('NLP_SECURITY_BURST_LIMIT', 
                                               server_config.get('security_settings', {}).get('rate_limiting', {}).get('burst_limit', 
                                               defaults.get('security_settings', {}).get('rate_limiting', {}).get('burst_limit', 150))))
                },
                'access_control': {
                    'allowed_ips': os.getenv('GLOBAL_ALLOWED_IPS', '10.20.30.0/24,127.0.0.1,::1'),  # PRESERVED GLOBAL
                    'cors_enabled': self._parse_bool(os.getenv('GLOBAL_ENABLE_CORS', 'true'))  # PRESERVED GLOBAL
                }
            },
            'operational_settings': {
                'health_check_interval': int(os.getenv('NLP_SERVER_HEALTH_CHECK_INTERVAL', 
                                                     server_config.get('operational_settings', {}).get('health_check_interval', 
                                                     defaults.get('operational_settings', {}).get('health_check_interval', 30)))),
                'graceful_shutdown_timeout': int(os.getenv('NLP_SERVER_SHUTDOWN_TIMEOUT', 
                                                         server_config.get('operational_settings', {}).get('graceful_shutdown_timeout', 
                                                         defaults.get('operational_settings', {}).get('graceful_shutdown_timeout', 10)))),
                'startup_timeout': int(os.getenv('NLP_SERVER_STARTUP_TIMEOUT', 
                                               server_config.get('operational_settings', {}).get('startup_timeout', 
                                               defaults.get('operational_settings', {}).get('startup_timeout', 120))))
            }
        }

    def _parse_bool(self, value: Union[str, bool]) -> bool:
        """Parse boolean value from string or bool"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return False

    def get_ensemble_mode(self) -> str:
        """
        Get current ensemble mode setting
        Phase 3d: Standardized ensemble mode access
        """
        logger.debug("🔍 Getting ensemble mode...")
        
        config = self.load_config_file('model_ensemble')
        
        if config:
            # Try to get from model ensemble configuration
            ensemble_mode = config.get('model_ensemble', {}).get('ensemble_settings', {}).get('mode')
            if ensemble_mode:
                logger.debug(f"✅ Ensemble mode from JSON: {ensemble_mode}")
                return ensemble_mode
        
        # Fallback to environment variable
        ensemble_mode = os.getenv('NLP_ENSEMBLE_MODE', 'consensus')
        logger.debug(f"🔧 Ensemble mode from environment: {ensemble_mode}")
        return ensemble_mode

    def get_hardware_configuration(self) -> Dict[str, Any]:
        """
        Get hardware configuration settings
        NEW in Phase 3d: Standardized hardware configuration access
        """
        logger.debug("🔍 Getting hardware configuration...")
        
        config = self.load_config_file('model_ensemble')
        
        if config:
            hardware_config = config.get('model_ensemble', {}).get('hardware_settings', {})
        else:
            hardware_config = {}
        
        # Return standardized hardware configuration
        return {
            'device': hardware_config.get('device', os.getenv('NLP_HARDWARE_DEVICE', 'auto')),
            'precision': hardware_config.get('precision', os.getenv('NLP_HARDWARE_PRECISION', 'float16')),
            'max_batch_size': int(hardware_config.get('max_batch_size', os.getenv('NLP_HARDWARE_MAX_BATCH_SIZE', '32'))),
            'inference_threads': int(hardware_config.get('inference_threads', os.getenv('NLP_HARDWARE_INFERENCE_THREADS', '16')))
        }

    def substitute_environment_variables(self, value: Any) -> Any:
        """
        Recursively substitute environment variables in configuration values
        Enhanced in Phase 3d for standardized variable names
        
        Args:
            value: Configuration value (can be str, dict, list, etc.)
        Returns:
            Value with environment variables substituted
        """
        if isinstance(value, str):
            # Handle environment variable substitution like ${VAR_NAME}
            def replace_env_var(match):
                env_var = match.group(1)
                env_value = os.getenv(env_var)
                
                logger.debug(f"🔄 Substituting ${{{env_var}}} = {env_value}")
                
                if env_value is not None:
                    # Try to convert to appropriate type
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
        """
        Load and parse a configuration file with environment variable substitution
        Enhanced in Phase 3d for new configuration files
        
        Args:
            config_name: Name of the configuration (key from self.config_files)
            
        Returns:
            Parsed configuration dictionary
        """
        if config_name in self.config_cache:
            logger.debug(f"📋 Using cached config for {config_name}")
            return self.config_cache[config_name]
        
        config_file = self.config_files.get(config_name)
        if not config_file:
            logger.error(f"❌ Unknown configuration: {config_name}")
            return {}
        
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            logger.warning(f"⚠️ Configuration file not found: {config_path}")
            return {}
        
        try:
            logger.debug(f"📁 Loading config file: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.debug(f"✅ JSON loaded successfully")
            
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

    def get_model_configuration(self) -> Dict[str, Any]:
        """
        Get model ensemble configuration with Phase 3d standardized variables
        Enhanced to use new variable naming: NLP_MODEL_[TYPE]_[ATTRIBUTE]
        """
        logger.debug("🔍 Getting model configuration (Phase 3d enhanced)...")
        
        config = self.load_config_file('model_ensemble')
        
        if not config:
            logger.warning("⚠️ Model ensemble configuration not found, using environment fallback")
            return self._get_fallback_model_config()
        
        # Extract and process model definitions with new variable names
        model_defs = config.get('model_ensemble', {}).get('model_definitions', {})
        processed_models = {}
        
        logger.debug("🔧 Processing model definitions with standardized variables...")
        
        for model_type, model_config in model_defs.items():
            logger.debug(f"🔍 Processing {model_type} model...")
            
            # Use standardized environment variable names
            model_name = model_config.get('name', '')
            weight_value = model_config.get('weight', 0.33)
            
            logger.debug(f"   Model name: {model_name}")
            logger.debug(f"   Weight value: {weight_value}")
            
            try:
                weight = float(weight_value) if weight_value else 0.33
                logger.debug(f"   Processed weight: {weight}")
            except (ValueError, TypeError):
                weight = 0.33
                logger.warning(f"⚠️ Invalid weight for {model_type}, using default: {weight}")
            
            processed_models[model_type] = {
                'name': model_name,
                'weight': weight,
                'type': model_config.get('type', 'unknown'),
                'purpose': model_config.get('purpose', ''),
                'pipeline_task': model_config.get('pipeline_task', 'text-classification'),
                'cache_dir': model_config.get('cache_dir', './models/cache')
            }
        
        logger.debug(f"✅ Processed {len(processed_models)} model definitions")
        
        return {
            'models': processed_models,
            'ensemble_mode': config.get('model_ensemble', {}).get('ensemble_settings', {}).get('mode', 'consensus'),
            'hardware_settings': config.get('model_ensemble', {}).get('hardware_settings', {}),
            'validation': config.get('model_ensemble', {}).get('ensemble_settings', {}).get('validation', {})
        }
    
    def get_storage_configuration(self) -> Dict[str, Any]:
        """
        Get storage configuration with Phase 3d unified variables
        NEW in Phase 3d: Consolidates multiple duplicate storage variables
        """
        logger.debug("🔍 Getting storage configuration (Phase 3d new)...")
        
        config = self.load_config_file('storage_settings')
        
        if not config:
            logger.warning("⚠️ Storage configuration not found, using environment fallback")
            return self._get_fallback_storage_config()
        
        storage_config = config.get('storage_configuration', {})
        
        processed_storage = {
            'directories': storage_config.get('directories', {}),
            'file_paths': storage_config.get('file_paths', {}),
            'cache_settings': storage_config.get('cache_settings', {}),
            'validation': storage_config.get('validation', {})
        }
        
        logger.debug(f"✅ Storage configuration loaded")
        return processed_storage
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Fallback model configuration using Phase 3d standardized environment variables"""
        logger.info("🔧 Using Phase 3d standardized environment variables for model configuration")
        
        return {
            'models': {
                'depression': {
                    'name': os.getenv('NLP_MODEL_DEPRESSION_NAME', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                    'weight': float(os.getenv('NLP_MODEL_DEPRESSION_WEIGHT', '0.4')),
                    'type': 'zero-shot-classification',
                    'cache_dir': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache')
                },
                'sentiment': {
                    'name': os.getenv('NLP_MODEL_SENTIMENT_NAME', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                    'weight': float(os.getenv('NLP_MODEL_SENTIMENT_WEIGHT', '0.3')),
                    'type': 'sentiment-analysis',
                    'cache_dir': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache')
                },
                'emotional_distress': {
                    'name': os.getenv('NLP_MODEL_DISTRESS_NAME', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                    'weight': float(os.getenv('NLP_MODEL_DISTRESS_WEIGHT', '0.3')),
                    'type': 'natural-language-inference',
                    'cache_dir': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache')
                }
            },
            'ensemble_mode': os.getenv('NLP_ENSEMBLE_MODE', 'consensus'),
            'hardware_settings': {
                'device': os.getenv('NLP_HARDWARE_DEVICE', 'auto'),
                'precision': os.getenv('NLP_HARDWARE_PRECISION', 'float16'),
                'max_batch_size': int(os.getenv('NLP_HARDWARE_MAX_BATCH_SIZE', '32'))
            }
        }
    
    def _get_fallback_storage_config(self) -> Dict[str, Any]:
        """Fallback storage configuration using Phase 3d standardized environment variables"""
        logger.info("🔧 Using Phase 3d standardized environment variables for storage configuration")
        
        return {
            'directories': {
                'data_directory': os.getenv('NLP_STORAGE_DATA_DIR', './data'),
                'models_directory': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'logs_directory': os.getenv('NLP_STORAGE_LOGS_DIR', './logs'),
                'learning_directory': os.getenv('NLP_STORAGE_LEARNING_DIR', './learning_data'),
                'cache_directory': os.getenv('NLP_STORAGE_CACHE_DIR', './cache'),
                'temp_directory': os.getenv('NLP_STORAGE_TEMP_DIR', './tmp'),
                'backup_directory': os.getenv('NLP_STORAGE_BACKUP_DIR', './backups')
            },
            'file_paths': {
                'log_file': os.getenv('NLP_STORAGE_LOG_FILE', 'nlp_service.log'),
                'learning_persistence_file': os.getenv('NLP_STORAGE_LEARNING_FILE', './learning_data/adjustments.json'),
                'pid_file': os.getenv('NLP_STORAGE_PID_FILE', './tmp/nlp_service.pid'),
                'health_check_file': os.getenv('NLP_STORAGE_HEALTH_FILE', './tmp/health_check.json'),
                'config_backup_file': os.getenv('NLP_STORAGE_CONFIG_BACKUP_FILE', './backups/config_backup.json')
            },
            'cache_settings': {
                'huggingface_cache': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'analysis_cache': os.getenv('NLP_STORAGE_CACHE_DIR', './cache'),
                'enable_model_caching': self._parse_bool(os.getenv('NLP_STORAGE_ENABLE_MODEL_CACHE', 'true')),
                'enable_analysis_caching': self._parse_bool(os.getenv('NLP_STORAGE_ENABLE_ANALYSIS_CACHE', 'true')),
                'cache_cleanup_on_startup': self._parse_bool(os.getenv('NLP_STORAGE_CACHE_CLEANUP_ON_STARTUP', 'false')),
                'model_cache_size_limit': os.getenv('NLP_STORAGE_MODEL_CACHE_SIZE_LIMIT', '10GB'),
                'analysis_cache_size_limit': os.getenv('NLP_STORAGE_ANALYSIS_CACHE_SIZE_LIMIT', '2GB'),
                'cache_expiry_hours': int(os.getenv('NLP_STORAGE_CACHE_EXPIRY_HOURS', '24'))
            },
            'validation': {
                'create_directories_on_startup': self._parse_bool(os.getenv('NLP_STORAGE_CREATE_DIRS_ON_STARTUP', 'true')),
                'validate_write_permissions': self._parse_bool(os.getenv('NLP_STORAGE_VALIDATE_PERMISSIONS', 'true')),
                'fail_on_inaccessible_directories': self._parse_bool(os.getenv('NLP_STORAGE_FAIL_ON_INACCESSIBLE', 'false'))
            }
        }
    
    # ========================================================================
    # EXISTING METHODS PRESERVED (Phase 3a-3c compatibility)
    # ========================================================================
    
    def get_crisis_patterns(self, pattern_type: str) -> Dict[str, Any]:
        """
        Get crisis pattern configuration by type - PRESERVED from Phase 3a
        No changes needed - working perfectly
        """
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

def create_config_manager(config_dir: str = "/app/config") -> ConfigManager:
    """
    Factory function to create ConfigManager instance
    
    Args:
        config_dir: Directory containing JSON configuration files
        
    Returns:
        ConfigManager instance
    """
    return ConfigManager(config_dir)

__all__ = ['ConfigManager', 'create_config_manager']

logger.info("✅ Enhanced ConfigManager v3.1d loaded - Phase 3d standardized variables supported")