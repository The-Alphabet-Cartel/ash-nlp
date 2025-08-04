# ash/ash-nlp/__init__.py (Clean v3.1 Architecture - Phase 2C Complete)
"""
Ash NLP Service - Enhanced Mental Health Crisis Detection
Version 3.1 - Clean Manager Architecture (Phase 2C Complete)

A specialized microservice for analyzing Discord messages to detect mental health crises
with a safety-first approach designed for LGBTQIA+ communities.

Phase 2C Status: Complete - All backward compatibility removed
Architecture: Clean v3.1 with direct manager access only
"""

__version__ = "3.1.0"
__author__ = "The Alphabet Cartel"
__description__ = "Enhanced Mental Health Crisis Detection with Clean Manager Architecture"

# ============================================================================
# CLEAN V3.1 IMPORTS - Direct Manager Access Only
# ============================================================================

# Core managers from clean v3.1 architecture
try:
    from .managers.config_manager import ConfigManager
    from .managers.settings_manager import SettingsManager
    from .managers.zero_shot_manager import ZeroShotManager
    from .managers.models_manager import ModelsManager  # Phase 2A Complete
    from .managers.pydantic_manager import PydanticManager, create_pydantic_manager  # Phase 2B Complete
    
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
    CrisisAnalyzer = None
    
    MANAGERS_AVAILABLE = False

# ============================================================================
# CLEAN V3.1 MODEL ACCESS FUNCTIONS
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
    
    # This function would typically be used with an initialized PydanticManager instance
    # For external usage, users should create their own PydanticManager instance
    raise RuntimeError(
        "Clean v3.1: Use create_pydantic_manager() to get an initialized PydanticManager instance, "
        "then call get_core_models(), get_learning_request_models(), etc."
    )

def create_model_manager(config_manager=None, model_config=None, hardware_config=None):
    """
    Create ModelsManager v3.1 instance with clean architecture
    
    Args:
        config_manager: ConfigManager instance (required)
        model_config: Model configuration dict (optional)
        hardware_config: Hardware configuration dict (optional)
        
    Returns:
        ModelsManager v3.1 instance
        
    Raises:
        RuntimeError: If ModelsManager v3.1 not available or invalid parameters
    """
    if not MANAGERS_AVAILABLE or not ModelsManager:
        raise RuntimeError(
            "Clean v3.1: ModelsManager not available. "
            "Ensure managers are properly installed in managers/ directory."
        )
    
    if not config_manager:
        raise RuntimeError(
            "Clean v3.1: ConfigManager instance required for ModelsManager initialization"
        )
    
    return ModelsManager(
        config_manager=config_manager,
        model_config=model_config,
        hardware_config=hardware_config
    )

# ============================================================================
# SERVICE METADATA - Updated for Clean v3.1
# ============================================================================

SERVICE_INFO = {
    "name": "Ash NLP Service",
    "version": __version__,
    "architecture": "clean_v3.1_phase_2c_complete",
    "description": __description__,
    "manager_architecture": {
        "config_manager": "Clean JSON + ENV configuration management",
        "models_manager": "Phase 2A - ML model management",
        "pydantic_manager": "Phase 2B - Pydantic model management", 
        "settings_manager": "Settings and configuration management",
        "zero_shot_manager": "Zero-shot label management",
        "backward_compatibility": "removed"
    },
    "capabilities": [
        "Crisis analysis with three zero-shot model ensemble",
        "JSON configuration with environment overrides",
        "Clean manager architecture with direct access",
        "Learning system with false positive/negative correction",
        "Advanced ensemble analysis with gap detection",
        "LGBTQIA+ specific pattern recognition"
    ],
    "performance_targets": {
        "overall_accuracy": "75%+ (vs baseline)",
        "high_crisis_detection": "95%+ (with keyword detection)",
        "false_positive_rate": "<8% (vs previous 15%)",
        "processing_time": "<100ms for analysis",
        "startup_time": "Faster without compatibility checks"
    },
    "hardware_requirements": {
        "min_ram": "8GB (three model ensemble)",
        "recommended_ram": "16GB+",
        "cpu_cores": "4+",
        "gpu": "Optional (NVIDIA RTX 3060+ recommended)",
        "storage": "2GB+ for model cache"
    },
    "phase_status": {
        "phase_2a": "complete - ModelsManager v3.1",
        "phase_2b": "complete - PydanticManager v3.1", 
        "phase_2c": "complete - Backward compatibility removed",
        "architecture": "clean_v3.1_production_ready"
    }
}

def get_service_info():
    """Get comprehensive service information for clean v3.1 architecture"""
    return SERVICE_INFO

def get_version_info():
    """Get version and build information for clean v3.1 architecture"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "architecture": "clean_v3.1_phase_2c_complete",
        "managers_available": MANAGERS_AVAILABLE,
        "api_endpoints": [
            "/analyze - Three zero-shot model ensemble analysis",
            "/health - System health with manager status",
            "/ensemble/status - Comprehensive ensemble status", 
            "/ensemble/health - Ensemble health check",
            "/ensemble/config - Configuration debugging",
            "/admin/labels/* - Label management endpoints",
            "/learning_statistics - Learning system statistics",
            "/analyze_false_positive - False positive learning",
            "/analyze_false_negative - False negative learning"
        ],
        "manager_integration": {
            "config_manager": ConfigManager is not None,
            "settings_manager": SettingsManager is not None,
            "zero_shot_manager": ZeroShotManager is not None,
            "models_manager_v3_1": ModelsManager is not None,
            "pydantic_manager_v3_1": PydanticManager is not None,
            "crisis_analyzer": CrisisAnalyzer is not None
        }
    }

def get_manager_status():
    """Get detailed manager availability status for clean v3.1 architecture"""
    return {
        "managers_available": MANAGERS_AVAILABLE,
        "architecture": "clean_v3.1_phase_2c_complete",
        "manager_components": {
            "ConfigManager": ConfigManager is not None,
            "SettingsManager": SettingsManager is not None,
            "ZeroShotManager": ZeroShotManager is not None,
            "ModelsManager_v3_1": ModelsManager is not None,
            "PydanticManager_v3_1": PydanticManager is not None,
            "CrisisAnalyzer": CrisisAnalyzer is not None
        },
        "phase_status": {
            "phase_2a_models_manager": ModelsManager is not None,
            "phase_2b_pydantic_manager": PydanticManager is not None,
            "phase_2c_cleanup": "complete",
            "backward_compatibility": "removed"
        },
        "usage_notes": {
            "manager_initialization": "Use create_pydantic_manager() and create_model_manager()",
            "direct_access_only": "No global functions or legacy imports",
            "fail_fast_design": "Clear errors when managers unavailable"
        }
    }

# ============================================================================
# CLEAN V3.1 PUBLIC API - No Legacy Imports
# ============================================================================

__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__description__",
    
    # Core managers (Phase 2A & 2B Complete)
    "ConfigManager",
    "SettingsManager", 
    "ZeroShotManager",
    "ModelsManager",  # Phase 2A
    "PydanticManager",  # Phase 2B
    "create_pydantic_manager",  # Phase 2B
    
    # Analysis components
    "CrisisAnalyzer",
    
    # Manager creation functions
    "get_pydantic_models",
    "create_model_manager",
    
    # Service info functions
    "SERVICE_INFO",
    "get_service_info",
    "get_version_info",
    "get_manager_status",
    
    # Status flags
    "MANAGERS_AVAILABLE"
]

# ============================================================================
# CLEAN V3.1 INITIALIZATION COMPLETE
# ============================================================================

# Log initialization status
if MANAGERS_AVAILABLE:
    import logging
    logger = logging.getLogger(__name__)
    logger.info("✅ Ash NLP Service v3.1 - Clean Manager Architecture initialized")
    logger.info("🎉 Phase 2C Complete - All backward compatibility removed")
    logger.debug(f"📊 Managers available: {sum(1 for m in [ConfigManager, SettingsManager, ZeroShotManager, ModelsManager, PydanticManager, CrisisAnalyzer] if m is not None)}/6")
else:
    # Managers not available - log warning but don't fail import
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ Ash NLP Service v3.1 - Some managers not available")
    logger.warning("💡 Check managers/ directory for proper installation")