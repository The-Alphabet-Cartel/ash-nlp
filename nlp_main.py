#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - Environment Variable Integration
Fixed to work with existing ModelManager architecture
"""

from fastapi import FastAPI, HTTPException
import logging
import time
import uvicorn
import os
from contextlib import asynccontextmanager
from pathlib import Path

from models.pydantic_models import (
    MessageRequest, CrisisResponse, HealthResponse,
    PhraseExtractionRequest, PatternLearningRequest, SemanticAnalysisRequest
)

# Try to import optional components (they may not exist yet)
try:
    from analysis.crisis_analyzer import CrisisAnalyzer
    CRISIS_ANALYZER_AVAILABLE = True
except ImportError:
    CRISIS_ANALYZER_AVAILABLE = False

try:
    from analysis.phrase_extractor import PhraseExtractor
    PHRASE_EXTRACTOR_AVAILABLE = True
except ImportError:
    PHRASE_EXTRACTOR_AVAILABLE = False

try:
    from analysis.pattern_learner import PatternLearner
    PATTERN_LEARNER_AVAILABLE = True
except ImportError:
    PATTERN_LEARNER_AVAILABLE = False

try:
    from analysis.semantic_analyzer import SemanticAnalyzer
    SEMANTIC_ANALYZER_AVAILABLE = True
except ImportError:
    SEMANTIC_ANALYZER_AVAILABLE = False

try:
    from utils.enhanced_learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    ENHANCED_LEARNING_AVAILABLE = True
except ImportError:
    ENHANCED_LEARNING_AVAILABLE = False

# Environment variable configuration with defaults
def get_env_config():
    """Get configuration from environment variables with proper defaults"""
    
    # Create directories if they don't exist
    directories = [
        os.getenv('DATA_DIR', './data'),
        os.getenv('MODELS_DIR', './models'),
        os.getenv('LOGS_DIR', './logs'),
        os.getenv('LEARNING_DATA_DIR', './learning_data'),
        os.path.dirname(os.getenv('MODEL_CACHE_DIR', './models/cache')),
        os.path.dirname(os.getenv('LEARNING_PERSISTENCE_FILE', './learning_data/adjustments.json')),
    ]
    
    for directory in directories:
        if directory and directory != '.':
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    config = {
        # Hugging Face Configuration
        'HUGGINGFACE_HUB_TOKEN': os.getenv('HUGGINGFACE_HUB_TOKEN'),
        'HUGGINGFACE_CACHE_DIR': os.getenv('HUGGINGFACE_CACHE_DIR', './models/cache'),
        
        # Learning System Configuration
        'ENABLE_LEARNING_SYSTEM': os.getenv('ENABLE_LEARNING_SYSTEM', 'true').lower() in ('true', '1', 'yes'),
        'LEARNING_RATE': float(os.getenv('LEARNING_RATE', '0.1')),
        'MAX_LEARNING_ADJUSTMENTS_PER_DAY': int(os.getenv('MAX_LEARNING_ADJUSTMENTS_PER_DAY', '50')),
        'LEARNING_PERSISTENCE_FILE': os.getenv('LEARNING_PERSISTENCE_FILE', './learning_data/adjustments.json'),
        'MIN_CONFIDENCE_ADJUSTMENT': float(os.getenv('MIN_CONFIDENCE_ADJUSTMENT', '0.05')),
        'MAX_CONFIDENCE_ADJUSTMENT': float(os.getenv('MAX_CONFIDENCE_ADJUSTMENT', '0.30')),
        
        # Model Configuration
        'DEPRESSION_MODEL': os.getenv('DEPRESSION_MODEL', 'rafalposwiata/deproberta-large-depression'),
        'SENTIMENT_MODEL': os.getenv('SENTIMENT_MODEL', 'cardiffnlp/twitter-roberta-base-sentiment-latest'),
        'MODEL_CACHE_DIR': os.getenv('MODEL_CACHE_DIR', './models/cache'),
        
        # Hardware Configuration
        'DEVICE': os.getenv('DEVICE', 'auto'),
        'MODEL_PRECISION': os.getenv('MODEL_PRECISION', 'float16'),
        
        # Performance Tuning
        'MAX_BATCH_SIZE': int(os.getenv('MAX_BATCH_SIZE', '32')),
        'INFERENCE_THREADS': int(os.getenv('INFERENCE_THREADS', '4')),
        'MAX_CONCURRENT_REQUESTS': int(os.getenv('MAX_CONCURRENT_REQUESTS', '10')),
        'REQUEST_TIMEOUT': int(os.getenv('REQUEST_TIMEOUT', '30')),
        
        # Server Configuration
        'NLP_SERVICE_HOST': os.getenv('NLP_SERVICE_HOST', '0.0.0.0'),
        'NLP_SERVICE_PORT': int(os.getenv('NLP_SERVICE_PORT', '8881')),
        'UVICORN_WORKERS': int(os.getenv('UVICORN_WORKERS', '1')),
        'RELOAD_ON_CHANGES': os.getenv('RELOAD_ON_CHANGES', 'false').lower() in ('true', '1', 'yes'),
        
        # Logging Configuration
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO').upper(),
        'LOG_FILE': os.getenv('LOG_FILE', 'nlp_service.log'),
        'ENABLE_DEBUG_LOGGING': os.getenv('ENABLE_DEBUG_LOGGING', 'false').lower() in ('true', '1', 'yes'),
        
        # Crisis Detection Thresholds
        'HIGH_CRISIS_THRESHOLD': float(os.getenv('HIGH_CRISIS_THRESHOLD', '0.7')),
        'MEDIUM_CRISIS_THRESHOLD': float(os.getenv('MEDIUM_CRISIS_THRESHOLD', '0.4')),
        'LOW_CRISIS_THRESHOLD': float(os.getenv('LOW_CRISIS_THRESHOLD', '0.2')),
        
        # Rate Limiting
        'MAX_REQUESTS_PER_MINUTE': int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60')),
        'MAX_REQUESTS_PER_HOUR': int(os.getenv('MAX_REQUESTS_PER_HOUR', '1000')),
        
        # Security
        'ALLOWED_IPS': os.getenv('ALLOWED_IPS', '10.20.30.0/24,127.0.0.1,::1'),
        'ENABLE_CORS': os.getenv('ENABLE_CORS', 'true').lower() in ('true', '1', 'yes'),
    }
    
    return config

# Get configuration
config = get_env_config()

# Configure logging using environment variables
log_level = config['LOG_LEVEL']
log_file = config['LOG_FILE']
enable_debug = config['ENABLE_DEBUG_LOGGING']

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

# Set Hugging Face token if provided
if config['HUGGINGFACE_HUB_TOKEN']:
    os.environ['HUGGINGFACE_HUB_TOKEN'] = config['HUGGINGFACE_HUB_TOKEN']
    logger.info("🔑 Hugging Face token configured")

# Print configuration on startup if debug enabled
if enable_debug:
    logger.info("=== NLP Service Configuration ===")
    for key, value in sorted(config.items()):
        if 'TOKEN' in key and value:
            display_value = f"{str(value)[:8]}..."
        else:
            display_value = value
        logger.info(f"{key}: {display_value}")
    logger.info("=== End Configuration ===")

# Global components
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
        # Initialize enhanced model manager with configuration
        logger.info("🔧 Initializing Enhanced ModelManager...")
        
        # Initialize enhanced model manager (it will load config from environment automatically)
        model_manager = ModelManager()  # No config needed - loads from environment
        
        # Load models with the enhanced method
        logger.info("📦 Loading ML models with environment configuration...")
        await model_manager.load_models()
        logger.info("✅ Enhanced ModelManager initialized and models loaded")
        
        # Initialize enhanced learning manager if available
        if ENHANCED_LEARNING_AVAILABLE and config['ENABLE_LEARNING_SYSTEM']:
            try:
                enhanced_learning_manager = EnhancedLearningManager(model_manager)
                logger.info("✅ Enhanced learning system initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize Enhanced Learning Manager: {e}")
                enhanced_learning_manager = None
        else:
            if not ENHANCED_LEARNING_AVAILABLE:
                logger.info("ℹ️ Enhanced learning system not available")
            else:
                logger.info("ℹ️ Learning system disabled via configuration")
            enhanced_learning_manager = None
        
        # Initialize analyzers (only if available)
        if CRISIS_ANALYZER_AVAILABLE:
            try:
                crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager)
                logger.info("✅ Crisis analyzer initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CrisisAnalyzer: {e}")
                crisis_analyzer = None
        else:
            logger.info("ℹ️ CrisisAnalyzer not available")
        
        if PHRASE_EXTRACTOR_AVAILABLE:
            try:
                phrase_extractor = PhraseExtractor(model_manager)
                logger.info("✅ Phrase extractor initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize PhraseExtractor: {e}")
                phrase_extractor = None
        else:
            logger.info("ℹ️ PhraseExtractor not available")
        
        if PATTERN_LEARNER_AVAILABLE:
            try:
                pattern_learner = PatternLearner(model_manager)
                logger.info("✅ Pattern learner initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize PatternLearner: {e}")
                pattern_learner = None
        else:
            logger.info("ℹ️ PatternLearner not available")
        
        if SEMANTIC_ANALYZER_AVAILABLE:
            try:
                semantic_analyzer = SemanticAnalyzer(model_manager)
                logger.info("✅ Semantic analyzer initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize SemanticAnalyzer: {e}")
                semantic_analyzer = None
        else:
            logger.info("ℹ️ SemanticAnalyzer not available")
        
        logger.info("✅ All available components initialized with environment configuration")
        
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
if config['ENABLE_CORS']:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("🌐 CORS middleware enabled")

# Add enhanced learning endpoints after app creation
@app.on_event("startup")
async def setup_enhanced_learning_endpoints():
    if ENHANCED_LEARNING_AVAILABLE and enhanced_learning_manager:
        try:
            add_enhanced_learning_endpoints(app, enhanced_learning_manager)
            logger.info("🧠 Enhanced learning endpoints added to FastAPI app")
        except Exception as e:
            logger.warning(f"⚠️ Could not add enhanced learning endpoints: {e}")

# Basic analyze endpoint - works with just ModelManager
@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Basic message analysis using ModelManager directly if other analyzers aren't available"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    try:
        # Use CrisisAnalyzer if available, otherwise use ModelManager directly
        if crisis_analyzer:
            # Use the full crisis analyzer
            result = await crisis_analyzer.analyze_crisis(
                request.message, 
                request.user_id, 
                request.channel_id
            )
        else:
            # Fallback: Use ModelManager directly for basic analysis
            logger.info("Using basic ModelManager analysis (CrisisAnalyzer not available)")
            
            # Get depression analysis
            depression_result = model_manager.analyze_with_depression_model(request.message)
            sentiment_result = model_manager.analyze_with_sentiment_model(request.message)
            
            # Basic classification logic
            if depression_result and len(depression_result) > 0:
                # Get the highest confidence result
                top_result = max(depression_result, key=lambda x: x['score'])
                
                # Simple threshold mapping
                if top_result['label'] == 'severe' and top_result['score'] > config['HIGH_CRISIS_THRESHOLD']:
                    crisis_level = 'high'
                    needs_response = True
                elif top_result['label'] in ['moderate', 'severe'] and top_result['score'] > config['MEDIUM_CRISIS_THRESHOLD']:
                    crisis_level = 'medium'
                    needs_response = True
                elif top_result['score'] > config['LOW_CRISIS_THRESHOLD']:
                    crisis_level = 'low'
                    needs_response = True
                else:
                    crisis_level = 'none'
                    needs_response = False
                
                confidence_score = top_result['score']
                detected_categories = [top_result['label']]
                reasoning = f"Depression model: {top_result['label']} ({confidence_score:.3f})"
                
                if sentiment_result:
                    sentiment_top = max(sentiment_result, key=lambda x: x['score'])
                    reasoning += f" | Sentiment: {sentiment_top['label']} ({sentiment_top['score']:.3f})"
            else:
                # No results from model
                needs_response = False
                crisis_level = 'none'
                confidence_score = 0.0
                detected_categories = []
                reasoning = "No significant crisis indicators detected"
            
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                'needs_response': needs_response,
                'crisis_level': crisis_level,
                'confidence_score': confidence_score,
                'detected_categories': detected_categories,
                'method': 'basic_model_manager_fallback',
                'processing_time_ms': processing_time,
                'model_info': 'depression+sentiment(basic)',
                'reasoning': reasoning
            }
        
        logger.info(f"Analysis complete: {result['crisis_level']} confidence={result['confidence_score']:.3f} time={result['processing_time_ms']:.1f}ms")
        return CrisisResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in message analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Optional endpoints that only work if components are available
@app.post("/extract_phrases")
async def extract_phrases_endpoint(request: PhraseExtractionRequest):
    """Extract crisis phrases from message"""
    
    if not phrase_extractor:
        raise HTTPException(status_code=503, detail="Phrase extraction not available")
    
    try:
        result = await phrase_extractor.extract_crisis_phrases(
            request.message,
            request.user_id,
            request.channel_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in phrase extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Phrase extraction failed: {str(e)}")

@app.post("/learn_patterns")
async def learn_patterns_endpoint(request: PatternLearningRequest):
    """Learn patterns from message history"""
    
    if not pattern_learner:
        raise HTTPException(status_code=503, detail="Pattern learning not available")
    
    try:
        result = await pattern_learner.learn_patterns(
            request.messages,
            request.analysis_type,
            request.time_window_days
        )
        return result
    except Exception as e:
        logger.error(f"Error in pattern learning: {e}")
        raise HTTPException(status_code=500, detail=f"Pattern learning failed: {str(e)}")

@app.post("/semantic_analysis")
async def semantic_analysis_endpoint(request: SemanticAnalysisRequest):
    """Perform semantic analysis for crisis detection"""
    
    if not semantic_analyzer:
        raise HTTPException(status_code=503, detail="Semantic analysis not available")
    
    try:
        result = await semantic_analyzer.analyze_semantic_context(
            request.message,
            request.community_vocabulary,
            request.context_hints
        )
        return result
    except Exception as e:
        logger.error(f"Error in semantic analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Semantic analysis failed: {str(e)}")

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with component status"""
    
    uptime = time.time() - startup_time
    models_loaded = model_manager and model_manager.models_loaded()
    
    # Check component availability
    components_status = {
        "model_manager": model_manager is not None,
        "crisis_analyzer": crisis_analyzer is not None,
        "phrase_extractor": phrase_extractor is not None,
        "pattern_learner": pattern_learner is not None,
        "semantic_analyzer": semantic_analyzer is not None,
        "enhanced_learning": enhanced_learning_manager is not None
    }
    
    status = "healthy" if models_loaded else "unhealthy"
    
    return HealthResponse(
        status=status,
        model_loaded=models_loaded,
        uptime_seconds=uptime,
        hardware_info={
            "device": config['DEVICE'],
            "precision": config['MODEL_PRECISION'],
            "max_batch_size": config['MAX_BATCH_SIZE'],
            "inference_threads": config['INFERENCE_THREADS'],
            "components_available": components_status,
            "learning_system": "enabled" if enhanced_learning_manager else "disabled"
        }
    )

# Stats endpoint
@app.get("/stats")
async def get_stats():
    """Get service statistics with configuration info"""
    
    uptime = time.time() - startup_time
    
    stats = {
        "service": "Enhanced Ash NLP Service with Environment Configuration",
        "version": "4.3",
        "uptime_seconds": uptime,
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "configuration": {
            "learning_enabled": config['ENABLE_LEARNING_SYSTEM'],
            "device": config['DEVICE'],
            "precision": config['MODEL_PRECISION'],
            "thresholds": {
                "high": config['HIGH_CRISIS_THRESHOLD'],
                "medium": config['MEDIUM_CRISIS_THRESHOLD'],
                "low": config['LOW_CRISIS_THRESHOLD']
            }
        },
        "components_available": {
            "model_manager": model_manager is not None,
            "crisis_analyzer": CRISIS_ANALYZER_AVAILABLE and crisis_analyzer is not None,
            "phrase_extractor": PHRASE_EXTRACTOR_AVAILABLE and phrase_extractor is not None,
            "pattern_learner": PATTERN_LEARNER_AVAILABLE and pattern_learner is not None,
            "semantic_analyzer": SEMANTIC_ANALYZER_AVAILABLE and semantic_analyzer is not None,
            "enhanced_learning": ENHANCED_LEARNING_AVAILABLE and enhanced_learning_manager is not None
        },
        "hardware_config": {
            "max_batch_size": config['MAX_BATCH_SIZE'],
            "inference_threads": config['INFERENCE_THREADS'],
            "max_concurrent_requests": config['MAX_CONCURRENT_REQUESTS'],
            "request_timeout": config['REQUEST_TIMEOUT']
        }
    }
    
    return stats

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v4.3 (Full Environment Support)")
    logger.info("🔧 Configuration loaded from environment variables")
    logger.info("🧠 Advanced capabilities with environment-driven configuration")
    
    # Get server configuration from environment
    host = config['NLP_SERVICE_HOST']
    port = config['NLP_SERVICE_PORT']
    workers = config['UVICORN_WORKERS']
    reload = config['RELOAD_ON_CHANGES']
    
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