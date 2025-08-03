"""
Debug Logging Helper for Ash NLP Service
Conditional debug logging that respects GLOBAL_ENABLE_DEBUG_MODE
"""

import os
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

class DebugLogger:
    """Conditional debug logger that respects debug mode configuration"""
    
    def __init__(self, config_manager=None):
        """Initialize debug logger with optional config manager"""
        self.config_manager = config_manager
        self._debug_enabled = None
        self._debug_config = None
        self._load_debug_config()
    
    def _load_debug_config(self):
        """Load debug configuration from JSON + ENV"""
        # Check environment variable first (immediate override)
        env_debug = os.getenv('GLOBAL_ENABLE_DEBUG_MODE', 'false').lower()
        self._debug_enabled = env_debug in ('true', '1', 'yes', 'on')
        
        # Try to load JSON configuration if available
        if self.config_manager:
            try:
                debug_config_file = "/app/config/debug_settings.json"
                if os.path.exists(debug_config_file):
                    import json
                    with open(debug_config_file, 'r') as f:
                        debug_config_raw = json.load(f)
                    
                    self._debug_config = debug_config_raw.get("debug_settings", {})
                    # ENV variables take precedence over JSON
                    json_debug = self._debug_config.get("enabled", "false")
                    if isinstance(json_debug, str) and json_debug.startswith("${"):
                        # Use environment variable (already loaded above)
                        pass
                    else:
                        # Use JSON value if no ENV override
                        if os.getenv('GLOBAL_ENABLE_DEBUG_MODE') is None:
                            self._debug_enabled = str(json_debug).lower() in ('true', '1', 'yes', 'on')
                    
                    logger.info(f"🔧 Debug configuration loaded: enabled={self._debug_enabled}")
                else:
                    logger.info(f"📁 Debug config file not found, using environment: enabled={self._debug_enabled}")
            except Exception as e:
                logger.warning(f"⚠️ Could not load debug configuration: {e}")
        else:
            logger.info(f"🔧 Debug mode from environment: enabled={self._debug_enabled}")
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled"""
        return self._debug_enabled
    
    def debug_info(self, message: str, *args, **kwargs):
        """Log info-level debug message only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def debug_detail(self, message: str, *args, **kwargs):
        """Log detailed debug information only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def debug_config(self, message: str, *args, **kwargs):
        """Log configuration debug information only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def debug_substitution(self, message: str, *args, **kwargs):
        """Log variable substitution debug information only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def debug_model(self, message: str, *args, **kwargs):
        """Log model loading debug information only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def debug_manager(self, message: str, *args, **kwargs):
        """Log manager initialization debug information only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def debug_validation(self, message: str, *args, **kwargs):
        """Log validation debug information only if debug mode is enabled"""
        if self._debug_enabled:
            logger.info(message, *args, **kwargs)
    
    def production_info(self, message: str, *args, **kwargs):
        """Always log important production information regardless of debug mode"""
        logger.info(message, *args, **kwargs)
    
    def production_success(self, message: str, *args, **kwargs):
        """Always log success information regardless of debug mode"""
        logger.info(message, *args, **kwargs)
    
    def production_warning(self, message: str, *args, **kwargs):
        """Always log warnings regardless of debug mode"""
        logger.warning(message, *args, **kwargs)
    
    def production_error(self, message: str, *args, **kwargs):
        """Always log errors regardless of debug mode"""
        logger.error(message, *args, **kwargs)

# Global debug logger instance
_debug_logger = None

def get_debug_logger(config_manager=None) -> DebugLogger:
    """Get global debug logger instance"""
    global _debug_logger
    if _debug_logger is None:
        _debug_logger = DebugLogger(config_manager)
    return _debug_logger

def set_debug_logger(config_manager):
    """Set debug logger with config manager (called during startup)"""
    global _debug_logger
    _debug_logger = DebugLogger(config_manager)
    return _debug_logger

# Convenience functions for common debug patterns
def debug_info(message: str, *args, **kwargs):
    """Log debug info if debug mode is enabled"""
    get_debug_logger().debug_info(message, *args, **kwargs)

def debug_config(message: str, *args, **kwargs):
    """Log debug configuration if debug mode is enabled"""
    get_debug_logger().debug_config(message, *args, **kwargs)

def debug_substitution(message: str, *args, **kwargs):
    """Log debug substitution if debug mode is enabled"""
    get_debug_logger().debug_substitution(message, *args, **kwargs)

def debug_model(message: str, *args, **kwargs):
    """Log debug model info if debug mode is enabled"""
    get_debug_logger().debug_model(message, *args, **kwargs)

def production_info(message: str, *args, **kwargs):
    """Always log production info"""
    get_debug_logger().production_info(message, *args, **kwargs)

def production_success(message: str, *args, **kwargs):
    """Always log production success"""
    get_debug_logger().production_success(message, *args, **kwargs)

def is_debug_enabled() -> bool:
    """Check if debug mode is enabled"""
    return get_debug_logger().is_debug_enabled()