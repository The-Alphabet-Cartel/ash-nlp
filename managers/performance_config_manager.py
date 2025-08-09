# ash-nlp/managers/performance_config_manager.py - PHASE 3D STEP 7 COMPLETE
"""
Performance Configuration Manager for Ash NLP Service v3.1d - Phase 3d Step 7 Complete
Comprehensive performance settings management system with Clean v3.1 architecture

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import re
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceConfigManager:
    """
    Performance Configuration Manager for Ash NLP Service v3.1d - Phase 3d Step 7 Complete
    
    Manages performance settings for crisis analysis system components with comprehensive validation and profile management.
    Implements Clean v3.1 architecture patterns with dependency injection and fail-fast validation.
    
    Features:
    - Analysis performance settings
    - Server performance configuration  
    - Model performance optimization
    - Rate limiting settings
    - Cache performance management
    - Performance profile management
    """
    
    def __init__(self, config_manager):
        """
        Initialize PerformanceConfigManager with dependency injection
        
        Args:
            config_manager: ConfigManager instance for accessing configuration
        """
        self.config_manager = config_manager
        self.config_cache = {}
        self.validation_errors = []
        
        logger.info("⚡ Initializing PerformanceConfigManager (Phase 3d Step 7)")
        
        try:
            self._load_performance_configuration()
            self._validate_performance_settings()
            logger.info("✅ PerformanceConfigManager initialization complete")
        except Exception as e:
            logger.error(f"❌ PerformanceConfigManager initialization failed: {e}")
            raise
    
    def _load_performance_configuration(self):
        """Load performance settings configuration from JSON with environment overrides"""
        try:
            # Load performance settings configuration through ConfigManager using correct method
            performance_config_raw = self.config_manager.load_config_file('performance_settings')
            
            if not performance_config_raw:
                logger.error("❌ Could not load performance_settings.json configuration")
                raise ValueError("Performance settings configuration not available")
            
            # Extract performance settings configuration
            if 'performance_settings' in performance_config_raw:
                self.config_cache = performance_config_raw['performance_settings']
            else:
                # Direct configuration format
                self.config_cache = performance_config_raw
                
            logger.debug("✅ Performance settings configuration loaded successfully")
            logger.debug(f"🔍 Configuration keys loaded: {list(self.config_cache.keys())}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load performance settings configuration: {e}")
            # Initialize with safe defaults to prevent system failure
            self.config_cache = {
                'analysis_performance': {
                    'defaults': {
                        'analysis_timeout_ms': 5000,
                        'analysis_max_concurrent': 10,
                        'analysis_cache_ttl': 300,
                        'request_timeout': 40
                    }
                },
                'server_performance': {
                    'defaults': {
                        'max_concurrent_requests': 100,
                        'worker_timeout': 60,
                        'keepalive_timeout': 5
                    }
                },
                'model_performance': {
                    'defaults': {
                        'max_batch_size': 32,
                        'inference_threads': 16,
                        'model_precision': 'float16',
                        'device': 'auto'
                    }
                },
                'cache_performance': {
                    'defaults': {
                        'model_cache_size_limit': '2GB',
                        'analysis_cache_size_limit': '1GB',
                        'cache_expiry_hours': 24
                    }
                }
            }
            logger.warning("⚠️ Using fallback performance settings configuration")
            raise
    
    def _validate_performance_settings(self):
        """Validate performance settings for consistency and ranges"""
        try:
            # Validate analysis performance settings
            analysis_settings = self.get_analysis_performance_settings()
            if analysis_settings['analysis_timeout_ms'] < 1000:
                self.validation_errors.append("Analysis timeout too low (minimum 1000ms)")
            if analysis_settings['analysis_max_concurrent'] < 1:
                self.validation_errors.append("Max concurrent analyses must be at least 1")
            
            # Validate server performance settings
            server_settings = self.get_server_performance_settings()
            if server_settings['max_concurrent_requests'] < 1:
                self.validation_errors.append("Max concurrent requests must be at least 1")
            
            # Validate model performance settings
            model_settings = self.get_model_performance_settings()
            if model_settings['max_batch_size'] < 1:
                self.validation_errors.append("Max batch size must be at least 1")
                
            if self.validation_errors:
                logger.warning(f"⚠️ Performance validation found {len(self.validation_errors)} issues")
            else:
                logger.debug("✅ Performance settings validation passed")
                
        except Exception as e:
            logger.warning(f"⚠️ Error during performance settings validation: {e}")
    
    # ========================================================================
    # ANALYSIS PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_analysis_timeout(self) -> float:
        """Get analysis timeout in seconds"""
        timeout_ms = self._get_performance_setting('analysis_performance', 'analysis_timeout_ms', 5000, int)
        return timeout_ms / 1000.0  # Convert to seconds
    
    def get_analysis_timeout_ms(self) -> int:
        """Get analysis timeout in milliseconds"""
        return self._get_performance_setting('analysis_performance', 'analysis_timeout_ms', 5000, int)
    
    def get_analysis_max_concurrent(self) -> int:
        """Get maximum concurrent analyses"""
        return self._get_performance_setting('analysis_performance', 'analysis_max_concurrent', 10, int)
    
    def get_analysis_cache_ttl(self) -> int:
        """Get analysis cache TTL in seconds"""
        return self._get_performance_setting('analysis_performance', 'analysis_cache_ttl', 300, int)
    
    def get_request_timeout(self) -> float:
        """Get request timeout in seconds"""
        return float(self._get_performance_setting('analysis_performance', 'request_timeout', 40, int))
    
    def get_analysis_performance_settings(self) -> Dict[str, Any]:
        """Get all analysis performance settings"""
        return {
            'analysis_timeout_ms': self.get_analysis_timeout_ms(),
            'analysis_max_concurrent': self.get_analysis_max_concurrent(),
            'analysis_cache_ttl': self.get_analysis_cache_ttl(),
            'request_timeout': self.get_request_timeout()
        }
    
    # ========================================================================
    # SERVER PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_max_concurrent_requests(self) -> int:
        """Get maximum concurrent server requests"""
        return self._get_performance_setting('server_performance', 'max_concurrent_requests', 100, int)
    
    def get_worker_timeout(self) -> int:
        """Get worker timeout in seconds"""
        return self._get_performance_setting('server_performance', 'worker_timeout', 60, int)
    
    def get_keepalive_timeout(self) -> int:
        """Get keepalive timeout in seconds"""
        return self._get_performance_setting('server_performance', 'keepalive_timeout', 5, int)
    
    def get_server_performance_settings(self) -> Dict[str, Any]:
        """Get all server performance settings"""
        return {
            'max_concurrent_requests': self.get_max_concurrent_requests(),
            'worker_timeout': self.get_worker_timeout(),
            'keepalive_timeout': self.get_keepalive_timeout(),
            'workers': self.get_workers()  # ADD THIS LINE
        }
    
    def get_workers(self) -> int:
        """Get number of server workers"""
        return self._get_performance_setting('server_performance', 'workers', 1, int)

    # ========================================================================
    # MODEL PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_max_batch_size(self) -> int:
        """Get maximum model batch size"""
        return self._get_performance_setting('model_performance', 'max_batch_size', 32, int)
    
    def get_inference_threads(self) -> int:
        """Get number of inference threads"""
        return self._get_performance_setting('model_performance', 'inference_threads', 16, int)
    
    def get_model_precision(self) -> str:
        """Get model precision setting"""
        return self._get_performance_setting('model_performance', 'model_precision', 'float16', str)
    
    def get_device(self) -> str:
        """Get device setting for model inference"""
        return self._get_performance_setting('model_performance', 'device', 'auto', str)
    
    def get_max_memory(self) -> Optional[str]:
        """Get maximum memory limit"""
        return self._get_performance_setting('model_performance', 'max_memory', None, str)
    
    def get_offload_folder(self) -> Optional[str]:
        """Get offload folder for model weights"""
        return self._get_performance_setting('model_performance', 'offload_folder', None, str)
    
    def get_model_performance_settings(self) -> Dict[str, Any]:
        """Get all model performance settings"""
        return {
            'max_batch_size': self.get_max_batch_size(),
            'inference_threads': self.get_inference_threads(),
            'model_precision': self.get_model_precision(),
            'device': self.get_device(),
            'max_memory': self.get_max_memory(),
            'offload_folder': self.get_offload_folder()
        }
    
    # ========================================================================
    # RATE LIMITING PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_rate_limit_requests_per_minute(self) -> int:
        """Get rate limit requests per minute"""
        return self._get_performance_setting('rate_limiting_performance', 'requests_per_minute', 1000, int)
    
    def get_rate_limit_burst_size(self) -> int:
        """Get rate limit burst size"""
        return self._get_performance_setting('rate_limiting_performance', 'burst_size', 50, int)
    
    def get_rate_limit_per_user_per_minute(self) -> int:
        """Get rate limit per user per minute"""
        return self._get_performance_setting('rate_limiting_performance', 'per_user_per_minute', 100, int)
    
    def get_rate_limiting_performance_settings(self) -> Dict[str, Any]:
        """Get all rate limiting performance settings"""
        return {
            'requests_per_minute': self.get_rate_limit_requests_per_minute(),
            'burst_size': self.get_rate_limit_burst_size(),
            'per_user_per_minute': self.get_rate_limit_per_user_per_minute()
        }
    
    # ========================================================================
    # CACHE PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_model_cache_size_limit(self) -> str:
        """Get model cache size limit"""
        return self._get_performance_setting('cache_performance', 'model_cache_size_limit', '2GB', str)
    
    def get_analysis_cache_size_limit(self) -> str:
        """Get analysis cache size limit"""
        return self._get_performance_setting('cache_performance', 'analysis_cache_size_limit', '1GB', str)
    
    def get_cache_expiry_hours(self) -> int:
        """Get cache expiry in hours"""
        return self._get_performance_setting('cache_performance', 'cache_expiry_hours', 24, int)
    
    def get_cache_settings(self) -> Dict[str, Any]:
        """Get comprehensive cache settings"""
        return {
            'enabled': True,  # Cache always enabled for performance
            'ttl': self.get_analysis_cache_ttl(),
            'model_cache_limit': self.get_model_cache_size_limit(),
            'analysis_cache_limit': self.get_analysis_cache_size_limit(),
            'expiry_hours': self.get_cache_expiry_hours()
        }
    
    def get_cache_performance_settings(self) -> Dict[str, Any]:
        """Get all cache performance settings"""
        return {
            'model_cache_size_limit': self.get_model_cache_size_limit(),
            'analysis_cache_size_limit': self.get_analysis_cache_size_limit(),
            'cache_expiry_hours': self.get_cache_expiry_hours()
        }
    
    # ========================================================================
    # OPTIMIZATION SETTINGS
    # ========================================================================
    
    def get_optimization_settings(self) -> Dict[str, Any]:
        """Get performance optimization settings"""
        return {
            'batch_processing': True,
            'parallel_models': True,
            'gpu_optimization': self.get_device() != 'cpu',
            'memory_optimization': self.get_max_memory() is not None,
            'cache_optimization': True
        }
    
    # ========================================================================
    # PERFORMANCE PROFILES
    # ========================================================================
    
    def get_available_profiles(self) -> List[str]:
        """Get list of available performance profiles"""
        profiles = self.config_cache.get('performance_profiles', {})
        return list(profiles.keys())
    
    def get_profile_settings(self, profile_name: str) -> Dict[str, Any]:
        """
        Get settings for a specific performance profile
        
        Args:
            profile_name: Name of the performance profile
            
        Returns:
            Dictionary with profile settings
        """
        profiles = self.config_cache.get('performance_profiles', {})
        if profile_name not in profiles:
            logger.warning(f"⚠️ Unknown performance profile: {profile_name}")
            return {}
        
        return profiles[profile_name].copy()
    
    def get_performance_profile(self) -> str:
        """Get current performance profile"""
        return self._get_performance_setting('general', 'performance_profile', 'balanced', str)
    
    def apply_profile(self, profile_name: str) -> bool:
        """
        Apply a performance profile (note: requires restart for most settings)
        
        Args:
            profile_name: Name of the performance profile to apply
            
        Returns:
            Boolean indicating if profile was found and applied
        """
        profile_settings = self.get_profile_settings(profile_name)
        if not profile_settings:
            return False
        
        logger.info(f"📊 Performance profile '{profile_name}' settings retrieved")
        logger.info("⚠️ Note: Most performance settings require server restart to take effect")
        
        return True
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_all_performance_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get all performance settings organized by category"""
        return {
            'analysis_performance': self.get_analysis_performance_settings(),
            'server_performance': self.get_server_performance_settings(),
            'model_performance': self.get_model_performance_settings(),
            'rate_limiting_performance': self.get_rate_limiting_performance_settings(),
            'cache_performance': self.get_cache_performance_settings()
        }
    
    def get_performance_monitoring_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Get performance monitoring and alerting thresholds"""
        return self.config_cache.get('performance_monitoring', {})
    
    def get_validation_errors(self) -> List[str]:
        """Get any performance settings validation errors"""
        return self.validation_errors.copy()
    
    def _get_performance_setting(self, category: str, setting: str, default: Any, type_converter: type) -> Any:
        """
        Internal method to get performance setting value with proper type conversion
        
        Args:
            category: Settings category
            setting: Setting name
            default: Default value if not found
            type_converter: Type to convert the value to
            
        Returns:
            Converted setting value
        """
        try:
            category_config = self.config_cache.get(category, {})
            value = category_config.get(setting)
            
            if value is None:
                # Fall back to defaults
                defaults = category_config.get('defaults', {})
                value = defaults.get(setting, default)
            
            # Handle None values for optional settings
            if value is None and setting in ['max_memory', 'offload_folder']:
                return None
            
            # Convert to appropriate type
            if type_converter == int:
                if isinstance(value, str):
                    return int(float(value))  # Handle "32.0" -> 32
                return int(value)
            elif type_converter == float:
                return float(value)
            elif type_converter == str:
                return str(value) if value is not None else default
            else:
                return value
                
        except Exception as e:
            logger.warning(f"⚠️ Error getting performance setting {category}.{setting}: {e}, using default: {default}")
            return default
    
    def _parse_memory_string(self, memory_str: str) -> int:
        """
        Parse memory string like '10GB', '2048MB' to bytes
        
        Args:
            memory_str: Memory string with unit
            
        Returns:
            Memory in bytes
        """
        if not memory_str:
            return 0
        
        pattern = re.compile(r'^(\d+(?:\.\d+)?)\s*([GMK]B?)$', re.IGNORECASE)
        match = pattern.match(memory_str.strip())
        
        if not match:
            logger.warning(f"⚠️ Invalid memory format: {memory_str}")
            return 0
        
        value = float(match.group(1))
        unit = match.group(2).upper()
        
        multipliers = {
            'KB': 1024,
            'K': 1024,
            'MB': 1024 ** 2,
            'M': 1024 ** 2,
            'GB': 1024 ** 3,
            'G': 1024 ** 3
        }
        
        return int(value * multipliers.get(unit, 1))

def create_performance_config_manager(config_manager) -> PerformanceConfigManager:
    """
    Factory function for PerformanceConfigManager (Clean v3.1 Pattern)
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        Initialized PerformanceConfigManager instance
    """
    return PerformanceConfigManager(config_manager)

# Export public interface
__all__ = ['PerformanceConfigManager', 'create_performance_config_manager']