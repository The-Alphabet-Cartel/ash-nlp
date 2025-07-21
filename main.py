#!/usr/bin/env python3
"""
Enhanced NLP Service for Ash Bot
Multi-model approach with improved scoring logic and context analysis
Targets: 80%+ overall accuracy, 95%+ high crisis detection, <10% false positives
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from transformers import pipeline
import logging
import time
import os
import uvicorn
import re
from typing import Optional, Dict, List, Tuple
from contextlib import asynccontextmanager
import numpy as np

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
depression_model = None
sentiment_model = None

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
    reasoning: Optional[str] = None

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    model_loaded: bool
    uptime_seconds: float
    hardware_info: dict

# Service startup time
startup_time = time.time()

# Contextual pattern libraries (no crisis keywords - handled by bot)
# Focus on context detection for better model interpretation

POSITIVE_CONTEXT_PATTERNS = {
    'humor': ['joke', 'funny', 'hilarious', 'laugh', 'comedy', 'lol', 'haha'],
    'entertainment': ['movie', 'show', 'game', 'book', 'story', 'video'],
    'work_success': ['work', 'job', 'project', 'performance', 'success', 'achievement'],
    'food': ['hungry', 'eat', 'food', 'burger', 'pizza', 'meal'],
    'fatigue': ['tired', 'exhausted', 'sleepy', 'worn out'],
    'frustration': ['traffic', 'homework', 'test', 'exam', 'assignment']
}

IDIOM_PATTERNS = [
    (r'\b(dead|dying) (tired|exhausted)\b', 'fatigue'),
    (r'\bjoke (killed|murdered) me\b', 'humor'),
    (r'\b(that|it) (killed|murdered) me\b', 'humor'),  # When followed by humor context
    (r'\bdying of laughter\b', 'humor'),
    (r'\b(killing|slaying) it\b', 'success'),
    (r'\bmurder (a|some) \w+\b', 'desire'),  # "murder a burger"
    (r'\bdriving me (crazy|insane|nuts)\b', 'frustration'),
    (r'\b(brutal|killer) (test|exam|workout)\b', 'difficulty')
]

async def load_models():
    """Load both depression and sentiment analysis models"""
    global depression_model, sentiment_model
    
    logger.info("=" * 50)
    logger.info("STARTING ENHANCED MODEL LOADING PROCESS")
    logger.info("=" * 50)
    
    try:
        # Primary depression model
        logger.info("Loading Depression Detection model...")
        depression_model = pipeline(
            "text-classification",
            model="rafalposwiata/deproberta-large-depression",
            device=-1,  # CPU inference
            top_k=None
        )
        
        # Secondary sentiment model for context
        logger.info("Loading Sentiment Analysis model...")
        sentiment_model = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=-1,
            top_k=None
        )
        
        logger.info("✅ Both models loaded successfully!")
        
        # Quick test
        test_message = "I want to kill myself"
        dep_result = depression_model(test_message)
        sent_result = sentiment_model(test_message)
        
        logger.info(f"✅ Depression test: {dep_result}")
        logger.info(f"✅ Sentiment test: {sent_result}")
        logger.info("✅ Enhanced multi-model system ready")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        logger.exception("Full traceback:")
        raise

def extract_context_signals(message: str) -> Dict[str, any]:
    """Extract contextual signals from the message"""
    message_lower = message.lower().strip()
    
    context = {
        'has_positive_words': False,
        'has_humor_context': False,
        'has_work_context': False,
        'has_idiom': False,
        'idiom_type': None,
        'question_mark': '?' in message,
        'exclamation': '!' in message,
        'negation_context': False,
        'temporal_indicators': [],
        'message_lower': message_lower  # Add for burden pattern detection
    }
    
    # Check for positive context
    for category, words in POSITIVE_CONTEXT_PATTERNS.items():
        if any(word in message_lower for word in words):
            context['has_positive_words'] = True
            if category == 'humor':
                context['has_humor_context'] = True
            elif category in ['work_success', 'entertainment']:
                context['has_work_context'] = True
    
    # Check for idioms
    for pattern, idiom_type in IDIOM_PATTERNS:
        if re.search(pattern, message_lower, re.IGNORECASE):
            context['has_idiom'] = True
            context['idiom_type'] = idiom_type
            break
    
    # Check for negation context (affects model interpretation)
    context['negation_context'] = detect_negation_context(message)
    
    # Temporal indicators
    temporal_words = ['today', 'yesterday', 'lately', 'recently', 'always', 'never', 'sometimes']
    context['temporal_indicators'] = [word for word in temporal_words if word in message_lower]
    
    return context

def detect_negation_context(message: str) -> bool:
    """Detect if the message contains negation that might affect crisis interpretation"""
    message_lower = message.lower().strip()
    
    negation_patterns = [
        r'\bnot (really|actually|that|very|going to|planning to|trying to)\b',
        r'\bdoesn\'t (really|actually|mean|want to)\b',
        r'\bisn\'t (really|actually|that)\b',
        r'\bwon\'t (really|actually|ever)\b',
        r'\bdon\'t (want to|plan to|intend to)\b'
    ]
    
    for pattern in negation_patterns:
        if re.search(pattern, message_lower):
            return True
    
    return False

def analyze_sentiment_context(sentiment_result) -> Dict[str, float]:
    """Analyze sentiment to provide additional context"""
    sentiment_scores = {'negative': 0.0, 'neutral': 0.0, 'positive': 0.0}
    
    if isinstance(sentiment_result, list) and len(sentiment_result) > 0:
        for item in sentiment_result:
            if isinstance(item, dict):
                label = item.get('label', '').lower()
                score = item.get('score', 0.0)
                
                if 'negative' in label:
                    sentiment_scores['negative'] = score
                elif 'positive' in label:
                    sentiment_scores['positive'] = score
                elif 'neutral' in label:
                    sentiment_scores['neutral'] = score
    
    return sentiment_scores

def enhanced_depression_analysis(depression_result, sentiment_scores: Dict, context: Dict) -> Tuple[float, List[str]]:
    """Enhanced depression model analysis with SAFETY-FIRST recalibration"""
    
    max_crisis_score = 0.0
    detected_categories = []
    
    if not depression_result:
        return max_crisis_score, detected_categories
    
    # Extract predictions
    predictions_to_process = []
    if isinstance(depression_result, list):
        if len(depression_result) > 0 and isinstance(depression_result[0], list):
            predictions_to_process = depression_result[0]
        elif len(depression_result) > 0 and isinstance(depression_result[0], dict):
            predictions_to_process = depression_result
        else:
            return max_crisis_score, detected_categories
    elif isinstance(depression_result, dict):
        predictions_to_process = [depression_result]
    else:
        return max_crisis_score, detected_categories
    
    # Extract depression scores
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
    
    # Calculate base depression score - SAFETY FIRST approach
    total_depression = moderate_score + severe_score
    
    # SAFETY-FIRST SCORING: Err on side of caution for potential crises
    if severe_score > 0.02:  # Any severe signal is HIGH
        base_score = 0.70 + (severe_score * 6.0)  # Ensure HIGH threshold
        reason = f"severe_detected ({severe_score:.3f})"
        
    elif moderate_score > 0.60:  # Strong moderate is HIGH
        base_score = 0.65 + (moderate_score * 0.4)  # Ensure HIGH
        reason = f"strong_moderate ({moderate_score:.3f})"
        
    elif moderate_score > 0.35:  # Moderate signal - likely HIGH or high MEDIUM
        base_score = 0.50 + (moderate_score * 0.6)  # Borderline HIGH
        reason = f"moderate_signal ({moderate_score:.3f})"
        
    elif moderate_score > 0.20:  # Mild moderate - MEDIUM range
        base_score = 0.25 + (moderate_score * 0.8)  # MEDIUM range
        reason = f"mild_moderate ({moderate_score:.3f})"
        
    elif total_depression > 0.15:  # Any depression signal - LOW to MEDIUM
        base_score = 0.12 + (total_depression * 0.8)  # LOW range
        reason = f"mild_depression ({total_depression:.3f})"
        
    elif not_depression_score > 0.90:  # Very confident not depression
        base_score = 0.05  # Small residual
        reason = f"confident_not_depression ({not_depression_score:.3f})"
        
    else:  # Weak signals
        base_score = total_depression * 0.6
        reason = f"weak_signals ({total_depression:.3f})"
    
    # CRITICAL PATTERN DETECTION: Patterns that MUST be HIGH
    message_lower = context.get('message_lower', '')
    
    # Burden ideation patterns (often missed by model)
    burden_patterns = [
        'better off without me', 'everyone would be better without me',
        'better off if i was gone', 'better off if i wasn\'t here',
        'nobody would miss me', 'wouldn\'t be missed'
    ]
    
    # Hopelessness patterns that should be HIGH
    hopelessness_patterns = [
        'everything feels pointless', 'life feels pointless',
        'i hate my life', 'hate my life',
        'wish i could disappear', 'want to disappear'
    ]
    
    # Struggle patterns that should be HIGH
    struggle_patterns = [
        'really struggling', 'struggling so much',
        'can\'t take it anymore', 'can\'t go on'
    ]
    
    critical_pattern_found = False
    
    for pattern_list, pattern_name in [
        (burden_patterns, "burden_ideation"),
        (hopelessness_patterns, "severe_hopelessness"),
        (struggle_patterns, "severe_struggle")
    ]:
        for pattern in pattern_list:
            if pattern in message_lower:
                base_score = max(base_score, 0.70)  # Force HIGH threshold
                reason += f" + {pattern_name}_boost"
                critical_pattern_found = True
                break
        if critical_pattern_found:
            break
    
    # Context-based adjustments (more conservative for safety)
    context_adjustment = 0.0
    adjustment_reasons = []
    
    # Only reduce scores for clearly positive contexts
    if context['has_humor_context'] and base_score < 0.35:  # Don't reduce HIGH scores
        context_adjustment -= 0.15
        adjustment_reasons.append("humor_context")
    
    if context['has_work_context'] and base_score < 0.25:  # Don't reduce MEDIUM+ scores
        context_adjustment -= 0.10
        adjustment_reasons.append("work_success_context")
    
    # Sentiment integration (conservative)
    negative_sentiment = sentiment_scores.get('negative', 0.0)
    positive_sentiment = sentiment_scores.get('positive', 0.0)
    
    if negative_sentiment > 0.80 and base_score > 0.15:
        context_adjustment += 0.05  # Small boost for negative sentiment
        adjustment_reasons.append("high_negative_sentiment")
    
    if positive_sentiment > 0.80 and base_score < 0.20:  # Only reduce low scores
        context_adjustment -= 0.10
        adjustment_reasons.append("high_positive_sentiment")
    
    # Apply adjustments
    max_crisis_score = base_score + context_adjustment
    max_crisis_score = max(0.0, min(1.0, max_crisis_score))
    
    if adjustment_reasons:
        logger.info(f"Context adjustments: {adjustment_reasons} -> {base_score:.3f} → {max_crisis_score:.3f}")
    
    logger.info(f"SAFETY-FIRST analysis: {reason} -> final score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories

def advanced_idiom_detection(message: str, context: Dict, base_score: float) -> float:
    """Advanced idiom detection with context verification"""
    message_lower = message.lower().strip()
    
    # Enhanced idiom patterns with stricter context requirements
    idiom_reductions = [
        # Fatigue idioms (only reduce if no other crisis indicators)
        {
            'patterns': [r'\b(dead|dying) (tired|exhausted|beat)\b'],
            'required_context': lambda ctx: not any(word in message_lower for word in ['depressed', 'sad', 'hopeless', 'hate', 'kill myself']),
            'reduction_factor': 0.15,
            'max_score_after': 0.10,
            'name': 'fatigue_idiom'
        },
        
        # Humor idioms (strong reduction if humor context present)
        {
            'patterns': [r'\b(joke|that|it) (killed|murdered) me\b', r'\bdying of laughter\b'],
            'required_context': lambda ctx: ctx['has_humor_context'] or any(word in message_lower for word in ['funny', 'hilarious', 'laugh']),
            'reduction_factor': 0.05,
            'max_score_after': 0.08,
            'name': 'humor_idiom'
        },
        
        # Success idioms
        {
            'patterns': [r'\b(killing|slaying|crushing) it\b'],
            'required_context': lambda ctx: ctx['has_work_context'] or any(word in message_lower for word in ['work', 'job', 'performance']),
            'reduction_factor': 0.10,
            'max_score_after': 0.05,
            'name': 'success_idiom'
        },
        
        # Food craving idioms
        {
            'patterns': [r'\bmurder (a|some) \w+\b', r'\bcould kill for\b'],
            'required_context': lambda ctx: any(word in message_lower for word in ['food', 'hungry', 'eat', 'burger', 'pizza']),
            'reduction_factor': 0.08,
            'max_score_after': 0.05,
            'name': 'food_craving_idiom'
        },
        
        # Frustration idioms (only if clear frustration context)
        {
            'patterns': [r'\bdriving me (crazy|insane|nuts)\b', r'\b(brutal|killer) (test|exam|homework)\b'],
            'required_context': lambda ctx: any(word in message_lower for word in ['traffic', 'homework', 'test', 'exam', 'work']),
            'reduction_factor': 0.12,
            'max_score_after': 0.08,
            'name': 'frustration_idiom'
        }
    ]
    
    for idiom_rule in idiom_reductions:
        for pattern in idiom_rule['patterns']:
            if re.search(pattern, message_lower, re.IGNORECASE):
                if idiom_rule['required_context'](context):
                    reduced_score = base_score * idiom_rule['reduction_factor']
                    final_score = min(reduced_score, idiom_rule['max_score_after'])
                    
                    logger.info(f"ADVANCED IDIOM REDUCTION: {idiom_rule['name']} -> {base_score:.3f} → {final_score:.3f}")
                    return final_score
    
    return base_score

def enhanced_crisis_level_mapping(crisis_score: float) -> str:
    """SAFETY-FIRST crisis level mapping - prioritizes catching HIGH cases"""
    
    # SAFETY-FIRST thresholds: Better to over-classify than miss a crisis
    if crisis_score >= 0.50:    # HIGH: Lowered back for safety
        return 'high'      
    elif crisis_score >= 0.22:  # MEDIUM: Reasonable range
        return 'medium'    
    elif crisis_score >= 0.12:  # LOW: Maintained
        return 'low'       
    else:
        return 'none'            # NONE: 0.00-0.11

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting up...")
    await load_models()
    logger.info("✅ Enhanced FastAPI app startup complete!")
    yield
    # Shutdown
    logger.info("🛑 Enhanced FastAPI app shutting down...")

app = FastAPI(
    title="Enhanced Ash NLP Service", 
    version="4.0",
    description="Multi-model Mental Health Crisis Detection with Advanced Context Analysis",
    lifespan=lifespan
)

@app.post("/analyze", response_model=CrisisResponse)
async def analyze_message(request: MessageRequest):
    """Enhanced message analysis with multi-model approach"""
    
    if not depression_model or not sentiment_model:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    
    start_time = time.time()
    reasoning_steps = []
    
    try:
        # Step 1: Extract context signals
        context = extract_context_signals(request.message)
        reasoning_steps.append(f"Context: {context}")
        
        # Step 2: Run both ML models
        depression_result = depression_model(request.message)
        sentiment_result = sentiment_model(request.message)
        
        # Step 3: Analyze sentiment for context
        sentiment_scores = analyze_sentiment_context(sentiment_result)
        reasoning_steps.append(f"Sentiment: {sentiment_scores}")
        
        # Step 4: Enhanced depression model analysis (no keyword overlay since bot handles that)
        depression_score, depression_categories = enhanced_depression_analysis(
            depression_result, sentiment_scores, context
        )
        reasoning_steps.append(f"Depression model: {depression_score:.3f}")
        
        # Step 5: Apply context adjustments and advanced idiom detection
        adjusted_score = advanced_idiom_detection(request.message, context, depression_score)
        reasoning_steps.append(f"Context-adjusted: {adjusted_score:.3f}")
        
        # Step 6: Final score
        final_score = adjusted_score
        reasoning_steps.append(f"Final score: {final_score:.3f}")
        
        # Step 7: Map to crisis level
        crisis_level = enhanced_crisis_level_mapping(final_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Combine categories (only depression model categories since bot handles keywords)
        all_categories = [cat['category'] for cat in depression_categories if isinstance(cat, dict)]
        
        # Create reasoning summary
        reasoning_summary = " | ".join(reasoning_steps)
        
        # Log results
        message_preview = request.message[:30] + "..." if len(request.message) > 30 else request.message
        logger.info(f"Enhanced Analysis: '{message_preview}' -> {crisis_level.upper()} (score: {final_score:.3f}, {processing_time:.1f}ms)")
        
        return CrisisResponse(
            needs_response=crisis_level != 'none',
            crisis_level=crisis_level,
            confidence_score=final_score,
            detected_categories=all_categories,
            method='enhanced_depression_model_with_context',
            processing_time_ms=processing_time,
            model_info="depression+sentiment+context_analysis",
            reasoning=reasoning_summary
        )
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check"""
    
    uptime = time.time() - startup_time
    
    return HealthResponse(
        status="healthy" if (depression_model and sentiment_model) else "unhealthy",
        model_loaded=depression_model is not None and sentiment_model is not None,
        uptime_seconds=uptime,
        hardware_info={
            "cpu": "Ryzen 7 7700x",
            "gpu": "RTX 3050 (8GB VRAM)",
            "ram": "64GB",
            "inference_device": "CPU",
            "models_loaded": 2
        }
    )

@app.get("/stats")
async def get_enhanced_stats():
    """Get enhanced service statistics"""
    
    uptime = time.time() - startup_time
    
    return {
        "service": "Enhanced Ash NLP Service",
        "version": "4.0",
        "models_loaded": {
            "depression": depression_model is not None,
            "sentiment": sentiment_model is not None
        },
        "uptime_seconds": uptime,
        "enhancements": {
            "dual_model_analysis": "Depression + Sentiment models",
            "advanced_context_detection": "Humor, work, idiom detection",
            "enhanced_depression_scoring": "Context-aware model interpretation", 
            "sentiment_integration": "Positive/negative context weighting",
            "advanced_idiom_filtering": "Context-aware false positive reduction",
            "refined_thresholds": "Data-driven crisis level mapping",
            "bot_keyword_integration": "Relies on bot's keyword detection for safety"
        },
        "expected_performance": {
            "overall_accuracy": "75%+ (vs 61.7% baseline)",
            "high_crisis_detection": "95%+ (with bot's keyword detection)",
            "false_positive_rate": "<8% (vs current 15%)",
            "processing_time": "<80ms average"
        },
        "model_info": {
            "primary": "rafalposwiata/deproberta-large-depression",
            "secondary": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "inference_device": "CPU (Ryzen 7 7700x)"
        }
    }

@app.get("/")
async def root():
    """Enhanced service info"""
    return {
        "service": "Enhanced Ash NLP Mental Health Crisis Detection",
        "version": "4.0",
        "status": "running",
        "description": "Multi-model approach with advanced context analysis and refined scoring",
        "key_improvements": [
            "🧠 Dual model analysis (depression + sentiment)",
            "🎯 Enhanced context-aware model interpretation",
            "🔍 Advanced context analysis (humor, idioms, work)",
            "⚖️ Sentiment-weighted scoring for better accuracy",
            "🎭 Sophisticated idiom filtering with context verification",
            "📊 Refined crisis level thresholds",
            "🤝 Designed to work with bot's keyword detection"
        ],
        "endpoints": {
            "analyze": "POST /analyze - Enhanced crisis analysis",
            "health": "GET /health - System health",
            "stats": "GET /stats - Performance statistics"
        },
        "target_performance": "75%+ accuracy, 95%+ high detection (with bot keywords), <8% false positives"
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Ash NLP Service v4.0")
    logger.info("🧠 Enhanced model approach: Depression + Sentiment + Context")
    logger.info("🤝 Designed to work with bot's keyword detection system")
    logger.info("🎯 Target: 75%+ accuracy, 95%+ high detection, <8% false positives")
    logger.info("🌐 Starting server on 0.0.0.0:8881")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8881,
            log_level="info",
            reload=False,
            workers=1
        )
    except Exception as e:
        logger.error(f"❌ Failed to start enhanced server: {e}")
        raise