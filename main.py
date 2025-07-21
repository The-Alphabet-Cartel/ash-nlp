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
    """PURE ML AGGRESSIVE scoring - trust the model completely"""
    
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
    
    # PURE MATHEMATICAL APPROACH - VERY AGGRESSIVE
    # Based on failure analysis: need to boost scores significantly
    
    total_depression = moderate_score + severe_score
    
    # Calculate model confidence (how decisive is the prediction?)
    all_scores = [not_depression_score, moderate_score, severe_score]
    max_prediction = max(all_scores)
    confidence_factor = max_prediction  # Use the strongest prediction as confidence
    
    # AGGRESSIVE AMPLIFICATION STRATEGY
    
    # Path 1: Any severe signal → HIGH
    if severe_score > 0.01:  # Even tiny severe signals
        base_score = 0.70
        severe_amplification = severe_score * 10.0  # Very aggressive
        moderate_support = moderate_score * 1.0
        confidence_boost = confidence_factor * 0.3
        
        max_crisis_score = base_score + severe_amplification + moderate_support + confidence_boost
        reason = f"severe_path (0.70 + {severe_score:.3f}*10 + {moderate_score:.3f} + conf_boost={confidence_factor:.3f}*0.3)"
        
    # Path 2: Strong moderate → HIGH  
    elif moderate_score > 0.50:
        base_score = 0.70
        moderate_amplification = (moderate_score - 0.50) * 4.0
        confidence_boost = confidence_factor * 0.2
        
        max_crisis_score = base_score + moderate_amplification + confidence_boost
        reason = f"strong_moderate_path (0.70 + excess={moderate_score-0.50:.3f}*4 + conf_boost={confidence_factor:.3f}*0.2)"
        
    # Path 3: Moderate depression → MEDIUM/HIGH
    elif moderate_score > 0.20:  # Much lower threshold
        base_score = 0.40  # Start at MEDIUM level
        moderate_amplification = moderate_score * 2.0  # Double the moderate score
        severe_boost = severe_score * 8.0  # Any severe helps a lot
        confidence_boost = confidence_factor * 0.15
        
        max_crisis_score = base_score + moderate_amplification + severe_boost + confidence_boost
        reason = f"moderate_path (0.40 + {moderate_score:.3f}*2 + {severe_score:.3f}*8 + conf_boost={confidence_factor:.3f}*0.15)"
        
    # Path 4: Any depression signal → LOW/MEDIUM
    elif total_depression > 0.10:
        base_score = 0.20  # Start at LOW level
        depression_amplification = total_depression * 2.5  # Aggressive amplification
        confidence_boost = confidence_factor * 0.1
        
        max_crisis_score = base_score + depression_amplification + confidence_boost
        reason = f"depression_path (0.20 + {total_depression:.3f}*2.5 + conf_boost={confidence_factor:.3f}*0.1)"
        
    # Path 5: Weak depression signals → LOW
    elif total_depression > 0.05:
        base_score = 0.10
        weak_amplification = total_depression * 3.0  # Even more aggressive for weak signals
        
        max_crisis_score = base_score + weak_amplification
        reason = f"weak_depression_path (0.10 + {total_depression:.3f}*3.0)"
        
    # Path 6: Very confident not depression → NONE
    elif not_depression_score > 0.90:
        max_crisis_score = 0.0
        reason = f"confident_not_depression ({not_depression_score:.3f})"
        
    # Path 7: Unclear but some signal → LOW
    else:
        max_crisis_score = total_depression * 2.0  # Simple amplification
        reason = f"unclear_signals ({total_depression:.3f}*2.0)"
    
    # Apply bounds
    max_crisis_score = min(max_crisis_score, 1.0)
    max_crisis_score = max(max_crisis_score, 0.0)
    
    logger.info(f"Aggressive ML scoring: {reason} -> crisis score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories

def map_score_to_crisis_level(crisis_score):
    """MUCH LOWER thresholds to match aggressive scoring"""
    
    # Much more aggressive thresholds based on the failure analysis
    if crisis_score >= 0.60:   # HIGH: Lower threshold to catch more cases
        return 'high'      
    elif crisis_score >= 0.30:  # MEDIUM: Much lower to catch the 0.18-0.35 range
        return 'medium'    
    elif crisis_score >= 0.10:  # LOW: Lower threshold
        return 'low'       
    else:
        return 'none'

@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Analyze a message for crisis indicators - PURE ML ONLY"""
    
    if not nlp_model:
        raise HTTPException(status_code=503, detail="NLP model not loaded")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    
    start_time = time.time()
    
    try:
        # Run ML inference
        prediction = nlp_model(request.message)
        
        # Analyze for crisis indicators - PURE ML
        crisis_score, categories = analyze_mental_health_prediction(prediction)
        
        # Map to crisis level
        crisis_level = map_score_to_crisis_level(crisis_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log for monitoring
        message_preview = request.message[:30] + "..." if len(request.message) > 30 else request.message
        logger.info(f"Pure ML analysis: '{message_preview}' -> {crisis_level} (score: {crisis_score:.3f}, {processing_time:.1f}ms)")
        
        return CrisisResponse(
            needs_response=crisis_level != 'none',
            crisis_level=crisis_level,
            confidence_score=crisis_score,
            detected_categories=[cat['category'] for cat in categories],
            method='deproberta_depression_severity_aggressive',
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