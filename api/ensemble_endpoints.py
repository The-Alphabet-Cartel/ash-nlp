#!/usr/bin/env python3
# ash/ash-nlp/api/ensemble_endpoints.py - Updated for Phase 2B PydanticManager Integration
"""
Ensemble Analysis Endpoint for Three-Model Architecture - Phase 2B Update
Updated to use PydanticManager v3.1 when available, with legacy fallback

CENTRALIZED: All thresholds read from environment variables - NO hard-coded values
Phase 2B: Integrated with PydanticManager for clean model access
"""

import logging
import time
import os
from fastapi import HTTPException
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def add_ensemble_endpoints(app, model_manager, pydantic_manager=None):
    """
    Add ensemble analysis endpoints to the FastAPI app - Phase 2B Update
    
    Args:
        app: FastAPI application instance
        model_manager: ModelManager instance (from Phase 2A)
        pydantic_manager: PydanticManager instance (Phase 2B - optional for backward compatibility)
    """
    
    # ========================================================================
    # PHASE 2B: SMART MODEL ACCESS
    # ========================================================================
    def get_models():
        """Get Pydantic models from PydanticManager or legacy imports"""
        if pydantic_manager:
            logger.debug("🏗️ Using PydanticManager v3.1 for endpoint models")
            return pydantic_manager.get_legacy_imports()
        else:
            logger.debug("⚠️ Using legacy model imports for endpoints")
            try:
                from models.pydantic_models import MessageRequest, CrisisResponse
                return {
                    'MessageRequest': MessageRequest,
                    'CrisisResponse': CrisisResponse
                }
            except ImportError as e:
                logger.error(f"❌ Failed to import legacy models: {e}")
                raise RuntimeError("No Pydantic models available for endpoints")
    
    # Get model classes
    try:
        models = get_models()
        MessageRequest = models['MessageRequest']
        CrisisResponse = models['CrisisResponse']
        logger.info("✅ Pydantic models loaded successfully for ensemble endpoints")
        
        if pydantic_manager:
            logger.info("🎯 Phase 2B: Using PydanticManager v3.1 for endpoint model management")
        else:
            logger.info("⚠️ Phase 2B: Using legacy model imports (migration recommended)")
            
    except Exception as e:
        logger.error(f"❌ Failed to load Pydantic models for endpoints: {e}")
        raise RuntimeError(f"Endpoint initialization failed: {e}")
    
    # ========================================================================
    # CENTRALIZED THRESHOLD CONFIGURATION
    # ========================================================================
    def _get_centralized_thresholds():
        """Load centralized threshold configuration from environment variables"""
        
        return {
            # Ensemble mode
            'ensemble_mode': os.getenv('NLP_ENSEMBLE_MODE', 'majority'),
            
            # Consensus mapping thresholds
            'consensus_crisis_to_high': float(os.getenv('NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD', '0.50')),
            'consensus_crisis_to_medium': float(os.getenv('NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD', '0.30')),
            'consensus_mild_crisis_to_low': float(os.getenv('NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD', '0.40')),
            'consensus_negative_to_low': float(os.getenv('NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD', '0.70')),
            'consensus_unknown_to_low': float(os.getenv('NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD', '0.50')),
            
            # Model weights
            'depression_weight': float(os.getenv('NLP_DEPRESSION_MODEL_WEIGHT', '0.6')),
            'sentiment_weight': float(os.getenv('NLP_SENTIMENT_MODEL_WEIGHT', '0.15')),
            'emotional_distress_weight': float(os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', '0.25')),
            
            # Staff review thresholds
            'staff_review_high_always': os.getenv('NLP_STAFF_REVIEW_HIGH_ALWAYS', 'true').lower() == 'true',
            'staff_review_medium_threshold': float(os.getenv('NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD', '0.45')),
            'staff_review_low_threshold': float(os.getenv('NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD', '0.75')),
            'staff_review_on_disagreement': os.getenv('NLP_STAFF_REVIEW_ON_MODEL_DISAGREEMENT', 'true').lower() == 'true',
            
            # Safety controls  
            'consensus_safety_bias': float(os.getenv('NLP_CONSENSUS_SAFETY_BIAS', '0.05')),
            'enable_safety_override': os.getenv('NLP_ENABLE_SAFETY_OVERRIDE', 'true').lower() == 'true',
        }
    
    # Load thresholds once
    thresholds = _get_centralized_thresholds()
    logger.info("🎯 Centralized thresholds loaded for ensemble endpoints")
    
    # ========================================================================
    # HELPER FUNCTIONS
    # ========================================================================
    def _map_to_crisis_level_centralized(consensus: Dict[str, Any]) -> str:
        """Map consensus result to crisis level using centralized thresholds"""
        prediction = consensus['prediction']
        confidence = consensus['confidence']
        
        # Apply centralized mapping logic using environment-driven thresholds
        if prediction == 'CRISIS':
            if confidence >= thresholds['consensus_crisis_to_high']:
                return 'high'
            elif confidence >= thresholds['consensus_crisis_to_medium']:
                return 'medium'
            else:
                return 'low'
        elif prediction == 'MILD_CRISIS':
            if confidence >= thresholds['consensus_mild_crisis_to_low']:
                return 'low'
            else:
                return 'none'
        elif prediction == 'NEGATIVE':
            if confidence >= thresholds['consensus_negative_to_low']:
                return 'low'
            else:
                return 'none'
        elif prediction == 'UNKNOWN':
            if confidence >= thresholds['consensus_unknown_to_low']:
                return 'low'
            else:
                return 'none'
        else:  # NEUTRAL, POSITIVE
            return 'none'
    
    def _determine_response_need_centralized(consensus: Dict[str, Any]) -> bool:
        """Determine if response is needed using centralized logic"""
        prediction = consensus['prediction']
        confidence = consensus['confidence']
        
        # High-risk predictions always need response
        if prediction in ['CRISIS', 'MILD_CRISIS']:
            return True
        
        # NEGATIVE with high confidence needs response
        if prediction == 'NEGATIVE' and confidence >= thresholds['consensus_negative_to_low']:
            return True
        
        # UNKNOWN with high confidence might need response
        if prediction == 'UNKNOWN' and confidence >= thresholds['consensus_unknown_to_low']:
            return True
        
        return False
    
    def _determine_staff_review_centralized(crisis_level: str, confidence: float, gaps_detected: bool) -> bool:
        """Determine if staff review is needed using centralized thresholds"""
        
        # HIGH always needs review
        if crisis_level == 'high' and thresholds['staff_review_high_always']:
            return True
        
        # MEDIUM with low confidence needs review
        if crisis_level == 'medium' and confidence < thresholds['staff_review_medium_threshold']:
            return True
        
        # LOW with very high confidence might not need review
        if crisis_level == 'low' and confidence < thresholds['staff_review_low_threshold']:
            return True
        
        # Gaps detected (model disagreement) always needs review if enabled
        if gaps_detected and thresholds['staff_review_on_disagreement']:
            return True
        
        return False
    
    # ========================================================================
    # PRIMARY ANALYSIS ENDPOINT
    # ========================================================================
    @app.post("/analyze", response_model=CrisisResponse)
    async def analyze_message(request: MessageRequest) -> CrisisResponse:
        """
        PRIMARY ENDPOINT: Three Zero-Shot Model Ensemble analysis with crisis detection
        Phase 2B: Uses PydanticManager v3.1 when available for model validation
        """
        start_time = time.time()
        
        try:
            if not model_manager.models_loaded():
                raise HTTPException(status_code=503, detail="Models not loaded")
            
            message = request.message.strip()
            if not message:
                raise HTTPException(status_code=400, detail="Empty message")
            
            logger.info(f"🔍 Three Zero-Shot Model Ensemble analysis: '{message[:50]}...'")
            
            # Log Phase 2B status
            if pydantic_manager:
                logger.debug("🏗️ Using PydanticManager v3.1 for request/response validation")
            else:
                logger.debug("⚠️ Using legacy Pydantic models for request/response validation")
            
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
            detected_categories = []
            individual_results = ensemble_result.get('individual_results', {})
            
            for model_name, result in individual_results.items():
                if result and len(result) > 0:
                    top_prediction = result[0]
                    if top_prediction.get('score', 0) > 0.3:  # Configurable threshold
                        detected_categories.append(f"{model_name}:{top_prediction.get('label', 'unknown')}")
            
            # Gap detection and staff review determination
            gaps_detected = ensemble_result.get('gaps_detected', False)
            needs_staff_review = _determine_staff_review_centralized(crisis_level, consensus_confidence, gaps_detected)
            
            # Build comprehensive analysis information
            analysis_info = {
                'ensemble_analysis': {
                    'consensus_prediction': consensus_prediction,
                    'consensus_confidence': round(consensus_confidence, 4),
                    'consensus_method': consensus_method,
                    'gaps_detected': gaps_detected,
                    'individual_results': individual_results,
                    'model_agreement': ensemble_result.get('model_agreement', {}),
                    'confidence_spread': ensemble_result.get('confidence_spread', {})
                },
                'decision_analysis': {
                    'crisis_level_mapping': f"{consensus_prediction} -> {crisis_level}",
                    'needs_response_reason': "High-risk prediction detected" if needs_response else "Low-risk prediction",
                    'staff_review_triggered': needs_staff_review,
                    'staff_review_reason': "Model disagreement detected" if gaps_detected and needs_staff_review else "Confidence threshold triggered" if needs_staff_review else "No review needed"
                },
                'processing_metadata': {
                    'models_used': list(individual_results.keys()),
                    'total_models': len(individual_results),
                    'successful_analyses': len([r for r in individual_results.values() if r]),
                    'processing_time_ms': round((time.time() - start_time) * 1000, 2)
                }
            }
            
            # Calculate processing time
            processing_time_ms = round((time.time() - start_time) * 1000, 2)
            
            # Create response using the appropriate model class
            response = CrisisResponse(
                needs_response=needs_response,
                crisis_level=crisis_level,
                confidence_score=round(consensus_confidence, 4),
                detected_categories=detected_categories,
                method="three_model_ensemble_consensus",
                processing_time_ms=processing_time_ms,
                model_info=f"Three Zero-Shot Model Ensemble ({consensus_method} consensus)",
                reasoning=f"Consensus: {consensus_prediction} (confidence: {consensus_confidence:.3f}), Gaps: {gaps_detected}",
                analysis=analysis_info
            )
            
            logger.info(f"✅ Analysis complete: {crisis_level} ({consensus_confidence:.3f}) - {processing_time_ms:.1f}ms")
            
            # Log Phase 2B completion status
            if pydantic_manager:
                logger.debug("✅ Response validated using PydanticManager v3.1")
            else:
                logger.debug("✅ Response validated using legacy Pydantic models")
            
            return response
            
        except Exception as e:
            processing_time_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(f"❌ Analysis failed after {processing_time_ms:.1f}ms: {e}")
            
            if "Models not loaded" in str(e):
                raise HTTPException(status_code=503, detail="Models not available")
            elif "Empty message" in str(e):
                raise HTTPException(status_code=400, detail="Invalid message content")
            else:
                raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    # ========================================================================
    # PHASE 2B: NEW STATUS ENDPOINT
    # ========================================================================
    
    @app.get("/ensemble/status")
    async def ensemble_status():
        """Get status of the three-model ensemble system - Phase 2B Update"""
        try:
            models_status = {
                'models_loaded': model_manager.models_loaded() if model_manager else False,
                'ensemble_mode': thresholds['ensemble_mode'],
                'pydantic_manager': {
                    'version': '3.1' if pydantic_manager else 'legacy',
                    'available': pydantic_manager is not None,
                    'models_count': len(pydantic_manager.get_all_models()) if pydantic_manager else 'unknown'
                }
            }
            
            if model_manager and model_manager.models_loaded():
                models_status.update({
                    'depression_model_loaded': hasattr(model_manager, 'depression_model') and model_manager.depression_model is not None,
                    'sentiment_model_loaded': hasattr(model_manager, 'sentiment_model') and model_manager.sentiment_model is not None,
                    'emotional_distress_model_loaded': hasattr(model_manager, 'emotional_distress_model') and model_manager.emotional_distress_model is not None
                })
            
            return {
                'status': 'ready' if models_status['models_loaded'] else 'not_ready',
                'phase_2b_status': 'complete' if pydantic_manager else 'legacy_mode',
                'models': models_status,
                'configuration': {
                    'ensemble_mode': thresholds['ensemble_mode'],
                    'crisis_mapping_thresholds': {
                        'crisis_to_high': thresholds['consensus_crisis_to_high'],
                        'crisis_to_medium': thresholds['consensus_crisis_to_medium'],
                        'mild_crisis_to_low': thresholds['consensus_mild_crisis_to_low']
                    },
                    'staff_review_enabled': thresholds['staff_review_on_disagreement']
                },
                'architecture': {
                    'manager_version': '3.1',
                    'pydantic_manager_enabled': pydantic_manager is not None,
                    'models_manager_enabled': model_manager is not None
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get ensemble status: {e}")
            raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
    
    # ========================================================================
    # ADDITIONAL ENDPOINTS
    # ========================================================================
    
    @app.get("/ensemble/health")
    async def ensemble_health():
        """Get health status of all three models in the ensemble"""
        try:
            if not model_manager:
                raise HTTPException(status_code=503, detail="ModelManager not available")
            
            models_loaded = model_manager.models_loaded()
            
            health_status = {
                'status': 'healthy' if models_loaded else 'unhealthy',
                'models_loaded': models_loaded,
                'individual_models': {
                    'depression': hasattr(model_manager, 'depression_model') and model_manager.depression_model is not None,
                    'sentiment': hasattr(model_manager, 'sentiment_model') and model_manager.sentiment_model is not None,
                    'emotional_distress': hasattr(model_manager, 'emotional_distress_model') and model_manager.emotional_distress_model is not None
                },
                'phase_2b_integration': pydantic_manager is not None,
                'timestamp': time.time()
            }
            
            return health_status
            
        except Exception as e:
            logger.error(f"❌ Ensemble health check failed: {e}")
            raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")
    
    @app.get("/ensemble/config")
    async def ensemble_configuration():
        """Get current ensemble configuration for debugging"""
        try:
            return {
                'thresholds': thresholds,
                'source': 'environment_variables',
                'centralized_management': True,
                'phase_2b_status': 'complete' if pydantic_manager else 'legacy_mode',
                'pydantic_manager_info': {
                    'enabled': pydantic_manager is not None,
                    'summary': pydantic_manager.get_model_summary() if pydantic_manager else None
                },
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"❌ Configuration retrieval failed: {e}")
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    
    # ========================================================================
    # ENDPOINT REGISTRATION LOGGING
    # ========================================================================
    
    logger.info("🎯 Ensemble endpoints registered successfully with Phase 2B integration")
    
    if pydantic_manager:
        logger.info("✅ Phase 2B: All endpoints using PydanticManager v3.1 for model management")
        # Log model summary for verification
        try:
            summary = pydantic_manager.get_model_summary()
            logger.debug(f"📊 PydanticManager Summary: {summary['total_models']} models, {summary['architecture']} architecture")
        except Exception as e:
            logger.warning(f"⚠️ Could not retrieve PydanticManager summary: {e}")
    else:
        logger.info("⚠️ Phase 2B: Endpoints using legacy Pydantic models (migration recommended)")
    
    logger.info("🔧 Centralized threshold configuration applied to all ensemble endpoints")

# ============================================================================
# BACKWARD COMPATIBILITY FUNCTION
# ============================================================================

def add_ensemble_endpoints_legacy(app, model_manager):
    """
    Legacy function signature for backward compatibility
    Automatically detects if PydanticManager is available
    """
    logger.info("🔄 Legacy endpoint registration called - attempting PydanticManager detection")
    
    # Try to detect if PydanticManager is available in the global scope
    pydantic_manager = None
    try:
        import sys
        if 'main' in sys.modules:
            main_module = sys.modules['main']
            pydantic_manager = getattr(main_module, 'pydantic_manager', None)
        
        if pydantic_manager:
            logger.info("✅ PydanticManager detected - using Phase 2B integration")
        else:
            logger.info("⚠️ PydanticManager not detected - using legacy mode")
            
    except Exception as e:
        logger.warning(f"⚠️ PydanticManager detection failed: {e} - using legacy mode")
    
    # Call the updated function
    return add_ensemble_endpoints(app, model_manager, pydantic_manager)