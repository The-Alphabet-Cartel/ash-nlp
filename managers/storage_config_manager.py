# managers/storage_config_manager.py
"""
Storage Configuration Manager v3.1d Step 6
Manages storage, cache, backup, and file management configuration

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageConfigManager:
    """
    Storage Configuration Manager v3.1d Step 6
    Handles storage, cache, backup, and logging file configuration
    
    Features:
    - Directory management and validation
    - Cache configuration and cleanup settings
    - Backup and archival policies
    - Log rotation and file management
    - Environment variable overrides
    """
    
    def __init__(self, config_manager):
        """Initialize with UnifiedConfigManager for Clean v3.1 compliance"""
        self.config_manager = config_manager
        self.config = {}
        
        logger.info("🗄️ Initializing StorageConfigManager (Phase 3d Step 6)")
        
        try:
            # Load storage configuration from JSON
            self.config = self.config_manager.load_config('storage_settings')
            logger.info("✅ Loaded configuration: storage_settings from storage_settings.json")
            logger.info("✅ Storage configuration loaded from JSON with environment overrides")
            logger.info("StorageConfigManager v3.1d Step 6 initialized - UnifiedConfigManager integration complete")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not load storage_settings.json: {e}")
            logger.info("🔧 Using default storage configuration")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default storage configuration if JSON loading fails"""
        return {
            "directories": {
                "data_directory": "./data",
                "models_directory": "./models/cache", 
                "logs_directory": "./logs",
                "learning_directory": "./learning_data",
                "cache_directory": "./cache",
                "backup_directory": "./backups"
            },
            "cache_settings": {
                "enable_model_cache": True,
                "enable_analysis_cache": True,
                "cache_cleanup_on_startup": False,
                "model_cache_size_limit": 1000,
                "analysis_cache_size_limit": 500,
                "cache_expiry_hours": 24
            },
            "backup_settings": {
                "enable_automatic_backup": False,
                "backup_interval_hours": 24,
                "backup_retention_days": 30,
                "compress_backups": True,
                "backup_learning_data": True,
                "backup_configuration": True
            },
            "cleanup_settings": {
                "enable_automatic_cleanup": True,
                "cleanup_temp_files": True,
                "temp_file_max_age_hours": 48,
                "log_rotation_enabled": True,
                "log_max_size_mb": 100,
                "log_backup_count": 5
            }
        }
    
    # ========================================================================
    # Directory Management
    # ========================================================================
    
    def get_directories(self) -> Dict[str, str]:
        """Get all configured directories"""
        try:
            directories = self.config.get('directories', {})
            
            # Apply environment overrides
            result = {}
            for key, default_value in directories.items():
                env_var = f"NLP_STORAGE_{key.upper()}"
                result[key] = self.config_manager.get_env(env_var, default_value)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting directories: {e}")
            return self._get_default_config()['directories']
    
    def get_data_directory(self) -> str:
        """Get data directory path"""
        return self.get_directories().get('data_directory', './data')
    
    def get_models_directory(self) -> str:
        """Get models directory path"""
        return self.get_directories().get('models_directory', './models/cache')
    
    def get_logs_directory(self) -> str:
        """Get logs directory path"""
        return self.get_directories().get('logs_directory', './logs')
    
    def get_cache_directory(self) -> str:
        """Get cache directory path"""
        return self.get_directories().get('cache_directory', './cache')
    
    def get_backup_directory(self) -> str:
        """Get backup directory path"""
        return self.get_directories().get('backup_directory', './backups')
    
    def get_learning_directory(self) -> str:
        """Get learning data directory path"""
        return self.get_directories().get('learning_directory', './learning_data')
    
    # ========================================================================
    # Cache Configuration
    # ========================================================================
    
    def get_cache_settings(self) -> Dict[str, Any]:
        """Get cache configuration settings"""
        try:
            cache_settings = self.config.get('cache_settings', {})
            
            return {
                'enable_model_cache': self.config_manager.get_env('NLP_STORAGE_ENABLE_MODEL_CACHE', 
                                                                 cache_settings.get('enable_model_cache', True)),
                'enable_analysis_cache': self.config_manager.get_env('NLP_STORAGE_ENABLE_ANALYSIS_CACHE',
                                                                   cache_settings.get('enable_analysis_cache', True)),
                'cache_cleanup_on_startup': self.config_manager.get_env('NLP_STORAGE_CACHE_CLEANUP_ON_STARTUP',
                                                                       cache_settings.get('cache_cleanup_on_startup', False)),
                'model_cache_size_limit': self.config_manager.get_env('NLP_STORAGE_MODEL_CACHE_SIZE_LIMIT',
                                                                     cache_settings.get('model_cache_size_limit', 1000)),
                'analysis_cache_size_limit': self.config_manager.get_env('NLP_STORAGE_ANALYSIS_CACHE_SIZE_LIMIT',
                                                                        cache_settings.get('analysis_cache_size_limit', 500)),
                'cache_expiry_hours': self.config_manager.get_env('NLP_STORAGE_CACHE_EXPIRY_HOURS',
                                                                 cache_settings.get('cache_expiry_hours', 24))
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting cache settings: {e}")
            return self._get_default_config()['cache_settings']
    
    def is_model_cache_enabled(self) -> bool:
        """Check if model caching is enabled"""
        return self.get_cache_settings().get('enable_model_cache', True)
    
    def is_analysis_cache_enabled(self) -> bool:
        """Check if analysis caching is enabled"""
        return self.get_cache_settings().get('enable_analysis_cache', True)
    
    # ========================================================================
    # Backup Configuration
    # ========================================================================
    
    def get_backup_settings(self) -> Dict[str, Any]:
        """Get backup configuration settings"""
        try:
            backup_settings = self.config.get('backup_settings', {})
            
            return {
                'enable_automatic_backup': self.config_manager.get_env('NLP_STORAGE_ENABLE_AUTO_BACKUP',
                                                                       backup_settings.get('enable_automatic_backup', False)),
                'backup_interval_hours': self.config_manager.get_env('NLP_STORAGE_BACKUP_INTERVAL_HOURS',
                                                                    backup_settings.get('backup_interval_hours', 24)),
                'backup_retention_days': self.config_manager.get_env('NLP_STORAGE_BACKUP_RETENTION_DAYS',
                                                                    backup_settings.get('backup_retention_days', 30)),
                'compress_backups': self.config_manager.get_env('NLP_STORAGE_COMPRESS_BACKUPS',
                                                               backup_settings.get('compress_backups', True)),
                'backup_learning_data': self.config_manager.get_env('NLP_STORAGE_BACKUP_LEARNING_DATA',
                                                                   backup_settings.get('backup_learning_data', True)),
                'backup_configuration': self.config_manager.get_env('NLP_STORAGE_BACKUP_CONFIG',
                                                                   backup_settings.get('backup_configuration', True))
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting backup settings: {e}")
            return self._get_default_config()['backup_settings']
    
    def is_automatic_backup_enabled(self) -> bool:
        """Check if automatic backup is enabled"""
        return self.get_backup_settings().get('enable_automatic_backup', False)
    
    # ========================================================================
    # Cleanup Configuration
    # ========================================================================
    
    def get_cleanup_settings(self) -> Dict[str, Any]:
        """Get cleanup configuration settings"""
        try:
            cleanup_settings = self.config.get('cleanup_settings', {})
            
            return {
                'enable_automatic_cleanup': self.config_manager.get_env('NLP_STORAGE_ENABLE_AUTO_CLEANUP',
                                                                        cleanup_settings.get('enable_automatic_cleanup', True)),
                'cleanup_temp_files': self.config_manager.get_env('NLP_STORAGE_CLEANUP_TEMP_FILES',
                                                                 cleanup_settings.get('cleanup_temp_files', True)),
                'temp_file_max_age_hours': self.config_manager.get_env('NLP_STORAGE_TEMP_FILE_MAX_AGE',
                                                                      cleanup_settings.get('temp_file_max_age_hours', 48)),
                'log_rotation_enabled': self.config_manager.get_env('NLP_STORAGE_LOG_ROTATION_ENABLED',
                                                                   cleanup_settings.get('log_rotation_enabled', True)),
                'log_max_size_mb': self.config_manager.get_env('NLP_STORAGE_LOG_MAX_SIZE_MB',
                                                              cleanup_settings.get('log_max_size_mb', 100)),
                'log_backup_count': self.config_manager.get_env('NLP_STORAGE_LOG_BACKUP_COUNT',
                                                               cleanup_settings.get('log_backup_count', 5))
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting cleanup settings: {e}")
            return self._get_default_config()['cleanup_settings']
    
    def is_automatic_cleanup_enabled(self) -> bool:
        """Check if automatic cleanup is enabled"""
        return self.get_cleanup_settings().get('enable_automatic_cleanup', True)
    
    # ========================================================================
    # Validation and Status
    # ========================================================================
    
    def validate_directories(self) -> Dict[str, bool]:
        """Validate that all configured directories exist or can be created"""
        directories = self.get_directories()
        validation_results = {}
        
        for name, path in directories.items():
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
                validation_results[name] = True
                logger.debug(f"✅ Directory validated: {name} -> {path}")
            except Exception as e:
                validation_results[name] = False
                logger.warning(f"⚠️ Directory validation failed: {name} -> {path}: {e}")
        
        return validation_results
    
    def get_status(self) -> Dict[str, Any]:
        """Get storage configuration manager status"""
        try:
            directories = self.get_directories()
            cache_settings = self.get_cache_settings()
            backup_settings = self.get_backup_settings()
            cleanup_settings = self.get_cleanup_settings()
            
            return {
                'version': 'v3.1d_step_6',
                'config_manager': 'UnifiedConfigManager',
                'status': 'operational',
                'directories_configured': len(directories),
                'directory_names': list(directories.keys()),
                'model_cache_enabled': cache_settings.get('enable_model_cache', True),
                'analysis_cache_enabled': cache_settings.get('enable_analysis_cache', True),
                'automatic_backup_enabled': backup_settings.get('enable_automatic_backup', False),
                'automatic_cleanup_enabled': cleanup_settings.get('enable_automatic_cleanup', True),
                'configuration_source': 'storage_settings.json'
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting status: {e}")
            return {
                'version': 'v3.1d_step_6',
                'status': 'error',
                'error': str(e)
            }
    
    # ========================================================================
    # Complete Configuration Access
    # ========================================================================
    
    def get_complete_configuration(self) -> Dict[str, Any]:
        """Get complete storage configuration for debugging"""
        return {
            'directories': self.get_directories(),
            'cache_settings': self.get_cache_settings(),
            'backup_settings': self.get_backup_settings(),
            'cleanup_settings': self.get_cleanup_settings(),
            'directory_validation': self.validate_directories(),
            'status': self.get_status()
        }


def create_storage_config_manager(config_manager) -> StorageConfigManager:
    """
    Factory function for StorageConfigManager - Clean v3.1 Compliance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        StorageConfigManager instance
    """
    return StorageConfigManager(config_manager)


__all__ = ['StorageConfigManager', 'create_storage_config_manager']