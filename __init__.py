# ash-nlp/__init__.py - Clean v3.1 Package Initialization
"""
Ash NLP Service - v3.1 Clean Architecture
Step 9.8: ConfigManager Eliminated - UnifiedConfigManager Only

Mental health crisis detection for The Alphabet Cartel LGBTQIA+ community.
Uses Clean v3.1 architecture with unified configuration management.
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
        ModelsManager, create_models_manager,
        PydanticManager, create_pydantic_manager,
        CrisisPatternManager, create_crisis_pattern_manager,
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
    ModelsManager = None
    create_models_manager = None
    PydanticManager = None
    create_pydantic_manager = None
    CrisisPatternManager = None
    create_crisis_pattern_manager = None
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

def create_models_manager():
    """
    Create ModelsManager instance with proper dependency injection
    
    Returns:
        ModelsManager instance for external usage
        
    Raises:
        RuntimeError: If ModelsManager v3.1 not available
    """
    if not MANAGERS_AVAILABLE or not ModelsManager:
        raise RuntimeError(
            "Clean v3.1: ModelsManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # Import factory function
    from .managers import create_models_manager as _create_models_manager
    return _create_models_manager()

def create_crisis_pattern_manager_instance(config_manager=None):
    """
    Create CrisisPatternManager instance with proper dependency injection
    
    Args:
        config_manager: Optional UnifiedConfigManager instance. If None, creates one.
        
    Returns:
        CrisisPatternManager instance for external usage
        
    Raises:
        RuntimeError: If CrisisPatternManager v3.1 not available
    """
    if not MANAGERS_AVAILABLE or not CrisisPatternManager:
        raise RuntimeError(
            "Clean v3.1: CrisisPatternManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # STEP 9.8: Create UnifiedConfigManager if not provided
    if config_manager is None:
        if not UnifiedConfigManager:
            raise RuntimeError(
                "Clean v3.1: UnifiedConfigManager not available for CrisisPatternManager dependency injection."
            )
        
        # Use factory function to create UnifiedConfigManager
        config_manager = create_unified_config_manager()
    
    # Import factory function
    from .managers import create_crisis_pattern_manager
    return create_crisis_pattern_manager(config_manager)

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
    'ModelsManager',
    'create_models_manager',
    'PydanticManager',
    'create_pydantic_manager',
    'CrisisPatternManager',
    'create_crisis_pattern_manager',
    'create_crisis_pattern_manager_instance',
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