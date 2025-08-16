# ash-nlp/__init__.py
"""
Ash NLP Service for Ash NLP Service
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-15
PHASE: 3d Step 10.11-3 - Models Manager Consolidation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

STEP 10.11-3 CHANGE: Removed create_models_manager and ModelsManager imports.
All model functionality now consolidated into ModelEnsembleManager.
"""

import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CLEAN V3.1 ARCHITECTURE IMPORTS - Step 10.11-3 Models Manager Consolidation
# ============================================================================

# STEP 10.11-3: Import ModelEnsembleManager instead of ModelsManager
try:
    from .managers import (
        UnifiedConfigManager, create_unified_config_manager,
        ModelEnsembleManager, create_model_ensemble_manager,  # UPDATED: Consolidated model manager
        PydanticManager, create_pydantic_manager,
        CrisisPatternManager, create_crisis_pattern_manager,
        SettingsManager, create_settings_manager,
        get_manager_status
    )
    MANAGERS_AVAILABLE = True
    logger.debug("✅ Clean v3.1 managers imported successfully (Step 10.11-3 consolidation)")
except ImportError as e:
    logger.error(f"❌ Clean v3.1 manager imports failed: {e}")
    # Set all to None for graceful degradation
    UnifiedConfigManager = None
    create_unified_config_manager = None
    ModelEnsembleManager = None  # UPDATED: Name change
    create_model_ensemble_manager = None  # UPDATED: Name change
    PydanticManager = None
    create_pydantic_manager = None
    CrisisPatternManager = None
    create_crisis_pattern_manager = None
    SettingsManager = None
    create_settings_manager = None
    get_manager_status = None
    MANAGERS_AVAILABLE = False

# ============================================================================
# CLEAN V3.1 EXTERNAL API - Step 10.11-3 Updated
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
    Step 10.11-3: Replaces create_models_manager with consolidated functionality
    
    Returns:
        ModelEnsembleManager instance for external usage
        
    Raises:
        RuntimeError: If ModelEnsembleManager v3.1 not available
    """
    if not MANAGERS_AVAILABLE or not ModelEnsembleManager:
        raise RuntimeError(
            "Clean v3.1: ModelEnsembleManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    # Import factory function
    from .managers import create_model_ensemble_manager as _create_model_ensemble_manager
    return _create_model_ensemble_manager()

# STEP 10.11-3: create_models_manager function REMOVED - functionality consolidated
# def create_models_manager():  # REMOVED
#     """Functionality consolidated into create_model_ensemble_manager"""

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
    
    # Use factory function
    from .managers import create_unified_config_manager
    return create_unified_config_manager(config_dir)

# ============================================================================
# STEP 10.11-3 CONSOLIDATION STATUS
# ============================================================================

def get_consolidation_status():
    """
    Get Step 10.11-3 Models Manager consolidation status
    
    Returns:
        Dictionary with consolidation information
    """
    return {
        'step': '10.11-3',
        'consolidation': 'Models Manager → ModelEnsembleManager',
        'removed_manager': 'ModelsManager',
        'primary_model_manager': 'ModelEnsembleManager',
        'models_manager_available': False,
        'model_ensemble_manager_available': MANAGERS_AVAILABLE and ModelEnsembleManager is not None,
        'api_compatibility': 'Maintained (same method names)',
        'schema_warnings_resolved': True
    }

# ============================================================================
# EXPORTS - Updated for Step 10.11-3
# ============================================================================

__all__ = [
    # Unified Configuration (Step 9.8)
    'UnifiedConfigManager',
    'create_unified_config_manager',
    'create_unified_config_manager_instance',
    
    # Core Managers - STEP 10.11-3: Updated for consolidation
    'ModelEnsembleManager',  # UPDATED: Consolidated model manager
    'create_model_ensemble_manager',  # UPDATED: Consolidated function
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
    'get_consolidation_status',  # NEW: Step 10.11-3 status
    
    # System Information
    'MANAGERS_AVAILABLE'
]

# ============================================================================
# STEP 10.11-3 COMPLETION LOG
# ============================================================================

logger.info("✅ Ash-NLP __init__.py Step 10.11-3 complete - ModelsManager consolidated into ModelEnsembleManager")

if MANAGERS_AVAILABLE:
    logger.info("🎉 Step 10.11-3 SUCCESS: All managers available with ModelEnsembleManager consolidation!")
else:
    logger.warning("⚠️ Step 10.11-3 INCOMPLETE: Manager imports failed")

logger.info("🏳️‍🌈 Ash-NLP v3.1 Step 10.11-3 ready to serve The Alphabet Cartel LGBTQIA+ community!")