# ash-nlp/__init__.py
"""
Ash NLP Service for Ash NLP Service
FILE VERSION: v3.1-3d-6-1
LAST MODIFIED: 2025-08-22
PHASE: 3d, Step 10.11-3
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CLEAN V3.1 ARCHITECTURE IMPORTS - Step 9.8 Complete
# ============================================================================

# STEP 9.8: Import UnifiedConfigManager instead of ConfigManager
try:
    from .managers import (
        UnifiedConfigManager, create_unified_config_manager,
        ModelEnsembleManager, create_model_ensemble_manager,
        PydanticManager, create_pydantic_manager,
        PatternDetectionManager, create_pattern_detection_manager,
        SettingsManager, create_settings_manager,
        get_manager_status
    )
    MANAGERS_AVAILABLE = True
    logger.debug("✅ Clean v3.1 managers imported successfully (Step 9.8)")
except ImportError as e:
    logger.error(f"❌ Clean v3.1 manager imports failed: {e}")
    # Set all to None for graceful degradation
    UnifiedConfigManager = None
    create_unified_config_manager = None
    ModelEnsembleManager = None
    create_model_ensemble_manager = None
    PydanticManager = None
    create_pydantic_manager = None
    PatternDetectionManager = None
    create_pattern_detection_manager = None
    SettingsManager = None
    create_settings_manager = None
    get_manager_status = None
    MANAGERS_AVAILABLE = False

# ============================================================================
# CLEAN V3.1 EXTERNAL API - Step 9.8 Updated
# ============================================================================

def get_pydantic_models():
    """
    Get Pydantic models for external usage
    
    Returns:
        Dictionary of available Pydantic models
        
    Raises:
        RuntimeError: If PydanticManager v3.1 not available
    """
    if not MANAGERS_AVAILABLE or not PydanticManager:
        raise RuntimeError(
            "Clean v3.1: PydanticManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # Create manager instance for model access
    from .managers import create_pydantic_manager
    pydantic_manager = create_pydantic_manager()
    
    if pydantic_manager and pydantic_manager.is_initialized():
        return pydantic_manager.get_core_models()
    else:
        raise RuntimeError(
            "Clean v3.1: PydanticManager failed to initialize. "
            "Check configuration and dependencies."
        )

def create_model_ensemble_manager():
    """
    Create ModelEnsembleManager instance with proper dependency injection
    
    Returns:
        ModelEnsembleManager instance for external usage
        
    Raises:
        RuntimeError: If ModelEnsembleManager not available
    """
    if not MANAGERS_AVAILABLE or not ModelEnsembleManager:
        raise RuntimeError(
            "Clean v3.1: ModelEnsembleManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # Import factory function
    from .managers import create_model_ensemble_manager as _create_model_ensemble_manager
    return _create_model_ensemble_manager()

def create_pattern_detection_manager_instance(config_manager=None):
    """
    Create PatternDetectionManager instance with proper dependency injection
    
    Args:
        config_manager: Optional UnifiedConfigManager instance. If None, creates one.
        
    Returns:
        PatternDetectionManager instance for external usage
        
    Raises:
        RuntimeError: If PatternDetectionManager v3.1 not available
    """
    if not MANAGERS_AVAILABLE or not PatternDetectionManager:
        raise RuntimeError(
            "Clean v3.1: PatternDetectionManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # STEP 9.8: Create UnifiedConfigManager if not provided
    if config_manager is None:
        if not UnifiedConfigManager:
            raise RuntimeError(
                "Clean v3.1: UnifiedConfigManager not available for PatternDetectionManager dependency injection."
            )
        
        # Use factory function to create UnifiedConfigManager
        config_manager = create_unified_config_manager()
    
    # Import factory function
    from .managers import create_pattern_detection_manager
    return create_pattern_detection_manager(config_manager)

def create_unified_config_manager_instance(config_dir: str = "/app/config"):
    """
    Create UnifiedConfigManager instance for external usage
    
    Args:
        config_dir: Configuration directory path
        
    Returns:
        UnifiedConfigManager instance
        
    Raises:
        RuntimeError: If UnifiedConfigManager not available
    """
    if not MANAGERS_AVAILABLE or not UnifiedConfigManager:
        raise RuntimeError(
            "Clean v3.1: UnifiedConfigManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # Import factory function
    from .managers import create_unified_config_manager
    return create_unified_config_manager(config_dir)

def get_system_status():
    """
    Get overall system status including all managers
    
    Returns:
        Dictionary containing system status information
    """
    if not MANAGERS_AVAILABLE:
        return {
            'status': 'error',
            'managers_available': False,
            'error': 'Clean v3.1 managers not available'
        }
    
    try:
        manager_status = get_manager_status() if get_manager_status else {}
        return {
            'status': 'operational',
            'managers_available': True,
            'architecture': 'Clean v3.1 Step 9.8',
            'configuration_system': 'UnifiedConfigManager',
            'manager_status': manager_status,
            'total_managers': len(manager_status),
            'available_managers': sum(manager_status.values())
        }
    except Exception as e:
        return {
            'status': 'error',
            'managers_available': True,
            'error': str(e)
        }

# ============================================================================
# STEP 9.8: UNIFIED CONFIGURATION EXPORTS
# ============================================================================

__all__ = [
    # Unified Configuration (Step 9.8)
    'UnifiedConfigManager',
    'create_unified_config_manager',
    'create_unified_config_manager_instance',
    
    # Core Managers
    'ModelEnsembleManager',
    'create_model_ensemble_manager',
    'PydanticManager',
    'create_pydantic_manager',
    'PatternDetectionManager',
    'create_pattern_detection_manager',
    'create_pattern_detection_manager_instance',
    'SettingsManager',
    'create_settings_manager',
    
    # External API Functions
    'get_pydantic_models',
    'get_system_status',
    'get_manager_status',
    
    # System Information
    'MANAGERS_AVAILABLE'
]

# ============================================================================
# STEP 9.8 COMPLETION LOG
# ============================================================================

logger.info("✅ Ash-NLP __init__.py Step 9.8 complete - ConfigManager eliminated, UnifiedConfigManager only")

if MANAGERS_AVAILABLE:
    logger.info("🎉 Step 9.8 SUCCESS: All managers available with UnifiedConfigManager architecture!")
else:
    logger.warning("⚠️ Step 9.8 INCOMPLETE: Manager imports failed")

logger.info("🏳️‍🌈 Ash-NLP v3.1 Step 9.8 ready to serve The Alphabet Cartel LGBTQIA+ community!")