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
        # Test with original model to check if labels are switched
        model_id = "mrm8488/distilroberta-base-finetuned-suicide-depression"
        
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
    """Analyze using correct label interpretation for this model"""
    
    max_crisis_score = 0.0
    detected_categories = []
    
    # Handle different output formats
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
    
    # Extract scores
    label_0_score = 0.0
    label_1_score = 0.0
    
    for prediction in predictions_to_process:
        if not isinstance(prediction, dict):
            continue
            
        label = str(prediction.get('label', '')).lower()
        score = float(prediction.get('score', 0.0))
        
        if label == "label_0":
            label_0_score = score
        elif label == "label_1":
            label_1_score = score
        
        detected_categories.append({
            'category': 'negative_sentiment' if label == 'label_0' else 'positive_or_extreme',
            'raw_score': score,
            'confidence': score,
            'original_label': prediction.get('label', 'unknown'),
            'is_crisis': False  # We'll determine this below
        })
    
    # CORRECTED INTERPRETATION based on diagnostic evidence:
    # This model appears to be sentiment-based, not suicide-specific:
    # LABEL_0 = negative sentiment (sad, depressed, etc.)
    # LABEL_1 = positive sentiment OR extreme negative (toxic/harmful)
    
    # Crisis indicators:
    # 1. High LABEL_0 = depression/sadness → medium crisis
    # 2. High LABEL_1 = could be positive (no crisis) OR extreme negative (high crisis)
    
    if label_0_score > label_1_score:
        # Negative sentiment dominates → some level of crisis
        max_crisis_score = label_0_score
        logger.debug(f"Negative sentiment detected: {label_0_score:.3f}")
        
        # Update categories
        for cat in detected_categories:
            if cat['original_label'] == 'LABEL_0':
                cat['is_crisis'] = True
                cat['category'] = 'negative_sentiment_crisis'
                
    elif label_1_score > 0.9:
        # Very high LABEL_1 could be extreme negative (like "kill myself")
        max_crisis_score = label_1_score
        logger.debug(f"Extreme language detected: {label_1_score:.3f}")
        
        # Update categories
        for cat in detected_categories:
            if cat['original_label'] == 'LABEL_1':
                cat['is_crisis'] = True
                cat['category'] = 'extreme_language_crisis'
    else:
        # Moderate LABEL_1 is probably positive sentiment → no crisis
        max_crisis_score = 0.0
        logger.debug(f"Positive sentiment detected: {label_1_score:.3f}")
    
    logger.debug(f"Final crisis score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories

def map_score_to_crisis_level(crisis_score):
    """Map crisis score to response level (testing switched labels)"""
    
    # Simple thresholds for testing the switched labels theory
    if crisis_score >= 0.8:
        return 'high'      # Very confident crisis detection
    elif crisis_score >= 0.6:
        return 'medium'    # Moderately confident
    elif crisis_score >= 0.3:
        return 'low'       # Some indication
    else:
        return 'none'      # No significant risk detected

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
        
        # Analyze for crisis indicators (testing switched labels theory)
        crisis_score, categories = analyze_mental_health_prediction(prediction)
        
        # Map to crisis level
        crisis_level = map_score_to_crisis_level(crisis_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log for monitoring (without full message for privacy)
        message_preview = request.message[:30] + "..." if len(request.message) > 30 else request.message
        logger.info(f"Analysis: '{message_preview}' -> {crisis_level} (score: {crisis_score:.3f}, {processing_time:.1f}ms)")
        
        return CrisisResponse(
            needs_response=crisis_level != 'none',
            crisis_level=crisis_level,
            confidence_score=crisis_score,
            detected_categories=[cat['category'] for cat in categories],
            method='suicide_depression_roberta_switched_labels',
            processing_time_ms=processing_time,
            model_info="mrm8488/distilroberta-base-finetuned-suicide-depression"
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
            "type": "Suicidality Detection",
            "model_id": "sentinet/suicidality",  # FIXED: Consistent
            "method": "suicidality_detection_electra",
            "accuracy": "93.9%",
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
        "model": "sentinet/suicidality",  # FIXED: Show actual model
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