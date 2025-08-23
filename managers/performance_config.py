# ash-nlp/managers/performance_config_manager.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Performance Configuration Manager for Ash NLP Service
---
FILE VERSION: v3.1-3e-5.5-6-2
LAST MODIFIED: 2025-08-21
PHASE: 3e Step 5.5 - PerformanceConfigManager Optimization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

OPTIMIZATION NOTES:
- Migrated utility methods to SharedUtilitiesManager (_get_performance_setting, _parse_memory_string)
- Updated configuration access to use get_config_section() patterns
- Consolidated repetitive getter methods into generic access patterns
- Added migration references for moved functionality
- Reduced file from ~600 lines to ~300 lines (50% reduction)
- Maintained 100% API compatibility for public methods
"""

import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class PerformanceConfigManager:
    """
    Performance Configuration Manager - OPTIMIZED with Utility Method Migration
    
    MIGRATION NOTICE: Utility methods have been moved to SharedUtilitiesManager for better reusability.
    Configuration access updated to use enhanced UnifiedConfigManager patterns.
    
    This manager now focuses on:
    - Performance settings organization and access
    - Performance profile management
    - Settings validation and defaults
    - Performance monitoring configuration
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
        
        logger.info("PerformanceConfigManager v3.1e optimized initializing...")
        
        try:
            self._load_performance_configuration()
            self._validate_performance_settings()
            logger.info("PerformanceConfigManager v3.1e optimization complete")
        except Exception as e:
            logger.error(f"PerformanceConfigManager initialization failed: {e}")
            logger.info("Falling back to safe defaults per Clean Architecture Charter Rule #5")
            self._initialize_safe_defaults()
    
    def _load_performance_configuration(self):
        """Load performance settings configuration using enhanced patterns"""
        try:
            # UPDATED: Use get_config_section instead of load_config_file
            self.config_cache = self.config_manager.get_config_section('performance_settings')
            
            if not self.config_cache:
                logger.warning("No performance_settings.json found, using safe defaults")
                raise ValueError("Performance settings configuration not available")
            
            logger.debug("Performance settings configuration loaded successfully")
            logger.debug(f"Configuration keys loaded: {list(self.config_cache.keys())}")
            
            # Validate configuration structure
            if not self._validate_configuration_structure():
                logger.warning("Configuration doesn't match expected format, using resilient fallbacks")
                
        except Exception as e:
            logger.error(f"Failed to load performance settings configuration: {e}")
            raise
    
    def _validate_configuration_structure(self) -> bool:
        """Validate that configuration matches expected format"""
        required_sections = ['performance_settings', 'performance_profiles']
        
        for section in required_sections:
            if section not in self.config_cache:
                logger.warning(f"Missing configuration section: {section}")
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
        logger.info("Safe defaults initialized for resilient operation")
    
    def _validate_performance_settings(self):
        """Validate performance settings for consistency and ranges"""
        try:
            # Validate analysis performance settings
            analysis_settings = self.get_analysis_performance_settings()
            if analysis_settings.get('timeout_seconds', 0) < 5.0:
                self.validation_errors.append("Analysis timeout too low (minimum 5.0s)")
            
            # Validate server performance settings
            server_config = self.get_server_performance_settings()
            if server_config.get('max_concurrent_requests', 0) < 1:
                self.validation_errors.append("Max concurrent requests must be at least 1")
            
            # Validate model performance settings
            model_settings = self.get_model_performance_settings()
            device = model_settings.get('device', 'auto')
            valid_devices = ['auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1', 'mps']
            if device not in valid_devices:
                self.validation_errors.append(f"Invalid device setting: {device}")
                
            if self.validation_errors:
                logger.warning(f"Performance validation found {len(self.validation_errors)} issues")
            else:
                logger.debug("Performance settings validation passed")
                
        except Exception as e:
            logger.warning(f"Error during performance settings validation: {e}")
    
    # ========================================================================
    # CONSOLIDATED PERFORMANCE SETTINGS ACCESS
    # ========================================================================
    
    def get_analysis_performance_settings(self) -> Dict[str, Any]:
        """Get all analysis performance settings"""
        return {
            'timeout_seconds': self.config_manager.get_config_section('performance_settings', 'performance_settings.analysis_performance.timeout_seconds', 30.0),
            'retry_attempts': self.config_manager.get_config_section('performance_settings', 'performance_settings.analysis_performance.retry_attempts', 3),
            'enable_timeout': self.config_manager.get_config_section('performance_settings', 'performance_settings.analysis_performance.enable_timeout', True),
            'batch_size': self.config_manager.get_config_section('performance_settings', 'performance_settings.analysis_performance.batch_size', 10)
        }
    
    def get_server_performance_settings(self) -> Dict[str, Any]:
        """Get all server performance settings"""
        return {
            'max_workers': self.config_manager.get_config_section('performance_settings', 'performance_settings.server_performance.max_workers', 4),
            'worker_timeout': self.config_manager.get_config_section('performance_settings', 'performance_settings.server_performance.worker_timeout', 60),
            'request_timeout': self.config_manager.get_config_section('performance_settings', 'performance_settings.analysis_performance.timeout_seconds', 30.0),
            'max_concurrent_requests': self.config_manager.get_config_section('performance_settings', 'performance_settings.server_performance.max_concurrent_requests', 20),
            'workers': self.config_manager.get_config_section('performance_settings', 'performance_settings.server_performance.workers', 1)
        }
    
    def get_model_performance_settings(self) -> Dict[str, Any]:
        """Get all model performance settings"""
        return {
            'device': self.config_manager.get_config_section('performance_settings', 'performance_settings.model_performance.device', 'auto'),
            'device_map': self.config_manager.get_config_section('performance_settings', 'performance_settings.model_performance.device_map', 'auto'),
            'load_in_8bit': self.config_manager.get_config_section('performance_settings', 'performance_settings.model_performance.load_in_8bit', False),
            'load_in_4bit': self.config_manager.get_config_section('performance_settings', 'performance_settings.model_performance.load_in_4bit', False),
            'max_memory': self.config_manager.get_config_section('performance_settings', 'performance_settings.model_performance.max_memory', None),
            'offload_folder': self.config_manager.get_config_section('performance_settings', 'performance_settings.model_performance.offload_folder', None)
        }
    
    def get_rate_limiting_performance_settings(self) -> Dict[str, Any]:
        """Get all rate limiting performance settings"""
        return {
            'rate_limit_per_minute': self.config_manager.get_config_section('performance_settings', 'performance_settings.rate_limiting_performance.rate_limit_per_minute', 120),
            'rate_limit_per_hour': self.config_manager.get_config_section('performance_settings', 'performance_settings.rate_limiting_performance.rate_limit_per_hour', 2000),
            'rate_limit_burst': self.config_manager.get_config_section('performance_settings', 'performance_settings.rate_limiting_performance.rate_limit_burst', 150)
        }
    
    def get_cache_performance_settings(self) -> Dict[str, Any]:
        """Get all cache performance settings"""
        return {
            'model_cache_size_limit': self.config_manager.get_config_section('performance_settings', 'performance_settings.cache_performance.model_cache_size_limit', '10GB'),
            'analysis_cache_size_limit': self.config_manager.get_config_section('performance_settings', 'performance_settings.cache_performance.analysis_cache_size_limit', '2GB'),
            'cache_expiry_hours': self.config_manager.get_config_section('performance_settings', 'performance_settings.cache_performance.cache_expiry_hours', 24)
        }
    
    # ========================================================================
    # INDIVIDUAL SETTING ACCESS (BACKWARD COMPATIBILITY)
    # ========================================================================
    
    def get_analysis_timeout(self) -> float:
        """Get analysis timeout in seconds"""
        return self.config_manager.get_config_section('performance_settings', 'analysis_performance.timeout_seconds', 30.0)
    
    def get_analysis_retry_attempts(self) -> int:
        """Get analysis retry attempts"""
        return self.config_manager.get_config_section('performance_settings', 'analysis_performance.retry_attempts', 3)
    
    def get_max_workers(self) -> int:
        """Get maximum worker threads"""
        return self.config_manager.get_config_section('performance_settings', 'server_performance.max_workers', 4)
    
    def get_max_concurrent_requests(self) -> int:
        """Get maximum concurrent server requests"""
        return self.config_manager.get_config_section('performance_settings', 'server_performance.max_concurrent_requests', 20)
    
    def get_device(self) -> str:
        """Get device setting for model inference"""
        return self.config_manager.get_config_section('performance_settings', 'model_performance.device', 'auto')
    
    def get_rate_limit_requests_per_minute(self) -> int:
        """Get rate limit requests per minute"""
        return self.config_manager.get_config_section('performance_settings', 'rate_limiting_performance.rate_limit_per_minute', 120)
    
    def get_model_cache_size_limit(self) -> str:
        """Get model cache size limit"""
        return self.config_manager.get_config_section('performance_settings', 'cache_performance.model_cache_size_limit', '10GB')
    
    # Legacy compatibility methods
    def get_request_timeout(self) -> float:
        """Get request timeout in seconds (legacy compatibility)"""
        return self.get_analysis_timeout()
    
    def is_analysis_timeout_enabled(self) -> bool:
        """Check if analysis timeout is enabled"""
        return self.config_manager.get_config_section('performance_settings', 'analysis_performance.enable_timeout', True)
    
    def is_load_in_8bit_enabled(self) -> bool:
        """Check if 8-bit quantization is enabled"""
        return self.config_manager.get_config_section('performance_settings', 'model_performance.load_in_8bit', False)
    
    # ========================================================================
    # PERFORMANCE PROFILES MANAGEMENT
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
            logger.warning(f"Unknown performance profile: {profile_name}")
            return {}
        
        return profiles[profile_name].copy()
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a performance profile
        
        Args:
            profile_name: Name of the performance profile to activate
            
        Returns:
            Boolean indicating if profile was found and applied
        
        NOT CURRENTLY USED!
        """
        profile_settings = self.get_profile_settings(profile_name)
        if not profile_settings:
            return False
        
        logger.info(f"Performance profile '{profile_name}' settings retrieved")
        logger.info("Note: Most performance settings require server restart to take effect")
        
        return False
    
    # ========================================================================
    # COMPREHENSIVE SETTINGS ACCESS
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
    
    def get_cache_settings(self) -> Dict[str, Any]:
        """Get comprehensive cache settings"""
        cache_perf = self.get_cache_performance_settings()
        return {
            'enabled': True,
            'ttl': cache_perf['cache_expiry_hours'] * 3600,  # Convert to seconds
            'model_cache_limit': cache_perf['model_cache_size_limit'],
            'analysis_cache_limit': cache_perf['analysis_cache_size_limit'],
            'expiry_hours': cache_perf['cache_expiry_hours']
        }
    
    def get_optimization_settings(self) -> Dict[str, Any]:
        """Get performance optimization settings"""
        model_settings = self.get_model_performance_settings()
        return {
            'batch_processing': True,
            'parallel_models': True,
            'gpu_optimization': model_settings['device'] not in ['cpu'],
            'memory_optimization': model_settings['max_memory'] is not None,
            'cache_optimization': True,
            'quantization_enabled': model_settings['load_in_8bit'] or model_settings['load_in_4bit']
        }
    
    # ========================================================================
    # VALIDATION AND MONITORING
    # ========================================================================
    
    def get_validation_errors(self) -> List[str]:
        """Get any performance settings validation errors"""
        return self.validation_errors.copy()
    
    def get_performance_monitoring_thresholds(self) -> Dict[str, Any]:
        """Get performance monitoring and alerting thresholds"""
        return self.config_cache.get('performance_monitoring', {})


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

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