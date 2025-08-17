# ash/ash-nlp/api/admin_endpoints.py
"""
Admin endpoints for label management and system administration for Ash NLP Service v3.1
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-13
CLEAN ARCHITECTURE: v3.1 Compliant
PHASE: 3d, Step 10.11-3
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
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

def setup_admin_endpoints(app, model_ensemble_manager, zero_shot_manager, crisis_pattern_manager=None,
                         analysis_parameters_manager=None, threshold_mapping_manager=None):
    """
    Setup admin endpoints with complete Phase 3c manager architecture
    
    Args:
        app: FastAPI application instance
        model_ensemble_manager: Model Ensemble Manager instance (required)
        zero_shot_manager: ZeroShotManager instance (required)
        crisis_pattern_manager: CrisisPatternManager instance (Phase 3a)
        analysis_parameters_manager: AnalysisParametersManager instance (Phase 3b) - NEW
        threshold_mapping_manager: ThresholdMappingManager instance (Phase 3c) - NEW
    """
    
    # ========================================================================
    # CLEAN V3.1 VALIDATION - No Fallbacks
    # ========================================================================
    
    if not model_ensemble_manager:
        logger.error("❌ Model Ensemble Manager is required for admin endpoints")
        raise RuntimeError("Model Ensemble Manager required for admin endpoints")
    
    if not zero_shot_manager:
        logger.error("❌ ZeroShotManager is required for admin endpoints")
        raise RuntimeError("ZeroShotManager required for admin endpoints")
    
    logger.info("✅ Clean v3.1: Admin endpoints using direct manager access - Phase 3c Enhanced")
    
    # ========================================================================
    # ENHANCED ADMIN STATUS ENDPOINT - REPLACE EXISTING @app.get("/admin/status")
    # ========================================================================
    
    @app.get("/admin/status")
    async def admin_status():
        """Get comprehensive admin status - Phase 3c Enhanced"""
        try:
            status = {
                "admin_available": True,
                "phase": "3c",
                "architecture": "clean_v3.1_with_phase_3c_integration",
                "endpoints": [
                    "/admin/status",
                    "/admin/configuration/summary",  # New Phase 3c endpoint
                    "/admin/thresholds/status",      # New Phase 3c endpoint
                    "/admin/analysis/parameters",    # New Phase 3b endpoint
                    "/admin/labels/status",
                    "/admin/labels/current",
                    "/admin/labels/list",
                    "/admin/labels/switch"
                ],
                "managers": {
                    "zero_shot_manager": zero_shot_manager is not None,
                    "model_ensemble_manager": model_ensemble_manager is not None,
                    "crisis_pattern_manager": crisis_pattern_manager is not None,
                    "analysis_parameters_manager": analysis_parameters_manager is not None,
                    "threshold_mapping_manager": threshold_mapping_manager is not None
                }
            }
            
            # Phase 3a - Crisis Pattern Manager Status
            if crisis_pattern_manager:
                try:
                    pattern_status = crisis_pattern_manager.get_status()
                    status["crisis_patterns"] = {
                        "loaded_patterns": pattern_status.get('loaded_pattern_sets', 0),
                        "available": True,
                        "phase_3a_integrated": True
                    }
                except Exception as e:
                    status["crisis_patterns"] = {"available": False, "error": str(e)}
            else:
                status["crisis_patterns"] = {"available": False, "note": "Crisis pattern manager not provided"}
            
            # Phase 3b - Analysis Parameters Manager Status - NEW
            if analysis_parameters_manager:
                try:
                    all_params = analysis_parameters_manager.get_all_parameters()
                    status["analysis_parameters"] = {
                        "categories": len(all_params),
                        "available": True,
                        "phase_3b_integrated": True,
                        "externalized": True
                    }
                except Exception as e:
                    status["analysis_parameters"] = {"available": False, "error": str(e)}
            else:
                status["analysis_parameters"] = {"available": False, "note": "Analysis parameters manager not provided"}
            
            # Phase 3c - Threshold Mapping Manager Status - NEW
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    status["threshold_mapping"] = {
                        "current_mode": current_mode,
                        "available": True,
                        "phase_3c_integrated": True,
                        "mode_aware": True
                    }
                except Exception as e:
                    status["threshold_mapping"] = {"available": False, "error": str(e)}
            else:
                status["threshold_mapping"] = {"available": False, "note": "Threshold mapping manager not provided"}
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Error getting admin status: {e}")
            return {"error": str(e), "admin_available": False, "phase": "3c"}

    # ========================================================================
    # NEW Phase 3c Configuration Summary Endpoint - ADD THIS
    # ========================================================================
    
    @app.get("/admin/configuration/summary")
    async def configuration_summary():
        """Get complete configuration summary - Phase 3c"""
        try:
            summary = {
                "phase": "3c",
                "architecture": "clean_v3.1",
                "configuration_externalized": True,
                "components": {}
            }
            
            # Phase 3a - Crisis Patterns
            if crisis_pattern_manager:
                try:
                    pattern_status = crisis_pattern_manager.get_status()
                    summary["components"]["crisis_patterns"] = {
                        "source": "JSON configuration",
                        "status": "externalized",
                        "manager": "CrisisPatternManager",
                        "loaded_patterns": pattern_status.get('loaded_pattern_sets', 0)
                    }
                except Exception as e:
                    summary["components"]["crisis_patterns"] = {"error": str(e)}
            
            # Phase 3b - Analysis Parameters
            if analysis_parameters_manager:
                try:
                    all_params = analysis_parameters_manager.get_all_parameters()
                    summary["components"]["analysis_parameters"] = {
                        "source": "JSON configuration + environment overrides",
                        "status": "externalized",
                        "categories": list(all_params.keys()),
                        "manager": "AnalysisParametersManager"
                    }
                except Exception as e:
                    summary["components"]["analysis_parameters"] = {"error": str(e)}
            
            # Phase 3c - Threshold Mapping
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    crisis_thresholds = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                    summary["components"]["threshold_mapping"] = {
                        "source": "JSON configuration + environment overrides",
                        "status": "externalized",
                        "current_mode": current_mode,
                        "crisis_levels": list(crisis_thresholds.keys()),
                        "manager": "ThresholdMappingManager"
                    }
                except Exception as e:
                    summary["components"]["threshold_mapping"] = {"error": str(e)}
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error getting configuration summary: {e}")
            raise HTTPException(status_code=500, detail=f"Configuration summary error: {str(e)}")

    # ========================================================================
    # NEW Phase 3c Threshold Status Endpoint - ADD THIS
    # ========================================================================
    
    @app.get("/admin/thresholds/status")
    async def threshold_status():
        """Get detailed threshold configuration status - Phase 3c"""
        try:
            if not threshold_mapping_manager:
                return {
                    "status": "not_available",
                    "message": "ThresholdMappingManager not provided",
                    "phase_3c_integrated": False
                }
            
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            crisis_thresholds = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
            staff_review_config = threshold_mapping_manager.get_staff_review_config()
            
            return {
                "status": "available",
                "current_mode": current_mode,
                "crisis_thresholds": crisis_thresholds,
                "staff_review": staff_review_config,
                "mode_aware": True,
                "configuration_source": "JSON + environment overrides",
                "phase_3c_complete": True
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting threshold status: {e}")
            raise HTTPException(status_code=500, detail=f"Threshold status error: {str(e)}")

    # ========================================================================
    # NEW Phase 3b Analysis Parameters Endpoint - ADD THIS
    # ========================================================================
    
    @app.get("/admin/analysis/parameters")
    async def analysis_parameters():
        """Get analysis parameters configuration - Phase 3b"""
        try:
            if not analysis_parameters_manager:
                return {
                    "status": "not_available",
                    "message": "AnalysisParametersManager not provided",
                    "phase_3b_integrated": False
                }
            
            all_params = analysis_parameters_manager.get_all_parameters()
            
            return {
                "status": "available",
                "parameters": all_params,
                "configuration_source": "JSON + environment overrides",
                "externalized": True,
                "phase_3b_complete": True
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting analysis parameters: {e}")
            raise HTTPException(status_code=500, detail=f"Analysis parameters error: {str(e)}")

    # ========================================================================
    # LABEL STATUS ENDPOINT - Clean v3.1 (Keep - This one works)
    # ========================================================================
    
    @app.get("/admin/labels/status")
    async def get_label_status():
        """Get current label configuration status - Clean v3.1 Implementation"""
        try:
            model_status = {}
            if model_ensemble_manager.models_loaded():
                try:
                    model_status = model_ensemble_manager.get_model_info()
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
                "models_loaded": model_ensemble_manager.models_loaded(),
                "model_status": model_status,
                "admin_endpoints_available": True,
                "manager_integration": {
                    "model_ensemble_manager": True,
                    "zero_shot_manager": True,
                    "direct_access_only": True,
                    "backward_compatibility": "removed"
                },
                "models_in_use": {
                    "depression": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
                    "sentiment": "Lowerated/lm6-deberta-v3-topic-sentiment",
                    "distress": "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
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
    # CURRENT LABEL INFO - FIXED
    # ========================================================================
    
    @app.get("/admin/labels/current")
    async def get_current_label_info():
        """Get information about currently active label set - FIXED"""
        try:
            # FIXED: Use zero_shot_manager with correct method name (no await)
            current_set = zero_shot_manager.get_current_label_set()
            
            # Get additional info from zero_shot_manager
            all_labels = zero_shot_manager.get_all_labels()
            manager_status = zero_shot_manager.get_manager_status()
            
            return {
                'current_set': current_set,
                'labels': all_labels,
                'stats': manager_status,
                'architecture': 'v3.1_clean_fixed',
                'manager_integration': {
                    'zero_shot_manager': True,
                    'direct_access': True
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error getting current label info: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 label info error: {str(e)}")

    # ========================================================================
    # LIST ALL LABEL SETS - FIXED
    # ========================================================================
    
    @app.get("/admin/labels/list")
    async def list_all_label_sets():
        """List all available label sets with detailed information - FIXED"""
        try:
            # FIXED: Use zero_shot_manager with correct method names (no await)
            available_sets = zero_shot_manager.get_available_label_sets()
            current_set = zero_shot_manager.get_current_label_set()
            
            detailed_sets = []
            for set_name in available_sets:
                detailed_sets.append({
                    'name': set_name,
                    'display_name': set_name,
                    'description': f'Label Set: {set_name}',
                    'is_current': set_name == current_set
                })
            
            return {
                'current_set': current_set,
                'total_sets': len(available_sets),
                'sets': detailed_sets,
                'architecture': 'v3.1_clean_fixed',
                'manager_integration': {
                    'zero_shot_manager': True,
                    'direct_access': True,
                    'backward_compatibility': 'removed'
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error listing label sets: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 label listing error: {str(e)}")

    # ========================================================================
    # SIMPLE LABEL SWITCHING - FIXED
    # ========================================================================
    
    @app.post("/admin/labels/simple-switch")
    async def simple_label_switch(request: dict):
        """Simple label switching endpoint - FIXED"""
        try:
            label_set = request.get("label_set")
            if not label_set:
                return {"error": "label_set required"}
            
            # FIXED: Use zero_shot_manager (no await, correct method)
            try:
                success = zero_shot_manager.switch_label_set(label_set)
                if success:
                    current_set = zero_shot_manager.get_current_label_set()
                    return {
                        "success": True,
                        "message": f"Switched to label set: {label_set}",
                        "current_set": current_set,
                        "architecture": "v3.1_clean_fixed",
                        "manager_used": "zero_shot_manager"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to switch to label set: {label_set}",
                        "architecture": "v3.1_clean_fixed"
                    }
            except Exception as e:
                logger.error(f"❌ Label switch failed: {e}")
                return {
                    "success": False,
                    "error": f"Label switch failed: {str(e)}",
                    "architecture": "v3.1_clean_fixed"
                }
                
        except Exception as e:
            logger.error(f"❌ Error in simple label switch: {e}")
            return {
                "success": False,
                "error": str(e),
                "architecture": "v3.1_clean_fixed"
            }

    # ========================================================================
    # FULL LABEL SWITCHING - FIXED
    # ========================================================================
    
    @app.post("/admin/labels/switch", response_model=LabelSetResponse)
    async def switch_label_set(request: LabelSetSwitchRequest):
        """Switch to a different label set - FIXED"""
        try:
            # FIXED: Use zero_shot_manager (no await, correct methods)
            available_sets = zero_shot_manager.get_available_label_sets()
            if request.label_set not in available_sets:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid label set '{request.label_set}'. Available: {available_sets}"
                )
            
            # FIXED: Switch label set using zero_shot_manager
            success = zero_shot_manager.switch_label_set(request.label_set)
            if not success:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Fixed v3.1: Failed to switch label set to {request.label_set}"
                )
            
            # Get updated info
            current_labels = zero_shot_manager.get_all_labels()
            
            logger.info(f"📋 Fixed v3.1: Label set switched to: {request.label_set}")
            
            return LabelSetResponse(
                success=True,
                message=f"Fixed v3.1: Successfully switched to label set: {request.label_set}",
                current_set=request.label_set,
                available_sets=available_sets,
                label_info={
                    "labels": current_labels,
                    "architecture": "v3.1_clean_fixed",
                    "manager_used": "zero_shot_manager"
                }
            )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error switching label set: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 label switch error: {str(e)}")

    # ========================================================================
    # LABEL CONFIGURATION - SIMPLIFIED (Remove get_config_info dependency)
    # ========================================================================
    
    @app.get("/admin/labels/config")
    async def get_label_configuration():
        """Get comprehensive label configuration information - SIMPLIFIED"""
        try:
            # FIXED: Build config info from available methods
            available_sets = zero_shot_manager.get_available_label_sets()
            current_set = zero_shot_manager.get_current_label_set()
            current_labels = zero_shot_manager.get_all_labels()
            manager_status = zero_shot_manager.get_manager_status()
            
            # Build detailed sets info
            detailed_sets = []
            for set_name in available_sets:
                detailed_sets.append({
                    'name': set_name,
                    'is_current': set_name == current_set,
                    'description': f'Label set: {set_name}'
                })
            
            return {
                'version': '3.1_fixed',
                'description': 'Fixed v3.1 Label Configuration - Using ZeroShotManager',
                'current_set': {
                    'name': current_set,
                    'labels': current_labels
                },
                'available_sets': detailed_sets,
                'total_label_sets': len(available_sets),
                'configuration': manager_status,
                'metadata': {
                    "architecture": "v3.1_clean_fixed",
                    "phase_3a_complete": True,
                    "manager_integration": "zero_shot_manager_direct",
                    "fixed_issues": ["method_names", "manager_usage", "async_await"]
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error getting label configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 configuration error: {str(e)}")

    # ========================================================================
    # LABEL VALIDATION - SIMPLIFIED
    # ========================================================================
    
    @app.get("/admin/labels/validate")
    async def validate_label_configuration():
        """Validate current label configuration - SIMPLIFIED"""
        try:
            # FIXED: Build validation from available methods
            current_set = zero_shot_manager.get_current_label_set()
            available_sets = zero_shot_manager.get_available_label_sets()
            current_labels = zero_shot_manager.get_all_labels()
            
            # Basic validation checks
            issues = []
            warnings = []
            
            if not current_set:
                issues.append("No current label set active")
            
            if current_set not in available_sets:
                issues.append(f"Current set '{current_set}' not in available sets")
            
            if not current_labels:
                issues.append("No labels loaded for current set")
            
            # Check label counts
            label_counts = {}
            total_labels = 0
            for model_type, labels in current_labels.items():
                count = len(labels) if labels else 0
                label_counts[model_type] = count
                total_labels += count
            
            if total_labels == 0:
                issues.append("No labels defined for any model")
            
            return {
                'valid': len(issues) == 0,
                'issues': issues,
                'warnings': warnings,
                'stats': {
                    'current_set': current_set,
                    'total_sets': len(available_sets),
                    'label_counts': label_counts,
                    'total_labels': total_labels,
                    "architecture": "v3.1_clean_fixed",
                    "manager_used": "zero_shot_manager"
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error validating label configuration: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 validation error: {str(e)}")

    # ========================================================================
    # LABEL SET DETAILS - SIMPLIFIED
    # ========================================================================
    
    @app.get("/admin/labels/details/{label_set_name}")
    async def get_label_set_details(label_set_name: str):
        """Get detailed information about a specific label set - SIMPLIFIED"""
        try:
            # FIXED: Use zero_shot_manager with correct methods
            available_sets = zero_shot_manager.get_available_label_sets()
            
            if label_set_name not in available_sets:
                raise HTTPException(
                    status_code=404,
                    detail=f"Label set '{label_set_name}' not found. Available: {available_sets}"
                )
            
            # Temporarily switch to get details
            original_set = zero_shot_manager.get_current_label_set()
            zero_shot_manager.switch_label_set(label_set_name)
            
            try:
                labels = zero_shot_manager.get_all_labels()
                manager_status = zero_shot_manager.get_manager_status()
                
                return {
                    'name': label_set_name,
                    'labels': labels,
                    'stats': manager_status,
                    'architecture': 'v3.1_clean_fixed',
                    'manager_integration': {
                        'zero_shot_manager': True,
                        'direct_access': True
                    }
                }
            
            finally:
                # Switch back to original
                zero_shot_manager.switch_label_set(original_set)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error getting label set details: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 label details error: {str(e)}")

    # ========================================================================
    # EXPORT LABEL SET - SIMPLIFIED
    # ========================================================================
    
    @app.get("/admin/labels/export/{label_set_name}")
    async def export_label_set(label_set_name: str):
        """Export a specific label set - SIMPLIFIED"""
        try:
            # FIXED: Use zero_shot_manager
            available_sets = zero_shot_manager.get_available_label_sets()
            if label_set_name not in available_sets:
                raise HTTPException(
                    status_code=404,
                    detail=f"Label set '{label_set_name}' not found. Available: {available_sets}"
                )
            
            # Temporarily switch to export set
            original_set = zero_shot_manager.get_current_label_set()
            zero_shot_manager.switch_label_set(label_set_name)
            
            try:
                export_data = {
                    'label_set_name': label_set_name,
                    'labels': zero_shot_manager.get_all_labels(),
                    'stats': zero_shot_manager.get_manager_status(),
                    'exported_at': datetime.utcnow().isoformat(),
                    'architecture': 'v3.1_clean_fixed',
                    'exported_by': 'zero_shot_manager'
                }
                return export_data
            
            finally:
                # Switch back to original
                zero_shot_manager.switch_label_set(original_set)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error exporting label set: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 export error: {str(e)}")

    # ========================================================================
    # RELOAD CONFIGURATION - SIMPLIFIED 
    # ========================================================================
    
    @app.post("/admin/labels/reload")
    async def reload_label_configuration():
        """Reload label configuration - SIMPLIFIED"""
        try:
            # For now, just return current status - full reload would need config_manager
            current_set = zero_shot_manager.get_current_label_set()
            available_sets = zero_shot_manager.get_available_label_sets()
            
            return {
                'message': 'Configuration status retrieved (full reload not implemented)',
                'current_set': current_set,
                'available_sets': available_sets,
                'reload_timestamp': datetime.utcnow().isoformat(),
                'architecture': 'v3.1_clean_fixed',
                'note': 'Full configuration reload requires config_manager integration'
            }
        
        except Exception as e:
            logger.error(f"❌ Error in configuration reload: {e}")
            raise HTTPException(status_code=500, detail=f"Fixed v3.1 reload error: {str(e)}")

    # ========================================================================
    # ENDPOINT REGISTRATION COMPLETE - FIXED
    # ========================================================================
    
    logger.info("🔧 Fixed v3.1: Admin endpoints registered successfully")
    logger.info("📋 Admin endpoints using correct managers and methods:")
    logger.info("   GET /admin/status - Admin system status")
    logger.info("   GET /admin/labels/status - Label configuration status")
    logger.info("   GET /admin/labels/current - Current label set information")
    logger.info("   GET /admin/labels/list - List all available label sets")
    logger.info("   POST /admin/labels/simple-switch - Simple label switching")
    logger.info("   POST /admin/labels/switch - Full label switching")
    logger.info("   GET /admin/labels/details/{name} - Detailed label set info")
    logger.info("   GET /admin/labels/export/{name} - Export specific label set")
    logger.info("   POST /admin/labels/reload - Configuration reload status")
    logger.info("✅ Fixed: All admin endpoints using correct manager methods")

# ========================================================================
# Enhanced Admin Endpoints Function Signature
# ========================================================================
def add_admin_endpoints(app, config_manager, settings_manager, zero_shot_manager, crisis_pattern_manager, 
                       model_ensemble_manager, analysis_parameters_manager=None, threshold_mapping_manager=None):
    """Add admin endpoints to FastAPI app - Phase 3c Enhanced"""
    logger.info("🔧 Adding admin endpoints with Phase 3c enhancement...")
    
    # Call the enhanced setup function with ALL managers
    try:
        setup_admin_endpoints(
            app=app,
            model_ensemble_manager=model_ensemble_manager,
            zero_shot_manager=zero_shot_manager,
            crisis_pattern_manager=crisis_pattern_manager,
            analysis_parameters_manager=analysis_parameters_manager,
            threshold_mapping_manager=threshold_mapping_manager
        )
        
        # Include the admin router
        app.include_router(admin_router)
        
        logger.info("✅ Admin endpoints added successfully - Phase 3c Enhanced")
        logger.info("🆕 New endpoints: /admin/configuration/summary, /admin/thresholds/status, /admin/analysis/parameters")
        
    except Exception as e:
        logger.error(f"❌ Failed to setup admin endpoints: {e}")
        logger.info("ℹ️ Continuing without admin endpoints")