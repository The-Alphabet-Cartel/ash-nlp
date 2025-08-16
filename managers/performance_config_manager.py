# ash-nlp/managers/performance_config_manager.py
"""
Performance Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3d-10-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10
CLEAN ARCHITECTURE: v3.1 Compliant
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
    Performance Configuration Manager for Ash NLP Service v3.1d - Updated for v3.1 Configuration Format
    
    Manages performance settings for crisis analysis system components with comprehensive validation and profile management.
    Implements Clean v3.1 architecture patterns with dependency injection and fail-fast validation.
    
    Features:
    - Analysis performance settings
    - Server performance configuration  
    - Model performance optimization
    - Rate limiting settings
    - Cache performance management
    - Performance profile management
    
    Updated for v3.1 configuration format with environment variable placeholders and comprehensive defaults.
    """
    
    def __init__(self, config_manager):
        """
        Initialize PerformanceConfigManager with dependency injection
        
        Args:
            config_manager: UnifiedConfigManager instance for accessing configuration
        """
        self.config_manager = config_manager
        self.config_cache = {}
        self.validation_errors = []
        
        logger.info("⚡ Initializing PerformanceConfigManager v3.1 (Updated for v3.1 Config Format)")
        
        try:
            self._load_performance_configuration()
            self._validate_performance_settings()
            logger.info("✅ PerformanceConfigManager v3.1 initialization complete")
        except Exception as e:
            logger.error(f"❌ PerformanceConfigManager initialization failed: {e}")
            logger.info("🛡️ Falling back to safe defaults per Clean Architecture Charter Rule #5")
            self._initialize_safe_defaults()
    
    def _load_performance_configuration(self):
        """Load performance settings configuration from v3.1 JSON with environment overrides"""
        try:
            # Load performance settings configuration through UnifiedConfigManager
            performance_config_raw = self.config_manager.load_config_file('performance_settings')
            
            if not performance_config_raw:
                logger.error("❌ Could not load performance_settings.json configuration")
                raise ValueError("Performance settings configuration not available")
            
            # Load the ENTIRE configuration for v3.1 format
            self.config_cache = performance_config_raw
                
            logger.debug("✅ Performance settings v3.1 configuration loaded successfully")
            logger.debug(f"🔍 Configuration keys loaded: {list(self.config_cache.keys())}")
            
            # Validate v3.1 structure
            if not self._validate_v31_structure():
                logger.warning("⚠️ Configuration doesn't match v3.1 format, using resilient fallbacks")
                
        except Exception as e:
            logger.error(f"❌ Failed to load performance settings configuration: {e}")
            raise
    
    def _validate_v31_structure(self) -> bool:
        """Validate that configuration matches v3.1 format"""
        required_sections = ['performance_settings', 'performance_profiles']
        
        for section in required_sections:
            if section not in self.config_cache:
                logger.warning(f"⚠️ Missing v3.1 section: {section}")
                return False
                
        # Check performance_settings subsections
        perf_settings = self.config_cache.get('performance_settings', {})
        required_perf_sections = [
            'analysis_performance',
            'server_performance', 
            'model_performance',
            'rate_limiting_performance'
        ]
        
        for section in required_perf_sections:
            if section not in perf_settings:
                logger.warning(f"⚠️ Missing v3.1 performance section: {section}")
                return False
                
        return True
    
    def _initialize_safe_defaults(self):
        """Initialize safe default configuration per Clean Architecture Charter Rule #5"""
        self.config_cache = {
            'performance_settings': {
                'analysis_performance': {
                    'defaults': {
                        'timeout_seconds': 30.0,
                        'retry_attempts': 3,
                        'enable_timeout': True,
                        'batch_size': 10
                    }
                },
                'server_performance': {
                    'defaults': {
                        'max_workers': 4,
                        'worker_timeout': 60,
                        'request_timeout': 30,
                        'max_concurrent_requests': 20,
                        'workers': 1
                    }
                },
                'model_performance': {
                    'defaults': {
                        'device': 'auto',
                        'device_map': 'auto',
                        'load_in_8bit': False,
                        'load_in_4bit': False,
                        'max_memory': None,
                        'offload_folder': None
                    }
                },
                'rate_limiting_performance': {
                    'defaults': {
                        'rate_limit_per_minute': 120,
                        'rate_limit_per_hour': 2000,
                        'rate_limit_burst': 150
                    }
                },
                'cache_performance': {
                    'defaults': {
                        'model_cache_size_limit': '10GB',
                        'analysis_cache_size_limit': '2GB',
                        'cache_expiry_hours': 24
                    }
                }
            },
            'performance_profiles': {
                'balanced': {
                    'description': 'Balanced settings for general production use',
                    'analysis_timeout': 30.0,
                    'max_workers': 4,
                    'device': 'auto'
                }
            }
        }
        logger.info("✅ Safe defaults initialized for resilient operation")
    
    def _validate_performance_settings(self):
        """Validate performance settings for consistency and ranges"""
        try:
            # Validate analysis performance settings
            analysis_settings = self.get_analysis_performance_settings()
            if analysis_settings['timeout_seconds'] < 5.0:
                self.validation_errors.append("Analysis timeout too low (minimum 5.0s)")
            
            # Validate server performance settings
            server_settings = self.get_server_performance_settings()
            if server_settings['max_concurrent_requests'] < 1:
                self.validation_errors.append("Max concurrent requests must be at least 1")
            
            # Validate model performance settings
            model_settings = self.get_model_performance_settings()
            device = model_settings.get('device', 'auto')
            if device not in ['auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1', 'mps']:
                self.validation_errors.append(f"Invalid device setting: {device}")
                
            if self.validation_errors:
                logger.warning(f"⚠️ Performance validation found {len(self.validation_errors)} issues")
            else:
                logger.debug("✅ Performance settings validation passed")
                
        except Exception as e:
            logger.warning(f"⚠️ Error during performance settings validation: {e}")
    
    # ========================================================================
    # ANALYSIS PERFORMANCE SETTINGS - Updated for v3.1
    # ========================================================================
    
    def get_analysis_timeout(self) -> float:
        """Get analysis timeout in seconds"""
        return self._get_performance_setting('analysis_performance', 'timeout_seconds', 30.0, float)
    
    def get_analysis_retry_attempts(self) -> int:
        """Get analysis retry attempts"""
        return self._get_performance_setting('analysis_performance', 'retry_attempts', 3, int)
    
    def get_analysis_batch_size(self) -> int:
        """Get analysis batch size"""
        return self._get_performance_setting('analysis_performance', 'batch_size', 10, int)
    
    def is_analysis_timeout_enabled(self) -> bool:
        """Check if analysis timeout is enabled"""
        return self._get_performance_setting('analysis_performance', 'enable_timeout', True, bool)
    
    def get_request_timeout(self) -> float:
        """Get request timeout in seconds (legacy compatibility)"""
        return self.get_analysis_timeout()
    
    def get_analysis_performance_settings(self) -> Dict[str, Any]:
        """Get all analysis performance settings"""
        return {
            'timeout_seconds': self.get_analysis_timeout(),
            'retry_attempts': self.get_analysis_retry_attempts(),
            'enable_timeout': self.is_analysis_timeout_enabled(),
            'batch_size': self.get_analysis_batch_size()
        }
    
    # ========================================================================
    # SERVER PERFORMANCE SETTINGS - Updated for v3.1
    # ========================================================================
    
    def get_max_workers(self) -> int:
        """Get maximum worker threads"""
        return self._get_performance_setting('server_performance', 'max_workers', 4, int)
    
    def get_worker_timeout(self) -> int:
        """Get worker timeout in seconds"""
        return self._get_performance_setting('server_performance', 'worker_timeout', 60, int)
    
    def get_max_concurrent_requests(self) -> int:
        """Get maximum concurrent server requests"""
        return self._get_performance_setting('server_performance', 'max_concurrent_requests', 20, int)
    
    def get_workers(self) -> int:
        """Get number of server worker processes"""
        return self._get_performance_setting('server_performance', 'workers', 1, int)
    
    def get_server_performance_settings(self) -> Dict[str, Any]:
        """Get all server performance settings"""
        return {
            'max_workers': self.get_max_workers(),
            'worker_timeout': self.get_worker_timeout(),
            'request_timeout': self.get_analysis_timeout(),  # Map to analysis timeout
            'max_concurrent_requests': self.get_max_concurrent_requests(),
            'workers': self.get_workers()
        }
    
    # ========================================================================
    # MODEL PERFORMANCE SETTINGS - Updated for v3.1
    # ========================================================================
    
    def get_device(self) -> str:
        """Get device setting for model inference"""
        return self._get_performance_setting('model_performance', 'device', 'auto', str)
    
    def get_device_map(self) -> str:
        """Get device mapping strategy"""
        return self._get_performance_setting('model_performance', 'device_map', 'auto', str)
    
    def is_load_in_8bit_enabled(self) -> bool:
        """Check if 8-bit quantization is enabled"""
        return self._get_performance_setting('model_performance', 'load_in_8bit', False, bool)
    
    def is_load_in_4bit_enabled(self) -> bool:
        """Check if 4-bit quantization is enabled"""
        return self._get_performance_setting('model_performance', 'load_in_4bit', False, bool)
    
    def get_max_memory(self) -> Optional[str]:
        """Get maximum memory limit"""
        return self._get_performance_setting('model_performance', 'max_memory', None, str)
    
    def get_offload_folder(self) -> Optional[str]:
        """Get offload folder for model weights"""
        return self._get_performance_setting('model_performance', 'offload_folder', None, str)
    
    def get_model_performance_settings(self) -> Dict[str, Any]:
        """Get all model performance settings"""
        return {
            'device': self.get_device(),
            'device_map': self.get_device_map(),
            'load_in_8bit': self.is_load_in_8bit_enabled(),
            'load_in_4bit': self.is_load_in_4bit_enabled(),
            'max_memory': self.get_max_memory(),
            'offload_folder': self.get_offload_folder()
        }
    
    # ========================================================================
    # RATE LIMITING PERFORMANCE SETTINGS - Updated for v3.1
    # ========================================================================
    
    def get_rate_limit_requests_per_minute(self) -> int:
        """Get rate limit requests per minute"""
        return self._get_performance_setting('rate_limiting_performance', 'rate_limit_per_minute', 120, int)
    
    def get_rate_limit_requests_per_hour(self) -> int:
        """Get rate limit requests per hour"""
        return self._get_performance_setting('rate_limiting_performance', 'rate_limit_per_hour', 2000, int)

    def get_rate_limit_burst_size(self) -> int:
        """Get rate limit burst size"""
        return self._get_performance_setting('rate_limiting_performance', 'rate_limit_burst', 150, int)
    
    def get_rate_limiting_performance_settings(self) -> Dict[str, Any]:
        """Get all rate limiting performance settings"""
        return {
            'rate_limit_per_minute': self.get_rate_limit_requests_per_minute(),
            'rate_limit_per_hour': self.get_rate_limit_requests_per_hour(),
            'rate_limit_burst': self.get_rate_limit_burst_size()
        }
    
    # ========================================================================
    # CACHE PERFORMANCE SETTINGS - Updated for v3.1
    # ========================================================================
    
    def get_model_cache_size_limit(self) -> str:
        """Get model cache size limit"""
        return self._get_performance_setting('cache_performance', 'model_cache_size_limit', '10GB', str)
    
    def get_analysis_cache_size_limit(self) -> str:
        """Get analysis cache size limit"""
        return self._get_performance_setting('cache_performance', 'analysis_cache_size_limit', '2GB', str)
    
    def get_cache_expiry_hours(self) -> int:
        """Get cache expiry in hours"""
        return self._get_performance_setting('cache_performance', 'cache_expiry_hours', 24, int)
    
    def get_cache_settings(self) -> Dict[str, Any]:
        """Get comprehensive cache settings"""
        return {
            'enabled': True,  # Cache always enabled for performance
            'ttl': self.get_cache_expiry_hours() * 3600,  # Convert to seconds
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
    # OPTIMIZATION SETTINGS - Updated for v3.1
    # ========================================================================
    
    def get_optimization_settings(self) -> Dict[str, Any]:
        """Get performance optimization settings"""
        return {
            'batch_processing': True,
            'parallel_models': True,
            'gpu_optimization': self.get_device() not in ['cpu'],
            'memory_optimization': self.get_max_memory() is not None,
            'cache_optimization': True,
            'quantization_enabled': self.is_load_in_8bit_enabled() or self.is_load_in_4bit_enabled()
        }
    
    # ========================================================================
    # PERFORMANCE PROFILES - Updated for v3.1
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
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a performance profile
        
        Args:
            profile_name: Name of the performance profile to activate
            
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
    # UTILITY METHODS - Updated for v3.1
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
    
    def get_performance_monitoring_thresholds(self) -> Dict[str, Any]:
        """Get performance monitoring and alerting thresholds"""
        return self.config_cache.get('performance_monitoring', {})
    
    def get_validation_errors(self) -> List[str]:
        """Get any performance settings validation errors"""
        return self.validation_errors.copy()
    
    def _get_performance_setting(self, category: str, setting: str, default: Any, type_converter: type) -> Any:
        """
        Internal method to get performance setting value with proper type conversion
        Handles v3.1 configuration format with environment variables and defaults
        
        Args:
            category: Settings category
            setting: Setting name
            default: Default value if not found
            type_converter: Type to convert the value to
            
        Returns:
            Converted setting value
        """
        try:
            # Look inside performance_settings section
            performance_settings = self.config_cache.get('performance_settings', {})
            category_config = performance_settings.get(category, {})
            
            # First try to get the value directly (after environment substitution)
            value = category_config.get(setting)
            
            # If value is None or still has placeholder, fall back to defaults
            if value is None or (isinstance(value, str) and value.startswith('${') and value.endswith('}')):
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
            elif type_converter == bool:
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
                return bool(value)
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
        config_manager: UnifiedConfigManager instance
        
    Returns:
        Initialized PerformanceConfigManager instance
    """
    return PerformanceConfigManager(config_manager)

# Export public interface
__all__ = ['PerformanceConfigManager', 'create_performance_config_manager']