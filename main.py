#!/usr/bin/env python3
# ash/ash-nlp/main.py (Clean Manager-Only Architecture with Debug Control - Phase 2B Update)
"""
Clean initialization system for Ash NLP Service v3.1
Manager-first architecture with conditional debug logging - Phase 2B Update
"""

import os
import sys
import time
import logging
from contextlib import asynccontextmanager
from pydantic import BaseModel

# Set up logging FIRST to catch any import errors
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s -- %(levelname)s -- %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
logger.info("🚀 Starting Ash NLP Service v3.1 with Clean Manager Architecture - Phase 2B")

# Global components
model_manager = None
pydantic_manager = None  # PHASE 2B: New global component
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
PYDANTIC_MANAGER_AVAILABLE = False  # PHASE 2B: New availability flag
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

# Import ModelManager - PHASE 2A COMPLETE
try:
    logger.info("🧠 Importing ModelsManager v3.1...")
    from managers.models_manager import ModelsManager as ModelManager
    MODEL_MANAGER_V3_1_AVAILABLE = True
    MODEL_MANAGER_AVAILABLE = True
    logger.info("✅ Phase 2A: ModelsManager v3.1 imported from managers/ (COMPLETE)")
except ImportError as e:
    logger.warning(f"⚠️ Phase 2A ModelsManager not available: {e}")
    try:
        logger.info("🧠 Falling back to legacy ModelManager...")
        from models.ml_models import ModelManager
        MODEL_MANAGER_V3_1_AVAILABLE = False
        MODEL_MANAGER_AVAILABLE = True
        logger.info("⚠️ Using legacy ModelManager - Phase 2A migration recommended")
    except ImportError as e2:
        MODEL_MANAGER_V3_1_AVAILABLE = False
        MODEL_MANAGER_AVAILABLE = False
        logger.error(f"❌ No ModelManager available: {e2}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Import PydanticManager - PHASE 2B NEW
try:
    logger.info("📋 Importing PydanticManager v3.1...")
    from managers.pydantic_manager import PydanticManager, create_pydantic_manager
    PYDANTIC_MANAGER_V3_1_AVAILABLE = True
    PYDANTIC_MANAGER_AVAILABLE = True
    logger.info("✅ Phase 2B: PydanticManager v3.1 imported from managers/")
except ImportError as e:
    logger.warning(f"⚠️ Phase 2B PydanticManager not available: {e}")
    try:
        logger.info("📋 Falling back to legacy Pydantic models...")
        # Import the most commonly used models for backward compatibility
        from models.pydantic_models import (
            MessageRequest, CrisisResponse, HealthResponse,
            FalsePositiveAnalysisRequest, FalseNegativeAnalysisRequest, 
            LearningUpdateRequest, FalsePositiveAnalysisResponse,
            FalseNegativeAnalysisResponse, LearningUpdateResponse,
            LearningStatisticsResponse
        )
        PYDANTIC_MANAGER_V3_1_AVAILABLE = False
        PYDANTIC_MANAGER_AVAILABLE = True
        logger.info("⚠️ Using legacy Pydantic models - Phase 2B migration recommended")
    except ImportError as e2:
        PYDANTIC_MANAGER_V3_1_AVAILABLE = False
        PYDANTIC_MANAGER_AVAILABLE = False
        logger.error(f"❌ No Pydantic models available: {e2}")
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

# Get configuration values
log_level = os.getenv('GLOBAL_LOG_LEVEL', 'INFO').upper()
log_file = os.getenv('NLP_LOG_FILE', 'nlp_service.log')

# NOW configure the proper logging system:
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s -- %(levelname)s -- %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Create new logger with proper configuration
logger = logging.getLogger(__name__)
logger.info("✅ Logging system configured properly")

# ============================================================================
# PHASE 2B: PYDANTIC MODEL ACCESS HELPERS
# ============================================================================

def get_pydantic_models():
    """
    Get Pydantic models from either PydanticManager v3.1 or legacy imports
    Returns: Dictionary of model classes for use in endpoints
    """
    if PYDANTIC_MANAGER_V3_1_AVAILABLE and pydantic_manager:
        logger.debug("🏗️ Using PydanticManager v3.1 for model access")
        return pydantic_manager.get_legacy_imports()
    
    elif PYDANTIC_MANAGER_AVAILABLE:
        logger.debug("⚠️ Using legacy Pydantic model imports")
        # Return legacy imports if available
        try:
            # These should already be imported above if available
            return {
                'MessageRequest': MessageRequest,
                'CrisisResponse': CrisisResponse,
                'HealthResponse': HealthResponse,
                'FalsePositiveAnalysisRequest': FalsePositiveAnalysisRequest,
                'FalseNegativeAnalysisRequest': FalseNegativeAnalysisRequest,
                'LearningUpdateRequest': LearningUpdateRequest,
                'FalsePositiveAnalysisResponse': FalsePositiveAnalysisResponse,
                'FalseNegativeAnalysisResponse': FalseNegativeAnalysisResponse,
                'LearningUpdateResponse': LearningUpdateResponse,
                'LearningStatisticsResponse': LearningStatisticsResponse
            }
        except NameError as e:
            logger.error(f"❌ Legacy Pydantic models not available: {e}")
            raise RuntimeError("No Pydantic models available")
    
    else:
        logger.error("❌ No Pydantic models available - cannot continue")
        raise RuntimeError("No Pydantic models available")

# Initialize threshold configuration using clean centralized approach
def initialize_centralized_threshold_config():
    """Initialize centralized threshold configuration from environment variables"""
    
    # Load centralized configuration from environment variables
    thresholds = {
        # Ensemble mode
        'ensemble_mode': os.getenv('NLP_ENSEMBLE_MODE', 'majority'),
        
        # Consensus mapping thresholds
        'consensus_crisis_to_high': float(os.getenv('NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD', '0.50')),
        'consensus_crisis_to_medium': float(os.getenv('NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD', '0.30')),
        'consensus_mild_crisis_to_low': float(os.getenv('NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD', '0.40')),
        'consensus_negative_to_low': float(os.getenv('NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD', '0.70')),
        'consensus_unknown_to_low': float(os.getenv('NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD', '0.50')),
        
        # Model weights
        'depression_weight': float(os.getenv('NLP_DEPRESSION_MODEL_WEIGHT', '0.6')),
        'sentiment_weight': float(os.getenv('NLP_SENTIMENT_MODEL_WEIGHT', '0.15')),
        'emotional_distress_weight': float(os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', '0.25')),
        
        # Staff review thresholds
        'staff_review_high_always': os.getenv('NLP_STAFF_REVIEW_HIGH_ALWAYS', 'true').lower() == 'true',
        'staff_review_medium_threshold': float(os.getenv('NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD', '0.45')),
        'staff_review_low_threshold': float(os.getenv('NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD', '0.75')),
        'staff_review_on_disagreement': os.getenv('NLP_STAFF_REVIEW_ON_MODEL_DISAGREEMENT', 'true').lower() == 'true',
        
        # Safety controls  
        'consensus_safety_bias': float(os.getenv('NLP_CONSENSUS_SAFETY_BIAS', '0.05')),
        'enable_safety_override': os.getenv('NLP_ENABLE_SAFETY_OVERRIDE', 'true').lower() == 'true',
        
        # Learning system
        'enable_learning': os.getenv('GLOBAL_ENABLE_LEARNING_SYSTEM', 'true').lower() == 'true'
    }
    
    # Validate model weights sum to 1.0
    total_weight = thresholds['depression_weight'] + thresholds['sentiment_weight'] + thresholds['emotional_distress_weight']
    if abs(total_weight - 1.0) > 0.001:
        logger.error(f"❌ Model weights must sum to 1.0, got {total_weight}")
        logger.error(f"   Depression: {thresholds['depression_weight']}")
        logger.error(f"   Sentiment: {thresholds['sentiment_weight']}")
        logger.error(f"   Emotional Distress: {thresholds['emotional_distress_weight']}")
        sys.exit(1)
    
    logger.info("🐳 Running in Docker mode - using system environment variables")
    logger.info("✅ Centralized threshold configuration validation passed")
    
    logger.debug("🎯 Centralized Threshold Configuration:")
    logger.debug(f"   Ensemble mode: {thresholds['ensemble_mode']}")
    logger.debug("   Consensus Mapping Thresholds:")
    logger.debug(f"     CRISIS → HIGH: {thresholds['consensus_crisis_to_high']}")
    logger.debug(f"     CRISIS → MEDIUM: {thresholds['consensus_crisis_to_medium']}")
    logger.debug(f"     MILD_CRISIS → LOW: {thresholds['consensus_mild_crisis_to_low']}")
    logger.debug(f"     NEGATIVE → LOW: {thresholds['consensus_negative_to_low']}")
    logger.debug("   Model Weights:")
    logger.debug(f"     Depression: {thresholds['depression_weight']}")
    logger.debug(f"     Sentiment: {thresholds['sentiment_weight']}")
    logger.debug(f"     Emotional Distress: {thresholds['emotional_distress_weight']}")
    logger.debug("   Staff Review Thresholds:")
    logger.debug(f"     MEDIUM confidence: {thresholds['staff_review_medium_threshold']}")
    logger.debug(f"     LOW confidence: {thresholds['staff_review_low_threshold']}")
    
    logger.debug("🎯 CENTRALIZED Ensemble endpoints configured - All thresholds from environment variables")
    
    return thresholds

# ============================================================================
# INITIALIZATION FUNCTIONS (Updated for Phase 2B)
# ============================================================================

async def initialize_components_with_clean_managers():
    """Initialize all components with clean manager-only architecture - Phase 2B Update"""
    global model_manager, pydantic_manager, crisis_analyzer, phrase_extractor, learning_manager
    global config_manager, settings_manager, zero_shot_manager
    
    try:
        logger.info("🚀 Initializing components with clean manager-only architecture - Phase 2B...")
        
        # ========================================================================
        # STEP 1: Initialize Core Configuration Managers
        # ========================================================================
        logger.info("📋 Initializing core configuration managers...")
        
        config_manager = ConfigManager("/app/config")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        
        logger.info("✅ Core managers initialized successfully")
        
        # ========================================================================
        # STEP 2: Initialize PydanticManager v3.1 (Phase 2B)
        # ========================================================================
        if PYDANTIC_MANAGER_V3_1_AVAILABLE:
            logger.info("📋 Initializing PydanticManager v3.1 with clean architecture...")
            
            pydantic_manager = create_pydantic_manager(config_manager=config_manager)
            
            if not pydantic_manager.is_initialized():
                raise RuntimeError("PydanticManager failed to initialize")
            
            logger.info("✅ PydanticManager v3.1 initialized successfully")
            
            # Log model summary for verification
            summary = pydantic_manager.get_model_summary()
            logger.info(f"📊 PydanticManager Summary: {summary['total_models']} models across {len(summary['categories'])} categories")
            logger.debug(f"📋 Available model categories: {list(summary['categories'].keys())}")
            
        else:
            logger.info("⚠️ Using legacy Pydantic models - PydanticManager v3.1 not available")
            pydantic_manager = None
        
        # Test model access
        try:
            models = get_pydantic_models()
            logger.info(f"✅ Pydantic models accessible: {len(models)} models available")
            logger.debug(f"📋 Available models: {list(models.keys())}")
        except Exception as e:
            logger.error(f"❌ Failed to access Pydantic models: {e}")
            raise
        
        # ========================================================================
        # STEP 3: Validate Configuration
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
        # STEP 4: Extract and Log Configuration (with debug control)
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
            logger.debug(f"   {model_type.title()} Weight: {model_info['weight']}")
        
        logger.info(f"   Ensemble Mode: {ensemble_mode}")
        
        gap_detection_enabled = model_config.get('ensemble_config', {}).get('gap_detection', {}).get('enabled', True)
        logger.info(f"   Gap Detection: {'✅ Enabled' if gap_detection_enabled else '❌ Disabled'}")
        
        # ========================================================================
        # STEP 5: Initialize Enhanced ModelManager
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
        # STEP 6: Load Models
        # ========================================================================
        logger.info("📦 Loading Three Zero-Shot Model Ensemble...")
        await model_manager.load_models()
        logger.info("✅ All three models loaded successfully")
        
        # Set global model manager for API access
        globals()['model_manager'] = model_manager
        logger.info("✅ Global model manager set for API access")
        
        # ========================================================================
        # STEP 7: Initialize Learning System
        # ========================================================================
        if LEARNING_AVAILABLE:
            learning_config = feature_flags.get('learning_system', {})
            if learning_config.get('enabled', True):
                learning_manager = EnhancedLearningManager(
                    model_manager=model_manager,
                    config_manager=config_manager
                )
                logger.info("✅ Learning system initialized with clean manager architecture")
            else:
                logger.info("ℹ️ Learning system disabled via configuration")
                learning_manager = None
        else:
            logger.info("ℹ️ Learning system not available")
            learning_manager = None
        
        # ========================================================================
        # STEP 8: Initialize Analysis Components
        # ========================================================================
        
        # Initialize CrisisAnalyzer
        if CRISIS_ANALYZER_AVAILABLE:
            try:
                crisis_analyzer = CrisisAnalyzer(
                    model_manager=model_manager,
                    learning_manager=learning_manager
                )
                logger.info("✅ CrisisAnalyzer initialized with current architecture")
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
                    model_manager=model_manager
                )
                logger.info("✅ PhraseExtractor initialized with current architecture")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize PhraseExtractor: {e}")
                phrase_extractor = None
        else:
            logger.info("ℹ️ PhraseExtractor not available")
            phrase_extractor = None
        
        # ========================================================================
        # STEP 9: Final Status Report (Phase 2B Update)
        # ========================================================================
        logger.debug("📊 Component Initialization Summary (Phase 2B):")
        
        components_status = {
            'core_managers': {
                'config_manager': config_manager is not None,
                'settings_manager': settings_manager is not None,
                'zero_shot_manager': zero_shot_manager is not None,
                'pydantic_manager': pydantic_manager is not None  # PHASE 2B: New status
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
            logger.debug(f"   {category.replace('_', ' ').title()}:")
            for component, status in components.items():
                status_icon = "✅" if status else "❌"
                logger.debug(f"     {component}: {status_icon}")
        
        # Check if any critical components failed
        critical_failures = []
        if not model_manager:
            critical_failures.append("ModelManager")
        if model_manager and not model_manager.models_loaded():
            critical_failures.append("Model Loading")
        if not PYDANTIC_MANAGER_AVAILABLE:
            critical_failures.append("Pydantic Models")
        
        if critical_failures:
            logger.error(f"❌ Critical component failures: {critical_failures}")
            raise RuntimeError(f"Critical components failed to initialize: {critical_failures}")
        
        logger.info("✅ All critical components initialized successfully with clean manager architecture - Phase 2B")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        logger.exception("Full initialization error:")
        raise

# ============================================================================
# Health Response Model (Updated for Phase 2B)
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
    logger.info("🚀 Enhanced FastAPI app starting with Clean Manager Architecture v3.1 - Phase 2B...")
    
    try:
        await initialize_components_with_clean_managers()
        
        # Import and add ensemble endpoints after initialization - PHASE 2B UPDATE
        try:
            logger.info("🔧 Adding Three Zero-Shot Model Ensemble endpoints with Phase 2B integration...")
            from api.ensemble_endpoints import add_ensemble_endpoints
            
            # Pass pydantic_manager to endpoints for Phase 2B integration
            add_ensemble_endpoints(app, model_manager, pydantic_manager)
            logger.info("🎯 Three Zero-Shot Model Ensemble endpoints added with Phase 2B manager integration!")
            
            if pydantic_manager:
                logger.info("✅ Phase 2B: Endpoints using PydanticManager v3.1 for model management")
            else:
                logger.info("⚠️ Phase 2B: Endpoints using legacy model imports (migration recommended)")
                
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
        
        logger.info("✅ Enhanced FastAPI app startup complete with Clean Manager Architecture - Phase 2B!")
        
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
        title="Ash NLP Service v3.1 - Clean Manager Architecture (Phase 2B)", 
        version="3.1.0",
        description="Advanced crisis detection using three specialized ML models with clean JSON+ENV configuration management and PydanticManager v3.1",
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
            logger.debug("🌐 CORS middleware enabled")
        except Exception as e:
            logger.warning(f"⚠️ Could not enable CORS: {e}")
    
    logger.info("✅ FastAPI app created successfully")
else:
    logger.error("❌ Cannot create FastAPI app - FastAPI import failed")
    sys.exit(1)

# Initialize configuration early
thresholds = initialize_centralized_threshold_config()

# ============================================================================
# Health Check Endpoint (Updated for Phase 2B)
# ============================================================================
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check with clean manager architecture status - Phase 2B Update"""
    
    uptime = time.time() - startup_time
    models_loaded = model_manager and model_manager.models_loaded() if model_manager else False
    
    # Check component availability
    components_status = {
        "model_manager": model_manager is not None,
        "pydantic_manager": pydantic_manager is not None,  # PHASE 2B: New status
        "crisis_analyzer": crisis_analyzer is not None,
        "phrase_extractor": phrase_extractor is not None,
        "learning_manager": learning_manager is not None,
        "three_model_ensemble": models_loaded
    }
    
    # Manager status (Updated for Phase 2B)
    manager_status = {
        "config_manager": config_manager is not None,
        "settings_manager": settings_manager is not None,
        "zero_shot_manager": zero_shot_manager is not None,
        "pydantic_manager_v3_1": pydantic_manager is not None,  # PHASE 2B: New status
        "manager_architecture": "clean_v3.1_phase2b"  # PHASE 2B: Updated version
    }
    
    # Configuration status
    configuration_status = {
        "json_config_loaded": config_manager is not None,
        "environment_overrides_applied": True,
        "model_configuration_valid": False,
        "ensemble_mode": "unknown",
        "config_validation_passed": False,
        "pydantic_models_available": PYDANTIC_MANAGER_AVAILABLE  # PHASE 2B: New status
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
    if (models_loaded and components_status["model_manager"] and 
        manager_status["config_manager"] and PYDANTIC_MANAGER_AVAILABLE):
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