# CENTRALIZED ensemble_endpoints.py - ALL thresholds from environment

"""
Ensemble Analysis Endpoint for Three-Model Architecture
CENTRALIZED: All thresholds read from environment variables - NO hard-coded values
"""

import logging
import time
from fastapi import HTTPException
from typing import Dict, Any, List
from models.pydantic_models import MessageRequest, CrisisResponse
from config.env_manager import get_config

logger = logging.getLogger(__name__)
config = get_config()

def add_ensemble_endpoints(app, model_manager):
    """Add ensemble analysis endpoints to the FastAPI app"""
    
    @app.post("/analyze", response_model=CrisisResponse)
    async def analyze_message(request: MessageRequest) -> CrisisResponse:
        """PRIMARY ENDPOINT: Three Zero-Shot Model Ensemble analysis with crisis detection"""
        start_time = time.time()
        
        try:
            if not model_manager.models_loaded():
                raise HTTPException(status_code=503, detail="Models not loaded")
            
            message = request.message.strip()
            if not message:
                raise HTTPException(status_code=400, detail="Empty message")
            
            logger.info(f"🔍 Three Zero-Shot Model Ensemble analysis: '{message[:50]}...'")
            
            # Perform ensemble analysis
            ensemble_result = model_manager.analyze_with_ensemble(message)
            
            # Extract consensus information
            consensus = ensemble_result.get('consensus')
            if not consensus:
                raise HTTPException(status_code=500, detail="Ensemble analysis failed to produce consensus")
            
            consensus_prediction = consensus['prediction']
            consensus_confidence = consensus['confidence']
            consensus_method = consensus['method']
            
            # CENTRALIZED: Use environment-driven crisis level mapping
            crisis_level = _map_to_crisis_level_centralized(consensus)
            needs_response = _determine_response_need_centralized(consensus)
            
            # Extract detected categories from individual models
            detected_categories = _extract_categories(ensemble_result)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            # CENTRALIZED: Determine staff review using environment thresholds
            requires_staff_review = _requires_staff_review_centralized(crisis_level, consensus_confidence, ensemble_result)
            
            # Build comprehensive response
            result = CrisisResponse(
                needs_response=needs_response,
                crisis_level=crisis_level,
                confidence_score=consensus_confidence,
                detected_categories=detected_categories,
                method=f"three_model_ensemble_{consensus_method}_centralized",
                processing_time_ms=processing_time,
                model_info="three_model_ensemble_centralized_thresholds",
                reasoning=f"Ensemble consensus: {consensus_prediction} (confidence: {consensus_confidence:.3f}, method: {consensus_method})",
                analysis={
                    "ensemble_analysis": ensemble_result,
                    "consensus_prediction": consensus_prediction,
                    "consensus_confidence": consensus_confidence,
                    "consensus_method": consensus_method,
                    "individual_results": ensemble_result.get('individual_results', {}),
                    "gaps_detected": ensemble_result.get('gaps_detected', False),
                    "gap_details": ensemble_result.get('gap_details', []),
                    "requires_staff_review": requires_staff_review,
                    "message_analyzed": message,
                    "user_id": request.user_id,
                    "channel_id": request.channel_id,
                    "timestamp": time.time(),
                    "thresholds_used": _get_all_thresholds_from_environment()
                }
            )
            
            logger.info(f"✅ Ensemble analysis complete: {crisis_level} (consensus: {consensus_prediction} @ {consensus_confidence:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ensemble analysis failed: {e}")
            logger.exception("Full traceback:")
            raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    @app.get("/ensemble_health")
    async def get_ensemble_health() -> Dict[str, Any]:
        """Get health status of all three models in the ensemble"""
        try:
            status = model_manager.get_model_status()
            
            ensemble_health = {
                "ensemble_status": "healthy" if status['models_loaded'] else "unhealthy",
                "individual_models": status['models'],
                "ensemble_mode": status['ensemble_mode'],
                "gap_detection": status['gap_detection'],
                "device": status['device'],
                "precision": status['precision'],
                "timestamp": time.time(),
                "centralized_thresholds": _get_all_thresholds_from_environment()
            }
            
            # Check each model individually
            for model_name, model_info in status['models'].items():
                if not model_info['loaded']:
                    ensemble_health['ensemble_status'] = "degraded"
                    ensemble_health['degraded_reason'] = f"{model_name} model not loaded"
            
            return ensemble_health
            
        except Exception as e:
            logger.error(f"Ensemble health check failed: {e}")
            raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")
    
    @app.get("/threshold_status")
    async def get_threshold_status() -> Dict[str, Any]:
        """Get current threshold configuration for debugging and tuning"""
        try:
            return {
                "threshold_source": "environment_variables",
                "centralized_management": True,
                "all_thresholds": _get_all_thresholds_from_environment(),
                "threshold_validation": _validate_threshold_consistency(),
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Threshold status check failed: {e}")
            raise HTTPException(status_code=500, detail=f"Threshold status error: {str(e)}")

def _get_all_thresholds_from_environment() -> Dict[str, float]:
    """Get ALL thresholds from environment variables - centralized access point"""
    return {
        # Consensus prediction mapping thresholds (PRIMARY)
        'consensus_crisis_to_high': config.get('NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD', 0.50),
        'consensus_crisis_to_medium': config.get('NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD', 0.30),
        'consensus_mild_crisis_to_low': config.get('NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD', 0.40),
        'consensus_negative_to_low': config.get('NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD', 0.70),
        'consensus_unknown_to_low': config.get('NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD', 0.50),
        
        # Staff review thresholds
        'staff_review_medium_confidence': config.get('NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD', 0.45),
        'staff_review_low_confidence': config.get('NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD', 0.75),
        
        # Safety controls
        'consensus_safety_bias': config.get('NLP_CONSENSUS_SAFETY_BIAS', 0.03),
        
        # Gap detection
        'gap_detection_threshold': config.get('NLP_GAP_DETECTION_THRESHOLD', 0.25),
        'disagreement_threshold': config.get('NLP_DISAGREEMENT_THRESHOLD', 0.35),
        
        # Legacy ensemble thresholds (for compatibility)
        'ensemble_high': config.get('NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD', 0.45),
        'ensemble_medium': config.get('NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD', 0.25),
        'ensemble_low': config.get('NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD', 0.12),
        
        # Individual model thresholds (for backward compatibility)
        'individual_high': config.get('NLP_HIGH_CRISIS_THRESHOLD', 0.45),
        'individual_medium': config.get('NLP_MEDIUM_CRISIS_THRESHOLD', 0.25),
        'individual_low': config.get('NLP_LOW_CRISIS_THRESHOLD', 0.15),
    }

def _map_to_crisis_level_centralized(consensus: Dict[str, Any]) -> str:
    """
    CENTRALIZED: Map ensemble consensus to crisis levels using ONLY environment thresholds
    NO hard-coded values - all thresholds from .env file
    """
    prediction = consensus.get('prediction', 'unknown').lower().strip()
    confidence = consensus.get('confidence', 0.0)
    
    # Get all thresholds from environment
    thresholds = _get_all_thresholds_from_environment()
    
    logger.info(f"🎯 Centralized mapping: prediction='{prediction}' confidence={confidence:.3f}")
    
    # Handle NORMALIZED predictions from Three Zero-Shot Model Ensemble
    if prediction == 'crisis':
        # Use environment thresholds for crisis prediction mapping
        if confidence >= thresholds['consensus_crisis_to_high']:
            result = 'high'
        elif confidence >= thresholds['consensus_crisis_to_medium']:
            result = 'medium'
        else:
            result = 'low'  # Any crisis prediction gets at least low
        
        logger.info(f"🚨 CRISIS consensus: {prediction} @ {confidence:.3f} -> {result} "
                   f"(thresholds: high={thresholds['consensus_crisis_to_high']}, "
                   f"medium={thresholds['consensus_crisis_to_medium']})")
        return result
    
    elif prediction == 'mild_crisis':
        # Use environment threshold for mild crisis mapping
        if confidence >= thresholds['consensus_mild_crisis_to_low']:
            result = 'low'
        else:
            result = 'none'
        
        logger.info(f"⚠️ MILD_CRISIS consensus: {prediction} @ {confidence:.3f} -> {result} "
                   f"(threshold: {thresholds['consensus_mild_crisis_to_low']})")
        return result
    
    elif prediction in ['safe', 'neutral', 'positive']:
        logger.info(f"✅ SAFE consensus: {prediction} @ {confidence:.3f} -> none")
        return 'none'
    
    elif prediction in ['negative', 'mild_negative']:
        # Use environment threshold for negative sentiment mapping
        if confidence >= thresholds['consensus_negative_to_low']:
            result = 'low'
        else:
            result = 'none'
        
        logger.info(f"➖ NEGATIVE consensus: {prediction} @ {confidence:.3f} -> {result} "
                   f"(threshold: {thresholds['consensus_negative_to_low']})")
        return result
    
    # Fallback for unknown predictions - use environment threshold
    else:
        logger.warning(f"❓ Unknown consensus prediction: '{prediction}' with confidence {confidence:.3f}")
        if confidence > thresholds['consensus_unknown_to_low']:
            result = 'low'
        else:
            result = 'none'
        
        logger.info(f"🤷 UNKNOWN consensus: {prediction} @ {confidence:.3f} -> {result} "
                   f"(threshold: {thresholds['consensus_unknown_to_low']})")
        return result

def _determine_response_need_centralized(consensus: Dict[str, Any]) -> bool:
    """
    CENTRALIZED: Determine if crisis response is needed based on environment-driven crisis level
    """
    crisis_level = _map_to_crisis_level_centralized(consensus)
    needs_response = crisis_level in ['low', 'medium', 'high']  # ANY crisis level needs response
    
    logger.info(f"📋 Response determination: crisis_level='{crisis_level}' -> needs_response={needs_response}")
    return needs_response

def _requires_staff_review_centralized(crisis_level: str, confidence: float, ensemble_result: Dict[str, Any]) -> bool:
    """CENTRALIZED: Determine staff review using ONLY environment thresholds"""
    thresholds = _get_all_thresholds_from_environment()
    
    # High crisis always requires review (configurable in future if needed)
    if crisis_level == 'high':
        return True
    
    # Medium crisis with sufficient confidence requires review
    if crisis_level == 'medium' and confidence >= thresholds['staff_review_medium_confidence']:
        return True
    
    # Low crisis with very high confidence might need review
    if crisis_level == 'low' and confidence >= thresholds['staff_review_low_confidence']:
        return True
    
    # Model disagreement requires review (configurable)
    if ensemble_result.get('gaps_detected', False):
        return config.get('NLP_STAFF_REVIEW_ON_MODEL_DISAGREEMENT', True)
    
    return False

def _validate_threshold_consistency() -> Dict[str, Any]:
    """Validate that thresholds are logically consistent"""
    thresholds = _get_all_thresholds_from_environment()
    issues = []
    
    # Check consensus thresholds are ordered correctly
    if thresholds['consensus_crisis_to_high'] <= thresholds['consensus_crisis_to_medium']:
        issues.append("consensus_crisis_to_high should be > consensus_crisis_to_medium")
    
    # Check staff review thresholds are reasonable
    if thresholds['staff_review_medium_confidence'] > 1.0:
        issues.append("staff_review_medium_confidence should be <= 1.0")
    
    # Check safety bias is reasonable
    if thresholds['consensus_safety_bias'] > 0.1:
        issues.append("consensus_safety_bias seems high (>0.1)")
    
    return {
        "consistent": len(issues) == 0,
        "issues": issues,
        "recommendations": [
            "Ensure high thresholds > medium thresholds > low thresholds",
            "Keep safety bias small (0.01-0.05)",
            "Staff review thresholds should be reasonable (0.4-0.8)"
        ]
    }

def _extract_categories(ensemble_result: Dict[str, Any]) -> List[str]:
    """Extract detected categories from ensemble analysis"""
    categories = []
    
    # Extract from individual model results
    individual_results = ensemble_result.get('individual_results', {})
    
    for model_name, results in individual_results.items():
        if results and isinstance(results, list) and len(results) > 0:
            top_result = max(results, key=lambda x: x.get('score', 0))
            label = top_result.get('label', '').lower()
            if label in ['severe', 'moderate', 'negative', 'high distress', 'medium distress']:
                categories.append(f"{model_name}_{label}")
    
    # Add ensemble-specific categories
    if ensemble_result.get('gaps_detected'):
        categories.append('model_disagreement')
    
    consensus = ensemble_result.get('consensus', {})
    if consensus.get('method') == 'unanimous_consensus':
        categories.append('unanimous_consensus')
    elif consensus.get('method') == 'weighted_ensemble':
        categories.append('weighted_consensus')
    
    return categories

logger.info("🎯 CENTRALIZED Ensemble endpoints configured - All thresholds from environment variables")