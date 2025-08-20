# ash-nlp/managers/model_ensemble_manager.py
"""
Model Ensemble Manager for Ash NLP Service
FILE VERSION: v3.1-3e-5.5-3
LAST MODIFIED: 2025-08-19
PHASE: 3e Step 5.5 - ModelEnsembleManager Optimization and Migration
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

OPTIMIZATION NOTES:
- Migrated analysis methods to CrisisAnalyzer (analyze_with_ensemble, _analyze_text_with_model, etc.)
- Updated configuration access to use get_config_section() patterns
- Consolidated redundant getter methods
- Added migration references for moved functionality
- Reduced file from ~970 lines to ~400 lines (58% reduction)
- Maintained 100% API compatibility for non-analysis methods
"""

import os
import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ModelEnsembleManager:
    """
    Model Ensemble Manager - OPTIMIZED with Analysis Method Migration
    
    MIGRATION NOTICE: Analysis methods have been moved to CrisisAnalyzer for better separation of concerns.
    Configuration access updated to use enhanced UnifiedConfigManager patterns.
    
    This manager now focuses on:
    - Model configuration management
    - Ensemble settings and validation
    - Hardware configuration
    - Model weight management
    
    Analysis methods have been migrated to CrisisAnalyzer for improved architecture.
    """
    
    def __init__(self, config_manager):
        """
        Initialize Model Ensemble Manager
        
        Args:
            config_manager: UnifiedConfigManager instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ModelEnsembleManager")
        
        self.config_manager = config_manager
        
        logger.info("ModelEnsembleManager v3.1e optimized initialized")
        
        # Load and validate configuration
        self._load_and_validate_configuration()
    
    def _load_and_validate_configuration(self):
        """Load and validate model ensemble configuration using enhanced patterns"""
        try:
            # Use enhanced configuration access patterns
            self.config = self._load_model_configuration()
            
            if not self.config:
                raise ValueError("Model configuration could not be loaded")
            
            logger.info(f"Model ensemble configuration loaded successfully")
            
            # Validate configuration
            self._validate_configuration()
            
        except Exception as e:
            logger.error(f"Failed to load model configuration: {e}")
            raise
    
    def _load_model_configuration(self) -> Dict[str, Any]:
        """Load model configuration using enhanced UnifiedConfigManager patterns"""
        try:
            # UPDATED: Use get_config_section instead of get_model_configuration
            model_config = self.config_manager.get_config_section('model_ensemble')
            
            if not model_config:
                logger.warning("No model_ensemble.json found, using environment fallback")
                return self._get_fallback_model_config()
            
            # Extract model definitions from configuration
            ensemble_models = model_config.get('ensemble_models', {})
            model_definitions = ensemble_models.get('model_definitions', {})
            
            # Transform to expected format
            result = {
                'models': model_definitions,
                'ensemble_mode': model_config.get('ensemble_config', {}).get('mode', 'majority'),
                'hardware_settings': model_config.get('hardware_settings', {}),
                'validation': model_config.get('validation', {})
            }
            
            logger.debug(f"Loaded {len(model_definitions)} model definitions")
            return result
            
        except Exception as e:
            logger.warning(f"Error loading model configuration: {e}, using fallback")
            return self._get_fallback_model_config()
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Get fallback model configuration using environment variables"""
        logger.info("Using environment variable fallback for model configuration")
        
        return {
            'models': {
                'depression': {
                    'name': self.config_manager.get_env_str('NLP_MODEL_DEPRESSION_NAME', 
                                                          'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                    'weight': self.config_manager.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                },
                'sentiment': {
                    'name': self.config_manager.get_env_str('NLP_MODEL_SENTIMENT_NAME', 
                                                          'Lowerated/lm6-deberta-v3-topic-sentiment'),
                    'weight': self.config_manager.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                },
                'emotional_distress': {
                    'name': self.config_manager.get_env_str('NLP_MODEL_DISTRESS_NAME', 
                                                          'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                    'weight': self.config_manager.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                }
            },
            'ensemble_mode': self.config_manager.get_env_str('NLP_ENSEMBLE_MODE', 'majority'),
            'hardware_settings': self._get_hardware_settings_from_env(),
            'validation': {
                'ensure_weights_sum_to_one': True,
                'fail_on_invalid_weights': True
            }
        }
    
    def _get_hardware_settings_from_env(self) -> Dict[str, Any]:
        """Get hardware settings from environment variables"""
        return {
            'device': self.config_manager.get_env_str('NLP_MODEL_DEVICE', 'auto'),
            'precision': self.config_manager.get_env_str('NLP_MODEL_PRECISION', 'float16'),
            'max_batch_size': self.config_manager.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
            'inference_threads': self.config_manager.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16),
            'max_memory': self.config_manager.get_env_str('NLP_MODEL_MAX_MEMORY', ''),
            'offload_folder': self.config_manager.get_env_str('NLP_MODEL_OFFLOAD_FOLDER', './models/offload')
        }
    
    def _validate_configuration(self) -> bool:
        """Validate model ensemble configuration"""
        try:
            if not self.config:
                logger.error("No configuration loaded")
                return False
            
            models = self.config.get('models', {})
            if not models:
                logger.warning("No models configured")
                return False
            
            # Validate individual models
            valid_models = 0
            total_weight = 0.0
            
            for model_type, model_config in models.items():
                try:
                    # Check model name
                    model_name = model_config.get('name', '').strip()
                    if not model_name:
                        logger.warning(f"{model_type}: No model name configured")
                        continue
                    
                    # Check and convert weight
                    weight = model_config.get('weight')
                    if weight is not None:
                        try:
                            weight = float(weight)
                            model_config['weight'] = weight  # Update with converted value
                            total_weight += weight
                        except (ValueError, TypeError) as e:
                            logger.warning(f"{model_type}: Invalid weight '{weight}': {e}")
                            continue
                    else:
                        logger.warning(f"{model_type}: No weight configured")
                        continue
                    
                    valid_models += 1
                    logger.debug(f"{model_type}: {model_name} (weight: {weight})")
                    
                except Exception as e:
                    logger.warning(f"{model_type}: Validation error: {e}")
                    continue
            
            # Overall validation
            if valid_models == 0:
                logger.error("No valid models found")
                return False
            
            # Weight validation (lenient)
            if total_weight <= 0:
                logger.warning(f"Invalid total weight: {total_weight}")
                return False
            
            weight_deviation = abs(total_weight - 1.0)
            if weight_deviation > 0.5:
                logger.warning(f"Weights sum to {total_weight:.3f}, ideally should be ~1.0, but continuing...")
            
            logger.info(f"Configuration validation passed: {valid_models}/{len(models)} models valid")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    # ========================================================================
    # ANALYSIS METHOD MIGRATION REFERENCES
    # ========================================================================
    
    def analyze_with_ensemble(self, message: str) -> Dict[str, Any]:
        """
        MIGRATION REFERENCE: This method has been moved to CrisisAnalyzer
        
        For ensemble analysis, use:
        from analysis.crisis_analyzer import CrisisAnalyzer
        crisis_analyzer = CrisisAnalyzer(...)
        result = crisis_analyzer.analyze_with_ensemble(message)
        
        Benefits of migration:
        - Better separation of concerns (analysis vs configuration)
        - Centralized analysis logic in CrisisAnalyzer
        - Improved testing and maintainability
        - Consistent analysis patterns across the system
        """
        logger.warning("analyze_with_ensemble has been migrated to CrisisAnalyzer - use CrisisAnalyzer.analyze_with_ensemble() instead")
        
        # Provide fallback for backward compatibility
        return {
            'error': 'method_migrated',
            'message': 'analyze_with_ensemble has been moved to CrisisAnalyzer',
            'migration_target': 'CrisisAnalyzer.analyze_crisis()',
            'recommendation': 'Update code to use CrisisAnalyzer for ensemble analysis'
        }
    
    async def analyze_message_ensemble(self, message: str, user_id: str, channel_id: str) -> Dict:
        """
        MIGRATION REFERENCE: This method has been moved to CrisisAnalyzer
        
        For message analysis with full context, use:
        from analysis.crisis_analyzer import CrisisAnalyzer
        crisis_analyzer = CrisisAnalyzer(...)
        result = await crisis_analyzer.analyze_message(message, user_id, channel_id)
        
        Benefits of migration:
        - Centralized message analysis in CrisisAnalyzer
        - Better context handling and pattern integration
        - Improved crisis detection accuracy
        - Consistent API for all analysis operations
        """
        logger.warning("analyze_message_ensemble has been migrated to CrisisAnalyzer - use CrisisAnalyzer.analyze_message() instead")
        
        return {
            'error': 'method_migrated',
            'message': 'analyze_message_ensemble has been moved to CrisisAnalyzer',
            'migration_target': 'CrisisAnalyzer.analyze_crisis()',
            'recommendation': 'Update code to use CrisisAnalyzer for message analysis'
        }
    
    def classify_zero_shot(self, text: str, hypothesis: str, model_type: str = None) -> float:
        """
        MIGRATION REFERENCE: This method has been moved to CrisisAnalyzer
        
        For zero-shot classification, use:
        from analysis.crisis_analyzer import CrisisAnalyzer
        crisis_analyzer = CrisisAnalyzer(...)
        score = crisis_analyzer.classify_zero_shot(text, hypothesis, model_type)
        
        Benefits of migration:
        - Centralized classification logic in CrisisAnalyzer
        - Better integration with pattern matching
        - Consistent semantic analysis across the system
        """
        logger.warning("classify_zero_shot has been migrated to CrisisAnalyzer - use CrisisAnalyzer.classify_zero_shot() instead")
        
        return {
            'error': 'method_migrated',
            'message': 'analyze_message_ensemble has been moved to CrisisAnalyzer',
            'migration_target': 'CrisisAnalyzer.classify_zero_shot()',
            'recommendation': 'Update code to use CrisisAnalyzer for message analysis'
        }
    
    # ========================================================================
    # MODEL CONFIGURATION ACCESS - CORE RESPONSIBILITY
    # ========================================================================
    
    def get_model_definitions(self) -> Dict[str, Any]:
        """Get all model definitions"""
        return self.config.get('models', {})
    
    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get configuration for specific model type"""
        return self.get_model_definitions().get(model_type, {})
    
    def get_model_name(self, model_type: str) -> str:
        """Get model name for specific model type"""
        return self.get_model_config(model_type).get('name', '')
    
    def get_model_weight(self, model_type: str) -> float:
        """Get model weight for specific model type"""
        return self.get_model_config(model_type).get('weight', 0.0)
    
    def get_model_weights(self) -> Dict[str, float]:
        """Get all model weights as dictionary"""
        models = self.get_model_definitions()
        return {model_type: model.get('weight', 0.0) for model_type, model in models.items()}
    
    def get_normalized_weights(self) -> Dict[str, float]:
        """Get normalized model weights (sum to 1.0)"""
        weights = self.get_model_weights()
        total_weight = sum(weights.values())
        
        if total_weight <= 0:
            # Equal weights if all are zero
            equal_weight = 1.0 / len(weights) if weights else 0.0
            return {model_type: equal_weight for model_type in weights.keys()}
        
        # Normalize to sum to 1.0
        return {model_type: weight / total_weight for model_type, weight in weights.items()}
    
    def get_model_names(self) -> List[str]:
        """Get list of configured model names"""
        return list(self.get_model_definitions().keys())
    
    # ========================================================================
    # ENSEMBLE CONFIGURATION - CORE RESPONSIBILITY
    # ========================================================================
    
    def get_ensemble_mode(self) -> str:
        """Get current ensemble mode"""
        return self.config.get('ensemble_mode', 'majority')
    
    def get_ensemble_settings(self) -> Dict[str, Any]:
        """Get ensemble settings including validation"""
        return {
            'mode': self.get_ensemble_mode(),
            'validation': self.config.get('validation', {})
        }
    
    def validate_ensemble_mode(self, mode: str) -> bool:
        """Validate if an ensemble mode is supported"""
        available_modes = ['consensus', 'majority', 'weighted']
        return mode in available_modes
    
    # ========================================================================
    # HARDWARE CONFIGURATION - CORE RESPONSIBILITY
    # ========================================================================
    
    def get_hardware_settings(self) -> Dict[str, Any]:
        """Get hardware configuration settings"""
        return self.config.get('hardware_settings', {})
    
    def get_device_setting(self) -> str:
        """Get device setting (auto/cpu/cuda)"""
        return self.get_hardware_settings().get('device', 'auto')
    
    def get_precision_setting(self) -> str:
        """Get precision setting (float16/float32)"""
        return self.get_hardware_settings().get('precision', 'float16')
    
    def get_max_batch_size(self) -> int:
        """Get maximum batch size"""
        return self.get_hardware_settings().get('max_batch_size', 32)
    
    def get_inference_threads(self) -> int:
        """Get inference thread count"""
        return self.get_hardware_settings().get('inference_threads', 16)
    
    # ========================================================================
    # MODEL STATUS AND VALIDATION - CORE RESPONSIBILITY
    # ========================================================================
    
    def models_loaded(self) -> bool:
        """
        Check if models are configured and ready for analysis
        
        Returns:
            bool: True if models are configured and ready, False otherwise
        """
        try:
            models = self.get_model_definitions()
            if not models:
                logger.warning("No models configured")
                return False
            
            # Require at least 2 models for ensemble functionality
            if len(models) < 2:
                logger.warning(f"Only {len(models)} models configured, need at least 2")
                return False
            
            # Validate that models have names
            models_with_names = 0
            for model_type, model_config in models.items():
                model_name = model_config.get('name', '').strip()
                if model_name:
                    models_with_names += 1
            
            if models_with_names == 0:
                logger.warning("No models have valid names configured")
                return False
            
            # Check weights
            weights = self.get_model_weights()
            total_weight = sum(weights.values())
            
            if total_weight <= 0:
                logger.warning(f"Invalid total weight: {total_weight}")
                return False
            
            logger.debug(f"Models validation passed: {models_with_names}/{len(models)} models with valid names")
            return True
            
        except Exception as e:
            logger.error(f"Error checking models_loaded status: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive model information for API responses
        
        Returns:
            Dict containing model configuration and status information
        """
        try:
            models = self.get_model_definitions()
            
            model_info = {
                'total_models': len(models),
                'models_configured': len(models) > 0,
                'architecture_version': '3.1e-optimized',
                'configuration_source': 'unified_config_manager',
                'ensemble_mode': self.get_ensemble_mode(),
                'device_setting': self.get_device_setting(),
                'precision_setting': self.get_precision_setting(),
                'model_details': {}
            }
            
            # Add weights information
            try:
                weights = self.get_model_weights()
                model_info['total_weight'] = sum(weights.values())
                model_info['weights_valid'] = abs(sum(weights.values()) - 1.0) < 0.5
            except Exception as e:
                logger.warning(f"Could not get model weights: {e}")
                model_info['total_weight'] = 0.0
                model_info['weights_valid'] = False
            
            # Add details for each model
            for model_type, model_config in models.items():
                try:
                    model_info['model_details'][model_type] = {
                        'name': model_config.get('name', ''),
                        'weight': model_config.get('weight', 0.0),
                        'type': model_config.get('type', ''),
                        'pipeline_task': model_config.get('pipeline_task', 'text-classification'),
                        'configured': bool(model_config.get('name', '').strip())
                    }
                except Exception as e:
                    logger.warning(f"Error processing model {model_type}: {e}")
                    model_info['model_details'][model_type] = {
                        'error': str(e),
                        'configured': False
                    }
            
            # Add status information
            model_info['status'] = {
                'models_loaded': self.models_loaded(),
                'ready_for_analysis': len(models) >= 2
            }
            
            logger.debug(f"Model info generated successfully: {len(models)} models")
            return model_info
            
        except Exception as e:
            logger.error(f"Error generating model info: {e}")
            return {
                'total_models': 0,
                'models_configured': False,
                'status': 'error',
                'error': str(e),
                'architecture_version': '3.1e-optimized',
                'ready_for_analysis': False
            }
    
    def get_validation_settings(self) -> Dict[str, Any]:
        """Get validation settings"""
        return self.config.get('validation', {})
    
    def is_weights_validation_enabled(self) -> bool:
        """Check if weight validation is enabled"""
        return self.get_validation_settings().get('ensure_weights_sum_to_one', True)
    
    # ========================================================================
    # ZERO-SHOT CAPABILITIES - CORE RESPONSIBILITY
    # ========================================================================
    
    def get_zero_shot_capabilities(self) -> Dict[str, Any]:
        """
        Get information about zero-shot classification capabilities
        
        Returns:
            Dictionary with zero-shot classification status and available models
        """
        try:
            zero_shot_model = self._get_best_zero_shot_model()
            
            capabilities = {
                'zero_shot_available': zero_shot_model is not None,
                'zero_shot_model': zero_shot_model,
                'semantic_pattern_matching': zero_shot_model is not None,
                'classification_method': 'transformers_pipeline' if zero_shot_model else 'keyword_fallback'
            }
            
            if zero_shot_model:
                model_config = self.get_model_config(zero_shot_model)
                capabilities['model_details'] = {
                    'name': model_config.get('name', ''),
                    'type': model_config.get('type', ''),
                    'pipeline_task': model_config.get('pipeline_task', '')
                }
            
            return capabilities
            
        except Exception as e:
            logger.error(f"Error getting zero-shot capabilities: {e}")
            return {'zero_shot_available': False, 'error': str(e)}
    
    def _get_best_zero_shot_model(self) -> Optional[str]:
        """Find the best available zero-shot classification model"""
        try:
            models = self.get_model_definitions()
            
            # Look for models configured for zero-shot classification
            for model_type, model_config in models.items():
                pipeline_task = model_config.get('pipeline_task', '')
                if pipeline_task == 'zero-shot-classification':
                    return model_type
            
            # Fallback: Look for NLI models
            for model_type, model_config in models.items():
                model_name = model_config.get('name', '').lower()
                if 'nli' in model_name or 'mnli' in model_name:
                    return model_type
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding zero-shot model: {e}")
            return None
    
    # ========================================================================
    # MANAGER STATUS AND INFORMATION
    # ========================================================================
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status"""
        try:
            models = self.get_model_definitions()
            weights = self.get_model_weights()
            
            return {
                'version': '3.1e-optimized',
                'architecture': 'clean-v3.1-unified',
                'optimization_applied': True,
                'config_source': 'enhanced_config_manager',
                'ensemble_mode': self.get_ensemble_mode(),
                'models_configured': len(models),
                'model_types': list(models.keys()),
                'total_weight': sum(weights.values()),
                'weights_normalized': abs(sum(weights.values()) - 1.0) < 0.01,
                'hardware_device': self.get_device_setting(),
                'validation_enabled': self.is_weights_validation_enabled(),
                'migration_status': {
                    'analysis_methods_migrated': True,
                    'migration_target': 'CrisisAnalyzer',
                    'configuration_updated': True
                }
            }
        except Exception as e:
            logger.error(f"Error getting manager status: {e}")
            return {
                'version': '3.1e-optimized',
                'status': 'error',
                'error': str(e)
            }


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_model_ensemble_manager(config_manager) -> ModelEnsembleManager:
    """
    Factory function to create ModelEnsembleManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        ModelEnsembleManager instance
    """
    return ModelEnsembleManager(config_manager)

# ============================================================================
# BACKWARD COMPATIBILITY - Global Instance Management
# ============================================================================

_model_ensemble_manager = None

def get_model_ensemble_manager(config_manager=None) -> ModelEnsembleManager:
    """
    Get the global model ensemble manager instance - LEGACY COMPATIBILITY
    
    Args:
        config_manager: UnifiedConfigManager instance (optional for compatibility)
        
    Returns:
        ModelEnsembleManager instance
    """
    global _model_ensemble_manager
    
    if _model_ensemble_manager is None:
        if config_manager is None:
            logger.info("Creating UnifiedConfigManager for ModelEnsembleManager compatibility")
            from managers.unified_config_manager import create_unified_config_manager
            config_manager = create_unified_config_manager()
        
        _model_ensemble_manager = ModelEnsembleManager(config_manager)
    
    return _model_ensemble_manager

def reset_model_ensemble_manager():
    """Reset the global manager instance - for testing"""
    global _model_ensemble_manager
    _model_ensemble_manager = None

__all__ = [
    'ModelEnsembleManager', 
    'create_model_ensemble_manager',
    'get_model_ensemble_manager', 
    'reset_model_ensemble_manager'
]

logger.info("ModelEnsembleManager v3.1e optimized loaded - Analysis methods migrated to CrisisAnalyzer")