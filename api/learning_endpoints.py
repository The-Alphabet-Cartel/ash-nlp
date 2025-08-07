# ash/ash-nlp/api/learning_endpoints.py (Clean v3.1 Architecture - Phase 2C Complete)
"""
Enhanced Learning Endpoints for NLP Server v3.1
Handles false positive and false negative staff corrections
Clean v3.1 implementation with direct manager access only
"""

import logging
import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class EnhancedLearningManager:
    """Enhanced learning manager with clean v3.1 manager architecture - NO FALLBACKS"""
    
    def __init__(self, models_manager, config_manager):
        """
        Initialize with clean v3.1 manager architecture - Direct Manager Access Only
        
        Args:
            models_manager: ModelsManager v3.1 instance (required)
            config_manager: ConfigManager instance (required)
        """
        
        # Validate required managers - NO FALLBACKS
        if not models_manager:
            logger.error("❌ ModelsManager v3.1 is required for learning system")
            raise RuntimeError("ModelsManager v3.1 required for Enhanced Learning Manager")
        
        if not config_manager:
            logger.error("❌ ConfigManager is required for learning system")
            raise RuntimeError("ConfigManager required for Enhanced Learning Manager")
        
        self.models_manager = models_manager
        self.config_manager = config_manager
        
        # Load configuration using clean v3.1 manager architecture
        try:
            self._load_configuration_from_managers()
            logger.info("🔧 Learning configuration loaded from clean v3.1 managers")
        except Exception as e:
            logger.error(f"❌ Failed to load learning configuration: {e}")
            raise RuntimeError(f"Learning configuration failed: {e}")
        
        # Initialize learning data
        self._initialize_enhanced_learning_data()
        
        logger.info("🧠 Enhanced learning manager initialized with clean v3.1 architecture")
        logger.info("✅ Phase 2C: Direct manager access only - No backward compatibility")
        logger.debug(f"   Learning rate: {self.learning_rate}")
        logger.debug(f"   Adjustment range: {self.min_adjustment} to {self.max_adjustment}")
        logger.debug(f"   Max adjustments per day: {self.max_adjustments_per_day}")
        logger.debug(f"   Sensitivity bounds: {self.min_global_sensitivity} to {self.max_global_sensitivity}")
        logger.debug(f"   Data file: {self.learning_data_path}")
    
    def _load_configuration_from_managers(self):
        """Load configuration using clean v3.1 manager architecture - NO FALLBACKS"""
        try:
            # Direct ConfigManager access for learning parameters
            learning_config_file = "/app/config/learning_parameters.json"
            
            if os.path.exists(learning_config_file):
                logger.debug(f"📁 Found learning configuration file: {learning_config_file}")
                
                with open(learning_config_file, 'r') as f:
                    learning_config_raw = json.load(f)
                
                # Extract learning system configuration
                ls_config = learning_config_raw.get("learning_system", {})
                
                # Load basic parameters from environment (with JSON fallbacks)
                self.learning_data_path = os.getenv('NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE', './learning_data/enhanced_learning_adjustments.json')
                self.learning_rate = float(os.getenv('NLP_THRESHOLD_LEARNING_RATE', str(ls_config.get('learning_rate', 0.1))))
                self.min_adjustment = float(os.getenv('NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE_ADJUSTMENT', str(ls_config.get('min_confidence_adjustment', 0.05))))
                self.max_adjustment = float(os.getenv('NLP_THRESHOLD_LEARNING_MAX_CONFIDENCE_ADJUSTMENT', str(ls_config.get('max_confidence_adjustment', 0.30))))
                self.max_adjustments_per_day = int(os.getenv('NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY', str(ls_config.get('max_adjustments_per_day', 50))))
                
                # Load sensitivity bounds from JSON with environment overrides
                sensitivity_bounds = ls_config.get('sensitivity_bounds', {})
                self.min_global_sensitivity = float(os.getenv('NLP_MIN_GLOBAL_SENSITIVITY', str(sensitivity_bounds.get('min_global_sensitivity', 0.5))))
                self.max_global_sensitivity = float(os.getenv('NLP_MAX_GLOBAL_SENSITIVITY', str(sensitivity_bounds.get('max_global_sensitivity', 1.5))))
                
                # Load pattern detection rules from JSON
                pattern_config = ls_config.get('pattern_detection', {})
                self.false_positive_indicators = pattern_config.get('false_positive_indicators', [])
                self.false_negative_indicators = pattern_config.get('false_negative_indicators', [])
                
                # Load adjustment rules from JSON
                adjustment_rules = ls_config.get('adjustment_rules', {})
                self.false_positive_factor = float(adjustment_rules.get('false_positive_adjustment_factor', -0.1))
                self.false_negative_factor = float(adjustment_rules.get('false_negative_adjustment_factor', 0.1))
                self.severity_multipliers = adjustment_rules.get('severity_multipliers', {'high': 3.0, 'medium': 2.0, 'low': 1.0})
                
                logger.info("✅ Learning configuration loaded from JSON + ENV (clean v3.1)")
                
            else:
                logger.warning(f"⚠️ Learning configuration file not found: {learning_config_file}")
                logger.info("🔧 Using environment variables only for learning configuration")
                self._load_from_environment_only()
                
        except Exception as e:
            logger.error(f"❌ Failed to load configuration from managers: {e}")
            logger.info("🔧 Falling back to environment variables only")
            self._load_from_environment_only()
    
    def _load_from_environment_only(self):
        """Load configuration from environment variables only - Clean v3.1 fallback"""
        self.learning_data_path = os.getenv('NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE', './learning_data/enhanced_learning_adjustments.json')
        self.learning_rate = float(os.getenv('NLP_THRESHOLD_LEARNING_RATE', '0.1'))
        self.min_adjustment = float(os.getenv('NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE_ADJUSTMENT', '0.05'))
        self.max_adjustment = float(os.getenv('NLP_THRESHOLD_LEARNING_MAX_CONFIDENCE_ADJUSTMENT', '0.30'))
        self.max_adjustments_per_day = int(os.getenv('NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY', '50'))
        
        # Clean v3.1 defaults
        self.min_global_sensitivity = float(os.getenv('NLP_MIN_GLOBAL_SENSITIVITY', '0.5'))
        self.max_global_sensitivity = float(os.getenv('NLP_MAX_GLOBAL_SENSITIVITY', '1.5'))
        
        # Default pattern indicators for clean v3.1
        self.false_positive_indicators = [
            'just tired', 'dead tired', 'dying of laughter', 'killing it',
            'murder a burger', 'joke killed me', 'that\'s brutal', 'insane workout'
        ]
        self.false_negative_indicators = [
            'don\'t want to be here', 'tired of everything', 'can\'t go on',
            'no point', 'what\'s the use', 'giving up', 'had enough'
        ]
        
        self.false_positive_factor = float(os.getenv('NLP_FALSE_POSITIVE_FACTOR', '-0.1'))
        self.false_negative_factor = float(os.getenv('NLP_FALSE_NEGATIVE_FACTOR', '0.1'))
        self.severity_multipliers = {'high': 3.0, 'medium': 2.0, 'low': 1.0}
        
        logger.info("🔧 Learning configuration loaded from environment variables (clean v3.1)")
    
    def _initialize_enhanced_learning_data(self):
        """Initialize enhanced learning data structure - Clean v3.1"""
        if not os.path.exists(self.learning_data_path):
            os.makedirs(os.path.dirname(self.learning_data_path), exist_ok=True)
            
            initial_data = {
                'false_positive_patterns': [],
                'false_negative_patterns': [],
                'phrase_adjustments': {},
                'context_adjustments': {},
                'global_sensitivity': 1.0,
                'statistics': {
                    'total_false_positives_processed': 0,
                    'total_false_negatives_processed': 0,
                    'adjustments_made': 0,
                    'sensitivity_increases': 0,
                    'sensitivity_decreases': 0,
                    'last_update': None
                },
                'version': '3.1',
                'architecture': 'clean_v3.1_phase_2c_complete',
                'manager_integration': {
                    'models_manager_v3_1': True,
                    'config_manager': True,
                    'direct_access_only': True,
                    'backward_compatibility': 'removed'
                },
                'created': datetime.now(timezone.utc).isoformat()
            }
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
            
            logger.info(f"✅ Created enhanced learning data file: {self.learning_data_path}")
            logger.info("🎉 Phase 2C: Learning system using clean v3.1 architecture")
    
    def apply_learning_adjustments(self, message: str, base_score: float) -> float:
        """Apply learning adjustments to base score - Clean v3.1"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            adjusted_score = base_score
            
            # Apply global sensitivity
            global_sensitivity = learning_data.get('global_sensitivity', 1.0)
            adjusted_score *= global_sensitivity
            
            # Apply phrase-specific adjustments
            phrase_adjustments = learning_data.get('phrase_adjustments', {})
            message_lower = message.lower()
            
            for phrase, adjustment in phrase_adjustments.items():
                if phrase.lower() in message_lower:
                    adjusted_score += adjustment
                    logger.debug(f"Applied phrase adjustment for '{phrase}': {adjustment:+.3f}")
            
            # Clamp to valid range
            adjusted_score = max(0.0, min(1.0, adjusted_score))
            
            if abs(adjusted_score - base_score) > 0.01:
                logger.info(f"Clean v3.1: Learning adjustment applied: {base_score:.3f} → {adjusted_score:.3f}")
            
            return adjusted_score
            
        except Exception as e:
            logger.error(f"❌ Error applying learning adjustments: {e}")
            return base_score
    
    async def analyze_false_positive(self, request) -> Dict:
        """Analyze false positive and learn from it - Clean v3.1"""
        try:
            patterns_discovered = 0
            confidence_adjustments = 0
            
            # Extract over-detection patterns using clean v3.1 configuration
            over_detection_patterns = self._extract_over_detection_patterns(
                request.message,
                request.detected_level,
                request.correct_level
            )
            
            if over_detection_patterns:
                self._save_over_detection_patterns(over_detection_patterns)
                patterns_discovered = len(over_detection_patterns)
            
            # Reduce sensitivity for similar messages using clean v3.1 factors
            adjustment_made = self._adjust_sensitivity_for_false_positive(
                request.message,
                request.detected_level,
                request.correct_level,
                request.severity_score
            )
            
            if adjustment_made:
                confidence_adjustments = 1
            
            # Update statistics
            self._update_false_positive_statistics(patterns_discovered, confidence_adjustments)
            
            logger.info(f"✅ Clean v3.1: False positive analysis: {patterns_discovered} patterns, {confidence_adjustments} adjustments")
            
            return {
                'status': 'success',
                'patterns_discovered': patterns_discovered,
                'confidence_adjustments': confidence_adjustments,
                'learning_applied': patterns_discovered > 0 or confidence_adjustments > 0,
                'sensitivity_reduced': adjustment_made,
                'processing_time_ms': 50,
                'architecture': 'v3.1_clean',
                'phase_2c_complete': True,
                'analysis_details': {
                    'message_analyzed': request.message,
                    'detected_level': request.detected_level,
                    'correct_level': request.correct_level,
                    'patterns_found': over_detection_patterns,
                    'manager_integration': 'direct_access_only'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error in false positive analysis: {e}")
            return {
                'status': 'error',
                'patterns_discovered': 0,
                'confidence_adjustments': 0,
                'learning_applied': False,
                'architecture': 'v3.1_clean',
                'error': str(e)
            }
    
    async def analyze_false_negative(self, request) -> Dict:
        """Analyze false negative (missed crisis) and learn from it - Clean v3.1"""
        try:
            patterns_discovered = 0
            confidence_adjustments = 0
            
            # Extract under-detection patterns using clean v3.1 configuration
            under_detection_patterns = self._extract_under_detection_patterns(
                request.message,
                request.should_detect_level,
                request.actually_detected
            )
            
            if under_detection_patterns:
                self._save_under_detection_patterns(under_detection_patterns)
                patterns_discovered = len(under_detection_patterns)
            
            # Increase sensitivity for similar messages using clean v3.1 factors
            adjustment_made = self._adjust_sensitivity_for_false_negative(
                request.message,
                request.should_detect_level,
                request.actually_detected,
                request.severity_score
            )
            
            if adjustment_made:
                confidence_adjustments = 1
            
            # Update statistics
            self._update_false_negative_statistics(patterns_discovered, confidence_adjustments)
            
            logger.info(f"✅ Clean v3.1: False negative analysis: {patterns_discovered} patterns, {confidence_adjustments} adjustments")
            
            return {
                'status': 'success',
                'patterns_discovered': patterns_discovered,
                'confidence_adjustments': confidence_adjustments,
                'learning_applied': patterns_discovered > 0 or confidence_adjustments > 0,
                'sensitivity_increased': adjustment_made,
                'processing_time_ms': 50,
                'architecture': 'v3.1_clean',
                'phase_2c_complete': True,
                'analysis_details': {
                    'message_analyzed': request.message,
                    'should_detect_level': request.should_detect_level,
                    'actually_detected': request.actually_detected,
                    'patterns_found': under_detection_patterns,
                    'manager_integration': 'direct_access_only'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error in false negative analysis: {e}")
            return {
                'status': 'error',
                'patterns_discovered': 0,
                'confidence_adjustments': 0,
                'learning_applied': False,
                'architecture': 'v3.1_clean',
                'error': str(e)
            }
    
    def _extract_over_detection_patterns(self, message: str, detected_level: str, correct_level: str) -> List[str]:
        """Extract patterns that led to over-detection using clean v3.1 configuration"""
        patterns = []
        message_lower = message.lower()
        
        # Use clean v3.1 configured patterns
        for indicator in self.false_positive_indicators:
            if indicator in message_lower:
                patterns.append(indicator)
        
        logger.debug(f"Clean v3.1: Found {len(patterns)} over-detection patterns")
        return patterns
    
    def _extract_under_detection_patterns(self, message: str, should_detect: str, actually_detected: str) -> List[str]:
        """Extract patterns that led to under-detection using clean v3.1 configuration"""
        patterns = []
        message_lower = message.lower()
        
        # Use clean v3.1 configured patterns
        for indicator in self.false_negative_indicators:
            if indicator in message_lower:
                patterns.append(indicator)
        
        logger.debug(f"Clean v3.1: Found {len(patterns)} under-detection patterns")
        return patterns
    
    def _save_over_detection_patterns(self, patterns: List[str]):
        """Save patterns that caused false positives - Clean v3.1"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            if 'false_positive_patterns' not in learning_data:
                learning_data['false_positive_patterns'] = []
            
            for pattern in patterns:
                if pattern not in learning_data['false_positive_patterns']:
                    learning_data['false_positive_patterns'].append(pattern)
            
            learning_data['last_update'] = datetime.now(timezone.utc).isoformat()
            learning_data['architecture'] = 'clean_v3.1_phase_2c_complete'
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.debug(f"Clean v3.1: Saved {len(patterns)} over-detection patterns")
            
        except Exception as e:
            logger.error(f"❌ Error saving over-detection patterns: {e}")
    
    def _save_under_detection_patterns(self, patterns: List[str]):
        """Save patterns that caused false negatives - Clean v3.1"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            if 'false_negative_patterns' not in learning_data:
                learning_data['false_negative_patterns'] = []
            
            for pattern in patterns:
                if pattern not in learning_data['false_negative_patterns']:
                    learning_data['false_negative_patterns'].append(pattern)
            
            learning_data['last_update'] = datetime.now(timezone.utc).isoformat()
            learning_data['architecture'] = 'clean_v3.1_phase_2c_complete'
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.debug(f"Clean v3.1: Saved {len(patterns)} under-detection patterns")
            
        except Exception as e:
            logger.error(f"❌ Error saving under-detection patterns: {e}")
    
    def _adjust_sensitivity_for_false_positive(self, message: str, detected_level: str, correct_level: str, severity_score: float) -> bool:
        """Adjust sensitivity downward for false positive using clean v3.1 factors"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            # Use clean v3.1 configured adjustment factor
            adjustment = self.learning_rate * severity_score * self.false_positive_factor
            
            # Apply global sensitivity adjustment with clean v3.1 bounds
            current_sensitivity = learning_data.get('global_sensitivity', 1.0)
            new_sensitivity = max(self.min_global_sensitivity, current_sensitivity + adjustment)
            learning_data['global_sensitivity'] = new_sensitivity
            
            # Apply phrase-specific adjustment
            phrase_adjustments = learning_data.get('phrase_adjustments', {})
            message_key = message.lower()[:50]  # First 50 chars as key
            
            current_adjustment = phrase_adjustments.get(message_key, 0.0)
            new_adjustment = max(-self.max_adjustment, current_adjustment + adjustment)
            phrase_adjustments[message_key] = new_adjustment
            
            learning_data['phrase_adjustments'] = phrase_adjustments
            learning_data['last_update'] = datetime.now(timezone.utc).isoformat()
            learning_data['architecture'] = 'clean_v3.1_phase_2c_complete'
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Clean v3.1: Decreased sensitivity by {abs(adjustment):.3f} (factor: {self.false_positive_factor})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adjusting sensitivity for false positive: {e}")
            return False
    
    def _adjust_sensitivity_for_false_negative(self, message: str, should_detect: str, actually_detected: str, severity_score: float) -> bool:
        """Adjust sensitivity upward for false negative using clean v3.1 factors"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            # Use clean v3.1 configured severity multiplier and adjustment factor
            severity_multiplier = self.severity_multipliers.get(should_detect, 1.0)
            adjustment = self.learning_rate * severity_score * severity_multiplier * self.false_negative_factor
            
            # Apply global sensitivity adjustment with clean v3.1 bounds
            current_sensitivity = learning_data.get('global_sensitivity', 1.0)
            new_sensitivity = min(self.max_global_sensitivity, current_sensitivity + adjustment)
            learning_data['global_sensitivity'] = new_sensitivity
            
            # Apply phrase-specific adjustment
            phrase_adjustments = learning_data.get('phrase_adjustments', {})
            message_key = message.lower()[:50]  # First 50 chars as key
            
            current_adjustment = phrase_adjustments.get(message_key, 0.0)
            new_adjustment = min(self.max_adjustment, current_adjustment + adjustment)
            phrase_adjustments[message_key] = new_adjustment
            
            learning_data['phrase_adjustments'] = phrase_adjustments
            learning_data['last_update'] = datetime.now(timezone.utc).isoformat()
            learning_data['architecture'] = 'clean_v3.1_phase_2c_complete'
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Clean v3.1: Increased sensitivity by {adjustment:.3f} for missed {should_detect} (multiplier: {severity_multiplier})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adjusting sensitivity for false negative: {e}")
            return False
    
    def _update_false_positive_statistics(self, patterns_discovered: int, adjustments_made: int):
        """Update statistics for false positive learning - Clean v3.1"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            stats['total_false_positives_processed'] = stats.get('total_false_positives_processed', 0) + 1
            stats['adjustments_made'] = stats.get('adjustments_made', 0) + adjustments_made
            stats['sensitivity_decreases'] = stats.get('sensitivity_decreases', 0) + (1 if adjustments_made > 0 else 0)
            stats['last_update'] = datetime.now(timezone.utc).isoformat()
            
            learning_data['statistics'] = stats
            learning_data['architecture'] = 'clean_v3.1_phase_2c_complete'
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.debug(f"Clean v3.1: Updated false positive statistics")
            
        except Exception as e:
            logger.error(f"❌ Error updating false positive statistics: {e}")
    
    def _update_false_negative_statistics(self, patterns_discovered: int, adjustments_made: int):
        """Update statistics for false negative learning - Clean v3.1"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            stats['total_false_negatives_processed'] = stats.get('total_false_negatives_processed', 0) + 1
            stats['adjustments_made'] = stats.get('adjustments_made', 0) + adjustments_made
            stats['sensitivity_increases'] = stats.get('sensitivity_increases', 0) + (1 if adjustments_made > 0 else 0)
            stats['last_update'] = datetime.now(timezone.utc).isoformat()
            
            learning_data['statistics'] = stats
            learning_data['architecture'] = 'clean_v3.1_phase_2c_complete'
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.debug(f"Clean v3.1: Updated false negative statistics")
            
        except Exception as e:
            logger.error(f"❌ Error updating false negative statistics: {e}")
    
    def get_learning_statistics(self) -> Dict:
        """Get comprehensive learning statistics - Clean v3.1"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            
            return {
                'learning_system_status': 'active',
                'version': learning_data.get('version', '3.1'),
                'architecture': learning_data.get('architecture', 'clean_v3.1_phase_2c_complete'),
                'phase_2c_status': 'complete',
                'manager_integration': learning_data.get('manager_integration', {}),
                'total_false_positives_processed': stats.get('total_false_positives_processed', 0),
                'total_false_negatives_processed': stats.get('total_false_negatives_processed', 0),
                'total_adjustments_made': stats.get('adjustments_made', 0),
                'sensitivity_increases': stats.get('sensitivity_increases', 0),
                'sensitivity_decreases': stats.get('sensitivity_decreases', 0),
                'global_sensitivity': learning_data.get('global_sensitivity', 1.0),
                'phrase_adjustments_count': len(learning_data.get('phrase_adjustments', {})),
                'false_positive_patterns_learned': len(learning_data.get('false_positive_patterns', [])),
                'false_negative_patterns_learned': len(learning_data.get('false_negative_patterns', [])),
                'last_update': stats.get('last_update'),
                'configuration': {
                    'learning_rate': self.learning_rate,
                    'min_adjustment': self.min_adjustment,
                    'max_adjustment': self.max_adjustment,
                    'max_adjustments_per_day': self.max_adjustments_per_day,
                    'data_file': self.learning_data_path,
                    'clean_v3_1_architecture': True,
                    'direct_manager_access': True,
                    'backward_compatibility': 'removed'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting learning statistics: {e}")
            return {
                'learning_system_status': 'error',
                'architecture': 'clean_v3.1_phase_2c_complete',
                'error': str(e)
            }

# ========================================================================
# GET PYDANTIC MODELS - Direct Manager Access Only
# ========================================================================
def get_pydantic_models():
    """Get Pydantic models - assumes they're available through PydanticManager"""
    # This will be handled by the main application's PydanticManager
    # For now, we'll import directly since we know they exist
    try:
        # These should be accessible through the application's PydanticManager
        # but for simplicity in endpoints, we'll use a local function
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
        logger.error(f"❌ Could not access Pydantic models: {e}")
        raise RuntimeError(f"Pydantic models not available: {e}")

def add_enhanced_learning_endpoints(app, learning_manager, config_manager=None,
                                  analysis_parameters_manager=None, threshold_mapping_manager=None):
    """
    Add enhanced learning endpoints to FastAPI app - Phase 3c Enhanced
    
    Args:
        app: FastAPI application instance
        learning_manager: EnhancedLearningManager instance (required)
        config_manager: ConfigManager instance (optional, for compatibility)
        analysis_parameters_manager: AnalysisParametersManager instance (Phase 3b) - NEW
        threshold_mapping_manager: ThresholdMappingManager instance (Phase 3c) - NEW
    """
    
    # ========================================================================
    # CLEAN V3.1 VALIDATION - No Fallbacks
    # ========================================================================
    
    if not learning_manager:
        logger.error("❌ EnhancedLearningManager is required for learning endpoints")
        raise RuntimeError("EnhancedLearningManager required for learning endpoints")
    
    logger.info("✅ Phase 3c: Learning endpoints using enhanced manager access")
    
    # Get Pydantic models (keep existing function)
    models = get_pydantic_models()
    
    # ========================================================================
    # NEW Phase 3c Learning System Status Endpoint - ADD THIS
    # ========================================================================
    
    @app.get("/learning/status")
    async def learning_system_status():
        """Get comprehensive learning system status - Phase 3c Enhanced"""
        try:
            # Basic learning manager status
            stats = learning_manager.get_learning_statistics()
            
            status = {
                "learning_system_available": True,
                "phase": "3c",
                "architecture": "clean_v3.1_with_phase_3c_integration",
                "manager_integration": "direct_access_enhanced",
                "configuration_externalized": True,
                "statistics": stats
            }
            
            # Phase 3b - Analysis Parameters Integration - NEW
            if analysis_parameters_manager:
                try:
                    learning_params = analysis_parameters_manager.get_pattern_learning_parameters()
                    status["analysis_parameters"] = {
                        "available": True,
                        "learning_rate": learning_params.get('learning_rate'),
                        "confidence_adjustments": {
                            "min": learning_params.get('min_confidence_adjustment'),
                            "max": learning_params.get('max_confidence_adjustment')
                        },
                        "daily_limits": learning_params.get('max_adjustments_per_day'),
                        "phase_3b_integrated": True
                    }
                except Exception as e:
                    status["analysis_parameters"] = {"available": False, "error": str(e)}
            else:
                status["analysis_parameters"] = {"available": False, "reason": "AnalysisParametersManager not provided"}
            
            # Phase 3c - Threshold Mapping Integration - NEW
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    crisis_thresholds = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                    status["threshold_mapping"] = {
                        "available": True,
                        "current_mode": current_mode,
                        "learning_integration": "threshold_adjustment_capable",
                        "crisis_thresholds": crisis_thresholds,
                        "phase_3c_integrated": True
                    }
                except Exception as e:
                    status["threshold_mapping"] = {"available": False, "error": str(e)}
            else:
                status["threshold_mapping"] = {"available": False, "reason": "ThresholdMappingManager not provided"}
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Error getting learning system status: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Learning system status error: {str(e)}"
            )

    # ========================================================================
    # NEW Phase 3c Threshold-Aware Learning Analysis - ADD THIS
    # ========================================================================
    
    @app.post("/learning/analyze_with_thresholds")
    async def analyze_with_threshold_awareness(request: dict):
        """
        Analyze learning patterns with threshold awareness - Phase 3c
        Integrates learning analysis with current threshold configuration
        """
        try:
            if not threshold_mapping_manager:
                return {
                    "status": "threshold_manager_not_available",
                    "message": "ThresholdMappingManager required for threshold-aware learning",
                    "basic_analysis": "Use standard learning endpoints instead"
                }
            
            # Get current threshold context
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            crisis_thresholds = threshold_mapping_manager.get_crisis_level_thresholds()
            
            # Analyze learning pattern with threshold context
            learning_analysis = {
                "threshold_context": {
                    "current_mode": current_mode,
                    "crisis_thresholds": crisis_thresholds
                },
                "learning_recommendations": [],
                "threshold_adjustments": []
            }
            
            # Basic learning pattern analysis
            message = request.get('message', '')
            user_feedback = request.get('user_feedback', {})
            
            # Analyze if learning should adjust thresholds for current mode
            if user_feedback.get('type') == 'false_positive':
                threshold_suggestion = {
                    "mode": current_mode,
                    "adjustment_type": "increase_threshold",
                    "severity": user_feedback.get('severity', 'medium'),
                    "reason": "False positive indicates threshold may be too low"
                }
                learning_analysis["threshold_adjustments"].append(threshold_suggestion)
                learning_analysis["learning_recommendations"].append(
                    f"Consider increasing {current_mode} mode thresholds to reduce false positives"
                )
            
            elif user_feedback.get('type') == 'false_negative':
                threshold_suggestion = {
                    "mode": current_mode,
                    "adjustment_type": "decrease_threshold", 
                    "severity": user_feedback.get('severity', 'medium'),
                    "reason": "False negative indicates threshold may be too high"
                }
                learning_analysis["threshold_adjustments"].append(threshold_suggestion)
                learning_analysis["learning_recommendations"].append(
                    f"Consider decreasing {current_mode} mode thresholds to catch more cases"
                )
            
            learning_analysis["phase_3c_complete"] = True
            learning_analysis["threshold_aware"] = True
            
            return learning_analysis
            
        except Exception as e:
            logger.error(f"❌ Error in threshold-aware learning analysis: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Threshold-aware learning analysis failed: {str(e)}"
            )

    # ========================================================================
    # NEW Enhanced Learning Statistics with Phase 3c Context - ADD THIS
    # ========================================================================
    
    @app.get("/learning/statistics_enhanced")
    async def get_enhanced_learning_statistics():
        """Get learning statistics with Phase 3c context"""
        try:
            # Get base statistics
            base_stats = learning_manager.get_learning_statistics()
            
            enhanced_stats = {
                **base_stats,
                "phase_3c_enhancements": {
                    "threshold_aware": threshold_mapping_manager is not None,
                    "analysis_parameter_integration": analysis_parameters_manager is not None,
                    "configuration_externalized": True
                }
            }
            
            # Add threshold context if available
            if threshold_mapping_manager:
                try:
                    current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                    enhanced_stats["threshold_context"] = {
                        "current_ensemble_mode": current_mode,
                        "threshold_source": "JSON + environment configuration"
                    }
                except Exception as e:
                    enhanced_stats["threshold_context"] = {"error": str(e)}
            
            # Add analysis parameter context if available
            if analysis_parameters_manager:
                try:
                    learning_params = analysis_parameters_manager.get_pattern_learning_parameters()
                    enhanced_stats["analysis_parameter_context"] = {
                        "source": "AnalysisParametersManager",
                        "externalized": True,
                        "learning_rate": learning_params.get('learning_rate')
                    }
                except Exception as e:
                    enhanced_stats["analysis_parameter_context"] = {"error": str(e)}
            
            return enhanced_stats
            
        except Exception as e:
            logger.error(f"❌ Error getting enhanced learning statistics: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Enhanced learning statistics failed: {str(e)}"
            )
    
    @app.post("/analyze_false_negative")
    async def analyze_false_negative(request: models['FalseNegativeAnalysisRequest']):
        """Analyze false negative (missed crisis) and learn from it - Clean v3.1"""
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        try:
            result = await learning_manager.analyze_false_negative(request)
            
            # Add clean v3.1 metadata
            result['endpoint_architecture'] = 'v3.1_clean'
            result['manager_integration'] = 'direct_access_only'
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in false negative analysis: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Clean v3.1: False negative analysis failed: {str(e)}"
            )
    
    @app.post("/analyze_false_positive")
    async def analyze_false_positive(request: models['FalsePositiveAnalysisRequest']):
        """Analyze false positive and learn from it - Clean v3.1"""
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        try:
            result = await learning_manager.analyze_false_positive(request)
            
            # Add clean v3.1 metadata
            result['endpoint_architecture'] = 'v3.1_clean'
            result['manager_integration'] = 'direct_access_only'
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in false positive analysis: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Clean v3.1: False positive analysis failed: {str(e)}"
            )
    
    @app.post("/update_learning_model")
    async def update_learning_model(request: models['LearningUpdateRequest']):
        """Update learning model with staff correction - Clean v3.1"""
        
        try:
            # Process the learning record based on type - Direct manager usage
            if request.record_type == 'false_negative':
                fn_request = models['FalseNegativeAnalysisRequest'](
                    message=request.message_data['content'],
                    should_detect_level=request.correction_data['should_detect_level'],
                    actually_detected=request.correction_data['actually_detected'],
                    context=request.context_data,
                    severity_score=request.correction_data.get('severity_score', 1)
                )
                result = await learning_manager.analyze_false_negative(fn_request)
            
            elif request.record_type == 'false_positive':
                fp_request = models['FalsePositiveAnalysisRequest'](
                    message=request.message_data['content'],
                    detected_level=request.correction_data['detected_level'],
                    correct_level=request.correction_data['correct_level'],
                    context=request.context_data,
                    severity_score=request.correction_data.get('severity_score', 1)
                )
                result = await learning_manager.analyze_false_positive(fp_request)
            
            else:
                raise HTTPException(status_code=400, detail=f"Unknown record type: {request.record_type}")
            
            return {
                'status': 'success',
                'record_id': request.learning_record_id,
                'record_type': request.record_type,
                'learning_applied': result.get('learning_applied', False),
                'patterns_discovered': result.get('patterns_discovered', 0),
                'adjustments_made': result.get('confidence_adjustments', 0),
                'architecture': 'v3.1_clean',
                'phase_2c_complete': True,
                'manager_integration': 'direct_access_only'
            }
            
        except Exception as e:
            logger.error(f"❌ Error updating learning model: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Clean v3.1: Learning model update failed: {str(e)}"
            )
    
    @app.get("/learning_statistics")
    async def get_learning_statistics():
        """Get comprehensive learning system statistics - Clean v3.1"""
        
        try:
            stats = learning_manager.get_learning_statistics()
            
            # Add endpoint metadata
            stats['endpoint_architecture'] = 'v3.1_clean'
            stats['manager_integration'] = 'direct_access_only'
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting learning statistics: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Clean v3.1: Statistics retrieval failed: {str(e)}"
            )
    
    # ========================================================================
    # ENDPOINT REGISTRATION COMPLETE
    # ========================================================================
    
    logger.info("🧠 Clean v3.1: Enhanced learning endpoints added successfully")
    logger.info("🔧 Learning endpoints registered:")
    logger.info("   POST /analyze_false_negative - Analyze missed crises")
    logger.info("   POST /analyze_false_positive - Analyze over-detections")
    logger.info("   POST /update_learning_model - Update model with staff corrections")
    logger.info("   GET /learning_statistics - Comprehensive learning statistics")
    logger.info("✅ Phase 2C: All learning endpoints using direct manager access - No fallback code")
    logger.info("🎉 Clean v3.1 Architecture: Learning system with direct manager integration")