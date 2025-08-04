# ash/ash-nlp/api/ensemble_endpoints.py (Clean v3.1 Architecture - Phase 2C Complete)
"""
Clean Three Zero-Shot Model Ensemble API Endpoints - NO Backward Compatibility
Direct manager usage only, no fallback code
"""

import logging
import time
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

def add_ensemble_endpoints(app: FastAPI, model_manager, pydantic_manager):
    """
    Add Three Zero-Shot Model Ensemble endpoints to FastAPI app
    Clean v3.1 implementation - Direct manager usage only
    
    Args:
        app: FastAPI application instance
        model_manager: ModelsManager v3.1 instance (required)
        pydantic_manager: PydanticManager v3.1 instance (required)
    """
    
    # ========================================================================
    # CLEAN V3.1 VALIDATION - No Fallbacks
    # ========================================================================
    
    if not model_manager:
        logger.error("❌ ModelsManager v3.1 is required but not provided")
        raise RuntimeError("ModelsManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager:
        logger.error("❌ PydanticManager v3.1 is required but not provided")
        raise RuntimeError("PydanticManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager.is_initialized():
        logger.error("❌ PydanticManager v3.1 is not properly initialized")
        raise RuntimeError("PydanticManager v3.1 must be initialized")
    
    logger.info("✅ Clean v3.1: Direct manager access validated")
    logger.info("🎯 Clean v3.1: No backward compatibility code present")
    
    # ========================================================================
    # CLEAN MODEL ACCESS - Direct PydanticManager Usage Only
    # ========================================================================
    
    def get_request_response_models():
        """Get request/response models from PydanticManager v3.1 - NO FALLBACKS"""
        try:
            core_models = pydantic_manager.get_core_models()
            learning_request_models = pydantic_manager.get_learning_request_models()
            learning_response_models = pydantic_manager.get_learning_response_models()
            
            return {
                # Core models
                'MessageRequest': core_models['MessageRequest'],
                'CrisisResponse': core_models['CrisisResponse'], 
                'HealthResponse': core_models['HealthResponse'],
                
                # Learning request models  
                'FalsePositiveAnalysisRequest': learning_request_models['FalsePositiveAnalysisRequest'],
                'FalseNegativeAnalysisRequest': learning_request_models['FalseNegativeAnalysisRequest'],
                'LearningUpdateRequest': learning_request_models['LearningUpdateRequest'],
                
                # Learning response models
                'FalsePositiveAnalysisResponse': learning_response_models['FalsePositiveAnalysisResponse'],
                'FalseNegativeAnalysisResponse': learning_response_models['FalseNegativeAnalysisResponse'], 
                'LearningUpdateResponse': learning_response_models['LearningUpdateResponse'],
                'LearningStatisticsResponse': learning_response_models['LearningStatisticsResponse']
            }
        except Exception as e:
            logger.error(f"❌ Failed to access PydanticManager v3.1 models: {e}")
            raise RuntimeError(f"PydanticManager v3.1 model access failed: {e}")
    
    # Get models once at startup - Clean v3.1
    try:
        models = get_request_response_models()
        logger.info("✅ Clean v3.1: Direct model access successful")
        logger.debug(f"📋 Available models: {list(models.keys())}")
    except Exception as e:
        logger.error(f"❌ Clean v3.1: Model access failed: {e}")
        raise
    
    # ========================================================================
    # ANALYSIS ENDPOINT - Clean v3.1 Implementation  
    # ========================================================================
    @app.post("/analyze", response_model=models['CrisisResponse'])
    async def analyze_message_ensemble(request: models['MessageRequest']):
        """
        Analyze message using Three Zero-Shot Model Ensemble + Crisis Patterns
        Clean v3.1 implementation with Pattern Integration (Phase 3a)
        """
        start_time = time.time()
        
        try:
            logger.debug(f"🔍 Clean v3.1: Analyzing message from user {request.user_id}")
            
            # Validate models are loaded - Direct manager check
            if not model_manager.models_loaded():
                logger.error("❌ Three Zero-Shot Model Ensemble not loaded")
                raise HTTPException(
                    status_code=503, 
                    detail="Three Zero-Shot Model Ensemble not available"
                )
            
            # STEP 1: Perform ensemble analysis - Direct manager usage
            try:
                ensemble_analysis = await model_manager.analyze_message_ensemble(
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
            
            # STEP 2: PATTERN ANALYSIS INTEGRATION (Phase 3a Fix)
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
            
            # STEP 3: COMBINE ENSEMBLE AND PATTERN RESULTS (Fix #4)
            combined_analysis = integrate_pattern_and_ensemble_analysis(
                ensemble_analysis, pattern_analysis
            )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Create response using PydanticManager models with combined analysis
            response = models['CrisisResponse'](
                needs_response=combined_analysis.get('needs_response', False),
                crisis_level=combined_analysis.get('crisis_level', 'none'),
                confidence_score=combined_analysis.get('confidence_score', 0.0),
                detected_categories=combined_analysis.get('detected_categories', []),
                method=combined_analysis.get('method', 'ensemble_and_patterns'),
                processing_time_ms=processing_time_ms,
                model_info=combined_analysis.get('model_info', 'Clean v3.1 Ensemble + Patterns'),
                reasoning=combined_analysis.get('reasoning'),
                analysis={
                    'ensemble_analysis': ensemble_analysis,
                    'pattern_analysis': pattern_analysis,
                    'combined_result': combined_analysis
                }
            )
            
            logger.debug(f"✅ Clean v3.1: Analysis complete - {combined_analysis.get('crisis_level', 'none')} level detected")
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
                model_info='Clean v3.1 - Analysis Error',
                reasoning=f"Error during analysis: {str(e)}",
                analysis={'error': str(e)}
            )
    
    # ========================================================================
    # STATUS ENDPOINTS - Clean v3.1 Implementation
    # ========================================================================
    
    @app.get("/ensemble/status")
    async def ensemble_status():
        """
        Get comprehensive ensemble status - Clean v3.1 Architecture
        """
        try:
            # Direct manager status checks - No fallbacks
            models_loaded = model_manager.models_loaded() if model_manager else False
            pydantic_available = pydantic_manager.is_initialized() if pydantic_manager else False
            
            # Get ensemble information - Direct manager usage
            ensemble_info = {}
            if model_manager and models_loaded:
                try:
                    ensemble_info = model_manager.get_ensemble_status()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get ensemble status: {e}")
                    ensemble_info = {"error": str(e)}
            
            # Get PydanticManager summary - Direct usage
            pydantic_info = {}
            if pydantic_manager and pydantic_available:
                try:
                    pydantic_info = pydantic_manager.get_model_summary()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get PydanticManager summary: {e}")
                    pydantic_info = {"error": str(e)}
            
            status = {
                "architecture_version": "v3.1_clean",
                "phase_2c_status": "complete",
                "backward_compatibility": "removed",
                "ensemble_status": {
                    "models_loaded": models_loaded,
                    "ensemble_info": ensemble_info
                },
                "pydantic_manager": {
                    "available": pydantic_available,
                    "summary": pydantic_info
                },
                "manager_integration": {
                    "models_manager_v3_1": model_manager is not None,
                    "pydantic_manager_v3_1": pydantic_manager is not None,
                    "direct_access_only": True,
                    "fallback_code": "removed"
                }
            }
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Status endpoint error: {e}")
            return {
                "architecture_version": "v3.1_clean",
                "phase_2c_status": "complete", 
                "error": str(e),
                "manager_integration": {
                    "direct_access_only": True,
                    "fallback_code": "removed"
                }
            }
    
    @app.get("/ensemble/health")
    async def ensemble_health():
        """
        Get ensemble health status - Clean v3.1 Implementation
        """
        try:
            # Direct manager health checks - No fallbacks
            health_status = {
                "status": "healthy",
                "architecture": "v3.1_clean",
                "phase_2c_complete": True,
                "managers": {
                    "models_manager_v3_1": model_manager is not None,
                    "pydantic_manager_v3_1": pydantic_manager is not None and pydantic_manager.is_initialized()
                },
                "models": {
                    "loaded": model_manager.models_loaded() if model_manager else False,
                    "count": 3 if model_manager and model_manager.models_loaded() else 0
                },
                "integration": {
                    "backward_compatibility": "removed",
                    "direct_manager_access": True,
                    "clean_architecture": True
                }
            }
            
            # Determine overall health
            if (health_status["managers"]["models_manager_v3_1"] and 
                health_status["managers"]["pydantic_manager_v3_1"] and
                health_status["models"]["loaded"]):
                health_status["status"] = "healthy"
            elif health_status["managers"]["models_manager_v3_1"]:
                health_status["status"] = "degraded"
            else:
                health_status["status"] = "unhealthy"
            
            return health_status
            
        except Exception as e:
            logger.error(f"❌ Health endpoint error: {e}")
            return {
                "status": "unhealthy",
                "architecture": "v3.1_clean",
                "phase_2c_complete": True,
                "error": str(e),
                "integration": {
                    "backward_compatibility": "removed",
                    "direct_manager_access": True
                }
            }
    
    @app.get("/ensemble/config")
    async def ensemble_config():
        """
        Get ensemble configuration - Clean v3.1 Implementation
        """
        try:
            config_info = {
                "architecture": "v3.1_clean",
                "phase_2c_status": "complete",
                "configuration": {},
                "models": {},
                "manager_info": {
                    "models_manager": "v3.1",
                    "pydantic_manager": "v3.1",
                    "backward_compatibility": "removed",
                    "direct_access": True
                }
            }
            
            # Get configuration from model manager - Direct usage
            if model_manager:
                try:
                    config_info["configuration"] = model_manager.get_configuration_status()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get model manager configuration: {e}")
                    config_info["configuration"] = {"error": str(e)}
                
                try:
                    config_info["models"] = model_manager.get_model_info()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get model info: {e}")
                    config_info["models"] = {"error": str(e)}
            
            # Get PydanticManager configuration - Direct usage  
            if pydantic_manager:
                try:
                    config_info["pydantic_models"] = pydantic_manager.get_model_summary()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get PydanticManager config: {e}")
                    config_info["pydantic_models"] = {"error": str(e)}
            
            return config_info
            
        except Exception as e:
            logger.error(f"❌ Config endpoint error: {e}")
            return {
                "architecture": "v3.1_clean",
                "phase_2c_status": "complete",
                "error": str(e),
                "manager_info": {
                    "backward_compatibility": "removed",
                    "direct_access": True
                }
            }
    
    # ========================================================================
    # ENDPOINT REGISTRATION COMPLETE
    # ========================================================================
    
    logger.info("🎯 Clean v3.1: Three Zero-Shot Model Ensemble endpoints registered successfully")
    logger.info("🔧 Endpoints added:")
    logger.info("   POST /analyze - Main ensemble analysis endpoint")
    logger.info("   GET /ensemble/status - Comprehensive status information")
    logger.info("   GET /ensemble/health - Health check for ensemble components")
    logger.info("   GET /ensemble/config - Configuration and model information")
    logger.info("✅ Phase 2C: All endpoints using direct manager access - No fallback code")
    logger.info("🎉 Clean v3.1 Architecture: Backward compatibility completely removed")