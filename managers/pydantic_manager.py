#!/usr/bin/env python3
# ash/ash-nlp/managers/pydantic_manager.py - Phase 2B Migration
"""
PydanticManager v3.1 - Clean Manager Architecture for Pydantic Models
Migrated from models/pydantic_models.py to follow the established manager pattern

Part of the Ash NLP Service v3.1 Clean Manager Architecture
Following the same successful pattern as ModelsManager v3.1
"""

import logging
from typing import Optional, Dict, List, Union, Any
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

class PydanticManager:
    """
    Manager class for all Pydantic models in the Ash NLP Service
    
    Provides centralized access to request/response models for:
    - Core analysis endpoints
    - Learning system endpoints
    - Health and statistics endpoints
    
    Follows the clean manager architecture established in Phase 2A
    """
    
    def __init__(self, config_manager=None):
        """
        Initialize PydanticManager with clean manager architecture
        
        Args:
            config_manager: ConfigManager instance for future configuration needs
        """
        self.config_manager = config_manager
        self._models_initialized = False
        
        logger.info("🏗️ PydanticManager v3.1 initializing with clean manager architecture...")
        
        # Initialize all model classes
        self._initialize_models()
        
        logger.info("✅ PydanticManager v3.1 initialized successfully")
    
    def _initialize_models(self):
        """Initialize all Pydantic model classes"""
        try:
            # Models are defined as inner classes for clean organization
            # This follows the manager pattern while keeping models accessible
            
            logger.debug("📋 Initializing Pydantic model definitions...")
            
            # All models are now available as class attributes
            self._models_initialized = True
            
            logger.debug("✅ All Pydantic models initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Pydantic models: {e}")
            raise
    
    def is_initialized(self) -> bool:
        """Check if the PydanticManager is properly initialized"""
        return self._models_initialized
    
    # ============================================================================
    # CORE ANALYSIS MODELS
    # ============================================================================
    
    class MessageRequest(BaseModel):
        """Request model for message analysis"""
        message: str
        user_id: Optional[str] = "unknown"
        channel_id: Optional[str] = "unknown"

    class CrisisResponse(BaseModel):
        """Response model for crisis analysis results"""
        model_config = ConfigDict(protected_namespaces=())
        
        needs_response: bool
        crisis_level: str  # 'none', 'low', 'medium', 'high'
        confidence_score: float
        detected_categories: list
        method: str
        processing_time_ms: float
        model_info: str
        reasoning: Optional[str] = None
        analysis: Optional[Dict[str, Any]] = None

    class HealthResponse(BaseModel):
        """Response model for health check endpoint"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        uptime: float
        model_loaded: bool
        components_available: dict
        configuration_status: dict
        manager_status: dict
        secrets_status: dict

    # ============================================================================
    # LEARNING SYSTEM REQUEST MODELS
    # ============================================================================
    
    class FalsePositiveAnalysisRequest(BaseModel):
        """Request model for false positive analysis (over-detection)"""
        model_config = ConfigDict(protected_namespaces=())
        
        message: str
        detected_level: str         # The level that was incorrectly detected
        correct_level: str          # The correct level that should have been detected
        context: Optional[Dict[str, Any]] = {}  # CRITICAL: Must be Dict[str, Any], not str
        severity_score: Optional[Union[int, float]] = 1

    class FalseNegativeAnalysisRequest(BaseModel):
        """Request model for false negative analysis (under-detection/missed crises)"""
        model_config = ConfigDict(protected_namespaces=())
        
        message: str
        should_detect_level: str    # The crisis level that should have been detected
        actually_detected: str      # What was actually detected (usually 'none' or lower level)
        context: Optional[Dict[str, Any]] = {}  # CRITICAL: Must be Dict[str, Any], not str
        severity_score: Optional[Union[int, float]] = 1

    class LearningUpdateRequest(BaseModel):
        """Request model for learning model updates"""
        model_config = ConfigDict(protected_namespaces=())
        
        learning_record_id: str
        record_type: str  # 'false_positive' or 'false_negative'
        message_data: Dict[str, Any]
        correction_data: Dict[str, Any]
        context_data: Optional[Dict[str, Any]] = {}
        timestamp: str

    # ============================================================================
    # LEARNING SYSTEM RESPONSE MODELS
    # ============================================================================

    class FalsePositiveAnalysisResponse(BaseModel):
        """Response model for false positive analysis"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        patterns_discovered: int
        confidence_adjustments: int
        learning_applied: bool
        sensitivity_reduced: bool
        processing_time_ms: float
        analysis_details: Optional[Dict] = {}

    class FalseNegativeAnalysisResponse(BaseModel):
        """Response model for false negative analysis"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        patterns_discovered: int
        confidence_adjustments: int
        learning_applied: bool
        sensitivity_increased: bool
        processing_time_ms: float
        analysis_details: Optional[Dict] = {}

    class LearningUpdateResponse(BaseModel):
        """Response model for learning model updates"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        model_updated: bool
        adjustments_applied: int
        processing_time_ms: float
        update_details: Optional[Dict] = {}

    class LearningStatisticsResponse(BaseModel):
        """Response model for learning statistics"""
        model_config = ConfigDict(protected_namespaces=())
        
        learning_system_status: str
        total_false_positives_processed: int
        total_false_negatives_processed: int
        total_adjustments_made: int
        false_positives_by_level: Dict[str, int]
        false_negatives_by_level: Dict[str, int]
        last_learning_update: Optional[str] = None
        learning_effectiveness: Optional[Dict] = {}
        model_performance_trends: Optional[Dict] = {}

    # ============================================================================
    # MODEL ACCESS METHODS - Following ModelsManager v3.1 Pattern
    # ============================================================================
    
    def get_core_models(self) -> Dict[str, type]:
        """Get dictionary of core analysis models"""
        return {
            'MessageRequest': self.MessageRequest,
            'CrisisResponse': self.CrisisResponse,
            'HealthResponse': self.HealthResponse
        }
    
    def get_learning_request_models(self) -> Dict[str, type]:
        """Get dictionary of learning system request models"""
        return {
            'FalsePositiveAnalysisRequest': self.FalsePositiveAnalysisRequest,
            'FalseNegativeAnalysisRequest': self.FalseNegativeAnalysisRequest,
            'LearningUpdateRequest': self.LearningUpdateRequest
        }
    
    def get_learning_response_models(self) -> Dict[str, type]:
        """Get dictionary of learning system response models"""
        return {
            'FalsePositiveAnalysisResponse': self.FalsePositiveAnalysisResponse,
            'FalseNegativeAnalysisResponse': self.FalseNegativeAnalysisResponse,
            'LearningUpdateResponse': self.LearningUpdateResponse,
            'LearningStatisticsResponse': self.LearningStatisticsResponse
        }
    
    def get_all_models(self) -> Dict[str, type]:
        """Get dictionary of all available Pydantic models"""
        all_models = {}
        all_models.update(self.get_core_models())
        all_models.update(self.get_learning_request_models())
        all_models.update(self.get_learning_response_models())
        return all_models
    
    # ============================================================================
    # VALIDATION AND UTILITY METHODS
    # ============================================================================
    
    def validate_model_structure(self, model_name: str) -> Dict[str, Any]:
        """
        Validate and return information about a specific model structure
        
        Args:
            model_name: Name of the model to validate
            
        Returns:
            Dictionary with model information and validation status
        """
        all_models = self.get_all_models()
        
        if model_name not in all_models:
            return {
                'valid': False,
                'error': f"Model '{model_name}' not found",
                'available_models': list(all_models.keys())
            }
        
        model_class = all_models[model_name]
        
        try:
            # Get model fields information
            fields_info = {}
            if hasattr(model_class, 'model_fields'):
                for field_name, field_info in model_class.model_fields.items():
                    fields_info[field_name] = {
                        'type': str(field_info.annotation),
                        'required': field_info.is_required(),
                        'default': field_info.default if hasattr(field_info, 'default') else None
                    }
            
            return {
                'valid': True,
                'model_name': model_name,
                'fields': fields_info,
                'field_count': len(fields_info)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f"Failed to validate model '{model_name}': {str(e)}"
            }
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get summary of all available models and their categories"""
        core_models = self.get_core_models()
        learning_request_models = self.get_learning_request_models()
        learning_response_models = self.get_learning_response_models()
        
        return {
            'manager_version': '3.1',
            'architecture': 'clean_manager',
            'total_models': len(core_models) + len(learning_request_models) + len(learning_response_models),
            'categories': {
                'core_analysis': {
                    'count': len(core_models),
                    'models': list(core_models.keys())
                },
                'learning_requests': {
                    'count': len(learning_request_models),
                    'models': list(learning_request_models.keys())
                },
                'learning_responses': {
                    'count': len(learning_response_models),
                    'models': list(learning_response_models.keys())
                }
            },
            'initialization_status': self.is_initialized()
        }
    
# ============================================================================
# FACTORY FUNCTION FOR CLEAN INITIALIZATION
# ============================================================================

def create_pydantic_manager(config_manager=None) -> PydanticManager:
    """
    Factory function to create PydanticManager with clean architecture
    
    Args:
        config_manager: Optional ConfigManager instance
        
    Returns:
        Initialized PydanticManager instance
    """
    logger.info("🏭 Creating PydanticManager v3.1 with clean manager architecture...")
    
    try:
        manager = PydanticManager(config_manager=config_manager)
        
        if not manager.is_initialized():
            raise RuntimeError("PydanticManager failed to initialize properly")
        
        logger.info("✅ PydanticManager v3.1 created successfully")
        return manager
        
    except Exception as e:
        logger.error(f"❌ Failed to create PydanticManager: {e}")
        raise

# ============================================================================
# BACKWARD COMPATIBILITY MODULE-LEVEL EXPORTS
# ============================================================================

# Create a default instance for backward compatibility
_default_manager = None

def _get_default_manager():
    """Get or create the default PydanticManager instance"""
    global _default_manager
    if _default_manager is None:
        _default_manager = create_pydantic_manager()
    return _default_manager

# ============================================================================
# MAIN EXECUTION FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test the PydanticManager
    logging.basicConfig(level=logging.DEBUG)
    
    print("🧪 Testing PydanticManager v3.1...")
    
    # Test manager creation
    manager = create_pydantic_manager()
    
    # Test model summary
    summary = manager.get_model_summary()
    print(f"📊 Model Summary: {summary}")
    
    # Test model access
    core_models = manager.get_core_models()
    print(f"🏗️ Core Models: {list(core_models.keys())}")
    
    # Test model validation
    validation = manager.validate_model_structure('MessageRequest')
    print(f"✅ MessageRequest Validation: {validation}")
    
    print("✅ PydanticManager v3.1 testing complete!")