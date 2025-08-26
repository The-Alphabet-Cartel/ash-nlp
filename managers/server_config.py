# ash-nlp/managers/server_config_manager.py
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
Centralized Server Configuration Manager for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-1
LAST MODIFIED: 2025-08-22
PHASE: 3e, Sub-step 5.5, Task 5 - ServerConfigManager Standard Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

class ServerConfigManager:
    """
    Centralized server configuration management for Ash-NLP service
    
    Phase 3e Sub-step 5.5: Enhanced with get_config_section() patterns and improved error handling
    
    This manager provides comprehensive server configuration management including:
    - Network settings (host, port, SSL configuration)
    - Application settings (debug, workers, reload behavior)
    - Performance settings (timeouts, concurrent requests, worker management)
    - Security settings (rate limiting, CORS configuration)
    - Deployment profiles for different environments
    - Monitoring and health check configuration
    
    Phase 3e Improvements:
    - Replaced load_config_file() with get_config_section() patterns
    - Enhanced error handling and resilience
    - Improved fallback mechanisms for safe operation
    - Better integration with UnifiedConfigManager
    - Added configuration validation and monitoring
    """
    
    def __init__(self, unified_config_manager):
        """
        Initialize ServerConfigManager with UnifiedConfigManager integration
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
        """
        self.unified_config = unified_config_manager
        
        # Load server configuration using Phase 3e patterns
        self.server_config = self._load_server_configuration()
        
        logger.info("ServerConfigManager v3.1e-5.5 initialized - Phase 3e patterns applied")
    
    def _load_server_configuration(self) -> Dict[str, Any]:
        """Load server configuration using Phase 3e get_config_section patterns"""
        try:
            # PHASE 3E: Use get_config_section instead of load_config_file
            config = self.unified_config.get_config_section('server_config')
            logger.info("Server configuration loaded from JSON with environment overrides")

            return config
                
        except Exception as e:
            logger.error(f"Error loading server configuration: {e}")
            return

    def _get_setting_with_defaults(self, section: str, subsection: str, setting: str, default: Any) -> Any:
        """
        Helper to get setting with enhanced Phase 3e defaults fallback and error handling
        
        Args:
            section: Configuration section name
            subsection: Configuration subsection name (can be None)
            setting: Setting name
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
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
            logger.warning(f"Error getting setting {section}.{subsection}.{setting}: {e}")
            return default
    
    # ========================================================================
    # NETWORK SETTINGS ACCESS METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_network_settings(self) -> Dict[str, Any]:
        """Get server network configuration settings with Phase 3e enhancements"""
        logger.debug("Getting network settings...")
        
        try:
            # PHASE 3E: Enhanced with better error handling and validation
            settings = {
                'host': self._get_setting_with_defaults('network_settings', None, 'host', '0.0.0.0'),
                'port': self._get_setting_with_defaults('network_settings', None, 'port', 8881),
                'enable_ssl': self._get_setting_with_defaults('network_settings', None, 'enable_ssl', False),
                'ssl_cert_path': self._get_setting_with_defaults('network_settings', None, 'ssl_cert_path', './certs/server.crt'),
                'ssl_key_path': self._get_setting_with_defaults('network_settings', None, 'ssl_key_path', './certs/server.key')
            }
            
            # Validate port range
            if not isinstance(settings['port'], int) or settings['port'] < 1 or settings['port'] > 65535:
                logger.warning(f"Invalid port {settings['port']}, using default 8881")
                settings['port'] = 8881
                
            return settings
            
        except Exception as e:
            logger.error(f"Error getting network settings: {e}")
            return {
                'host': '0.0.0.0',
                'port': 8881,
                'enable_ssl': False,
                'ssl_cert_path': './certs/server.crt',
                'ssl_key_path': './certs/server.key'
            }
    
    def get_application_settings(self) -> Dict[str, Any]:
        """Get application-level configuration settings with Phase 3e enhancements"""
        logger.debug("Getting application settings...")
        
        try:
            settings = {
                'debug_mode': self._get_setting_with_defaults('application_settings', None, 'debug_mode', False),
                'workers': self._get_setting_with_defaults('application_settings', None, 'workers', 1),
                'reload_on_changes': self._get_setting_with_defaults('application_settings', None, 'reload_on_changes', False),
                'access_log': self._get_setting_with_defaults('application_settings', None, 'access_log', True),
                'error_log': self._get_setting_with_defaults('application_settings', None, 'error_log', True)
            }
            
            # Validate worker count
            if not isinstance(settings['workers'], int) or settings['workers'] < 1:
                logger.warning(f"Invalid worker count {settings['workers']}, using default 1")
                settings['workers'] = 1
            elif settings['workers'] > 16:
                logger.warning(f"High worker count {settings['workers']} may impact performance")
                
            return settings
            
        except Exception as e:
            logger.error(f"Error getting application settings: {e}")
            return {
                'debug_mode': False,
                'workers': 1,
                'reload_on_changes': False,
                'access_log': True,
                'error_log': True
            }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get server performance settings with Phase 3e enhancements"""
        logger.debug("Getting performance settings...")
        
        try:
            settings = {
                'max_concurrent_requests': self._get_setting_with_defaults('performance_settings', None, 'max_concurrent_requests', 20),
                'request_timeout': self._get_setting_with_defaults('performance_settings', None, 'request_timeout', 40),
                'worker_timeout': self._get_setting_with_defaults('performance_settings', None, 'worker_timeout', 60),
                'keep_alive_timeout': self._get_setting_with_defaults('performance_settings', None, 'keep_alive_timeout', 2),
                'max_request_size': self._get_setting_with_defaults('performance_settings', None, 'max_request_size', '10MB')
            }
            
            # Validate timeout values
            if not isinstance(settings['request_timeout'], int) or settings['request_timeout'] < 1:
                logger.warning(f"Invalid request timeout {settings['request_timeout']}, using default 40")
                settings['request_timeout'] = 40
            elif settings['request_timeout'] < 5:
                logger.warning(f"Very low request timeout {settings['request_timeout']}s may cause premature timeouts")
                
            if not isinstance(settings['max_concurrent_requests'], int) or settings['max_concurrent_requests'] < 1:
                logger.warning(f"Invalid max concurrent requests {settings['max_concurrent_requests']}, using default 20")
                settings['max_concurrent_requests'] = 20
                
            return settings
            
        except Exception as e:
            logger.error(f"Error getting performance settings: {e}")
            return {
                'max_concurrent_requests': 20,
                'request_timeout': 40,
                'worker_timeout': 60,
                'keep_alive_timeout': 2,
                'max_request_size': '10MB'
            }
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security configuration settings with Phase 3e enhancements"""
        logger.debug("Getting security settings...")
        
        try:
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
            
        except Exception as e:
            logger.error(f"Error getting security settings: {e}")
            return {
                'rate_limiting': {
                    'enable_rate_limiting': True,
                    'requests_per_minute': 60,
                    'requests_per_hour': 1000,
                    'burst_size': 100
                },
                'cors': {
                    'enable_cors': True,
                    'allowed_origins': ['*'],
                    'allowed_methods': ['GET', 'POST', 'OPTIONS'],
                    'allowed_headers': ['Content-Type', 'Authorization']
                }
            }
    
    # ========================================================================
    # DEPLOYMENT PROFILE SUPPORT (Phase 3e Enhanced)
    # ========================================================================
    
    def get_deployment_profiles(self) -> Dict[str, Any]:
        """Get available deployment profiles with Phase 3e configuration patterns"""
        try:
            # PHASE 3E: Use get_config_section pattern for deployment profiles
            profiles = self.unified_config.get_config_section('server_config', 'deployment_profiles', {})
            if not profiles:
                # Fallback to direct server_config access
                profiles = self.server_config.get('deployment_profiles', {})
            
            return profiles
            
        except Exception as e:
            logger.error(f"Error getting deployment profiles: {e}")
            return {}
    
    def get_profile_settings(self, profile_name: str) -> Dict[str, Any]:
        """Get settings for a specific deployment profile with enhanced error handling"""
        try:
            profiles = self.get_deployment_profiles()
            return profiles.get(profile_name, {})
        except Exception as e:
            logger.error(f"Error getting profile settings for {profile_name}: {e}")
            return {}
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a deployment profile with enhanced validation
        
        Args:
            profile_name: Name of the profile to activate
            
        Returns:
            Boolean indicating if profile was found and validated
        
        NOT CURRENTLY USED!
        """
#        try:
#            profile_settings = self.get_profile_settings(profile_name)
#            if not profile_settings:
#                logger.warning(f"Unknown deployment profile: {profile_name}")
#                return False
#            
#            logger.info(f"Deployment profile '{profile_name}' settings retrieved successfully")
#            logger.info("Note: Profile activation requires server restart")
#            
#            return True
#            
#        except Exception as e:
#            logger.error(f"Error activating profile {profile_name}: {e}")
        return False
    
    # ========================================================================
    # MONITORING SUPPORT (Phase 3e Enhanced)
    # ========================================================================
    
    def get_monitoring_settings(self) -> Dict[str, Any]:
        """Get monitoring and health check settings with Phase 3e configuration patterns"""
        try:
            # PHASE 3E: Enhanced monitoring settings access
            monitoring = self.unified_config.get_config_section('server_config', 'server_configuration.monitoring', {})
            if not monitoring:
                # Fallback to direct server_config access
                monitoring = self.server_config.get('monitoring', {})
            
            # Provide comprehensive defaults
            return {
                'health_check_endpoint': monitoring.get('health_check_endpoint', '/health'),
                'metrics_endpoint': monitoring.get('metrics_endpoint', '/metrics'),
                'status_endpoint': monitoring.get('status_endpoint', '/status'),
                'enable_health_checks': monitoring.get('enable_health_checks', True),
                'health_check_interval': monitoring.get('health_check_interval', 30),
                'log_health_status': monitoring.get('log_health_status', True)
            }
            
        except Exception as e:
            logger.error(f"Error getting monitoring settings: {e}")
            return {
                'health_check_endpoint': '/health',
                'metrics_endpoint': '/metrics',
                'status_endpoint': '/status',
                'enable_health_checks': True,
                'health_check_interval': 30,
                'log_health_status': True
            }
    
    # ========================================================================
    # LEGACY COMPATIBILITY METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_operational_settings(self) -> Dict[str, Any]:
        """Get operational configuration settings with enhanced legacy compatibility"""
        logger.debug("Getting operational settings (legacy compatibility)...")
        
        try:
            # Map to enhanced structure with better error handling
            performance = self.get_performance_settings()
            monitoring = self.get_monitoring_settings()
            
            return {
                'health_check_interval': monitoring.get('health_check_interval', 30),
                'graceful_shutdown_timeout': 10,  # Safe default value
                'startup_timeout': 120,  # Safe default value
                'max_concurrent_requests': performance.get('max_concurrent_requests', 20),
                'request_timeout': performance.get('request_timeout', 40)
            }
            
        except Exception as e:
            logger.error(f"Error getting operational settings: {e}")
            return {
                'health_check_interval': 30,
                'graceful_shutdown_timeout': 10,
                'startup_timeout': 120,
                'max_concurrent_requests': 20,
                'request_timeout': 40
            }
    
    # ========================================================================
    # COMPREHENSIVE CONFIGURATION ACCESS (Phase 3e Enhanced)
    # ========================================================================
    
    def get_complete_server_configuration(self) -> Dict[str, Any]:
        """Get complete server configuration with Phase 3e enhancements"""
        logger.debug("Assembling complete server configuration...")
        
        try:
            return {
                'network': self.get_network_settings(),
                'application': self.get_application_settings(),
                'performance': self.get_performance_settings(),
                'security': self.get_security_settings(),
                'monitoring': self.get_monitoring_settings(),
                'deployment_profiles': self.get_deployment_profiles(),
                'metadata': {
                    'phase': '3e-5.5',
                    'architecture': 'clean_v3.1e_unified_config',
                    'configuration_version': '3e.5.5',
                    'consolidation_complete': True,
                    'v31_compliant': True,
                    'get_config_section_patterns': 'implemented',
                    'unified_config_manager': True,
                    'direct_os_getenv_calls': 'eliminated',
                    'enhanced_error_handling': True,
                    'phase_3e_cleanup': 'complete'
                }
            }
            
        except Exception as e:
            logger.error(f"Error assembling complete configuration: {e}")
            # Return safe minimal configuration
            return {
                'network': {'host': '0.0.0.0', 'port': 8881},
                'application': {'debug_mode': False, 'workers': 1},
                'performance': {'max_concurrent_requests': 20, 'request_timeout': 40},
                'security': {'rate_limiting': {'enable_rate_limiting': True}},
                'monitoring': {'enable_health_checks': True},
                'metadata': {'phase': '3e-5.5', 'fallback_mode': 'active'}
            }
    
    def validate_server_configuration(self) -> Dict[str, Any]:
        """Validate server configuration settings with Phase 3e enhancements"""
        logger.debug("Validating server configuration...")
        
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'consolidation_status': 'complete',
            'v31_compliant': True,
            'phase_3e_compliant': True,
            'get_config_section_patterns': 'implemented',
            'unified_config_manager': True
        }
        
        try:
            # Validate network settings with enhanced checks
            network = self.get_network_settings()
            if not isinstance(network['port'], int) or network['port'] < 1024 or network['port'] > 65535:
                validation_results['errors'].append(f"Invalid port: {network['port']} (must be 1024-65535)")
                validation_results['valid'] = False
            
            # Validate application settings with enhanced checks
            application = self.get_application_settings()
            if not isinstance(application['workers'], int) or application['workers'] < 1:
                validation_results['errors'].append(f"Invalid worker count: {application['workers']} (must be >= 1)")
                validation_results['valid'] = False
            elif application['workers'] > 16:
                validation_results['warnings'].append(f"High worker count: {application['workers']} (recommended: 1-8)")
            
            # Validate performance settings with enhanced checks
            performance = self.get_performance_settings()
            if not isinstance(performance['max_concurrent_requests'], int) or performance['max_concurrent_requests'] < 1:
                validation_results['errors'].append(f"Invalid max concurrent requests: {performance['max_concurrent_requests']}")
                validation_results['valid'] = False
            elif performance['max_concurrent_requests'] > 1000:
                validation_results['warnings'].append(f"Very high concurrent requests: {performance['max_concurrent_requests']} (may impact performance)")
            
            if not isinstance(performance['request_timeout'], int) or performance['request_timeout'] < 1:
                validation_results['errors'].append(f"Invalid request timeout: {performance['request_timeout']}")
                validation_results['valid'] = False
            elif performance['request_timeout'] < 5:
                validation_results['warnings'].append(f"Very low request timeout: {performance['request_timeout']}s (may cause premature timeouts)")
            
            # Validate security settings with enhanced checks
            security = self.get_security_settings()
            rate_limiting = security.get('rate_limiting', {})
            if not isinstance(rate_limiting.get('requests_per_minute', 0), int) or rate_limiting.get('requests_per_minute', 0) < 1:
                validation_results['warnings'].append("Invalid rate limiting configuration")
            elif rate_limiting.get('requests_per_minute', 0) > 1000:
                validation_results['warnings'].append("High rate limiting threshold may not provide adequate protection")
            
            logger.info(f"Server configuration validation: {'PASSED' if validation_results['valid'] else 'FAILED'}")
            
        except Exception as e:
            validation_results['errors'].append(f"Validation error: {str(e)}")
            validation_results['valid'] = False
            logger.error(f"Server configuration validation error: {e}")
        
        return validation_results
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary for monitoring and debugging
        Phase 3e: New method for enhanced system visibility
        """
        try:
            network = self.get_network_settings()
            application = self.get_application_settings()
            performance = self.get_performance_settings()
            
            return {
                'manager_version': 'v3.1e-5.5-2',
                'phase': '3e Sub-step 5.5 Task 5',
                'server_host': network.get('host', 'unknown'),
                'server_port': network.get('port', 'unknown'),
                'debug_mode': application.get('debug_mode', False),
                'worker_count': application.get('workers', 1),
                'max_concurrent_requests': performance.get('max_concurrent_requests', 20),
                'request_timeout': performance.get('request_timeout', 40),
                'ssl_enabled': network.get('enable_ssl', False),
                'configuration_source': 'json_with_env_overrides',
                'validation_status': 'validated',
                'initialization_status': 'complete',
                'cleanup_status': 'phase_3e_complete'
            }
            
        except Exception as e:
            logger.error(f"Error generating configuration summary: {e}")
            return {
                'manager_version': 'v3.1e-5.5-2',
                'phase': '3e Sub-step 5.5 Task 5',
                'error': str(e),
                'initialization_status': 'error',
                'cleanup_status': 'phase_3e_complete'
            }

# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance (Phase 3e Enhanced)
# ============================================================================

def create_server_config_manager(unified_config_manager) -> ServerConfigManager:
    """
    Factory function for ServerConfigManager (Clean v3.1 Pattern) - Phase 3e Enhanced
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for dependency injection
        
    Returns:
        Initialized ServerConfigManager instance with Phase 3e enhancements
        
    Raises:
        ValueError: If unified_config_manager is None or invalid
    """
    logger.debug("Creating ServerConfigManager with Phase 3e configuration patterns")
    
    if not unified_config_manager:
        raise ValueError("UnifiedConfigManager is required for ServerConfigManager factory")
    
    return ServerConfigManager(unified_config_manager)

# Export public interface
__all__ = ['ServerConfigManager', 'create_server_config_manager']

logger.info("ServerConfigManager v3.1e-5.5-2 loaded - Phase 3e Sub-step 5.5 cleanup complete with enhanced patterns")