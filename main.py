#!/usr/bin/env python3
"""
Standalone NLP Service for Ash Bot
Runs Mental Health RoBERTa model for crisis detection
Designed to run on separate AI rig hardware
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from transformers import pipeline
import logging
import time
import os
import uvicorn
from typing import Optional
from contextlib import asynccontextmanager

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nlp_service.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global model storage
nlp_model = None

class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = "unknown"
    channel_id: Optional[str] = "unknown"

class CrisisResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    needs_response: bool
    crisis_level: str  # 'none', 'low', 'medium', 'high'
    confidence_score: float
    detected_categories: list
    method: str
    processing_time_ms: float
    model_info: str

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    model_loaded: bool
    uptime_seconds: float
    hardware_info: dict

# Service startup time
startup_time = time.time()

async def load_model():
    """Load the Mental Health RoBERTa model on startup"""
    global nlp_model
    
    logger.info("=" * 50)
    logger.info("STARTING MODEL LOADING PROCESS")
    logger.info("=" * 50)
    logger.info("Loading Mental Health RoBERTa model...")
    logger.info("Hardware: Ryzen 7 7700x + RTX 3050 + 64GB RAM")
    
    try:
        # Use proper depression severity assessment model
        model_id = "rafalposwiata/deproberta-large-depression"
        
        logger.info(f"Loading model: {model_id}")
        logger.info("This may take several minutes for first-time download...")
        
        nlp_model = pipeline(
            "text-classification",
            model=model_id,
            device=-1,  # Force CPU inference (RTX 3050 has limited VRAM)
            top_k=None  # Return all scores for analysis
        )
        
        logger.info("✅ Mental Health RoBERTa model loaded successfully!")
        
        # Test inference to verify everything works
        test_result = nlp_model("I feel sad today")
        logger.info(f"✅ Model test successful")
        logger.info(f"Test result type: {type(test_result)}")
        logger.info(f"Test result content: {test_result}")
        
        # Extract the actual predictions from nested structure
        if isinstance(test_result, list) and len(test_result) > 0:
            if isinstance(test_result[0], list):
                # Nested list format: [[{'label': 'LABEL_0', 'score': 0.6}, {'label': 'LABEL_1', 'score': 0.4}]]
                predictions = test_result[0]
                logger.info(f"✅ Found nested list format with {len(predictions)} labels")
                logger.info(f"Available labels: {[pred['label'] for pred in predictions]}")
            elif isinstance(test_result[0], dict):
                # Direct list format: [{'label': 'LABEL_0', 'score': 0.6}, {'label': 'LABEL_1', 'score': 0.4}]
                predictions = test_result
                logger.info(f"✅ Found direct list format with {len(predictions)} labels")
                logger.info(f"Available labels: {[pred['label'] for pred in predictions]}")
            else:
                logger.info(f"Unexpected nested structure: {test_result}")
        else:
            logger.info(f"Unexpected result format: {test_result}")
        
        # Log model info
        logger.info("✅ Model ready for crisis detection")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Failed to load NLP model: {e}")
        logger.exception("Full traceback:")
        nlp_model = None
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 FastAPI app starting up...")
    await load_model()
    logger.info("✅ FastAPI app startup complete!")
    yield
    # Shutdown (if needed)
    logger.info("🛑 FastAPI app shutting down...")

app = FastAPI(
    title="Ash NLP Service (Standalone)", 
    version="2.0",
    description="Mental Health Crisis Detection Service for Ash Bot",
    lifespan=lifespan
)

def analyze_mental_health_prediction(prediction_result):
    """IMPROVED scoring mathematics to boost HIGH crisis detection"""
    
    max_crisis_score = 0.0
    detected_categories = []
    
    if not prediction_result:
        return max_crisis_score, detected_categories
    
    # Extract predictions
    predictions_to_process = []
    
    if isinstance(prediction_result, list):
        if len(prediction_result) > 0 and isinstance(prediction_result[0], list):
            predictions_to_process = prediction_result[0]
        elif len(prediction_result) > 0 and isinstance(prediction_result[0], dict):
            predictions_to_process = prediction_result
        else:
            logger.warning(f"Unexpected list format: {prediction_result}")
            return max_crisis_score, detected_categories
    elif isinstance(prediction_result, dict):
        predictions_to_process = [prediction_result]
    else:
        logger.warning(f"Unexpected prediction format: {type(prediction_result)}")
        return max_crisis_score, detected_categories
    
    # Extract the three depression scores
    not_depression_score = 0.0
    moderate_score = 0.0
    severe_score = 0.0
    
    for prediction in predictions_to_process:
        if not isinstance(prediction, dict):
            continue
            
        label = str(prediction.get('label', '')).lower().strip()
        score = float(prediction.get('score', 0.0))
        
        if label == 'not depression':
            not_depression_score = score
        elif label == 'moderate':
            moderate_score = score
        elif label == 'severe':
            severe_score = score
        
        detected_categories.append({
            'category': label,
            'raw_score': score,
            'confidence': score,
            'original_label': prediction.get('label', 'unknown'),
            'is_crisis': label in ['moderate', 'severe']
        })
    
    logger.info(f"Raw ML scores - Not: {not_depression_score:.4f}, Moderate: {moderate_score:.4f}, Severe: {severe_score:.4f}")
    
    # ENHANCED SCORING MATHEMATICS
    # The key insight: we need to AMPLIFY depression signals more aggressively
    
    # Calculate total depression evidence
    total_depression = moderate_score + severe_score
    
    # Calculate how decisive the model is (confidence in top prediction)
    all_scores = [not_depression_score, moderate_score, severe_score]
    max_prediction = max(all_scores)
    prediction_strength = max_prediction - (1.0 - max_prediction) / 2  # Boost strong predictions
    
    # AGGRESSIVE CRISIS AMPLIFICATION
    if severe_score > 0.03:  # Any severe signal gets major boost
        # Severe depression pathway - ensure HIGH classification
        base_score = 0.60  # Start high
        severe_boost = severe_score * 8.0  # Amplify severe signals dramatically
        moderate_boost = moderate_score * 2.0  # Moderate provides additional evidence
        
        max_crisis_score = base_score + severe_boost + moderate_boost
        reason = f"severe_amplified (severe={severe_score:.3f}*8 + moderate={moderate_score:.3f}*2)"
        
    elif moderate_score > 0.30:  # Strong moderate signal
        # Moderate depression pathway - ensure at least MEDIUM, often HIGH
        base_score = 0.35  # Start at medium level
        moderate_boost = moderate_score * 3.0  # Amplify moderate signals
        
        # Extra boost if not_depression is low (model is uncertain about "not depression")
        uncertainty_boost = max(0, 0.7 - not_depression_score) * 0.5
        
        max_crisis_score = base_score + moderate_boost + uncertainty_boost
        reason = f"moderate_amplified (moderate={moderate_score:.3f}*3 + uncertainty_boost={uncertainty_boost:.3f})"
        
    elif total_depression > 0.20:  # Any meaningful depression signal
        # Weak depression pathway - ensure at least LOW
        base_score = 0.15
        depression_boost = total_depression * 2.0
        
        max_crisis_score = base_score + depression_boost
        reason = f"weak_depression_amplified (total_dep={total_depression:.3f}*2)"
        
    elif not_depression_score > 0.85:  # Very confident not depression
        max_crisis_score = 0.0
        reason = f"confident_not_depression ({not_depression_score:.3f})"
        
    else:  # Very unclear signals
        # Use conservative scoring for unclear cases
        max_crisis_score = total_depression * 0.8
        reason = f"unclear_signals (total_dep={total_depression:.3f}*0.8)"
    
    # Apply final bounds
    max_crisis_score = min(max_crisis_score, 1.0)
    max_crisis_score = max(max_crisis_score, 0.0)
    
    logger.info(f"Enhanced scoring: {reason} -> crisis score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories


def map_score_to_crisis_level(crisis_score):
    """Updated thresholds for enhanced scoring"""
    
    # With amplified scoring, we can use higher thresholds
    if crisis_score >= 0.65:   # HIGH: Should catch amplified severe signals
        return 'high'      
    elif crisis_score >= 0.30:  # MEDIUM: Should catch amplified moderate signals
        return 'medium'    
    elif crisis_score >= 0.10:  # LOW: Should catch weak depression signals
        return 'low'       
    else:
        return 'none'

@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Analyze a message for crisis indicators"""
    
    if not nlp_model:
        raise HTTPException(status_code=503, detail="NLP model not loaded")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    
    start_time = time.time()
    
    try:
        # Run ML inference
        prediction = nlp_model(request.message)
        
        # Analyze for crisis indicators
        crisis_score, categories = analyze_mental_health_prediction(prediction)
        
        # CONTENT-AWARE REFINEMENT: Distinguish positive vs negative extreme language
        if crisis_score > 0:
            message_lower = request.message.lower()
            
            # Check if high LABEL_1 score is actually positive language (not crisis)
            positive_indicators = [
                'thank', 'love', 'great', 'awesome', 'happy', 'excited', 
                'wonderful', 'amazing', 'good', 'help', 'appreciate',
                'pizza', 'food', 'movie', 'fun', 'enjoy'
            ]
            
            # Crisis language indicators
            crisis_indicators = [
                'kill', 'die', 'suicide', 'hurt', 'harm', 'depressed', 
                'sad', 'hopeless', 'worthless', 'hate myself', 'end it',
                'can\'t go on', 'pointless', 'empty', 'lost', 'give up'
            ]
            
            has_positive = any(word in message_lower for word in positive_indicators)
            has_crisis = any(word in message_lower for word in crisis_indicators)
            
            if has_positive and not has_crisis:
                # High score but positive content → no crisis
                final_crisis_score = 0.0
                reason = "positive_language_detected"
            elif has_crisis:
                # Crisis language confirmed → keep score
                final_crisis_score = crisis_score
                reason = "crisis_language_confirmed"
            else:
                # Unclear → use moderate score
                final_crisis_score = crisis_score * 0.6
                reason = "unclear_sentiment"
                
            logger.debug(f"Content refinement: '{message_lower[:30]}...' -> {reason}, score: {crisis_score:.3f} -> {final_crisis_score:.3f}")
        else:
            final_crisis_score = crisis_score
            reason = "no_crisis_detected"
        
        # Map to crisis level
        crisis_level = map_score_to_crisis_level(final_crisis_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log for monitoring (without full message for privacy)
        message_preview = request.message[:30] + "..." if len(request.message) > 30 else request.message
        logger.info(f"Analysis: '{message_preview}' -> {crisis_level} (score: {final_crisis_score:.3f}, reason: {reason}, {processing_time:.1f}ms)")
        
        return CrisisResponse(
            needs_response=crisis_level != 'none',
            crisis_level=crisis_level,
            confidence_score=final_crisis_score,
            detected_categories=[cat['category'] for cat in categories],
            method='deproberta_depression_severity',
            processing_time_ms=processing_time,
            model_info="rafalposwiata/deproberta-large-depression"
        )
        
    except Exception as e:
        logger.error(f"Error analyzing message: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    
    uptime = time.time() - startup_time
    
    return HealthResponse(
        status="healthy" if nlp_model else "unhealthy",
        model_loaded=nlp_model is not None,
        uptime_seconds=uptime,
        hardware_info={
            "cpu": "Ryzen 7 7700x",
            "gpu": "RTX 3050 (8GB VRAM)",
            "ram": "64GB",
            "inference_device": "CPU"
        }
    )

@app.get("/stats")
async def get_stats():
    """Get detailed service statistics"""
    
    uptime = time.time() - startup_time
    
    return {
        "service": "Ash NLP Service (Standalone)",
        "version": "2.0",
        "model_loaded": nlp_model is not None,
        "uptime_seconds": uptime,
        "uptime_hours": uptime / 3600,
        "model_info": {
            "type": "Depression Severity Detection",
            "model_id": "rafalposwiata/deproberta-large-depression",  # FIXED
            "method": "depression_severity_classification",
            "labels": ["not depression", "moderate", "severe"],
            "inference_device": "CPU (Ryzen 7 7700x)",
            "hardware": "RTX 3050 + 64GB RAM"
        },
        "hardware": {
            "cpu": "AMD Ryzen 7 7700x",
            "gpu": "NVIDIA RTX 3050 (8GB)",
            "ram": "64GB DDR4/DDR5",
            "os": "Windows 11"
        }
    }

@app.get("/")
async def root():
    """Service info endpoint"""
    return {
        "service": "Ash NLP Crisis Detection Service",
        "version": "2.0",
        "status": "running",
        "model": "rafalposwiata/deproberta-large-depression",  # FIXED
        "endpoints": {
            "analyze": "POST /analyze - Analyze message for crisis",
            "health": "GET /health - Health check",
            "stats": "GET /stats - Service statistics"
        }
    }

if __name__ == "__main__":
    # Standalone service configuration
    logger.info("🚀 Starting Ash NLP Service (Standalone)")
    logger.info("💻 Optimized for Ryzen 7 7700x + RTX 3050 + 64GB RAM")
    logger.info("🔍 Using professional suicidality detection model (93.9% accuracy)")
    logger.info("🌐 Starting server on 0.0.0.0:8881")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",        # Listen on all interfaces
            port=8881,             # Standard port
            log_level="info",
            reload=False,
            workers=1              # Single worker for model memory efficiency
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        logger.exception("Full traceback:")
        raise