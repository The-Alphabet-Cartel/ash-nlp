"""
Enhanced Learning Endpoints for NLP Server v3.1
Handles false positive and false negative staff corrections
FIXED: Clean manager architecture with proper function signatures
"""

import logging
import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from fastapi import HTTPException

# Import centralized models
from models.pydantic_models import (
    FalsePositiveAnalysisRequest, 
    FalseNegativeAnalysisRequest, 
    LearningUpdateRequest
)

logger = logging.getLogger(__name__)

class EnhancedLearningManager:
    """Enhanced learning manager with clean manager architecture support"""
    
    def __init__(self, model_manager, config_manager):
        """Initialize with clean manager architecture - JSON defaults + ENV overrides"""
        self.model_manager = model_manager
        self.config_manager = config_manager
        
        # Use ConfigManager for JSON defaults + ENV overrides pattern
        if config_manager:
            try:
                # Load learning configuration with JSON defaults + ENV overrides
                learning_config = config_manager.get_config("learning_parameters")
                if learning_config and "learning_system" in learning_config:
                    ls_config = learning_config["learning_system"]
                    
                    # ConfigManager handles ${VAR} substitution automatically
                    self.learning_data_path = ls_config.get('persistence_file', './learning_data/enhanced_learning_adjustments.json')
                    self.learning_rate = float(ls_config.get('learning_rate', 0.1))
                    self.min_adjustment = float(ls_config.get('min_adjustment', 0.05))
                    self.max_adjustment = float(ls_config.get('max_adjustment', 0.30))
                    self.max_adjustments_per_day = int(ls_config.get('max_adjustments_per_day', 50))
                    
                    # Load sensitivity bounds
                    sensitivity_bounds = ls_config.get('sensitivity_bounds', {})
                    self.min_global_sensitivity = float(sensitivity_bounds.get('min_global_sensitivity', 0.5))
                    self.max_global_sensitivity = float(sensitivity_bounds.get('max_global_sensitivity', 1.5))
                    
                    # Load pattern detection rules
                    pattern_config = ls_config.get('pattern_detection', {})
                    self.false_positive_indicators = pattern_config.get('false_positive_indicators', [])
                    self.false_negative_indicators = pattern_config.get('false_negative_indicators', [])
                    
                    # Load adjustment rules
                    adjustment_rules = ls_config.get('adjustment_rules', {})
                    self.false_positive_factor = float(adjustment_rules.get('false_positive_adjustment_factor', -0.1))
                    self.false_negative_factor = float(adjustment_rules.get('false_negative_adjustment_factor', 0.1))
                    self.severity_multipliers = adjustment_rules.get('severity_multipliers', {'high': 3.0, 'medium': 2.0, 'low': 1.0})
                    
                    logger.info("🔧 Learning configuration loaded from JSON + ENV overrides")
                else:
                    raise Exception("learning_parameters.json not found or invalid")
            except Exception as e:
                logger.warning(f"⚠️ Could not load learning config from JSON, using environment fallback: {e}")
                self._load_from_environment()
        else:
            logger.warning("⚠️ No config_manager provided, using environment fallback")
            self._load_from_environment()
        
        # Initialize learning data
        self._initialize_enhanced_learning_data()
        
        logger.info("🧠 Enhanced learning manager initialized with clean manager architecture")
        logger.info(f"   Learning rate: {self.learning_rate}")
        logger.info(f"   Adjustment range: {self.min_adjustment} to {self.max_adjustment}")
        logger.info(f"   Max adjustments per day: {self.max_adjustments_per_day}")
        logger.info(f"   Sensitivity bounds: {self.min_global_sensitivity} to {self.max_global_sensitivity}")
        logger.info(f"   Data file: {self.learning_data_path}")
    
    def _load_from_environment(self):
        """Fallback method to load configuration from environment variables only"""
        self.learning_data_path = os.getenv('NLP_LEARNING_PERSISTENCE_FILE', './learning_data/enhanced_learning_adjustments.json')
        self.learning_rate = float(os.getenv('NLP_LEARNING_RATE', '0.1'))
        self.min_adjustment = float(os.getenv('NLP_MIN_CONFIDENCE_ADJUSTMENT', '0.05'))
        self.max_adjustment = float(os.getenv('NLP_MAX_CONFIDENCE_ADJUSTMENT', '0.30'))
        self.max_adjustments_per_day = int(os.getenv('NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY', '50'))
        
        # Hardcoded defaults for fallback
        self.min_global_sensitivity = 0.5
        self.max_global_sensitivity = 1.5
        self.false_positive_indicators = [
            'just tired', 'dead tired', 'dying of laughter', 'killing it',
            'murder a burger', 'joke killed me', 'that\'s brutal', 'insane workout'
        ]
        self.false_negative_indicators = [
            'don\'t want to be here', 'tired of everything', 'can\'t go on',
            'no point', 'what\'s the use', 'giving up', 'had enough'
        ]
        self.false_positive_factor = -0.1
        self.false_negative_factor = 0.1
        self.severity_multipliers = {'high': 3.0, 'medium': 2.0, 'low': 1.0}
        
        logger.info("🔧 Learning configuration loaded from environment variables (fallback)")
    
    def _initialize_enhanced_learning_data(self):
        """Initialize enhanced learning data structure"""
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
                'architecture': 'clean_manager_v3.1',
                'created': datetime.now(timezone.utc).isoformat()
            }
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
            
            logger.info(f"✅ Created enhanced learning data file: {self.learning_data_path}")
    
    def apply_learning_adjustments(self, message: str, base_score: float) -> float:
        """Apply learning adjustments to base score"""
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
                logger.info(f"Learning adjustment applied: {base_score:.3f} → {adjusted_score:.3f}")
            
            return adjusted_score
            
        except Exception as e:
            logger.error(f"Error applying learning adjustments: {e}")
            return base_score
    
    async def analyze_false_positive(self, request: FalsePositiveAnalysisRequest) -> Dict:
        """Analyze false positive and learn from it"""
        try:
            patterns_discovered = 0
            confidence_adjustments = 0
            
            # Extract over-detection patterns
            over_detection_patterns = self._extract_over_detection_patterns(
                request.message,
                request.detected_level,
                request.correct_level
            )
            
            if over_detection_patterns:
                self._save_over_detection_patterns(over_detection_patterns)
                patterns_discovered = len(over_detection_patterns)
            
            # Reduce sensitivity for similar messages
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
            
            logger.info(f"✅ False positive analysis: {patterns_discovered} patterns, {confidence_adjustments} adjustments")
            
            return {
                'status': 'success',
                'patterns_discovered': patterns_discovered,
                'confidence_adjustments': confidence_adjustments,
                'learning_applied': patterns_discovered > 0 or confidence_adjustments > 0,
                'sensitivity_reduced': adjustment_made,
                'processing_time_ms': 50,  # Placeholder
                'analysis_details': {
                    'message_analyzed': request.message,
                    'detected_level': request.detected_level,
                    'correct_level': request.correct_level,
                    'patterns_found': over_detection_patterns
                }
            }
            
        except Exception as e:
            logger.error(f"Error in false positive analysis: {e}")
            return {
                'status': 'error',
                'patterns_discovered': 0,
                'confidence_adjustments': 0,
                'learning_applied': False,
                'error': str(e)
            }
    
    async def analyze_false_negative(self, request: FalseNegativeAnalysisRequest) -> Dict:
        """Analyze false negative (missed crisis) and learn from it"""
        try:
            patterns_discovered = 0
            confidence_adjustments = 0
            
            # Extract under-detection patterns
            under_detection_patterns = self._extract_under_detection_patterns(
                request.message,
                request.should_detect_level,
                request.actually_detected
            )
            
            if under_detection_patterns:
                self._save_under_detection_patterns(under_detection_patterns)
                patterns_discovered = len(under_detection_patterns)
            
            # Increase sensitivity for similar messages
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
            
            logger.info(f"✅ False negative analysis: {patterns_discovered} patterns, {confidence_adjustments} adjustments")
            
            return {
                'status': 'success',
                'patterns_discovered': patterns_discovered,
                'confidence_adjustments': confidence_adjustments,
                'learning_applied': patterns_discovered > 0 or confidence_adjustments > 0,
                'sensitivity_increased': adjustment_made,
                'processing_time_ms': 50,  # Placeholder
                'analysis_details': {
                    'message_analyzed': request.message,
                    'should_detect_level': request.should_detect_level,
                    'actually_detected': request.actually_detected,
                    'patterns_found': under_detection_patterns
                }
            }
            
        except Exception as e:
            logger.error(f"Error in false negative analysis: {e}")
            return {
                'status': 'error',
                'patterns_discovered': 0,
                'confidence_adjustments': 0,
                'learning_applied': False,
                'error': str(e)
            }
    
    def _extract_over_detection_patterns(self, message: str, detected_level: str, correct_level: str) -> List[str]:
        """Extract patterns that led to over-detection using JSON-configured patterns"""
        patterns = []
        message_lower = message.lower()
        
        # Use JSON-configured patterns (with ENV overrides)
        for indicator in self.false_positive_indicators:
            if indicator in message_lower:
                patterns.append(indicator)
        
        return patterns
    
    def _extract_under_detection_patterns(self, message: str, should_detect: str, actually_detected: str) -> List[str]:
        """Extract patterns that led to under-detection using JSON-configured patterns"""
        patterns = []
        message_lower = message.lower()
        
        # Use JSON-configured patterns (with ENV overrides)
        for indicator in self.false_negative_indicators:
            if indicator in message_lower:
                patterns.append(indicator)
        
        return patterns
    
    def _save_over_detection_patterns(self, patterns: List[str]):
        """Save patterns that caused false positives"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            if 'false_positive_patterns' not in learning_data:
                learning_data['false_positive_patterns'] = []
            
            for pattern in patterns:
                if pattern not in learning_data['false_positive_patterns']:
                    learning_data['false_positive_patterns'].append(pattern)
            
            learning_data['last_update'] = datetime.now(timezone.utc).isoformat()
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving over-detection patterns: {e}")
    
    def _save_under_detection_patterns(self, patterns: List[str]):
        """Save patterns that caused false negatives"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            if 'false_negative_patterns' not in learning_data:
                learning_data['false_negative_patterns'] = []
            
            for pattern in patterns:
                if pattern not in learning_data['false_negative_patterns']:
                    learning_data['false_negative_patterns'].append(pattern)
            
            learning_data['last_update'] = datetime.now(timezone.utc).isoformat()
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving under-detection patterns: {e}")
    
    def _adjust_sensitivity_for_false_positive(self, message: str, detected_level: str, correct_level: str, severity_score: float) -> bool:
        """Adjust sensitivity downward for false positive using JSON-configured factors"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            # Use JSON-configured adjustment factor
            adjustment = self.learning_rate * severity_score * self.false_positive_factor
            
            # Apply global sensitivity adjustment with JSON-configured bounds
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
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Decreased sensitivity by {abs(adjustment):.3f} for false positive (JSON-configured factor: {self.false_positive_factor})")
            return True
            
        except Exception as e:
            logger.error(f"Error adjusting sensitivity for false positive: {e}")
            return False
    
    def _adjust_sensitivity_for_false_negative(self, message: str, should_detect: str, actually_detected: str, severity_score: float) -> bool:
        """Adjust sensitivity upward for false negative using JSON-configured factors"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            # Use JSON-configured severity multiplier and adjustment factor
            severity_multiplier = self.severity_multipliers.get(should_detect, 1.0)
            adjustment = self.learning_rate * severity_score * severity_multiplier * self.false_negative_factor
            
            # Apply global sensitivity adjustment with JSON-configured bounds
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
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Increased sensitivity by {adjustment:.3f} for missed {should_detect} crisis (multiplier: {severity_multiplier}, factor: {self.false_negative_factor})")
            return True
            
        except Exception as e:
            logger.error(f"Error adjusting sensitivity for false negative: {e}")
            return False
    
    def _update_false_positive_statistics(self, patterns_discovered: int, adjustments_made: int):
        """Update statistics for false positive learning"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            stats['total_false_positives_processed'] = stats.get('total_false_positives_processed', 0) + 1
            stats['adjustments_made'] = stats.get('adjustments_made', 0) + adjustments_made
            stats['sensitivity_decreases'] = stats.get('sensitivity_decreases', 0) + (1 if adjustments_made > 0 else 0)
            stats['last_update'] = datetime.now(timezone.utc).isoformat()
            
            learning_data['statistics'] = stats
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating false positive statistics: {e}")
    
    def _update_false_negative_statistics(self, patterns_discovered: int, adjustments_made: int):
        """Update statistics for false negative learning"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            stats['total_false_negatives_processed'] = stats.get('total_false_negatives_processed', 0) + 1
            stats['adjustments_made'] = stats.get('adjustments_made', 0) + adjustments_made
            stats['sensitivity_increases'] = stats.get('sensitivity_increases', 0) + (1 if adjustments_made > 0 else 0)
            stats['last_update'] = datetime.now(timezone.utc).isoformat()
            
            learning_data['statistics'] = stats
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating false negative statistics: {e}")
    
    def get_learning_statistics(self) -> Dict:
        """Get comprehensive learning statistics"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            
            return {
                'learning_system_status': 'active',
                'version': learning_data.get('version', '3.1'),
                'architecture': learning_data.get('architecture', 'clean_manager_v3.1'),
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
                    'data_file': self.learning_data_path
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            return {
                'learning_system_status': 'error',
                'error': str(e)
            }

def add_enhanced_learning_endpoints(app, learning_manager, config_manager=None):
    """
    Add enhanced learning endpoints to FastAPI app
    FIXED: Function signature now accepts config_manager parameter
    """
    
    @app.post("/analyze_false_negative")
    async def analyze_false_negative(request: FalseNegativeAnalysisRequest):
        """Analyze false negative (missed crisis) and learn from it"""
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        try:
            result = await learning_manager.analyze_false_negative(request)
            return result
            
        except Exception as e:
            logger.error(f"Error in false negative analysis: {e}")
            raise HTTPException(status_code=500, detail=f"False negative analysis failed: {str(e)}")
    
    @app.post("/analyze_false_positive")
    async def analyze_false_positive(request: FalsePositiveAnalysisRequest):
        """Analyze false positive and learn from it"""
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        try:
            result = await learning_manager.analyze_false_positive(request)
            return result
            
        except Exception as e:
            logger.error(f"Error in false positive analysis: {e}")
            raise HTTPException(status_code=500, detail=f"False positive analysis failed: {str(e)}")
    
    @app.post("/update_learning_model")
    async def update_learning_model(request: LearningUpdateRequest):
        """Update learning model with staff correction"""
        
        try:
            # Process the learning record based on type
            if request.record_type == 'false_negative':
                fn_request = FalseNegativeAnalysisRequest(
                    message=request.message_data['content'],
                    should_detect_level=request.correction_data['should_detect_level'],
                    actually_detected=request.correction_data['actually_detected'],
                    context=request.context_data,
                    severity_score=request.correction_data.get('severity_score', 1)
                )
                result = await learning_manager.analyze_false_negative(fn_request)
            
            elif request.record_type == 'false_positive':
                fp_request = FalsePositiveAnalysisRequest(
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
                'adjustments_made': result.get('confidence_adjustments', 0)
            }
            
        except Exception as e:
            logger.error(f"Error updating learning model: {e}")
            raise HTTPException(status_code=500, detail=f"Learning model update failed: {str(e)}")
    
    @app.get("/learning_statistics")
    async def get_learning_statistics():
        """Get comprehensive learning system statistics"""
        
        try:
            stats = learning_manager.get_learning_statistics()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")
    
    logger.info("🧠 Enhanced learning endpoints added with clean manager architecture v3.1")