# ash/ash-nlp/__init__.py (Clean v3.1 Architecture - Phase 3a Complete)
"""
Ash NLP Service - Enhanced Mental Health Crisis Detection
Version 3.1 - Clean Manager Architecture (Phase 3a Complete)

A specialized microservice for analyzing Discord messages to detect mental health crises
with a safety-first approach designed for LGBTQIA+ communities.

Phase 3a Status: Complete - Crisis Pattern Manager integrated
Architecture: Clean v3.1 with direct manager access and JSON configuration
"""

__version__ = "3.1.0"
__author__ = "The Alphabet Cartel"
__description__ = "Enhanced Mental Health Crisis Detection with Clean Manager Architecture and Crisis Patterns"

# ============================================================================
# CLEAN V3.1 IMPORTS - Direct Manager Access Only (Phase 3a Updated)
# ============================================================================

# Core managers from clean v3.1 architecture
try:
    from .managers.config_manager import ConfigManager
    from .managers.settings_manager import SettingsManager
    from .managers.zero_shot_manager import ZeroShotManager
    from .managers.models_manager import ModelsManager  # Phase 2A Complete
    from .managers.pydantic_manager import PydanticManager, create_pydantic_manager  # Phase 2B Complete
    from .managers.crisis_pattern_manager import CrisisPatternManager, create_crisis_pattern_manager  # Phase 3a Complete
    
    # Analysis components
    from .analysis.crisis_analyzer import CrisisAnalyzer
    
    MANAGERS_AVAILABLE = True
    
except ImportError as e:
    # Clean v3.1: Fail gracefully but provide clear error information
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Clean v3.1: Manager imports failed: {e}")
    logger.error("💡 Ensure all managers are properly installed in managers/ directory")
    
    # Set placeholders to None for graceful degradation
    ConfigManager = None
    SettingsManager = None
    ZeroShotManager = None
    ModelsManager = None
    PydanticManager = None
    create_pydantic_manager = None
    CrisisPatternManager = None
    create_crisis_pattern_manager = None
    CrisisAnalyzer = None
    
    MANAGERS_AVAILABLE = False

# ============================================================================
# CLEAN V3.1 MODEL ACCESS FUNCTIONS (Phase 3a Updated)
# ============================================================================

def get_pydantic_models():
    """
    Get Pydantic models from clean v3.1 architecture
    
    Returns:
        Dictionary of Pydantic model classes for external usage
        
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

def create_model_manager():
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
    from .managers import create_model_manager as _create_model_manager
    return _create_model_manager()

def create_crisis_pattern_manager_instance(config_manager=None):
    """
    Create CrisisPatternManager instance with proper dependency injection
    
    Args:
        config_manager: Optional ConfigManager instance. If None, creates one.
        
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
    
    # Create ConfigManager if not provided
    if config_manager is None:
        if not ConfigManager:
            raise RuntimeError(
                "Clean v3.1: ConfigManager not available for CrisisPatternManager dependency injection."
            )
        config_manager = ConfigManager()
    
    # Import factory function
    return create_crisis_pattern_manager(config_manager)

# ============================================================================
# SERVICE INFORMATION FUNCTIONS (Phase 3a Updated)
# ============================================================================

SERVICE_INFO = {
    "service": "Ash NLP Service",
    "version": "3.1.0",
    "architecture": "clean_v3.1_phase_3a_complete",
    "description": "Enhanced Mental Health Crisis Detection with Crisis Pattern Manager",
    "author": "The Alphabet Cartel",
    "discord": "https://discord.gg/alphabetcartel",
    "website": "http://alphabetcartel.org",
    "phases_complete": ["2A", "2B", "2C", "3a"],
    "features": {
        "crisis_detection": True,
        "multi_model_ensemble": True,
        "lgbtqia_community_patterns": True,
        "json_configuration": True,
        "crisis_pattern_manager": True,
        "clean_architecture": True
    }
}

def get_service_info():
    """Get comprehensive service information including Phase 3a features"""
    return SERVICE_INFO

def get_version_info():
    """Get version and architecture information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
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
            "crisis_pattern_manager_v3_1": CrisisPatternManager is not None,
            "crisis_analyzer": CrisisAnalyzer is not None
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
            "CrisisPatternManager_v3_1": CrisisPatternManager is not None,
            "CrisisAnalyzer": CrisisAnalyzer is not None
        },
        "phase_status": {
            "phase_2a_models_manager": ModelsManager is not None,
            "phase_2b_pydantic_manager": PydanticManager is not None,
            "phase_2c_cleanup": "complete",
            "phase_3a_crisis_patterns": CrisisPatternManager is not None
        },
        "usage_notes": {
            "manager_initialization": "Use create_pydantic_manager(), create_model_manager(), and create_crisis_pattern_manager_instance()",
            "direct_access_only": "No global functions or legacy imports",
            "fail_fast_design": "Clear errors when managers unavailable",
            "crisis_patterns": "Crisis patterns now managed via CrisisPatternManager with JSON configuration"
        }
    }

# ============================================================================
# CLEAN V3.1 PUBLIC API - Phase 3a Complete
# ============================================================================

__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__description__",
    
    # Core managers (Phase 2A, 2B, 3a Complete)
    "ConfigManager",
    "SettingsManager", 
    "ZeroShotManager",
    "ModelsManager",  # Phase 2A
    "PydanticManager",  # Phase 2B
    "create_pydantic_manager",  # Phase 2B
    "CrisisPatternManager",  # Phase 3a
    "create_crisis_pattern_manager",  # Phase 3a
    
    # Analysis components
    "CrisisAnalyzer",
    
    # Manager creation functions
    "get_pydantic_models",
    "create_model_manager",
    "create_crisis_pattern_manager_instance",  # Phase 3a
    
    # Service info functions
    "SERVICE_INFO",
    "get_service_info",
    "get_version_info",
    "get_manager_status",
    
    # Status flags
    "MANAGERS_AVAILABLE"
]

# ============================================================================
# CLEAN V3.1 PHASE 3A INITIALIZATION COMPLETE
# ============================================================================

# Log initialization status
if MANAGERS_AVAILABLE:
    import logging
    logger = logging.getLogger(__name__)
    logger.info("✅ Ash NLP Service v3.1 - Clean Manager Architecture with Crisis Patterns initialized")
    logger.info("🎉 Phase 3a Complete - Crisis Pattern Manager integrated")
    logger.debug(f"📊 Managers available: {sum(1 for m in [ConfigManager, SettingsManager, ZeroShotManager, ModelsManager, PydanticManager, CrisisPatternManager, CrisisAnalyzer] if m is not None)}/7")
else:
    # Managers not available - log warning but don't fail import
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ Ash NLP Service v3.1 - Some managers not available")
    logger.warning("💡 Check managers/ directory for proper installation")
    if not CrisisPatternManager:
        logger.warning("🔍 CrisisPatternManager not available - Phase 3a integration incomplete")