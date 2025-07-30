#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - With Secrets Support
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

# Sentinment Adjustments
from utils.context_helpers import analyze_sentiment_context
from utils.scoring_helpers import (
    extract_depression_score,
    enhanced_depression_analysis,
    apply_comprehensive_false_positive_reduction
)

from endpoints.ensemble_endpoints import add_ensemble_endpoints

# Initialize configuration manager with secrets support
config_manager = get_nlp_config()
config = get_env_config()  # Backward compatibility - returns dict

# Configure logging using environment variables
log_level = config['GLOBAL_LOG_LEVEL']
log_file = config['NLP_LOG_FILE']
enable_debug = config['GLOBAL_ENABLE_DEBUG_MODE']

# Set GLOBAL_PYTHONUNBUFFERED for Docker
os.environ['GLOBAL_PYTHONUNBUFFERED'] = '1'

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

try:
    from analysis.pattern_learner import PatternLearner
    PATTERN_LEARNER_AVAILABLE = True
    logger.info("✅ PatternLearner import successful")
except ImportError as e:
    PATTERN_LEARNER_AVAILABLE = False
    logger.warning(f"⚠️ PatternLearner import failed: {e}")

try:
    from analysis.semantic_analyzer import SemanticAnalyzer
    SEMANTIC_ANALYZER_AVAILABLE = True
    logger.info("✅ SemanticAnalyzer import successful")
except ImportError as e:
    SEMANTIC_ANALYZER_AVAILABLE = False
    logger.warning(f"⚠️ SemanticAnalyzer import failed: {e}")

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
    logger.info("🚀 Enhanced FastAPI app starting with secrets-aware configuration...")
    await initialize_components_with_config()
    logger.info("✅ Enhanced FastAPI app startup complete!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

async def initialize_components_with_config():
    global model_manager, crisis_analyzer, phrase_extractor, pattern_learner, semantic_analyzer, enhanced_learning_manager
    
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
        logger.info("📦 Loading ML models with secrets-aware configuration...")
        await model_manager.load_models()
        logger.info("✅ Enhanced ModelManager initialized and models loaded")
        
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
        
        if PATTERN_LEARNER_AVAILABLE:
            try:
                # Try to pass config manager if PatternLearner supports it
                try:
                    pattern_learner = PatternLearner(model_manager, config_manager)
                    logger.info("✅ Pattern learner initialized with secrets support")
                except TypeError:
                    # Fallback: PatternLearner doesn't support config parameter yet
                    pattern_learner = PatternLearner(model_manager)
                    logger.info("✅ Pattern learner initialized (using environment variables)")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize PatternLearner: {e}")
                pattern_learner = None
        else:
            logger.info("ℹ️ PatternLearner not available")
        
        if SEMANTIC_ANALYZER_AVAILABLE:
            try:
                # Try to pass config manager if SemanticAnalyzer supports it
                try:
                    semantic_analyzer = SemanticAnalyzer(model_manager, config_manager)
                    logger.info("✅ Semantic analyzer initialized with secrets support")
                except TypeError:
                    # Fallback: SemanticAnalyzer doesn't support config parameter yet
                    semantic_analyzer = SemanticAnalyzer(model_manager)
                    logger.info("✅ Semantic analyzer initialized (using environment variables)")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize SemanticAnalyzer: {e}")
                semantic_analyzer = None
        else:
            logger.info("ℹ️ SemanticAnalyzer not available")

        # Add enhanced learning endpoints if manager is available
        if enhanced_learning_manager:
            try:
                logger.info("🔧 Adding enhanced learning endpoints...")
                add_enhanced_learning_endpoints(app, enhanced_learning_manager)
                logger.info("🧠 Enhanced learning endpoints added to FastAPI app!")
            except Exception as e:
                logger.error(f"❌ Failed to add enhanced learning endpoints: {e}")
                logger.exception("Full traceback:")

        # Add ensemble endpoints if model manager is available
        if model_manager:
            try:
                logger.info("🔧 Adding ensemble endpoints...")
                add_ensemble_endpoints(app, model_manager)
                logger.info("🎯 Ensemble endpoints added to FastAPI app!")
            except Exception as e:
                logger.error(f"❌ Failed to add ensemble endpoints: {e}")
                logger.exception("Full traceback:")

        logger.info("✅ All available components initialized with secrets-aware configuration")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise

# Create FastAPI app with enhanced config
app = FastAPI(
    title="Enhanced Ash NLP Service with Secrets Support", 
    version="4.4",
    description="Multi-model Mental Health Crisis Detection with Secure Configuration Management",
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

def extract_sentiment_scores_from_result(sentiment_result) -> dict:
    """Extract sentiment scores in the format ash-bot expects"""
    
    sentiment_scores = {'negative': 0.0, 'positive': 0.0, 'neutral': 0.0}
    
    if not sentiment_result:
        return sentiment_scores
    
    # Handle different sentiment result formats
    if isinstance(sentiment_result, list) and len(sentiment_result) > 0:
        for item in sentiment_result:
            if isinstance(item, dict):
                label = item.get('label', '').lower()
                score = item.get('score', 0.0)
                
                # Map sentiment labels to our expected format
                if 'negative' in label or 'sadness' in label or 'anger' in label:
                    sentiment_scores['negative'] = max(sentiment_scores['negative'], score)
                elif 'positive' in label or 'joy' in label or 'optimism' in label:
                    sentiment_scores['positive'] = max(sentiment_scores['positive'], score)
                elif 'neutral' in label:
                    sentiment_scores['neutral'] = max(sentiment_scores['neutral'], score)
    
    return sentiment_scores

@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Message analysis using available analyzers"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    try:
        # Use CrisisAnalyzer if available
        if crisis_analyzer:
            result = await crisis_analyzer.analyze_message(
                request.message, 
                request.user_id, 
                request.channel_id
            )
        else:
            # UPDATED FALLBACK: Include sentiment data
            depression_result = model_manager.analyze_with_depression_model(request.message)
            sentiment_result = model_manager.analyze_with_sentiment_model(request.message)
            
            # Extract sentiment scores properly
            sentiment_scores = extract_sentiment_scores_from_result(sentiment_result)
            
            if depression_result and len(depression_result) > 0:
                top_result = max(depression_result, key=lambda x: x['score'])
                
                # Apply false positive reduction
                original_score = top_result['score']
                adjusted_score = apply_comprehensive_false_positive_reduction(request.message, original_score)
                
                # Determine crisis level
                if top_result['label'] == 'severe' and adjusted_score > config['NLP_HIGH_CRISIS_THRESHOLD']:
                    crisis_level = 'high'
                    needs_response = True
                elif top_result['label'] in ['moderate', 'severe'] and adjusted_score > config['NLP_MEDIUM_CRISIS_THRESHOLD']:
                    crisis_level = 'medium'
                    needs_response = True
                elif adjusted_score > config['NLP_LOW_CRISIS_THRESHOLD']:
                    crisis_level = 'low'
                    needs_response = True
                else:
                    crisis_level = 'none'
                    needs_response = False
                
                confidence_score = adjusted_score
                detected_categories = [top_result['label']]
                reasoning = f"Basic model: {top_result['label']} (original: {original_score:.3f}, adjusted: {adjusted_score:.3f})"
                
                # BUILD RESPONSE WITH SENTIMENT DATA
                result = {
                    'needs_response': needs_response,
                    'crisis_level': crisis_level,
                    'confidence_score': confidence_score,
                    'detected_categories': detected_categories,
                    'method': 'basic_model_manager_with_sentiment',
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'model_info': 'depression+sentiment(basic)+false_positive_reduction',
                    'reasoning': reasoning,
                    'analysis': {  # ← ADD THIS SECTION
                        'depression_score': original_score,
                        'sentiment_scores': sentiment_scores,  # ← KEY ADDITION
                        'confidence_adjustment': adjusted_score - original_score,
                        'crisis_indicators': [top_result['label']]
                    }
                }
            else:
                # No results case
                result = {
                    'needs_response': False,
                    'crisis_level': 'none',
                    'confidence_score': 0.0,
                    'detected_categories': [],
                    'method': 'no_detection',
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'model_info': 'no_significant_indicators',
                    'reasoning': "No significant crisis indicators detected",
                    'analysis': {  # ← ADD THIS SECTION EVEN FOR NO DETECTION
                        'depression_score': 0.0,
                        'sentiment_scores': sentiment_scores,  # ← STILL INCLUDE SENTIMENT
                        'crisis_indicators': []
                    }
                }
        
        # Return the result
        if isinstance(result, dict):
            return CrisisResponse(**result)
        else:
            return result
            
    except Exception as e:
        logger.error(f"Error in message analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

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
        "pattern_learner": pattern_learner is not None,
        "semantic_analyzer": semantic_analyzer is not None,
        "enhanced_learning": enhanced_learning_manager is not None
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
            "learning_system": "enabled" if enhanced_learning_manager else "disabled",
            "secrets_status": api_keys_status,
            "using_secrets": any(api_keys_status.values())
        }
    )

# Stats endpoint
@app.get("/stats")
async def get_stats():
    """Get service statistics with configuration and secrets info"""
    
    uptime = time.time() - startup_time
    api_keys_status = get_api_keys_status()
    
    stats = {
        "service": "Enhanced Ash NLP Service with Secrets Support",
        "version": "4.4",
        "uptime_seconds": uptime,
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "configuration": {
            "learning_enabled": config['GLOBAL_ENABLE_LEARNING_SYSTEM'],
            "device": config['NLP_DEVICE'],
            "precision": config['NLP_MODEL_PRECISION'],
            "using_secrets": any(api_keys_status.values()),
            "thresholds": {
                "high": config['NLP_HIGH_CRISIS_THRESHOLD'],
                "medium": config['NLP_MEDIUM_CRISIS_THRESHOLD'],
                "low": config['NLP_LOW_CRISIS_THRESHOLD']
            }
        },
        "secrets_status": api_keys_status,
        "components_available": {
            "model_manager": model_manager is not None,
            "crisis_analyzer": CRISIS_ANALYZER_AVAILABLE and crisis_analyzer is not None,
            "phrase_extractor": PHRASE_EXTRACTOR_AVAILABLE and phrase_extractor is not None,
            "pattern_learner": PATTERN_LEARNER_AVAILABLE and pattern_learner is not None,
            "semantic_analyzer": SEMANTIC_ANALYZER_AVAILABLE and semantic_analyzer is not None,
            "enhanced_learning": ENHANCED_LEARNING_AVAILABLE and enhanced_learning_manager is not None
        },
        "hardware_config": {
            "max_batch_size": config['NLP_MAX_BATCH_SIZE'],
            "inference_threads": config['NLP_INFERENCE_THREADS'],
            "max_concurrent_requests": config['NLP_MAX_CONCURRENT_REQUESTS'],
            "request_timeout": config['NLP_REQUEST_TIMEOUT']
        }
    }
    
    return stats

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v4.4 (Secrets Support)")
    logger.info("🔧 Configuration loaded with secrets-aware management")
    logger.info("🧠 Advanced capabilities with secure configuration")
    
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