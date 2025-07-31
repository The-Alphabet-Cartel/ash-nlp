# UPDATED ensemble_endpoints.py - Clean endpoint structure

"""
Ensemble Analysis Endpoint for Three-Model Architecture
Provides comprehensive analysis with gap detection and consensus building
UPDATED: /analyze_ensemble renamed to /analyze (primary endpoint)
"""

import logging
import time
from fastapi import HTTPException
from typing import Dict, Any, List
from models.pydantic_models import MessageRequest, CrisisResponse

logger = logging.getLogger(__name__)

def add_ensemble_endpoints(app, model_manager):
    """Add ensemble analysis endpoints to the FastAPI app"""
    
    @app.post("/analyze", response_model=CrisisResponse)
    async def analyze_message(request: MessageRequest) -> CrisisResponse:
        """
        PRIMARY ENDPOINT: Three-model ensemble analysis with crisis detection
        RENAMED from /analyze_ensemble - this is now the main analysis endpoint
        """
        start_time = time.time()
        
        try:
            if not model_manager.models_loaded():
                raise HTTPException(status_code=503, detail="Models not loaded")
            
            message = request.message.strip()
            if not message:
                raise HTTPException(status_code=400, detail="Empty message")
            
            logger.info(f"🔍 Three-model ensemble analysis: '{message[:50]}...'")
            
            # Perform ensemble analysis
            ensemble_result = model_manager.analyze_with_ensemble(message)
            
            # Extract consensus information
            consensus = ensemble_result.get('consensus')
            if not consensus:
                raise HTTPException(status_code=500, detail="Ensemble analysis failed to produce consensus")
            
            consensus_prediction = consensus['prediction']
            consensus_confidence = consensus['confidence']
            consensus_method = consensus['method']
            
            # FIXED: Map consensus to crisis level using corrected logic
            crisis_level = _map_to_crisis_level(consensus)
            needs_response = _determine_response_need(consensus)
            
            # Extract detected categories from individual models
            detected_categories = _extract_categories(ensemble_result)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            # Determine if staff review is required
            requires_staff_review = _requires_staff_review(crisis_level, consensus_confidence, ensemble_result)
            
            # Build comprehensive response in CrisisResponse format
            result = CrisisResponse(
                needs_response=needs_response,
                crisis_level=crisis_level,
                confidence_score=consensus_confidence,
                detected_categories=detected_categories,
                method=f"three_model_ensemble_{consensus_method}",
                processing_time_ms=processing_time,
                model_info="three_model_ensemble",
                reasoning=f"Ensemble consensus: {consensus_prediction} (confidence: {consensus_confidence:.3f}, method: {consensus_method})",
                analysis={
                    # Core ensemble data
                    "ensemble_analysis": ensemble_result,
                    "consensus_prediction": consensus_prediction,
                    "consensus_confidence": consensus_confidence,
                    "consensus_method": consensus_method,
                    
                    # Individual model results
                    "individual_results": ensemble_result.get('individual_results', {}),
                    
                    # Gap detection
                    "gaps_detected": ensemble_result.get('gaps_detected', False),
                    "gap_details": ensemble_result.get('gap_details', []),
                    "requires_staff_review": requires_staff_review,
                    
                    # Request metadata
                    "message_analyzed": message,
                    "user_id": request.user_id,
                    "channel_id": request.channel_id,
                    "timestamp": time.time()
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
            
            # Add ensemble-specific health checks
            ensemble_health = {
                "ensemble_status": "healthy" if status['models_loaded'] else "unhealthy",
                "individual_models": status['models'],
                "ensemble_mode": status['ensemble_mode'],
                "gap_detection": status['gap_detection'],
                "device": status['device'],
                "precision": status['precision'],
                "timestamp": time.time()
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
    
    @app.get("/gap_analysis")
    async def get_recent_gaps() -> Dict[str, Any]:
        """Analyze recent model disagreements and gaps"""
        try:
            # This would typically load from a gap tracking system
            # For now, return structure for implementation
            
            return {
                "gap_analysis_available": False,
                "message": "Gap tracking system not yet implemented",
                "suggested_implementation": {
                    "store_disagreements": "Log all model disagreements to database",
                    "track_patterns": "Identify common disagreement patterns",
                    "staff_feedback": "Integrate with staff correction commands",
                    "learning_integration": "Feed gaps back into learning system"
                },
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Gap analysis error: {str(e)}")
    
    @app.get("/confidence_distribution")
    async def get_confidence_distribution() -> Dict[str, Any]:
        """Analyze confidence patterns across models"""
        try:
            # This would typically analyze historical confidence data
            # For now, return structure for implementation
            
            return {
                "confidence_analysis_available": False,
                "message": "Confidence tracking system not yet implemented", 
                "suggested_metrics": {
                    "average_confidence_by_model": "Track average confidence per model",
                    "confidence_spread_patterns": "Identify high-spread scenarios",
                    "consensus_success_rate": "Track consensus prediction accuracy",
                    "disagreement_frequency": "Monitor model disagreement rates"
                },
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Confidence analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Confidence analysis error: {str(e)}")

def _map_to_crisis_level(consensus: Dict[str, Any]) -> str:
    """
    FIXED: Map ensemble consensus to crisis levels using NORMALIZED predictions
    This handles the actual ensemble output: 'crisis', 'mild_crisis', 'safe', etc.
    """
    prediction = consensus.get('prediction', 'unknown').lower().strip()
    confidence = consensus.get('confidence', 0.0)
    
    logger.info(f"🎯 Mapping consensus: prediction='{prediction}' confidence={confidence:.3f}")
    
    # Handle NORMALIZED predictions from three-model ensemble
    if prediction == 'crisis':
        if confidence >= 0.70:
            result = 'high'      # High confidence crisis
        elif confidence >= 0.45:
            result = 'medium'    # Medium confidence crisis  
        else:
            result = 'low'       # Low confidence crisis, but still crisis
        
        logger.info(f"🚨 CRISIS consensus: {prediction} @ {confidence:.3f} -> {result}")
        return result
    
    elif prediction == 'mild_crisis':
        if confidence >= 0.60:
            result = 'low'       # Mild crisis with good confidence
        else:
            result = 'none'      # Very uncertain mild crisis
        
        logger.info(f"⚠️ MILD_CRISIS consensus: {prediction} @ {confidence:.3f} -> {result}")
        return result
    
    elif prediction in ['safe', 'neutral', 'positive']:
        logger.info(f"✅ SAFE consensus: {prediction} @ {confidence:.3f} -> none")
        return 'none'
    
    elif prediction in ['negative', 'mild_negative']:
        if confidence >= 0.80:  # Very confident negative sentiment
            result = 'low'        # Might need monitoring
        else:
            result = 'none'
        
        logger.info(f"➖ NEGATIVE consensus: {prediction} @ {confidence:.3f} -> {result}")
        return result
    
    # Fallback for unknown predictions - be conservative
    else:
        logger.warning(f"❓ Unknown consensus prediction: '{prediction}' with confidence {confidence:.3f}")
        if confidence > 0.60:  # If we're confident but don't know what it means, be safe
            result = 'low'
        else:
            result = 'none'
        
        logger.info(f"🤷 UNKNOWN consensus: {prediction} @ {confidence:.3f} -> {result} (conservative fallback)")
        return result

def _determine_response_need(consensus: Dict[str, Any]) -> bool:
    """
    FIXED: Determine if crisis response is needed based on PROPER crisis level mapping
    """
    crisis_level = _map_to_crisis_level(consensus)
    needs_response = crisis_level in ['low', 'medium', 'high']  # ANY crisis level needs response
    
    logger.info(f"📋 Response determination: crisis_level='{crisis_level}' -> needs_response={needs_response}")
    return needs_response

def _requires_staff_review(crisis_level: str, confidence: float, ensemble_result: Dict[str, Any]) -> bool:
    """Determine if staff review is required"""
    # High crisis always requires review
    if crisis_level == 'high':
        return True
    
    # Medium crisis with good confidence requires review
    if crisis_level == 'medium' and confidence >= 0.60:
        return True
    
    # Low crisis with very high confidence might need review
    if crisis_level == 'low' and confidence >= 0.80:
        return True
    
    # Any model disagreement requires review
    if ensemble_result.get('gaps_detected', False):
        return True
    
    return False

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

logger.info("🎯 Ensemble analysis endpoints configured - /analyze is now the primary three-model endpoint")