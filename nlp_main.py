#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - Modular Version
Multi-model approach with keyword discovery capabilities
Version: 4.1 - Modular Architecture
"""

from fastapi import FastAPI, HTTPException
import logging
import time
import uvicorn
from contextlib import asynccontextmanager

# Import our modular components
from models.pydantic_models import (
    MessageRequest, CrisisResponse, HealthResponse,
    PhraseExtractionRequest, PatternLearningRequest, SemanticAnalysisRequest
)
from models.ml_models import ModelManager
from analysis.crisis_analyzer import CrisisAnalyzer
from analysis.phrase_extractor import PhraseExtractor
from analysis.pattern_learner import PatternLearner
from analysis.semantic_analyzer import SemanticAnalyzer
from config.nlp_settings import SERVER_CONFIG
from utils.learning_endpoints import LearningManager, add_learning_endpoints

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nlp_service.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global components
model_manager = None
crisis_analyzer = None
phrase_extractor = None
pattern_learner = None
semantic_analyzer = None
learning_manager = None
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting up...")
    await initialize_components()
    logger.info("✅ Enhanced FastAPI app startup complete!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

async def initialize_components():
    global model_manager, crisis_analyzer, phrase_extractor, pattern_learner, semantic_analyzer, learning_manager
    
    try:
        # Initialize model manager and load models
        model_manager = ModelManager()
        await model_manager.load_models()
        
        # Initialize learning manager first
        learning_manager = LearningManager(model_manager)
        
        # Initialize analyzers with the loaded models AND learning manager
        crisis_analyzer = CrisisAnalyzer(model_manager, learning_manager)  # Pass learning_manager
        phrase_extractor = PhraseExtractor(model_manager)
        pattern_learner = PatternLearner(model_manager)
        semantic_analyzer = SemanticAnalyzer(model_manager)
        
        # Add learning endpoints to the app
        add_learning_endpoints(app, learning_manager)
        
        logger.info("✅ All components initialized successfully including learning system")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise

app = FastAPI(
    title="Enhanced Ash NLP Service", 
    version="4.1",
    description="Modular Multi-model Mental Health Crisis Detection with Keyword Discovery",
    lifespan=lifespan
)

# Initialize learning endpoints after app creation
@app.on_event("startup")
async def setup_learning_endpoints():
    if learning_manager:
        add_learning_endpoints(app, learning_manager)
        logger.info("🧠 Learning endpoints added to FastAPI app")

# EXISTING ENDPOINT - Keep your original crisis analysis
@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Enhanced message analysis with multi-model approach"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    
    try:
        # Use the crisis analyzer component
        result = await crisis_analyzer.analyze_message(
            request.message, 
            request.user_id, 
            request.channel_id
        )
        
        return CrisisResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")

# NEW ENDPOINT - Phrase extraction for keyword discovery
@app.post("/extract_phrases")
async def extract_crisis_phrases(request: PhraseExtractionRequest):
    """Extract potential crisis keywords/phrases using your existing models"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if not request.message.strip():
        return {'phrases': [], 'processing_time_ms': 0}
    
    try:
        result = await phrase_extractor.extract_phrases(
            request.message,
            request.user_id,
            request.channel_id,
            request.parameters
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in phrase extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Phrase extraction failed: {str(e)}")

# NEW ENDPOINT - Pattern learning from community messages
@app.post("/learn_patterns")
async def learn_community_patterns(request: PatternLearningRequest):
    """Learn crisis communication patterns from community message history"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
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

# NEW ENDPOINT - Enhanced semantic analysis
@app.post("/semantic_analysis")
async def semantic_crisis_analysis(request: SemanticAnalysisRequest):
    """Perform semantic analysis for crisis detection with community context"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
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

# EXISTING ENDPOINTS - Keep your health check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check"""
    
    uptime = time.time() - startup_time
    
    return HealthResponse(
        status="healthy" if (model_manager and model_manager.models_loaded()) else "unhealthy",
        model_loaded=model_manager.models_loaded() if model_manager else False,
        uptime_seconds=uptime,
        hardware_info=SERVER_CONFIG["hardware_info"]
    )

@app.get("/stats")
async def get_enhanced_stats():
    """Get enhanced service statistics"""
    
    uptime = time.time() - startup_time
    
    return {
        "service": "Enhanced Ash NLP Service",
        "version": "4.1",
        "architecture": "modular",
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "uptime_seconds": uptime,
        "components": {
            "crisis_analyzer": "Original depression + sentiment analysis",
            "phrase_extractor": "Extract crisis keywords using model scoring", 
            "pattern_learner": "Learn patterns from community messages",
            "semantic_analyzer": "Enhanced semantic analysis with community context"
        },
        "capabilities": SERVER_CONFIG["capabilities"],
        "performance_targets": SERVER_CONFIG["performance_targets"]
    }

@app.get("/enhanced_stats")
async def get_comprehensive_stats():
    """Get comprehensive statistics for bot integration"""
    
    uptime = time.time() - startup_time
    
    base_stats = {
        "service": "Enhanced Ash NLP Service with Keyword Discovery",
        "version": "4.1",
        "architecture": "modular",
        "uptime_seconds": uptime,
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "cost_optimization": SERVER_CONFIG["cost_optimization"],
        "bot_integration": SERVER_CONFIG["bot_integration"]
    }
    
    # Add component-specific stats if available
    if phrase_extractor:
        base_stats["phrase_extraction_ready"] = True
    if pattern_learner:
        base_stats["pattern_learning_ready"] = True
    if semantic_analyzer:
        base_stats["semantic_analysis_ready"] = True
    
    return base_stats

@app.get("/")
async def enhanced_root():
    """Enhanced service info with modular architecture"""
    return {
        "service": "Enhanced Ash NLP Mental Health Crisis Detection + Keyword Discovery",
        "version": "4.1",
        "architecture": "modular", 
        "status": "running",
        "description": "Modular multi-model approach with keyword discovery and community pattern learning",
        "components": [
            "🧠 Crisis Analyzer - Original depression + sentiment analysis",
            "🔍 Phrase Extractor - Keyword discovery using model scoring",
            "📚 Pattern Learner - Community pattern learning",
            "🎯 Semantic Analyzer - Enhanced context analysis",
            "⚡ Model Manager - Efficient model loading and management"
        ],
        "benefits": [
            "Modular architecture for better maintainability",
            "Cost-optimized to minimize external API usage", 
            "Leverages your existing AI hardware investment",
            "Provides keyword suggestions to bot's Crisis Response team",
            "Adapts to LGBTQIA+ specific crisis communication"
        ],
        "endpoints": {
            "analyze": "POST /analyze - Original crisis detection",
            "extract_phrases": "POST /extract_phrases - Extract keyword candidates",
            "learn_patterns": "POST /learn_patterns - Learn from message history",
            "semantic_analysis": "POST /semantic_analysis - Enhanced semantic detection",
            "health": "GET /health - System health check",
            "stats": "GET /stats - Service statistics",
            "enhanced_stats": "GET /enhanced_stats - Comprehensive bot integration stats"
        }
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v4.1 (Modular)")
    logger.info("🏗️ Architecture: Modular components for better maintainability")
    logger.info("🧠 Enhanced capabilities: Crisis analysis + Keyword discovery + Pattern learning")
    logger.info("🤝 Designed for cost-optimized bot integration")
    logger.info("🌐 Starting server on 0.0.0.0:8881")
    
    try:
        uvicorn.run(
            "nlp_main:app",
            host="0.0.0.0",
            port=8881,
            log_level="info",
            reload=False,
            workers=1
        )
    except Exception as e:
        logger.error(f"❌ Failed to start enhanced server: {e}")
        raise