"""
Scoring Helpers for Ash NLP Service v3.1 - Phase 3a Updated
Enhanced scoring utilities with crisis pattern integration

Phase 3a: Updated to work without hardcoded pattern imports
All pattern analysis now handled by CrisisPatternManager
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Basic crisis level thresholds - these are algorithm constants, not patterns
DEFAULT_CRISIS_THRESHOLDS = {
    "high": 0.55,    # Reduced from 0.50 - matches new systematic approach
    "medium": 0.28,  # Reduced from 0.22 - more selective for medium alerts
    "low": 0.16      # Reduced from 0.12 - avoids very mild expressions
}

def extract_depression_score(message: str, depression_model, context: Dict = None) -> float:
    """Extract depression score from model - Phase 3a compatible"""
    
    if not depression_model:
        logger.warning("No depression model available for scoring")
        return 0.0
    
    try:
        # Get model prediction
        result = depression_model(message)
        
        if not result or not isinstance(result, list):
            logger.warning("Invalid depression model result")
            return 0.0
        
        # Extract score based on model output format
        for item in result:
            if isinstance(item, dict):
                label = item.get('label', '').lower()
                score = item.get('score', 0.0)
                
                # Look for crisis/depression indicators
                if any(indicator in label for indicator in ['crisis', 'depression', 'severe', 'high']):
                    logger.debug(f"Depression model score: {score:.3f} (label: {label})")
                    return float(score)
        
        # Fallback: return highest score
        max_score = max(item.get('score', 0.0) for item in result if isinstance(item, dict))
        logger.debug(f"Depression model fallback score: {max_score:.3f}")
        return float(max_score)
        
    except Exception as e:
        logger.error(f"Error extracting depression score: {e}")
        return 0.0

def enhanced_depression_analysis(message: str, base_score: float, depression_model, sentiment_model, 
                               context: Dict = None, crisis_pattern_manager=None) -> Dict[str, Any]:
    """
    Enhanced depression analysis with pattern integration - Phase 3a compatible
    
    Args:
        message: Message text to analyze
        base_score: Base depression score
        depression_model: Depression detection model
        sentiment_model: Sentiment analysis model  
        context: Optional context information
        crisis_pattern_manager: Optional CrisisPatternManager for pattern analysis
        
    Returns:
        Dictionary with enhanced analysis results
    """
    
    logger.debug(f"Enhanced depression analysis: base_score={base_score:.3f}")
    
    try:
        detected_categories = []
        adjustment_reasons = []
        
        # Sentiment analysis
        sentiment_scores = {}
        if sentiment_model:
            try:
                sentiment_result = sentiment_model(message)
                sentiment_scores = _process_sentiment_result(sentiment_result)
            except Exception as e:
                logger.warning(f"Sentiment analysis failed: {e}")
        
        # Pattern-based adjustments using CrisisPatternManager if available
        pattern_adjustment = 0.0
        if crisis_pattern_manager:
            try:
                # Apply context weights if available
                modified_score, weight_details = crisis_pattern_manager.apply_context_weights(message, base_score)
                pattern_adjustment = modified_score - base_score
                
                if pattern_adjustment != 0:
                    adjustment_reasons.append(f"pattern_analysis({pattern_adjustment:+.3f})")
                    logger.debug(f"Pattern adjustment: {pattern_adjustment:+.3f}")
                
            except Exception as e:
                logger.warning(f"Pattern analysis failed: {e}")
        
        # Context-based adjustments (conservative)
        context_adjustment = 0.0
        if context:
            # Social isolation indicators
            isolation_count = context.get('social_isolation_indicators', 0)
            if isolation_count > 2:
                context_adjustment += 0.04
                adjustment_reasons.append("social_isolation(+0.04)")
            
            # Hopelessness indicators
            hopelessness_count = context.get('hopelessness_indicators', 0)
            if hopelessness_count > 1:
                context_adjustment += 0.06
                adjustment_reasons.append("hopelessness(+0.06)")
            
            # Negation context (reduce score)
            if context.get('negation_context'):
                context_adjustment -= 0.05
                adjustment_reasons.append("negation(-0.05)")
        
        # Sentiment-based adjustments (conservative)
        sentiment_adjustment = 0.0
        if sentiment_scores:
            negative_score = sentiment_scores.get('negative', 0.0)
            if negative_score > 0.85:  # Very negative sentiment
                sentiment_adjustment += 0.08
                adjustment_reasons.append("very_negative_sentiment(+0.08)")
            elif negative_score > 0.70:  # Moderately negative
                sentiment_adjustment += 0.04
                adjustment_reasons.append("negative_sentiment(+0.04)")
        
        # Calculate final score
        total_adjustment = pattern_adjustment + context_adjustment + sentiment_adjustment
        final_score = base_score + total_adjustment
        final_score = max(0.0, min(1.0, final_score))  # Clamp to [0,1]
        
        # Determine categories
        if final_score >= 0.4:
            detected_categories.append("depression_indicators")
        if sentiment_scores.get('negative', 0) > 0.7:
            detected_categories.append("negative_sentiment")
        if context and context.get('social_isolation_indicators', 0) > 1:
            detected_categories.append("social_isolation")
        
        # Create reasoning
        reasoning_parts = [f"base_depression={base_score:.3f}"]
        reasoning_parts.extend(adjustment_reasons)
        reasoning_parts.append(f"final={final_score:.3f}")
        reasoning = " + ".join(reasoning_parts)
        
        logger.debug(f"Enhanced analysis complete: {reasoning}")
        
        return {
            'final_score': final_score,
            'base_score': base_score,
            'total_adjustment': total_adjustment,
            'pattern_adjustment': pattern_adjustment,
            'context_adjustment': context_adjustment,
            'sentiment_adjustment': sentiment_adjustment,
            'detected_categories': detected_categories,
            'sentiment_scores': sentiment_scores,
            'reasoning': reasoning,
            'adjustment_reasons': adjustment_reasons
        }
        
    except Exception as e:
        logger.error(f"Enhanced depression analysis failed: {e}")
        return {
            'final_score': base_score,
            'base_score': base_score,
            'total_adjustment': 0.0,
            'detected_categories': ['analysis_error'],
            'reasoning': f"Enhanced analysis failed: {str(e)}",
            'error': str(e)
        }

def advanced_idiom_detection(message: str, context: Dict, base_score: float, 
                           crisis_pattern_manager=None) -> float:
    """
    Advanced idiom detection with pattern manager integration - Phase 3a compatible
    
    Args:
        message: Message text to analyze
        context: Context information
        base_score: Base crisis score
        crisis_pattern_manager: Optional CrisisPatternManager for idiom patterns
        
    Returns:
        Adjusted score after idiom detection
    """
    
    if not crisis_pattern_manager:
        logger.debug("No CrisisPatternManager available for idiom detection")
        return base_score
    
    try:
        # Get idiom patterns from manager
        idiom_patterns = crisis_pattern_manager.get_idiom_patterns()
        
        if not idiom_patterns or not idiom_patterns.get('patterns'):
            logger.debug("No idiom patterns available")
            return base_score
        
        message_lower = message.lower().strip()
        
        # Check each idiom pattern group
        for pattern_name, pattern_group in idiom_patterns['patterns'].items():
            patterns = pattern_group.get('patterns', [])
            
            for pattern_config in patterns:
                pattern = pattern_config.get('pattern', '')
                reduction_factor = pattern_group.get('reduction_factor', 0.15)
                max_score_after = pattern_group.get('max_score_after', 0.10)
                
                try:
                    if re.search(pattern, message_lower, re.IGNORECASE):
                        # Apply idiom reduction
                        reduced_score = base_score * (1.0 - reduction_factor)
                        final_score = min(reduced_score, max_score_after)
                        
                        logger.info(f"Idiom detected ({pattern_name}): {base_score:.3f} → {final_score:.3f}")
                        return final_score
                        
                except re.error as e:
                    logger.warning(f"Invalid regex pattern '{pattern}': {e}")
                    continue
        
        return base_score
        
    except Exception as e:
        logger.error(f"Advanced idiom detection failed: {e}")
        return base_score

def enhanced_crisis_level_mapping(crisis_score: float, thresholds: Dict = None) -> str:
    """
    Enhanced crisis level mapping with configurable thresholds
    
    Args:
        crisis_score: Crisis confidence score (0.0 to 1.0)
        thresholds: Optional custom thresholds
        
    Returns:
        Crisis level string ('none', 'low', 'medium', 'high')
    """
    
    if thresholds is None:
        thresholds = DEFAULT_CRISIS_THRESHOLDS
    
    if crisis_score >= thresholds.get('high', 0.55):
        return 'high'
    elif crisis_score >= thresholds.get('medium', 0.28):
        return 'medium'
    elif crisis_score >= thresholds.get('low', 0.16):
        return 'low'
    else:
        return 'none'

def map_confidence_to_crisis_level(confidence: float, thresholds: Dict = None) -> str:
    """Map confidence score to crisis level using enhanced thresholds"""
    return enhanced_crisis_level_mapping(confidence, thresholds)

def determine_crisis_level_from_context(phrase_data: Dict, confidence: float) -> str:
    """Determine crisis level based on context and confidence"""
    
    context_type = phrase_data.get('context_type', '')
    crisis_boost = phrase_data.get('crisis_boost', 'low')
    
    # Temporal urgency is always concerning
    if context_type == 'temporal_urgency':
        return 'high' if confidence > 0.50 else 'medium'
    
    # Social isolation is medium-high concern
    if context_type == 'social_isolation':
        return 'medium' if confidence > 0.30 else 'low'
    
    # Capability loss varies by confidence
    if context_type == 'capability_loss':
        return 'medium' if confidence > 0.45 else 'low'
    
    # Default mapping with balanced thresholds
    return map_confidence_to_crisis_level(confidence)

async def score_phrases_with_models(model_manager, phrases: List[str], original_message: str) -> List[Dict]:
    """
    Score extracted phrases using the ML models
    
    Args:
        model_manager: ML model manager
        phrases: List of phrases to score
        original_message: Original message for context
        
    Returns:
        List of phrases with scores
    """
    
    if not model_manager or not phrases:
        return []
    
    scored_phrases = []
    
    try:
        # Get models
        depression_model = model_manager.get_model('depression') if hasattr(model_manager, 'get_model') else None
        
        for phrase in phrases:
            if isinstance(phrase, dict):
                phrase_text = phrase.get('text', '')
            else:
                phrase_text = str(phrase)
            
            if not phrase_text.strip():
                continue
            
            try:
                # Score phrase with depression model
                score = 0.0
                if depression_model:
                    score = extract_depression_score(phrase_text, depression_model)
                
                phrase_data = {
                    'text': phrase_text,
                    'score': score,
                    'model': 'depression',
                    'context': 'phrase_scoring'
                }
                
                # Preserve original phrase data if it was a dict
                if isinstance(phrase, dict):
                    phrase_data.update(phrase)
                    phrase_data['score'] = score  # Override with new score
                
                scored_phrases.append(phrase_data)
                
            except Exception as e:
                logger.warning(f"Failed to score phrase '{phrase_text}': {e}")
                continue
        
        logger.debug(f"Scored {len(scored_phrases)} phrases successfully")
        return scored_phrases
        
    except Exception as e:
        logger.error(f"Phrase scoring failed: {e}")
        return []

def filter_and_rank_phrases(phrases: List[Dict], parameters: Dict = None) -> List[Dict]:
    """
    Filter and rank phrases by relevance and confidence
    
    Args:
        phrases: List of phrase dictionaries with scores
        parameters: Optional filtering parameters
        
    Returns:
        Filtered and ranked list of phrases
    """
    
    if not phrases:
        return []
    
    try:
        # Default parameters
        min_confidence = parameters.get('min_confidence', 0.3) if parameters else 0.3
        max_results = parameters.get('max_results', 20) if parameters else 20
        
        # Filter by minimum confidence
        filtered_phrases = [
            phrase for phrase in phrases 
            if phrase.get('score', 0.0) >= min_confidence
        ]
        
        # Sort by score (descending)
        ranked_phrases = sorted(
            filtered_phrases,
            key=lambda x: x.get('score', 0.0),
            reverse=True
        )
        
        # Limit results
        final_phrases = ranked_phrases[:max_results]
        
        logger.debug(f"Filtered and ranked: {len(phrases)} → {len(final_phrases)} phrases")
        return final_phrases
        
    except Exception as e:
        logger.error(f"Phrase filtering failed: {e}")
        return phrases  # Return original if filtering fails

def _process_sentiment_result(sentiment_result) -> Dict[str, float]:
    """Helper function to process sentiment model results"""
    
    if not sentiment_result or not isinstance(sentiment_result, list):
        return {}
    
    sentiment_scores = {}
    
    try:
        for result in sentiment_result:
            if not isinstance(result, dict):
                continue
                
            label = result.get('label', '').upper()
            score = result.get('score', 0.0)
            
            # Handle different label formats
            if label in ['POSITIVE', 'POS']:
                sentiment_scores['positive'] = score
            elif label in ['NEGATIVE', 'NEG']:
                sentiment_scores['negative'] = score
            elif label in ['NEUTRAL', 'NEU']:
                sentiment_scores['neutral'] = score
            elif label in ['LABEL_0']:  # Cardiff NLP negative
                sentiment_scores['negative'] = score
            elif label in ['LABEL_1']:  # Cardiff NLP neutral
                sentiment_scores['neutral'] = score
            elif label in ['LABEL_2']:  # Cardiff NLP positive
                sentiment_scores['positive'] = score
        
        return sentiment_scores
        
    except Exception as e:
        logger.error(f"Error processing sentiment result: {e}")
        return {}

# Export for clean architecture
__all__ = [
    'extract_depression_score',
    'enhanced_depression_analysis',
    'advanced_idiom_detection',
    'enhanced_crisis_level_mapping',
    'map_confidence_to_crisis_level',
    'determine_crisis_level_from_context',
    'score_phrases_with_models',
    'filter_and_rank_phrases'
]