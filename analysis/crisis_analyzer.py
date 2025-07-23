"""
Crisis Analyzer - Your existing crisis analysis logic
Handles the original depression + sentiment analysis with context
"""

import logging
import time
import re
from typing import Dict, List, Tuple, Any
from utils.context_helpers import extract_context_signals, analyze_sentiment_context
from utils.scoring_helpers import enhanced_depression_analysis, advanced_idiom_detection, enhanced_crisis_level_mapping
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
        This is your existing /analyze endpoint logic
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
            depression_score, depression_categories = enhanced_depression_analysis(
                depression_result, sentiment_scores, context
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
            reasoning_steps.append(f"Final score: {final_score:.3f}")
            
            # Step 7: Map to crisis level
            crisis_level = enhanced_crisis_level_mapping(final_score)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            # Combine categories
            all_categories = [cat['category'] for cat in depression_categories if isinstance(cat, dict)]
            
            # Create reasoning summary
            reasoning_summary = " | ".join(reasoning_steps)
            
            # Log results
            message_preview = message[:30] + "..." if len(message) > 30 else message
            logger.info(f"Enhanced Analysis: '{message_preview}' -> {crisis_level.upper()} (score: {final_score:.3f}, {processing_time:.1f}ms)")
            
            return {
                'needs_response': crisis_level != 'none',
                'crisis_level': crisis_level,
                'confidence_score': final_score,
                'detected_categories': all_categories,
                'method': 'enhanced_depression_model_with_context',
                'processing_time_ms': processing_time,
                'model_info': "depression+sentiment+context_analysis",
                'reasoning': reasoning_summary
            }
            
        except Exception as e:
            logger.error(f"Error in crisis analysis: {e}")
            raise