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
            'performance_settings': 'performance_settings.json',
            'threshold_mapping': 'threshold_mapping.json',
            'storage_settings': 'storage_settings.json',    # NEW in Phase 3d
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
        """Fallback storage configuration using Phase 3d unified environment variables"""
        logger.info("🔧 Using Phase 3d unified environment variables for storage configuration")
        
        return {
            'directories': {
                'data_directory': os.getenv('NLP_STORAGE_DATA_DIR', './data'),
                'models_directory': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'logs_directory': os.getenv('NLP_STORAGE_LOGS_DIR', './logs'),
                'learning_directory': os.getenv('NLP_STORAGE_LEARNING_DIR', './learning_data')
            },
            'file_paths': {
                'log_file': os.getenv('NLP_STORAGE_LOG_FILE', 'nlp_service.log'),
                'learning_persistence_file': os.getenv('NLP_STORAGE_LEARNING_FILE', './learning_data/adjustments.json')
            },
            'cache_settings': {
                'huggingface_cache': os.getenv('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'enable_model_caching': True
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