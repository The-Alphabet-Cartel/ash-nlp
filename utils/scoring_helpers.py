"""
Enhanced Scoring Helpers for Crisis Analysis
Provides advanced scoring algorithms and crisis level mapping

Updated: Cleaned up - removed phrase extraction specific functions
"""

import logging
import re
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

# Default crisis thresholds - Balanced for Three Zero-Shot Model Ensemble
DEFAULT_CRISIS_THRESHOLDS = {
    'high': 0.55,     # Definite intervention required
    'medium': 0.28,   # Monitor closely, potential intervention
    'low': 0.16,      # Basic awareness, minimal intervention
    'none': 0.0       # No crisis indicators
}

# Advanced idiom patterns with context awareness
ADVANCED_IDIOM_PATTERNS = {
    'killing_me': {
        'pattern': r'\b(killing me|kills me)\b',
        'reduction_factor': 0.3,
        'positive_context_keywords': ['funny', 'hilarious', 'lol', 'haha', 'game', 'homework', 'work'],
        'max_score_limit': 0.4
    },
    'dying': {
        'pattern': r'\b(dying|die)\b(?!\s+(to|for))',  # Don't match "dying to see" or "die for this"
        'reduction_factor': 0.4,
        'positive_context_keywords': ['funny', 'laughter', 'excited'],
        'max_score_limit': 0.35
    },
    'dead': {
        'pattern': r'\b(dead|deceased)\b(?!\s+(serious|really|literally))',
        'reduction_factor': 0.5,
        'positive_context_keywords': ['tired', 'exhausted', 'funny'],
        'max_score_limit': 0.3
    }
}

def extract_depression_score(message: str, model_result) -> float:
    """
    Extract depression score from model output with enhanced logic
    
    Args:
        message: Original message text
        model_result: Model prediction result
        
    Returns:
        Depression confidence score (0.0 to 1.0)
    """
    
    if not model_result:
        return 0.0
    
    try:
        # Handle different model output formats
        if isinstance(model_result, list) and len(model_result) > 0:
            result = model_result[0]
            
            if isinstance(result, dict):
                # Standard format: {'label': 'CRISIS', 'score': 0.85}
                label = result.get('label', '').upper()
                score = result.get('score', 0.0)
                
                # Map different label formats to depression score
                if label in ['CRISIS', 'DEPRESSION', 'NEGATIVE', 'HIGH']:
                    return score
                elif label in ['MILD_CRISIS', 'MILD_DEPRESSION', 'MEDIUM']:
                    return score * 0.7
                elif label in ['NEUTRAL', 'LOW']:
                    return score * 0.3
                else:
                    return 0.0
        
        elif isinstance(model_result, dict):
            # Direct dictionary format
            if 'depression_score' in model_result:
                return float(model_result['depression_score'])
            elif 'score' in model_result:
                return float(model_result['score'])
        
        elif isinstance(model_result, (int, float)):
            # Direct numeric score
            return float(model_result)
        
        return 0.0
        
    except Exception as e:
        logger.error(f"Error extracting depression score: {e}")
        return 0.0

def enhanced_depression_analysis(message: str, model_result, context: Dict = None) -> Dict[str, Any]:
    """
    Enhanced depression analysis with safety-first recalibration
    
    Args:
        message: Message text
        model_result: Depression model result
        context: Optional context information
        
    Returns:
        Enhanced analysis results with adjusted scores
    """
    
    base_score = extract_depression_score(message, model_result)
    
    # Safety-first recalibration factors
    safety_adjustments = {
        'temporal_urgency_boost': 0.15,    # "tonight", "now", "today"
        'definitive_language_boost': 0.12,  # "will", "going to", "plan to"
        'isolation_language_boost': 0.08,   # "alone", "nobody", "no one"
        'capability_loss_boost': 0.10       # "can't", "unable", "impossible"
    }
    
    adjusted_score = base_score
    applied_adjustments = []
    
    try:
        message_lower = message.lower()
        
        # Temporal urgency detection
        temporal_patterns = ['tonight', 'today', 'right now', 'immediately', 'soon']
        if any(pattern in message_lower for pattern in temporal_patterns):
            adjusted_score += safety_adjustments['temporal_urgency_boost']
            applied_adjustments.append('temporal_urgency')
        
        # Definitive language detection
        definitive_patterns = ['will kill', 'going to', 'plan to', 'decided to']
        if any(pattern in message_lower for pattern in definitive_patterns):
            adjusted_score += safety_adjustments['definitive_language_boost']
            applied_adjustments.append('definitive_language')
        
        # Isolation indicators
        isolation_patterns = ['alone', 'nobody cares', 'no one understands', 'isolated']
        if any(pattern in message_lower for pattern in isolation_patterns):
            adjusted_score += safety_adjustments['isolation_language_boost']
            applied_adjustments.append('isolation_language')
        
        # Capability loss indicators
        capability_patterns = ["can't go on", "can't take", "unable to", "impossible to"]
        if any(pattern in message_lower for pattern in capability_patterns):
            adjusted_score += safety_adjustments['capability_loss_boost']
            applied_adjustments.append('capability_loss')
        
        # Cap at 1.0
        adjusted_score = min(adjusted_score, 1.0)
        
        return {
            'base_score': base_score,
            'adjusted_score': adjusted_score,
            'applied_adjustments': applied_adjustments,
            'adjustment_total': adjusted_score - base_score,
            'safety_first_applied': len(applied_adjustments) > 0
        }
        
    except Exception as e:
        logger.error(f"Enhanced depression analysis failed: {e}")
        return {
            'base_score': base_score,
            'adjusted_score': base_score,
            'applied_adjustments': [],
            'adjustment_total': 0.0,
            'safety_first_applied': False,
            'error': str(e)
        }

def advanced_idiom_detection(message: str, base_score: float) -> float:
    """
    Advanced idiom detection with context-aware filtering
    
    Args:
        message: Message text to analyze
        base_score: Base crisis score before idiom filtering
        
    Returns:
        Adjusted score after idiom detection and filtering
    """
    
    if base_score <= 0.15:  # Don't reduce very low scores further
        return base_score
    
    try:
        message_lower = message.lower()
        
        for idiom_name, config in ADVANCED_IDIOM_PATTERNS.items():
            pattern = config['pattern']
            reduction_factor = config['reduction_factor']
            positive_keywords = config['positive_context_keywords']
            max_score_limit = config['max_score_limit']
            
            try:
                # Check if idiom pattern matches
                if re.search(pattern, message_lower):
                    # Check for positive context indicators
                    has_positive_context = any(
                        keyword in message_lower for keyword in positive_keywords
                    )
                    
                    if has_positive_context:
                        # Apply reduction factor
                        base_score *= (1 - reduction_factor)
                        
                        # Apply max score limit
                        base_score = min(base_score, max_score_limit)
                        
                        logger.debug(f"Applied idiom reduction for '{idiom_name}': score capped at {base_score:.3f}")
                        
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
    'determine_crisis_level_from_context'
]