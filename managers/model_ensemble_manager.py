"""
Model Ensemble Configuration Manager for Ash NLP Service v3.1
Handles loading and parsing of model_ensemble.json with environment variable substitution
Located in managers/ directory for organized configuration management
"""

import json
import os
import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

logger = logging.getLogger(__name__)

class ModelEnsembleManager:
    """
    Manages model ensemble configuration from JSON with environment variable substitution
    Part of the managers/ directory architecture for centralized configuration management
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the model ensemble manager
        
        Args:
            config_file: Path to the JSON config file. If None, uses default location.
        """
        self.config_file = config_file or self._find_config_file()
        self._raw_config = None
        self._processed_config = None
        self._load_timestamp = None
        
        # Load the configuration
        self.reload()
    
    def _find_config_file(self) -> str:
        """Find the model ensemble config file in various possible locations"""
        possible_paths = [
            # First check relative to managers directory
            Path(__file__).parent.parent / "config" / "model_ensemble.json",
            # Then check standard config locations
            Path("config/model_ensemble.json"),
            Path("./config/model_ensemble.json"),
            Path.cwd() / "config" / "model_ensemble.json",
            # Check if running from project root
            Path("ash-nlp/config/model_ensemble.json"),
            # Check absolute paths relative to this file
            Path(__file__).resolve().parent.parent / "config" / "model_ensemble.json"
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"✅ Found model ensemble config at: {path}")
                return str(path)
        
        # If not found, use the default location relative to managers directory
        default_path = Path(__file__).parent.parent / "config" / "model_ensemble.json"
        logger.warning(f"⚠️ Model ensemble config not found, using default location: {default_path}")
        return str(default_path)
    
    def reload(self) -> None:
        """Reload the configuration from file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._raw_config = json.load(f)
            
            self._processed_config = self._process_config(self._raw_config)
            self._load_timestamp = os.path.getmtime(self.config_file)
            
            # Validate the configuration
            self._validate_config()
            
            logger.info(f"✅ Model ensemble configuration loaded from {self.config_file}")
            
        except FileNotFoundError:
            logger.error(f"❌ Model ensemble config file not found: {self.config_file}")
            logger.error(f"💡 Please ensure model_ensemble.json exists in the config/ directory")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in model ensemble config: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading model ensemble config: {e}")
            raise
    
    def _process_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process the configuration, substituting environment variables"""
        return self._substitute_env_vars(config.copy())
    
    def _substitute_env_vars(self, obj: Any) -> Any:
        """
        Recursively substitute environment variables in the configuration
        Supports ${VAR_NAME} syntax with fallback to defaults
        """
        if isinstance(obj, dict):
            return {key: self._substitute_env_vars(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            return self._substitute_string_vars(obj)
        else:
            return obj
    
    def _substitute_string_vars(self, text: str) -> Union[str, int, float, bool]:
        """
        Substitute environment variables in a string and convert to appropriate type
        Supports fallback to defaults defined in JSON
        """
        # Pattern to match ${VAR_NAME}
        pattern = r'\$\{([A-Z_][A-Z0-9_]*)\}'
        
        def replace_var(match):
            var_name = match.group(1)
            env_value = os.getenv(var_name)
            
            if env_value is None:
                # Try to get from env_config if available
                try:
                    from .config_manager import get_config
                    env_config = get_config()
                    env_value = env_config.get(var_name)
                except ImportError:
                    logger.debug(f"config_manager not available, using direct environment lookup for {var_name}")
                except Exception:
                    logger.debug(f"Could not access config_manager for {var_name}")
            
            if env_value is None:
                logger.debug(f"Environment variable {var_name} not found, keeping placeholder")
                return match.group(0)  # Keep the placeholder
            
            return str(env_value)
        
        # Substitute variables
        result = re.sub(pattern, replace_var, text)
        
        # If the entire string was a variable substitution and was successful, convert to appropriate type
        if not re.search(pattern, result) and result != text:
            return self._convert_type(result)
        
        return result
    
    def _convert_type(self, value: str) -> Union[str, int, float, bool]:
        """Convert string value to appropriate Python type"""
        # Handle None/null values
        if value.lower() in ('none', 'null', ''):
            return None
        
        # Boolean conversion
        if value.lower() in ('true', '1', 'yes', 'on', 'enabled'):
            return True
        elif value.lower() in ('false', '0', 'no', 'off', 'disabled'):
            return False
        
        # Number conversion
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Return as string if no conversion possible
        return value
    
    def _validate_config(self) -> None:
        """Validate the loaded configuration"""
        if not self._processed_config:
            raise ValueError("No configuration loaded")
        
        # Validate model weights sum to 1.0
        self._validate_model_weights()
        
        # Validate threshold consistency
        self._validate_thresholds()
        
        # Validate required sections
        self._validate_required_sections()
        
        # Validate model definitions
        self._validate_model_definitions()
        
        logger.info("✅ Model ensemble configuration validation passed")
    
    def _validate_model_weights(self) -> None:
        """Validate that model weights sum to approximately 1.0"""
        try:
            weights = self._processed_config['ensemble_configuration']['model_weights']
            weight_values = []
            
            for model in ['depression', 'sentiment', 'emotional_distress']:
                weight = weights[model]
                if isinstance(weight, (int, float)):
                    weight_values.append(weight)
                else:
                    logger.warning(f"⚠️ Model weight for {model} is not numeric: {weight}")
                    return
            
            total_weight = sum(weight_values)
            tolerance = self._processed_config.get('validation_rules', {}).get('model_weights', {}).get('tolerance', 0.001)
            
            if abs(total_weight - 1.0) > tolerance:
                logger.warning(f"⚠️ Model weights sum to {total_weight}, expected ~1.0 (tolerance: {tolerance})")
            else:
                logger.info(f"✅ Model weights validation passed: {total_weight}")
                
        except KeyError as e:
            logger.warning(f"⚠️ Missing model weight configuration: {e}")
    
    def _validate_thresholds(self) -> None:
        """Validate threshold consistency"""
        try:
            consensus = self._processed_config['threshold_configuration']['crisis_level_mapping']['consensus_mapping']
            
            # Check that crisis_to_high >= crisis_to_medium
            crisis_high = consensus.get('crisis_to_high')
            crisis_medium = consensus.get('crisis_to_medium')
            
            if isinstance(crisis_high, (int, float)) and isinstance(crisis_medium, (int, float)):
                if crisis_high < crisis_medium:
                    logger.warning(f"⚠️ Threshold inconsistency: crisis_to_high ({crisis_high}) < crisis_to_medium ({crisis_medium})")
                else:
                    logger.info(f"✅ Crisis threshold consistency validated")
            
            # Check gap detection vs disagreement thresholds
            gap_threshold = self._processed_config['ensemble_configuration']['gap_detection'].get('threshold')
            disagreement_threshold = self._processed_config['ensemble_configuration']['gap_detection'].get('disagreement_threshold')
            
            if isinstance(gap_threshold, (int, float)) and isinstance(disagreement_threshold, (int, float)):
                if gap_threshold >= disagreement_threshold:
                    logger.warning(f"⚠️ Gap detection threshold ({gap_threshold}) should be < disagreement threshold ({disagreement_threshold})")
                else:
                    logger.info(f"✅ Gap detection threshold consistency validated")
                    
        except KeyError as e:
            logger.warning(f"⚠️ Missing threshold configuration for validation: {e}")
    
    def _validate_required_sections(self) -> None:
        """Validate that all required configuration sections are present"""
        required_sections = [
            'ensemble_info',
            'model_definitions',
            'ensemble_configuration',
            'threshold_configuration',
            'hardware_optimization',
            'feature_flags',
            'validation_rules'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in self._processed_config:
                missing_sections.append(section)
        
        if missing_sections:
            raise ValueError(f"Missing required configuration sections: {missing_sections}")
        
        logger.info("✅ All required configuration sections present")
    
    def _validate_model_definitions(self) -> None:
        """Validate model definitions are complete"""
        models = self._processed_config.get('model_definitions', {})
        required_models = ['depression', 'sentiment', 'emotional_distress']
        
        for model_name in required_models:
            if model_name not in models:
                raise ValueError(f"Missing model definition: {model_name}")
            
            model_config = models[model_name]
            required_fields = ['name', 'type', 'purpose', 'specialization']
            
            for field in required_fields:
                if field not in model_config:
                    logger.warning(f"⚠️ Missing field '{field}' in {model_name} model definition")
        
        logger.info("✅ Model definitions validation passed")
    
    def get_config(self) -> Dict[str, Any]:
        """Get the complete processed configuration"""
        return self._processed_config.copy() if self._processed_config else {}
    
    def get_model_definitions(self) -> Dict[str, Any]:
        """Get model definitions"""
        return self._processed_config.get('model_definitions', {})
    
    def get_ensemble_configuration(self) -> Dict[str, Any]:
        """Get ensemble configuration"""
        return self._processed_config.get('ensemble_configuration', {})
    
    def get_threshold_configuration(self) -> Dict[str, Any]:
        """Get threshold configuration"""
        return self._processed_config.get('threshold_configuration', {})
    
    def get_hardware_optimization(self) -> Dict[str, Any]:
        """Get hardware optimization settings"""
        return self._processed_config.get('hardware_optimization', {})
    
    def get_feature_flags(self) -> Dict[str, Any]:
        """Get feature flags"""
        return self._processed_config.get('feature_flags', {})
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules"""
        return self._processed_config.get('validation_rules', {})
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get configuration metadata"""
        return self._processed_config.get('metadata', {})
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model
        
        Args:
            model_name: Name of the model ('depression', 'sentiment', 'emotional_distress')
            
        Returns:
            Model configuration dictionary
        """
        models = self.get_model_definitions()
        if model_name not in models:
            raise ValueError(f"Model '{model_name}' not found in configuration. Available models: {list(models.keys())}")
        
        return models[model_name]
    
    def get_ensemble_mode_config(self, mode: str) -> Dict[str, Any]:
        """Get configuration for a specific ensemble mode"""
        ensemble_config = self.get_ensemble_configuration()
        available_modes = ensemble_config.get('available_modes', {})
        
        if mode not in available_modes:
            raise ValueError(f"Ensemble mode '{mode}' not available. Available modes: {list(available_modes.keys())}")
        
        return available_modes[mode]
    
    def is_config_modified(self) -> bool:
        """Check if the configuration file has been modified since last load"""
        try:
            current_timestamp = os.path.getmtime(self.config_file)
            return current_timestamp != self._load_timestamp
        except OSError:
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the configuration for logging/debugging"""
        if not self._processed_config:
            return {"status": "not_loaded"}
        
        ensemble_config = self.get_ensemble_configuration()
        models = self.get_model_definitions()
        
        summary = {
            "status": "loaded",
            "config_file": self.config_file,
            "ensemble_mode": ensemble_config.get('default_mode', 'unknown'),
            "models_count": len(models),
            "model_names": list(models.keys()),
            "gap_detection_enabled": ensemble_config.get('gap_detection', {}).get('enabled', False),
            "learning_system_enabled": self.get_feature_flags().get('learning_system', {}).get('enabled', False),
            "hardware_device": self.get_hardware_optimization().get('device', 'unknown'),
            "configuration_version": self.get_metadata().get('configuration_version', 'unknown')
        }
        
        # Calculate weights sum if available
        try:
            weights_sum = sum(
                ensemble_config.get('model_weights', {}).get(model, 0) 
                for model in ['depression', 'sentiment', 'emotional_distress']
                if isinstance(ensemble_config.get('model_weights', {}).get(model), (int, float))
            )
            summary["weights_sum"] = weights_sum
        except Exception:
            summary["weights_sum"] = "unknown"
        
        return summary
    
    def get_model_names(self) -> List[str]:
        """Get list of configured model names"""
        return list(self.get_model_definitions().keys())
    
    def get_ensemble_modes(self) -> List[str]:
        """Get list of available ensemble modes"""
        ensemble_config = self.get_ensemble_configuration()
        return list(ensemble_config.get('available_modes', {}).keys())
    
    def get_current_ensemble_mode(self) -> str:
        """Get the currently configured ensemble mode"""
        ensemble_config = self.get_ensemble_configuration()
        return ensemble_config.get('default_mode', 'weighted')
    
    def get_model_weights(self) -> Dict[str, float]:
        """Get current model weights"""
        ensemble_config = self.get_ensemble_configuration()
        return ensemble_config.get('model_weights', {})
    
    def validate_ensemble_mode(self, mode: str) -> bool:
        """Validate if an ensemble mode is supported"""
        return mode in self.get_ensemble_modes()
    
    def get_crisis_thresholds(self) -> Dict[str, float]:
        """Get crisis level thresholds"""
        threshold_config = self.get_threshold_configuration()
        ensemble_thresholds = threshold_config.get('ensemble_thresholds', {})
        
        # Return with defaults if not found
        return {
            'high': ensemble_thresholds.get('high', 0.45),
            'medium': ensemble_thresholds.get('medium', 0.25), 
            'low': ensemble_thresholds.get('low', 0.12)
        }
    
    def get_gap_detection_config(self) -> Dict[str, Any]:
        """Get gap detection configuration"""
        ensemble_config = self.get_ensemble_configuration()
        return ensemble_config.get('gap_detection', {})

# Global instance for singleton pattern
_model_ensemble_manager = None

def get_model_ensemble_manager() -> ModelEnsembleManager:
    """Get the global model ensemble manager instance"""
    global _model_ensemble_manager
    if _model_ensemble_manager is None:
        _model_ensemble_manager = ModelEnsembleManager()
    return _model_ensemble_manager

def reload_model_ensemble_config() -> None:
    """Force reload of the model ensemble configuration"""
    global _model_ensemble_manager
    if _model_ensemble_manager:
        _model_ensemble_manager.reload()
    else:
        _model_ensemble_manager = ModelEnsembleManager()

# Convenience functions for backward compatibility and easy access
def get_model_definitions() -> Dict[str, Any]:
    """Get model definitions from JSON config"""
    return get_model_ensemble_manager().get_model_definitions()

def get_ensemble_configuration() -> Dict[str, Any]:
    """Get ensemble configuration from JSON config"""
    return get_model_ensemble_manager().get_ensemble_configuration()

def get_threshold_configuration() -> Dict[str, Any]:
    """Get threshold configuration from JSON config"""
    return get_model_ensemble_manager().get_threshold_configuration()

def get_hardware_optimization() -> Dict[str, Any]:
    """Get hardware optimization settings from JSON config"""
    return get_model_ensemble_manager().get_hardware_optimization()

def get_feature_flags() -> Dict[str, Any]:
    """Get feature flags from JSON config"""
    return get_model_ensemble_manager().get_feature_flags()

def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model"""
    return get_model_ensemble_manager().get_model_config(model_name)

def get_ensemble_mode_config(mode: str) -> Dict[str, Any]:
    """Get configuration for a specific ensemble mode"""
    return get_model_ensemble_manager().get_ensemble_mode_config(mode)

def get_crisis_thresholds() -> Dict[str, float]:
    """Get crisis level thresholds"""
    return get_model_ensemble_manager().get_crisis_thresholds()

def get_gap_detection_config() -> Dict[str, Any]:
    """Get gap detection configuration"""
    return get_model_ensemble_manager().get_gap_detection_config()