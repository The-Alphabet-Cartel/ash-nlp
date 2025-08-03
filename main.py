#!/usr/bin/env python3
# ash/ash-nlp/main.py (Clean Manager-Only Architecture)
"""
Clean initialization system for Ash NLP Service v3.1
Manager-first architecture with no backward compatibility
FIXED: All imports in try-catch blocks to prevent silent failures
"""

import os
import sys
import time
import logging
from contextlib import asynccontextmanager
from pydantic import BaseModel

# Set up logging FIRST to catch any import errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.info("🚀 Starting Ash NLP Service v3.1 with Clean Manager Architecture")

# Global components
model_manager = None
crisis_analyzer = None
phrase_extractor = None
learning_manager = None
config_manager = None
settings_manager = None
zero_shot_manager = None
startup_time = time.time()

# Component availability flags
MANAGERS_AVAILABLE = False
MODEL_MANAGER_AVAILABLE = False
CRISIS_ANALYZER_AVAILABLE = False
PHRASE_EXTRACTOR_AVAILABLE = False
LEARNING_AVAILABLE = False
FASTAPI_AVAILABLE = False

# ============================================================================
# SAFE IMPORT SECTION - All imports wrapped in try-catch
# ============================================================================

# Import FastAPI
try:
    from fastapi import FastAPI
    FASTAPI_AVAILABLE = True
    logger.info("✅ FastAPI import successful")
except ImportError as e:
    FASTAPI_AVAILABLE = False
    logger.error(f"❌ FastAPI import failed: {e}")
    sys.exit(1)

# Import managers
try:
    logger.info("🔧 Importing managers...")
    from managers.config_manager import ConfigManager
    from managers.settings_manager import SettingsManager
    from managers.zero_shot_manager import ZeroShotManager
    MANAGERS_AVAILABLE = True
    logger.info("✅ All managers imported successfully")
except ImportError as e:
    MANAGERS_AVAILABLE = False
    logger.error(f"❌ Manager imports failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import ModelManager
try:
    logger.info("🧠 Importing ModelManager...")
    from models.ml_models import ModelManager
    MODEL_MANAGER_AVAILABLE = True
    logger.info("✅ ModelManager import successful")
except ImportError as e:
    MODEL_MANAGER_AVAILABLE = False
    logger.error(f"❌ ModelManager import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import analysis components (optional)
try:
    logger.info("🔍 Importing CrisisAnalyzer...")
    from analysis.crisis_analyzer import CrisisAnalyzer
    CRISIS_ANALYZER_AVAILABLE = True
    logger.info("✅ CrisisAnalyzer import successful")
except ImportError as e:
    CRISIS_ANALYZER_AVAILABLE = False
    logger.warning(f"⚠️ CrisisAnalyzer import failed: {e}")

try:
    logger.info("📝 Importing PhraseExtractor...")
    from analysis.phrase_extractor import PhraseExtractor
    PHRASE_EXTRACTOR_AVAILABLE = True
    logger.info("✅ PhraseExtractor import successful")
except ImportError as e:
    PHRASE_EXTRACTOR_AVAILABLE = False
    logger.warning(f"⚠️ PhraseExtractor import failed: {e}")

# Import learning system (optional)
try:
    logger.info("🧠 Importing Learning System...")
    from api.learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    LEARNING_AVAILABLE = True
    logger.info("✅ Learning system import successful")
except ImportError as e:
    LEARNING_AVAILABLE = False
    logger.warning(f"⚠️ Learning system import failed: {e}")

# ============================================================================
# INITIALIZATION FUNCTIONS
# ============================================================================

async def initialize_components_with_clean_managers():
    """Initialize all components with clean manager-only architecture"""
    global model_manager, crisis_analyzer, phrase_extractor, learning_manager
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
        
        if not MODEL_MANAGER_AVAILABLE:
            logger.error("❌ ModelManager not available - cannot continue")
            raise RuntimeError("ModelManager import failed")
        
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
        # STEP 6: Initialize Learning System
        # ========================================================================
        if LEARNING_AVAILABLE:
            learning_config = feature_flags.get('learning_system', {})
            if learning_config.get('enabled', True):
                learning_manager = EnhancedLearningManager(
                    model_manager=model_manager,
                    config_manager=config_manager,
                    settings_manager=settings_manager
                )
                logger.info("✅ Learning system initialized with clean manager architecture")
            else:
                logger.info("ℹ️ Learning system disabled via configuration")
                learning_manager = None
        else:
            logger.info("ℹ️ Learning system not available")
            learning_manager = None
        
        # ========================================================================
        # STEP 7: Initialize Analysis Components
        # ========================================================================
        
        # Initialize CrisisAnalyzer
        if CRISIS_ANALYZER_AVAILABLE:
            try:
                crisis_analyzer = CrisisAnalyzer(
                    model_manager=model_manager,
                    config_manager=config_manager,
                    settings_manager=settings_manager,
                    learning_manager=learning_manager
                )
                logger.info("✅ CrisisAnalyzer initialized with clean manager architecture")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CrisisAnalyzer: {e}")
                crisis_analyzer = None
        else:
            logger.info("ℹ️ CrisisAnalyzer not available")
            crisis_analyzer = None
        
        # Initialize PhraseExtractor
        if PHRASE_EXTRACTOR_AVAILABLE:
            try:
                phrase_extractor = PhraseExtractor(
                    model_manager=model_manager,
                    config_manager=config_manager,
                    zero_shot_manager=zero_shot_manager
                )
                logger.info("✅ PhraseExtractor initialized with clean manager architecture")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize PhraseExtractor: {e}")
                phrase_extractor = None
        else:
            logger.info("ℹ️ PhraseExtractor not available")
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
                'learning_manager': learning_manager is not None
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
    
    try:
        await initialize_components_with_clean_managers()
        
        # Import and add ensemble endpoints after initialization
        try:
            logger.info("🔧 Adding Three Zero-Shot Model Ensemble endpoints...")
            from api.ensemble_endpoints import add_ensemble_endpoints
            add_ensemble_endpoints(app, model_manager, config_manager)
            logger.info("🎯 Three Zero-Shot Model Ensemble endpoints added with manager integration!")
        except Exception as e:
            logger.error(f"❌ Failed to add ensemble endpoints: {e}")
            raise
        
        # Add learning endpoints if available
        if learning_manager and LEARNING_AVAILABLE:
            try:
                logger.info("🔧 Adding enhanced learning endpoints...")
                add_enhanced_learning_endpoints(app, learning_manager, config_manager)
                logger.info("🧠 Enhanced learning endpoints added with manager integration!")
            except Exception as e:
                logger.error(f"❌ Failed to add learning endpoints: {e}")
                raise
        else:
            logger.info("ℹ️ Learning system not available - skipping learning endpoints")
        
        logger.info("✅ Enhanced FastAPI app startup complete with Clean Manager Architecture!")
        
    except Exception as e:
        logger.error(f"❌ FastAPI app startup failed: {e}")
        logger.exception("Full startup error:")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 FastAPI app shutting down...")

# Create FastAPI app
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Ash NLP Service v3.1 - Clean Manager Architecture", 
        version="3.1.0",
        description="Advanced crisis detection using three specialized ML models with clean JSON+ENV configuration management",
        lifespan=lifespan
    )
    
    # Configure CORS if enabled
    cors_enabled = os.getenv('GLOBAL_ENABLE_CORS', 'true').lower() == 'true'
    if cors_enabled:
        try:
            from fastapi.middleware.cors import CORSMiddleware
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],  # Configure appropriately for production
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            logger.info("🌐 CORS middleware enabled")
        except Exception as e:
            logger.warning(f"⚠️ Could not enable CORS: {e}")
    
    logger.info("✅ FastAPI app created successfully")
else:
    logger.error("❌ Cannot create FastAPI app - FastAPI import failed")
    sys.exit(1)

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
        "learning_manager": learning_manager is not None,
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

# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    logger.info("🎯 Starting Ash NLP Service directly...")
    
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv('GLOBAL_NLP_API_PORT', 8881)),
        log_level=os.getenv('GLOBAL_LOG_LEVEL', 'info').lower()
    )