# ash/ash-nlp/managers/__init__.py
"""
Managers Package for Ash NLP Service v3.1 - Clean Architecture Only
No backward compatibility - forward-looking manager-only architecture
"""

import logging

logger = logging.getLogger(__name__)

# Import new clean manager classes
try:
    from .config_manager import ConfigManager
    CONFIG_MANAGER_AVAILABLE = True
    logger.info("✅ ConfigManager available (clean architecture)")
except ImportError as e:
    CONFIG_MANAGER_AVAILABLE = False
    logger.error(f"❌ ConfigManager import failed: {e}")

try:
    from .settings_manager import SettingsManager
    SETTINGS_MANAGER_AVAILABLE = True
    logger.info("✅ SettingsManager available (clean architecture)")
except ImportError as e:
    SETTINGS_MANAGER_AVAILABLE = False
    logger.error(f"❌ SettingsManager import failed: {e}")

try:
    from .zero_shot_manager import ZeroShotManager
    ZERO_SHOT_MANAGER_AVAILABLE = True
    logger.info("✅ ZeroShotManager available (clean architecture)")
except ImportError as e:
    ZERO_SHOT_MANAGER_AVAILABLE = False
    logger.error(f"❌ ZeroShotManager import failed: {e}")

# Manager status for clean architecture
MANAGERS_STATUS = {
    "config_manager": CONFIG_MANAGER_AVAILABLE,
    "settings_manager": SETTINGS_MANAGER_AVAILABLE, 
    "zero_shot_manager": ZERO_SHOT_MANAGER_AVAILABLE
}

def get_managers_status():
    """Get status of all manager classes"""
    return MANAGERS_STATUS.copy()

def validate_managers():
    """Validate that all required managers are available"""
    if not CONFIG_MANAGER_AVAILABLE:
        raise ImportError("ConfigManager is required but not available")
    
    if not SETTINGS_MANAGER_AVAILABLE:
        raise ImportError("SettingsManager is required but not available")
    
    if not ZERO_SHOT_MANAGER_AVAILABLE:
        raise ImportError("ZeroShotManager is required but not available")
    
    logger.info("✅ All required managers validated")

# Export clean manager classes
__all__ = [
    'ConfigManager',
    'SettingsManager', 
    'ZeroShotManager',
    'MANAGERS_STATUS',
    'get_managers_status',
    'validate_managers'
]

# Log clean architecture initialization
logger.info("📦 Clean Manager Architecture initialized")
for manager_name, available in MANAGERS_STATUS.items():
    status = "✅ Available" if available else "❌ Failed"
    logger.info(f"   {manager_name}: {status}")

if all(MANAGERS_STATUS.values()):
    logger.info("🎯 All managers loaded successfully - clean architecture ready")
else:
    failed_managers = [name for name, status in MANAGERS_STATUS.items() if not status]
    logger.warning(f"⚠️ Failed managers: {failed_managers}")