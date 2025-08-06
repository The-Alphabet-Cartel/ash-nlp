# ash-nlp/api/ensemble_endpoints.py - PHASE 3C UPDATED
"""
Phase 3c UPDATED: Clean Three Zero-Shot Model Ensemble API Endpoints with ThresholdMappingManager
Mode-aware threshold integration with fail-fast validation and staff review logic

Clean v3.1 Architecture - NO Backward Compatibility
"""

import logging
import time
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

def integrate_pattern_and_ensemble_analysis_v3c(ensemble_result: Dict[str, Any], 
                                               pattern_result: Dict[str, Any],
                                               threshold_mapping_manager=None) -> Dict[str, Any]:
    """
    PHASE 3C: Combine ensemble and pattern analysis results using ThresholdMappingManager
    Mode-aware integration with dynamic threshold configuration
    
    Args:
        ensemble_result: Results from the three-model ensemble
        pattern_result: Results from crisis pattern analysis  
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds
        
    Returns:
        Combined analysis with final crisis determination
    """
    try:
        # Extract ensemble consensus
        ensemble_consensus = ensemble_result.get('consensus', {})
        ensemble_prediction = ensemble_consensus.get('prediction', 'unknown')
        ensemble_confidence = ensemble_consensus.get('confidence', 0.0)
        
        # Extract pattern information
        patterns_triggered = pattern_result.get('patterns_triggered', [])
        pattern_error = pattern_result.get('error')
        
        # Get current mode and configuration
        if threshold_mapping_manager:
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
            pattern_integration_config = threshold_mapping_manager.get_pattern_integration_config()
            
            logger.debug(f"🎯 Integration using {current_mode} mode thresholds")
        else:
            current_mode = 'fallback'
            crisis_mapping = {
                'crisis_to_high': 0.50,
                'crisis_to_medium': 0.30,
                'mild_crisis_to_low': 0.40,
                'negative_to_low': 0.70,
                'unknown_to_low': 0.50
            }
            pattern_integration_config = {
                'pattern_weight_multiplier': 1.2,
                'pattern_override_threshold': 0.8
            }
            logger.warning("⚠️ Using fallback thresholds - ThresholdMappingManager not available")
        
        # Determine pattern severity
        pattern_severity = 'none'
        highest_pattern_level = 'none'
        pattern_confidence = 0.0
        
        if patterns_triggered:
            for pattern in patterns_triggered:
                pattern_level = pattern.get('crisis_level', 'low')
                pattern_conf = pattern.get('confidence', 0.5)
                pattern_confidence = max(pattern_confidence, pattern_conf)
                
                if pattern_level == 'high':
                    highest_pattern_level = 'high'
                    pattern_severity = 'high'
                    break
                elif pattern_level == 'medium' and highest_pattern_level != 'high':
                    highest_pattern_level = 'medium'
                    pattern_severity = 'medium'
                elif pattern_level == 'low' and highest_pattern_level == 'none':
                    highest_pattern_level = 'low'
                    pattern_severity = 'low'
        
        # PHASE 3C: Mode-aware ensemble prediction to crisis level mapping
        final_crisis_level = 'none'
        final_confidence = ensemble_confidence
        integration_reasoning = []
        
        # Map ensemble prediction using mode-aware thresholds
        ensemble_crisis_level = _map_ensemble_prediction_to_crisis_level_v3c(
            ensemble_prediction, ensemble_confidence, crisis_mapping
        )
        integration_reasoning.append(f"Ensemble ({current_mode}): {ensemble_prediction} -> {ensemble_crisis_level}")
        
        # Pattern integration logic with mode-aware configuration
        if patterns_triggered:
            integration_reasoning.append(f"Patterns: {len(patterns_triggered)} triggered, highest: {highest_pattern_level}")
            
            # Apply pattern weight multiplier
            pattern_multiplier = pattern_integration_config.get('pattern_weight_multiplier', 1.2)
            weighted_pattern_confidence = pattern_confidence * pattern_multiplier
            
            # Pattern override logic
            pattern_override_threshold = pattern_integration_config.get('pattern_override_threshold', 0.8)
            
            if pattern_confidence >= pattern_override_threshold:
                # High-confidence patterns can override ensemble results
                if pattern_severity == 'high':
                    final_crisis_level = 'high'
                    final_confidence = max(final_confidence, weighted_pattern_confidence)
                    integration_reasoning.append(f"Pattern override: HIGH pattern (conf={pattern_confidence:.3f}) -> HIGH")
                elif pattern_severity == 'medium':
                    final_crisis_level = max_crisis_level(ensemble_crisis_level, 'medium')
                    final_confidence = max(final_confidence, weighted_pattern_confidence)
                    integration_reasoning.append(f"Pattern override: MEDIUM pattern (conf={pattern_confidence:.3f}) -> {final_crisis_level}")
                else:
                    final_crisis_level = max_crisis_level(ensemble_crisis_level, 'low')
                    final_confidence = max(final_confidence, weighted_pattern_confidence)
                    integration_reasoning.append(f"Pattern override: LOW pattern (conf={pattern_confidence:.3f}) -> {final_crisis_level}")
            else:
                # Normal pattern escalation logic
                if pattern_severity == 'high':
                    final_crisis_level = max_crisis_level(ensemble_crisis_level, 'high')
                    final_confidence = max(final_confidence, 0.75)
                    integration_reasoning.append("Pattern escalation: HIGH crisis pattern detected")
                    
                elif pattern_severity == 'medium':
                    if ensemble_crisis_level in ['high', 'medium']:
                        final_crisis_level = ensemble_crisis_level
                    else:
                        final_crisis_level = max_crisis_level(ensemble_crisis_level, 'medium')
                    final_confidence = max(final_confidence, 0.60)
                    integration_reasoning.append(f"Pattern escalation: MEDIUM pattern -> {final_crisis_level}")
                    
                elif pattern_severity == 'low':
                    final_crisis_level = max_crisis_level(ensemble_crisis_level, 'low')
                    final_confidence = max(final_confidence, 0.35)
                    integration_reasoning.append("Pattern escalation: LOW pattern detected")
        else:
            final_crisis_level = ensemble_crisis_level
            integration_reasoning.append("No patterns triggered, using ensemble result")
        
        # Safety checks and bias application
        if threshold_mapping_manager:
            safety_config = threshold_mapping_manager.get_safety_controls_config()
            safety_bias = safety_config.get('consensus_safety_bias', 0.03)
            
            # Apply safety bias toward higher crisis levels
            final_confidence += safety_bias
            final_confidence = min(final_confidence, 1.0)
            
            # Safety override: Never downgrade from ensemble HIGH
            if (ensemble_crisis_level == 'high' and 
                final_crisis_level != 'high' and 
                safety_config.get('enable_safety_override', True)):
                final_crisis_level = 'high'
                integration_reasoning.append("Safety override: Maintaining ensemble HIGH crisis level")
            
            # Fail-safe escalation for very high confidence
            if (final_confidence >= 0.90 and 
                final_crisis_level == 'none' and 
                safety_config.get('fail_safe_escalation', True)):
                final_crisis_level = 'low'
                integration_reasoning.append("Fail-safe escalation: Very high confidence requires response")
        
        # Determine if response needed
        needs_response = final_crisis_level != 'none'
        
        # Build detected categories
        detected_categories = []
        if patterns_triggered:
            detected_categories.extend([p.get('pattern_name', 'unknown_pattern') for p in patterns_triggered])
        
        ensemble_categories = ensemble_result.get('detected_categories', [])
        detected_categories.extend(ensemble_categories)
        detected_categories = list(set(detected_categories))
        
        # Phase 3c: Determine staff review requirement
        staff_review_required = False
        if threshold_mapping_manager:
            has_model_disagreement = ensemble_result.get('gap_detection', {}).get('gap_detected', False)
            has_gap_detection = ensemble_result.get('gap_detection', {}).get('requires_review', False)
            
            staff_review_required = threshold_mapping_manager.is_staff_review_required(
                final_crisis_level, final_confidence, has_model_disagreement, has_gap_detection
            )
        else:
            # Fallback staff review logic
            staff_review_required = (final_crisis_level == 'high' or 
                                   (final_crisis_level == 'medium' and final_confidence >= 0.45))
        
        return {
            'needs_response': needs_response,
            'crisis_level': final_crisis_level,
            'confidence_score': final_confidence,
            'detected_categories': detected_categories,
            'method': f'ensemble_and_patterns_integrated_v3c_{current_mode}',
            'model_info': f'Three Zero-Shot Model Ensemble + Crisis Pattern Analysis ({current_mode} mode)',
            'reasoning': ' | '.join(integration_reasoning),
            'staff_review_required': staff_review_required,  # Phase 3c addition
            'threshold_mode': current_mode,  # Phase 3c addition
            'integration_details': {
                'ensemble_prediction': ensemble_prediction,
                'ensemble_crisis_level': ensemble_crisis_level,
                'pattern_severity': pattern_severity,
                'patterns_count': len(patterns_triggered),
                'pattern_confidence': pattern_confidence,
                'final_determination': final_crisis_level,
                'pattern_available': not bool(pattern_error),
                'safety_bias_applied': threshold_mapping_manager is not None
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error in pattern/ensemble integration: {e}")
        return {
            'needs_response': ensemble_result.get('consensus', {}).get('prediction', 'unknown') != 'neutral',
            'crisis_level': 'low',  # Conservative fallback
            'confidence_score': ensemble_result.get('consensus', {}).get('confidence', 0.0),
            'detected_categories': ensemble_result.get('detected_categories', []),
            'method': 'integration_error_fallback',
            'model_info': 'Integration error - using conservative fallback',
            'reasoning': f"Integration failed: {str(e)}",
            'staff_review_required': True,  # Always require review on errors
            'integration_error': str(e)
        }

def _map_ensemble_prediction_to_crisis_level_v3c(prediction: str, confidence: float, 
                                                crisis_mapping: Dict[str, float]) -> str:
    """
    PHASE 3C: Map ensemble prediction to crisis level using mode-aware thresholds
    Replaces hardcoded mapping logic with dynamic threshold configuration
    """
    try:
        pred_lower = prediction.lower()
        
        # CRISIS predictions
        if pred_lower == 'crisis':
            if confidence >= crisis_mapping.get('crisis_to_high', 0.50):
                return 'high'
            elif confidence >= crisis_mapping.get('crisis_to_medium', 0.30):
                return 'medium'
            else:
                return 'low'  # Any crisis prediction gets at least low
        
        # MILD_CRISIS predictions
        elif pred_lower == 'mild_crisis':
            if confidence >= crisis_mapping.get('mild_crisis_to_low', 0.40):
                return 'low'
            else:
                return 'none'
        
        # NEGATIVE sentiment predictions
        elif pred_lower in ['negative', 'very_negative']:
            if confidence >= crisis_mapping.get('negative_to_low', 0.70):
                return 'low'
            else:
                return 'none'
        
        # LOW_RISK predictions
        elif pred_lower in ['low_risk', 'minimal_distress']:
            if confidence >= 0.80:  # Higher threshold for these
                return 'low'
            else:
                return 'none'
        
        # UNKNOWN predictions
        elif pred_lower == 'unknown':
            if confidence >= crisis_mapping.get('unknown_to_low', 0.50):
                return 'low'
            else:
                return 'none'
        
        # POSITIVE/NEUTRAL predictions
        elif pred_lower in ['positive', 'very_positive', 'neutral', 'no_risk']:
            return 'none'
        
        # Unexpected predictions
        else:
            logger.warning(f"⚠️ Unexpected ensemble prediction: {prediction}")
            return 'low' if confidence >= 0.60 else 'none'
            
    except Exception as e:
        logger.error(f"❌ Error mapping ensemble prediction: {e}")
        return 'low' if confidence >= 0.50 else 'none'

def max_crisis_level(level1: str, level2: str) -> str:
    """Return the higher crisis level"""
    crisis_hierarchy = {'none': 0, 'low': 1, 'medium': 2, 'high': 3}
    reverse_hierarchy = {0: 'none', 1: 'low', 2: 'medium', 3: 'high'}
    
    level1_value = crisis_hierarchy.get(level1, 0)
    level2_value = crisis_hierarchy.get(level2, 0)
    
    return reverse_hierarchy.get(max(level1_value, level2_value), 'none')

def add_ensemble_endpoints_v3c(app: FastAPI, models_manager, pydantic_manager, 
                              crisis_pattern_manager=None, threshold_mapping_manager=None):
    """
    PHASE 3C: Add Three Zero-Shot Model Ensemble endpoints with ThresholdMappingManager integration
    Clean v3.1 implementation with mode-aware threshold management
    
    Args:
        app: FastAPI application instance
        models_manager: ModelsManager v3.1 instance (required)
        pydantic_manager: PydanticManager v3.1 instance (required)
        crisis_pattern_manager: CrisisPatternManager instance (optional)
        threshold_mapping_manager: ThresholdMappingManager instance (optional but recommended)
    """
    
    # ========================================================================
    # CLEAN V3.1 VALIDATION - No Fallbacks
    # ========================================================================
    
    if not models_manager:
        logger.error("❌ ModelsManager v3.1 is required but not provided")
        raise RuntimeError("ModelsManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager:
        logger.error("❌ PydanticManager v3.1 is required but not provided")
        raise RuntimeError("PydanticManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager.is_initialized():
        logger.error("❌ PydanticManager v3.1 is not properly initialized")
        raise RuntimeError("PydanticManager v3.1 not initialized")
    
    # Get Pydantic models
    try:
        models = pydantic_manager.get_core_models()
        logger.info("✅ Pydantic models loaded for ensemble endpoints")
    except Exception as e:
        logger.error(f"❌ Failed to load Pydantic models: {e}")
        raise RuntimeError(f"Pydantic model loading failed: {e}")
    
    # Phase 3c: Log threshold manager status
    if threshold_mapping_manager:
        current_mode = threshold_mapping_manager.get_current_ensemble_mode()
        logger.info(f"✅ ThresholdMappingManager v3c integrated - Current mode: {current_mode}")
        
        # Log current threshold configuration
        crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
        logger.debug(f"🎯 Current crisis mapping thresholds: {crisis_mapping}")
    else:
        logger.warning("⚠️ ThresholdMappingManager not provided - using fallback thresholds")
    
    logger.info("🚀 Adding Clean v3.1 Three Zero-Shot Model Ensemble endpoints (Phase 3c)")
    
    # ========================================================================
    # ENSEMBLE ANALYSIS ENDPOINT - PHASE 3C UPDATED
    # ========================================================================
    
    @app.post("/analyze", response_model=models['CrisisResponse'])
    async def analyze_message_ensemble_v3c(request: models['MessageRequest']):
        """
        PHASE 3C: Analyze message using Three Zero-Shot Model Ensemble + Crisis Patterns + ThresholdMappingManager
        Clean v3.1 implementation with mode-aware threshold integration
        """
        start_time = time.time()
        
        try:
            logger.debug(f"🔍 Clean v3.1 Phase 3c: Analyzing message from user {request.user_id}")
            
            # Validate models are loaded - Direct manager check
            if not models_manager.models_loaded():
                logger.error("❌ Three Zero-Shot Model Ensemble not loaded")
                raise HTTPException(
                    status_code=503, 
                    detail="Three Zero-Shot Model Ensemble not available"
                )
            
            # STEP 1: Perform ensemble analysis - Direct manager usage
            try:
                ensemble_analysis = await models_manager.analyze_message_ensemble(
                    message=request.message,
                    user_id=request.user_id,
                    channel_id=request.channel_id
                )
                logger.debug(f"✅ Ensemble analysis complete")
            except Exception as e:
                logger.error(f"❌ Ensemble analysis failed: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Ensemble analysis failed: {str(e)}"
                )
            
            # STEP 2: CRISIS PATTERN ANALYSIS INTEGRATION (Phase 3a compatibility)
            pattern_analysis = {}
            if crisis_pattern_manager:
                try:
                    logger.debug("🔍 Running crisis pattern analysis...")
                    pattern_analysis = crisis_pattern_manager.analyze_message(
                        message=request.message,
                        user_id=request.user_id,
                        channel_id=request.channel_id
                    )
                    patterns_found = pattern_analysis.get('patterns_triggered', [])
                    logger.debug(f"✅ Pattern analysis complete: {len(patterns_found)} patterns triggered")
                    
                    if patterns_found:
                        logger.info(f"🚨 Crisis patterns detected: {[p.get('pattern_name', 'unknown') for p in patterns_found]}")
                except Exception as e:
                    logger.warning(f"⚠️ Pattern analysis failed: {e}")
                    pattern_analysis = {
                        "error": str(e), 
                        "patterns_triggered": [],
                        "analysis_available": False
                    }
            else:
                logger.debug("⚠️ No crisis pattern manager available - skipping pattern analysis")
                pattern_analysis = {
                    "error": "CrisisPatternManager not available", 
                    "patterns_triggered": [],
                    "analysis_available": False
                }
            
            # STEP 3: PHASE 3C - COMBINE ENSEMBLE AND PATTERN RESULTS WITH THRESHOLDMAPPINGMANAGER
            combined_analysis = integrate_pattern_and_ensemble_analysis_v3c(
                ensemble_analysis, pattern_analysis, threshold_mapping_manager
            )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Create response using PydanticManager models with combined analysis
            response = models['CrisisResponse'](
                needs_response=combined_analysis.get('needs_response', False),
                crisis_level=combined_analysis.get('crisis_level', 'none'),
                confidence_score=combined_analysis.get('confidence_score', 0.0),
                detected_categories=combined_analysis.get('detected_categories', []),
                method=combined_analysis.get('method', 'ensemble_and_patterns_v3c'),
                processing_time_ms=processing_time_ms,
                model_info=combined_analysis.get('model_info', 'Clean v3.1 Ensemble + Patterns + ThresholdMapping'),
                reasoning=combined_analysis.get('reasoning'),
                analysis={
                    'ensemble_analysis': ensemble_analysis,
                    'pattern_analysis': pattern_analysis,
                    'combined_result': combined_analysis,
                    'threshold_configuration': combined_analysis.get('threshold_mode', 'unknown'),
                    'staff_review_required': combined_analysis.get('staff_review_required', False)
                }
            )
            
            # Phase 3c: Log comprehensive analysis summary
            crisis_level = combined_analysis.get('crisis_level', 'none')
            staff_review = combined_analysis.get('staff_review_required', False)
            threshold_mode = combined_analysis.get('threshold_mode', 'unknown')
            
            logger.debug(f"✅ Clean v3.1 Phase 3c: Analysis complete - {crisis_level} level detected "
                        f"(mode={threshold_mode}, staff_review={staff_review})")
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            logger.error(f"❌ Unexpected error in analysis: {e}")
            logger.exception("Full analysis error:")
            
            # Return error response using PydanticManager models  
            return models['CrisisResponse'](
                needs_response=False,
                crisis_level='none',
                confidence_score=0.0,
                detected_categories=[],
                method='error',
                processing_time_ms=processing_time_ms,
                model_info='Clean v3.1 Phase 3c - Analysis Error',
                reasoning=f"Error during analysis: {str(e)}",
                analysis={'error': str(e), 'staff_review_required': True}
            )
    
    # ========================================================================
    # HEALTH CHECK ENDPOINT - PHASE 3C UPDATED
    # ========================================================================
    
    @app.get("/health")
    async def ensemble_health_check():
        """
        PHASE 3C: Health check for ensemble system with threshold configuration status
        """
        start_time = time.time()
        
        try:
            # Check models manager
            models_loaded = models_manager.models_loaded()
            model_info = models_manager.get_model_info() if models_loaded else {}
            
            # Check pattern manager
            pattern_manager_status = crisis_pattern_manager is not None
            pattern_info = {}
            if crisis_pattern_manager:
                try:
                    pattern_info = {
                        'patterns_loaded': len(crisis_pattern_manager.get_available_patterns()),
                        'categories': crisis_pattern_manager.get_pattern_categories()
                    }
                except Exception as e:
                    pattern_info = {'error': str(e)}
            
            # Phase 3c: Check threshold manager
            threshold_manager_status = threshold_mapping_manager is not None
            threshold_info = {}
            if threshold_mapping_manager:
                try:
                    threshold_info = {
                        'current_mode': threshold_mapping_manager.get_current_ensemble_mode(),
                        'validation_status': threshold_mapping_manager.get_validation_summary(),
                        'crisis_mapping_loaded': bool(threshold_mapping_manager.get_crisis_level_mapping_for_mode()),
                        'staff_review_enabled': threshold_mapping_manager.get_staff_review_config().get('high_always', False)
                    }
                except Exception as e:
                    threshold_info = {'error': str(e)}
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            overall_status = "healthy" if (models_loaded and pattern_manager_status and threshold_manager_status) else "degraded"
            
            return {
                "status": overall_status,
                "timestamp": time.time(),
                "processing_time_ms": processing_time_ms,
                "phase": "3c",
                "architecture": "clean_v3_1",
                "components": {
                    "ensemble_models": {
                        "status": "healthy" if models_loaded else "error",
                        "details": model_info
                    },
                    "pattern_analysis": {
                        "status": "healthy" if pattern_manager_status else "not_available",
                        "details": pattern_info
                    },
                    "threshold_mapping": {
                        "status": "healthy" if threshold_manager_status else "not_available", 
                        "details": threshold_info
                    }
                },
                "capabilities": {
                    "ensemble_analysis": models_loaded,
                    "pattern_integration": pattern_manager_status,
                    "mode_aware_thresholds": threshold_manager_status,
                    "staff_review_logic": threshold_manager_status,
                    "learning_system_ready": threshold_manager_status and threshold_info.get('validation_status', {}).get('configuration_loaded', False)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "timestamp": time.time(),
                "processing_time_ms": (time.time() - start_time) * 1000,
                "error": str(e),
                "phase": "3c",
                "architecture": "clean_v3_1"
            }
    
    logger.info("✅ Clean v3.1 Phase 3c Three Zero-Shot Model Ensemble endpoints configured successfully")
    
    # Phase 3c: Log configuration summary
    if threshold_mapping_manager:
        try:
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
            logger.info(f"🎯 Ensemble endpoints configured with {current_mode} mode thresholds")
            logger.debug(f"📊 Crisis mapping configuration: {crisis_mapping}")
        except Exception as e:
            logger.warning(f"⚠️ Could not log threshold configuration: {e}")

# Legacy function name for backward compatibility during transition
def add_ensemble_endpoints(app: FastAPI, models_manager, pydantic_manager, 
                          crisis_pattern_manager=None, threshold_mapping_manager=None):
    """Legacy wrapper for add_ensemble_endpoints_v3c"""
    return add_ensemble_endpoints_v3c(app, models_manager, pydantic_manager, 
                                     crisis_pattern_manager, threshold_mapping_manager)