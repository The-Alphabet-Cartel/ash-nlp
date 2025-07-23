"""
Enhanced Learning Endpoints for NLP Server
ADD these endpoints to your ash-nlp/utils/learning_endpoints.py
"""

import logging
import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Any
from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class FalseNegativeRequest(BaseModel):
    """Request model for false negative analysis"""
    message: str
    should_detect_level: str
    actually_detected: str
    context: str
    severity_score: int

class LearningRecordRequest(BaseModel):
    """Request model for learning record updates"""
    learning_record_id: str
    record_type: str  # 'false_positive' or 'false_negative'
    message_data: Dict
    correction_data: Dict
    context_data: str
    timestamp: str

class EnhancedLearningManager:
    """Enhanced learning manager that handles both false positives and false negatives"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.learning_data_path = os.getenv('LEARNING_DATA_PATH', './data/enhanced_learning_adjustments.json')
        self.learning_rate = float(os.getenv('LEARNING_RATE', '0.1'))
        self.min_adjustment = float(os.getenv('MIN_CONFIDENCE_ADJUSTMENT', '0.05'))
        self.max_adjustment = float(os.getenv('MAX_CONFIDENCE_ADJUSTMENT', '0.30'))
        
        # Initialize learning data
        self._initialize_enhanced_learning_data()
        
        logger.info("🧠 Enhanced learning manager initialized with false positive + negative support")
    
    def _initialize_enhanced_learning_data(self):
        """Initialize enhanced learning data structure"""
        if not os.path.exists(self.learning_data_path):
            os.makedirs(os.path.dirname(self.learning_data_path), exist_ok=True)
            
            initial_data = {
                'false_positive_patterns': [],
                'false_negative_patterns': [],  # NEW: Patterns for missed crises
                'phrase_adjustments': {},
                'context_adjustments': {},
                'global_sensitivity': 1.0,  # NEW: Global sensitivity multiplier
                'statistics': {
                    'total_false_positives_processed': 0,
                    'total_false_negatives_processed': 0,  # NEW
                    'adjustments_made': 0,
                    'sensitivity_increases': 0,  # NEW: Track sensitivity increases
                    'sensitivity_decreases': 0,  # NEW: Track sensitivity decreases
                    'last_update': None
                }
            }
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
            
            logger.info(f"Created enhanced learning data file: {self.learning_data_path}")
    
    def apply_learning_adjustments(self, message: str, base_score: float) -> float:
        """Apply learned adjustments to crisis score"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            adjusted_score = base_score
            message_lower = message.lower()
            
            # Apply phrase-specific adjustments
            phrase_adjustments = learning_data.get('phrase_adjustments', {})
            for phrase, adjustment in phrase_adjustments.items():
                if phrase in message_lower:
                    adjusted_score += adjustment
                    logger.debug(f"Applied phrase adjustment for '{phrase}': {adjustment:+.3f}")
            
            # Apply context adjustments
            context_adjustments = learning_data.get('context_adjustments', {})
            for context_pattern, adjustment in context_adjustments.items():
                if context_pattern in message_lower:
                    adjusted_score += adjustment
                    logger.debug(f"Applied context adjustment for '{context_pattern}': {adjustment:+.3f}")
            
            # Apply global sensitivity multiplier
            global_sensitivity = learning_data.get('global_sensitivity', 1.0)
            if global_sensitivity != 1.0:
                adjusted_score *= global_sensitivity
                logger.debug(f"Applied global sensitivity: {global_sensitivity:.3f}")
            
            # Clamp to valid range
            adjusted_score = max(0.0, min(1.0, adjusted_score))
            
            return adjusted_score
            
        except Exception as e:
            logger.error(f"Error applying learning adjustments: {e}")
            return base_score
    
    async def analyze_false_negative(self, request: FalseNegativeRequest) -> Dict:
        """NEW: Analyze false negative (missed crisis) and update learning"""
        try:
            patterns_discovered = 0
            confidence_adjustments = 0
            
            # Analyze the message to understand why it was missed
            depression_result = self.model_manager.analyze_with_depression_model(request.message)
            sentiment_result = self.model_manager.analyze_with_sentiment_model(request.message)
            
            message_lower = request.message.lower()
            
            # Extract crisis patterns that were missed
            crisis_patterns = self._extract_missed_crisis_patterns(
                request.message, 
                request.should_detect_level,
                request.actually_detected,
                depression_result,
                sentiment_result
            )
            
            # Save missed patterns for future detection
            if crisis_patterns:
                self._save_missed_crisis_patterns(crisis_patterns, request.should_detect_level)
                patterns_discovered = len(crisis_patterns)
            
            # Adjust sensitivity for similar messages
            adjustment_made = self._adjust_sensitivity_for_missed_crisis(
                request.message,
                request.should_detect_level,
                request.actually_detected,
                request.severity_score
            )
            
            if adjustment_made:
                confidence_adjustments = 1
            
            # Update statistics
            self._update_false_negative_statistics(patterns_discovered, confidence_adjustments)
            
            logger.info(f"False negative analysis: {patterns_discovered} patterns, {confidence_adjustments} adjustments")
            
            return {
                'patterns_discovered': patterns_discovered,
                'confidence_adjustments': confidence_adjustments,
                'learning_applied': patterns_discovered > 0 or confidence_adjustments > 0,
                'analysis_type': 'false_negative',
                'sensitivity_increased': adjustment_made
            }
            
        except Exception as e:
            logger.error(f"Error in false negative analysis: {e}")
            return {
                'patterns_discovered': 0,
                'confidence_adjustments': 0,
                'learning_applied': False,
                'error': str(e)
            }
    
    def _extract_missed_crisis_patterns(self, message: str, should_detect: str, 
                                      actually_detected: str, depression_result, sentiment_result) -> List[str]:
        """Extract patterns from missed crisis messages"""
        patterns = []
        message_lower = message.lower()
        words = message_lower.split()
        
        # Extract key phrases that indicate crisis but were missed
        crisis_indicators = [
            'struggling with', 'can\'t handle', 'overwhelmed by', 'breaking down',
            'falling apart', 'losing it', 'at my limit', 'can\'t cope',
            'drowning in', 'suffocating', 'trapped', 'hopeless about',
            'giving up on', 'no point in', 'why bother', 'what\'s the use'
        ]
        
        for indicator in crisis_indicators:
            if indicator in message_lower:
                patterns.append(indicator)
        
        # Extract n-grams that might be crisis-related
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if len(bigram) > 8 and self._looks_like_crisis_pattern(bigram):
                patterns.append(bigram)
        
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
            if len(trigram) > 12 and self._looks_like_crisis_pattern(trigram):
                patterns.append(trigram)
        
        # Remove duplicates and filter
        unique_patterns = list(set(patterns))
        return [p for p in unique_patterns if self._is_valid_crisis_pattern(p)]
    
    def _looks_like_crisis_pattern(self, phrase: str) -> bool:
        """Check if a phrase looks like it could be a crisis pattern"""
        # Simple heuristics for crisis language
        crisis_words = [
            'feel', 'feeling', 'can\'t', 'cannot', 'don\'t', 'not', 'never',
            'always', 'struggling', 'hard', 'difficult', 'pain', 'hurt',
            'sad', 'angry', 'scared', 'worried', 'anxious', 'depressed'
        ]
        
        return any(word in phrase for word in crisis_words)
    
    def _is_valid_crisis_pattern(self, phrase: str) -> bool:
        """Validate that a phrase is a valid crisis pattern"""
        # Filter out overly generic phrases
        generic_phrases = ['i feel', 'i am', 'it is', 'i think', 'i know', 'i have']
        return phrase not in generic_phrases and len(phrase) > 4
    
    def _save_missed_crisis_patterns(self, patterns: List[str], crisis_level: str):
        """Save patterns from missed crises for future detection"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            if 'false_negative_patterns' not in learning_data:
                learning_data['false_negative_patterns'] = []
            
            for pattern in patterns:
                pattern_record = {
                    'pattern': pattern,
                    'crisis_level': crisis_level,
                    'discovered_at': datetime.now(timezone.utc).isoformat(),
                    'frequency': 1
                }
                
                # Check if pattern already exists
                existing_pattern = None
                for existing in learning_data['false_negative_patterns']:
                    if existing['pattern'] == pattern:
                        existing_pattern = existing
                        break
                
                if existing_pattern:
                    existing_pattern['frequency'] += 1
                else:
                    learning_data['false_negative_patterns'].append(pattern_record)
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Saved {len(patterns)} missed crisis patterns")
            
        except Exception as e:
            logger.error(f"Error saving missed crisis patterns: {e}")
    
    def _adjust_sensitivity_for_missed_crisis(self, message: str, should_detect: str, 
                                            actually_detected: str, severity_score: int) -> bool:
        """Adjust system sensitivity to catch similar missed crises"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            message_lower = message.lower()
            words = message_lower.split()
            
            # Calculate adjustment based on severity
            base_adjustment = self.learning_rate * (severity_score / 10.0)
            adjustment = min(self.max_adjustment, max(self.min_adjustment, base_adjustment))
            
            # Apply positive adjustments to increase sensitivity
            phrase_adjustments = learning_data.get('phrase_adjustments', {})
            
            # Extract key phrases and boost their scores
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                if self._looks_like_crisis_pattern(phrase):
                    current_adj = phrase_adjustments.get(phrase, 0.0)
                    phrase_adjustments[phrase] = min(self.max_adjustment, current_adj + adjustment)
            
            # Increase global sensitivity slightly
            current_sensitivity = learning_data.get('global_sensitivity', 1.0)
            sensitivity_increase = adjustment * 0.1  # Small global increase
            learning_data['global_sensitivity'] = min(1.5, current_sensitivity + sensitivity_increase)
            
            learning_data['phrase_adjustments'] = phrase_adjustments
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Increased sensitivity by {adjustment:.3f} for missed {should_detect} crisis")
            return True
            
        except Exception as e:
            logger.error(f"Error adjusting sensitivity for missed crisis: {e}")
            return False
    
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
    
    # Enhanced version of existing false positive analysis
    async def analyze_false_positive(self, request) -> Dict:
        """Enhanced false positive analysis"""
        try:
            patterns_discovered = 0
            confidence_adjustments = 0
            
            message_lower = request.message.lower()
            
            # Analyze why this was a false positive
            depression_result = self.model_manager.analyze_with_depression_model(request.message)
            sentiment_result = self.model_manager.analyze_with_sentiment_model(request.message)
            
            # Extract patterns that led to over-detection
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
            
            logger.info(f"False positive analysis: {patterns_discovered} patterns, {confidence_adjustments} adjustments")
            
            return {
                'patterns_discovered': patterns_discovered,
                'confidence_adjustments': confidence_adjustments,
                'learning_applied': patterns_discovered > 0 or confidence_adjustments > 0,
                'analysis_type': 'false_positive',
                'sensitivity_decreased': adjustment_made
            }
            
        except Exception as e:
            logger.error(f"Error in false positive analysis: {e}")
            return {
                'patterns_discovered': 0,
                'confidence_adjustments': 0,
                'learning_applied': False,
                'error': str(e)
            }
    
    def _extract_over_detection_patterns(self, message: str, detected_level: str, correct_level: str) -> List[str]:
        """Extract patterns that led to over-detection"""
        patterns = []
        message_lower = message.lower()
        
        # Common false positive patterns
        false_positive_indicators = [
            'just tired', 'dead tired', 'dying of laughter', 'killing it',
            'murder a burger', 'joke killed me', 'that\'s brutal', 'insane workout',
            'crazy day', 'driving me nuts', 'killing time', 'dead serious'
        ]
        
        for indicator in false_positive_indicators:
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
                pattern_record = {
                    'pattern': pattern,
                    'discovered_at': datetime.now(timezone.utc).isoformat(),
                    'frequency': 1
                }
                
                # Check if pattern already exists
                existing_pattern = None
                for existing in learning_data['false_positive_patterns']:
                    if existing['pattern'] == pattern:
                        existing_pattern = existing
                        break
                
                if existing_pattern:
                    existing_pattern['frequency'] += 1
                else:
                    learning_data['false_positive_patterns'].append(pattern_record)
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving over-detection patterns: {e}")
    
    def _adjust_sensitivity_for_false_positive(self, message: str, detected_level: str, 
                                             correct_level: str, severity_score: int) -> bool:
        """Adjust system sensitivity to reduce false positives"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            message_lower = message.lower()
            words = message_lower.split()
            
            # Calculate adjustment based on severity (negative for false positives)
            base_adjustment = -self.learning_rate * (severity_score / 10.0)
            adjustment = max(-self.max_adjustment, min(-self.min_adjustment, base_adjustment))
            
            # Apply negative adjustments to decrease sensitivity
            phrase_adjustments = learning_data.get('phrase_adjustments', {})
            
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                current_adj = phrase_adjustments.get(phrase, 0.0)
                phrase_adjustments[phrase] = max(-self.max_adjustment, current_adj + adjustment)
            
            # Decrease global sensitivity slightly
            current_sensitivity = learning_data.get('global_sensitivity', 1.0)
            sensitivity_decrease = -abs(adjustment) * 0.1  # Small global decrease
            learning_data['global_sensitivity'] = max(0.5, current_sensitivity + sensitivity_decrease)
            
            learning_data['phrase_adjustments'] = phrase_adjustments
            
            with open(self.learning_data_path, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            logger.info(f"Decreased sensitivity by {abs(adjustment):.3f} for false positive")
            return True
            
        except Exception as e:
            logger.error(f"Error adjusting sensitivity for false positive: {e}")
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
    
    def get_learning_statistics(self) -> Dict:
        """Get comprehensive learning statistics"""
        try:
            with open(self.learning_data_path, 'r') as f:
                learning_data = json.load(f)
            
            stats = learning_data.get('statistics', {})
            
            return {
                'learning_system_status': 'active',
                'total_false_positives_processed': stats.get('total_false_positives_processed', 0),
                'total_false_negatives_processed': stats.get('total_false_negatives_processed', 0),
                'total_adjustments_made': stats.get('adjustments_made', 0),
                'sensitivity_increases': stats.get('sensitivity_increases', 0),
                'sensitivity_decreases': stats.get('sensitivity_decreases', 0),
                'global_sensitivity': learning_data.get('global_sensitivity', 1.0),
                'phrase_adjustments_count': len(learning_data.get('phrase_adjustments', {})),
                'false_positive_patterns_learned': len(learning_data.get('false_positive_patterns', [])),
                'false_negative_patterns_learned': len(learning_data.get('false_negative_patterns', [])),
                'last_update': stats.get('last_update')
            }
            
        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            return {'error': str(e)}

def add_enhanced_learning_endpoints(app, learning_manager):
    """Add enhanced learning endpoints to FastAPI app"""
    
    @app.post("/analyze_false_negative")
    async def analyze_false_negative(request: FalseNegativeRequest):
        """NEW: Analyze false negative (missed crisis) and learn from it"""
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        try:
            result = await learning_manager.analyze_false_negative(request)
            return result
            
        except Exception as e:
            logger.error(f"Error in false negative analysis: {e}")
            raise HTTPException(status_code=500, detail=f"False negative analysis failed: {str(e)}")
    
    @app.post("/analyze_false_positive")
    async def analyze_false_positive(request):
        """Enhanced false positive analysis"""
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        try:
            result = await learning_manager.analyze_false_positive(request)
            return result
            
        except Exception as e:
            logger.error(f"Error in false positive analysis: {e}")
            raise HTTPException(status_code=500, detail=f"False positive analysis failed: {str(e)}")
    
    @app.post("/update_learning_model")
    async def update_learning_model(request: LearningRecordRequest):
        """Enhanced learning model update for both false positives and negatives"""
        
        try:
            # Process the learning record based on type
            if request.record_type == 'false_negative':
                # Create a false negative request
                fn_request = FalseNegativeRequest(
                    message=request.message_data['content'],
                    should_detect_level=request.correction_data['should_detect_level'],
                    actually_detected=request.correction_data['actually_detected'],
                    context=request.context_data,
                    severity_score=request.correction_data['severity_score']
                )
                result = await learning_manager.analyze_false_negative(fn_request)
            
            elif request.record_type == 'false_positive':
                # Handle false positive (existing logic enhanced)
                class FPRequest:
                    def __init__(self, msg, det, cor, ctx, sev):
                        self.message = msg
                        self.detected_level = det
                        self.correct_level = cor
                        self.context = ctx
                        self.severity_score = sev
                
                fp_request = FPRequest(
                    request.message_data['content'],
                    request.correction_data['detected_level'],
                    request.correction_data['correct_level'],
                    request.context_data,
                    request.correction_data['severity_score']
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
    
    logger.info("🧠 Enhanced learning endpoints added (false positives + negatives)")