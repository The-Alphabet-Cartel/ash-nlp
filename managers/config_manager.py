# ash/ash-nlp/managers/config_manager.py (Phase 3a Enhanced)
"""
Enhanced Configuration Manager for Ash NLP Service v3.1 - Phase 3a Crisis Patterns Integration
Handles JSON configuration with environment variable overrides + Crisis Patterns
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
    """Enhanced configuration manager with JSON + environment variable support + Crisis Patterns (Phase 3a)"""
    
    def __init__(self, config_dir: str = "/app/config"):
        """
        Initialize configuration manager with crisis patterns support
        
        Args:
            config_dir: Directory containing JSON configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.crisis_patterns = {}  # Phase 3a: Crisis patterns storage
        self.env_override_pattern = re.compile(r'\$\{([^}]+)\}')
        
        # Configuration files to load (existing + crisis patterns)
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json',
            'analysis_parameters': 'analysis_parameters.json',
            'performance_settings': 'performance_settings.json',
            'threshold_mapping': 'threshold_mapping.json'
        }
        
        # Phase 3a: Crisis pattern files mapping
        self.crisis_pattern_files = {
            'lgbtqia_patterns': 'crisis_lgbtqia_patterns.json',
            'burden_patterns': 'crisis_burden_patterns.json',
            'hopelessness_patterns': 'crisis_hopelessness_patterns.json',
            'struggle_patterns': 'crisis_struggle_patterns.json',
            'idiom_patterns': 'crisis_idiom_patterns.json',
            'positive_context_patterns': 'crisis_positive_context_patterns.json',
            'context_patterns': 'crisis_context_patterns.json',
            'community_vocabulary': 'crisis_community_vocabulary.json',
            'temporal_patterns': 'crisis_temporal_patterns.json',
            'context_weights': 'crisis_context_weights.json',
            'negation_patterns': 'crisis_negation_patterns.json',
            'basic_idiom_patterns': 'basic_idiom_patterns.json'
        }
        
        logger.info(f"✅ ConfigManager initialized with config directory: {config_dir}")
        
        # Phase 3a: Load crisis patterns
        self._load_crisis_patterns()
        
        # DEBUG: Log key environment variables
        logger.debug("🔍 Key Environment Variables:")
        env_vars_to_check = [
            'NLP_DEPRESSION_MODEL',
            'NLP_SENTIMENT_MODEL', 
            'NLP_EMOTIONAL_DISTRESS_MODEL',
            'NLP_DEPRESSION_MODEL_WEIGHT',
            'NLP_SENTIMENT_MODEL_WEIGHT',
            'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT',
            'NLP_ENSEMBLE_MODE',
            # Phase 3a: Crisis pattern environment variables
            'NLP_CONFIG_ENABLE_LGBTQIA_PATTERNS',
            'NLP_CONFIG_ENABLE_BURDEN_PATTERNS',
            'NLP_CONFIG_ENABLE_IDIOM_FILTERING'
        ]
        
        for env_var in env_vars_to_check:
            value = os.getenv(env_var)
            logger.debug(f"   {env_var}: {value}")
    
    
    # ========================================================================
    # PHASE 3A: CRISIS PATTERNS LOADING METHODS
    # ========================================================================
    
    def _load_crisis_patterns(self):
        """Load all crisis pattern JSON files (Phase 3a)"""
        logger.info("🔍 Loading crisis patterns from JSON configuration files...")
        
        patterns_loaded = 0
        patterns_fallback = 0
        
        for pattern_type, filename in self.crisis_pattern_files.items():
            pattern_path = self.config_dir / filename
            
            if pattern_path.exists():
                try:
                    with open(pattern_path, 'r', encoding='utf-8') as f:
                        pattern_data = json.load(f)
                    
                    # Apply environment overrides to pattern configuration
                    pattern_data = self._apply_crisis_pattern_overrides(pattern_data, pattern_type)
                    
                    # Validate pattern structure
                    if self._validate_crisis_pattern_structure(pattern_data, pattern_type):
                        self.crisis_patterns[pattern_type] = pattern_data
                        patterns_loaded += 1
                        
                        # Log pattern summary
                        metadata = pattern_data.get('metadata', {})
                        total_patterns = metadata.get('total_patterns', 'unknown')
                        enabled = pattern_data.get('configuration', {}).get('enabled', True)
                        status = "✅ enabled" if enabled else "❌ disabled"
                        logger.debug(f"📋 Loaded {pattern_type}: {total_patterns} patterns ({status})")
                    else:
                        logger.error(f"❌ Invalid structure for {pattern_type}")
                        self._load_fallback_pattern(pattern_type)
                        patterns_fallback += 1
                        
                except Exception as e:
                    logger.error(f"❌ Failed to load {filename}: {e}")
                    self._load_fallback_pattern(pattern_type)
                    patterns_fallback += 1
            else:
                logger.warning(f"⚠️ Crisis pattern file not found: {filename}")
                self._load_fallback_pattern(pattern_type)
                patterns_fallback += 1
        
        total_files = len(self.crisis_pattern_files)
        logger.info(f"✅ Crisis patterns loaded: {patterns_loaded} JSON files, {patterns_fallback} fallbacks ({total_files} total)")
        
        if patterns_fallback > 0:
            logger.warning(f"⚠️ {patterns_fallback} crisis pattern types using fallback from settings_manager constants")
    
    def _apply_crisis_pattern_overrides(self, pattern_data: Dict, pattern_type: str) -> Dict:
        """Apply environment variable overrides to crisis pattern configuration"""
        metadata = pattern_data.get('metadata', {})
        env_overrides = metadata.get('environment_overrides', {})
        configuration = pattern_data.get('configuration', {})
        
        overrides_applied = 0
        
        for config_key, env_var in env_overrides.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert string to appropriate type
                converted_value = self._convert_env_value(env_value)
                
                # Apply override to configuration
                old_value = configuration.get(config_key, 'not_set')
                configuration[config_key] = converted_value
                overrides_applied += 1
                
                logger.debug(f"🔄 {pattern_type}.{config_key}: {old_value} → {converted_value} (from {env_var})")
        
        if overrides_applied > 0:
            pattern_data['configuration'] = configuration
            logger.debug(f"✅ Applied {overrides_applied} environment overrides to {pattern_type}")
        
        return pattern_data
    
    def _convert_env_value(self, env_value: str) -> Union[str, int, float, bool]:
        """Convert environment variable string to appropriate type"""
        # Boolean conversion
        if env_value.lower() in ('true', 'false'):
            return env_value.lower() == 'true'
        
        # Numeric conversion
        try:
            if '.' in env_value:
                return float(env_value)
            else:
                return int(env_value)
        except ValueError:
            # Return as string if conversion fails
            return env_value
    
    def _validate_crisis_pattern_structure(self, pattern_data: Dict, pattern_type: str) -> bool:
        """Validate the structure of a crisis pattern configuration"""
        required_keys = ['metadata', 'configuration', 'patterns']
        
        for key in required_keys:
            if key not in pattern_data:
                logger.error(f"❌ Missing required key '{key}' in {pattern_type}")
                return False
        
        # Validate metadata
        metadata = pattern_data['metadata']
        required_metadata = ['pattern_type', 'version', 'description']
        for key in required_metadata:
            if key not in metadata:
                logger.error(f"❌ Missing metadata key '{key}' in {pattern_type}")
                return False
        
        # Validate configuration
        configuration = pattern_data['configuration']
        if not isinstance(configuration.get('enabled'), bool):
            logger.warning(f"⚠️ Invalid 'enabled' value in {pattern_type} configuration")
        
        return True
    
    def _load_fallback_pattern(self, pattern_type: str):
        """Load fallback pattern from settings_manager constants"""
        logger.debug(f"🔄 Loading fallback for {pattern_type} from settings_manager constants")
        
        # Import here to avoid circular imports
        try:
            from managers.settings_manager import (
                LGBTQIA_PATTERNS, BURDEN_PATTERNS, HOPELESSNESS_PATTERNS, 
                STRUGGLE_PATTERNS, ENHANCED_IDIOM_PATTERNS, POSITIVE_CONTEXT_PATTERNS,
                CRISIS_CONTEXTS, COMMUNITY_VOCABULARY, TEMPORAL_INDICATORS,
                CONTEXT_WEIGHTS, NEGATION_PATTERNS, IDIOM_PATTERNS
            )
            
            fallback_mapping = {
                'lgbtqia_patterns': LGBTQIA_PATTERNS,
                'burden_patterns': BURDEN_PATTERNS,
                'hopelessness_patterns': HOPELESSNESS_PATTERNS,
                'struggle_patterns': STRUGGLE_PATTERNS,
                'idiom_patterns': ENHANCED_IDIOM_PATTERNS,
                'positive_context_patterns': POSITIVE_CONTEXT_PATTERNS,
                'context_patterns': CRISIS_CONTEXTS,
                'community_vocabulary': COMMUNITY_VOCABULARY,
                'temporal_patterns': TEMPORAL_INDICATORS,
                'context_weights': CONTEXT_WEIGHTS,
                'negation_patterns': NEGATION_PATTERNS,
                'basic_idiom_patterns': IDIOM_PATTERNS
            }
            
            if pattern_type in fallback_mapping:
                fallback_data = {
                    'metadata': {
                        'pattern_type': pattern_type,
                        'version': '3.1.0-fallback',
                        'description': f'Fallback {pattern_type} from settings_manager constants',
                        'source': 'settings_manager.py'
                    },
                    'configuration': {
                        'enabled': True,
                        'source': 'fallback'
                    },
                    'patterns': fallback_mapping[pattern_type]
                }
                
                self.crisis_patterns[pattern_type] = fallback_data
                logger.debug(f"✅ Loaded fallback for {pattern_type}")
            else:
                logger.warning(f"⚠️ No fallback available for {pattern_type}")
                
        except ImportError as e:
            logger.error(f"❌ Failed to import fallback patterns: {e}")
    
    # ========================================================================
    # PHASE 3A: CRISIS PATTERNS ACCESS METHODS
    # ========================================================================
    
    def get_crisis_patterns(self, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get crisis patterns (all or specific type)
        
        Args:
            pattern_type: Specific pattern type to retrieve, or None for all
            
        Returns:
            Dictionary of crisis patterns
        """
        if pattern_type:
            if pattern_type in self.crisis_patterns:
                pattern_data = self.crisis_patterns[pattern_type]
                
                # Check if pattern type is enabled
                enabled = pattern_data.get('configuration', {}).get('enabled', True)
                if not enabled:
                    logger.debug(f"🚫 Pattern type {pattern_type} is disabled")
                    return {}
                
                return pattern_data
            else:
                logger.warning(f"⚠️ Crisis pattern type not found: {pattern_type}")
                return {}
        
        # Return all enabled patterns
        enabled_patterns = {}
        for ptype, pdata in self.crisis_patterns.items():
            enabled = pdata.get('configuration', {}).get('enabled', True)
            if enabled:
                enabled_patterns[ptype] = pdata
        
        return enabled_patterns
    
    def get_crisis_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of loaded crisis patterns"""
        summary = {
            'total_pattern_types': len(self.crisis_patterns),
            'enabled_patterns': 0,
            'disabled_patterns': 0,
            'fallback_patterns': 0,
            'json_patterns': 0,
            'pattern_details': {}
        }
        
        for pattern_type, pattern_data in self.crisis_patterns.items():
            config = pattern_data.get('configuration', {})
            metadata = pattern_data.get('metadata', {})
            
            enabled = config.get('enabled', True)
            source = metadata.get('source', 'unknown')
            total_patterns = metadata.get('total_patterns', 'unknown')
            
            if enabled:
                summary['enabled_patterns'] += 1
            else:
                summary['disabled_patterns'] += 1
            
            if 'fallback' in metadata.get('version', ''):
                summary['fallback_patterns'] += 1
            else:
                summary['json_patterns'] += 1
            
            summary['pattern_details'][pattern_type] = {
                'enabled': enabled,
                'source': source,
                'total_patterns': total_patterns,
                'version': metadata.get('version', 'unknown')
            }
        
        return summary
    
    def validate_crisis_patterns(self) -> Dict[str, Any]:
        """Validate all crisis patterns and return status"""
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'pattern_results': {}
        }
        
        for pattern_type, pattern_data in self.crisis_patterns.items():
            pattern_valid = True
            pattern_warnings = []
            pattern_errors = []
            
            # Check if enabled
            enabled = pattern_data.get('configuration', {}).get('enabled', True)
            if not enabled:
                pattern_warnings.append(f"Pattern type {pattern_type} is disabled")
            
            # Check structure
            if not self._validate_crisis_pattern_structure(pattern_data, pattern_type):
                pattern_errors.append(f"Invalid structure for {pattern_type}")
                pattern_valid = False
            
            # Check patterns content
            patterns = pattern_data.get('patterns', {})
            if not patterns:
                pattern_warnings.append(f"No patterns defined for {pattern_type}")
            
            validation_results['pattern_results'][pattern_type] = {
                'valid': pattern_valid,
                'warnings': pattern_warnings,
                'errors': pattern_errors
            }
            
            if pattern_errors:
                validation_results['errors'].extend(pattern_errors)
                validation_results['valid'] = False
            
            if pattern_warnings:
                validation_results['warnings'].extend(pattern_warnings)
        
    
    # ========================================================================
    # EXISTING METHODS FROM ORIGINAL ConfigManager (PRESERVED)
    # ========================================================================
    
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
            
            # DEBUG: Log before substitution
            model_defs = raw_config.get('model_definitions', {})
            logger.debug("🔍 Model definitions BEFORE substitution:")
            for model_type, model_config in model_defs.items():
                logger.debug(f"   {model_type}: {model_config.get('name', 'NO_NAME')}")
            
            # Substitute environment variables
            logger.debug("🔄 Starting environment variable substitution...")
            processed_config = self.substitute_environment_variables(raw_config)
            
            # DEBUG: Log after substitution
            processed_model_defs = processed_config.get('model_definitions', {})
            logger.debug("🔍 Model definitions AFTER substitution:")
            for model_type, model_config in processed_model_defs.items():
                logger.debug(f"   {model_type}: {model_config.get('name', 'NO_NAME')}")
            
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
        logger.debug("🔍 Getting model configuration...")
        
        config = self.load_config_file('model_ensemble')
        
        if not config:
            logger.warning("⚠️ Model ensemble configuration not found, using environment fallback")
            return self._get_fallback_model_config()
        
        # Extract and process model definitions
        model_defs = config.get('model_definitions', {})
        processed_models = {}
        
        logger.debug("🔧 Processing model definitions...")
        
        for model_type, model_config in model_defs.items():
            logger.debug(f"🔍 Processing {model_type} model...")
            
            # Get model name with environment override
            env_var = model_config.get('environment_variable')
            logger.debug(f"   Environment variable: {env_var}")
            
            if env_var and os.getenv(env_var):
                model_name = os.getenv(env_var)
                logger.debug(f"🔄 Environment override for {model_type}: {model_name}")
            else:
                model_name = model_config.get('name', model_config.get('default_name', ''))
                logger.debug(f"   Using config/default name: {model_name}")
            
            # Get weight with environment override
            weight_str = str(model_config.get('weight', model_config.get('default_weight', 0.33)))
            logger.debug(f"   Weight string: {weight_str}")
            
            try:
                weight = float(weight_str)
                logger.debug(f"   Weight value: {weight}")
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
            
            logger.debug(f"✅ Processed {model_type}: {model_name} (weight: {weight})")
        
        # Validate weights sum to 1.0
        total_weight = sum(model['weight'] for model in processed_models.values())
        logger.debug(f"🔍 Total weight: {total_weight}")
        
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
        
        logger.debug("✅ Model configuration processing complete")
        return result
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Fallback configuration using only environment variables"""
        logger.debug("🔄 Using fallback environment configuration")
        
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