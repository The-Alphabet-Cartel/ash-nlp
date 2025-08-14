# ash-nlp/api/ensemble_endpoints.py
"""
Three Zero-Shot Model Ensemble API Endpoints for Ash NLP Service v3.1
FILE VERSION: v3.1-3d-10.8-1
LAST MODIFIED: 2025-08-14
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Step 10.8 API response extraction fixed
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
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
    # ENSEMBLE ANALYSIS ENDPOINT - STEP 10.8 FIXED
    # ========================================================================
    @app.post("/analyze", response_model=models['CrisisResponse'])
    async def analyze_message_v3d_clean(request: models['MessageRequest']):
        """
        CLEAN v3.1 Architecture: Single Analysis via CrisisAnalyzer
        STEP 10.8 FIX: Updated response extraction for new CrisisAnalyzer structure
        
        Removed redundant API-level analysis - CrisisAnalyzer is the single source of truth
        """
        try:
            start_time = time.time()
            logger.debug(f"🔍 Clean v3.1 Architecture: Analyzing message from user {request.user_id}")
            
            # ========================================================================
            # CLEAN ARCHITECTURE: SINGLE SOURCE OF TRUTH
            # CrisisAnalyzer handles all analysis logic including:
            # - Feature flag enforcement
            # - Ensemble analysis
            # - Pattern analysis (if enabled)
            # - Context analysis (Step 10.8)
            # - Threshold mapping
            # - Integration logic
            # ========================================================================
            
            if not models_manager:
                raise HTTPException(
                    status_code=500,
                    detail="Models manager not available"
                )
            
            try:
                # Single analysis call - CrisisAnalyzer does everything
                complete_analysis = await models_manager.analyze_message_ensemble(
                    message=request.message,
                    user_id=request.user_id,
                    channel_id=request.channel_id
                )
                logger.debug(f"✅ Complete analysis via CrisisAnalyzer: {complete_analysis.get('method', 'unknown')}")
                
            except Exception as e:
                logger.error(f"❌ CrisisAnalyzer analysis failed: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Analysis failed: {str(e)}"
                )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # ========================================================================
            # STEP 10.8 FIX: RESPONSE EXTRACTION FROM NESTED STRUCTURE
            # CrisisAnalyzer now returns nested analysis_results structure
            # ========================================================================
            
            # Extract from nested analysis_results structure (Step 10.8 fix)
            analysis_results = complete_analysis.get('analysis_results', {})
            
            # Map crisis_score -> confidence_score for API compatibility
            crisis_level = analysis_results.get('crisis_level', 'none')
            confidence_score = analysis_results.get('crisis_score', 0.0)  # Note: crisis_score, not confidence_score
            
            # Use fallback to top-level keys if nested structure not found (backward compatibility)
            if not analysis_results:
                logger.debug("🔄 Falling back to top-level keys for backward compatibility")
                crisis_level = complete_analysis.get('crisis_level', 'none')
                confidence_score = complete_analysis.get('confidence_score', 0.0)
            
            logger.debug(f"🔍 Step 10.8 Fix: Extracted crisis_level={crisis_level}, confidence_score={confidence_score}")
            logger.debug(f"🔍 Analysis structure: has_analysis_results={bool(analysis_results)}")
            
            response = models['CrisisResponse'](
                needs_response=complete_analysis.get('needs_response', False),
                crisis_level=crisis_level,  # From analysis_results.crisis_level
                confidence_score=confidence_score,  # From analysis_results.crisis_score
                detected_categories=complete_analysis.get('detected_categories', []),
                method=complete_analysis.get('method', 'crisis_analyzer_complete_v3d_step_10_8'),
                processing_time_ms=processing_time_ms,
                model_info=complete_analysis.get('model_info', 'Clean v3.1 Architecture - CrisisAnalyzer Complete (Step 10.8)'),
                reasoning=complete_analysis.get('reasoning', 'Single analysis via CrisisAnalyzer with ContextPatternManager'),
                analysis={
                    'complete_analysis': complete_analysis,
                    'architecture': 'clean_v3_1_single_source_of_truth',
                    'redundant_processing': False,
                    'feature_flags_respected': True,
                    'api_processing_time_ms': processing_time_ms,
                    'step_10_8_integration': True,
                    'context_analysis_available': bool(analysis_results.get('context_analysis')),
                    'note': 'Step 10.8: CrisisAnalyzer with ContextPatternManager integration'
                }
            )
            
            # ========================================================================
            # LOGGING - FINAL RESULT
            # ========================================================================
            
            method = complete_analysis.get('method', 'unknown')
            feature_flags = complete_analysis.get('feature_flags_applied', {})
            
            logger.debug(f"✅ Clean Architecture Result: {crisis_level} (conf: {confidence_score:.3f}) via {method}")
            logger.debug(f"🗣️ Feature flags applied: {feature_flags}")
            logger.info(f"🎯 Step 10.8 Fix Applied: API response extraction successful")
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0.0
            logger.error(f"❌ Unexpected error in clean analysis endpoint: {e}")
            logger.exception("Full error details:")
            
            # Return clean error response
            return models['CrisisResponse'](
                needs_response=False,
                crisis_level='none',
                confidence_score=0.0,
                detected_categories=[],
                method='error_clean_architecture_step_10_8',
                processing_time_ms=processing_time_ms,
                model_info='Clean v3.1 Architecture - Error (Step 10.8)',
                reasoning=f"Error during clean analysis: {str(e)}",
                analysis={
                    'error': str(e),
                    'architecture': 'clean_v3_1_error_handling',
                    'processing_time_ms': processing_time_ms,
                    'step_10_8_context': True
                }
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
                "phase": "3d",  # Updated for Step 10.8
                "architecture": "clean_v3_1",
                "step_10_8_integration": True,
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
                    "context_analysis": True,  # Step 10.8 capability
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
                "phase": "3d",  # Updated for Step 10.8
                "architecture": "clean_v3_1",
                "step_10_8_context": True
            }
    
    # ========================================================================
    # MISSING ENSEMBLE CONFIGURATION ENDPOINTS - ADD THESE
    # ========================================================================
    
    @app.get("/ensemble/config")
    async def get_ensemble_configuration():
        """Get current ensemble configuration - Phase 3c"""
        try:
            config = {
                "ensemble_method": "three_zero_shot_models",
                "models_loaded": models_manager.models_loaded() if models_manager else False,
                "phase": "3d",  # Updated for Step 10.8
                "architecture": "clean_v3_1",
                "step_10_8_integration": True
            }
            
            # Add model info if available
            if models_manager:
                try:
                    model_info = models_manager.get_model_info()
                    config["model_details"] = model_info
                except:
                    config["model_details"] = "unavailable"
            
            # Add threshold configuration if available
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                    config["threshold_configuration"] = {
                        "current_mode": current_mode,
                        "crisis_levels": list(crisis_mapping.keys()),
                        "threshold_count": len(crisis_mapping)
                    }
                except Exception as e:
                    config["threshold_configuration"] = {"error": str(e)}
            
            # Add pattern configuration if available
            if crisis_pattern_manager:
                try:
                    patterns = crisis_pattern_manager.get_available_patterns()
                    config["pattern_configuration"] = {
                        "patterns_loaded": len(patterns),
                        "categories": crisis_pattern_manager.get_pattern_categories()
                    }
                except Exception as e:
                    config["pattern_configuration"] = {"error": str(e)}
            
            return config
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    
    @app.get("/ensemble/health")
    async def get_ensemble_health():
        """Get ensemble system health status - Phase 3c"""
        try:
            start_time = time.time()
            
            # Check core components
            models_status = models_manager.models_loaded() if models_manager else False
            pattern_status = crisis_pattern_manager is not None
            threshold_status = threshold_mapping_manager is not None
            
            # Detailed health info
            health = {
                "status": "healthy" if all([models_status, pattern_status, threshold_status]) else "degraded",
                "timestamp": time.time(),
                "components": {
                    "models": models_status,
                    "patterns": pattern_status,
                    "thresholds": threshold_status
                },
                "phase": "3d",  # Updated for Step 10.8
                "step_10_8_integration": True,
                "processing_time_ms": (time.time() - start_time) * 1000
            }
            
            # Add detailed component info
            if models_manager and models_status:
                try:
                    model_info = models_manager.get_model_info()
                    health["model_details"] = model_info
                except:
                    health["model_details"] = "unavailable"
            
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    validation = threshold_mapping_manager.get_validation_summary()
                    health["threshold_details"] = {
                        "mode": current_mode,
                        "validation_errors": validation.get('validation_errors', 0),
                        "operational": validation.get('validation_errors', 0) == 0
                    }
                except Exception as e:
                    health["threshold_details"] = {"error": str(e)}
            
            return health
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble health: {e}")
            raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")
    
    @app.get("/ensemble/status")
    async def get_ensemble_status():
        """Get detailed ensemble system status - Phase 3c"""
        try:
            status = {
                "ensemble_operational": False,
                "phase": "3d",  # Updated for Step 10.8
                "architecture": "clean_v3_1",
                "step_10_8_integration": True,
                "timestamp": time.time()
            }
            
            # Check all components
            components = {}
            
            # Models status
            if models_manager:
                try:
                    models_loaded = models_manager.models_loaded()
                    model_info = models_manager.get_model_info() if models_loaded else {}
                    components["models"] = {
                        "status": "operational" if models_loaded else "unavailable",
                        "loaded": models_loaded,
                        "info": model_info
                    }
                except Exception as e:
                    components["models"] = {"status": "error", "error": str(e)}
            
            # Pattern manager status
            if crisis_pattern_manager:
                try:
                    patterns = crisis_pattern_manager.get_available_patterns()
                    components["patterns"] = {
                        "status": "operational",
                        "pattern_count": len(patterns),
                        "categories": crisis_pattern_manager.get_pattern_categories()
                    }
                except Exception as e:
                    components["patterns"] = {"status": "error", "error": str(e)}
            
            # Threshold manager status (Phase 3c)
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                    validation = threshold_mapping_manager.get_validation_summary()
                    
                    components["thresholds"] = {
                        "status": "operational" if validation.get('validation_errors', 0) == 0 else "warning",
                        "current_mode": current_mode,
                        "crisis_levels": list(crisis_mapping.keys()),
                        "validation_summary": validation
                    }
                except Exception as e:
                    components["thresholds"] = {"status": "error", "error": str(e)}
            
            status["components"] = components
            
            # Determine overall operational status
            operational_components = [
                comp.get("status") == "operational" 
                for comp in components.values()
            ]
            status["ensemble_operational"] = len(operational_components) > 0 and all(operational_components)
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble status: {e}")
            raise HTTPException(status_code=500, detail=f"Status error: {str(e)}")

    logger.info("✅ Clean v3.1 Phase 3d Three Zero-Shot Model Ensemble endpoints configured successfully")
    logger.info("🎯 Step 10.8 Fix Applied: API response extraction updated for CrisisAnalyzer structure")
    
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