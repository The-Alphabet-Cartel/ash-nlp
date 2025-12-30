# ash-nlp/managers/storage_config_manager.py
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
Storage Configuration Manager for Ash NLP Service
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageConfigManager:
    """
    Storage Configuration Manager - OPTIMIZED with Enhanced Configuration Access

    MIGRATION NOTICE: Directory validation utilities moved to SharedUtilitiesManager.
    Configuration access updated to use enhanced UnifiedConfigManager patterns.

    This manager focuses on:
    - Directory management and configuration
    - Cache settings and policies
    - Backup configuration
    - Cleanup and maintenance settings
    - Environment variable integration
    """

    def __init__(self, config_manager):
        """Initialize with UnifiedConfigManager for Clean v3.1 compliance"""
        from .shared_utilities import SharedUtilitiesManager

        self.config_manager = config_manager
        shared_utils = SharedUtilitiesManager(config_manager)

        self.config = {}

        logger.info("StorageConfigManager v3.1e optimized initializing...")

        try:
            # UPDATED: Use get_config_section instead of load_config_file
            self.config = self.config_manager.get_config_section("storage_settings")

            if self.config:
                logger.info(
                    "Storage configuration loaded from JSON with environment overrides"
                )
            else:
                logger.info("Using default storage configuration")
                self.config = self._get_default_config()

            logger.info("StorageConfigManager v3.1e optimization complete")

        except Exception as e:
            logger.warning(f"Could not load storage_settings.json: {e}")
            logger.info("Using default storage configuration")
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default storage configuration if JSON loading fails"""
        return {
            "directories": {
                "data_directory": "./data",
                "models_directory": "./cache/models",
                "logs_directory": "./logs",
                "learning_directory": "./data/learning",
                "cache_directory": "./cache",
                "backup_directory": "./backups",
            },
            "cache_settings": {
                "enable_model_cache": True,
                "enable_analysis_cache": False,
                "cache_cleanup_on_startup": False,
                "model_cache_size_limit": 1000,
                "analysis_cache_size_limit": 500,
                "cache_expiry_hours": 24,
            },
            "backup_settings": {
                "enable_automatic_backup": False,
                "backup_interval_hours": 24,
                "backup_retention_days": 30,
                "compress_backups": True,
                "backup_learning_data": True,
                "backup_configuration": True,
            },
            "cleanup_settings": {
                "enable_automatic_cleanup": True,
                "cleanup_temp_files": True,
                "temp_file_max_age_hours": 48,
                "log_rotation_enabled": True,
                "log_max_size_mb": 100,
                "log_backup_count": 5,
            },
        }

    # ========================================================================
    # DIRECTORY MANAGEMENT - CORE RESPONSIBILITY
    # ========================================================================

    def get_directories(self) -> Dict[str, str]:
        """Get all configured directories with environment overrides"""
        try:
            directories = self.config.get("directories", {})

            # Apply environment overrides using enhanced pattern
            result = {}
            for key, default_value in directories.items():
                env_var = f"NLP_STORAGE_{key.upper()}"
                result[key] = self.config_manager.get_env_str(env_var, default_value)

            return result

        except Exception as e:
            logger.error(f"Error getting directories: {e}")
            return self._get_default_config()["directories"]

    def get_data_directory(self) -> str:
        """Get data directory path"""
        return self.get_directories().get("data_directory", "./data")

    def get_models_directory(self) -> str:
        """Get models directory path"""
        return self.get_directories().get("models_directory", "./cache/models")

    def get_logs_directory(self) -> str:
        """Get logs directory path"""
        return self.get_directories().get("logs_directory", "./logs")

    def get_cache_directory(self) -> str:
        """Get cache directory path"""
        return self.get_directories().get("cache_directory", "./cache")

    def get_backup_directory(self) -> str:
        """Get backup directory path"""
        return self.get_directories().get("backup_directory", "./backups")

    def get_learning_directory(self) -> str:
        """Get learning data directory path"""
        return self.get_directories().get("learning_directory", "./data/learning")

    # ========================================================================
    # CONSOLIDATED SETTINGS ACCESS
    # ========================================================================

    def get_cache_settings(self) -> Dict[str, Any]:
        """Get cache configuration settings with environment overrides"""
        try:
            cache_settings = self.config.get("cache_settings", {})

            return {
                "enable_model_cache": self.config_manager.get_env_bool(
                    "NLP_STORAGE_ENABLE_MODEL_CACHE",
                    cache_settings.get("enable_model_cache", True),
                ),
                "enable_analysis_cache": self.config_manager.get_env_bool(
                    "NLP_STORAGE_ENABLE_ANALYSIS_CACHE",
                    cache_settings.get("enable_analysis_cache", False),
                ),
                "cache_cleanup_on_startup": self.config_manager.get_env_bool(
                    "NLP_STORAGE_CACHE_CLEANUP_ON_STARTUP",
                    cache_settings.get("cache_cleanup_on_startup", False),
                ),
                "model_cache_size_limit": self.config_manager.get_env_int(
                    "NLP_STORAGE_MODEL_CACHE_SIZE_LIMIT",
                    cache_settings.get("model_cache_size_limit", 1000),
                ),
                "analysis_cache_size_limit": self.config_manager.get_env_int(
                    "NLP_STORAGE_ANALYSIS_CACHE_SIZE_LIMIT",
                    cache_settings.get("analysis_cache_size_limit", 500),
                ),
                "cache_expiry_hours": self.config_manager.get_env_int(
                    "NLP_STORAGE_CACHE_EXPIRY_HOURS",
                    cache_settings.get("cache_expiry_hours", 24),
                ),
            }

        except Exception as e:
            logger.error(f"Error getting cache settings: {e}")
            return self._get_default_config()["cache_settings"]

    def get_backup_settings(self) -> Dict[str, Any]:
        """Get backup configuration settings with environment overrides"""
        try:
            backup_settings = self.config.get("backup_settings", {})

            return {
                "enable_automatic_backup": self.config_manager.get_env_bool(
                    "NLP_STORAGE_ENABLE_AUTO_BACKUP",
                    backup_settings.get("enable_automatic_backup", False),
                ),
                "backup_interval_hours": self.config_manager.get_env_int(
                    "NLP_STORAGE_BACKUP_INTERVAL_HOURS",
                    backup_settings.get("backup_interval_hours", 24),
                ),
                "backup_retention_days": self.config_manager.get_env_int(
                    "NLP_STORAGE_BACKUP_RETENTION_DAYS",
                    backup_settings.get("backup_retention_days", 30),
                ),
                "compress_backups": self.config_manager.get_env_bool(
                    "NLP_STORAGE_COMPRESS_BACKUPS",
                    backup_settings.get("compress_backups", True),
                ),
                "backup_learning_data": self.config_manager.get_env_bool(
                    "NLP_STORAGE_BACKUP_LEARNING_DATA",
                    backup_settings.get("backup_learning_data", True),
                ),
                "backup_configuration": self.config_manager.get_env_bool(
                    "NLP_STORAGE_BACKUP_CONFIG",
                    backup_settings.get("backup_configuration", True),
                ),
            }

        except Exception as e:
            logger.error(f"Error getting backup settings: {e}")
            return self._get_default_config()["backup_settings"]

    def get_cleanup_settings(self) -> Dict[str, Any]:
        """Get cleanup configuration settings with environment overrides"""
        try:
            cleanup_settings = self.config.get("cleanup_settings", {})

            return {
                "enable_automatic_cleanup": self.config_manager.get_env_bool(
                    "NLP_STORAGE_ENABLE_AUTO_CLEANUP",
                    cleanup_settings.get("enable_automatic_cleanup", True),
                ),
                "cleanup_temp_files": self.config_manager.get_env_bool(
                    "NLP_STORAGE_CLEANUP_TEMP_FILES",
                    cleanup_settings.get("cleanup_temp_files", True),
                ),
                "temp_file_max_age_hours": self.config_manager.get_env_int(
                    "NLP_STORAGE_TEMP_FILE_MAX_AGE",
                    cleanup_settings.get("temp_file_max_age_hours", 48),
                ),
                "log_rotation_enabled": self.config_manager.get_env_bool(
                    "NLP_STORAGE_LOG_ROTATION_ENABLED",
                    cleanup_settings.get("log_rotation_enabled", True),
                ),
                "log_max_size_mb": self.config_manager.get_env_int(
                    "NLP_STORAGE_LOG_MAX_SIZE_MB",
                    cleanup_settings.get("log_max_size_mb", 100),
                ),
                "log_backup_count": self.config_manager.get_env_int(
                    "NLP_STORAGE_LOG_BACKUP_COUNT",
                    cleanup_settings.get("log_backup_count", 5),
                ),
            }

        except Exception as e:
            logger.error(f"Error getting cleanup settings: {e}")
            return self._get_default_config()["cleanup_settings"]

    # ========================================================================
    # INDIVIDUAL SETTING ACCESS (BACKWARD COMPATIBILITY)
    # ========================================================================

    def is_model_cache_enabled(self) -> bool:
        """Check if model caching is enabled"""
        return self.get_cache_settings().get("enable_model_cache", True)

    def is_analysis_cache_enabled(self) -> bool:
        """Check if analysis caching is enabled"""
        return self.get_cache_settings().get("enable_analysis_cache", False)

    def is_automatic_backup_enabled(self) -> bool:
        """Check if automatic backup is enabled"""
        return self.get_backup_settings().get("enable_automatic_backup", False)

    def is_automatic_cleanup_enabled(self) -> bool:
        """Check if automatic cleanup is enabled"""
        return self.get_cleanup_settings().get("enable_automatic_cleanup", True)

    # ========================================================================
    # STATUS AND COMPREHENSIVE ACCESS
    # ========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get storage configuration manager status"""
        try:
            directories = self.get_directories()
            cache_settings = self.get_cache_settings()
            backup_settings = self.get_backup_settings()
            cleanup_settings = self.get_cleanup_settings()

            return {
                "version": "v3.1e_optimized",
                "config_manager": "UnifiedConfigManager",
                "status": "operational",
                "optimization_applied": True,
                "directories_configured": len(directories),
                "directory_names": list(directories.keys()),
                "model_cache_enabled": cache_settings.get("enable_model_cache", True),
                "analysis_cache_enabled": cache_settings.get(
                    "enable_analysis_cache", False
                ),
                "automatic_backup_enabled": backup_settings.get(
                    "enable_automatic_backup", False
                ),
                "automatic_cleanup_enabled": cleanup_settings.get(
                    "enable_automatic_cleanup", True
                ),
                "configuration_source": "storage_settings.json",
            }

        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {"version": "v3.1e_optimized", "status": "error", "error": str(e)}

    def get_complete_configuration(self) -> Dict[str, Any]:
        """Get complete storage configuration for debugging"""
        return {
            "directories": self.get_directories(),
            "cache_settings": self.get_cache_settings(),
            "backup_settings": self.get_backup_settings(),
            "cleanup_settings": self.get_cleanup_settings(),
            "directory_validation": self.shared_utils.validate_directories(),
            "status": self.get_status(),
        }


# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================


def create_storage_config_manager(config_manager) -> StorageConfigManager:
    """
    Factory function for StorageConfigManager - Clean v3.1 Compliance

    Args:
        config_manager: UnifiedConfigManager instance

    Returns:
        StorageConfigManager instance
    """
    return StorageConfigManager(config_manager)


__all__ = ["StorageConfigManager", "create_storage_config_manager"]
