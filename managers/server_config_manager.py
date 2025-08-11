# ash-nlp/managers/server_config_manager.py
"""
Centralized Server Configuration Manager for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

class ServerConfigManager:
    """
    Centralized server configuration management for Ash-NLP
    Phase 3d Step 5: Consolidates all server-related environment variables
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    """
    
    def __init__(self, unified_config_manager):
        """
        Initialize ServerConfigManager with UnifiedConfigManager integration
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
        """
        # STEP 9 CHANGE: Use UnifiedConfigManager instead of ConfigManager
        self.unified_config = unified_config_manager
        
        # Load server configuration using unified manager
        self.server_config = self._load_server_configuration()
        
        logger.info("ServerConfigManager v3.1d Step 9 initialized - UnifiedConfigManager integration complete")
    
    def _load_server_configuration(self) -> Dict[str, Any]:
        """Load server configuration using UnifiedConfigManager (NO MORE os.getenv())"""
        try:
            # Load server configuration from JSON through unified manager
            config = self.unified_config.load_config_file('server_settings')
            
            if config and 'server_configuration' in config:
                logger.info("✅ Server configuration loaded from JSON with environment overrides")
                return config
            else:
                logger.warning("⚠️ JSON server configuration not found, using environment fallback")
                return self._get_fallback_server_config()
                
        except Exception as e:
            logger.error(f"❌ Error loading server configuration: {e}")
            return self._get_fallback_server_config()
    
    def _get_fallback_server_config(self) -> Dict[str, Any]:
        """Get fallback server configuration using UnifiedConfigManager (NO MORE os.getenv())"""
        logger.info("🔧 Using UnifiedConfigManager for fallback server configuration")
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv() for ALL variables
        return {
            'server_configuration': {
                'network_settings': {
                    'host': self.unified_config.get_env('NLP_SERVER_HOST', '0.0.0.0'),
                    'port': self.unified_config.get_env_int('GLOBAL_NLP_API_PORT', 8881),  # PRESERVED GLOBAL
                    'workers': self.unified_config.get_env_int('NLP_PERFORMANCE_WORKERS', 1),
                    'reload_on_changes': self.unified_config.get_env_bool('NLP_FEATURE_RELOAD_ON_CHANGES', False)
                },
                'performance_settings': {
                    'max_concurrent_requests': self.unified_config.get_env_int('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 20),
                    'request_timeout': self.unified_config.get_env_int('NLP_PERFORMANCE_REQUEST_TIMEOUT', 40),
                    'worker_timeout': self.unified_config.get_env_int('NLP_PERFORMANCE_WORKER_TIMEOUT', 60)
                },
                'security_settings': {
                    'rate_limiting': {
                        'requests_per_minute': self.unified_config.get_env_int('NLP_PERFORMANCE_RATE_LIMIT_PER_MINUTE', 120),
                        'requests_per_hour': self.unified_config.get_env_int('NLP_PERFORMANCE_RATE_LIMIT_PER_HOUR', 2000),
                        'burst_limit': self.unified_config.get_env_int('NLP_SECURITY_BURST_LIMIT', 150)
                    },
                    'access_control': {
                        'allowed_ips': self.unified_config.get_env('GLOBAL_ALLOWED_IPS', '10.20.30.0/24,127.0.0.1,::1'),  # PRESERVED GLOBAL
                        'cors_enabled': self.unified_config.get_env_bool('GLOBAL_ENABLE_CORS', True)  # PRESERVED GLOBAL
                    }
                },
                'operational_settings': {
                    'health_check_interval': self.unified_config.get_env_int('NLP_SERVER_HEALTH_CHECK_INTERVAL', 30),
                    'graceful_shutdown_timeout': self.unified_config.get_env_int('NLP_SERVER_SHUTDOWN_TIMEOUT', 10),
                    'startup_timeout': self.unified_config.get_env_int('NLP_SERVER_STARTUP_TIMEOUT', 120)
                }
            },
            'defaults': {
                'network_settings': {
                    'host': '0.0.0.0',
                    'port': 8881,
                    'workers': 1,
                    'reload_on_changes': False
                },
                'performance_settings': {
                    'max_concurrent_requests': 20,
                    'request_timeout': 40,
                    'worker_timeout': 60
                },
                'security_settings': {
                    'rate_limiting': {
                        'requests_per_minute': 120,
                        'requests_per_hour': 2000,
                        'burst_limit': 150
                    }
                },
                'operational_settings': {
                    'health_check_interval': 30,
                    'graceful_shutdown_timeout': 10,
                    'startup_timeout': 120
                }
            }
        }
    
    def _parse_bool(self, value: Union[str, bool]) -> bool:
        """Parse boolean value from string or bool"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return False
    
    # ========================================================================
    # NETWORK SETTINGS ACCESS METHODS
    # ========================================================================
    
    def get_network_settings(self) -> Dict[str, Any]:
        """Get server network configuration settings"""
        logger.debug("🌐 Getting network settings...")
        
        defaults = self.server_config.get('defaults', {}).get('network_settings', {})
        config_settings = self.server_config.get('server_configuration', {}).get('network_settings', {})
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv()
        return {
            'host': self.unified_config.get_env('NLP_SERVER_HOST', 
                                              config_settings.get('host', 
                                              defaults.get('host', '0.0.0.0'))),
            'port': self.unified_config.get_env_int('GLOBAL_NLP_API_PORT', 8881),  # PRESERVED GLOBAL
            'workers': self.unified_config.get_env_int('NLP_PERFORMANCE_WORKERS', 
                                                     config_settings.get('workers', 
                                                     defaults.get('workers', 1))),
            'reload_on_changes': self.unified_config.get_env_bool('NLP_FEATURE_RELOAD_ON_CHANGES', 
                                                               config_settings.get('reload_on_changes', 
                                                               defaults.get('reload_on_changes', False)))
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get server performance settings"""
        logger.debug("⚡ Getting performance settings...")
        
        defaults = self.server_config.get('defaults', {}).get('performance_settings', {})
        config_settings = self.server_config.get('server_configuration', {}).get('performance_settings', {})
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv()
        return {
            'max_concurrent_requests': self.unified_config.get_env_int('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 
                                                                     config_settings.get('max_concurrent_requests', 
                                                                     defaults.get('max_concurrent_requests', 20))),
            'request_timeout': self.unified_config.get_env_int('NLP_PERFORMANCE_REQUEST_TIMEOUT', 
                                                             config_settings.get('request_timeout', 
                                                             defaults.get('request_timeout', 40))),
            'worker_timeout': self.unified_config.get_env_int('NLP_PERFORMANCE_WORKER_TIMEOUT', 
                                                            config_settings.get('worker_timeout', 
                                                            defaults.get('worker_timeout', 60)))
        }
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security configuration settings"""
        logger.debug("🔒 Getting security settings...")
        
        defaults = self.server_config.get('defaults', {}).get('security_settings', {}).get('rate_limiting', {})
        config_settings = self.server_config.get('server_configuration', {}).get('security_settings', {}).get('rate_limiting', {})
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv()
        return {
            'rate_limiting': {
                'requests_per_minute': self.unified_config.get_env_int('NLP_PERFORMANCE_RATE_LIMIT_PER_MINUTE', 
                                                                     config_settings.get('requests_per_minute', 
                                                                     defaults.get('requests_per_minute', 120))),
                'requests_per_hour': self.unified_config.get_env_int('NLP_PERFORMANCE_RATE_LIMIT_PER_HOUR', 
                                                                   config_settings.get('requests_per_hour', 
                                                                   defaults.get('requests_per_hour', 2000))),
                'burst_limit': self.unified_config.get_env_int('NLP_SECURITY_BURST_LIMIT', 
                                                             config_settings.get('burst_limit', 
                                                             defaults.get('burst_limit', 150)))
            },
            'access_control': {
                'allowed_ips': self.unified_config.get_env('GLOBAL_ALLOWED_IPS', '10.20.30.0/24,127.0.0.1,::1'),  # PRESERVED GLOBAL
                'cors_enabled': self.unified_config.get_env_bool('GLOBAL_ENABLE_CORS', True)  # PRESERVED GLOBAL
            }
        }
    
    def get_operational_settings(self) -> Dict[str, Any]:
        """Get operational configuration settings"""
        logger.debug("⚙️ Getting operational settings...")
        
        defaults = self.server_config.get('defaults', {}).get('operational_settings', {})
        config_settings = self.server_config.get('server_configuration', {}).get('operational_settings', {})
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv()
        return {
            'health_check_interval': self.unified_config.get_env_int('NLP_SERVER_HEALTH_CHECK_INTERVAL', 
                                                                   config_settings.get('health_check_interval', 
                                                                   defaults.get('health_check_interval', 30))),
            'graceful_shutdown_timeout': self.unified_config.get_env_int('NLP_SERVER_SHUTDOWN_TIMEOUT', 
                                                                       config_settings.get('graceful_shutdown_timeout', 
                                                                       defaults.get('graceful_shutdown_timeout', 10))),
            'startup_timeout': self.unified_config.get_env_int('NLP_SERVER_STARTUP_TIMEOUT', 
                                                             config_settings.get('startup_timeout', 
                                                             defaults.get('startup_timeout', 120)))
        }
    
    def get_complete_server_configuration(self) -> Dict[str, Any]:
        """Get complete server configuration"""
        logger.debug("📊 Assembling complete server configuration...")
        
        return {
            'network': self.get_network_settings(),
            'performance': self.get_performance_settings(),
            'security': self.get_security_settings(),
            'operational': self.get_operational_settings(),
            'metadata': {
                'phase': '3d-step9',
                'architecture': 'clean_v3.1d_unified_config',
                'consolidation_complete': True,
                'duplicates_eliminated': 5,
                'unified_config_manager': True,
                'direct_os_getenv_calls': 'eliminated'
            }
        }
    
    def validate_server_configuration(self) -> Dict[str, Any]:
        """Validate server configuration settings"""
        logger.debug("🔍 Validating server configuration...")
        
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'consolidation_status': 'complete',
            'unified_config_manager': True
        }
        
        try:
            # Validate network settings
            network = self.get_network_settings()
            if network['port'] < 1024 or network['port'] > 65535:
                validation_results['errors'].append(f"Invalid port: {network['port']} (must be 1024-65535)")
                validation_results['valid'] = False
            
            if network['workers'] < 1 or network['workers'] > 8:
                validation_results['warnings'].append(f"Unusual worker count: {network['workers']} (recommended: 1-4)")
            
            # Validate performance settings
            performance = self.get_performance_settings()
            if performance['max_concurrent_requests'] > 100:
                validation_results['warnings'].append(f"High concurrent requests: {performance['max_concurrent_requests']} (may impact performance)")
            
            if performance['request_timeout'] < 10:
                validation_results['warnings'].append(f"Low request timeout: {performance['request_timeout']}s (may cause premature timeouts)")
            
            logger.info(f"✅ Server configuration validation: {'PASSED' if validation_results['valid'] else 'FAILED'}")
            
        except Exception as e:
            validation_results['errors'].append(f"Validation error: {str(e)}")
            validation_results['valid'] = False
            logger.error(f"❌ Server configuration validation error: {e}")
        
        return validation_results

# ========================================================================
# FACTORY FUNCTION - Updated for Phase 3d Step 9
# ========================================================================

def create_server_config_manager(unified_config_manager) -> ServerConfigManager:
    """
    Factory function for creating ServerConfigManager instance - Phase 3d Step 9
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for dependency injection
        
    Returns:
        Initialized ServerConfigManager instance
        
    Raises:
        ValueError: If unified_config_manager is None or invalid
    """
    logger.debug("🏭 Creating ServerConfigManager with UnifiedConfigManager (Phase 3d Step 9)")
    
    if not unified_config_manager:
        raise ValueError("UnifiedConfigManager is required for ServerConfigManager factory")
    
    return ServerConfigManager(unified_config_manager)

# ========================================================================
# MODULE EXPORTS - CLEAN V3.1 STANDARD
# ========================================================================

__all__ = ['ServerConfigManager', 'create_server_config_manager']

logger.info("✅ ServerConfigManager v3.1d Step 9 loaded - UnifiedConfigManager integration complete, direct os.getenv() calls eliminated")