# ash-nlp/managers/server_config_manager.py
"""
Centralized Server Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3d-11-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

class ServerConfigManager:
    """
    Centralized server configuration management for Ash-NLP
    Updated for v3.1 configuration format with comprehensive settings and environment overrides
    Phase 3d Step 5: Consolidates all server-related environment variables
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    Updated for v3.1: Works with new server_settings.json format
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
        
        logger.info("ServerConfigManager v3.1 Step 9 initialized - v3.1 configuration format support added")
    
    def _load_server_configuration(self) -> Dict[str, Any]:
        """Load server configuration using UnifiedConfigManager with v3.1 format support"""
        try:
            # Load server configuration from v3.1 JSON through unified manager
            config = self.unified_config.load_config_file('server_settings')
            
            if config and 'server_configuration' in config:
                logger.info("✅ Server configuration loaded from v3.1 JSON with environment overrides")
                return config
            else:
                logger.warning("⚠️ v3.1 JSON server configuration not found, using environment fallback")
                return self._get_fallback_server_config()
                
        except Exception as e:
            logger.error(f"❌ Error loading v3.1 server configuration: {e}")
            logger.info("🛡️ Falling back to safe defaults per Clean Architecture Charter Rule #5")
            return self._get_fallback_server_config()
    
    def _get_fallback_server_config(self) -> Dict[str, Any]:
        """Get fallback server configuration using UnifiedConfigManager (NO MORE os.getenv())"""
        logger.info("🔧 Using UnifiedConfigManager for fallback server configuration")
        
        # STEP 9 CHANGE: Use unified_config instead of os.getenv() for ALL variables
        return {
            'server_configuration': {
                'network_settings': {
                    'host': self.unified_config.get_env('NLP_SERVER_NETWORK_HOST', '0.0.0.0'),
                    'port': self.unified_config.get_env_int('NLP_SERVER_NETWORK_PORT', 8881),
                    'enable_ssl': self.unified_config.get_env_bool('NLP_SERVER_NETWORK_ENABLE_SSL', False),
                    'ssl_cert_path': self.unified_config.get_env('NLP_SERVER_NETWORK_SSL_CERT_PATH', './certs/server.crt'),
                    'ssl_key_path': self.unified_config.get_env('NLP_SERVER_NETWORK_SSL_KEY_PATH', './certs/server.key'),
                    'defaults': {
                        'host': '0.0.0.0',
                        'port': 8881,
                        'enable_ssl': False,
                        'ssl_cert_path': './certs/server.crt',
                        'ssl_key_path': './certs/server.key'
                    }
                },
                'application_settings': {
                    'debug_mode': self.unified_config.get_env_bool('NLP_SERVER_APPLICATION_DEBUG_MODE', False),
                    'workers': self.unified_config.get_env_int('NLP_SERVER_APPLICATION_WORKERS', 1),
                    'reload_on_changes': self.unified_config.get_env_bool('NLP_SERVER_APPLICATION_RELOAD_ON_CHANGES', False),
                    'access_log': self.unified_config.get_env_bool('NLP_SERVER_APPLICATION_ACCESS_LOG', True),
                    'error_log': self.unified_config.get_env_bool('NLP_SERVER_APPLICATION_ERROR_LOG', True),
                    'defaults': {
                        'debug_mode': False,
                        'workers': 1,
                        'reload_on_changes': False,
                        'access_log': True,
                        'error_log': True
                    }
                },
                'performance_settings': {
                    'max_concurrent_requests': self.unified_config.get_env_int('NLP_SERVER_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 20),
                    'request_timeout': self.unified_config.get_env_int('NLP_SERVER_PERFORMANCE_REQUEST_TIMEOUT', 40),
                    'worker_timeout': self.unified_config.get_env_int('NLP_PERFORMANCE_WORKER_TIMEOUT', 60),
                    'keep_alive_timeout': self.unified_config.get_env_int('NLP_SERVER_PERFORMANCE_KEEP_ALIVE_TIMEOUT', 2),
                    'max_request_size': self.unified_config.get_env('NLP_SERVER_PERFORMANCE_MAX_REQUEST_SIZE', '10MB'),
                    'defaults': {
                        'max_concurrent_requests': 20,
                        'request_timeout': 40,
                        'worker_timeout': 60,
                        'keep_alive_timeout': 2,
                        'max_request_size': '10MB'
                    }
                },
                'security_settings': {
                    'rate_limiting': {
                        'enable_rate_limiting': self.unified_config.get_env_bool('NLP_SERVER_SECURITY_RATE_LIMIT_ENABLE', True),
                        'requests_per_minute': self.unified_config.get_env_int('NLP_SERVER_SECURITY_RATE_LIMIT_PER_MINUTE', 60),
                        'requests_per_hour': self.unified_config.get_env_int('NLP_SERVER_SECURITY_RATE_LIMIT_PER_HOUR', 1000),
                        'burst_size': self.unified_config.get_env_int('NLP_SERVER_SECURITY_RATE_LIMIT_BURST_SIZE', 100),
                        'defaults': {
                            'enable_rate_limiting': True,
                            'requests_per_minute': 60,
                            'requests_per_hour': 1000,
                            'burst_size': 100
                        }
                    },
                    'cors': {
                        'enable_cors': self.unified_config.get_env_bool('GLOBAL_ENABLE_CORS', True),
                        'allowed_origins': self.unified_config.get_env('GLOBAL_CORS_ALLOWED_ORIGINS', '["*"]'),
                        'allowed_methods': self.unified_config.get_env('GLOBAL_CORS_ALLOWED_METHODS', '["GET", "POST", "OPTIONS"]'),
                        'allowed_headers': self.unified_config.get_env('GLOBAL_CORS_ALLOWED_HEADERS', '["Content-Type", "Authorization"]'),
                        'defaults': {
                            'enable_cors': True,
                            'allowed_origins': ['*'],
                            'allowed_methods': ['GET', 'POST', 'OPTIONS'],
                            'allowed_headers': ['Content-Type', 'Authorization']
                        }
                    }
                }
            }
        }
    
    def _get_setting_with_defaults(self, section: str, subsection: str, setting: str, default: Any) -> Any:
        """Helper to get setting with v3.1 defaults fallback"""
        try:
            config_section = self.server_config.get('server_configuration', {}).get(section, {})
            
            if subsection:
                config_subsection = config_section.get(subsection, {})
                value = config_subsection.get(setting)
                
                # Fall back to defaults if value is placeholder or None
                if value is None or (isinstance(value, str) and value.startswith('${') and value.endswith('}')):
                    defaults = config_subsection.get('defaults', {})
                    value = defaults.get(setting, default)
            else:
                value = config_section.get(setting)
                
                # Fall back to defaults if value is placeholder or None
                if value is None or (isinstance(value, str) and value.startswith('${') and value.endswith('}')):
                    defaults = config_section.get('defaults', {})
                    value = defaults.get(setting, default)
            
            return value
            
        except Exception as e:
            logger.warning(f"⚠️ Error getting setting {section}.{subsection}.{setting}: {e}")
            return default
    
    # ========================================================================
    # NETWORK SETTINGS ACCESS METHODS - Updated for v3.1
    # ========================================================================
    
    def get_network_settings(self) -> Dict[str, Any]:
        """Get server network configuration settings from v3.1 format"""
        logger.debug("🌐 Getting network settings...")
        
        return {
            'host': self._get_setting_with_defaults('network_settings', None, 'host', '0.0.0.0'),
            'port': self._get_setting_with_defaults('network_settings', None, 'port', 8881),
            'enable_ssl': self._get_setting_with_defaults('network_settings', None, 'enable_ssl', False),
            'ssl_cert_path': self._get_setting_with_defaults('network_settings', None, 'ssl_cert_path', './certs/server.crt'),
            'ssl_key_path': self._get_setting_with_defaults('network_settings', None, 'ssl_key_path', './certs/server.key')
        }
    
    def get_application_settings(self) -> Dict[str, Any]:
        """Get application-level configuration settings"""
        logger.debug("⚙️ Getting application settings...")
        
        return {
            'debug_mode': self._get_setting_with_defaults('application_settings', None, 'debug_mode', False),
            'workers': self._get_setting_with_defaults('application_settings', None, 'workers', 1),
            'reload_on_changes': self._get_setting_with_defaults('application_settings', None, 'reload_on_changes', False),
            'access_log': self._get_setting_with_defaults('application_settings', None, 'access_log', True),
            'error_log': self._get_setting_with_defaults('application_settings', None, 'error_log', True)
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get server performance settings from v3.1 format"""
        logger.debug("⚡ Getting performance settings...")
        
        return {
            'max_concurrent_requests': self._get_setting_with_defaults('performance_settings', None, 'max_concurrent_requests', 20),
            'request_timeout': self._get_setting_with_defaults('performance_settings', None, 'request_timeout', 40),
            'worker_timeout': self._get_setting_with_defaults('performance_settings', None, 'worker_timeout', 60),
            'keep_alive_timeout': self._get_setting_with_defaults('performance_settings', None, 'keep_alive_timeout', 2),
            'max_request_size': self._get_setting_with_defaults('performance_settings', None, 'max_request_size', '10MB')
        }
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security configuration settings from v3.1 format"""
        logger.debug("🔒 Getting security settings...")
        
        return {
            'rate_limiting': {
                'enable_rate_limiting': self._get_setting_with_defaults('security_settings', 'rate_limiting', 'enable_rate_limiting', True),
                'requests_per_minute': self._get_setting_with_defaults('security_settings', 'rate_limiting', 'requests_per_minute', 60),
                'requests_per_hour': self._get_setting_with_defaults('security_settings', 'rate_limiting', 'requests_per_hour', 1000),
                'burst_size': self._get_setting_with_defaults('security_settings', 'rate_limiting', 'burst_size', 100)
            },
            'cors': {
                'enable_cors': self._get_setting_with_defaults('security_settings', 'cors', 'enable_cors', True),
                'allowed_origins': self._get_setting_with_defaults('security_settings', 'cors', 'allowed_origins', ['*']),
                'allowed_methods': self._get_setting_with_defaults('security_settings', 'cors', 'allowed_methods', ['GET', 'POST', 'OPTIONS']),
                'allowed_headers': self._get_setting_with_defaults('security_settings', 'cors', 'allowed_headers', ['Content-Type', 'Authorization'])
            }
        }
    
    # ========================================================================
    # DEPLOYMENT PROFILE SUPPORT - New for v3.1
    # ========================================================================
    
    def get_deployment_profiles(self) -> Dict[str, Any]:
        """Get available deployment profiles from v3.1 configuration"""
        return self.server_config.get('deployment_profiles', {})
    
    def get_profile_settings(self, profile_name: str) -> Dict[str, Any]:
        """Get settings for a specific deployment profile"""
        profiles = self.get_deployment_profiles()
        return profiles.get(profile_name, {})
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a deployment profile
        
        Args:
            profile_name: Name of the profile to activate
            
        Returns:
            Boolean indicating if profile was found
        """
        profile_settings = self.get_profile_settings(profile_name)
        if not profile_settings:
            logger.warning(f"⚠️ Unknown deployment profile: {profile_name}")
            return False
        
        logger.info(f"🔄 Deployment profile '{profile_name}' settings retrieved")
        logger.info("⚠️ Note: Profile activation requires server restart")
        
        return True
    
    # ========================================================================
    # MONITORING SUPPORT - New for v3.1
    # ========================================================================
    
    def get_monitoring_settings(self) -> Dict[str, Any]:
        """Get monitoring and health check settings from v3.1 configuration"""
        return self.server_config.get('monitoring', {
            'health_check_endpoint': '/health',
            'metrics_endpoint': '/metrics',
            'status_endpoint': '/status',
            'enable_health_checks': True,
            'health_check_interval': 30,
            'log_health_status': True
        })
    
    # ========================================================================
    # LEGACY COMPATIBILITY METHODS - Preserved for backward compatibility
    # ========================================================================
    
    def get_operational_settings(self) -> Dict[str, Any]:
        """Get operational configuration settings (legacy compatibility)"""
        logger.debug("⚙️ Getting operational settings (legacy compatibility)...")
        
        # Map to v3.1 structure
        performance = self.get_performance_settings()
        monitoring = self.get_monitoring_settings()
        
        return {
            'health_check_interval': monitoring.get('health_check_interval', 30),
            'graceful_shutdown_timeout': 10,  # Default value
            'startup_timeout': 120,  # Default value
            'max_concurrent_requests': performance.get('max_concurrent_requests', 20),
            'request_timeout': performance.get('request_timeout', 40)
        }
    
    # ========================================================================
    # COMPREHENSIVE CONFIGURATION ACCESS
    # ========================================================================
    
    def get_complete_server_configuration(self) -> Dict[str, Any]:
        """Get complete server configuration from v3.1 format"""
        logger.debug("📊 Assembling complete server configuration...")
        
        return {
            'network': self.get_network_settings(),
            'application': self.get_application_settings(),
            'performance': self.get_performance_settings(),
            'security': self.get_security_settings(),
            'monitoring': self.get_monitoring_settings(),
            'deployment_profiles': self.get_deployment_profiles(),
            'metadata': {
                'phase': '3d-step9-v3.1',
                'architecture': 'clean_v3.1d_unified_config',
                'configuration_version': '3d.1',
                'consolidation_complete': True,
                'v31_compliant': True,
                'unified_config_manager': True,
                'direct_os_getenv_calls': 'eliminated'
            }
        }
    
    def validate_server_configuration(self) -> Dict[str, Any]:
        """Validate server configuration settings for v3.1 format"""
        logger.debug("🔍 Validating server configuration...")
        
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'consolidation_status': 'complete',
            'v31_compliant': True,
            'unified_config_manager': True
        }
        
        try:
            # Validate network settings
            network = self.get_network_settings()
            if network['port'] < 1024 or network['port'] > 65535:
                validation_results['errors'].append(f"Invalid port: {network['port']} (must be 1024-65535)")
                validation_results['valid'] = False
            
            # Validate application settings
            application = self.get_application_settings()
            if application['workers'] < 1 or application['workers'] > 16:
                validation_results['warnings'].append(f"Unusual worker count: {application['workers']} (recommended: 1-8)")
            
            # Validate performance settings
            performance = self.get_performance_settings()
            if performance['max_concurrent_requests'] > 1000:
                validation_results['warnings'].append(f"Very high concurrent requests: {performance['max_concurrent_requests']} (may impact performance)")
            
            if performance['request_timeout'] < 5:
                validation_results['warnings'].append(f"Very low request timeout: {performance['request_timeout']}s (may cause premature timeouts)")
            
            # Validate security settings
            security = self.get_security_settings()
            rate_limiting = security.get('rate_limiting', {})
            if rate_limiting.get('requests_per_minute', 0) > 1000:
                validation_results['warnings'].append("High rate limiting threshold may not provide adequate protection")
            
            logger.info(f"✅ Server configuration validation: {'PASSED' if validation_results['valid'] else 'FAILED'}")
            
        except Exception as e:
            validation_results['errors'].append(f"Validation error: {str(e)}")
            validation_results['valid'] = False
            logger.error(f"❌ Server configuration validation error: {e}")
        
        return validation_results

# ========================================================================
# FACTORY FUNCTION - Updated for v3.1 Configuration Format
# ========================================================================

def create_server_config_manager(unified_config_manager) -> ServerConfigManager:
    """
    Factory function for creating ServerConfigManager instance - v3.1 Updated
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for dependency injection
        
    Returns:
        Initialized ServerConfigManager instance
        
    Raises:
        ValueError: If unified_config_manager is None or invalid
    """
    logger.debug("🏭 Creating ServerConfigManager with v3.1 configuration format support")
    
    if not unified_config_manager:
        raise ValueError("UnifiedConfigManager is required for ServerConfigManager factory")
    
    return ServerConfigManager(unified_config_manager)

# ========================================================================
# MODULE EXPORTS - CLEAN V3.1 STANDARD
# ========================================================================

__all__ = ['ServerConfigManager', 'create_server_config_manager']

logger.info("✅ ServerConfigManager v3.1 loaded - v3.1 configuration format support added")