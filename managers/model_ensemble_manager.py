# ash/ash-nlp/managers/model_ensemble_manager.py - Phase 3d Updated
"""
Model Ensemble Manager for Ash NLP Service v3.1d - Updated for Standardized Variables
Phase 3d: Uses enhanced ConfigManager with standardized variable naming

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
"""

import os
import json
import logging
import re
from typing import Dict, Any, List, Union, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelEnsembleManager:
    """
    Model Ensemble Manager with Phase 3d standardized variable support
    Updated to use enhanced ConfigManager with unified configuration approach
    """
    
    def __init__(self, config_manager):
        """
        Initialize Model Ensemble Manager
        
        Args:
            config_manager: Enhanced ConfigManager instance (Phase 3d)
        """
        if config_manager is None:
            raise ValueError("ConfigManager is required for ModelEnsembleManager")
        
        self.config_manager = config_manager
        self.config = None
        
        logger.info("✅ ModelEnsembleManager v3.1d initialized with enhanced ConfigManager")
        
        # Load configuration using enhanced ConfigManager
        self._load_configuration()
        
        # Validate configuration
        self._validate_configuration()
    
    def _load_configuration(self):
        """Load model ensemble configuration using enhanced ConfigManager"""
        try:
            # Use enhanced ConfigManager's get_model_configuration method
            self.config = self.config_manager.get_model_configuration()
            
            if not self.config:
                raise ValueError("Model configuration could not be loaded")
            
            logger.info(f"✅ Model ensemble configuration loaded via enhanced ConfigManager")
            logger.debug(f"🔍 Loaded {len(self.config.get('models', {}))} model definitions")
            
            # Log standardized variables being used
            models = self.config.get('models', {})
            for model_type, model_config in models.items():
                logger.debug(f"   {model_type}: {model_config.get('name')} (weight: {model_config.get('weight')})")
        
        except Exception as e:
            logger.error(f"❌ Failed to load model configuration: {e}")
            raise
    
def _validate_configuration(self):
        """Validate model ensemble configuration with Phase 3d standards"""
        try:
            models = self.config.get('models', {})
            
            if not models:
                raise ValueError("No model definitions found")
            
            # Validate required models
            required_models = ['depression', 'sentiment', 'emotional_distress']
            for model_type in required_models:
                if model_type not in models:
                    raise ValueError(f"Required model '{model_type}' not found in configuration")
            
            # DEBUG: Log weight types and values before validation
            logger.debug("🔍 Debugging weight types before validation:")
            for model_type, model_config in models.items():
                weight_value = model_config.get('weight', 0)
                logger.debug(f"   {model_type}: weight={weight_value} (type: {type(weight_value)})")
            
            # Validate model weights sum to approximately 1.0 with explicit type conversion
            weights = []
            for model_type, model_config in models.items():
                weight_value = model_config.get('weight', 0)
                try:
                    # Explicit type conversion to handle string weights from JSON
                    if isinstance(weight_value, str):
                        weight_float = float(weight_value)
                        logger.debug(f"🔧 Converted string weight '{weight_value}' to float {weight_float} for {model_type}")
                    elif isinstance(weight_value, (int, float)):
                        weight_float = float(weight_value)
                    else:
                        logger.warning(f"⚠️ Unexpected weight type {type(weight_value)} for {model_type}, using 0.0")
                        weight_float = 0.0
                    weights.append(weight_float)
                except (ValueError, TypeError) as e:
                    logger.error(f"❌ Could not convert weight '{weight_value}' to float for {model_type}: {e}")
                    raise ValueError(f"Invalid weight value for {model_type}: {weight_value}")
            
            total_weight = sum(weights)
            weight_tolerance = self.config.get('validation', {}).get('weight_tolerance', 0.01)
            
            logger.debug(f"🔍 Total weight calculated: {total_weight}")
            
            if abs(total_weight - 1.0) > weight_tolerance:
                logger.warning(f"⚠️ Model weights sum to {total_weight}, should be ~1.0 (tolerance: {weight_tolerance})")
                if self.config.get('validation', {}).get('fail_on_invalid_weights', False):
                    raise ValueError(f"Model weights sum to {total_weight}, must be ~1.0")
            
            # Validate model names are not empty
            for model_type, model_config in models.items():
                if not model_config.get('name'):
                    raise ValueError(f"Model '{model_type}' has empty name")
            
            logger.info("✅ Model ensemble configuration validation passed")
            
        except Exception as e:
            logger.error(f"❌ Model configuration validation failed: {e}")
            raise
        
    # ========================================================================
    # Model Configuration Access - Phase 3d Enhanced
    # ========================================================================
    
    def get_model_definitions(self) -> Dict[str, Any]:
        """Get all model definitions with standardized variable support"""
        return self.config.get('models', {})
    
    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get configuration for specific model type"""
        models = self.get_model_definitions()
        return models.get(model_type, {})
    
    def get_model_name(self, model_type: str) -> str:
        """Get model name for specific model type"""
        model_config = self.get_model_config(model_type)
        return model_config.get('name', '')
    
    def get_model_weight(self, model_type: str) -> float:
        """Get model weight for specific model type"""
        model_config = self.get_model_config(model_type)
        return model_config.get('weight', 0.0)
    
    def get_model_cache_dir(self, model_type: str) -> str:
        """Get cache directory for specific model type"""
        model_config = self.get_model_config(model_type)
        return model_config.get('cache_dir', './models/cache')
    
    def get_model_pipeline_task(self, model_type: str) -> str:
        """Get pipeline task for specific model type"""
        model_config = self.get_model_config(model_type)
        return model_config.get('pipeline_task', 'text-classification')
    
    # ========================================================================
    # Ensemble Configuration - Phase 3d Enhanced  
    # ========================================================================
    
    def get_ensemble_mode(self) -> str:
        """Get current ensemble mode"""
        return self.config.get('ensemble_mode', 'consensus')
    
    def get_ensemble_settings(self) -> Dict[str, Any]:
        """Get ensemble settings including validation and performance"""
        return {
            'mode': self.get_ensemble_mode(),
            'validation': self.config.get('validation', {}),
            'performance': self.config.get('performance', {})
        }
    
    def get_current_ensemble_mode(self) -> str:
        """Get the currently configured ensemble mode - alias for compatibility"""
        return self.get_ensemble_mode()
    
    # ========================================================================
    # Hardware Configuration - Phase 3d Enhanced
    # ========================================================================
    
    def get_hardware_settings(self) -> Dict[str, Any]:
        """Get hardware configuration settings"""
        return self.config.get('hardware_settings', {})
    
    def get_device_setting(self) -> str:
        """Get device setting (auto/cpu/cuda)"""
        hardware = self.get_hardware_settings()
        return hardware.get('device', 'auto')
    
    def get_precision_setting(self) -> str:
        """Get precision setting (float16/float32)"""
        hardware = self.get_hardware_settings()
        return hardware.get('precision', 'float16')
    
    def get_max_batch_size(self) -> int:
        """Get maximum batch size"""
        hardware = self.get_hardware_settings()
        return hardware.get('max_batch_size', 32)
    
    def get_inference_threads(self) -> int:
        """Get inference thread count"""
        hardware = self.get_hardware_settings()
        return hardware.get('inference_threads', 16)
    
    # ========================================================================
    # Model Weight Management - Phase 3d Enhanced
    # ========================================================================
    
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
    
    # ========================================================================
    # Validation and Utility Methods - Phase 3d Enhanced
    # ========================================================================
    
    def validate_ensemble_mode(self, mode: str) -> bool:
        """Validate if an ensemble mode is supported"""
        available_modes = ['consensus', 'majority', 'weighted']
        return mode in available_modes
    
    def get_model_names(self) -> List[str]:
        """Get list of configured model names"""
        return list(self.get_model_definitions().keys())
    
    def get_validation_settings(self) -> Dict[str, Any]:
        """Get validation settings"""
        return self.config.get('validation', {})
    
    def is_weights_validation_enabled(self) -> bool:
        """Check if weight validation is enabled"""
        validation = self.get_validation_settings()
        return validation.get('ensure_weights_sum_to_one', True)
    
    def should_fail_on_invalid_weights(self) -> bool:
        """Check if system should fail on invalid weights"""
        validation = self.get_validation_settings()
        return validation.get('fail_on_invalid_weights', True)
    
    # ========================================================================
    # Storage Configuration - Phase 3d Enhanced  
    # ========================================================================
    
    def get_storage_configuration(self) -> Dict[str, Any]:
        """Get storage configuration via enhanced ConfigManager"""
        try:
            return self.config_manager.get_storage_configuration()
        except Exception as e:
            logger.warning(f"⚠️ Could not get storage configuration: {e}")
            return {
                'directories': {
                    'models_directory': './models/cache'
                }
            }
    
    def get_models_directory(self) -> str:
        """Get models directory from storage configuration"""
        storage_config = self.get_storage_configuration()
        directories = storage_config.get('directories', {})
        return directories.get('models_directory', './models/cache')
    
    # ========================================================================
    # Status and Information Methods - Phase 3d Enhanced
    # ========================================================================
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status"""
        try:
            models = self.get_model_definitions()
            weights = self.get_model_weights()
            
            return {
                'version': '3.1d-enhanced',
                'architecture': 'clean-v3.1-unified',
                'config_source': 'enhanced_config_manager',
                'ensemble_mode': self.get_ensemble_mode(),
                'models_configured': len(models),
                'model_types': list(models.keys()),
                'total_weight': sum(weights.values()),
                'weights_normalized': abs(sum(weights.values()) - 1.0) < 0.01,
                'hardware_device': self.get_device_setting(),
                'storage_directory': self.get_models_directory(),
                'validation_enabled': self.is_weights_validation_enabled()
            }
        except Exception as e:
            logger.error(f"❌ Error getting manager status: {e}")
            return {
                'version': '3.1d-enhanced',
                'status': 'error',
                'error': str(e)
            }
    
    def print_configuration_summary(self):
        """Print detailed configuration summary for debugging"""
        logger.info("=== ModelEnsembleManager v3.1d Configuration Summary ===")
        
        status = self.get_manager_status()
        for key, value in status.items():
            logger.info(f"{key}: {value}")
        
        logger.info("--- Model Details ---")
        models = self.get_model_definitions()
        for model_type, model_config in models.items():
            logger.info(f"{model_type}:")
            logger.info(f"  Name: {model_config.get('name')}")
            logger.info(f"  Weight: {model_config.get('weight')}")
            logger.info(f"  Type: {model_config.get('type')}")
            logger.info(f"  Pipeline Task: {model_config.get('pipeline_task')}")
        
        logger.info("=== End Configuration Summary ===")

# ============================================================================
# Global Instance Management - Singleton Pattern
# ============================================================================

_model_ensemble_manager = None

def get_model_ensemble_manager(config_manager=None) -> ModelEnsembleManager:
    """
    Get the global model ensemble manager instance - TRANSITION COMPATIBLE
    
    Args:
        config_manager: Enhanced ConfigManager instance (optional for compatibility)
        
    Returns:
        ModelEnsembleManager instance
    """
    global _model_ensemble_manager
    
    if _model_ensemble_manager is None:
        # If no config_manager provided, create one (for backward compatibility)
        if config_manager is None:
            logger.info("🔄 Creating ConfigManager for ModelEnsembleManager compatibility")
            from managers.config_manager import ConfigManager
            config_manager = ConfigManager("/app/config")
        
        _model_ensemble_manager = ModelEnsembleManager(config_manager)
    
    return _model_ensemble_manager

def reset_model_ensemble_manager():
    """Reset the global manager instance - for testing"""
    global _model_ensemble_manager
    _model_ensemble_manager = None

# ============================================================================
# Factory Function - Clean v3.1 Architecture Compliance
# ============================================================================

def create_model_ensemble_manager(config_manager) -> ModelEnsembleManager:
    """
    Factory function to create ModelEnsembleManager instance
    
    Args:
        config_manager: Enhanced ConfigManager instance
        
    Returns:
        ModelEnsembleManager instance
    """
    return ModelEnsembleManager(config_manager)

__all__ = [
    'ModelEnsembleManager', 
    'get_model_ensemble_manager', 
    'create_model_ensemble_manager',
    'reset_model_ensemble_manager'
]

logger.info("✅ Enhanced ModelEnsembleManager v3.1d loaded - Phase 3d standardized variables supported")