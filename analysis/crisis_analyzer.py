"""
Updated Crisis Analyzer - Pass message parameter to enhanced_depression_analysis
This file needs to be updated to work with the false positive reduction fix
"""

import logging
import time
import re
from typing import Dict, List, Tuple, Any
from utils.context_helpers import extract_context_signals, analyze_sentiment_context
from utils.scoring_helpers import (
    extract_depression_score,
    enhanced_depression_analysis, 
    advanced_idiom_detection, 
    enhanced_crisis_level_mapping
)
from config.nlp_settings import CRISIS_THRESHOLDS

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """Handles crisis analysis using your existing depression + sentiment models"""
    
    def __init__(self, model_manager, learning_manager=None):
        self.model_manager = model_manager
        self.learning_manager = learning_manager

    async def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict:
        """
        Enhanced message analysis with multi-model approach
        This is your existing /analyze endpoint logic - UPDATED for false positive reduction
        """
        
        start_time = time.time()
        reasoning_steps = []
        
        try:
            # Step 1: Extract context signals
            context = extract_context_signals(message)
            reasoning_steps.append(f"Context: {context}")
            
            # Step 2: Run both ML models
            depression_result = self.model_manager.analyze_with_depression_model(message)
            sentiment_result = self.model_manager.analyze_with_sentiment_model(message)
            
            # Step 3: Analyze sentiment for context
            sentiment_scores = analyze_sentiment_context(sentiment_result)
            reasoning_steps.append(f"Sentiment: {sentiment_scores}")
            
            # Step 4: Enhanced depression model analysis
            # CRITICAL CHANGE: Pass message parameter for false positive reduction
            depression_score, depression_categories = enhanced_depression_analysis(
                depression_result, sentiment_scores, context, message=message  # <-- ADDED message parameter
            )
            reasoning_steps.append(f"Depression model: {depression_score:.3f}")
            
            # Step 4.5: Apply learning adjustments if available
            if self.learning_manager:
                adjusted_score = self.learning_manager.apply_learning_adjustments(message, depression_score)
                if abs(adjusted_score - depression_score) > 0.01:  # Only log if significant change
                    reasoning_steps.append(f"Learning adjustment: {depression_score:.3f} → {adjusted_score:.3f}")
                    depression_score = adjusted_score

            # Step 5: Apply context adjustments and advanced idiom detection
            adjusted_score = advanced_idiom_detection(message, context, depression_score)
            reasoning_steps.append(f"Context-adjusted: {adjusted_score:.3f}")
            
            # Step 6: Final score
            final_score = adjusted_score
            
            # Step 7: Map to crisis level using enhanced mapping
            crisis_level = enhanced_crisis_level_mapping(final_score)
            needs_response = crisis_level != 'none'
            
            # Step 8: Collect all detected categories
            detected_categories = []
            if depression_categories:
                detected_categories.extend([cat.get('category', 'unknown') for cat in depression_categories])
            
            # Add sentiment categories if significant
            if sentiment_scores:
                for sentiment_type, score in sentiment_scores.items():
                    if score > 0.6:  # Significant sentiment
                        detected_categories.append(f"{sentiment_type}_sentiment")
            
            processing_time = (time.time() - start_time) * 1000
            
            # Compile reasoning
            full_reasoning = " | ".join(reasoning_steps)
            
            result = {
                'needs_response': needs_response,
                'crisis_level': crisis_level,
                'confidence_score': final_score,
                'detected_categories': detected_categories,
                'method': 'enhanced_ml_analysis_with_false_positive_reduction',  # Updated method name
                'processing_time_ms': processing_time,
                'model_info': 'DeBERTa + RoBERTa with Enhanced Learning + False Positive Reduction',
                'reasoning': full_reasoning,
                'analysis': {
                    'depression_score': extract_depression_score(depression_result),
                    'sentiment_scores': sentiment_scores,  # ← KEY ADDITION
                    'context_signals': context,
                    'crisis_indicators': [cat.get('category', 'unknown') for cat in detected_categories if isinstance(cat, dict)]
                }
            }
            
            logger.info(f"Enhanced analysis complete: {result['crisis_level']} confidence={result['confidence_score']:.3f} time={result['processing_time_ms']:.1f}ms")
            return result
            
        except Exception as e:
            logger.error(f"Error in enhanced crisis analysis: {e}")
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

    def analyze_with_context(self, message: str, context: Dict, message_text: str = None) -> Tuple[float, List[Dict]]:
        """
        Compatibility method for direct scoring calls
        This method may be called by other parts of the system
        """
        try:
            # Use the message_text parameter if provided, otherwise use the first message parameter
            text_to_analyze = message_text if message_text else message
            
            # Run the models
            depression_result = self.model_manager.analyze_with_depression_model(text_to_analyze)
            sentiment_result = self.model_manager.analyze_with_sentiment_model(text_to_analyze)
            
            # Analyze sentiment for context
            sentiment_scores = analyze_sentiment_context(sentiment_result)
            
            # Enhanced depression analysis with message parameter
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