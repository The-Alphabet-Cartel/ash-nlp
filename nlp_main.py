#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot - With False Positive & Negative Learning
UPDATE: ash-nlp/nlp_main.py - Replace the initialization and endpoint sections
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

# Import enhanced learning system
from utils.enhanced_learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints

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
enhanced_learning_manager = None  # NEW: Enhanced learning manager
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting up with advanced learning...")
    await initialize_enhanced_components()
    logger.info("✅ Enhanced FastAPI app startup complete with learning system!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

async def initialize_enhanced_components():
    global model_manager, crisis_analyzer, phrase_extractor, pattern_learner, semantic_analyzer, enhanced_learning_manager
    
    try:
        # Initialize model manager and load models
        model_manager = ModelManager()
        await model_manager.load_models()
        
        # Initialize ENHANCED learning manager first
        enhanced_learning_manager = EnhancedLearningManager(model_manager)
        
        # Initialize analyzers with the loaded models AND enhanced learning manager
        crisis_analyzer = CrisisAnalyzer(model_manager, enhanced_learning_manager)  # Pass enhanced learning manager
        phrase_extractor = PhraseExtractor(model_manager)
        pattern_learner = PatternLearner(model_manager)
        semantic_analyzer = SemanticAnalyzer(model_manager)
        
        # Add enhanced learning endpoints to the app (will be done after app creation)
        logger.info("✅ All components initialized successfully including ENHANCED learning system")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize enhanced components: {e}")
        raise

app = FastAPI(
    title="Enhanced Ash NLP Service with Advanced Learning", 
    version="4.2",
    description="Multi-model Mental Health Crisis Detection with False Positive & Negative Learning",
    lifespan=lifespan
)

# Initialize enhanced learning endpoints after app creation
@app.on_event("startup")
async def setup_enhanced_learning_endpoints():
    if enhanced_learning_manager:
        add_enhanced_learning_endpoints(app, enhanced_learning_manager)
        logger.info("🧠 Enhanced learning endpoints added to FastAPI app (false positives + negatives)")

# EXISTING ENDPOINT - Enhanced with learning
@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Enhanced message analysis with learning-adjusted scoring"""
    
    if not model_manager or not model_manager.models_loaded():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    
    try:
        # Use the crisis analyzer component (now with enhanced learning)
        result = await crisis_analyzer.analyze_message(
            request.message, 
            request.user_id, 
            request.channel_id
        )
        
        return CrisisResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")

# EXISTING ENDPOINTS - Keep phrase extraction, pattern learning, semantic analysis
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

# EXISTING ENDPOINTS - Keep health check and stats
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check with learning system status"""
    
    uptime = time.time() - startup_time
    
    # Check learning system health
    learning_healthy = enhanced_learning_manager is not None
    
    return HealthResponse(
        status="healthy" if (model_manager and model_manager.models_loaded() and learning_healthy) else "unhealthy",
        model_loaded=model_manager.models_loaded() if model_manager else False,
        uptime_seconds=uptime,
        hardware_info={
            **SERVER_CONFIG["hardware_info"],
            "learning_system": "Enhanced (False Positives + Negatives)" if learning_healthy else "Disabled"
        }
    )

@app.get("/stats")
async def get_enhanced_stats():
    """Get enhanced service statistics with learning system info"""
    
    uptime = time.time() - startup_time
    
    base_stats = {
        "service": "Enhanced Ash NLP Service with Advanced Learning",
        "version": "4.2",
        "architecture": "modular with enhanced learning",
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "uptime_seconds": uptime,
        "components": {
            "crisis_analyzer": "Depression + sentiment analysis with learning adjustments",
            "phrase_extractor": "Extract crisis keywords using model scoring", 
            "pattern_learner": "Learn patterns from community messages",
            "semantic_analyzer": "Enhanced semantic analysis with community context",
            "enhanced_learning_manager": "False positive & negative learning system"
        },
        "capabilities": {
            **SERVER_CONFIG["capabilities"],
            "false_positive_learning": "Reduces over-detection sensitivity",
            "false_negative_learning": "Increases under-detection sensitivity",
            "adaptive_scoring": "Learns from both types of detection errors"
        },
        "performance_targets": SERVER_CONFIG["performance_targets"]
    }
    
    # Add learning system stats if available
    if enhanced_learning_manager:
        try:
            learning_stats = enhanced_learning_manager.get_learning_statistics()
            base_stats["learning_system"] = learning_stats
        except Exception as e:
            logger.error(f"Error getting learning stats: {e}")
            base_stats["learning_system"] = {"error": "Statistics unavailable"}
    
    return base_stats

@app.get("/enhanced_stats")
async def get_comprehensive_stats():
    """Get comprehensive statistics for bot integration with learning metrics"""
    
    uptime = time.time() - startup_time
    
    base_stats = {
        "service": "Enhanced Ash NLP Service with False Positive & Negative Learning",
        "version": "4.2",
        "architecture": "modular with adaptive learning",
        "uptime_seconds": uptime,
        "models_loaded": model_manager.get_model_status() if model_manager else {},
        "cost_optimization": {
            **SERVER_CONFIG["cost_optimization"],
            "learning_efficiency": "Reduces both over-detection and under-detection errors"
        },
        "bot_integration": {
            **SERVER_CONFIG["bot_integration"],
            "false_positive_learning": "Bot reports via /report_false_positive command",
            "false_negative_learning": "Bot reports via /report_missed_crisis command",
            "adaptive_scoring": "Real-time score adjustments based on community feedback"
        }
    }
    
    # Add component readiness status
    if phrase_extractor:
        base_stats["phrase_extraction_ready"] = True
    if pattern_learner:
        base_stats["pattern_learning_ready"] = True
    if semantic_analyzer:
        base_stats["semantic_analysis_ready"] = True
    if enhanced_learning_manager:
        base_stats["enhanced_learning_ready"] = True
        
        # Add learning system metrics
        try:
            learning_stats = enhanced_learning_manager.get_learning_statistics()
            base_stats["learning_metrics"] = learning_stats
        except Exception as e:
            base_stats["learning_metrics"] = {"error": str(e)}
    
    return base_stats

@app.get("/")
async def enhanced_root():
    """Enhanced service info with advanced learning capabilities"""
    return {
        "service": "Enhanced Ash NLP Mental Health Crisis Detection with Advanced Learning",
        "version": "4.2",
        "architecture": "modular with adaptive learning", 
        "status": "running",
        "description": "Multi-model approach with false positive & negative learning from community feedback",
        "components": [
            "🧠 Crisis Analyzer - Depression + sentiment analysis with learning adjustments",
            "🔍 Phrase Extractor - Keyword discovery using model scoring",
            "📚 Pattern Learner - Community pattern learning",
            "🎯 Semantic Analyzer - Enhanced context analysis",
            "⚡ Model Manager - Efficient model loading and management",
            "🎓 Enhanced Learning Manager - False positive & negative learning system"
        ],
        "learning_capabilities": [
            "🚨 False Positive Learning - Reduces over-sensitive detection",
            "🎯 False Negative Learning - Improves missed crisis detection", 
            "📊 Adaptive Scoring - Real-time sensitivity adjustments",
            "📈 Community Feedback Integration - Learns from Crisis Response team",
            "🔄 Continuous Improvement - Gets better with each report"
        ],
        "benefits": [
            "Modular architecture for better maintainability",
            "Cost-optimized to minimize external API usage", 
            "Leverages your existing AI hardware investment",
            "Provides keyword suggestions to bot's Crisis Response team",
            "Adapts to LGBTQIA+ specific crisis communication",
            "Self-improving system that learns from mistakes"
        ],
        "endpoints": {
            "analyze": "POST /analyze - Crisis detection with learning adjustments",
            "extract_phrases": "POST /extract_phrases - Extract keyword candidates",
            "learn_patterns": "POST /learn_patterns - Learn from message history",
            "semantic_analysis": "POST /semantic_analysis - Enhanced semantic detection",
            "analyze_false_positive": "POST /analyze_false_positive - Learn from over-detection",
            "analyze_false_negative": "POST /analyze_false_negative - Learn from missed crises",
            "update_learning_model": "POST /update_learning_model - Update learning system",
            "learning_statistics": "GET /learning_statistics - Learning system metrics",
            "health": "GET /health - System health check",
            "stats": "GET /stats - Service statistics",
            "enhanced_stats": "GET /enhanced_stats - Comprehensive bot integration stats"
        }
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v4.2 (Advanced Learning)")
    logger.info("🏗️ Architecture: Modular components with false positive & negative learning")
    logger.info("🧠 Advanced capabilities: Crisis analysis + Keyword discovery + Pattern learning + Adaptive scoring")
    logger.info("🎓 Learning system: Reduces both over-detection and under-detection errors")
    logger.info("🤝 Designed for cost-optimized bot integration with community feedback")
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