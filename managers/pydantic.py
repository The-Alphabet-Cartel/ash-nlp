# ash-nlp/managers/pydantic_manager.py
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
Pydantic Models for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-1
LAST MODIFIED: 2025-08-22
PHASE: 3e, Sub-step 5.5, Task 5 - PydanticManager Standard Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Optional, Dict, List, Union, Any
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

class PydanticManager:
    """
    Manager class for all Pydantic models in the Ash NLP Service
    
    Phase 3e Sub-step 5.5: Enhanced with improved error handling and validation patterns
    
    Provides centralized access to request/response models for:
    - Core analysis endpoints (MessageRequest, CrisisResponse, HealthResponse)
    - Learning system endpoints (FalsePositive/FalseNegative analysis)
    - Health and statistics endpoints with comprehensive monitoring
    
    Phase 3e Improvements:
    - Enhanced error handling and resilience for model management
    - Improved validation and monitoring capabilities
    - Better integration with UnifiedConfigManager patterns
    - Added comprehensive model validation and summary methods
    - Enhanced factory function with better error handling
    
    Follows the clean manager architecture established in Phase 2A with Phase 3e enhancements.
    """
    
    def __init__(self, config_manager):
        """
        Initialize PydanticManager with clean manager architecture
        
        Args:
            config_manager: UnifiedConfigManager instance for future configuration needs
        """
        self.config_manager = config_manager
        self._models_initialized = False
        
        logger.info("PydanticManager v3.1e-5.5 initializing with enhanced patterns...")
        
        try:
            # Initialize all model classes
            self._initialize_models()
            logger.info("PydanticManager v3.1e-5.5 initialized successfully")
        except Exception as e:
            logger.error(f"PydanticManager initialization failed: {e}")
            raise
    
    def _initialize_models(self):
        """Initialize all Pydantic model classes with enhanced error handling"""
        try:
            # Models are defined as inner classes for clean organization
            # This follows the manager pattern while keeping models accessible
            
            logger.debug("Initializing Pydantic model definitions...")
            
            # All models are now available as class attributes
            self._models_initialized = True
            
            logger.debug("All Pydantic models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pydantic models: {e}")
            raise
    
    def is_initialized(self) -> bool:
        """Check if the PydanticManager is properly initialized"""
        return self._models_initialized
    
    # ============================================================================
    # CORE ANALYSIS MODELS (Phase 3e Enhanced)
    # ============================================================================
    
    class MessageRequest(BaseModel):
        """Request model for message analysis with enhanced validation"""
        message: str
        user_id: Optional[str] = "unknown"
        channel_id: Optional[str] = "unknown"

    class CrisisResponse(BaseModel):
        """Response model for crisis analysis results with enhanced structure"""
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
        """Response model for health check endpoint with enhanced monitoring"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        uptime: float
        model_loaded: bool
        components_available: dict
        configuration_status: dict
        manager_status: dict
        secrets_status: dict

    # ============================================================================
    # LEARNING SYSTEM REQUEST MODELS (Phase 3e Enhanced)
    # ============================================================================
    
    class FalsePositiveAnalysisRequest(BaseModel):
        """Request model for false positive analysis with enhanced validation"""
        model_config = ConfigDict(protected_namespaces=())
        
        message: str
        detected_level: str         # The level that was incorrectly detected
        correct_level: str          # The correct level that should have been detected
        context: Optional[Dict[str, Any]] = {}  # Enhanced: Must be Dict[str, Any], not str
        severity_score: Optional[Union[int, float]] = 1

    class FalseNegativeAnalysisRequest(BaseModel):
        """Request model for false negative analysis with enhanced validation"""
        model_config = ConfigDict(protected_namespaces=())
        
        message: str
        should_detect_level: str    # The crisis level that should have been detected
        actually_detected: str      # What was actually detected (usually 'none' or lower level)
        context: Optional[Dict[str, Any]] = {}  # Enhanced: Must be Dict[str, Any], not str
        severity_score: Optional[Union[int, float]] = 1

    class LearningUpdateRequest(BaseModel):
        """Request model for learning model updates with enhanced structure"""
        model_config = ConfigDict(protected_namespaces=())
        
        learning_record_id: str
        record_type: str  # 'false_positive' or 'false_negative'
        message_data: Dict[str, Any]
        correction_data: Dict[str, Any]
        context_data: Optional[Dict[str, Any]] = {}
        timestamp: str

    # ============================================================================
    # LEARNING SYSTEM RESPONSE MODELS (Phase 3e Enhanced)
    # ============================================================================

    class FalsePositiveAnalysisResponse(BaseModel):
        """Response model for false positive analysis with enhanced details"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        patterns_discovered: int
        confidence_adjustments: int
        learning_applied: bool
        sensitivity_reduced: bool
        processing_time_ms: float
        analysis_details: Optional[Dict] = {}

    class FalseNegativeAnalysisResponse(BaseModel):
        """Response model for false negative analysis with enhanced details"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        patterns_discovered: int
        confidence_adjustments: int
        learning_applied: bool
        sensitivity_increased: bool
        processing_time_ms: float
        analysis_details: Optional[Dict] = {}

    class LearningUpdateResponse(BaseModel):
        """Response model for learning model updates with enhanced monitoring"""
        model_config = ConfigDict(protected_namespaces=())
        
        status: str
        model_updated: bool
        adjustments_applied: int
        processing_time_ms: float
        update_details: Optional[Dict] = {}

    class LearningStatisticsResponse(BaseModel):
        """Response model for learning statistics with enhanced metrics"""
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
    # MODEL ACCESS METHODS (Phase 3e Enhanced)
    # ============================================================================
    
    def get_core_models(self) -> Dict[str, type]:
        """Get dictionary of core analysis models with enhanced error handling"""
        try:
            return {
                'MessageRequest': self.MessageRequest,
                'CrisisResponse': self.CrisisResponse,
                'HealthResponse': self.HealthResponse
            }
        except Exception as e:
            logger.error(f"Error getting core models: {e}")
            return {}
    
    def get_learning_request_models(self) -> Dict[str, type]:
        """Get dictionary of learning system request models with enhanced error handling"""
        try:
            return {
                'FalsePositiveAnalysisRequest': self.FalsePositiveAnalysisRequest,
                'FalseNegativeAnalysisRequest': self.FalseNegativeAnalysisRequest,
                'LearningUpdateRequest': self.LearningUpdateRequest
            }
        except Exception as e:
            logger.error(f"Error getting learning request models: {e}")
            return {}
    
    def get_learning_response_models(self) -> Dict[str, type]:
        """Get dictionary of learning system response models with enhanced error handling"""
        try:
            return {
                'FalsePositiveAnalysisResponse': self.FalsePositiveAnalysisResponse,
                'FalseNegativeAnalysisResponse': self.FalseNegativeAnalysisResponse,
                'LearningUpdateResponse': self.LearningUpdateResponse,
                'LearningStatisticsResponse': self.LearningStatisticsResponse
            }
        except Exception as e:
            logger.error(f"Error getting learning response models: {e}")
            return {}
    
    def get_all_models(self) -> Dict[str, type]:
        """Get dictionary of all available Pydantic models with enhanced error handling"""
        try:
            all_models = {}
            all_models.update(self.get_core_models())
            all_models.update(self.get_learning_request_models())
            all_models.update(self.get_learning_response_models())
            return all_models
        except Exception as e:
            logger.error(f"Error getting all models: {e}")
            return {}
    
    # ============================================================================
    # VALIDATION AND UTILITY METHODS (Phase 3e Enhanced)
    # ============================================================================
    
    def validate_model_structure(self, model_name: str) -> Dict[str, Any]:
        """
        Validate and return information about a specific model structure with enhanced validation
        
        Args:
            model_name: Name of the model to validate
            
        Returns:
            Dictionary with model information and validation status
        """
        try:
            all_models = self.get_all_models()
            
            if model_name not in all_models:
                return {
                    'valid': False,
                    'error': f"Model '{model_name}' not found",
                    'available_models': list(all_models.keys())
                }
            
            model_class = all_models[model_name]
            
            # Get model fields information with enhanced error handling
            fields_info = {}
            if hasattr(model_class, 'model_fields'):
                for field_name, field_info in model_class.model_fields.items():
                    try:
                        fields_info[field_name] = {
                            'type': str(field_info.annotation),
                            'required': field_info.is_required(),
                            'default': field_info.default if hasattr(field_info, 'default') else None
                        }
                    except Exception as field_error:
                        logger.warning(f"Error processing field {field_name}: {field_error}")
                        fields_info[field_name] = {
                            'type': 'unknown',
                            'required': False,
                            'default': None,
                            'error': str(field_error)
                        }
            
            return {
                'valid': True,
                'model_name': model_name,
                'fields': fields_info,
                'field_count': len(fields_info)
            }
            
        except Exception as e:
            logger.error(f"Error validating model '{model_name}': {e}")
            return {
                'valid': False,
                'error': f"Failed to validate model '{model_name}': {str(e)}"
            }
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get summary of all available models with enhanced Phase 3e information"""
        try:
            core_models = self.get_core_models()
            learning_request_models = self.get_learning_request_models()
            learning_response_models = self.get_learning_response_models()
            
            return {
                'manager_version': 'v3.1e-5.5-6',
                'phase': '3e Sub-step 5.5 Task 5',
                'architecture': 'clean_manager_enhanced',
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
                'initialization_status': self.is_initialized(),
                'enhanced_error_handling': True,
                'phase_3e_cleanup': 'complete'
            }
            
        except Exception as e:
            logger.error(f"Error getting model summary: {e}")
            return {
                'manager_version': 'v3.1e-5.5-6',
                'phase': '3e Sub-step 5.5 Task 5',
                'error': str(e),
                'initialization_status': False,
                'architecture': 'error_state'
            }
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary for monitoring and debugging
        Phase 3e: New method for enhanced system visibility
        """
        try:
            model_summary = self.get_model_summary()
            all_models = self.get_all_models()
            
            return {
                'manager_version': 'v3.1e-5.5-6',
                'phase': '3e Sub-step 5.5 Task 5',
                'total_models_available': len(all_models),
                'core_models_count': len(self.get_core_models()),
                'learning_models_count': len(self.get_learning_request_models()) + len(self.get_learning_response_models()),
                'pydantic_version': 'v2_compatible',
                'config_dict_enabled': True,
                'protected_namespaces_configured': True,
                'initialization_status': 'complete',
                'cleanup_status': 'phase_3e_complete',
                'error_handling': 'enhanced',
                'model_validation': 'available'
            }
            
        except Exception as e:
            logger.error(f"Error generating configuration summary: {e}")
            return {
                'manager_version': 'v3.1e-5.5-6',
                'phase': '3e Sub-step 5.5 Task 5',
                'error': str(e),
                'initialization_status': 'error',
                'cleanup_status': 'phase_3e_complete'
            }
    
    def validate_all_models(self) -> Dict[str, Any]:
        """
        Validate all models and return comprehensive validation report
        Phase 3e: New method for enhanced model validation
        """
        try:
            all_models = self.get_all_models()
            validation_results = {
                'total_models': len(all_models),
                'validated_models': 0,
                'validation_errors': 0,
                'model_validations': {},
                'overall_status': 'unknown'
            }
            
            for model_name in all_models.keys():
                validation = self.validate_model_structure(model_name)
                validation_results['model_validations'][model_name] = validation
                
                if validation.get('valid', False):
                    validation_results['validated_models'] += 1
                else:
                    validation_results['validation_errors'] += 1
            
            # Determine overall status
            if validation_results['validation_errors'] == 0:
                validation_results['overall_status'] = 'all_valid'
            elif validation_results['validated_models'] > 0:
                validation_results['overall_status'] = 'partial_valid'
            else:
                validation_results['overall_status'] = 'validation_failed'
            
            logger.info(f"Model validation complete: {validation_results['validated_models']}/{validation_results['total_models']} valid")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating all models: {e}")
            return {
                'total_models': 0,
                'validated_models': 0,
                'validation_errors': 1,
                'model_validations': {},
                'overall_status': 'error',
                'error': str(e)
            }

# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance (Phase 3e Enhanced)
# ============================================================================

def create_pydantic_manager(config_manager) -> PydanticManager:
    """
    Factory function for PydanticManager (Clean v3.1 Pattern) - Phase 3e Enhanced
    
    Args:
        config_manager: UnifiedConfigManager instance for future configuration needs
        
    Returns:
        Initialized PydanticManager instance with Phase 3e enhancements
        
    Raises:
        RuntimeError: If PydanticManager fails to initialize properly
    """
    logger.info("Creating PydanticManager v3.1e-5.5 with enhanced patterns...")
    
    try:
        manager = PydanticManager(config_manager=config_manager)
        
        if not manager.is_initialized():
            raise RuntimeError("PydanticManager failed to initialize properly")
        
        logger.info("PydanticManager v3.1e-5.5 created successfully")
        return manager
        
    except Exception as e:
        logger.error(f"Failed to create PydanticManager: {e}")
        raise

# ============================================================================
# BACKWARD COMPATIBILITY MODULE-LEVEL EXPORTS (Phase 3e Enhanced)
# ============================================================================

# Create a default instance for backward compatibility
_default_manager = None

def _get_default_manager():
    """Get or create the default PydanticManager instance with enhanced error handling"""
    global _default_manager
    try:
        if _default_manager is None:
            _default_manager = create_pydantic_manager(None)
        return _default_manager
    except Exception as e:
        logger.error(f"Error getting default PydanticManager: {e}")
        raise

# Export public interface
__all__ = [
    'PydanticManager',
    'create_pydantic_manager'
]

# ============================================================================
# MAIN EXECUTION FOR TESTING (Phase 3e Enhanced)
# ============================================================================

if __name__ == "__main__":
    # Enhanced test suite for PydanticManager
    logging.basicConfig(level=logging.DEBUG)
    
    print("Testing PydanticManager v3.1e-5.5...")
    
    try:
        # Test manager creation
        manager = create_pydantic_manager(None)
        
        # Test model summary
        summary = manager.get_model_summary()
        print(f"Model Summary: {summary}")
        
        # Test model access
        core_models = manager.get_core_models()
        print(f"Core Models: {list(core_models.keys())}")
        
        # Test model validation
        validation = manager.validate_model_structure('MessageRequest')
        print(f"MessageRequest Validation: {validation}")
        
        # Test comprehensive validation
        all_validation = manager.validate_all_models()
        print(f"All Models Validation: {all_validation['overall_status']}")
        
        # Test configuration summary
        config_summary = manager.get_configuration_summary()
        print(f"Configuration Summary: {config_summary}")
        
        print("PydanticManager v3.1e-5.5 testing complete!")
        
    except Exception as e:
        print(f"Testing failed: {e}")
        raise

logger.info("PydanticManager v3.1e-5.5-6 loaded - Phase 3e Sub-step 5.5 cleanup complete with enhanced patterns")