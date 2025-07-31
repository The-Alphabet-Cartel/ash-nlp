"""
Ensemble Analysis Endpoint for Three-Model Architecture
Provides comprehensive analysis with gap detection and consensus building
"""

import logging
import time
from fastapi import HTTPException
from typing import Dict, Any, List
from models.pydantic_models import MessageRequest, CrisisResponse

logger = logging.getLogger(__name__)

def add_ensemble_endpoints(app, model_manager):
    """Add ensemble analysis endpoints to the FastAPI app"""
    
    @app.post("/analyze_ensemble")
    async def analyze_message_with_ensemble(request: MessageRequest) -> Dict[str, Any]:
        """
        Comprehensive ensemble analysis using all three models
        Includes gap detection and consensus building
        """
        start_time = time.time()
        
        try:
            if not model_manager.models_loaded():
                raise HTTPException(status_code=503, detail="Models not loaded")
            
            message = request.message.strip()
            if not message:
                raise HTTPException(status_code=400, detail="Empty message")
            
            # Perform ensemble analysis
            ensemble_result = model_manager.analyze_with_ensemble(message)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            # Build comprehensive response
            response = {
                "message_analyzed": message,
                "user_id": request.user_id,
                "channel_id": request.channel_id,
                "ensemble_analysis": ensemble_result,
                "processing_time_ms": processing_time,
                "model_info": "three_model_ensemble",
                "timestamp": time.time()
            }
            
            # Add gap detection summary
            if ensemble_result.get('gaps_detected'):
                response['requires_staff_review'] = True
                response['gap_summary'] = _summarize_gaps(ensemble_result.get('gap_details', []))
            else:
                response['requires_staff_review'] = False
            
            # Add consensus information
            consensus = ensemble_result.get('consensus')
            if consensus:
                response['consensus_prediction'] = consensus['prediction']
                response['consensus_confidence'] = consensus['confidence']
                response['consensus_method'] = consensus['method']
                
                # Map to traditional crisis levels for compatibility
                response['crisis_level'] = _map_to_crisis_level(consensus)
                response['needs_response'] = _determine_response_need(consensus)
            
            return response
            
        except Exception as e:
            logger.error(f"Ensemble analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Ensemble analysis error: {str(e)}")
    
    @app.post("/analyze")
    async def analyze_message_legacy(request: MessageRequest) -> CrisisResponse:
        """
        Legacy analysis endpoint - now uses ensemble but returns compatible format
        """
        start_time = time.time()
        
        try:
            if not model_manager.models_loaded():
                raise HTTPException(status_code=503, detail="Models not loaded")
            
            message = request.message.strip()
            if not message:
                raise HTTPException(status_code=400, detail="Empty message")
            
            # Use ensemble analysis but format as legacy response
            ensemble_result = model_manager.analyze_with_ensemble(message)
            consensus = ensemble_result.get('consensus')
            
            processing_time = (time.time() - start_time) * 1000
            
            # Build legacy-compatible response
            if consensus:
                crisis_level = _map_to_crisis_level(consensus)
                needs_response = _determine_response_need(consensus)
                confidence = consensus['confidence']
                method = f"ensemble_{consensus['method']}"
                
                # Extract detected categories from individual models
                detected_categories = _extract_categories(ensemble_result)
                
                # Add reasoning if gaps detected
                reasoning = None
                if ensemble_result.get('gaps_detected'):
                    reasoning = f"Model disagreement detected: {len(ensemble_result.get('gap_details', []))} gaps found"
                
            else:
                # Fallback values
                crisis_level = "none"
                needs_response = False
                confidence = 0.0
                method = "ensemble_error"
                detected_categories = []
                reasoning = "Ensemble analysis failed"
            
            return CrisisResponse(
                needs_response=needs_response,
                crisis_level=crisis_level,
                confidence_score=confidence,
                detected_categories=detected_categories,
                method=method,
                processing_time_ms=processing_time,
                model_info="three_model_ensemble",
                reasoning=reasoning,
                analysis=ensemble_result  # Include full ensemble details
            )
            
        except Exception as e:
            logger.error(f"Legacy analysis failed: {e}")
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

def _summarize_gaps(gap_details: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize detected gaps for staff review"""
    summary = {
        "total_gaps": len(gap_details),
        "gap_types": {},
        "requires_immediate_attention": False
    }
    
    for gap in gap_details:
        gap_type = gap.get('type', 'unknown')
        if gap_type not in summary['gap_types']:
            summary['gap_types'][gap_type] = 0
        summary['gap_types'][gap_type] += 1
        
        # Flag for immediate attention if high confidence disagreement
        if gap_type == 'confidence_disagreement' and gap.get('spread', 0) > 0.7:
            summary['requires_immediate_attention'] = True
    
    return summary

def _map_to_crisis_level(consensus: Dict[str, Any]) -> str:
    """Enhanced mapping for swapped models with zero-shot depression detection"""
    prediction = consensus.get('prediction', 'unknown').lower()
    confidence = consensus.get('confidence', 0.0)
    
    # Handle depression model predictions (zero-shot) - MOST IMPORTANT
    if prediction == 'severe':
        return 'high'  # Severe depression is always high crisis
    elif prediction == 'moderate':
        if confidence >= 0.7:
            return 'high'
        elif confidence >= 0.5:
            return 'medium'
        else:
            return 'low'
    elif prediction == 'mild':
        if confidence >= 0.8:
            return 'medium'  # High confidence mild can be medium
        else:
            return 'low'
    elif prediction == 'not depression':
        return 'none'
    
    # Handle emotion model predictions (sentiment context)
    elif prediction in ['sadness', 'fear']:
        if confidence >= 0.8:
            return 'medium'  # Emotions are contextual, not primary
        elif confidence >= 0.6:
            return 'low'
        else:
            return 'none'
    elif prediction == 'anger':
        if confidence >= 0.8:
            return 'low'  # Anger less predictive than sadness/fear
        else:
            return 'none'
    elif prediction in ['joy', 'love', 'surprise']:
        return 'none'
    
    # Handle normalized predictions from ensemble
    elif prediction == 'crisis':
        if confidence >= 0.8:
            return 'high'
        elif confidence >= 0.6:
            return 'medium'
        else:
            return 'low'
    elif prediction == 'mild_crisis':
        return 'low'
    elif prediction == 'safe':
        return 'none'
    
    # Keep existing mappings for other predictions
    elif prediction in ['negative'] and confidence > 0.8:
        return 'medium'
    elif prediction in ['negative'] and confidence > 0.6:
        return 'low'
    elif prediction in ['positive']:
        return 'none'
    
    # Default fallback
    else:
        return 'none'

def _determine_response_need(consensus: Dict[str, Any]) -> bool:
    """Determine if crisis response is needed based on consensus"""
    crisis_level = _map_to_crisis_level(consensus)
    return crisis_level in ['medium', 'high']

def _extract_categories(ensemble_result: Dict[str, Any]) -> List[str]:
    """Extract detected categories from ensemble analysis"""
    categories = []
    
    # Extract from individual model results
    individual_results = ensemble_result.get('individual_results', {})
    
    for model_name, results in individual_results.items():
        for result in results:
            label = result.get('label', '').lower()
            if label in ['severe', 'negative', 'moderate'] and label not in categories:
                categories.append(f"{model_name}_{label}")
    
    # Add ensemble-specific categories
    if ensemble_result.get('gaps_detected'):
        categories.append('model_disagreement')
    
    consensus = ensemble_result.get('consensus', {})
    if consensus.get('method') == 'unanimous_consensus':
        categories.append('unanimous_consensus')
    
    return categories

logger.info("🎯 Ensemble analysis endpoints defined (three-model architecture)")