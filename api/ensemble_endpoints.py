# ash-nlp/api/ensemble_endpoints.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models â†' Pattern Enhancement â†' Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Three Zero-Shot Model Ensemble API Endpoints for Ash NLP Service
---
FILE VERSION: v3.1-4b-2
LAST MODIFIED: 2025-09-07
PHASE: 3e, Step 5.6 - Integration Testing Updates + Crisis Score Fix
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

def add_ensemble_endpoints(app: FastAPI, crisis_analyzer, pydantic_manager, pattern_detection_manager=None, crisis_threshold_manager=None):
    """
    Add Three Zero-Shot Model Ensemble endpoints with enhanced validation
    
    Args:
        app: FastAPI application instance
        model_coordination_manager: Model Ensemble Manager instance (required)
        pydantic_manager: PydanticManager v3.1 instance (required)
        pattern_detection_manager: PatternDetectionManager instance (optional)
        crisis_threshold_manager: CrisisThresholdManager instance (optional but recommended)
    """
    
    # ========================================================================
    # ENHANCED VALIDATION
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
    
    logger.info("Adding Clean v3.1 Three Zero-Shot Model Ensemble endpoints")
    
    # ========================================================================
    # ENSEMBLE ANALYSIS ENDPOINT
    # ========================================================================
    @app.post("/analyze", response_model=models['CrisisResponse'])
    async def analyze_message_clean(request: models['MessageRequest']):
        """
        Uses CrisisAnalyzer as the single source of truth for all analysis logic
        """
        try:
            start_time = time.time()
            logger.debug(f"Clean Architecture: Analyzing message from user {request.user_id}")
            
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
            # ENHANCED RESPONSE EXTRACTION
            # ========================================================================
            # Extract from nested analysis_results structure with enhanced validation
            analysis_results = complete_analysis.get('analysis_results', {})
            
            # Extract crisis_score, crisis_level, and confidence_score
            crisis_level = analysis_results.get('crisis_level', 'none')
            crisis_score = analysis_results.get('crisis_score', 0.0)  # ✅ FIX: Extract crisis_score
            confidence_score = analysis_results.get('confidence_score', 0.0)
            
            # Debug logging
            logger.debug(f"complete_analysis keys: {list(complete_analysis.keys())}")
            logger.debug(f"analysis_results keys: {list(analysis_results.keys())}")
            logger.debug(f"complete_analysis crisis_score: {complete_analysis.get('crisis_score', 'missing')}")
            logger.debug(f"analysis_results crisis_score: {analysis_results.get('crisis_score', 'missing')}")

            # Enhanced fallback to top-level keys for backward compatibility
            if not analysis_results:
                logger.debug("Falling back to top-level keys for backward compatibility")
                crisis_level = complete_analysis.get('crisis_level', 'none')
                crisis_score = complete_analysis.get('crisis_score', 0.0)  # ✅ FIX: Fallback for crisis_score
                confidence_score = complete_analysis.get('confidence_score', 0.0)
            
            # Validate extracted values
            if not isinstance(crisis_level, str) or crisis_level not in ['none', 'low', 'medium', 'high', 'critical']:
                logger.warning(f"Invalid crisis_level '{crisis_level}', using 'none'")
                crisis_level = 'none'
                
            if not isinstance(crisis_score, (int, float)) or crisis_score < 0 or crisis_score > 1:
                logger.warning(f"Invalid crisis_score '{crisis_score}', using 0.0")
                crisis_score = 0.0  # ✅ FIX: Validate crisis_score
                
            if not isinstance(confidence_score, (int, float)) or confidence_score < 0 or confidence_score > 1:
                logger.warning(f"Invalid confidence_score '{confidence_score}', using 0.0")
                confidence_score = 0.0
            
            logger.debug(f"Extracted crisis_level={crisis_level}, crisis_score={crisis_score:.3f}, confidence_score={confidence_score:.3f}")
            logger.debug(f"Analysis structure: has_analysis_results={bool(analysis_results)}")
            
            try:
                response = models['CrisisResponse'](
                    needs_response=complete_analysis.get('needs_response', False),
                    crisis_level=crisis_level,
                    crisis_score=crisis_score,  # ✅ FIX: Pass crisis_score to response model
                    confidence_score=confidence_score,
                    detected_categories=complete_analysis.get('detected_categories', []),
                    method=complete_analysis.get('method', 'crisis_analyzer'),
                    processing_time_ms=processing_time_ms,
                    model_info=complete_analysis.get('model_info', 'Clean Architecture - CrisisAnalyzer Complete'),
                    reasoning=complete_analysis.get('reasoning', 'Single analysis via CrisisAnalyzer with enhanced validation'),
                    analysis={
                        'complete_analysis': complete_analysis,
                        'architecture': 'clean',
                        'redundant_processing': False,
                        'feature_flags_respected': True,
                        'api_processing_time_ms': processing_time_ms,
                        'enhanced_validation': True,
                        'context_analysis_available': bool(analysis_results.get('context_analysis'))
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
            
            logger.debug(f"Clean Architecture Result: {crisis_level} (crisis_score: {crisis_score:.3f}, conf: {confidence_score:.3f}) via {method}")
            logger.debug(f"Feature flags applied: {feature_flags}")
            logger.info(f"API response extraction successful with validation - crisis_score field included")
            
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
                    crisis_score=0.0,  # ✅ FIX: Include crisis_score in error response
                    confidence_score=0.0,
                    detected_categories=[],
                    method='error_clean_architecture',
                    processing_time_ms=processing_time_ms,
                    model_info='Clean Architecture - Error',
                    reasoning=f"Error during clean analysis: {str(e)}",
                    analysis={
                        'error': str(e),
                        'architecture': 'clean_error_handling',
                        'processing_time_ms': processing_time_ms
                    }
                )
            except Exception as response_error:
                logger.error(f"Failed to create error response: {response_error}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Critical error: {str(e)}"
                )
    
    # ========================================================================
    # HEALTH CHECK ENDPOINT
    # ========================================================================
    @app.get("/ensemble/health")
    async def ensemble_health_check():
        """
        Health check for ensemble system with validation
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
                "architecture": "clean",
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
                    "enhanced_error_handling": True
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "timestamp": time.time(),
                "processing_time_ms": (time.time() - start_time) * 1000,
                "error": str(e),
                "architecture": "clean",
                "enhanced_validation": True
            }
    
    # ========================================================================
    # WEIGHTS
    # ========================================================================
    @app.post("/ensemble/set-weights")
    async def set_ensemble_weights(
        depression_weight: float,
        sentiment_weight: float,
        distress_weight: float,
        ensemble_mode: str = "majority"
    ):
        """Directly set weights without environment variables"""
        try:
            # Normalize weights
            total = depression_weight + sentiment_weight + distress_weight
            if total > 0:
                depression_weight /= total
                sentiment_weight /= total
                distress_weight /= total
            
            # Update performance optimizer directly
            if hasattr(crisis_analyzer, 'performance_optimizer'):
                old_weights = getattr(crisis_analyzer.performance_optimizer, '_cached_model_weights', {})
                old_mode = getattr(crisis_analyzer.performance_optimizer, '_cached_ensemble_mode', 'unknown')
                
                crisis_analyzer.performance_optimizer._cached_model_weights = {
                    'depression': depression_weight,
                    'sentiment': sentiment_weight,
                    'emotional_distress': distress_weight
                }
                crisis_analyzer.performance_optimizer._cached_ensemble_mode = ensemble_mode
                
                # Enhanced logging for debugging
                logger.info("🎯 Weights updated via /ensemble/set-weights endpoint:")
                logger.info(f"   Old weights: {old_weights}")
                logger.info(f"   New weights: {crisis_analyzer.performance_optimizer._cached_model_weights}")
                logger.info(f"   Old mode: {old_mode}")
                logger.info(f"   New mode: {ensemble_mode}")
                
                # CRITICAL DEBUG: Check other sources of ensemble mode
                logger.info("🔍 MODE DEBUG - Checking all sources:")
                
                # Check model coordination manager
                if hasattr(crisis_analyzer, 'model_coordination_manager') and crisis_analyzer.model_coordination_manager:
                    try:
                        manager_mode = crisis_analyzer.model_coordination_manager.get_ensemble_mode()
                        logger.info(f"🔍   ModelCoordinationManager mode: {manager_mode}")
                    except Exception as e:
                        logger.info(f"🔍   ModelCoordinationManager mode ERROR: {e}")
                
                # Check performance optimizer cache
                perf_mode = getattr(crisis_analyzer.performance_optimizer, '_cached_ensemble_mode', 'NOT_SET')
                logger.info(f"🔍   PerformanceOptimizer cached mode: {perf_mode}")
                
            # Success logging for observational troubleshooting
            logger.info(f"✅ Ensemble weights successfully set:")
            logger.info(f"   Depression: {depression_weight:.3f}")
            logger.info(f"   Sentiment: {sentiment_weight:.3f}")
            logger.info(f"   Emotional Distress: {distress_weight:.3f}")
            logger.info(f"   Ensemble Mode: {ensemble_mode}")
            logger.info(f"   Cache Updated: {hasattr(crisis_analyzer, 'performance_optimizer')}")
            
            return {
                'status': 'success',
                'weights': {
                    'depression': depression_weight,
                    'sentiment': sentiment_weight,
                    'emotional_distress': distress_weight
                },
                'ensemble_mode': ensemble_mode,
                'cache_updated': hasattr(crisis_analyzer, 'performance_optimizer'),
                'message': 'Weights set successfully - will be used for next classifications'
            }
        except Exception as e:
            logger.error(f"Failed to set weights: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/ensemble/refresh-weights")
    async def refresh_ensemble_weights(force_reload: bool = False):
        """
        Refresh cached ensemble weights from current environment variables
        
        Args:
            force_reload: If true, bypass all caching and read directly from environment
        """
        import os
        
        try:
            start_time = time.time()
            refresh_results = {}
            
            # Show current environment variables for debugging
            env_vars = {
                'NLP_MODEL_DEPRESSION_WEIGHT': os.getenv('NLP_MODEL_DEPRESSION_WEIGHT', 'not_set'),
                'NLP_MODEL_SENTIMENT_WEIGHT': os.getenv('NLP_MODEL_SENTIMENT_WEIGHT', 'not_set'),
                'NLP_MODEL_DISTRESS_WEIGHT': os.getenv('NLP_MODEL_DISTRESS_WEIGHT', 'not_set'),
                'NLP_ENSEMBLE_MODE': os.getenv('NLP_ENSEMBLE_MODE', 'not_set')
            }
            refresh_results['current_environment'] = env_vars
            
            # Refresh CrisisAnalyzer performance optimizer cache
            if hasattr(crisis_analyzer, 'performance_optimizer'):
                try:
                    if force_reload:
                        # Use nuclear option to force environment variable reload
                        success = crisis_analyzer.performance_optimizer.force_environment_variable_reload()
                        method = 'nuclear_reload'
                    else:
                        # Try normal refresh first
                        success = crisis_analyzer.performance_optimizer.refresh_cached_weights()
                        method = 'normal_refresh'
                        
                        # If normal refresh failed, try nuclear option
                        if not success:
                            logger.warning("Normal refresh failed, trying nuclear reload...")
                            success = crisis_analyzer.performance_optimizer.force_environment_variable_reload()
                            method = 'nuclear_fallback'
                    
                    refresh_results['performance_optimizer'] = {
                        'success': success,
                        'method': method,
                        'cached_weights': crisis_analyzer.performance_optimizer._cached_model_weights,
                        'cached_mode': crisis_analyzer.performance_optimizer._cached_ensemble_mode
                    }
                    
                    logger.info(f"Performance optimizer cache refreshed via {method}: {success}")
                    
                except Exception as e:
                    refresh_results['performance_optimizer'] = {'error': str(e)}
                    logger.error(f"Failed to refresh performance optimizer cache: {e}")
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            return {
                'status': 'success',
                'processing_time_ms': processing_time_ms,
                'refresh_results': refresh_results,
                'message': f'Ensemble weights refreshed via {method if "method" in locals() else "unknown"}'
            }
            
        except Exception as e:
            logger.error(f"Weight refresh failed: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Weight refresh failed: {str(e)}"
            )

    # ========================================================================
    # CONFIGURATION ENDPOINT
    # ========================================================================
    @app.get("/ensemble/config")
    async def get_ensemble_configuration():
        """Get current ensemble configuration with validation"""
        try:
            config = {
                "ensemble_method": "three_zero_shot_models",
                "models_loaded": False,
                "architecture": "clean",
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
    
    logger.info("Zero-Shot Model Ensemble endpoints configured successfully")
    
    if crisis_threshold_manager:
        try:
            current_mode = crisis_threshold_manager.get_current_ensemble_mode()
            crisis_mapping = crisis_threshold_manager.get_crisis_level_mapping_for_mode()
            logger.info(f"Ensemble endpoints configured with {current_mode} mode thresholds")
            logger.debug(f"Crisis mapping configuration: {crisis_mapping}")
        except Exception as e:
            logger.warning(f"Could not log threshold configuration: {e}")
    
    logger.info("Ensemble endpoints ready")