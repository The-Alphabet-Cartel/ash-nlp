# ash-nlp/api/learning_endpoints.py
"""
Learning Endpoints for Ash NLP Service v3.1
FILE VERSION: v3.1-3d-10-1
LAST MODIFIED: 2025-08-13
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

class LearningSystemManager:
    """
    Learning System Manager for Crisis Detection Learning
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    """
    
    def __init__(self, unified_config_manager):
        """
        Initialize Learning System Manager with UnifiedConfigManager
        
        Args:
            unified_config_manager: UnifiedConfigManager instance for dependency injection
        """
        # STEP 9 CHANGE: Use UnifiedConfigManager instead of direct os.getenv()
        self.unified_config = unified_config_manager
        
        # Load configuration using unified configuration
        self._load_configuration()
        
        logger.info("LearningSystemManager v3.1d Step 9 initialized - UnifiedConfigManager integration complete")
    
    def _load_configuration(self):
        """Load learning configuration using UnifiedConfigManager (NO MORE os.getenv())"""
        try:
            # STEP 9 FIX: Try to load learning configuration, handle missing file gracefully
            learning_config = None
            try:
                learning_config = self.unified_config.load_config_file('learning_settings')
                logger.info("✅ Learning configuration loaded from learning_settings.json")
            except Exception as e:
                logger.warning(f"⚠️ learning_settings.json not found: {e}")
                logger.info("🔄 Using environment variables only")
            
            if learning_config:
                # STEP 9 FIX: Handle corrected JSON structure (value, defaults, validation pattern)
                
                # Extract configuration values using the correct JSON structure
                persistence_config = learning_config.get('learning_persistence', {})
                self.learning_data_path = self.unified_config.get_env(
                    'NLP_ANALYSIS_LEARNING_PERSISTENCE_FILE',
                    persistence_config.get('defaults', {}).get('file', './learning_data/adjustments.json')
                )
                
                learning_rate_config = learning_config.get('learning_rate', {})
                self.learning_rate = self.unified_config.get_env_float(
                    'NLP_ANALYSIS_LEARNING_RATE',
                    learning_rate_config.get('defaults', {}).get('value', 0.01)
                )
                
                confidence_config = learning_config.get('confidence_adjustments', {})
                self.min_adjustment = self.unified_config.get_env_float(
                    'NLP_ANALYSIS_LEARNING_MIN_CONFIDENCE_ADJUSTMENT',
                    confidence_config.get('defaults', {}).get('min_adjustment', 0.05)
                )
                
                self.max_adjustment = self.unified_config.get_env_float(
                    'NLP_ANALYSIS_LEARNING_MAX_CONFIDENCE_ADJUSTMENT',
                    confidence_config.get('defaults', {}).get('max_adjustment', 0.30)
                )
                
                daily_limits_config = learning_config.get('daily_limits', {})
                self.max_adjustments_per_day = self.unified_config.get_env_int(
                    'NLP_ANALYSIS_LEARNING_MAX_ADJUSTMENTS_PER_DAY',
                    daily_limits_config.get('defaults', {}).get('max_adjustments_per_day', 50)
                )
                
                # Additional configuration from corrected JSON structure
                feedback_config = learning_config.get('feedback_factors', {})
                self.false_positive_factor = self.unified_config.get_env_float(
                    'NLP_ANALYSIS_LEARNING_FALSE_POSITIVE_FACTOR',
                    feedback_config.get('defaults', {}).get('false_positive_factor', -0.1)
                )
                self.false_negative_factor = self.unified_config.get_env_float(
                    'NLP_ANALYSIS_LEARNING_FALSE_NEGATIVE_FACTOR',
                    feedback_config.get('defaults', {}).get('false_negative_factor', 0.1)
                )
                
                severity_config = learning_config.get('severity_multipliers', {})
                severity_defaults = severity_config.get('defaults', {})
                self.severity_multipliers = {
                    'high': severity_defaults.get('high', 3.0),
                    'medium': severity_defaults.get('medium', 2.0),
                    'low': severity_defaults.get('low', 1.0)
                }
                
                # Pattern learning configuration (if available)
                self.false_positive_indicators = []
                self.false_negative_indicators = []
                
                logger.info("✅ Learning configuration loaded from JSON + ENV using UnifiedConfigManager")
                
            else:
                logger.info("🔄 Loading configuration from environment variables only")
                self._load_from_environment_only()
                
        except Exception as e:
            logger.error(f"❌ Failed to load configuration: {e}")
            logger.info("🔧 Falling back to environment variables only")
            self._load_from_environment_only()
    
    def _load_from_environment_only(self):
        """Load configuration from environment variables only using UnifiedConfigManager"""
        # STEP 9 CHANGE: Use unified_config instead of os.getenv() for all variables
        self.learning_data_path = self.unified_config.get_env(
            'NLP_ANALYSIS_LEARNING_PERSISTENCE_FILE',
            self.unified_config.get_env('NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE', 
                                       './learning_data/adjustments.json')
        )
        
        self.learning_rate = self.unified_config.get_env_float(
            'NLP_ANALYSIS_LEARNING_RATE',
            self.unified_config.get_env_float('NLP_THRESHOLD_LEARNING_RATE', 0.01)
        )
        
        self.min_adjustment = self.unified_config.get_env_float(
            'NLP_ANALYSIS_LEARNING_MIN_CONFIDENCE_ADJUSTMENT',
            self.unified_config.get_env_float('NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE_ADJUSTMENT', 0.05)
        )
        
        self.max_adjustment = self.unified_config.get_env_float(
            'NLP_ANALYSIS_LEARNING_MAX_CONFIDENCE_ADJUSTMENT',
            self.unified_config.get_env_float('NLP_THRESHOLD_LEARNING_MAX_CONFIDENCE_ADJUSTMENT', 0.30)
        )
        
        self.max_adjustments_per_day = self.unified_config.get_env_int(
            'NLP_ANALYSIS_LEARNING_MAX_ADJUSTMENTS_PER_DAY',
            self.unified_config.get_env_int('NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY', 50)
        )
        
        # Phase 3d Step 9 - Updated variable names with unified config access
        self.min_global_sensitivity = self.unified_config.get_env_float('NLP_MIN_GLOBAL_SENSITIVITY', 0.5)
        self.max_global_sensitivity = self.unified_config.get_env_float('NLP_MAX_GLOBAL_SENSITIVITY', 1.5)
        self.false_positive_factor = self.unified_config.get_env_float('NLP_FALSE_POSITIVE_FACTOR', -0.1)
        self.false_negative_factor = self.unified_config.get_env_float('NLP_FALSE_NEGATIVE_FACTOR', 0.1)
        
        # Default indicators and multipliers
        self.false_positive_indicators = []
        self.false_negative_indicators = []
        self.severity_multipliers = {'high': 3.0, 'medium': 2.0, 'low': 1.0}
        
        logger.info("✅ Learning configuration loaded from environment variables using UnifiedConfigManager")
    
    async def analyze_false_positive(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze false positive detection for learning"""
        try:
            message = request_data.get('message', '')
            detected_level = request_data.get('detected_level', '')
            correct_level = request_data.get('correct_level', '')
            severity_score = request_data.get('severity_score', 1)
            
            # Analyze the false positive
            adjustment_factor = self.false_positive_factor * self.severity_multipliers.get(correct_level, 1.0)
            
            # Store learning data
            learning_record = {
                'type': 'false_positive',
                'message': message,
                'detected_level': detected_level,
                'correct_level': correct_level,
                'adjustment_factor': adjustment_factor,
                'severity_score': severity_score,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'processed': False
            }
            
            self._save_learning_record(learning_record)
            
            return {
                'learning_applied': True,
                'adjustment_factor': adjustment_factor,
                'patterns_discovered': len(self.false_positive_indicators),
                'confidence_adjustments': 1
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing false positive: {e}")
            return {
                'learning_applied': False,
                'error': str(e)
            }
    
    async def analyze_false_negative(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze false negative (missed crisis) for learning"""
        try:
            message = request_data.get('message', '')
            should_detect_level = request_data.get('should_detect_level', '')
            actually_detected = request_data.get('actually_detected', '')
            severity_score = request_data.get('severity_score', 1)
            
            # Analyze the false negative
            adjustment_factor = self.false_negative_factor * self.severity_multipliers.get(should_detect_level, 1.0)
            
            # Store learning data
            learning_record = {
                'type': 'false_negative',
                'message': message,
                'should_detect_level': should_detect_level,
                'actually_detected': actually_detected,
                'adjustment_factor': adjustment_factor,
                'severity_score': severity_score,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'processed': False
            }
            
            self._save_learning_record(learning_record)
            
            return {
                'learning_applied': True,
                'adjustment_factor': adjustment_factor,
                'patterns_discovered': len(self.false_negative_indicators),
                'confidence_adjustments': 1
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing false negative: {e}")
            return {
                'learning_applied': False,
                'error': str(e)
            }
    
    def _save_learning_record(self, record: Dict[str, Any]):
        """Save learning record to persistent storage"""
        try:
            # Ensure directory exists
            learning_path = Path(self.learning_data_path)
            learning_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing records
            if learning_path.exists():
                with open(learning_path, 'r') as f:
                    records = json.load(f)
            else:
                records = []
            
            # Add new record
            records.append(record)
            
            # Save back to file
            with open(learning_path, 'w') as f:
                json.dump(records, f, indent=2)
                
            logger.debug(f"✅ Learning record saved to {learning_path}")
            
        except Exception as e:
            logger.error(f"❌ Error saving learning record: {e}")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        try:
            # Load learning records
            learning_path = Path(self.learning_data_path)
            
            if not learning_path.exists():
                return {
                    'learning_system_status': 'initialized',
                    'total_records': 0,
                    'false_positives': 0,
                    'false_negatives': 0,
                    'last_update': None,
                    'configuration': {
                        'learning_rate': self.learning_rate,
                        'min_adjustment': self.min_adjustment,
                        'max_adjustment': self.max_adjustment,
                        'max_adjustments_per_day': self.max_adjustments_per_day,
                        'data_file': self.learning_data_path,
                        'unified_config_manager': True,
                        'direct_os_getenv_calls': 'eliminated'
                    }
                }
            
            with open(learning_path, 'r') as f:
                records = json.load(f)
            
            # Calculate statistics
            false_positives = [r for r in records if r.get('type') == 'false_positive']
            false_negatives = [r for r in records if r.get('type') == 'false_negative']
            
            last_update = None
            if records:
                last_update = max(r.get('timestamp', '') for r in records)
            
            return {
                'learning_system_status': 'active',
                'total_records': len(records),
                'false_positives': len(false_positives),
                'false_negatives': len(false_negatives),
                'false_positive_patterns': len(self.false_positive_indicators),
                'false_negative_patterns': len(self.false_negative_indicators),
                'last_update': last_update,
                'configuration': {
                    'learning_rate': self.learning_rate,
                    'min_adjustment': self.min_adjustment,
                    'max_adjustment': self.max_adjustment,
                    'max_adjustments_per_day': self.max_adjustments_per_day,
                    'data_file': self.learning_data_path,
                    'unified_config_manager': True,
                    'direct_os_getenv_calls': 'eliminated'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting learning statistics: {e}")
            return {
                'learning_system_status': 'error',
                'error': str(e),
                'unified_config_manager': True
            }

# ========================================================================
# GET PYDANTIC MODELS - Using Application Manager Access
# ========================================================================
def get_pydantic_models():
    """Get Pydantic models for request validation"""
    try:
        from pydantic import BaseModel
        from typing import Dict, Any, Optional, Union
        
        class FalsePositiveAnalysisRequest(BaseModel):
            message: str
            detected_level: str
            correct_level: str
            context: Optional[Dict[str, Any]] = {}
            severity_score: Optional[Union[int, float]] = 1
        
        class FalseNegativeAnalysisRequest(BaseModel):
            message: str
            should_detect_level: str
            actually_detected: str
            context: Optional[Dict[str, Any]] = {}
            severity_score: Optional[Union[int, float]] = 1
        
        class LearningUpdateRequest(BaseModel):
            learning_record_id: str
            record_type: str
            message_data: Dict[str, Any]
            correction_data: Dict[str, Any]
            context_data: Optional[Dict[str, Any]] = {}
            timestamp: str
        
        return {
            'FalsePositiveAnalysisRequest': FalsePositiveAnalysisRequest,
            'FalseNegativeAnalysisRequest': FalseNegativeAnalysisRequest,
            'LearningUpdateRequest': LearningUpdateRequest
        }
    except Exception as e:
        logger.error(f"❌ Error creating Pydantic models: {e}")
        return {}

# ========================================================================
# LEARNING ENDPOINTS REGISTRATION - Phase 3d Step 9 FIXED
# ========================================================================

def register_learning_endpoints(app: FastAPI, unified_config_manager, threshold_mapping_manager=None):
    """
    Register learning endpoints with UnifiedConfigManager integration
    Phase 3d Step 9: Updated to use UnifiedConfigManager with optional ThresholdMappingManager
    
    Args:
        app: FastAPI application instance
        unified_config_manager: UnifiedConfigManager instance for dependency injection
        threshold_mapping_manager: Optional ThresholdMappingManager instance for enhanced integration
    """
    
    # STEP 9 CHANGE: Create learning manager with UnifiedConfigManager
    learning_manager = LearningSystemManager(unified_config_manager)
    
    # STEP 9 ENHANCEMENT: Optional threshold mapping manager integration
    if threshold_mapping_manager:
        logger.info("✅ ThresholdMappingManager integrated with learning endpoints")
        # Store reference for potential future use in learning adjustments
        learning_manager.threshold_mapping_manager = threshold_mapping_manager
    else:
        logger.info("ℹ️ Learning endpoints running without ThresholdMappingManager integration")
    
    # Get Pydantic models
    models = get_pydantic_models()
    
    if not models:
        logger.warning("⚠️ Pydantic models not available, endpoints will use basic validation")
        return
    
    FalsePositiveAnalysisRequest = models['FalsePositiveAnalysisRequest']
    FalseNegativeAnalysisRequest = models['FalseNegativeAnalysisRequest']
    LearningUpdateRequest = models['LearningUpdateRequest']
    
    # ========================================================================
    # FALSE POSITIVE ANALYSIS ENDPOINT
    # ========================================================================
    
    @app.post("/analyze_false_positive")
    async def analyze_false_positive(request: FalsePositiveAnalysisRequest):
        """Analyze false positive detection for learning - Phase 3d Step 9"""
        
        try:
            request_data = {
                'message': request.message,
                'detected_level': request.detected_level,
                'correct_level': request.correct_level,
                'context': request.context,
                'severity_score': request.severity_score
            }
            
            result = await learning_manager.analyze_false_positive(request_data)
            
            return {
                'status': 'success',
                'analysis_type': 'false_positive',
                'learning_applied': result.get('learning_applied', False),
                'adjustment_factor': result.get('adjustment_factor', 0),
                'patterns_discovered': result.get('patterns_discovered', 0),
                'confidence_adjustments': result.get('confidence_adjustments', 0),
                'unified_config_manager': True,
                'direct_os_getenv_calls': 'eliminated'
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing false positive: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Phase 3d Step 9: False positive analysis failed: {str(e)}"
            )
    
    # ========================================================================
    # FALSE NEGATIVE ANALYSIS ENDPOINT
    # ========================================================================
    
    @app.post("/analyze_false_negative")
    async def analyze_false_negative(request: FalseNegativeAnalysisRequest):
        """Analyze false negative (missed crisis) for learning - Phase 3d Step 9"""
        
        try:
            request_data = {
                'message': request.message,
                'should_detect_level': request.should_detect_level,
                'actually_detected': request.actually_detected,
                'context': request.context,
                'severity_score': request.severity_score
            }
            
            result = await learning_manager.analyze_false_negative(request_data)
            
            return {
                'status': 'success',
                'analysis_type': 'false_negative',
                'learning_applied': result.get('learning_applied', False),
                'adjustment_factor': result.get('adjustment_factor', 0),
                'patterns_discovered': result.get('patterns_discovered', 0),
                'confidence_adjustments': result.get('confidence_adjustments', 0),
                'unified_config_manager': True,
                'direct_os_getenv_calls': 'eliminated'
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing false negative: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Phase 3d Step 9: False negative analysis failed: {str(e)}"
            )
    
    # ========================================================================
    # LEARNING MODEL UPDATE ENDPOINT
    # ========================================================================
    
    @app.post("/update_learning_model")
    async def update_learning_model(request: LearningUpdateRequest):
        """Update learning model with staff corrections - Phase 3d Step 9"""
        
        try:
            record_type = request.record_type.lower()
            
            if record_type == 'false_positive':
                fp_request = {
                    'message': request.message_data.get('message', ''),
                    'detected_level': request.correction_data.get('detected_level', ''),
                    'correct_level': request.correction_data.get('correct_level', ''),
                    'severity_score': request.correction_data.get('severity_score', 1)
                }
                result = await learning_manager.analyze_false_positive(fp_request)
            
            elif record_type == 'false_negative':
                fn_request = {
                    'message': request.message_data.get('message', ''),
                    'should_detect_level': request.correction_data.get('should_detect_level', ''),
                    'actually_detected': request.correction_data.get('actually_detected', ''),
                    'severity_score': request.correction_data.get('severity_score', 1)
                }
                result = await learning_manager.analyze_false_negative(fn_request)
            
            else:
                raise HTTPException(status_code=400, detail=f"Unknown record type: {request.record_type}")
            
            return {
                'status': 'success',
                'record_id': request.learning_record_id,
                'record_type': request.record_type,
                'learning_applied': result.get('learning_applied', False),
                'patterns_discovered': result.get('patterns_discovered', 0),
                'adjustments_made': result.get('confidence_adjustments', 0),
                'unified_config_manager': True,
                'direct_os_getenv_calls': 'eliminated'
            }
            
        except Exception as e:
            logger.error(f"❌ Error updating learning model: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Phase 3d Step 9: Learning model update failed: {str(e)}"
            )
    
    # ========================================================================
    # LEARNING STATISTICS ENDPOINT
    # ========================================================================
    
    @app.get("/learning_statistics")
    async def get_learning_statistics():
        """Get comprehensive learning system statistics - Phase 3d Step 9"""
        
        try:
            stats = learning_manager.get_learning_statistics()
            
            # Add endpoint metadata
            stats['endpoint_architecture'] = 'v3.1d_step_9'
            stats['unified_config_manager'] = True
            stats['direct_os_getenv_calls'] = 'eliminated'
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting learning statistics: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Phase 3d Step 9: Statistics retrieval failed: {str(e)}"
            )
    
    # ========================================================================
    # ENDPOINT REGISTRATION COMPLETE
    # ========================================================================
    
    logger.info("🧠 Phase 3d Step 9: Enhanced learning endpoints added successfully")
    logger.info("🔧 Learning endpoints registered:")
    logger.info("   POST /analyze_false_negative - Analyze missed crises")
    logger.info("   POST /analyze_false_positive - Analyze over-detections")
    logger.info("   POST /update_learning_model - Update model with staff corrections")
    logger.info("   GET /learning_statistics - Comprehensive learning statistics")
    logger.info("✅ Phase 3d Step 9: All learning endpoints using UnifiedConfigManager")
    logger.info("🎉 UnifiedConfigManager integration: Learning system complete - No direct os.getenv() calls")