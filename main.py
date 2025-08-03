#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - With JSON Configuration and Three Zero-Shot Model Ensemble
UPDATED: Now uses managers/ directory for organized configuration management
"""

from fastapi import FastAPI, HTTPException
import logging
import time
import uvicorn
import os
from contextlib import asynccontextmanager
from pathlib import Path

# Import existing components
from models.pydantic_models import (
    # Core models
    MessageRequest, CrisisResponse, HealthResponse,
    
    # Learning models (now centralized)
    FalsePositiveAnalysisRequest, FalseNegativeAnalysisRequest, LearningUpdateRequest,
    
    # Learning response models (if you want to use them for type hints)
    FalsePositiveAnalysisResponse, FalseNegativeAnalysisResponse, 
    LearningUpdateResponse, LearningStatisticsResponse
)

# UPDATED: Import from managers/ directory - organized configuration management
from managers import (
    # Model Ensemble Configuration (JSON)
    get_model_ensemble_manager,
    get_model_definitions,
    get_ensemble_configuration,
    get_threshold_configuration,
    get_hardware_optimization,
    get_feature_flags,
    
    # Environment and NLP Config (backward compatibility)
    get_nlp_config, 
    get_env_config, 
    get_api_keys_status,
    
    # Manager utilities
    get_all_config_summary,
    validate_all_configs,
    MANAGERS_STATUS,
    CONFIG_MANAGER_AVAILABLE,
    SETTINGS_MANAGER_AVAILABLE
)

# Sentiment Adjustments
try:
    from utils.context_helpers import analyze_sentiment_context
    from utils.scoring_helpers import (
        extract_depression_score,
        enhanced_depression_analysis,
        apply_comprehensive_false_positive_reduction
    )
    UTILS_AVAILABLE = True
except ImportError as e:
    UTILS_AVAILABLE = False
    logging.warning(f"⚠️ Utils not available: {e}")

# CRITICAL: Import ensemble endpoints FIRST
try:
    from api.ensemble_endpoints import add_ensemble_endpoints
    ENSEMBLE_ENDPOINTS_AVAILABLE = True
except ImportError as e:
    ENSEMBLE_ENDPOINTS_AVAILABLE = False
    logging.warning(f"⚠️ Ensemble endpoints not available: {e}")

# Initialize configuration managers with safety checks
config_manager = get_nlp_config() if CONFIG_MANAGER_AVAILABLE else None
config = get_env_config() if get_env_config else {}  # Always available with fallback

# UPDATED: Load JSON configuration from managers/
try:
    ensemble_manager = get_model_ensemble_manager()
    ensemble_config = ensemble_manager.get_config()
    print("✅ JSON model ensemble configuration loaded successfully from managers/")
    
    # Log configuration summary
    config_summary = ensemble_manager.get_summary()
    print(f"📊 Ensemble Config Summary: {config_summary}")
    
    # Log all managers status
    managers_status = MANAGERS_STATUS
    print(f"📦 Managers Status: {managers_status}")
    print(f"   Config Manager Available: {CONFIG_MANAGER_AVAILABLE}")
    print(f"   Settings Manager Available: {SETTINGS_MANAGER_AVAILABLE}")
    
except Exception as e:
    print(f"❌ Failed to load JSON model ensemble configuration: {e}")
    print("⚠️ Falling back to environment variable configuration")
    ensemble_config = None
    ensemble_manager = None

# Configure logging using environment variables OR JSON config
if ensemble_config:
    # Use hardware optimization settings from JSON
    hardware_config = get_hardware_optimization()
    log_level = config.get('GLOBAL_LOG_LEVEL', 'INFO')
    log_file = config.get('NLP_LOG_FILE', 'nlp_service.log')
    enable_debug = config.get('GLOBAL_ENABLE_DEBUG_MODE', False)
else:
    # Fallback to environment variables or defaults
    log_level = config.get('GLOBAL_LOG_LEVEL', 'INFO')
    log_file = config.get('NLP_LOG_FILE', 'nlp_service.log')
    enable_debug = config.get('GLOBAL_ENABLE_DEBUG_MODE', False)

# Set PYTHONUNBUFFERED for Docker
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure logging
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add this import for admin endpoints
try:
    from api.admin_endpoints import admin_router
    ADMIN_ENDPOINTS_AVAILABLE = True
    logger.info("✅ Admin endpoints module loaded")
except ImportError as e:
    ADMIN_ENDPOINTS_AVAILABLE = False
    logger.warning(f"⚠️ Admin endpoints not available: {e}")
    logger.warning("⚠️ Create api/admin_endpoints.py for label management")

# Set Hugging Face token if provided (now from secrets or environment)
hf_token = config_manager.get('GLOBAL_HUGGINGFACE_TOKEN') if config_manager else None
if hf_token:
    os.environ['GLOBAL_HUGGINGFACE_TOKEN'] = hf_token
    logger.info("🔑 Hugging Face token configured from secrets")
elif config.get('GLOBAL_HUGGINGFACE_TOKEN'):
    os.environ['GLOBAL_HUGGINGFACE_TOKEN'] = config['GLOBAL_HUGGINGFACE_TOKEN']
    logger.info("🔑 Hugging Face token configured from environment")

# Log secrets status on startup
api_keys_status = get_api_keys_status()
logger.info("🔐 API Keys Status:")
for key, available in api_keys_status.items():
    status = "✅ Available" if available else "❌ Not found"
    logger.info(f"   {key}: {status}")

# UPDATED: Log JSON configuration status from managers/
if ensemble_config:
    logger.info("🎯 JSON Configuration Status (managers/):")
    logger.info(f"   Model Ensemble Config: ✅ Loaded from {ensemble_manager.config_file}")
    
    model_defs = get_model_definitions()
    for model_name, model_config in model_defs.items():
        logger.info(f"   {model_name.title()} Model: {model_config['name']}")
        logger.info(f"   {model_name.title()} Weight: {model_config.get('weight', 'default')}")
    
    ensemble_mode = get_ensemble_configuration().get('default_mode', 'unknown')
    logger.info(f"   Ensemble Mode: {ensemble_mode}")
    
    gap_detection = get_ensemble_configuration().get('gap_detection', {})
    gap_enabled = gap_detection.get('enabled', False)
    logger.info(f"   Gap Detection: {'✅ Enabled' if gap_enabled else '❌ Disabled'}")

# Print configuration on startup if debug enabled
if enable_debug:
    logger.info("=== NLP Service Configuration (managers/ + Secrets Support) ===")
    if config_manager:
        safe_config = config_manager.get_all_safe() if hasattr(config_manager, 'get_all_safe') else {}
        for key, value in sorted(safe_config.items()):
            logger.info(f"{key}: {value}")
    
    if ensemble_config:
        logger.info("\n=== JSON Model Ensemble Configuration (managers/) ===")
        summary = ensemble_manager.get_summary()
        for key, value in sorted(summary.items()):
            logger.info(f"{key}: {value}")
    
    # Log all configuration validation
    logger.info("\n=== Configuration Validation ===")
    validation_results = validate_all_configs()
    for config_name, result in validation_results.items():
        status = "✅ Valid" if result["status"] == "valid" else "❌ Invalid"
        logger.info(f"{config_name}: {status}")
        if result["errors"]:
            for error in result["errors"]:
                logger.warning(f"   Error: {error}")
    
    logger.info("=== End Configuration ===")

# Import ModelManager with backward compatibility (after logger is defined)
try:
    from models.ml_models import EnhancedModelManager as ModelManager
    logger.info("✅ Using Enhanced ModelManager")
except ImportError:
    try:
        from models.ml_models import ModelManager
        logger.info("⚠️ Using basic ModelManager (enhanced features not available)")
    except ImportError:
        logger.error("❌ Could not import ModelManager")
        raise

# Try to import optional components with diagnostic logging
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

# FIXED: Import learning system with proper error handling
try:
    from api.learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    ENHANCED_LEARNING_AVAILABLE = True
    logger.info("✅ EnhancedLearningManager import successful")
except ImportError as e:
    ENHANCED_LEARNING_AVAILABLE = False
    logger.warning(f"⚠️ EnhancedLearningManager import failed: {e}")
    logger.info("ℹ️ Learning system will be disabled")

# Global components
model_manager = None
crisis_analyzer = None
phrase_extractor = None
enhanced_learning_manager = None
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting with managers/ JSON Configuration + Three Zero-Shot Model Ensemble...")
    await initialize_components_with_managers_config()
    
    # CRITICAL: Add ensemble endpoints AFTER initialization
    if ENSEMBLE_ENDPOINTS_AVAILABLE and model_manager:
        logger.info("🔧 Adding Three Zero-Shot Model Ensemble endpoints...")
        add_ensemble_endpoints(app, model_manager)
        logger.info("🎯 Three Zero-Shot Model Ensemble endpoints added - /analyze is now ensemble-powered!")
    else:
        logger.warning("⚠️ Ensemble endpoints not available - /analyze endpoint not added")
    
    # FIXED: Add learning endpoints if available
    if enhanced_learning_manager:
        logger.info("🔧 Adding enhanced learning endpoints...")
        add_enhanced_learning_endpoints(app, enhanced_learning_manager)
        logger.info("🧠 Enhanced learning endpoints added to FastAPI app!")
    else:
        logger.info("ℹ️ Learning system not available - skipping learning endpoints")
    
    logger.info("✅ Enhanced FastAPI app startup complete with managers/ JSON configuration!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

async def initialize_components_with_managers_config():
    """UPDATED: Initialize components using managers/ JSON configuration where available"""
    global model_manager, crisis_analyzer, phrase_extractor, enhanced_learning_manager
    
    try:
        # UPDATED: Initialize enhanced model manager with managers/ JSON config
        try:
            if ensemble_manager:
                # Pass both config manager and JSON ensemble manager
                model_manager = ModelManager(config_manager, ensemble_manager)
                logger.info("✅ ModelManager initialized with managers/ JSON config + secrets support")
            else:
                # Fallback to config manager only
                model_manager = ModelManager(config_manager)
                logger.info("✅ ModelManager initialized with secrets-aware config (no JSON)")
        except TypeError:
            # Fallback: ModelManager doesn't support new parameters yet
            model_manager = ModelManager()
            logger.info("✅ ModelManager initialized (using environment variables)")
        
        # Load models with the enhanced method
        if ensemble_config:
            logger.info("📦 Loading Three Zero-Shot Model Ensemble with managers/ JSON configuration...")
        else:
            logger.info("📦 Loading Three Zero-Shot Model Ensemble with environment configuration...")
            
        await model_manager.load_models()
        logger.info("✅ Enhanced ModelManager initialized and THREE MODELS loaded")
        
        # CRITICAL FIX: Set the global model manager for API access
        from models.ml_models import set_model_manager
        set_model_manager(model_manager)
        logger.info("✅ Global model manager set for API access")
        
        # UPDATED: Initialize enhanced learning manager with managers/ JSON config if available
        learning_enabled = False
        if ensemble_config:
            learning_flags = get_feature_flags().get('learning_system', {})
            learning_enabled = learning_flags.get('enabled', False)
        else:
            learning_enabled = config.get('GLOBAL_ENABLE_LEARNING_SYSTEM', False)
        
        if ENHANCED_LEARNING_AVAILABLE and learning_enabled:
            try:
                if ensemble_manager:
                    # Try to pass both config manager and JSON manager
                    try:
                        enhanced_learning_manager = EnhancedLearningManager(model_manager, config_manager, ensemble_manager)
                        logger.info("✅ Enhanced learning system initialized with managers/ JSON config + secrets support")
                    except TypeError:
                        # Fallback: EnhancedLearningManager doesn't support JSON config yet
                        enhanced_learning_manager = EnhancedLearningManager(model_manager, config_manager)
                        logger.info("✅ Enhanced learning system initialized with secrets support")
                else:
                    # Fallback: Use config manager only
                    enhanced_learning_manager = EnhancedLearningManager(model_manager, config_manager)
                    logger.info("✅ Enhanced learning system initialized (using environment variables)")
            except Exception as e:
                logger.error(f"❌ Could not initialize Enhanced Learning Manager: {e}")
                logger.exception("Full initialization error:")
                enhanced_learning_manager = None
        else:
            if not ENHANCED_LEARNING_AVAILABLE:
                logger.info("ℹ️ Enhanced learning system not available")
            elif not learning_enabled:
                logger.info("ℹ️ Learning system disabled via configuration")
            enhanced_learning_manager = None
        
        # UPDATED: Initialize analyzers with managers/ JSON config if available
        if CRISIS_ANALYZER_AVAILABLE:
            try:
                if ensemble_manager:
                    # Try to pass JSON manager
                    try:
                        crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager, config_manager, ensemble_manager)
                        logger.info("✅ Crisis analyzer initialized with managers/ JSON config + secrets support")
                    except TypeError:
                        # Fallback: CrisisAnalyzer doesn't support JSON config yet
                        crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager, config_manager)
                        logger.info("✅ Crisis analyzer initialized with secrets support")
                else:
                    # Fallback to config manager only
                    crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager, config_manager)
                    logger.info("✅ Crisis analyzer initialized (using environment variables)")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CrisisAnalyzer: {e}")
                crisis_analyzer = None
        else:
            logger.info("ℹ️ CrisisAnalyzer not available")
        
        if PHRASE_EXTRACTOR_AVAILABLE:
            try:
                if ensemble_manager:
                    # Try to pass JSON manager
                    try:
                        phrase_extractor = PhraseExtractor(model_manager, config_manager, ensemble_manager)
                        logger.info("✅ Advanced phrase extractor initialized with managers/ JSON config + secrets support")
                    except TypeError:
                        # Fallback: PhraseExtractor doesn't support JSON config yet
                        phrase_extractor = PhraseExtractor(model_manager, config_manager)
                        logger.info("✅ Advanced phrase extractor initialized with secrets support")
                else:
                    # Fallback to config manager only
                    phrase_extractor = PhraseExtractor(model_manager, config_manager)
                    logger.info("✅ Advanced phrase extractor initialized (using environment variables)")
            except ImportError as e:
                logger.warning(f"⚠️ Import error in PhraseExtractor: {e}")
                phrase_extractor = None
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize PhraseExtractor: {e}")
                logger.exception("Full initialization error:")
                phrase_extractor = None
        else:
            logger.info("ℹ️ PhraseExtractor not available")
            phrase_extractor = None

        if ensemble_config:
            logger.info("✅ All available components initialized with managers/ JSON configuration + secrets support")
        else:
            logger.info("✅ All available components initialized with environment + secrets configuration")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise

# Create FastAPI app with enhanced config
app = FastAPI(
    title="Enhanced Ash NLP Service - managers/ JSON Configured Three Zero-Shot Model Ensemble", 
    version="3.1.0",  # Updated version for managers/ architecture
    description="Advanced crisis detection using three specialized ML models with managers/ JSON configuration, ensemble consensus, and secure configuration",
    lifespan=lifespan
)

# Add admin endpoints if available
if ADMIN_ENDPOINTS_AVAILABLE:
    app.include_router(admin_router)
    logger.info("✅ Admin endpoints added - /admin/labels/* routes available")
else:
    logger.warning("⚠️ Admin endpoints not included - label management via API unavailable")

# Configure CORS if enabled
cors_enabled = config.get('GLOBAL_ENABLE_CORS', False) if config else False
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

# UPDATED: Health check endpoint with managers/ JSON config info
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with component status, secrets info, and managers/ JSON config status"""
    
    uptime = time.time() - startup_time
    models_loaded = model_manager and model_manager.models_loaded()
    
    # Check component availability
    components_status = {
        "model_manager": model_manager is not None,
        "crisis_analyzer": crisis_analyzer is not None,
        "phrase_extractor": phrase_extractor is not None,
        "enhanced_learning": enhanced_learning_manager is not None,
        "three_model_ensemble": model_manager and hasattr(model_manager, 'analyze_with_ensemble'),
        "json_configuration": ensemble_config is not None,
        "managers_available": MANAGERS_STATUS
    }
    
    # Get API keys status
    api_keys_status = get_api_keys_status()
    
    # UPDATED: Add managers/ JSON configuration info
    json_config_info = {}
    if ensemble_manager:
        json_config_info = ensemble_manager.get_summary()
        json_config_info["config_file_modified"] = ensemble_manager.is_config_modified()
        json_config_info["managers_directory"] = "managers/"
    
    status = "healthy" if models_loaded else "unhealthy"
    
    # UPDATED: Get hardware info from managers/ JSON config if available
    if ensemble_config:
        hardware_config = get_hardware_optimization()
        device_info = {
            "device": hardware_config.get('device', config.get('NLP_DEVICE', 'auto')),
            "precision": hardware_config.get('precision', config.get('NLP_MODEL_PRECISION', 'float16')),
            "max_batch_size": hardware_config.get('performance_settings', {}).get('max_batch_size', config.get('NLP_MAX_BATCH_SIZE', 32)),
            "inference_threads": hardware_config.get('performance_settings', {}).get('inference_threads', config.get('NLP_INFERENCE_THREADS', 16)),
        }
    else:
        device_info = {
            "device": config.get('NLP_DEVICE', 'auto'),
            "precision": config.get('NLP_MODEL_PRECISION', 'float16'),
            "max_batch_size": config.get('NLP_MAX_BATCH_SIZE', 32),
            "inference_threads": config.get('NLP_INFERENCE_THREADS', 16),
        }
    
    return HealthResponse(
        status=status,
        model_loaded=models_loaded,
        uptime_seconds=uptime,
        hardware_info={
            **device_info,
            "components_available": components_status,
            "learning_system": "enabled" if enhanced_learning_manager else "disabled",
            "secrets_status": api_keys_status,
            "using_secrets": any(api_keys_status.values()),
            "json_configuration": json_config_info,
            "ensemble_info": {
                "models_count": 3,
                "ensemble_modes": ["consensus", "majority", "weighted"],
                "gap_detection": "enabled",
                "configuration_source": "managers/json" if ensemble_config else "environment"
            }
        }
    )

# UPDATED: Stats endpoint with managers/ JSON config details
@app.get("/stats")
async def get_stats():
    """Get service statistics with configuration, secrets info, and managers/ JSON config details"""
    
    uptime = time.time() - startup_time
    api_keys_status = get_api_keys_status()
    
    # UPDATED: Get configuration from managers/ JSON or environment
    if ensemble_config:
        ensemble_cfg = get_ensemble_configuration()
        threshold_cfg = get_threshold_configuration()
        hardware_cfg = get_hardware_optimization()
        feature_flags = get_feature_flags()
        
        config_source = "managers/json"
        learning_enabled = feature_flags.get('learning_system', {}).get('enabled', False)
        ensemble_mode = ensemble_cfg.get('default_mode', 'weighted')
        device = hardware_cfg.get('device', 'auto')
        precision = hardware_cfg.get('precision', 'float16')
        
        # Get thresholds from JSON
        ensemble_thresholds = threshold_cfg.get('ensemble_thresholds', {})
        thresholds = {
            "high": ensemble_thresholds.get('high', 0.45),
            "medium": ensemble_thresholds.get('medium', 0.25),
            "low": ensemble_thresholds.get('low', 0.12)
        }
    else:
        config_source = "environment"
        learning_enabled = config.get('GLOBAL_ENABLE_LEARNING_SYSTEM', False)
        ensemble_mode = config.get('NLP_ENSEMBLE_MODE', 'weighted')
        device = config.get('NLP_DEVICE', 'auto')
        precision = config.get('NLP_MODEL_PRECISION', 'float16')
        
        # Get thresholds from environment
        thresholds = {
            "high": config.get('NLP_HIGH_CRISIS_THRESHOLD', 0.55),
            "medium": config.get('NLP_MEDIUM_CRISIS_THRESHOLD', 0.28),
            "low": config.get('NLP_LOW_CRISIS_THRESHOLD', 0.16)
        }
    
    stats = {
        "service": "Enhanced Ash NLP Service - managers/ JSON Configured Three Zero-Shot Model Ensemble",
        "version": "3.1.0",
        "uptime_seconds": uptime,
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "configuration": {
            "source": config_source,
            "learning_enabled": learning_enabled,
            "device": device,
            "precision": precision,
            "using_secrets": any(api_keys_status.values()),
            "ensemble_enabled": True,
            "models_count": 3,
            "ensemble_mode": ensemble_mode,
            "thresholds": thresholds,
            "managers_status": MANAGERS_STATUS
        },
        "secrets_status": api_keys_status,
        "components_available": {
            "model_manager": model_manager is not None,
            "crisis_analyzer": CRISIS_ANALYZER_AVAILABLE and crisis_analyzer is not None,
            "phrase_extractor": PHRASE_EXTRACTOR_AVAILABLE and phrase_extractor is not None,
            "enhanced_learning": ENHANCED_LEARNING_AVAILABLE and enhanced_learning_manager is not None,
            "three_model_ensemble": model_manager and hasattr(model_manager, 'analyze_with_ensemble'),
            "json_configuration": ensemble_config is not None
        }
    }
    
    # UPDATED: Add managers/ JSON-specific configuration details
    if ensemble_config:
        stats["json_configuration"] = ensemble_manager.get_summary()
        stats["managers_directory"] = "managers/"
        
        # Add model details from JSON
        model_defs = get_model_definitions()
        stats["ensemble_details"] = {
            "models": {name: {"name": cfg["name"], "weight": cfg.get("weight")} for name, cfg in model_defs.items()},
            "gap_detection": get_ensemble_configuration().get('gap_detection', {}),
            "hardware_optimization": get_hardware_optimization(),
            "validation_status": validate_all_configs()
        }
    
    return stats

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v3.1 (managers/ JSON Configured Three Zero-Shot Model Ensemble)")
    logger.info("🔧 Configuration loaded with managers/ JSON + secrets-aware management")
    logger.info("🧠 Three specialized models with JSON-configured ensemble consensus")
    logger.info("🏷️ Configuration Status:")
    
    if ensemble_config:
        logger.info(f"   managers/ JSON Configuration: ✅ Loaded from {ensemble_manager.config_file}")
        logger.info(f"   Environment Variables: ✅ Supporting JSON substitution")
    else:
        logger.info(f"   managers/ JSON Configuration: ❌ Not loaded, using environment variables")
        logger.info(f"   Environment Variables: ✅ Primary configuration source")
    
    logger.info(f"   Admin Endpoints: {'✅ Available' if ADMIN_ENDPOINTS_AVAILABLE else '❌ Not Available'}")
    logger.info(f"   Secrets Support: ✅ Enabled")
    logger.info(f"   Managers Status: {MANAGERS_STATUS}")
    
    # UPDATED: Get server configuration from managers/ JSON or environment
    if ensemble_config:
        # Try to get from hardware optimization first, fallback to environment
        hardware_config = get_hardware_optimization()
        host = config.get('NLP_SERVICE_HOST', '0.0.0.0')  # Not in JSON yet
        port = config.get('NLP_SERVICE_PORT', 8881)      # Not in JSON yet
        workers = config.get('NLP_UVICORN_WORKERS', 1)   # Not in JSON yet
        reload = config.get('NLP_RELOAD_ON_CHANGES', False)  # Not in JSON yet
    else:
        # Use environment variables
        host = config.get('NLP_SERVICE_HOST', '0.0.0.0')
        port = config.get('NLP_SERVICE_PORT', 8881)
        workers = config.get('NLP_UVICORN_WORKERS', 1)
        reload = config.get('NLP_RELOAD_ON_CHANGES', False)
    
    logger.info(f"🌐 Starting server on {host}:{port} with {workers} workers")
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            log_level=log_level.lower(),
            reload=reload,
            workers=workers
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise