#!/usr/bin/env python3
"""
Standalone NLP Service for Ash Bot
Runs MentalRoBERTa model for mental health crisis detection
Designed to run on separate AI rig hardware
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from transformers import pipeline
from huggingface_hub import login
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
    """Load the MentalRoBERTa model with authentication"""
    global nlp_model
    
    logger.info("=" * 50)
    logger.info("STARTING MODEL LOADING PROCESS")
    logger.info("=" * 50)
    
    try:
        # Authenticate with Hugging Face
        hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN')
        if hf_token:
            login(token=hf_token)
            logger.info("✅ Authenticated with Hugging Face via token")
        else:
            # Try using stored credentials from huggingface-cli login
            try:
                login()
                logger.info("✅ Using stored Hugging Face credentials")
            except Exception as e:
                logger.error(f"❌ No Hugging Face token found. Set HUGGINGFACE_HUB_TOKEN environment variable")
                logger.error(f"Or run: huggingface-cli login")
                raise
        
        logger.info("Loading MentalRoBERTa model...")
        logger.info("Hardware: Ryzen 7 7700x + RTX 3050 + 64GB RAM")
        
        # Load the mental health model
        model_id = "mental/mental-roberta-base"
        
        logger.info(f"Loading model: {model_id}")
        logger.info("This model is trained on mental health Reddit data (r/SuicideWatch, r/depression, etc.)...")
        
        nlp_model = pipeline(
            "text-classification",
            model=model_id,
            device=-1,  # CPU inference (RTX 3050 has limited VRAM)
            top_k=None  # Return all scores for analysis
        )
        
        logger.info("✅ MentalRoBERTa model loaded successfully!")
        
        # Test the model to understand output format
        test_result = nlp_model("I feel sad today")
        logger.info(f"✅ Model test successful")
        logger.info(f"Test result format: {test_result}")
        
        # Test with a more neutral message
        test_neutral = nlp_model("The weather is nice today")
        logger.info(f"Neutral test result: {test_neutral}")
        
        logger.info("✅ Model ready for mental health crisis detection")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Failed to load NLP model: {e}")
        logger.exception("Full traceback:")
        nlp_model = None
        raise

def analyze_mental_health_prediction(prediction_result):
    """Analyze MentalRoBERTa output - CORRECTED for actual label behavior"""
    
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
    
    # MentalRoBERTa outputs:
    # LABEL_0: Non-mental health / Normal (higher = more normal)
    # LABEL_1: Mental health concern (higher = more concerning)
    
    normal_score = 0.0
    mental_health_score = 0.0
    
    for prediction in predictions_to_process:
        if not isinstance(prediction, dict):
            continue
            
        label = str(prediction.get('label', '')).upper()
        score = float(prediction.get('score', 0.0))
        
        if label == 'LABEL_0':  # Normal/non-mental health
            normal_score = score
        elif label == 'LABEL_1':  # Mental health concern
            mental_health_score = score
        
        detected_categories.append({
            'category': label,
            'raw_score': score,
            'confidence': score,
            'original_label': prediction.get('label', 'unknown'),
            'is_crisis': label == 'LABEL_1'
        })
    
    logger.info(f"MentalRoBERTa scores - Normal: {normal_score:.4f}, Mental Health Concern: {mental_health_score:.4f}")
    
    # CORRECTED SCORING LOGIC
    # Focus on how confident the model is in mental health concern (LABEL_1)
    # and how much it beats the normal score (LABEL_0)
    
    # Calculate confidence margin
    confidence_margin = mental_health_score - normal_score
    
    # High confidence mental health concern
    if mental_health_score > 0.8 and confidence_margin > 0.2:
        # Very confident mental health concern → HIGH
        max_crisis_score = 0.75 + (mental_health_score * 0.25)  # 0.75-1.00 range
        reason = f"high_confidence_mental_health (score={mental_health_score:.3f}, margin={confidence_margin:.3f})"
        
    elif mental_health_score > 0.7 and confidence_margin > 0.1:
        # Strong mental health concern → HIGH
        max_crisis_score = 0.65 + (mental_health_score * 0.25)  # 0.65-0.925 range
        reason = f"strong_mental_health (score={mental_health_score:.3f}, margin={confidence_margin:.3f})"
        
    elif mental_health_score > 0.6 and confidence_margin > 0.05:
        # Moderate mental health concern → MEDIUM
        max_crisis_score = 0.45 + (mental_health_score * 0.25)  # 0.45-0.70 range
        reason = f"moderate_mental_health (score={mental_health_score:.3f}, margin={confidence_margin:.3f})"
        
    elif mental_health_score > 0.5 and confidence_margin > 0.0:
        # Slight mental health concern → MEDIUM
        max_crisis_score = 0.30 + (mental_health_score * 0.30)  # 0.30-0.60 range
        reason = f"slight_mental_health (score={mental_health_score:.3f}, margin={confidence_margin:.3f})"
        
    elif mental_health_score > 0.4:
        # Weak mental health signal → LOW
        max_crisis_score = 0.15 + (mental_health_score * 0.25)  # 0.15-0.40 range
        reason = f"weak_mental_health (score={mental_health_score:.3f}, margin={confidence_margin:.3f})"
        
    elif normal_score > 0.7:
        # Confident normal/no concern → NONE
        max_crisis_score = 0.0
        reason = f"confident_normal (normal_score={normal_score:.3f})"
        
    else:
        # Very unclear or low signals → NONE/LOW
        max_crisis_score = mental_health_score * 0.3  # Scale down uncertain cases
        reason = f"unclear_signals (mental={mental_health_score:.3f}, normal={normal_score:.3f})"
    
    # Apply bounds
    max_crisis_score = min(max_crisis_score, 1.0)
    max_crisis_score = max(max_crisis_score, 0.0)
    
    logger.info(f"MentalRoBERTa analysis: {reason} -> crisis score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories

def map_score_to_crisis_level(crisis_score):
    """Map crisis score to response level (calibrated for MentalRoBERTa)"""
    
    # Adjusted thresholds based on the corrected scoring
    if crisis_score >= 0.60:   # HIGH: Strong mental health concern
        return 'high'      
    elif crisis_score >= 0.30:  # MEDIUM: Moderate mental health concern
        return 'medium'    
    elif crisis_score >= 0.10:  # LOW: Mild mental health indicators
        return 'low'       
    else:
        return 'none'      # No significant concern detected

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
    title="Ash NLP Service (MentalRoBERTa)", 
    version="3.0",
    description="Mental Health Crisis Detection Service using MentalRoBERTa",
    lifespan=lifespan
)

@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Analyze a message for mental health crisis indicators"""
    
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
        
        # Map to crisis level
        crisis_level = map_score_to_crisis_level(crisis_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log for monitoring (privacy-aware)
        message_preview = request.message[:30] + "..." if len(request.message) > 30 else request.message
        logger.info(f"Analysis: '{message_preview}' -> {crisis_level} (score: {crisis_score:.3f}, {processing_time:.1f}ms)")
        
        return CrisisResponse(
            needs_response=crisis_level != 'none',
            crisis_level=crisis_level,
            confidence_score=crisis_score,
            detected_categories=[cat['category'] for cat in categories],
            method='mental_roberta_classification',
            processing_time_ms=processing_time,
            model_info="mental/mental-roberta-base"
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
        "service": "Ash NLP Service (MentalRoBERTa)",
        "version": "3.0",
        "model_loaded": nlp_model is not None,
        "uptime_seconds": uptime,
        "uptime_hours": uptime / 3600,
        "model_info": {
            "type": "Mental Health Crisis Detection",
            "model_id": "mental/mental-roberta-base",
            "method": "mental_health_classification",
            "architecture": "RoBERTa",
            "description": "Domain-specific RoBERTa trained on mental health Reddit data",
            "training_data": "r/SuicideWatch, r/depression, r/Anxiety, r/bipolar, etc.",
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
        "service": "Ash NLP Mental Health Crisis Detection",
        "version": "3.0",
        "status": "running",
        "model": "mental/mental-roberta-base",
        "description": "MentalRoBERTa - specialized mental health detection model",
        "endpoints": {
            "analyze": "POST /analyze - Analyze message for mental health crisis",
            "health": "GET /health - Health check",
            "stats": "GET /stats - Service statistics"
        }
    }

if __name__ == "__main__":
    # Standalone service configuration
    logger.info("🚀 Starting Ash NLP Service (MentalRoBERTa)")
    logger.info("💻 Optimized for Ryzen 7 7700x + RTX 3050 + 64GB RAM")
    logger.info("🧠 Using MentalRoBERTa for mental health crisis detection")
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