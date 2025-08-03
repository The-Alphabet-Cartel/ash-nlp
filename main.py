# ash/ash-nlp/main.py (Clean Manager-Only Architecture)
"""
Clean initialization system for Ash NLP Service v3.1
Manager-first architecture with no backward compatibility
"""

import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

# Import managers (our new clean architecture)
from managers.config_manager import ConfigManager
from managers.settings_manager import SettingsManager
from managers.zero_shot_manager import ZeroShotManager

# Import ModelManager (clean version)
from models.ml_models import ModelManager

logger = logging.getLogger(__name__)

# Global components
model_manager = None
crisis_analyzer = None
phrase_extractor = None
enhanced_learning_manager = None
config_manager = None
settings_manager = None
zero_shot_manager = None
startup_time = time.time()

# Component availability flags (will be set during imports)
CRISIS_ANALYZER_AVAILABLE = False
PHRASE_EXTRACTOR_AVAILABLE = False
ENHANCED_LEARNING_AVAILABLE = False

# Import components with manager requirement
try:
    from analysis.crisis_analyzer import CrisisAnalyzer
    CRISIS_ANALYZER_AVAILABLE = True
    logger.info("✅ CrisisAnalyzer import successful")
except ImportError as e:
    CRISIS_ANALYZER_AVAILABLE = False
    logger.warning(f"⚠️ CrisisAnalyzer import failed: {e}")

try:
    from analysis.phrase_extractor import PhraseExtractor
    PHRASE_EXTRACTOR_AVAILABLE = True
    logger.info("✅ PhraseExtractor import successful")
except ImportError as e:
    PHRASE_EXTRACTOR_AVAILABLE = False
    logger.warning(f"⚠️ PhraseExtractor import failed: {e}")

try:
    from api.enhanced_learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    ENHANCED_LEARNING_AVAILABLE = True
    logger.info("✅ EnhancedLearningManager import successful")
except ImportError as e:
    ENHANCED_LEARNING_AVAILABLE = False
    logger.warning(f"⚠️ EnhancedLearningManager import failed: {e}")

async def initialize_components_with_clean_managers():
    """Initialize all components with clean manager-only architecture"""
    global model_manager, crisis_analyzer, phrase_extractor, enhanced_learning_manager
    global config_manager, settings_manager, zero_shot_manager
    
    try:
        logger.info("🚀 Initializing components with clean manager-only architecture...")
        
        # ========================================================================
        # STEP 1: Initialize Core Configuration Managers
        # ========================================================================
        logger.info("📋 Initializing core configuration managers...")
        
        config_manager = ConfigManager("/app/config")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        
        logger.info("✅ Core managers initialized successfully")
        
        # ========================================================================
        # STEP 2: Validate Configuration
        # ========================================================================
        logger.info("🔍 Validating configuration...")
        
        validation_result = config_manager.validate_configuration()
        if not validation_result['valid']:
            logger.error(f"❌ Configuration validation failed: {validation_result['errors']}")
            raise RuntimeError(f"Invalid configuration: {validation_result['errors']}")
        
        for warning in validation_result['warnings']:
            logger.warning(f"⚠️ Configuration warning: {warning}")
        
        logger.info("✅ Configuration validation passed")
        
        # ========================================================================
        # STEP 3: Extract and Log Configuration
        # ========================================================================
        logger.info("📊 Extracting processed configuration...")
        
        model_config = config_manager.get_model_configuration()
        hardware_config = config_manager.get_hardware_configuration()
        threshold_config = config_manager.get_threshold_configuration()
        feature_flags = config_manager.get_feature_flags()
        ensemble_mode = config_manager.get_ensemble_mode()
        
        # Log the models that will be loaded (with environment overrides applied)
        models = model_config.get('models', {})
        logger.info("🎯 Final Model Configuration (JSON + Environment Overrides):")
        for model_type, model_info in models.items():
            logger.info(f"   {model_type.title()} Model: {model_info['name']}")
            logger.info(f"   {model_type.title()} Weight: {model_info['weight']}")
        
        logger.info(f"   Ensemble Mode: {ensemble_mode}")
        
        gap_detection_enabled = model_config.get('ensemble_config', {}).get('gap_detection', {}).get('enabled', True)
        logger.info(f"   Gap Detection: {'✅ Enabled' if gap_detection_enabled else '❌ Disabled'}")
        
        # ========================================================================
        # STEP 4: Initialize Enhanced ModelManager
        # ========================================================================
        logger.info("🧠 Initializing Enhanced ModelManager with processed configuration...")
        
        model_manager = ModelManager(
            config_manager=config_manager,
            model_config=model_config,
            hardware_config=hardware_config
        )
        
        logger.info("✅ ModelManager initialized with clean manager architecture")
        
        # ========================================================================
        # STEP 5: Load Models
        # ========================================================================
        logger.info("📦 Loading Three Zero-Shot Model Ensemble...")
        await model_manager.load_models()
        logger.info("✅ All three models loaded successfully")
        
        # Set global model manager for API access
        globals()['model_manager'] = model_manager
        logger.info("✅ Global model manager set for API access")
        
        # ========================================================================
        # STEP 6: Initialize Learning System (FAIL FAST)
        # ========================================================================
        if ENHANCED_LEARNING_AVAILABLE:
            learning_config = feature_flags.get('learning_system', {})
            if learning_config.get('enabled', True):
                # FAIL FAST - require proper manager integration
                enhanced_learning_manager = EnhancedLearningManager(
                    model_manager=model_manager,
                    config_manager=config_manager,
                    settings_manager=settings_manager
                )
                logger.info("✅ Enhanced learning system initialized with clean manager architecture")
            else:
                logger.info("ℹ️ Learning system disabled via configuration")
                enhanced_learning_manager = None
        else:
            logger.info("ℹ️ Enhanced learning system not available")
            enhanced_learning_manager = None
        
        # ========================================================================
        # STEP 7: Initialize Analysis Components (FAIL FAST)
        # ========================================================================
        
        # Initialize CrisisAnalyzer - FAIL FAST if not compatible
        if CRISIS_ANALYZER_AVAILABLE:
            crisis_analyzer = CrisisAnalyzer(
                model_manager=model_manager,
                config_manager=config_manager,
                settings_manager=settings_manager,
                learning_manager=enhanced_learning_manager
            )
            logger.info("✅ CrisisAnalyzer initialized with clean manager architecture")
        else:
            logger.error("❌ CrisisAnalyzer not available - import failed")
            crisis_analyzer = None
        
        # Initialize PhraseExtractor - FAIL FAST if not compatible
        if PHRASE_EXTRACTOR_AVAILABLE:
            phrase_extractor = PhraseExtractor(
                model_manager=model_manager,
                config_manager=config_manager,
                zero_shot_manager=zero_shot_manager
            )
            logger.info("✅ PhraseExtractor initialized with clean manager architecture")
        else:
            logger.error("❌ PhraseExtractor not available - import failed")
            phrase_extractor = None
        
        # ========================================================================
        # STEP 8: Final Status Report
        # ========================================================================
        logger.info("📊 Component Initialization Summary:")
        
        components_status = {
            'core_managers': {
                'config_manager': config_manager is not None,
                'settings_manager': settings_manager is not None,
                'zero_shot_manager': zero_shot_manager is not None
            },
            'ml_components': {
                'model_manager': model_manager is not None,
                'three_model_ensemble': model_manager and model_manager.models_loaded() if model_manager else False
            },
            'analysis_components': {
                'crisis_analyzer': crisis_analyzer is not None,
                'phrase_extractor': phrase_extractor is not None,
                'enhanced_learning': enhanced_learning_manager is not None
            }
        }
        
        for category, components in components_status.items():
            logger.info(f"   {category.replace('_', ' ').title()}:")
            for component, status in components.items():
                status_icon = "✅" if status else "❌"
                logger.info(f"     {component}: {status_icon}")
        
        # Check if any critical components failed
        critical_failures = []
        if not model_manager:
            critical_failures.append("ModelManager")
        if model_manager and not model_manager.models_loaded():
            critical_failures.append("Model Loading")
        
        if critical_failures:
            logger.error(f"❌ Critical component failures: {critical_failures}")
            raise RuntimeError(f"Critical components failed to initialize: {critical_failures}")
        
        logger.info("✅ All critical components initialized successfully with clean manager architecture")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        logger.exception("Full initialization error:")
        raise

# ============================================================================
# Health Response Model
# ============================================================================
class HealthResponse(BaseModel):
    status: str
    uptime: float
    model_loaded: bool
    components_available: dict
    configuration_status: dict
    manager_status: dict
    secrets_status: dict

# ============================================================================
# FastAPI Application Setup
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager with clean manager architecture"""
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting with Clean Manager Architecture v3.1...")
    await initialize_components_with_clean_managers()
    
    # Import and add ensemble endpoints after initialization
    try:
        from api.ensemble_endpoints import add_ensemble_endpoints
        logger.info("🔧 Adding Three Zero-Shot Model Ensemble endpoints...")
        add_ensemble_endpoints(app, model_manager, config_manager)
        logger.info("🎯 Three Zero-Shot Model Ensemble endpoints added with manager integration!")
    except ImportError:
        # FALLBACK: Try old endpoints directory
        from api.ensemble_endpoints import add_ensemble_endpoints
        logger.warning("⚠️ Imported ensemble_endpoints from old 'endpoints' path - should update to 'api'")
        logger.info("🔧 Adding Three Zero-Shot Model Ensemble endpoints...")
        add_ensemble_endpoints(app, model_manager, config_manager)
        logger.info("🎯 Three Zero-Shot Model Ensemble endpoints added with manager integration!")
    
    # Add learning endpoints if available
    if enhanced_learning_manager and ENHANCED_LEARNING_AVAILABLE:
        logger.info("🔧 Adding enhanced learning endpoints...")
        add_enhanced_learning_endpoints(app, enhanced_learning_manager, config_manager)
        logger.info("🧠 Enhanced learning endpoints added with manager integration!")
    else:
        logger.error("❌ Learning system required but not available")
        raise RuntimeError("Enhanced learning system is required but not available")
    
    logger.info("✅ Enhanced FastAPI app startup complete with Clean Manager Architecture!")
    
    yield
    
    # Shutdown
    logger.info("🛑 FastAPI app shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Ash NLP Service v3.1 - Clean Manager Architecture", 
    version="3.1.0",
    description="Advanced crisis detection using three specialized ML models with clean JSON+ENV configuration management",
    lifespan=lifespan
)

# Configure CORS if enabled
cors_enabled = os.getenv('GLOBAL_ENABLE_CORS', 'true').lower() == 'true'
if cors_enabled:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("🌐 CORS middleware enabled")

# ============================================================================
# Health Check Endpoint
# ============================================================================
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check with clean manager architecture status"""
    
    uptime = time.time() - startup_time
    models_loaded = model_manager and model_manager.models_loaded() if model_manager else False
    
    # Check component availability
    components_status = {
        "model_manager": model_manager is not None,
        "crisis_analyzer": crisis_analyzer is not None,
        "phrase_extractor": phrase_extractor is not None,
        "enhanced_learning": enhanced_learning_manager is not None,
        "three_model_ensemble": models_loaded
    }
    
    # Manager status
    manager_status = {
        "config_manager": config_manager is not None,
        "settings_manager": settings_manager is not None,
        "zero_shot_manager": zero_shot_manager is not None,
        "manager_architecture": "clean_v3.1"
    }
    
    # Configuration status
    configuration_status = {
        "json_config_loaded": config_manager is not None,
        "environment_overrides_applied": True,
        "model_configuration_valid": False,
        "ensemble_mode": "unknown",
        "config_validation_passed": False
    }
    
    if config_manager:
        try:
            validation_result = config_manager.validate_configuration()
            configuration_status["model_configuration_valid"] = validation_result['valid']
            configuration_status["config_validation_passed"] = validation_result['valid']
            configuration_status["ensemble_mode"] = config_manager.get_ensemble_mode()
        except Exception as e:
            logger.warning(f"Health check configuration validation error: {e}")
    
    # Check secrets status
    secrets_status = {
        "huggingface_token": bool(os.getenv('GLOBAL_HUGGINGFACE_TOKEN')),
        "claude_api_key": bool(os.getenv('GLOBAL_CLAUDE_API_KEY')),
        "openai_api_key": bool(os.getenv('OPENAI_API_KEY'))
    }
    
    # Determine overall status
    if models_loaded and components_status["model_manager"] and manager_status["config_manager"]:
        overall_status = "healthy"
    elif model_manager and manager_status["config_manager"]:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        uptime=uptime,
        model_loaded=models_loaded,
        components_available=components_status,
        configuration_status=configuration_status,
        manager_status=manager_status,
        secrets_status=secrets_status
    )