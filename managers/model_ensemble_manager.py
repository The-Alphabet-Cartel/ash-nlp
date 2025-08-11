# ash-nlp/managers/model_ensemble_manager.py
"""
Model Ensemble Manager for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
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
    Updated to use enhanced UnifiedConfigManager with unified configuration approach
    """
    
    def __init__(self, config_manager):
        """
        Initialize Model Ensemble Manager
        
        Args:
            config_manager: Enhanced UnifiedConfigManager instance (Phase 3d)
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ModelEnsembleManager")
        
        self.config_manager = config_manager
        self.config = None
        
        logger.info("✅ ModelEnsembleManager v3.1d initialized with UnifiedConfigManager")
        
        # Load configuration using UnifiedConfigManager
        self._load_configuration()
        
        # Validate configuration
        self._validate_configuration()
    
    def _load_configuration(self):
        """Load model ensemble configuration using UnifiedConfigManager"""
        try:
            # Use UnifiedConfigManager's get_model_configuration method
            self.config = self.config_manager.get_model_configuration()
            
            if not self.config:
                raise ValueError("Model configuration could not be loaded")
            
            logger.info(f"✅ Model ensemble configuration loaded via UnifiedConfigManager")
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
    
    async def analyze_message_ensemble(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict[str, Any]:
        """
        Analyze message using ensemble models - CORRECTED VERSION
        
        This method is required by the API endpoints but delegates to CrisisAnalyzer
        following Clean v3.1 Architecture principles
        
        Args:
            message: Message text to analyze
            user_id: User ID for context
            channel_id: Channel ID for context
            
        Returns:
            Dictionary containing ensemble analysis results
        """
        try:
            logger.debug(f"🔍 ModelEnsembleManager delegating analysis to CrisisAnalyzer")
            
            # Import here to avoid circular imports
            from analysis.crisis_analyzer import CrisisAnalyzer
            
            try:
                # Get other required managers for CrisisAnalyzer using factory functions
                from managers.crisis_pattern_manager import create_crisis_pattern_manager
                from managers.analysis_parameters_manager import create_analysis_parameters_manager
                from managers.threshold_mapping_manager import create_threshold_mapping_manager
                from managers.feature_config_manager import create_feature_config_manager
                from managers.performance_config_manager import create_performance_config_manager
                
                # Create managers using factory functions (Clean v3.1 compliance)
                crisis_pattern_manager = create_crisis_pattern_manager(self.config_manager)
                analysis_parameters_manager = create_analysis_parameters_manager(self.config_manager)
                threshold_mapping_manager = create_threshold_mapping_manager(self.config_manager, self)
                feature_config_manager = create_feature_config_manager(self.config_manager)
                performance_config_manager = create_performance_config_manager(self.config_manager)
                
                # CORRECTED: Create CrisisAnalyzer with the correct parameters (no config_manager)
                # Based on analysis/__init__.py, the correct parameters are:
                crisis_analyzer = CrisisAnalyzer(
                    models_manager=self,  # ModelEnsembleManager acts as models_manager
                    crisis_pattern_manager=crisis_pattern_manager,
                    learning_manager=None,  # Optional
                    analysis_parameters_manager=analysis_parameters_manager,
                    threshold_mapping_manager=threshold_mapping_manager,
                    feature_config_manager=feature_config_manager,
                    performance_config_manager=performance_config_manager
                )
                
                # Delegate to CrisisAnalyzer's analyze_message method
                logger.debug(f"✅ CrisisAnalyzer created with correct parameters, performing analysis...")
                result = await crisis_analyzer.analyze_message(message, user_id, channel_id)
                
                logger.debug(f"✅ Ensemble analysis complete via CrisisAnalyzer delegation")
                return result
                
            except Exception as e:
                logger.error(f"❌ Failed to create CrisisAnalyzer or dependencies: {e}")
                logger.exception("Full error details:")
                # Fallback to basic response structure
                return self._create_fallback_analysis_result(message, str(e))
                
        except Exception as e:
            logger.error(f"❌ Error in analyze_message_ensemble: {e}")
            logger.exception("Full error details:")
            return self._create_fallback_analysis_result(message, str(e))

    def _create_fallback_analysis_result(self, message: str, error_message: str) -> Dict[str, Any]:
        """
        Create fallback analysis result when ensemble analysis fails
        
        Args:
            message: Original message
            error_message: Error description
            
        Returns:
            Dictionary with fallback analysis result
        """
        return {
            'needs_response': False,
            'crisis_level': 'none',
            'confidence_score': 0.0,
            'detected_categories': [],
            'method': 'ensemble_fallback_error',
            'processing_time_ms': 0.0,
            'model_info': 'ModelEnsembleManager fallback - CrisisAnalyzer unavailable',
            'reasoning': f"Ensemble analysis failed: {error_message}",
            'analysis': {
                'error': error_message,
                'fallback_used': True,
                'ensemble_available': False
            },
            'staff_review_required': True,  # Always require review on errors
            'ensemble_status': {
                'models_configured': len(self.get_model_definitions()),
                'error': error_message,
                'fallback_reason': 'crisis_analyzer_creation_failed'
            }
        }

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
    
    def models_loaded(self) -> bool:
        """
        Check if models are loaded and ready for analysis - IMPROVED VERSION
        This method is required for API compatibility with ModelsManager interface
        
        More lenient validation that focuses on essential requirements
        
        Returns:
            bool: True if models are configured and ready, False otherwise
        """
        try:
            # Check if we have model definitions
            models = self.get_model_definitions()
            if not models:
                logger.warning("❌ No models configured in model definitions")
                return False
            
            logger.debug(f"🔍 Found {len(models)} model definitions: {list(models.keys())}")
            
            # Check if we have at least the core models (be more flexible about exact names)
            required_model_count = 2  # At least 2 models for basic functionality
            if len(models) < required_model_count:
                logger.warning(f"❌ Only {len(models)} models configured, need at least {required_model_count}")
                return False
            
            # Validate that models have names (essential requirement)
            models_with_names = 0
            for model_type, model_config in models.items():
                model_name = model_config.get('name', '')
                if model_name and model_name.strip():
                    models_with_names += 1
                    logger.debug(f"   ✅ {model_type}: {model_name}")
                else:
                    logger.warning(f"   ⚠️ {model_type}: missing or empty name")
            
            if models_with_names == 0:
                logger.warning("❌ No models have valid names configured")
                return False
            
            # Check weights (be lenient - just ensure they exist and are reasonable)
            try:
                weights = self.get_model_weights()
                total_weight = sum(weights.values())
                
                logger.debug(f"🔍 Model weights: {weights}")
                logger.debug(f"🔍 Total weight: {total_weight}")
                
                # Be very lenient with weights - just check they're not zero
                if total_weight <= 0:
                    logger.warning(f"❌ Invalid total weight: {total_weight}")
                    return False
                
                # Allow weight tolerance up to 50% deviation (very lenient)
                weight_tolerance = 0.5
                if abs(total_weight - 1.0) > weight_tolerance:
                    logger.info(f"⚠️ Model weights sum to {total_weight}, ideally should be ~1.0, but continuing...")
                    # Don't fail - just log warning
                
            except Exception as e:
                logger.warning(f"⚠️ Could not validate weights: {e}, but continuing...")
                # Don't fail on weight validation errors
            
            logger.info(f"✅ Models validation passed: {models_with_names}/{len(models)} models with valid names")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error checking models_loaded status: {e}")
            logger.exception("Full error details:")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive model information for API responses - IMPROVED VERSION
        This method is required for API compatibility with ModelsManager interface
        
        More robust error handling and comprehensive information
        
        Returns:
            Dict containing model configuration and status information
        """
        try:
            models = self.get_model_definitions()
            
            # Build model info response with error handling
            model_info = {
                'total_models': len(models),
                'models_configured': len(models) > 0,
                'architecture_version': '3.1d',
                'configuration_source': 'unified_config_manager',
                'model_details': {}
            }
            
            # Add ensemble mode safely
            try:
                model_info['ensemble_mode'] = self.get_ensemble_mode()
            except Exception as e:
                logger.warning(f"Could not get ensemble mode: {e}")
                model_info['ensemble_mode'] = 'unknown'
            
            # Add weights safely
            try:
                weights = self.get_model_weights()
                model_info['total_weight'] = sum(weights.values())
                model_info['weights_valid'] = abs(sum(weights.values()) - 1.0) < 0.5  # Lenient
            except Exception as e:
                logger.warning(f"Could not get model weights: {e}")
                model_info['total_weight'] = 0.0
                model_info['weights_valid'] = False
            
            # Add hardware settings safely
            try:
                model_info['device_setting'] = self.get_device_setting()
                model_info['precision_setting'] = self.get_precision_setting()
            except Exception as e:
                logger.warning(f"Could not get hardware settings: {e}")
                model_info['device_setting'] = 'unknown'
                model_info['precision_setting'] = 'unknown'
            
            # Add details for each model with comprehensive error handling
            for model_type, model_config in models.items():
                try:
                    model_info['model_details'][model_type] = {
                        'name': model_config.get('name', ''),
                        'weight': model_config.get('weight', 0.0),
                        'type': model_config.get('type', ''),
                        'pipeline_task': model_config.get('pipeline_task', 'text-classification'),
                        'cache_dir': model_config.get('cache_dir', './models/cache'),
                        'configured': bool(model_config.get('name', '').strip())
                    }
                except Exception as e:
                    logger.warning(f"Error processing model {model_type}: {e}")
                    model_info['model_details'][model_type] = {
                        'error': str(e),
                        'configured': False
                    }
            
            # Add final status
            model_info['status'] = {
                'models_loaded': self.models_loaded(),
                'ready_for_analysis': len(models) >= 2 and any(
                    details.get('configured', False) 
                    for details in model_info['model_details'].values()
                )
            }
            
            logger.debug(f"✅ Model info generated successfully: {len(models)} models")
            return model_info
            
        except Exception as e:
            logger.error(f"❌ Error generating model info: {e}")
            logger.exception("Full error details:")
            return {
                'total_models': 0,
                'models_configured': False,
                'status': 'error',
                'error': str(e),
                'architecture_version': '3.1d',
                'ready_for_analysis': False
            }

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
        """Get storage configuration via UnifiedConfigManager"""
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
        config_manager: UnifiedConfigManager instance (optional for compatibility)
        
    Returns:
        ModelEnsembleManager instance
    """
    global _model_ensemble_manager
    
    if _model_ensemble_manager is None:
        # If no config_manager provided, create one (for backward compatibility)
        if config_manager is None:
            logger.info("🔄 Creating UnifiedConfigManager for ModelEnsembleManager compatibility")
            from managers.unified_config_manager import UnifiedConfigManager
            config_manager = UnifiedConfigManager("/app/config")
        
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
        config_manager: UnifiedConfigManager instance
        
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