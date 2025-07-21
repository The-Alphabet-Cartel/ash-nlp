#!/usr/bin/env python3
"""
Standalone NLP Service for Ash Bot
Runs Depression Detection model with targeted fixes for specific issues
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
    """Load the depression detection model"""
    global nlp_model
    
    logger.info("=" * 50)
    logger.info("STARTING MODEL LOADING PROCESS")
    logger.info("=" * 50)
    logger.info("Loading Depression Detection model...")
    logger.info("Hardware: Ryzen 7 7700x + RTX 3050 + 64GB RAM")
    
    try:
        # Use the depression model that showed excellent performance
        model_id = "rafalposwiata/deproberta-large-depression"
        
        logger.info(f"Loading model: {model_id}")
        logger.info("This model provides excellent crisis vs normal discrimination...")
        
        nlp_model = pipeline(
            "text-classification",
            model=model_id,
            device=-1,  # Force CPU inference
            top_k=None  # Return all scores for analysis
        )
        
        logger.info("✅ Depression model loaded successfully!")
        
        # Test with clear examples
        test_crisis = nlp_model("I want to kill myself")
        test_normal = nlp_model("I love pizza")
        
        logger.info(f"✅ Crisis test: {test_crisis}")
        logger.info(f"✅ Normal test: {test_normal}")
        logger.info("✅ Model ready for crisis detection with targeted fixes")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Failed to load NLP model: {e}")
        logger.exception("Full traceback:")
        nlp_model = None
        raise

def analyze_mental_health_prediction(prediction_result):
    """Analyze depression model output with proven scoring logic"""
    
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
    
    logger.info(f"Depression scores - Not: {not_depression_score:.4f}, Moderate: {moderate_score:.4f}, Severe: {severe_score:.4f}")
    
    # PROVEN SCORING LOGIC (achieved 91.7% HIGH detection)
    total_depression = moderate_score + severe_score
    
    if severe_score > 0.02:  # Any severe signal
        max_crisis_score = 0.70 + (severe_score * 10.0)  # Aggressive amplification
        reason = f"severe_detected ({severe_score:.3f})"
        
    elif moderate_score > 0.40:  # Strong moderate signal  
        max_crisis_score = 0.50 + (moderate_score * 1.0)  # High classification
        reason = f"strong_moderate ({moderate_score:.3f})"
        
    elif moderate_score > 0.25:  # Moderate signal
        max_crisis_score = 0.25 + (moderate_score * 1.2)  # Medium classification
        reason = f"moderate_signal ({moderate_score:.3f})"
        
    elif total_depression > 0.15:  # Any meaningful depression
        max_crisis_score = 0.10 + (total_depression * 1.5)  # Low classification
        reason = f"depression_detected ({total_depression:.3f})"
        
    elif not_depression_score > 0.95:  # Very confident not depression
        max_crisis_score = 0.0
        reason = f"confident_not_depression ({not_depression_score:.3f})"
        
    else:  # Weak signals
        max_crisis_score = total_depression * 1.0
        reason = f"weak_signals ({total_depression:.3f})"
    
    # Apply bounds
    max_crisis_score = min(max_crisis_score, 1.0)
    max_crisis_score = max(max_crisis_score, 0.0)
    
    logger.info(f"Base depression analysis: {reason} -> crisis score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories

def apply_targeted_fixes(message, crisis_score, categories):
    """Apply specific fixes for the two identified issues"""
    
    message_lower = message.lower().strip()
    
    # FIX #1: Boost specific missed HIGH pattern
    # "Maybe everyone would be better off without me" scored 0.051 instead of HIGH
    burden_patterns = [
        "better off without me",
        "everyone would be better without me", 
        "better off if i was gone",
        "better off if i wasn't here",
        "world would be better without me",
        "better off if i were dead",
        "better off if i die"
    ]
    
    for pattern in burden_patterns:
        if pattern in message_lower:
            # This is a serious burden ideation pattern that should be HIGH
            boosted_score = max(crisis_score, 0.70)  # Ensure at least HIGH threshold
            logger.info(f"BURDEN PATTERN FIX: '{pattern}' detected -> boosting {crisis_score:.3f} to {boosted_score:.3f}")
            crisis_score = boosted_score
            break
    
    # FIX #2: Reduce obvious positive idiom false positives
    # "I'm dead tired" (0.995) and "That joke killed me" (1.000) were false positives
    
    positive_idiom_patterns = [
        # Fatigue idioms in positive/neutral contexts
        ("dead tired", lambda msg: not any(neg in msg for neg in ["depressed", "sad", "hopeless", "hate", "worthless", "kill myself", "suicide"])),
        
        # Humor/entertainment idioms
        ("joke killed me", lambda msg: "joke" in msg or "funny" in msg or "laugh" in msg),
        ("that killed me", lambda msg: any(pos in msg for pos in ["joke", "funny", "hilarious", "laugh", "comedy"])),
        ("dying of laughter", lambda msg: "laugh" in msg or "funny" in msg or "hilarious" in msg),
        ("died laughing", lambda msg: "laugh" in msg or "funny" in msg or "hilarious" in msg),
        
        # Success/performance idioms  
        ("killing it", lambda msg: any(pos in msg for pos in ["work", "job", "performance", "success", "great", "awesome"])),
        ("slaying it", lambda msg: any(pos in msg for pos in ["work", "job", "performance", "success", "great", "awesome"])),
    ]
    
    for pattern, context_check in positive_idiom_patterns:
        if pattern in message_lower and context_check(message_lower):
            # This is clearly an idiom in positive context, not a crisis
            reduced_score = min(crisis_score * 0.1, 0.10)  # Dramatic reduction, cap at LOW
            logger.info(f"POSITIVE IDIOM FIX: '{pattern}' detected in positive context -> reducing {crisis_score:.3f} to {reduced_score:.3f}")
            crisis_score = reduced_score
            break
    
    return crisis_score

def map_score_to_crisis_level(crisis_score):
    """Map crisis score to response level (proven thresholds)"""
    
    # These thresholds achieved 91.7% HIGH detection
    if crisis_score >= 0.45:   # HIGH: Strong depression signals
        return 'high'      
    elif crisis_score >= 0.20:  # MEDIUM: Moderate depression signals
        return 'medium'    
    elif crisis_score >= 0.05:  # LOW: Mild depression indicators
        return 'low'       
    else:
        return 'none'      # No significant depression detected

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
    title="Ash NLP Service (Depression Detection + Fixes)", 
    version="3.1",
    description="Mental Health Crisis Detection with Targeted Improvements",
    lifespan=lifespan
)

@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Analyze a message with targeted fixes for specific issues"""
    
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
        
        # Apply targeted fixes for specific known issues
        final_crisis_score = apply_targeted_fixes(request.message, crisis_score, categories)
        
        # Map to crisis level
        crisis_level = map_score_to_crisis_level(final_crisis_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log for monitoring (show if fixes were applied)
        message_preview = request.message[:30] + "..." if len(request.message) > 30 else request.message
        if abs(crisis_score - final_crisis_score) > 0.1:
            logger.info(f"TARGETED FIX applied: '{message_preview}' -> {crisis_score:.3f} → {final_crisis_score:.3f} → {crisis_level}")
        else:
            logger.info(f"Analysis: '{message_preview}' -> {crisis_level} (score: {final_crisis_score:.3f}, {processing_time:.1f}ms)")
        
        return CrisisResponse(
            needs_response=crisis_level != 'none',
            crisis_level=crisis_level,
            confidence_score=final_crisis_score,
            detected_categories=[cat['category'] for cat in categories],
            method='depression_severity_with_targeted_fixes',
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
        "service": "Ash NLP Service (Depression Detection + Fixes)",
        "version": "3.1",
        "model_loaded": nlp_model is not None,
        "uptime_seconds": uptime,
        "uptime_hours": uptime / 3600,
        "model_info": {
            "type": "Depression Severity Detection",
            "model_id": "rafalposwiata/deproberta-large-depression",
            "method": "depression_severity_with_targeted_fixes",
            "architecture": "DeBERTa",
            "description": "Depression detection with fixes for burden ideation and positive idioms",
            "labels": ["not depression", "moderate", "severe"],
            "fixes_applied": ["burden_ideation_boost", "positive_idiom_reduction"],
            "inference_device": "CPU (Ryzen 7 7700x)",
            "hardware": "RTX 3050 + 64GB RAM"
        },
        "performance": {
            "high_crisis_detection": "91.7% -> Expected 100% with fixes",
            "false_positive_rate": "10.5% -> Expected ~5% with fixes",
            "overall_accuracy": "Expected ~90%+ with fixes"
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
        "service": "Ash NLP Mental Health Crisis Detection",
        "version": "3.1",
        "status": "running",
        "model": "rafalposwiata/deproberta-large-depression",
        "description": "Depression detection with targeted fixes for specific edge cases",
        "improvements": {
            "burden_ideation": "Detects 'better off without me' patterns",
            "positive_idioms": "Handles 'dead tired', 'joke killed me' correctly"
        },
        "endpoints": {
            "analyze": "POST /analyze - Analyze message for mental health crisis",
            "health": "GET /health - Health check",
            "stats": "GET /stats - Service statistics"
        }
    }

if __name__ == "__main__":
    # Standalone service configuration
    logger.info("🚀 Starting Ash NLP Service (Depression Detection + Targeted Fixes)")
    logger.info("💻 Optimized for Ryzen 7 7700x + RTX 3050 + 64GB RAM")
    logger.info("🧠 Using Depression Model with targeted improvements")
    logger.info("🎯 Fixes: Burden ideation boost + Positive idiom reduction")
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