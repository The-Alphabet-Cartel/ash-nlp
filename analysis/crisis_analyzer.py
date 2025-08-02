"""
CRITICAL FIXES for Crisis Analyzer - Three Zero-Shot Model Ensemble INTEGRATION
These changes fix the dangerous under-response bug and integrate ensemble analysis
"""

import logging
import time
import re
from typing import Dict, List, Tuple, Any
from utils.context_helpers import extract_context_signals, analyze_sentiment_context, process_sentiment_with_flip
from utils.scoring_helpers import (
    extract_depression_score,
    enhanced_depression_analysis, 
    advanced_idiom_detection, 
    enhanced_crisis_level_mapping
)
from managers.settings_manager import CRISIS_THRESHOLDS

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """UPDATED: Three Zero-Shot Model Ensemble crisis analysis with proper crisis level mapping"""
    
    def __init__(self, model_manager, learning_manager=None):
        self.model_manager = model_manager
        self.learning_manager = learning_manager

    async def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict:
        """
        UPDATED: Three Zero-Shot Model Ensemble analysis with FIXED crisis level mapping
        """
        
        start_time = time.time()
        reasoning_steps = []
        
        try:
            # Step 1: Extract context signals
            context = extract_context_signals(message)
            reasoning_steps.append(f"Context: {context}")
            
            # Step 2: Three Zero-Shot Model Ensemble ANALYSIS
            if hasattr(self.model_manager, 'analyze_with_ensemble'):
                # Use the new Three Zero-Shot Model Ensemble if available
                ensemble_result = self.model_manager.analyze_with_ensemble(message)
                
                # Extract consensus prediction for crisis level mapping
                consensus = ensemble_result.get('consensus', {})
                consensus_prediction = consensus.get('prediction', 'unknown')
                consensus_confidence = consensus.get('confidence', 0.0)
                
                # CRITICAL FIX: Map consensus prediction to crisis level
                crisis_level = self._map_consensus_to_crisis_level(consensus_prediction, consensus_confidence)
                needs_response = crisis_level != 'none'
                
                # Extract detected categories from all three models
                detected_categories = []
                individual_results = ensemble_result.get('individual_results', {})
                
                for model_name, results in individual_results.items():
                    if results and isinstance(results, list):
                        top_result = max(results, key=lambda x: x.get('score', 0))
                        detected_categories.append(f"{model_name}_{top_result.get('label', 'unknown')}")
                
                processing_time = (time.time() - start_time) * 1000
                
                # Enhanced result with ensemble data
                result = {
                    'message_analyzed': message,
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'ensemble_analysis': ensemble_result,  # Full ensemble details
                    'processing_time_ms': processing_time,
                    'model_info': 'three_model_ensemble',
                    'timestamp': time.time(),
                    
                    # FIXED: Crisis level determination
                    'requires_staff_review': self._requires_staff_review(crisis_level, consensus_confidence),
                    'consensus_prediction': consensus_prediction,
                    'consensus_confidence': consensus_confidence,
                    'consensus_method': consensus.get('method', 'unknown'),
                    
                    # CRITICAL: Proper crisis level and response determination
                    'crisis_level': crisis_level,
                    'needs_response': needs_response,
                    
                    # Legacy compatibility
                    'confidence_score': consensus_confidence,
                    'detected_categories': detected_categories,
                    'method': 'three_model_ensemble_v2'
                }
                
                logger.info(f"Three Zero-Shot Model Ensemble analysis: {crisis_level} confidence={consensus_confidence:.3f} consensus={consensus_prediction}")
                return result
                
            else:
                # Fallback to legacy two-model analysis
                return await self._legacy_two_model_analysis(message, user_id, channel_id, start_time)
                
        except Exception as e:
            logger.error(f"Error in ensemble crisis analysis: {e}")
            logger.exception("Full traceback:")
            # Return a safe fallback result
            return {
                'needs_response': False,
                'crisis_level': 'none', 
                'confidence_score': 0.0,
                'detected_categories': [],
                'method': 'error_fallback',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': 'Error fallback',
                'reasoning': f"Analysis failed: {str(e)}"
            }

    def _map_consensus_to_crisis_level(self, consensus_prediction: str, confidence: float) -> str:
        """
        CRITICAL FIX: Properly map ensemble consensus to crisis levels
        This fixes the dangerous under-response bug
        """
        pred_lower = consensus_prediction.lower()
        
        # CRISIS predictions (normalized from ensemble)
        if pred_lower == 'crisis':
            if confidence >= 0.70:
                return 'high'      # High confidence crisis
            elif confidence >= 0.45:
                return 'medium'    # Medium confidence crisis  
            else:
                return 'low'       # Low confidence crisis, but still crisis
        
        # MILD_CRISIS predictions 
        elif pred_lower == 'mild_crisis':
            if confidence >= 0.60:
                return 'low'       # Mild crisis with good confidence
            else:
                return 'none'      # Very uncertain mild crisis
        
        # SAFE predictions
        elif pred_lower in ['safe', 'neutral']:
            return 'none'
        
        # UNKNOWN or error cases - be conservative
        else:
            logger.warning(f"Unknown consensus prediction: {consensus_prediction}")
            if confidence > 0.50:  # If we're confident but don't know what it means, be safe
                return 'low'
            else:
                return 'none'

    def _requires_staff_review(self, crisis_level: str, confidence: float) -> bool:
        """Determine if staff review is required"""
        # High crisis always requires review
        if crisis_level == 'high':
            return True
        
        # Medium crisis with good confidence requires review
        if crisis_level == 'medium' and confidence >= 0.60:
            return True
        
        # Low crisis with very high confidence might need review
        if crisis_level == 'low' and confidence >= 0.80:
            return True
        
        return False

    async def _legacy_two_model_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Fallback to legacy two-model analysis if ensemble not available
        UPDATED: Fixed message parameter passing
        """
        reasoning_steps = []
        
        # Step 1: Extract context signals
        context = extract_context_signals(message)
        reasoning_steps.append(f"Context: {context}")
        
        # Step 2: Run both ML models
        depression_result = self.model_manager.analyze_with_depression_model(message)
        sentiment_result = self.model_manager.analyze_with_sentiment_model(message)
        
        # Step 3: Analyze sentiment for context
        raw_sentiment = analyze_sentiment_context(sentiment_result)
        sentiment_scores = process_sentiment_with_flip(raw_sentiment)
        reasoning_steps.append(f"Sentiment: {sentiment_scores}")
        
        # Step 4: Enhanced depression model analysis with MESSAGE PARAMETER
        depression_score, depression_categories = enhanced_depression_analysis(
            depression_result, sentiment_scores, context, message=message
        )
        reasoning_steps.append(f"Depression model: {depression_score:.3f}")
        
        # Step 4.5: Apply learning adjustments if available
        if self.learning_manager:
            adjusted_score = self.learning_manager.apply_learning_adjustments(message, depression_score)
            if abs(adjusted_score - depression_score) > 0.01:
                reasoning_steps.append(f"Learning adjustment: {depression_score:.3f} → {adjusted_score:.3f}")
                depression_score = adjusted_score

        # Step 5: Apply context adjustments and advanced idiom detection
        adjusted_score = advanced_idiom_detection(message, context, depression_score)
        reasoning_steps.append(f"Context-adjusted: {adjusted_score:.3f}")
        
        # Step 6: Final score
        final_score = adjusted_score
        
        # Step 7: FIXED crisis level mapping
        crisis_level = self._map_score_to_crisis_level(final_score)
        needs_response = crisis_level != 'none'
        
        # Step 8: Collect all detected categories
        detected_categories = []
        if depression_categories:
            detected_categories.extend([cat.get('category', 'unknown') for cat in depression_categories])
        
        # Add sentiment categories if significant
        if sentiment_scores:
            for sentiment_type, score in sentiment_scores.items():
                if score > 0.6:
                    detected_categories.append(f"{sentiment_type}_sentiment")
        
        processing_time = (time.time() - start_time) * 1000
        full_reasoning = " | ".join(reasoning_steps)
        
        result = {
            'needs_response': needs_response,
            'crisis_level': crisis_level,
            'confidence_score': final_score,
            'detected_categories': detected_categories,
            'method': 'enhanced_ml_analysis_with_false_positive_reduction',
            'processing_time_ms': processing_time,
            'model_info': 'DeBERTa + RoBERTa with Enhanced Learning + False Positive Reduction',
            'reasoning': full_reasoning,
            'analysis': {
                'depression_score': extract_depression_score(depression_result),
                'sentiment_scores': sentiment_scores,
                'context_signals': context,
                'crisis_indicators': [cat.get('category', 'unknown') for cat in detected_categories if isinstance(cat, dict)]
            }
        }
        
        logger.info(f"Legacy analysis complete: {result['crisis_level']} confidence={result['confidence_score']:.3f}")
        return result

    def _map_score_to_crisis_level(self, score: float) -> str:
        """
        FIXED: Legacy score-based crisis level mapping
        Uses proper thresholds for crisis classification
        """
        if score >= 0.65:    # Very high confidence crisis
            return 'high'
        elif score >= 0.40:  # Medium confidence crisis
            return 'medium'
        elif score >= 0.20:  # Low confidence crisis
            return 'low'
        else:
            return 'none'

    def analyze_with_context(self, message: str, context: Dict, message_text: str = None) -> Tuple[float, List[Dict]]:
        """
        UPDATED: Compatibility method with proper message parameter passing
        """
        try:
            text_to_analyze = message_text if message_text else message
            
            # Run the models
            depression_result = self.model_manager.analyze_with_depression_model(text_to_analyze)
            sentiment_result = self.model_manager.analyze_with_sentiment_model(text_to_analyze)
            
            # Analyze sentiment for context
            raw_sentiment = analyze_sentiment_context(sentiment_result)
            sentiment_scores = process_sentiment_with_flip(raw_sentiment)
            
            # Enhanced depression analysis with MESSAGE PARAMETER
            depression_score, depression_categories = enhanced_depression_analysis(
                depression_result, sentiment_scores, context, message=text_to_analyze
            )
            
            # Apply learning adjustments if available
            if self.learning_manager:
                depression_score = self.learning_manager.apply_learning_adjustments(text_to_analyze, depression_score)
            
            # Apply context adjustments
            final_score = advanced_idiom_detection(text_to_analyze, context, depression_score)
            
            return final_score, depression_categories
            
        except Exception as e:
            logger.error(f"Error in analyze_with_context: {e}")
            return 0.0, []