# ash-nlp/api/ensemble_endpoints.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Three Zero-Shot Model Ensemble API Endpoints for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-3
LAST MODIFIED: 2025-08-22
PHASE: 3e, Step 5.6 - Integration Testing Updates
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

def integrate_pattern_and_ensemble_analysis(ensemble_result: Dict[str, Any], pattern_result: Dict[str, Any], crisis_threshold_manager=None) -> Dict[str, Any]:
    """
    Phase 3e: Combine ensemble and pattern analysis results with enhanced error handling
    Mode-aware integration with dynamic threshold configuration
    
    Args:
        ensemble_result: Results from the three-model ensemble
        pattern_result: Results from crisis pattern analysis  
        crisis_threshold_manager: CrisisThresholdManager for mode-aware thresholds
        
    Returns:
        Combined analysis with final crisis determination
    """
    try:
        # Extract ensemble consensus with enhanced validation
        ensemble_consensus = ensemble_result.get('consensus', {})
        ensemble_prediction = ensemble_consensus.get('prediction', 'unknown')
        ensemble_confidence = ensemble_consensus.get('confidence', 0.0)
        
        # Extract pattern information with enhanced validation
        patterns_triggered = pattern_result.get('patterns_triggered', [])
        pattern_error = pattern_result.get('error')
        
        # Get current mode and configuration with enhanced error handling
        if crisis_threshold_manager:
            try:
                current_mode = crisis_threshold_manager.get_current_ensemble_mode()
                crisis_mapping = crisis_threshold_manager.get_crisis_level_mapping_for_mode()
                pattern_integration_config = crisis_threshold_manager.get_pattern_integration_config()
                
                logger.debug(f"Integration using {current_mode} mode thresholds")
            except Exception as e:
                logger.warning(f"Error accessing threshold configuration: {e}")
                current_mode = 'fallback'
                crisis_mapping = _get_fallback_crisis_mapping()
                pattern_integration_config = _get_fallback_pattern_config()
        else:
            current_mode = 'fallback'
            crisis_mapping = _get_fallback_crisis_mapping()
            pattern_integration_config = _get_fallback_pattern_config()
            logger.warning("Using fallback thresholds - CrisisThresholdManager not available")
        
        # Determine pattern severity with enhanced validation
        pattern_severity = 'none'
        highest_pattern_level = 'none'
        pattern_confidence = 0.0
        
        if patterns_triggered:
            for pattern in patterns_triggered:
                try:
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
                except Exception as e:
                    logger.warning(f"Error processing pattern: {e}")
                    continue
        
        # Phase 3e: Mode-aware ensemble prediction to crisis level mapping
        final_crisis_level = 'none'
        final_confidence = ensemble_confidence
        integration_reasoning = []
        
        # Map ensemble prediction using mode-aware thresholds
        ensemble_crisis_level = _map_ensemble_prediction_to_crisis_level(
            ensemble_prediction, ensemble_confidence, crisis_mapping
        )
        integration_reasoning.append(f"Ensemble ({current_mode}): {ensemble_prediction} -> {ensemble_crisis_level}")
        
        # Pattern integration logic with enhanced error handling
        if patterns_triggered:
            integration_reasoning.append(f"Patterns: {len(patterns_triggered)} triggered, highest: {highest_pattern_level}")
            
            try:
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
            except Exception as e:
                logger.warning(f"Error in pattern integration logic: {e}")
                final_crisis_level = ensemble_crisis_level
                integration_reasoning.append(f"Pattern integration error, using ensemble result: {e}")
        else:
            final_crisis_level = ensemble_crisis_level
            integration_reasoning.append("No patterns triggered, using ensemble result")
        
        # Safety checks and bias application with enhanced error handling
        if crisis_threshold_manager:
            try:
                safety_config = crisis_threshold_manager.get_safety_controls_config()
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
            except Exception as e:
                logger.warning(f"Error applying safety controls: {e}")
        
        # Determine if response needed
        needs_response = final_crisis_level != 'none'
        
        # Build detected categories with enhanced validation
        detected_categories = []
        if patterns_triggered:
            try:
                detected_categories.extend([p.get('pattern_name', 'unknown_pattern') for p in patterns_triggered])
            except Exception as e:
                logger.warning(f"Error extracting pattern categories: {e}")
        
        try:
            ensemble_categories = ensemble_result.get('detected_categories', [])
            detected_categories.extend(ensemble_categories)
            detected_categories = list(set(detected_categories))
        except Exception as e:
            logger.warning(f"Error processing ensemble categories: {e}")
        
        # Phase 3e: Determine staff review requirement with enhanced error handling
        staff_review_required = False
        if crisis_threshold_manager:
            try:
                has_model_disagreement = ensemble_result.get('gap_detection', {}).get('gap_detected', False)
                has_gap_detection = ensemble_result.get('gap_detection', {}).get('requires_review', False)
                
                staff_review_required = crisis_threshold_manager.is_staff_review_required(
                    final_crisis_level, final_confidence, has_model_disagreement, has_gap_detection
                )
            except Exception as e:
                logger.warning(f"Error determining staff review requirement: {e}")
                # Fallback staff review logic
                staff_review_required = (final_crisis_level == 'high' or 
                                       (final_crisis_level == 'medium' and final_confidence >= 0.45))
        else:
            # Fallback staff review logic
            staff_review_required = (final_crisis_level == 'high' or 
                                   (final_crisis_level == 'medium' and final_confidence >= 0.45))
        
        return {
            'needs_response': needs_response,
            'crisis_level': final_crisis_level,
            'confidence_score': final_confidence,
            'detected_categories': detected_categories,
            'method': f'ensemble_and_patterns_integrated_{current_mode}',
            'model_info': f'Three Zero-Shot Model Ensemble + Crisis Pattern Analysis ({current_mode} mode)',
            'reasoning': ' | '.join(integration_reasoning),
            'staff_review_required': staff_review_required,
            'threshold_mode': current_mode,
            'integration_details': {
                'ensemble_prediction': ensemble_prediction,
                'ensemble_crisis_level': ensemble_crisis_level,
                'pattern_severity': pattern_severity,
                'patterns_count': len(patterns_triggered),
                'pattern_confidence': pattern_confidence,
                'final_determination': final_crisis_level,
                'pattern_available': not bool(pattern_error),
                'safety_bias_applied': crisis_threshold_manager is not None,
                'phase_3e_enhanced': True
            }
        }
        
    except Exception as e:
        logger.error(f"Error in pattern/ensemble integration: {e}")
        return {
            'needs_response': ensemble_result.get('consensus', {}).get('prediction', 'unknown') != 'neutral',
            'crisis_level': 'low',  # Conservative fallback
            'confidence_score': ensemble_result.get('consensus', {}).get('confidence', 0.0),
            'detected_categories': ensemble_result.get('detected_categories', []),
            'method': 'integration_error_fallback',
            'model_info': 'Integration error - using conservative fallback',
            'reasoning': f"Integration failed: {str(e)}",
            'staff_review_required': True,  # Always require review on errors
            'integration_error': str(e),
            'phase_3e_enhanced': True
        }

def _get_fallback_crisis_mapping() -> Dict[str, float]:
    """Get fallback crisis mapping configuration"""
    return {
        'crisis_to_high': 0.50,
        'crisis_to_medium': 0.30,
        'mild_crisis_to_low': 0.40,
        'negative_to_low': 0.70,
        'unknown_to_low': 0.50
    }

def _get_fallback_pattern_config() -> Dict[str, float]:
    """Get fallback pattern integration configuration"""
    return {
        'pattern_weight_multiplier': 1.2,
        'pattern_override_threshold': 0.8
    }

def _map_ensemble_prediction_to_crisis_level(prediction: str, confidence: float, crisis_mapping: Dict[str, float]) -> str:
    """
    Phase 3e: Map ensemble prediction to crisis level with enhanced error handling
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
            logger.warning(f"Unexpected ensemble prediction: {prediction}")
            return 'low' if confidence >= 0.60 else 'none'
            
    except Exception as e:
        logger.error(f"Error mapping ensemble prediction: {e}")
        return 'low' if confidence >= 0.50 else 'none'

def max_crisis_level(level1: str, level2: str) -> str:
    """Return the higher crisis level with enhanced validation"""
    try:
        crisis_hierarchy = {'none': 0, 'low': 1, 'medium': 2, 'high': 3}
        reverse_hierarchy = {0: 'none', 1: 'low', 2: 'medium', 3: 'high'}
        
        level1_value = crisis_hierarchy.get(level1, 0)
        level2_value = crisis_hierarchy.get(level2, 0)
        
        return reverse_hierarchy.get(max(level1_value, level2_value), 'none')
    except Exception as e:
        logger.warning(f"Error comparing crisis levels: {e}")
        return 'low'  # Safe fallback

def add_ensemble_endpoints(app: FastAPI, crisis_analyzer, pydantic_manager, pattern_detection_manager=None, crisis_threshold_manager=None):
    """
    Phase 3e: Add Three Zero-Shot Model Ensemble endpoints with enhanced validation
    Clean v3.1 implementation with improved error handling and Phase 3e patterns
    
    Args:
        app: FastAPI application instance
        model_coordination_manager: Model Ensemble Manager instance (required)
        pydantic_manager: PydanticManager v3.1 instance (required)
        pattern_detection_manager: PatternDetectionManager instance (optional)
        crisis_threshold_manager: CrisisThresholdManager instance (optional but recommended)
    """
    
    # ========================================================================
    # ENHANCED VALIDATION - Phase 3e
    # ========================================================================
    
    if not crisis_analyzer:
        logger.error("CrisisAnalyzer is required but not provided")
        raise RuntimeError("CrisisAnalyzer required for ensemble endpoints")
    
    if not pydantic_manager:
        logger.error("PydanticManager v3.1 is required but not provided")
        raise RuntimeError("PydanticManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager.is_initialized():
        logger.error("PydanticManager v3.1 is not properly initialized")
        raise RuntimeError("PydanticManager v3.1 not initialized")
    
    # Get Pydantic models with enhanced error handling
    try:
        models = pydantic_manager.get_core_models()
        logger.info("Pydantic models loaded for ensemble endpoints")
    except Exception as e:
        logger.error(f"Failed to load Pydantic models: {e}")
        raise RuntimeError(f"Pydantic model loading failed: {e}")
    
    # Phase 3e: Enhanced threshold manager validation
    if crisis_threshold_manager:
        try:
            current_mode = crisis_threshold_manager.get_current_ensemble_mode()
            logger.info(f"CrisisThresholdManager integrated - Current mode: {current_mode}")
            
            # Validate threshold configuration
            crisis_mapping = crisis_threshold_manager.get_crisis_level_mapping_for_mode()
            logger.debug(f"Current crisis mapping thresholds: {crisis_mapping}")
        except Exception as e:
            logger.warning(f"CrisisThresholdManager validation failed: {e}")
    else:
        logger.warning("CrisisThresholdManager not provided - using fallback thresholds")
    
    logger.info("Adding Clean v3.1 Three Zero-Shot Model Ensemble endpoints (Phase 3e)")
    
    # ========================================================================
    # ENSEMBLE ANALYSIS ENDPOINT - Phase 3e Enhanced
    # ========================================================================
    @app.post("/analyze", response_model=models['CrisisResponse'])
    async def analyze_message_clean(request: models['MessageRequest']):
        """
        Clean v3.1 Architecture: Single Analysis via CrisisAnalyzer
        Phase 3e: Enhanced error handling and validation
        
        Uses CrisisAnalyzer as the single source of truth for all analysis logic
        """
        try:
            start_time = time.time()
            logger.debug(f"Clean v3.1 Architecture: Analyzing message from user {request.user_id}")
            
            # Enhanced validation
            if not crisis_analyzer:
                raise HTTPException(
                    status_code=500,
                    detail="Crisis Analyzer not available"
                )
            
            # Single analysis call with enhanced error handling
            try:
                complete_analysis = await crisis_analyzer.analyze_crisis(
                    message=request.message,
                    user_id=request.user_id,
                    channel_id=request.channel_id
                )
                logger.debug(f"Complete analysis via CrisisAnalyzer: {complete_analysis.get('method', 'unknown')}")
                
            except Exception as e:
                logger.error(f"CrisisAnalyzer analysis failed: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Analysis failed: {str(e)}"
                )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # ========================================================================
            # PHASE 3E: ENHANCED RESPONSE EXTRACTION
            # ========================================================================
            
            # Extract from nested analysis_results structure with enhanced validation
            analysis_results = complete_analysis.get('analysis_results', {})
            
            # Map crisis_score -> confidence_score for API compatibility
            crisis_level = analysis_results.get('crisis_level', 'none')
            confidence_score = analysis_results.get('crisis_score', 0.0)
            
            # Enhanced fallback to top-level keys for backward compatibility
            if not analysis_results:
                logger.debug("Falling back to top-level keys for backward compatibility")
                crisis_level = complete_analysis.get('crisis_level', 'none')
                confidence_score = complete_analysis.get('confidence_score', 0.0)
            
            # Validate extracted values
            if not isinstance(crisis_level, str) or crisis_level not in ['none', 'low', 'medium', 'high', 'critical']:
                logger.warning(f"Invalid crisis_level '{crisis_level}', using 'none'")
                crisis_level = 'none'
                
            if not isinstance(confidence_score, (int, float)) or confidence_score < 0 or confidence_score > 1:
                logger.warning(f"Invalid confidence_score '{confidence_score}', using 0.0")
                confidence_score = 0.0
            
            logger.debug(f"Extracted crisis_level={crisis_level}, confidence_score={confidence_score}")
            logger.debug(f"Analysis structure: has_analysis_results={bool(analysis_results)}")
            
            try:
                response = models['CrisisResponse'](
                    needs_response=complete_analysis.get('needs_response', False),
                    crisis_level=crisis_level,
                    confidence_score=confidence_score,
                    detected_categories=complete_analysis.get('detected_categories', []),
                    method=complete_analysis.get('method', 'crisis_analyzer_complete_phase_3e'),
                    processing_time_ms=processing_time_ms,
                    model_info=complete_analysis.get('model_info', 'Clean v3.1 Architecture - CrisisAnalyzer Complete (Phase 3e)'),
                    reasoning=complete_analysis.get('reasoning', 'Single analysis via CrisisAnalyzer with enhanced validation'),
                    analysis={
                        'complete_analysis': complete_analysis,
                        'architecture': 'clean_v3.1',
                        'redundant_processing': False,
                        'feature_flags_respected': True,
                        'api_processing_time_ms': processing_time_ms,
                        'phase_3e_enhanced': True,
                        'enhanced_validation': True,
                        'context_analysis_available': bool(analysis_results.get('context_analysis')),
                        'note': 'Phase 3e: Enhanced error handling and validation applied'
                    }
                )
            except Exception as e:
                logger.error(f"Error creating response model: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Response creation failed: {str(e)}"
                )
            
            # ========================================================================
            # LOGGING - FINAL RESULT
            # ========================================================================
            
            method = complete_analysis.get('method', 'unknown')
            feature_flags = complete_analysis.get('feature_flags_applied', {})
            
            logger.debug(f"Clean Architecture Result: {crisis_level} (conf: {confidence_score:.3f}) via {method}")
            logger.debug(f"Feature flags applied: {feature_flags}")
            logger.info(f"Phase 3e Enhancement: API response extraction successful with validation")
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0.0
            logger.error(f"Unexpected error in clean analysis endpoint: {e}")
            logger.exception("Full error details:")
            
            # Return clean error response with enhanced error handling
            try:
                return models['CrisisResponse'](
                    needs_response=False,
                    crisis_level='none',
                    confidence_score=0.0,
                    detected_categories=[],
                    method='error_clean_architecture_phase_3e',
                    processing_time_ms=processing_time_ms,
                    model_info='Clean v3.1 Architecture - Error (Phase 3e)',
                    reasoning=f"Error during clean analysis: {str(e)}",
                    analysis={
                        'error': str(e),
                        'architecture': 'clean_v3_1_error_handling',
                        'processing_time_ms': processing_time_ms,
                        'phase_3e_enhanced': True
                    }
                )
            except Exception as response_error:
                logger.error(f"Failed to create error response: {response_error}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Critical error: {str(e)}"
                )
    
    # ========================================================================
    # HEALTH CHECK ENDPOINT - Phase 3e Enhanced
    # ========================================================================
    
    @app.get("/health")
    async def ensemble_health_check():
        """
        Phase 3e: Health check for ensemble system with enhanced validation
        """
        start_time = time.time()
        
        try:
            # Check models manager with enhanced validation
            models_loaded = False
            model_info = {}
            try:
                models_loaded = model_coordination_manager.models_loaded()
                model_info = model_coordination_manager.get_model_info() if models_loaded else {}
            except Exception as e:
                logger.warning(f"Error checking model status: {e}")
                model_info = {'error': str(e)}
            
            # Check pattern manager with enhanced validation
            pattern_manager_status = pattern_detection_manager is not None
            pattern_info = {}
            if pattern_detection_manager:
                try:
                    pattern_info = {
                        'patterns_loaded': len(pattern_detection_manager.get_available_patterns()),
                        'categories': pattern_detection_manager.get_pattern_categories()
                    }
                except Exception as e:
                    pattern_info = {'error': str(e)}
            
            # Phase 3e: Enhanced threshold manager validation
            threshold_manager_status = crisis_threshold_manager is not None
            threshold_info = {}
            if crisis_threshold_manager:
                try:
                    threshold_info = {
                        'current_mode': crisis_threshold_manager.get_current_ensemble_mode(),
                        'validation_status': crisis_threshold_manager.get_validation_summary(),
                        'crisis_mapping_loaded': bool(crisis_threshold_manager.get_crisis_level_mapping_for_mode()),
                        'staff_review_config': crisis_threshold_manager.get_staff_review_config()
                    }
                except Exception as e:
                    threshold_info = {'error': str(e)}
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            overall_status = "healthy" if (models_loaded and pattern_manager_status and threshold_manager_status) else "degraded"
            
            return {
                "status": overall_status,
                "timestamp": time.time(),
                "processing_time_ms": processing_time_ms,
                "phase": "3e",
                "architecture": "clean_v3_1",
                "enhanced_validation": True,
                "components": {
                    "ensemble_models": {
                        "status": "healthy" if models_loaded else "error",
                        "details": model_info
                    },
                    "pattern_analysis": {
                        "status": "healthy" if pattern_manager_status else "not_available",
                        "details": pattern_info
                    },
                    "crisis_threshold": {
                        "status": "healthy" if threshold_manager_status else "not_available", 
                        "details": threshold_info
                    }
                },
                "capabilities": {
                    "ensemble_analysis": models_loaded,
                    "pattern_integration": pattern_manager_status,
                    "context_analysis": True,
                    "mode_aware_thresholds": threshold_manager_status,
                    "staff_review_logic": threshold_manager_status,
                    "enhanced_error_handling": True,
                    "phase_3e_validation": True
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "timestamp": time.time(),
                "processing_time_ms": (time.time() - start_time) * 1000,
                "error": str(e),
                "phase": "3e",
                "architecture": "clean_v3_1",
                "enhanced_validation": True
            }
    
    # ========================================================================
    # CONFIGURATION AND STATUS ENDPOINTS - Phase 3e Enhanced
    # ========================================================================
    
    @app.get("/ensemble/config")
    async def get_ensemble_configuration():
        """Get current ensemble configuration with enhanced validation - Phase 3e"""
        try:
            config = {
                "ensemble_method": "three_zero_shot_models",
                "models_loaded": False,
                "phase": "3e",
                "architecture": "clean_v3_1",
                "enhanced_validation": True
            }
            
            # Add model info with enhanced validation
            if model_coordination_manager:
                try:
                    config["models_loaded"] = model_coordination_manager.models_loaded()
                    model_info = model_coordination_manager.get_model_info()
                    config["model_details"] = model_info
                except Exception as e:
                    config["model_details"] = {"error": str(e)}
            
            # Add threshold configuration with enhanced validation
            if crisis_threshold_manager:
                try:
                    current_mode = crisis_threshold_manager.get_current_ensemble_mode()
                    crisis_mapping = crisis_threshold_manager.get_crisis_level_mapping_for_mode()
                    config["threshold_configuration"] = {
                        "current_mode": current_mode,
                        "crisis_levels": list(crisis_mapping.keys()),
                        "threshold_count": len(crisis_mapping)
                    }
                except Exception as e:
                    config["threshold_configuration"] = {"error": str(e)}
            
            # Add pattern configuration with enhanced validation
            if pattern_detection_manager:
                try:
                    patterns = pattern_detection_manager.get_available_patterns()
                    config["pattern_configuration"] = {
                        "patterns_loaded": len(patterns),
                        "categories": pattern_detection_manager.get_pattern_categories()
                    }
                except Exception as e:
                    config["pattern_configuration"] = {"error": str(e)}
            
            return config
            
        except Exception as e:
            logger.error(f"Error getting ensemble configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    
    logger.info("Clean v3.1 Phase 3e Three Zero-Shot Model Ensemble endpoints configured successfully")
    logger.info("Phase 3e Enhancement: Enhanced error handling and validation applied throughout")
    
    # Phase 3e: Enhanced configuration summary logging
    if crisis_threshold_manager:
        try:
            current_mode = crisis_threshold_manager.get_current_ensemble_mode()
            crisis_mapping = crisis_threshold_manager.get_crisis_level_mapping_for_mode()
            logger.info(f"Ensemble endpoints configured with {current_mode} mode thresholds")
            logger.debug(f"Crisis mapping configuration: {crisis_mapping}")
        except Exception as e:
            logger.warning(f"Could not log threshold configuration: {e}")
    
    logger.info("Phase 3e Step 5.6: Ensemble endpoints ready for integration testing")