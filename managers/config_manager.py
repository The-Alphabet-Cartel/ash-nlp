# ash/ash-nlp/managers/config_manager.py (Debug Version)
"""
DEBUG Enhanced Configuration Manager for Ash NLP Service v3.1
Handles JSON configuration with environment variable overrides
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import json
import logging
import re
from typing import Dict, Any, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigManager:
    """Enhanced configuration manager with JSON + environment variable support"""
    
    def __init__(self, config_dir: str = "/app/config"):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory containing JSON configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.env_override_pattern = re.compile(r'\$\{([^}]+)\}')
        
        # Configuration files to load
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json',
            'analysis_parameters': 'analysis_parameters.json',
            'performance_settings': 'performance_settings.json',
            'threshold_mapping': 'threshold_mapping.json'
        }
        
        logger.info(f"✅ ConfigManager initialized with config directory: {config_dir}")
        
        # DEBUG: Log key environment variables
        logger.info("🔍 DEBUG: Key Environment Variables:")
        env_vars_to_check = [
            'NLP_DEPRESSION_MODEL',
            'NLP_SENTIMENT_MODEL', 
            'NLP_EMOTIONAL_DISTRESS_MODEL',
            'NLP_DEPRESSION_MODEL_WEIGHT',
            'NLP_SENTIMENT_MODEL_WEIGHT',
            'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT',
            'NLP_ENSEMBLE_MODE'
        ]
        
        for env_var in env_vars_to_check:
            value = os.getenv(env_var)
            logger.info(f"   {env_var}: {value}")
    
    def substitute_environment_variables(self, value: Any) -> Any:
        """
        Recursively substitute environment variables in configuration values
        
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
                
                logger.info(f"🔄 DEBUG: Substituting ${{{env_var}}} = {env_value}")
                
                if env_value is not None:
                    # Try to convert to appropriate type
                    if env_value.lower() in ('true', 'false'):
                        result = str(env_value.lower() == 'true')
                        logger.info(f"   → Converted to boolean: {result}")
                        return result
                    elif env_value.replace('.', '').replace('-', '').isdigit():
                        try:
                            # Try float first, then int
                            if '.' in env_value:
                                result = str(float(env_value))
                                logger.info(f"   → Converted to float: {result}")
                                return result
                            else:
                                result = str(int(env_value))
                                logger.info(f"   → Converted to int: {result}")
                                return result
                        except ValueError:
                            logger.info(f"   → Kept as string: {env_value}")
                            return env_value
                    else:
                        logger.info(f"   → Used as string: {env_value}")
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
        
        Args:
            config_name: Name of the configuration (key from self.config_files)
            
        Returns:
            Parsed configuration dictionary
        """
        if config_name in self.config_cache:
            logger.info(f"📋 DEBUG: Using cached config for {config_name}")
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
            logger.info(f"📁 DEBUG: Loading config file: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.info(f"✅ DEBUG: JSON loaded successfully")
            
            # DEBUG: Log before substitution
            model_defs = raw_config.get('model_definitions', {})
            logger.info("🔍 DEBUG: Model definitions BEFORE substitution:")
            for model_type, model_config in model_defs.items():
                logger.info(f"   {model_type}: {model_config.get('name', 'NO_NAME')}")
            
            # Substitute environment variables
            logger.info("🔄 DEBUG: Starting environment variable substitution...")
            processed_config = self.substitute_environment_variables(raw_config)
            
            # DEBUG: Log after substitution
            processed_model_defs = processed_config.get('model_definitions', {})
            logger.info("🔍 DEBUG: Model definitions AFTER substitution:")
            for model_type, model_config in processed_model_defs.items():
                logger.info(f"   {model_type}: {model_config.get('name', 'NO_NAME')}")
            
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
        """Get model ensemble configuration with environment overrides"""
        logger.info("🔍 DEBUG: Getting model configuration...")
        
        config = self.load_config_file('model_ensemble')
        
        if not config:
            logger.warning("⚠️ Model ensemble configuration not found, using environment fallback")
            return self._get_fallback_model_config()
        
        # Extract and process model definitions
        model_defs = config.get('model_definitions', {})
        processed_models = {}
        
        logger.info("🔧 DEBUG: Processing model definitions...")
        
        for model_type, model_config in model_defs.items():
            logger.info(f"🔍 DEBUG: Processing {model_type} model...")
            
            # Get model name with environment override
            env_var = model_config.get('environment_variable')
            logger.info(f"   Environment variable: {env_var}")
            
            if env_var and os.getenv(env_var):
                model_name = os.getenv(env_var)
                logger.info(f"🔄 Environment override for {model_type}: {model_name}")
            else:
                model_name = model_config.get('name', model_config.get('default_name', ''))
                logger.info(f"   Using config/default name: {model_name}")
            
            # Get weight with environment override
            weight_str = str(model_config.get('weight', model_config.get('default_weight', 0.33)))
            logger.info(f"   Weight string: {weight_str}")
            
            try:
                weight = float(weight_str)
                logger.info(f"   Weight value: {weight}")
            except (ValueError, TypeError):
                weight = model_config.get('default_weight', 0.33)
                logger.warning(f"⚠️ Invalid weight for {model_type}, using default: {weight}")
            
            processed_models[model_type] = {
                'name': model_name,
                'weight': weight,
                'type': model_config.get('type', 'unknown'),
                'purpose': model_config.get('purpose', ''),
                'pipeline_task': model_config.get('pipeline_task', 'zero-shot-classification'),
                'model_kwargs': model_config.get('model_kwargs', {}),
                'pipeline_kwargs': model_config.get('pipeline_kwargs', {})
            }
            
            logger.info(f"✅ Processed {model_type}: {model_name} (weight: {weight})")
        
        # Validate weights sum to 1.0
        total_weight = sum(model['weight'] for model in processed_models.values())
        logger.info(f"🔍 DEBUG: Total weight: {total_weight}")
        
        if abs(total_weight - 1.0) > 0.001:
            logger.warning(f"⚠️ Model weights sum to {total_weight}, should be 1.0")
        
        result = {
            'models': processed_models,
            'ensemble_config': config.get('ensemble_configuration', {}),
            'hardware_config': config.get('hardware_optimization', {}),
            'threshold_config': config.get('threshold_configuration', {}),
            'feature_flags': config.get('feature_flags', {}),
            'validation_rules': config.get('validation_rules', {})
        }
        
        logger.info("✅ DEBUG: Model configuration processing complete")
        return result
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Fallback configuration using only environment variables"""
        logger.info("🔄 DEBUG: Using fallback environment configuration")
        
        config = {
            'models': {
                'depression': {
                    'name': os.getenv('NLP_DEPRESSION_MODEL', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                    'weight': float(os.getenv('NLP_DEPRESSION_MODEL_WEIGHT', '0.75')),
                    'type': 'DeBERTa-based classification'
                },
                'sentiment': {
                    'name': os.getenv('NLP_SENTIMENT_MODEL', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                    'weight': float(os.getenv('NLP_SENTIMENT_MODEL_WEIGHT', '0.10')),
                    'type': 'DeBERTa-based sentiment'
                },
                'emotional_distress': {
                    'name': os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                    'weight': float(os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', '0.15')),
                    'type': 'Topic sentiment analysis'
                }
            },
            'ensemble_config': {
                'default_mode': os.getenv('NLP_ENSEMBLE_MODE', 'majority'),
                'gap_detection': {
                    'enabled': os.getenv('NLP_ENABLE_GAP_DETECTION', 'true').lower() == 'true',
                    'threshold': float(os.getenv('NLP_GAP_DETECTION_THRESHOLD', '0.25'))
                }
            }
        }
        
        for model_type, model_info in config['models'].items():
            logger.info(f"   {model_type}: {model_info['name']} (weight: {model_info['weight']})")
        
        return config
    
    def get_threshold_configuration(self) -> Dict[str, Any]:
        """Get threshold configuration with environment overrides"""
        config = self.load_config_file('model_ensemble')
        
        if config and 'threshold_configuration' in config:
            return config['threshold_configuration']
        
        # Fallback to environment variables
        return {
            'consensus_mapping': {
                'crisis_to_high': float(os.getenv('NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD', '0.25')),
                'crisis_to_medium': float(os.getenv('NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD', '0.15')),
                'mild_crisis_to_low': float(os.getenv('NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD', '0.10')),
                'negative_to_low': float(os.getenv('NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD', '0.55')),
                'unknown_to_low': float(os.getenv('NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD', '0.50'))
            },
            'ensemble_thresholds': {
                'high': float(os.getenv('NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD', '0.45')),
                'medium': float(os.getenv('NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD', '0.25')),
                'low': float(os.getenv('NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD', '0.12'))
            }
        }
    
    def get_hardware_configuration(self) -> Dict[str, Any]:
        """Get hardware configuration with environment overrides"""
        config = self.load_config_file('model_ensemble')
        
        if config and 'hardware_optimization' in config:
            hw_config = config['hardware_optimization']
        else:
            hw_config = {}
        
        # Apply environment overrides
        return {
            'device': os.getenv('NLP_DEVICE', hw_config.get('default_device', 'auto')),
            'precision': os.getenv('NLP_MODEL_PRECISION', hw_config.get('default_precision', 'float16')),
            'performance_settings': {
                'max_batch_size': int(os.getenv('NLP_MAX_BATCH_SIZE', '32')),
                'inference_threads': int(os.getenv('NLP_INFERENCE_THREADS', '16')),
                'max_concurrent_requests': int(os.getenv('NLP_MAX_CONCURRENT_REQUESTS', '20')),
                'request_timeout': int(os.getenv('NLP_REQUEST_TIMEOUT', '40'))
            },
            'memory_optimization': {
                'cache_dir': os.getenv('NLP_MODEL_CACHE_DIR', './models/cache')
            }
        }
    
    def get_feature_flags(self) -> Dict[str, Any]:
        """Get feature flags with environment overrides"""
        config = self.load_config_file('model_ensemble')
        
        if config and 'feature_flags' in config:
            flags = config['feature_flags']
        else:
            flags = {}
        
        return {
            'experimental_features': {
                'enable_ensemble_analysis': os.getenv('NLP_ENABLE_ENSEMBLE_ANALYSIS', 'true').lower() == 'true',
                'enable_gap_detection': os.getenv('NLP_ENABLE_GAP_DETECTION', 'true').lower() == 'true',
                'enable_confidence_spreading': os.getenv('NLP_ENABLE_CONFIDENCE_SPREADING', 'true').lower() == 'true',
                'log_model_disagreements': os.getenv('NLP_LOG_MODEL_DISAGREEMENTS', 'true').lower() == 'true'
            },
            'learning_system': {
                'enabled': os.getenv('GLOBAL_ENABLE_LEARNING_SYSTEM', 'true').lower() == 'true',
                'learning_rate': float(os.getenv('NLP_LEARNING_RATE', '0.1')),
                'max_adjustments_per_day': int(os.getenv('NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY', '50'))
            }
        }
    
    def get_ensemble_mode(self) -> str:
        """Get ensemble mode with environment override"""
        return os.getenv('NLP_ENSEMBLE_MODE', 'majority')
    
    def get_all_configuration(self) -> Dict[str, Any]:
        """Get complete configuration with all sections"""
        return {
            'models': self.get_model_configuration(),
            'thresholds': self.get_threshold_configuration(),
            'hardware': self.get_hardware_configuration(),
            'features': self.get_feature_flags(),
            'ensemble_mode': self.get_ensemble_mode()
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate configuration and return status"""
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            model_config = self.get_model_configuration()
            models = model_config.get('models', {})
            
            # Check model weights
            total_weight = sum(model.get('weight', 0) for model in models.values())
            if abs(total_weight - 1.0) > 0.001:
                validation_results['warnings'].append(f"Model weights sum to {total_weight}, should be 1.0")
            
            # Check required models
            required_models = ['depression', 'sentiment', 'emotional_distress']
            missing_models = [model for model in required_models if model not in models]
            if missing_models:
                validation_results['errors'].append(f"Missing required models: {missing_models}")
                validation_results['valid'] = False
            
            # Check model names are not empty
            for model_type, model_config in models.items():
                if not model_config.get('name'):
                    validation_results['errors'].append(f"Model {model_type} has no name specified")
                    validation_results['valid'] = False
        
        except Exception as e:
            validation_results['errors'].append(f"Configuration validation error: {e}")
            validation_results['valid'] = False
        
        return validation_results
    
    def clear_cache(self):
        """Clear configuration cache"""
        self.config_cache.clear()
        logger.info("🔄 Configuration cache cleared")
    
    def reload_configuration(self):
        """Reload all configuration from files"""
        self.clear_cache()
        logger.info("🔄 Configuration reloaded")


# Factory function for easy import
def create_config_manager(config_dir: str = "/app/config") -> ConfigManager:
    """Create and return a ConfigManager instance"""
    return ConfigManager(config_dir)