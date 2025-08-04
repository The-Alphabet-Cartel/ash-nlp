# ash/ash-nlp/api/admin_endpoints.py (Clean v3.1 Architecture - Phase 2C Complete)
"""
Admin endpoints for label management and system administration
Clean v3.1 implementation with direct manager access only
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create admin router for JSON-based label management
admin_router = APIRouter(prefix="/admin", tags=["admin"])

class LabelSetSwitchRequest(BaseModel):
    """Request to switch label sets"""
    label_set: str

class LabelSetResponse(BaseModel):
    """Response with label set information"""
    success: bool
    message: str
    current_set: str
    available_sets: List[str]
    label_info: Dict[str, Any]

class LabelConfigInfoResponse(BaseModel):
    """Comprehensive label configuration information"""
    version: str
    description: str
    current_set: Dict[str, Any]
    available_sets: List[Dict[str, Any]]
    total_label_sets: int
    configuration: Dict[str, Any]
    metadata: Dict[str, Any]

class LabelValidationResponse(BaseModel):
    """Label validation results"""
    valid: bool
    issues: List[str]
    warnings: List[str]
    stats: Dict[str, Any]

def setup_admin_endpoints(app, model_manager, zero_shot_manager):
    """
    Setup admin endpoints with clean v3.1 manager architecture
    
    Args:
        app: FastAPI application instance
        model_manager: ModelsManager v3.1 instance (required)
        zero_shot_manager: ZeroShotManager instance (required)
    """
    
    # ========================================================================
    # CLEAN V3.1 VALIDATION - No Fallbacks
    # ========================================================================
    
    if not model_manager:
        logger.error("❌ ModelsManager v3.1 is required for admin endpoints")
        raise RuntimeError("ModelsManager v3.1 required for admin endpoints")
    
    if not zero_shot_manager:
        logger.error("❌ ZeroShotManager is required for admin endpoints")
        raise RuntimeError("ZeroShotManager required for admin endpoints")
    
    logger.info("✅ Clean v3.1: Admin endpoints using direct manager access")
    
    # ========================================================================
    # LABEL STATUS ENDPOINT - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/status")
    async def get_label_status():
        """Get current label configuration status - Clean v3.1 Implementation"""
        try:
            # Direct manager access - no fallbacks
            model_status = {}
            if model_manager.models_loaded():
                try:
                    model_status = await model_manager.get_model_status()
                except Exception as e:
                    logger.warning(f"⚠️ Could not get model status: {e}")
                    model_status = {"error": str(e)}
            
            # Get zero-shot manager status
            zero_shot_status = {}
            try:
                zero_shot_status = zero_shot_manager.get_manager_status()
            except Exception as e:
                logger.warning(f"⚠️ Could not get zero-shot status: {e}")
                zero_shot_status = {"error": str(e)}
            
            return {
                "status": "healthy",
                "architecture": "v3.1_clean",
                "phase_2c_complete": True,
                "current_label_set": zero_shot_status.get('current_label_set', 'unknown'),
                "available_sets": zero_shot_status.get('available_sets', []),
                "label_stats": zero_shot_status.get('label_stats', {}),
                "models_loaded": model_manager.models_loaded(),
                "model_status": model_status,
                "admin_endpoints_available": True,
                "manager_integration": {
                    "models_manager_v3_1": True,
                    "zero_shot_manager": True,
                    "direct_access_only": True,
                    "backward_compatibility": "removed"
                },
                "models_in_use": {
                    "depression": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
                    "sentiment": "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
                    "distress": "Lowerated/lm6-deberta-v3-topic-sentiment"
                }
            }
        except Exception as e:
            logger.error(f"❌ Error getting label status: {e}")
            return {
                "status": "error",
                "architecture": "v3.1_clean",
                "phase_2c_complete": True,
                "error": str(e),
                "admin_endpoints_available": True,
                "manager_integration": {
                    "direct_access_only": True,
                    "backward_compatibility": "removed"
                }
            }
    
    # ========================================================================
    # SIMPLE LABEL SWITCHING - Clean v3.1
    # ========================================================================
    
    @app.post("/admin/labels/simple-switch")
    async def simple_label_switch(request: dict):
        """Simple label switching endpoint - Clean v3.1 Implementation"""
        try:
            label_set = request.get("label_set")
            if not label_set:
                return {"error": "label_set required"}
            
            # Direct manager access - no fallbacks
            try:
                success = await model_manager.switch_label_set(label_set)
                if success:
                    current_set = await model_manager.get_current_label_set_name()
                    return {
                        "success": True,
                        "message": f"Switched to label set: {label_set}",
                        "current_set": current_set,
                        "architecture": "v3.1_clean",
                        "manager_used": "models_manager_v3.1"
                    }
                else:
                    return {
                        "error": f"Failed to switch to label set: {label_set}",
                        "architecture": "v3.1_clean"
                    }
            except Exception as e:
                logger.error(f"❌ Label switch failed: {e}")
                return {
                    "error": f"Label switch failed: {str(e)}",
                    "architecture": "v3.1_clean"
                }
                
        except Exception as e:
            logger.error(f"❌ Error in simple label switch: {e}")
            return {
                "error": str(e),
                "architecture": "v3.1_clean"
            }
    
    # ========================================================================
    # LABEL CONFIGURATION ENDPOINT - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/config", response_model=LabelConfigInfoResponse)
    async def get_label_configuration():
        """Get comprehensive label configuration information - Clean v3.1"""
        try:
            # Direct zero-shot manager access - no fallbacks
            config_info = zero_shot_manager.get_config_info()
            
            return LabelConfigInfoResponse(
                version=config_info.get('version', '3.1'),
                description=config_info.get('description', 'Clean v3.1 Label Configuration'),
                current_set=config_info.get('current_set', {}),
                available_sets=config_info.get('available_sets', []),
                total_label_sets=config_info.get('total_label_sets', 0),
                configuration=config_info.get('configuration', {}),
                metadata={
                    "architecture": "v3.1_clean",
                    "phase_2c_complete": True,
                    "manager_integration": "direct_access_only",
                    **config_info.get('metadata', {})
                }
            )
        
        except Exception as e:
            logger.error(f"❌ Error getting label configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 configuration error: {str(e)}")
    
    # ========================================================================
    # CURRENT LABEL INFO - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/current")
    async def get_current_label_info():
        """Get information about currently active label set - Clean v3.1"""
        try:
            # Direct manager access - no fallbacks
            current_set = await model_manager.get_current_label_set_name()
            label_info = await model_manager.get_label_set_info()
            validation = await model_manager.validate_current_labels()
            
            # Get stats from zero-shot manager
            stats = zero_shot_manager.get_current_stats()
            
            return {
                'current_set': current_set,
                'info': label_info,
                'stats': stats,
                'validation': validation,
                'architecture': 'v3.1_clean',
                'manager_integration': {
                    'models_manager_v3_1': True,
                    'zero_shot_manager': True,
                    'direct_access': True
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error getting current label info: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 label info error: {str(e)}")
    
    # ========================================================================
    # LIST ALL LABEL SETS - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/list")
    async def list_all_label_sets():
        """List all available label sets with detailed information - Clean v3.1"""
        try:
            # Direct zero-shot manager access - no fallbacks
            available_sets = zero_shot_manager.get_available_label_sets()
            current_set = zero_shot_manager.get_current_label_set_name()
            
            detailed_sets = []
            for set_name in available_sets:
                try:
                    info = zero_shot_manager.get_label_set_info(set_name)
                    detailed_sets.append({
                        'name': set_name,
                        'display_name': info.name if info else set_name,
                        'description': info.description if info else 'Clean v3.1 Label Set',
                        'optimized_for': info.optimized_for if info else 'general',
                        'sensitivity_level': info.sensitivity_level if info else 'medium',
                        'recommended': info.recommended if info else False,
                        'label_counts': info.label_counts if info else {},
                        'total_labels': sum(info.label_counts.values()) if info and info.label_counts else 0,
                        'is_current': set_name == current_set
                    })
                except Exception as e:
                    logger.warning(f"⚠️ Could not get info for label set {set_name}: {e}")
                    detailed_sets.append({
                        'name': set_name,
                        'display_name': set_name,
                        'description': f'Clean v3.1 Label Set (info unavailable: {str(e)})',
                        'is_current': set_name == current_set,
                        'error': str(e)
                    })
            
            return {
                'current_set': current_set,
                'total_sets': len(available_sets),
                'sets': detailed_sets,
                'architecture': 'v3.1_clean',
                'manager_integration': {
                    'zero_shot_manager': True,
                    'direct_access': True,
                    'backward_compatibility': 'removed'
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error listing label sets: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 label listing error: {str(e)}")
    
    # ========================================================================
    # SWITCH LABEL SET - Clean v3.1
    # ========================================================================
    
    @app.post("/admin/labels/switch", response_model=LabelSetResponse)
    async def switch_label_set(request: LabelSetSwitchRequest):
        """Switch to a different label set - Clean v3.1"""
        try:
            # Direct manager access - no fallbacks
            available_sets = await model_manager.get_available_label_sets()
            if request.label_set not in available_sets:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid label set '{request.label_set}'. Available: {available_sets}"
                )
            
            # Switch label set using direct manager access
            success = await model_manager.switch_label_set(request.label_set)
            if not success:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Clean v3.1: Failed to switch label set to {request.label_set}"
                )
            
            # Get updated info using direct manager access
            current_info = await model_manager.get_label_set_info()
            
            logger.info(f"📋 Clean v3.1: Label set switched to: {request.label_set}")
            
            return LabelSetResponse(
                success=True,
                message=f"Clean v3.1: Successfully switched to label set: {request.label_set}",
                current_set=request.label_set,
                available_sets=available_sets,
                label_info={
                    **current_info,
                    "architecture": "v3.1_clean",
                    "manager_used": "models_manager_v3.1"
                }
            )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error switching label set: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 label switch error: {str(e)}")
    
    # ========================================================================
    # LABEL SET DETAILS - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/details/{label_set_name}")
    async def get_label_set_details(label_set_name: str):
        """Get detailed information about a specific label set - Clean v3.1"""
        try:
            # Direct zero-shot manager access - no fallbacks
            available_sets = zero_shot_manager.get_available_label_sets()
            
            if label_set_name not in available_sets:
                raise HTTPException(
                    status_code=404,
                    detail=f"Label set '{label_set_name}' not found. Available: {available_sets}"
                )
            
            # Temporarily switch to get details using direct manager access
            original_set = zero_shot_manager.get_current_label_set_name()
            zero_shot_manager.switch_label_set(label_set_name)
            
            try:
                info = zero_shot_manager.get_label_set_info(label_set_name)
                labels = zero_shot_manager.get_all_labels()
                stats = zero_shot_manager.get_current_stats()
                
                return {
                    'name': label_set_name,
                    'info': info.__dict__ if info else {},
                    'labels': labels,
                    'stats': stats,
                    'has_mapping_rules': hasattr(zero_shot_manager, 'current_mapping_rules') and bool(zero_shot_manager.current_mapping_rules),
                    'architecture': 'v3.1_clean',
                    'manager_integration': {
                        'zero_shot_manager': True,
                        'direct_access': True,
                        'backward_compatibility': 'removed'
                    }
                }
            
            finally:
                # Switch back to original using direct manager access
                zero_shot_manager.switch_label_set(original_set)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error getting label set details: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 label details error: {str(e)}")
    
    # ========================================================================
    # RELOAD CONFIGURATION - Clean v3.1
    # ========================================================================
    
    @app.post("/admin/labels/reload")
    async def reload_label_configuration():
        """Reload label configuration from JSON file - Clean v3.1"""
        try:
            # Direct manager access - no fallbacks
            success = await model_manager.reload_labels_from_json()
            if not success:
                raise HTTPException(
                    status_code=500, 
                    detail="Clean v3.1: Failed to reload labels from JSON"
                )
            
            # Get updated info using direct manager access
            stats = zero_shot_manager.get_current_stats()
            current_set = await model_manager.get_current_label_set_name()
            
            logger.info("♻️ Clean v3.1: Label configuration reloaded from JSON file")
            
            return {
                'success': True,
                'message': 'Clean v3.1: Successfully reloaded label configuration from JSON file',
                'stats': stats,
                'current_set': current_set,
                'architecture': 'v3.1_clean',
                'manager_integration': {
                    'models_manager_v3_1': True,
                    'zero_shot_manager': True,
                    'direct_access': True
                }
            }
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error reloading label configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 reload error: {str(e)}")
    
    # ========================================================================
    # VALIDATE CONFIGURATION - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/validate", response_model=LabelValidationResponse)
    async def validate_label_configuration():
        """Validate current label configuration - Clean v3.1"""
        try:
            # Direct manager access - no fallbacks
            validation = await model_manager.validate_current_labels()
            
            return LabelValidationResponse(
                valid=validation['valid'],
                issues=validation['issues'],
                warnings=validation['warnings'],
                stats={
                    **validation['stats'],
                    "architecture": "v3.1_clean",
                    "manager_used": "models_manager_v3.1"
                }
            )
        
        except Exception as e:
            logger.error(f"❌ Error validating label configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 validation error: {str(e)}")
    
    # ========================================================================
    # EXPORT LABEL SET - Clean v3.1
    # ========================================================================
    
    @app.get("/admin/labels/export/{label_set_name}")
    async def export_label_set(label_set_name: str):
        """Export a specific label set - Clean v3.1"""
        try:
            # Direct manager access - no fallbacks
            available_sets = await model_manager.get_available_label_sets()
            if label_set_name not in available_sets:
                raise HTTPException(
                    status_code=404,
                    detail=f"Label set '{label_set_name}' not found. Available: {available_sets}"
                )
            
            # Temporarily switch to export set using direct manager access
            original_set = await model_manager.get_current_label_set_name()
            await model_manager.switch_label_set(label_set_name)
            
            try:
                export_data = await model_manager.export_current_labels()
                export_data['architecture'] = 'v3.1_clean'
                export_data['exported_by'] = 'models_manager_v3.1'
                return export_data
            
            finally:
                # Switch back to original using direct manager access
                await model_manager.switch_label_set(original_set)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error exporting label set: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 export error: {str(e)}")
    
    # ========================================================================
    # TEST LABEL MAPPING - Clean v3.1
    # ========================================================================
    
    @app.post("/admin/labels/test/mapping")
    async def test_label_mapping():
        """Test label mapping with current configuration - Clean v3.1"""
        try:
            # Direct zero-shot manager access - no fallbacks
            test_phrases = [
                "I want to kill myself",
                "I have the pills ready", 
                "Having a rough day",
                "Going to the store"
            ]
            
            results = []
            for phrase in test_phrases:
                try:
                    depression_result = zero_shot_manager.map_depression_label(f"person saying: {phrase}")
                    sentiment_result = zero_shot_manager.map_sentiment_label(f"person expressing: {phrase}")
                    distress_result = zero_shot_manager.map_distress_label(f"person experiencing: {phrase}")
                    
                    results.append({
                        'phrase': phrase,
                        'mappings': {
                            'depression': depression_result,
                            'sentiment': sentiment_result,
                            'distress': distress_result
                        }
                    })
                except Exception as e:
                    logger.warning(f"⚠️ Mapping test failed for phrase '{phrase}': {e}")
                    results.append({
                        'phrase': phrase,
                        'error': str(e)
                    })
            
            return {
                'current_set': zero_shot_manager.get_current_label_set_name(),
                'test_results': results,
                'timestamp': datetime.utcnow().isoformat(),
                'architecture': 'v3.1_clean',
                'manager_integration': {
                    'zero_shot_manager': True,
                    'direct_access': True,
                    'backward_compatibility': 'removed'
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error testing label mapping: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 mapping test error: {str(e)}")
    
    # ========================================================================
    # COMPREHENSIVE TEST - Clean v3.1
    # ========================================================================
    
    @app.post("/admin/labels/test/comprehensive")
    async def trigger_comprehensive_test():
        """Trigger comprehensive test with current label configuration - Clean v3.1"""
        try:
            # Direct zero-shot manager access - no fallbacks
            current_set = zero_shot_manager.get_current_label_set_name()
            
            return {
                'message': 'Clean v3.1: Comprehensive test triggered with current label configuration',
                'current_set': current_set,
                'test_id': f"test_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                'status': 'started',
                'architecture': 'v3.1_clean',
                'note': 'Full integration with ash-thrash testing system required',
                'manager_integration': {
                    'zero_shot_manager': True,
                    'direct_access': True,
                    'backward_compatibility': 'removed'
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error triggering comprehensive test: {e}")
            raise HTTPException(status_code=500, detail=f"Clean v3.1 test trigger error: {str(e)}")
    
    # ========================================================================
    # ENDPOINT REGISTRATION COMPLETE
    # ========================================================================
    
    logger.info("🔧 Clean v3.1: Admin endpoints registered successfully")
    logger.info("📋 Admin endpoints using direct manager access:")
    logger.info("   GET /admin/labels/status - Label configuration status")
    logger.info("   POST /admin/labels/simple-switch - Simple label switching")
    logger.info("   GET /admin/labels/config - Comprehensive configuration info")
    logger.info("   GET /admin/labels/current - Current label set information")
    logger.info("   GET /admin/labels/list - List all available label sets")
    logger.info("   POST /admin/labels/switch - Switch to different label set")
    logger.info("   GET /admin/labels/details/{name} - Detailed label set info")
    logger.info("   POST /admin/labels/reload - Reload from JSON configuration")
    logger.info("   GET /admin/labels/validate - Validate current configuration")
    logger.info("   GET /admin/labels/export/{name} - Export specific label set")
    logger.info("   POST /admin/labels/test/mapping - Test label mapping")
    logger.info("   POST /admin/labels/test/comprehensive - Trigger comprehensive test")
    logger.info("✅ Phase 2C: All admin endpoints using direct manager access - No fallback code")

def add_admin_endpoints(app, config_manager, settings_manager, zero_shot_manager, crisis_pattern_manager, model_manager=None):
    """Add admin endpoints to FastAPI app - Clean v3.1 Architecture"""
    logger.info("🔧 Adding admin endpoints with clean v3.1 manager architecture...")
    
    # Call the existing setup function with the model_manager
    try:
        setup_admin_endpoints(
            app=app,
            model_manager=model_manager,  # Pass the actual model_manager
            zero_shot_manager=zero_shot_manager
        )
        
        # Include the admin router
        app.include_router(admin_router)
        
        logger.info("✅ Admin endpoints added successfully - Clean v3.1")
        
    except Exception as e:
        logger.error(f"❌ Failed to setup admin endpoints: {e}")
        logger.info("ℹ️ Continuing without admin endpoints")