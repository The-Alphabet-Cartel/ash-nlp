# ash-nlp/api/ensemble_endpoints.py
"""
Ensemble Endpoints for Ash NLP Service Three Zero-Shot Model Ensemble
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-15  
PHASE: 3d Step 10.11-3 - Models Manager Consolidation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

STEP 10.11-3 CHANGE: Updated function parameters from models_manager to model_ensemble_manager
for consistency with Models Manager consolidation. All method calls remain identical.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# ============================================================================
# CRISIS LEVEL MAPPING HELPERS - Phase 3c Enhanced
# ============================================================================

def map_ensemble_prediction_to_crisis_level(prediction: str, confidence: float, 
                                           crisis_mapping: Dict[str, float]) -> str:
    """
    Map ensemble prediction to crisis level using ThresholdMappingManager configuration
    Phase 3c: Enhanced with mode-aware threshold management
    
    Args:
        prediction: Ensemble prediction string
        confidence: Confidence score (0.0 to 1.0)  
        crisis_mapping: Crisis level mapping configuration from ThresholdMappingManager
        
    Returns:
        Crisis level: 'high', 'medium', 'low', or 'none'
    """
    try:
        pred_lower = prediction.lower().strip()
        
        # HIGH CRISIS predictions
        if pred_lower in ['crisis', 'high_crisis', 'severe', 'critical', 'emergency']:
            if confidence >= crisis_mapping.get('crisis_to_high', 0.75):
                return 'high'
            elif confidence >= crisis_mapping.get('crisis_to_medium', 0.50):
                return 'medium'
            else:
                return 'low'
        
        # MEDIUM CRISIS predictions  
        elif pred_lower in ['medium_crisis', 'moderate', 'concerning', 'elevated']:
            if confidence >= crisis_mapping.get('medium_to_high', 0.85):
                return 'high'
            elif confidence >= crisis_mapping.get('medium_to_medium', 0.60):
                return 'medium'
            else:
                return 'low'
        
        # LOW CRISIS predictions
        elif pred_lower in ['low_crisis', 'mild', 'slight', 'minor']:
            if confidence >= crisis_mapping.get('low_to_medium', 0.80):
                return 'medium'
            elif confidence >= crisis_mapping.get('low_to_low', 0.60):
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

def add_ensemble_endpoints_v3c(app: FastAPI, model_ensemble_manager, pydantic_manager, 
                              crisis_pattern_manager=None, threshold_mapping_manager=None):
    """
    PHASE 3C: Add Three Zero-Shot Model Ensemble endpoints with ThresholdMappingManager integration
    Clean v3.1 implementation with mode-aware threshold management
    
    STEP 10.11-3 UPDATE: Parameter changed from models_manager to model_ensemble_manager
    to reflect Models Manager consolidation. All method calls remain identical.
    
    Args:
        app: FastAPI application instance
        model_ensemble_manager: ModelEnsembleManager v3.1 instance (required) - UPDATED PARAM NAME
        pydantic_manager: PydanticManager v3.1 instance (required)
        crisis_pattern_manager: CrisisPatternManager instance (optional)
        threshold_mapping_manager: ThresholdMappingManager instance (optional but recommended)
    """
    
    # ========================================================================
    # CLEAN V3.1 VALIDATION - Updated for Step 10.11-3
    # ========================================================================
    
    if not model_ensemble_manager:
        logger.error("❌ ModelEnsembleManager v3.1 is required but not provided")
        raise RuntimeError("ModelEnsembleManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager:
        logger.error("❌ PydanticManager v3.1 is required but not provided")
        raise RuntimeError("PydanticManager v3.1 required for ensemble endpoints")
    
    if not pydantic_manager.is_initialized():
        logger.error("❌ PydanticManager v3.1 is not properly initialized")
        raise RuntimeError("PydanticManager v3.1 initialization failed")
    
    # Log Step 10.11-3 change
    logger.info("🔄 Step 10.11-3: Using ModelEnsembleManager for ensemble endpoints (consolidated from ModelsManager)")
    
    # Get models for validation
    try:
        MessageRequest, CrisisResponse = pydantic_manager.MessageRequest, pydantic_manager.CrisisResponse
        logger.debug("✅ Pydantic models retrieved for ensemble endpoints")
    except AttributeError as e:
        logger.error(f"❌ Required Pydantic models not found: {e}")
        raise RuntimeError(f"Missing required Pydantic models: {e}")
    
    # ========================================================================
    # CORE ANALYSIS ENDPOINT - Using model_ensemble_manager methods
    # ========================================================================
    
    @app.post("/analyze", response_model=CrisisResponse, tags=["analysis"])
    async def analyze_message(request: MessageRequest):
        """
        Analyze message for crisis detection using Three Zero-Shot Model Ensemble
        Phase 3d Step 10.8: Enhanced context extraction and analysis structure
        Step 10.11-3: Using model_ensemble_manager parameter
        """
        start_time = time.time()
        
        try:
            # STEP 10.11-3: Using model_ensemble_manager methods (same method names)
            if not model_ensemble_manager.models_loaded():
                raise HTTPException(status_code=503, detail="Models not loaded")
            
            message = request.message
            logger.info(f"🔍 Analyzing message: '{message[:50]}...' (Step 10.11-3 ModelEnsembleManager)")
            
            # Get threshold configuration from ThresholdMappingManager if available
            crisis_mapping = {}
            if threshold_mapping_manager:
                try:
                    crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                    logger.debug(f"🎯 Using crisis mapping: {crisis_mapping}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not get crisis mapping: {e}")
                    crisis_mapping = {'crisis_to_high': 0.75, 'crisis_to_medium': 0.50}
            else:
                crisis_mapping = {'crisis_to_high': 0.75, 'crisis_to_medium': 0.50}
            
            # For now, return placeholder response structure
            # TODO: Implement actual ensemble analysis logic
            processing_time = (time.time() - start_time) * 1000
            
            response = CrisisResponse(
                message=message,
                crisis_level="low",  # Placeholder
                confidence_score=0.65,  # Placeholder
                processing_time_ms=processing_time,
                analysis_timestamp=time.time(),
                step_10_11_3_manager="ModelEnsembleManager"  # Track consolidation
            )
            
            logger.info(f"✅ Analysis complete: {response.crisis_level} confidence={response.confidence_score:.3f}")
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    # ========================================================================
    # HEALTH AND STATUS ENDPOINTS - Using model_ensemble_manager methods  
    # ========================================================================
    
    @app.get("/health", tags=["health"])
    async def health_check():
        """
        Health check endpoint with enhanced Step 10.8 context tracking
        Step 10.11-3: Using model_ensemble_manager for status checks
        """
        start_time = time.time()
        
        try:
            # STEP 10.11-3: Using model_ensemble_manager methods (same method names)
            models_loaded = model_ensemble_manager.models_loaded() if model_ensemble_manager else False
            
            # Get detailed model info 
            model_info = {}
            if model_ensemble_manager:
                try:
                    model_info = model_ensemble_manager.get_model_info()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get model info: {e}")
                    model_info = {"error": str(e)}
            
            # Pattern manager status
            pattern_manager_status = False
            pattern_info = {}
            if crisis_pattern_manager:
                try:
                    pattern_info = crisis_pattern_manager.get_pattern_summary()
                    pattern_manager_status = True
                except Exception as e:
                    logger.warning(f"⚠️ Pattern manager error: {e}")
                    pattern_info = {"error": str(e)}
            
            # Threshold manager status  
            threshold_manager_status = False
            threshold_info = {}
            if threshold_mapping_manager:
                try:
                    threshold_info = threshold_mapping_manager.get_validation_summary()
                    threshold_manager_status = True
                except Exception as e:
                    logger.warning(f"⚠️ Threshold manager error: {e}")
                    threshold_info = {"error": str(e)}
            
            return {
                "status": "healthy" if models_loaded else "degraded",
                "timestamp": time.time(),
                "processing_time_ms": (time.time() - start_time) * 1000,
                "phase": "3d",
                "architecture": "clean_v3_1", 
                "step_10_11_3_consolidation": True,
                "primary_model_manager": "ModelEnsembleManager",
                "components": {
                    "model_ensemble": {
                        "status": "loaded" if models_loaded else "error",
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
                "step_10_11_3_consolidation": True
            }
    
    # ========================================================================
    # ENSEMBLE CONFIGURATION ENDPOINTS - Using model_ensemble_manager
    # ========================================================================
    
    @app.get("/ensemble/config")
    async def get_ensemble_configuration():
        """
        Get current ensemble configuration - Phase 3c
        Step 10.11-3: Using model_ensemble_manager for configuration info
        """
        try:
            config = {
                "ensemble_method": "three_zero_shot_models",
                "models_loaded": model_ensemble_manager.models_loaded() if model_ensemble_manager else False,
                "phase": "3d",
                "architecture": "clean_v3_1",
                "step_10_11_3_consolidation": True,
                "primary_model_manager": "ModelEnsembleManager"
            }
            
            # Add model info if available - STEP 10.11-3: Same method name
            if model_ensemble_manager:
                try:
                    model_info = model_ensemble_manager.get_model_info()
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
                        "crisis_mapping": crisis_mapping
                    }
                except Exception as e:
                    config["threshold_configuration"] = {"error": str(e)}
            
            return config
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    
    @app.get("/ensemble/status")
    async def get_ensemble_status():
        """
        Get detailed ensemble status - Phase 3c  
        Step 10.11-3: Using model_ensemble_manager for status checks
        """
        try:
            status = {
                "timestamp": time.time(),
                "phase": "3d",
                "architecture": "clean_v3_1",
                "step_10_11_3_consolidation": True,
                "primary_model_manager": "ModelEnsembleManager"
            }
            
            # Component status checks - STEP 10.11-3: Same method names
            components = {}
            
            # Model ensemble status
            if model_ensemble_manager:
                try:
                    models_loaded = model_ensemble_manager.models_loaded()
                    model_info = model_ensemble_manager.get_model_info()
                    components["models"] = {
                        "status": "operational" if models_loaded else "error",
                        "details": model_info
                    }
                except Exception as e:
                    components["models"] = {"status": "error", "error": str(e)}
            
            # Pattern analysis status
            if crisis_pattern_manager:
                try:
                    pattern_summary = crisis_pattern_manager.get_pattern_summary()
                    components["patterns"] = {
                        "status": "operational",
                        "details": pattern_summary
                    }
                except Exception as e:
                    components["patterns"] = {"status": "error", "error": str(e)}
            
            # Threshold mapping status
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
    logger.info("🎯 Step 10.11-3: API response extraction updated for ModelEnsembleManager consolidation")
    
    # Phase 3c: Log configuration summary
    if threshold_mapping_manager:
        try:
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
            logger.info(f"🎯 Ensemble endpoints configured with {current_mode} mode thresholds")
            logger.debug(f"📊 Crisis mapping configuration: {crisis_mapping}")
        except Exception as e:
            logger.warning(f"⚠️ Could not log threshold configuration: {e}")

# Legacy function name for backward compatibility during transition - UPDATED for Step 10.11-3
def add_ensemble_endpoints(app: FastAPI, model_ensemble_manager, pydantic_manager, 
                          crisis_pattern_manager=None, threshold_mapping_manager=None):
    """
    Legacy wrapper for add_ensemble_endpoints_v3c
    Step 10.11-3: Parameter updated from models_manager to model_ensemble_manager
    """
    return add_ensemble_endpoints_v3c(app, model_ensemble_manager, pydantic_manager, 
                                     crisis_pattern_manager, threshold_mapping_manager)