# CRITICAL FIX: Update your main.py file - FIXED LEARNING SYSTEM INTEGRATION

#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - With Secrets Support and Three Zero-Shot Model Ensemble
UPDATED: Fixed learning system integration
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

# Import enhanced configuration with secrets support
from config import get_nlp_config, get_env_config, get_api_keys_status

# Sentiment Adjustments
from utils.context_helpers import analyze_sentiment_context
from utils.scoring_helpers import (
    extract_depression_score,
    enhanced_depression_analysis,
    apply_comprehensive_false_positive_reduction
)

# CRITICAL: Import ensemble endpoints FIRST
from endpoints.ensemble_endpoints import add_ensemble_endpoints

# Initialize configuration manager with secrets support
config_manager = get_nlp_config()
config = get_env_config()  # Backward compatibility - returns dict

# Configure logging using environment variables
log_level = config['GLOBAL_LOG_LEVEL']
log_file = config['NLP_LOG_FILE']
enable_debug = config['GLOBAL_ENABLE_DEBUG_MODE']

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

# Set Hugging Face token if provided (now from secrets or environment)
hf_token = config_manager.get('GLOBAL_HUGGINGFACE_TOKEN')
if hf_token:
    os.environ['GLOBAL_HUGGINGFACE_TOKEN'] = hf_token
    logger.info("🔑 Hugging Face token configured from secrets")
elif config['GLOBAL_HUGGINGFACE_TOKEN']:
    os.environ['GLOBAL_HUGGINGFACE_TOKEN'] = config['GLOBAL_HUGGINGFACE_TOKEN']
    logger.info("🔑 Hugging Face token configured from environment")

# Log secrets status on startup
api_keys_status = get_api_keys_status()
logger.info("🔐 API Keys Status:")
for key, available in api_keys_status.items():
    status = "✅ Available" if available else "❌ Not found"
    logger.info(f"   {key}: {status}")

# Print configuration on startup if debug enabled
if enable_debug:
    logger.info("=== NLP Service Configuration (with Secrets Support) ===")
    safe_config = config_manager.get_all_safe()
    for key, value in sorted(safe_config.items()):
        logger.info(f"{key}: {value}")
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
    from endpoints.enhanced_learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
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
    logger.info("🚀 Enhanced FastAPI app starting with Three Zero-Shot Model Ensemble...")
    await initialize_components_with_config()
    
    # CRITICAL: Add ensemble endpoints AFTER initialization
    logger.info("🔧 Adding Three Zero-Shot Model Ensemble endpoints...")
    add_ensemble_endpoints(app, model_manager)
    logger.info("🎯 Three Zero-Shot Model Ensemble endpoints added - /analyze is now ensemble-powered!")
    
    # FIXED: Add learning endpoints if available
    if enhanced_learning_manager:
        logger.info("🔧 Adding enhanced learning endpoints...")
        add_enhanced_learning_endpoints(app, enhanced_learning_manager)
        logger.info("🧠 Enhanced learning endpoints added to FastAPI app!")
    else:
        logger.info("ℹ️ Learning system not available - skipping learning endpoints")
    
    logger.info("✅ Enhanced FastAPI app startup complete!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

async def initialize_components_with_config():
    global model_manager, crisis_analyzer, phrase_extractor, enhanced_learning_manager
    
    try:
        # Initialize enhanced model manager (pass config manager for secrets support)
        try:
            # Try to pass config manager if ModelManager supports it
            model_manager = ModelManager(config_manager)
            logger.info("✅ ModelManager initialized with secrets-aware config")
        except TypeError:
            # Fallback: ModelManager doesn't support config parameter yet
            model_manager = ModelManager()
            logger.info("✅ ModelManager initialized (using environment variables)")
        
        # Load models with the enhanced method
        logger.info("📦 Loading Three Zero-Shot Model Ensemble with secrets-aware configuration...")
        await model_manager.load_models()
        logger.info("✅ Enhanced ModelManager initialized and THREE MODELS loaded")
        
        # FIXED: Initialize enhanced learning manager if available and enabled
        if ENHANCED_LEARNING_AVAILABLE and config['GLOBAL_ENABLE_LEARNING_SYSTEM']:
            try:
                # Try to pass config manager if EnhancedLearningManager supports it
                try:
                    enhanced_learning_manager = EnhancedLearningManager(model_manager, config_manager)
                    logger.info("✅ Enhanced learning system initialized with secrets support")
                except TypeError:
                    # Fallback: EnhancedLearningManager doesn't support config parameter yet
                    enhanced_learning_manager = EnhancedLearningManager(model_manager)
                    logger.info("✅ Enhanced learning system initialized (using environment variables)")
            except Exception as e:
                logger.error(f"❌ Could not initialize Enhanced Learning Manager: {e}")
                logger.exception("Full initialization error:")
                enhanced_learning_manager = None
        else:
            if not ENHANCED_LEARNING_AVAILABLE:
                logger.info("ℹ️ Enhanced learning system not available")
            elif not config['GLOBAL_ENABLE_LEARNING_SYSTEM']:
                logger.info("ℹ️ Learning system disabled via GLOBAL_ENABLE_LEARNING_SYSTEM=false")
            enhanced_learning_manager = None
        
        # Initialize analyzers (only if available)
        if CRISIS_ANALYZER_AVAILABLE:
            try:
                # Try to pass config manager if CrisisAnalyzer supports it
                try:
                    crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager, config_manager)
                    logger.info("✅ Crisis analyzer initialized with secrets support")
                except TypeError:
                    # Fallback: CrisisAnalyzer doesn't support config parameter yet
                    crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager)
                    logger.info("✅ Crisis analyzer initialized (using environment variables)")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CrisisAnalyzer: {e}")
                crisis_analyzer = None
        else:
            logger.info("ℹ️ CrisisAnalyzer not available")
        
        if PHRASE_EXTRACTOR_AVAILABLE:
            try:
                # Try to pass config manager if PhraseExtractor supports it
                try:
                    phrase_extractor = PhraseExtractor(model_manager, config_manager)
                    logger.info("✅ Advanced phrase extractor initialized with secrets support")
                except TypeError:
                    # Fallback: PhraseExtractor doesn't support config parameter yet
                    phrase_extractor = PhraseExtractor(model_manager)
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

        logger.info("✅ All available components initialized with secrets-aware configuration")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise

# Create FastAPI app with enhanced config
app = FastAPI(
    title="Enhanced Ash NLP Service - Three Zero-Shot Model Ensemble", 
    version="4.5.0",  # Updated version
    description="Advanced crisis detection using three specialized ML models with ensemble consensus and secure configuration",
    lifespan=lifespan
)

# Configure CORS if enabled
if config['GLOBAL_ENABLE_CORS']:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("🌐 CORS middleware enabled")

# REMOVED: Old /analyze endpoint - now handled by ensemble_endpoints.py
# The Three Zero-Shot Model Ensemble /analyze endpoint is added via add_ensemble_endpoints()

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with component status and secrets info"""
    
    uptime = time.time() - startup_time
    models_loaded = model_manager and model_manager.models_loaded()
    
    # Check component availability
    components_status = {
        "model_manager": model_manager is not None,
        "crisis_analyzer": crisis_analyzer is not None,
        "phrase_extractor": phrase_extractor is not None,
        "enhanced_learning": enhanced_learning_manager is not None,  # FIXED
        "three_model_ensemble": model_manager and hasattr(model_manager, 'analyze_with_ensemble')
    }
    
    # Get API keys status
    api_keys_status = get_api_keys_status()
    
    status = "healthy" if models_loaded else "unhealthy"
    
    return HealthResponse(
        status=status,
        model_loaded=models_loaded,
        uptime_seconds=uptime,
        hardware_info={
            "device": config['NLP_DEVICE'],
            "precision": config['NLP_MODEL_PRECISION'],
            "max_batch_size": config['NLP_MAX_BATCH_SIZE'],
            "inference_threads": config['NLP_INFERENCE_THREADS'],
            "components_available": components_status,
            "learning_system": "enabled" if enhanced_learning_manager else "disabled",  # FIXED
            "secrets_status": api_keys_status,
            "using_secrets": any(api_keys_status.values()),
            "ensemble_info": {
                "models_count": 3,
                "ensemble_modes": ["consensus", "majority", "weighted"],
                "gap_detection": "enabled"
            }
        }
    )

# Stats endpoint
@app.get("/stats")
async def get_stats():
    """Get service statistics with configuration and secrets info"""
    
    uptime = time.time() - startup_time
    api_keys_status = get_api_keys_status()
    
    stats = {
        "service": "Enhanced Ash NLP Service - Three Zero-Shot Model Ensemble",
        "version": "4.5.0",
        "uptime_seconds": uptime,
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "configuration": {
            "learning_enabled": config['GLOBAL_ENABLE_LEARNING_SYSTEM'],
            "device": config['NLP_DEVICE'],
            "precision": config['NLP_MODEL_PRECISION'],
            "using_secrets": any(api_keys_status.values()),
            "ensemble_enabled": True,
            "models_count": 3,
            "thresholds": {
                "high": config.get('NLP_HIGH_CRISIS_THRESHOLD', 0.55),
                "medium": config.get('NLP_MEDIUM_CRISIS_THRESHOLD', 0.28),
                "low": config.get('NLP_LOW_CRISIS_THRESHOLD', 0.16)
            }
        },
        "secrets_status": api_keys_status,
        "components_available": {
            "model_manager": model_manager is not None,
            "crisis_analyzer": CRISIS_ANALYZER_AVAILABLE and crisis_analyzer is not None,
            "phrase_extractor": PHRASE_EXTRACTOR_AVAILABLE and phrase_extractor is not None,
            "enhanced_learning": ENHANCED_LEARNING_AVAILABLE and enhanced_learning_manager is not None,  # FIXED
            "three_model_ensemble": model_manager and hasattr(model_manager, 'analyze_with_ensemble')
        },
        "hardware_config": {
            "max_batch_size": config['NLP_MAX_BATCH_SIZE'],
            "inference_threads": config['NLP_INFERENCE_THREADS'],
            "max_concurrent_requests": config['NLP_MAX_CONCURRENT_REQUESTS'],
            "request_timeout": config['NLP_REQUEST_TIMEOUT']
        },
        "ensemble_info": {
            "depression_model": config.get('NLP_DEPRESSION_MODEL', 'unknown'),
            "sentiment_model": config.get('NLP_SENTIMENT_MODEL', 'unknown'),
            "emotional_distress_model": config.get('NLP_EMOTIONAL_DISTRESS_MODEL', 'unknown'),
            "ensemble_mode": config.get('NLP_ENSEMBLE_MODE', 'weighted'),
            "gap_detection_enabled": True
        }
    }
    
    return stats

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v3.0 (Three Zero-Shot Model Ensemble)")
    logger.info("🔧 Configuration loaded with secrets-aware management")
    logger.info("🧠 Three specialized models with ensemble consensus")
    
    # Get server configuration from enhanced config
    host = config['NLP_SERVICE_HOST']
    port = config['NLP_SERVICE_PORT']
    workers = config['NLP_UVICORN_WORKERS']
    reload = config['NLP_RELOAD_ON_CHANGES']
    
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