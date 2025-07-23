#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - Environment Variable Integration
Updated to use centralized environment configuration
"""

from fastapi import FastAPI, HTTPException
import logging
import time
import uvicorn
from contextlib import asynccontextmanager

# Import configuration manager
from config.env_manager import get_config, get_config_value

# Import existing components (unchanged)
from models.pydantic_models import (
    MessageRequest, CrisisResponse, HealthResponse,
    PhraseExtractionRequest, PatternLearningRequest, SemanticAnalysisRequest
)
from models.ml_models import ModelManager
from analysis.crisis_analyzer import CrisisAnalyzer
from analysis.phrase_extractor import PhraseExtractor
from analysis.pattern_learner import PatternLearner
from analysis.semantic_analyzer import SemanticAnalyzer

# Get configuration
config = get_config()

# Configure logging using environment variables
log_level = get_config_value('LOG_LEVEL', 'INFO')
log_file = get_config_value('LOG_FILE', 'nlp_service.log')
enable_debug = get_config_value('ENABLE_DEBUG_LOGGING', False)

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Print configuration on startup
if enable_debug:
    config.print_config()

# Global components (updated to use config)
model_manager = None
crisis_analyzer = None
phrase_extractor = None
pattern_learner = None
semantic_analyzer = None
enhanced_learning_manager = None
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting with environment configuration...")
    await initialize_components_with_config()
    logger.info("✅ Enhanced FastAPI app startup complete!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

async def initialize_components_with_config():
    global model_manager, crisis_analyzer, phrase_extractor, pattern_learner, semantic_analyzer, enhanced_learning_manager
    
    try:
        # Initialize model manager with config
        model_config = {
            'depression_model': get_config_value('DEPRESSION_MODEL'),
            'sentiment_model': get_config_value('SENTIMENT_MODEL'),
            'cache_dir': get_config_value('MODEL_CACHE_DIR'),
            'device': get_config_value('DEVICE'),
            'precision': get_config_value('MODEL_PRECISION'),
            'max_batch_size': get_config_value('MAX_BATCH_SIZE'),
            'huggingface_token': get_config_value('HUGGINGFACE_HUB_TOKEN')
        }
        
        model_manager = ModelManager(model_config)
        await model_manager.load_models()
        
        # Initialize learning system with config
        learning_config = {
            'enable_learning': get_config_value('ENABLE_LEARNING_SYSTEM'),
            'learning_rate': get_config_value('LEARNING_RATE'),
            'max_adjustments_per_day': get_config_value('MAX_LEARNING_ADJUSTMENTS_PER_DAY'),
            'persistence_file': get_config_value('LEARNING_PERSISTENCE_FILE'),
            'min_adjustment': get_config_value('MIN_CONFIDENCE_ADJUSTMENT'),
            'max_adjustment': get_config_value('MAX_CONFIDENCE_ADJUSTMENT')
        }
        
        if learning_config['enable_learning']:
            from utils.enhanced_learning_endpoints import EnhancedLearningManager
            enhanced_learning_manager = EnhancedLearningManager(model_manager, learning_config)
        
        # Initialize analyzers with config
        crisis_config = {
            'high_threshold': get_config_value('HIGH_CRISIS_THRESHOLD'),
            'medium_threshold': get_config_value('MEDIUM_CRISIS_THRESHOLD'),
            'low_threshold': get_config_value('LOW_CRISIS_THRESHOLD')
        }
        
        crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager, crisis_config)
        phrase_extractor = PhraseExtractor(model_manager)
        pattern_learner = PatternLearner(model_manager)
        semantic_analyzer = SemanticAnalyzer(model_manager)
        
        logger.info("✅ All components initialized with environment configuration")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise

# Create FastAPI app with config
app = FastAPI(
    title="Enhanced Ash NLP Service with Environment Configuration", 
    version="4.3",
    description="Multi-model Mental Health Crisis Detection with Full Environment Variable Support",
    lifespan=lifespan
)

# Configure CORS if enabled
if get_config_value('ENABLE_CORS', True):
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add rate limiting if configured
# TODO: Implement rate limiting based on MAX_REQUESTS_PER_MINUTE/HOUR

# Existing endpoints remain the same but now use config values...
# [Keep all existing endpoint code but integrate config values where appropriate]

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v4.3 (Full Environment Support)")
    logger.info("🔧 Configuration loaded from environment variables")
    logger.info("🧠 Advanced capabilities with environment-driven configuration")
    
    # Get server configuration from environment
    host = get_config_value('NLP_SERVICE_HOST', '0.0.0.0')
    port = get_config_value('NLP_SERVICE_PORT', 8881)
    workers = get_config_value('UVICORN_WORKERS', 1)
    reload = get_config_value('RELOAD_ON_CHANGES', False)
    
    logger.info(f"🌐 Starting server on {host}:{port} with {workers} workers")
    
    try:
        uvicorn.run(
            "nlp_main:app",
            host=host,
            port=port,
            log_level=log_level.lower(),
            reload=reload,
            workers=workers
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise