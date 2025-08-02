# Add these endpoints to your main API file
# Location: ash/ash-nlp/api/admin_endpoints.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from models.ml_models import get_model_manager
from config.zero_shot_config import get_labels_config, reload_labels_config

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

@admin_router.get("/labels/config", response_model=LabelConfigInfoResponse)
async def get_label_configuration():
    """Get comprehensive label configuration information from JSON"""
    try:
        labels_config = get_labels_config()
        config_info = labels_config.get_config_info()
        
        return LabelConfigInfoResponse(
            version=config_info.get('version', '1.0'),
            description=config_info.get('description', ''),
            current_set=config_info.get('current_set', {}),
            available_sets=config_info.get('available_sets', []),
            total_label_sets=config_info.get('total_label_sets', 0),
            configuration=config_info.get('configuration', {}),
            metadata=config_info.get('metadata', {})
        )
    
    except Exception as e:
        logger.error(f"Error getting label configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/labels/current")
async def get_current_label_info():
    """Get information about currently active label set"""
    try:
        model_manager = get_model_manager()
        if not model_manager:
            raise HTTPException(status_code=503, detail="Model manager not available")
        
        return {
            'current_set': model_manager.get_current_label_set_name(),
            'info': model_manager.get_label_set_info(),
            'stats': model_manager.labels_config.get_current_stats(),
            'validation': model_manager.validate_current_labels()
        }
    
    except Exception as e:
        logger.error(f"Error getting current label info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/labels/list")
async def list_all_label_sets():
    """List all available label sets with detailed information"""
    try:
        labels_config = get_labels_config()
        available_sets = labels_config.get_available_label_sets()
        current_set = labels_config.get_current_label_set_name()
        
        detailed_sets = []
        for set_name in available_sets:
            info = labels_config.get_label_set_info(set_name)
            detailed_sets.append({
                'name': set_name,
                'display_name': info.name if info else set_name,
                'description': info.description if info else '',
                'optimized_for': info.optimized_for if info else 'general',
                'sensitivity_level': info.sensitivity_level if info else 'medium',
                'recommended': info.recommended if info else False,
                'label_counts': info.label_counts if info else {},
                'total_labels': sum(info.label_counts.values()) if info and info.label_counts else 0,
                'is_current': set_name == current_set
            })
        
        return {
            'current_set': current_set,
            'total_sets': len(available_sets),
            'sets': detailed_sets
        }
    
    except Exception as e:
        logger.error(f"Error listing label sets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/labels/switch", response_model=LabelSetResponse)
async def switch_label_set(request: LabelSetSwitchRequest):
    """Switch to a different label set"""
    try:
        model_manager = get_model_manager()
        if not model_manager:
            raise HTTPException(status_code=503, detail="Model manager not available")
        
        # Validate label set name
        available_sets = model_manager.get_available_label_sets()
        if request.label_set not in available_sets:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid label set '{request.label_set}'. Available: {available_sets}"
            )
        
        # Switch label set
        success = model_manager.switch_label_set(request.label_set)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to switch label set")
        
        # Get updated info
        current_info = model_manager.get_label_set_info()
        
        logger.info(f"📋 Label set switched to: {request.label_set}")
        
        return LabelSetResponse(
            success=True,
            message=f"Successfully switched to label set: {request.label_set}",
            current_set=request.label_set,
            available_sets=available_sets,
            label_info=current_info
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error switching label set: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/labels/details/{label_set_name}")
async def get_label_set_details(label_set_name: str):
    """Get detailed information about a specific label set"""
    try:
        labels_config = get_labels_config()
        available_sets = labels_config.get_available_label_sets()
        
        if label_set_name not in available_sets:
            raise HTTPException(
                status_code=404,
                detail=f"Label set '{label_set_name}' not found. Available: {available_sets}"
            )
        
        # Temporarily switch to get details
        original_set = labels_config.get_current_label_set_name()
        labels_config.switch_label_set(label_set_name)
        
        try:
            info = labels_config.get_label_set_info(label_set_name)
            labels = labels_config.get_all_labels()
            stats = labels_config.get_current_stats()
            
            return {
                'name': label_set_name,
                'info': info.__dict__ if info else {},
                'labels': labels,
                'stats': stats,
                'has_mapping_rules': hasattr(labels_config, 'current_mapping_rules') and bool(labels_config.current_mapping_rules)
            }
        
        finally:
            # Switch back to original
            labels_config.switch_label_set(original_set)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting label set details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/labels/reload")
async def reload_label_configuration():
    """Reload label configuration from JSON file"""
    try:
        model_manager = get_model_manager()
        if not model_manager:
            raise HTTPException(status_code=503, detail="Model manager not available")
        
        # Reload from JSON file
        success = model_manager.reload_labels_from_json()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to reload labels from JSON")
        
        # Get updated info
        stats = model_manager.labels_config.get_current_stats()
        
        logger.info("♻️ Label configuration reloaded from JSON file")
        
        return {
            'success': True,
            'message': 'Successfully reloaded label configuration from JSON file',
            'stats': stats,
            'current_set': model_manager.get_current_label_set_name()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reloading label configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/labels/validate", response_model=LabelValidationResponse)
async def validate_label_configuration():
    """Validate current label configuration"""
    try:
        model_manager = get_model_manager()
        if not model_manager:
            raise HTTPException(status_code=503, detail="Model manager not available")
        
        validation = model_manager.validate_current_labels()
        
        return LabelValidationResponse(
            valid=validation['valid'],
            issues=validation['issues'],
            warnings=validation['warnings'],
            stats=validation['stats']
        )
    
    except Exception as e:
        logger.error(f"Error validating label configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.get("/labels/export/{label_set_name}")
async def export_label_set(label_set_name: str):
    """Export a specific label set"""
    try:
        model_manager = get_model_manager()
        if not model_manager:
            raise HTTPException(status_code=503, detail="Model manager not available")
        
        available_sets = model_manager.get_available_label_sets()
        if label_set_name not in available_sets:
            raise HTTPException(
                status_code=404,
                detail=f"Label set '{label_set_name}' not found. Available: {available_sets}"
            )
        
        # Temporarily switch to export set
        original_set = model_manager.get_current_label_set_name()
        model_manager.switch_label_set(label_set_name)
        
        try:
            export_data = model_manager.export_current_labels()
            return export_data
        
        finally:
            # Switch back to original
            model_manager.switch_label_set(original_set)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting label set: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/labels/test/mapping")
async def test_label_mapping():
    """Test label mapping with current configuration"""
    try:
        labels_config = get_labels_config()
        
        test_phrases = [
            "I want to kill myself",
            "I have the pills ready", 
            "Having a rough day",
            "Going to the store"
        ]
        
        results = []
        for phrase in test_phrases:
            depression_result = labels_config.map_depression_label(f"person saying: {phrase}")
            sentiment_result = labels_config.map_sentiment_label(f"person expressing: {phrase}")
            distress_result = labels_config.map_distress_label(f"person experiencing: {phrase}")
            
            results.append({
                'phrase': phrase,
                'mappings': {
                    'depression': depression_result,
                    'sentiment': sentiment_result,
                    'distress': distress_result
                }
            })
        
        return {
            'current_set': labels_config.get_current_label_set_name(),
            'test_results': results,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error testing label mapping: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/labels/test/comprehensive")
async def trigger_comprehensive_test():
    """Trigger comprehensive test with current label configuration"""
    try:
        # This would integrate with your ash-thrash testing system
        # For now, return placeholder
        return {
            'message': 'Comprehensive test triggered with current label configuration',
            'current_set': get_labels_config().get_current_label_set_name(),
            'test_id': f"test_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'status': 'started',
            'note': 'Full integration with ash-thrash testing system required'
        }
    
    except Exception as e:
        logger.error(f"Error triggering comprehensive test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Example of how to include this in your main app:
"""
from api.admin_endpoints import admin_router

app = FastAPI(title="Ash NLP Service")
app.include_router(admin_router)
"""