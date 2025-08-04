# ash/ash-nlp/managers/__init__.py (Clean v3.1 Architecture - Phase 3a Updated)
"""
Ash NLP Service Managers - Clean v3.1 Architecture
Phase 3a: Crisis Pattern Manager Integration Complete

Provides centralized access to all manager components following clean v3.1 patterns.
All managers use dependency injection and fail-fast design.
"""

import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CLEAN V3.1 MANAGER IMPORTS - Phase 3a Updated
# ============================================================================

# Core Configuration Managers
try:
    from .config_manager import ConfigManager
    from .settings_manager import SettingsManager, create_settings_manager
    from .zero_shot_manager import ZeroShotManager
    CONFIG_MANAGERS_AVAILABLE = True
    logger.debug("✅ Core configuration managers imported")
except ImportError as e:
    logger.error(f"❌ Core configuration manager imports failed: {e}")
    ConfigManager = None
    SettingsManager = None
    create_settings_manager = None
    ZeroShotManager = None
    CONFIG_MANAGERS_AVAILABLE = False

# ML Model Managers (Phase 2A)
try:
    from .models_manager import ModelsManager, create_model_manager
    MODELS_MANAGER_AVAILABLE = True
    logger.debug("✅ ModelsManager v3.1 imported (Phase 2A)")
except ImportError as e:
    logger.error(f"❌ ModelsManager v3.1 import failed: {e}")
    ModelsManager = None
    create_model_manager = None
    MODELS_MANAGER_AVAILABLE = False

# Pydantic Model Managers (Phase 2B)
try:
    from .pydantic_manager import PydanticManager, create_pydantic_manager
    PYDANTIC_MANAGER_AVAILABLE = True
    logger.debug("✅ PydanticManager v3.1 imported (Phase 2B)")
except ImportError as e:
    logger.error(f"❌ PydanticManager v3.1 import failed: {e}")
    PydanticManager = None
    create_pydantic_manager = None
    PYDANTIC_MANAGER_AVAILABLE = False

# Crisis Pattern Manager (Phase 3a) 
try:
    from .crisis_pattern_manager import CrisisPatternManager, create_crisis_pattern_manager
    CRISIS_PATTERN_MANAGER_AVAILABLE = True
    logger.debug("✅ CrisisPatternManager v3.1 imported (Phase 3a)")
except ImportError as e:
    logger.error(f"❌ CrisisPatternManager v3.1 import failed: {e}")
    CrisisPatternManager = None
    create_crisis_pattern_manager = None
    CRISIS_PATTERN_MANAGER_AVAILABLE = False

# ============================================================================
# MANAGER AVAILABILITY STATUS
# ============================================================================

MANAGERS_AVAILABLE = all([
    CONFIG_MANAGERS_AVAILABLE,
    MODELS_MANAGER_AVAILABLE,
    PYDANTIC_MANAGER_AVAILABLE,
    CRISIS_PATTERN_MANAGER_AVAILABLE
])

SERVICE_INFO = {
    "service": "Ash NLP Service",
    "version": "3.1.0",
    "architecture": "clean_v3.1_phase_3a_complete",
    "description": "Enhanced Mental Health Crisis Detection with Crisis Pattern Manager",
    "phases_complete": ["2A", "2B", "2C", "3a"],
    "managers": {
        "config_managers": CONFIG_MANAGERS_AVAILABLE,
        "models_manager_v3_1": MODELS_MANAGER_AVAILABLE,
        "pydantic_manager_v3_1": PYDANTIC_MANAGER_AVAILABLE,
        "crisis_pattern_manager_v3_1": CRISIS_PATTERN_MANAGER_AVAILABLE
    }
}

# ============================================================================
# SERVICE INFORMATION FUNCTIONS
# ============================================================================

def get_service_info():
    """Get comprehensive service information"""
    return SERVICE_INFO

def get_version_info():
    """Get version and architecture information"""
    return {
        "version": "3.1.0",
        "architecture": "clean_v3.1_phase_3a_complete",
        "phase_status": {
            "phase_2a_models_manager": "complete",
            "phase_2b_pydantic_manager": "complete", 
            "phase_2c_cleanup": "complete",
            "phase_3a_crisis_patterns": "complete"
        },
        "backward_compatibility": "removed_phase_2c",
        "manager_integration": {
            "config_manager": ConfigManager is not None,
            "settings_manager": SettingsManager is not None,
            "zero_shot_manager": ZeroShotManager is not None,
            "models_manager_v3_1": ModelsManager is not None,
            "pydantic_manager_v3_1": PydanticManager is not None,
            "crisis_pattern_manager_v3_1": CrisisPatternManager is not None
        }
    }

def get_manager_status():
    """Get detailed manager availability status for clean v3.1 architecture"""
    return {
        "managers_available": MANAGERS_AVAILABLE,
        "architecture": "clean_v3.1_phase_3a_complete",
        "manager_components": {
            "ConfigManager": ConfigManager is not None,
            "SettingsManager": SettingsManager is not None,
            "ZeroShotManager": ZeroShotManager is not None,
            "ModelsManager_v3_1": ModelsManager is not None,
            "PydanticManager_v3_1": PydanticManager is not None,
            "CrisisPatternManager_v3_1": CrisisPatternManager is not None
        },
        "phase_status": {
            "phase_2a_models_manager": "complete",
            "phase_2b_pydantic_manager": "complete",
            "phase_2c_cleanup": "complete",
            "phase_3a_crisis_patterns": "complete"
        },
        "usage_notes": {
            "manager_initialization": "Use create_*_manager() factory functions with dependency injection",
            "direct_access_only": "No global functions or legacy imports",
            "fail_fast_design": "Clear errors when managers unavailable",
            "crisis_patterns": "Use create_crisis_pattern_manager(config_manager) for pattern access"
        }
    }

# ============================================================================
# CLEAN V3.1 PUBLIC API - Phase 3a Updated
# ============================================================================

__all__ = [
    # Core Configuration Managers
    "ConfigManager",
    "SettingsManager", 
    "create_settings_manager",
    "ZeroShotManager",
    
    # ML Model Managers (Phase 2A)
    "ModelsManager",
    "create_model_manager",
    
    # Pydantic Model Managers (Phase 2B) 
    "PydanticManager",
    "create_pydantic_manager",
    
    # Crisis Pattern Manager (Phase 3a)
    "CrisisPatternManager",
    "create_crisis_pattern_manager",
    
    # Service info functions
    "SERVICE_INFO",
    "get_service_info",
    "get_version_info",
    "get_manager_status",
    
    # Status flags
    "MANAGERS_AVAILABLE",
    "CONFIG_MANAGERS_AVAILABLE",
    "MODELS_MANAGER_AVAILABLE", 
    "PYDANTIC_MANAGER_AVAILABLE",
    "CRISIS_PATTERN_MANAGER_AVAILABLE"
]

# ============================================================================
# CLEAN V3.1 PHASE 3A INITIALIZATION COMPLETE
# ============================================================================

# Log initialization status
if MANAGERS_AVAILABLE:
    logger.info("✅ Ash NLP Service v3.1 - Clean Manager Architecture with Crisis Patterns initialized")
    logger.info("🎉 Phase 3a Complete - Crisis Pattern Manager integrated")
    logger.debug(f"📊 Managers available: {sum(1 for flag in [CONFIG_MANAGERS_AVAILABLE, MODELS_MANAGER_AVAILABLE, PYDANTIC_MANAGER_AVAILABLE, CRISIS_PATTERN_MANAGER_AVAILABLE] if flag)}/4 manager groups")
else:
    # Managers not available - log warning but don't fail import
    logger.warning("⚠️ Ash NLP Service v3.1 - Some managers not available")
    logger.warning("💡 Check managers/ directory for proper installation")
    if not CRISIS_PATTERN_MANAGER_AVAILABLE:
        logger.warning("🔍 CrisisPatternManager not available - Phase 3a integration incomplete")