# ash/ash-nlp/managers/settings_manager.py
"""
Settings Manager for Ash NLP Service v3.1
Handles runtime settings and configuration overrides
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class SettingsManager:
    """Settings manager for runtime configuration and overrides"""
    
    def __init__(self, config_manager):
        """
        Initialize settings manager
        
        Args:
            config_manager: ConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("ConfigManager is required for SettingsManager")
        
        self.config_manager = config_manager
        self.runtime_settings = {}
        self.setting_overrides = {}
        
        logger.info("✅ SettingsManager initialized with ConfigManager integration")
        
        # Load initial settings
        self._load_initial_settings()
    
    def _load_initial_settings(self):
        """Load initial settings from configuration"""
        try:
            # Get hardware settings
            hardware_config = self.config_manager.get_hardware_configuration()
            self.runtime_settings['hardware'] = hardware_config
            
            # Get feature flags
            feature_flags = self.config_manager.get_feature_flags()
            self.runtime_settings['features'] = feature_flags
            
            # Get threshold settings
            threshold_config = self.config_manager.get_threshold_configuration()
            self.runtime_settings['thresholds'] = threshold_config
            
            logger.info("✅ Initial settings loaded from ConfigManager")
            
        except Exception as e:
            logger.error(f"❌ Failed to load initial settings: {e}")
            self.runtime_settings = {}
    
    def get_setting(self, setting_path: str, default: Any = None) -> Any:
        """
        Get a setting value using dot notation
        
        Args:
            setting_path: Dot-separated path to setting (e.g., 'hardware.device')
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
        try:
            # Check for runtime overrides first
            if setting_path in self.setting_overrides:
                return self.setting_overrides[setting_path]
            
            # Navigate through nested settings
            current = self.runtime_settings
            for part in setting_path.split('.'):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            
            return current
            
        except Exception as e:
            logger.warning(f"⚠️ Error accessing setting {setting_path}: {e}")
            return default
    
    def set_setting_override(self, setting_path: str, value: Any):
        """
        Set a runtime override for a setting
        
        Args:
            setting_path: Dot-separated path to setting
            value: New value to set
        """
        self.setting_overrides[setting_path] = value
        logger.info(f"🔄 Setting override: {setting_path} = {value}")
    
    def clear_setting_override(self, setting_path: str):
        """Clear a runtime setting override"""
        if setting_path in self.setting_overrides:
            del self.setting_overrides[setting_path]
            logger.info(f"🔄 Cleared setting override: {setting_path}")
    
    def get_hardware_settings(self) -> Dict[str, Any]:
        """Get hardware configuration settings"""
        return self.runtime_settings.get('hardware', {})
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance configuration settings"""
        hardware = self.get_hardware_settings()
        return hardware.get('performance_settings', {})
    
    def get_feature_settings(self) -> Dict[str, Any]:
        """Get feature flag settings"""
        return self.runtime_settings.get('features', {})
    
    def get_threshold_settings(self) -> Dict[str, Any]:
        """Get threshold configuration settings"""
        return self.runtime_settings.get('thresholds', {})
    
    def get_device_setting(self) -> str:
        """Get device setting"""
        return self.get_setting('hardware.device', 'auto')
    
    def get_precision_setting(self) -> str:
        """Get model precision setting"""
        return self.get_setting('hardware.precision', 'float16')
    
    def get_cache_dir_setting(self) -> str:
        """Get model cache directory setting"""
        return self.get_setting('hardware.memory_optimization.cache_dir', './models/cache')
    
    def get_learning_enabled_setting(self) -> bool:
        """Get learning system enabled setting"""
        return self.get_setting('features.learning_system.enabled', True)
    
    def get_gap_detection_enabled_setting(self) -> bool:
        """Get gap detection enabled setting"""
        return self.get_setting('features.experimental_features.enable_gap_detection', True)
    
    def get_ensemble_analysis_enabled_setting(self) -> bool:
        """Get ensemble analysis enabled setting"""
        return self.get_setting('features.experimental_features.enable_ensemble_analysis', True)
    
    def reload_settings(self):
        """Reload settings from ConfigManager"""
        logger.info("🔄 Reloading settings from ConfigManager...")
        self._load_initial_settings()
        logger.info("✅ Settings reloaded")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings including overrides"""
        result = self.runtime_settings.copy()
        
        # Apply overrides
        for path, value in self.setting_overrides.items():
            # Simple override application (doesn't handle nested paths)
            result[f"override_{path}"] = value
        
        return result
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings"""
        return {
            'device': self.get_device_setting(),
            'precision': self.get_precision_setting(),
            'cache_dir': self.get_cache_dir_setting(),
            'learning_enabled': self.get_learning_enabled_setting(),
            'gap_detection_enabled': self.get_gap_detection_enabled_setting(),
            'ensemble_analysis_enabled': self.get_ensemble_analysis_enabled_setting(),
            'active_overrides': len(self.setting_overrides),
            'total_settings_categories': len(self.runtime_settings)
        }
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate current settings"""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Validate device setting
            device = self.get_device_setting()
            if device not in ['auto', 'cpu', 'cuda']:
                validation_result['warnings'].append(f"Unusual device setting: {device}")
            
            # Validate precision setting
            precision = self.get_precision_setting()
            if precision not in ['float16', 'float32', 'auto']:
                validation_result['warnings'].append(f"Unusual precision setting: {precision}")
            
            # Validate cache directory exists
            cache_dir = self.get_cache_dir_setting()
            if not Path(cache_dir).exists():
                validation_result['warnings'].append(f"Cache directory does not exist: {cache_dir}")
            
        except Exception as e:
            validation_result['errors'].append(f"Settings validation error: {e}")
            validation_result['valid'] = False
        
        return validation_result


# Export for clean architecture
__all__ = [
    'SettingsManager',
    'create_settings_manager'
]