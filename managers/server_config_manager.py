# managers/server_config_manager.py
"""
Phase 3d Step 5: Server Configuration Manager
Consolidates server infrastructure variables following Clean v3.1 architecture
"""

import logging
import os
from typing import Dict, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class ServerConfigManager:
    """
    Server Configuration Manager for Ash-NLP v3.1d Step 5
    Manages server infrastructure configuration with environment variable overrides
    Consolidates duplicate server variables into standardized naming convention
    """
    
    def __init__(self, config_manager):
        """
        Initialize ServerConfigManager
        
        Args:
            config_manager: ConfigManager instance for JSON configuration loading
        """
        self.config_manager = config_manager
        self.server_config = None
        
        logger.info("🖥️ Initializing ServerConfigManager (Phase 3d Step 5)")
        self._load_configuration()
        logger.info("✅ ServerConfigManager initialization complete")
    
    def _load_configuration(self):
        """Load server configuration from JSON with environment overrides"""
        try:
            logger.debug("📋 Loading server configuration...")
            
            # Load server_settings.json configuration
            self.server_config = self.config_manager.load_config_file('server_settings')
            
            if not self.server_config:
                logger.warning("⚠️ No server_settings.json found, using environment variables only")
                self.server_config = {'server_configuration': {}, 'defaults': {}}
            
            logger.info("✅ Server configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load server configuration: {e}")
            # Fallback to empty configuration
            self.server_config = {'server_configuration': {}, 'defaults': {}}
    
    def get_network_settings(self) -> Dict[str, Any]:
        """
        Get network configuration settings
        Consolidates: NLP_HOST, NLP_SERVICE_HOST -> NLP_SERVER_HOST
        Preserves: GLOBAL_NLP_API_PORT (ecosystem requirement)
        """
        logger.debug("🌐 Getting network settings...")
        
        defaults = self.server_config.get('defaults', {}).get('network_settings', {})
        config_settings = self.server_config.get('server_configuration', {}).get('network_settings', {})
        
        return {
            'host': os.getenv('NLP_SERVER_HOST', 
                             config_settings.get('host', 
                             defaults.get('host', '0.0.0.0'))),
            'port': int(os.getenv('GLOBAL_NLP_API_PORT', '8881')),  # PRESERVED GLOBAL
            'workers': int(os.getenv('NLP_PERFORMANCE_WORKERS', 
                                   config_settings.get('workers', 
                                   defaults.get('workers', 1)))),
            'reload_on_changes': self._parse_bool(os.getenv('NLP_FEATURE_RELOAD_ON_CHANGES', 
                                                          config_settings.get('reload_on_changes', 
                                                          defaults.get('reload_on_changes', False))))
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """
        Get server performance settings
        Consolidates: NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS -> NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS
        Distinguishes: NLP_PERFORMANCE_REQUEST_TIMEOUT -> NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS (vs NLP_ANALYSIS_TIMEOUT)
        """
        logger.debug("⚡ Getting performance settings...")
        
        defaults = self.server_config.get('defaults', {}).get('performance_settings', {})
        config_settings = self.server_config.get('server_configuration', {}).get('performance_settings', {})
        
        return {
            'max_concurrent_requests': int(os.getenv('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 
                                                   config_settings.get('max_concurrent_requests', 
                                                   defaults.get('max_concurrent_requests', 20)))),
            'request_timeout': int(os.getenv('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 
                                           config_settings.get('request_timeout', 
                                           defaults.get('request_timeout', 40)))),
            'worker_timeout': int(os.getenv('NLP_PERFORMANCE_WORKER_TIMEOUT', 
                                          config_settings.get('worker_timeout', 
                                          defaults.get('worker_timeout', 60))))
        }
    
    def get_security_settings(self) -> Dict[str, Any]:
        """
        Get security configuration settings
        Preserves: GLOBAL_ALLOWED_IPS, GLOBAL_ENABLE_CORS (ecosystem requirements)
        Standardizes: Rate limiting with NLP_SECURITY_* prefix
        """
        logger.debug("🔒 Getting security settings...")
        
        defaults = self.server_config.get('defaults', {}).get('security_settings', {}).get('rate_limiting', {})
        config_settings = self.server_config.get('server_configuration', {}).get('security_settings', {}).get('rate_limiting', {})
        
        return {
            'rate_limiting': {
                'requests_per_minute': int(os.getenv('NLP_PERFORMANCE_RATE_LIMIT_PER_MINUTE', 
                                                   config_settings.get('requests_per_minute', 
                                                   defaults.get('requests_per_minute', 120)))),
                'requests_per_hour': int(os.getenv('NLP_PERFORMANCE_RATE_LIMIT_PER_HOUR', 
                                                 config_settings.get('requests_per_hour', 
                                                 defaults.get('requests_per_hour', 2000)))),
                'burst_limit': int(os.getenv('NLP_SECURITY_BURST_LIMIT', 
                                           config_settings.get('burst_limit', 
                                           defaults.get('burst_limit', 150))))
            },
            'access_control': {
                'allowed_ips': os.getenv('GLOBAL_ALLOWED_IPS', '10.20.30.0/24,127.0.0.1,::1'),  # PRESERVED GLOBAL
                'cors_enabled': self._parse_bool(os.getenv('GLOBAL_ENABLE_CORS', 'true'))  # PRESERVED GLOBAL
            }
        }
    
    def get_operational_settings(self) -> Dict[str, Any]:
        """
        Get operational configuration settings
        New standardized variables for server lifecycle management
        """
        logger.debug("⚙️ Getting operational settings...")
        
        defaults = self.server_config.get('defaults', {}).get('operational_settings', {})
        config_settings = self.server_config.get('server_configuration', {}).get('operational_settings', {})
        
        return {
            'health_check_interval': int(os.getenv('NLP_SERVER_HEALTH_CHECK_INTERVAL', 
                                                 config_settings.get('health_check_interval', 
                                                 defaults.get('health_check_interval', 30)))),
            'graceful_shutdown_timeout': int(os.getenv('NLP_SERVER_SHUTDOWN_TIMEOUT', 
                                                     config_settings.get('graceful_shutdown_timeout', 
                                                     defaults.get('graceful_shutdown_timeout', 10)))),
            'startup_timeout': int(os.getenv('NLP_SERVER_STARTUP_TIMEOUT', 
                                           config_settings.get('startup_timeout', 
                                           defaults.get('startup_timeout', 120))))
        }
    
    def get_complete_server_configuration(self) -> Dict[str, Any]:
        """
        Get complete server configuration
        Returns all server settings in organized structure
        """
        logger.debug("📊 Assembling complete server configuration...")
        
        return {
            'network': self.get_network_settings(),
            'performance': self.get_performance_settings(),
            'security': self.get_security_settings(),
            'operational': self.get_operational_settings(),
            'metadata': {
                'phase': '3d-step5',
                'architecture': 'clean_v3.1',
                'consolidation_complete': True,
                'duplicates_eliminated': 5
            }
        }
    
    def validate_server_configuration(self) -> Dict[str, Any]:
        """
        Validate server configuration settings
        Returns validation status and any issues found
        """
        logger.debug("🔍 Validating server configuration...")
        
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'consolidation_status': 'complete'
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
            if performance['max_concurrent_requests'] < 1:
                validation_results['errors'].append("max_concurrent_requests must be >= 1")
                validation_results['valid'] = False
            
            if performance['request_timeout'] < 5:
                validation_results['warnings'].append("Request timeout < 5 seconds may cause issues")
            
            # Validate security settings
            security = self.get_security_settings()
            if security['rate_limiting']['requests_per_minute'] < 1:
                validation_results['errors'].append("requests_per_minute must be >= 1")
                validation_results['valid'] = False
            
            logger.info(f"🔍 Server configuration validation: {'✅ Valid' if validation_results['valid'] else '❌ Invalid'}")
            
        except Exception as e:
            validation_results['valid'] = False
            validation_results['errors'].append(f"Validation error: {str(e)}")
            logger.error(f"❌ Server configuration validation failed: {e}")
        
        return validation_results
    
    def _parse_bool(self, value: Union[str, bool]) -> bool:
        """Parse boolean value from string or bool"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get ServerConfigManager status for health checks
        """
        return {
            'manager': 'ServerConfigManager',
            'phase': '3d-step5',
            'status': 'operational',
            'configuration_loaded': self.server_config is not None,
            'architecture': 'clean_v3.1',
            'variable_consolidation': 'complete'
        }


def create_server_config_manager(config_manager) -> ServerConfigManager:
    """
    Factory function to create ServerConfigManager
    Follows Clean v3.1 architecture pattern
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        ServerConfigManager instance
    """
    logger.info("🏭 Creating ServerConfigManager (Phase 3d Step 5)")
    return ServerConfigManager(config_manager)


__all__ = ['ServerConfigManager', 'create_server_config_manager']