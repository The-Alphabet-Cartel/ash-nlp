"""
Scoring Helper Functions - BALANCED SAFETY-FIRST VERSION
Handles depression analysis, idiom detection, and crisis level mapping
"""

import logging
import re
from typing import Dict, List, Tuple
from config.nlp_settings import (
    CRISIS_THRESHOLDS, BURDEN_PATTERNS, HOPELESSNESS_PATTERNS, 
    STRUGGLE_PATTERNS, ENHANCED_IDIOM_PATTERNS
)

logger = logging.getLogger(__name__)

def extract_depression_score(depression_result) -> float:
    """Extract depression score from model's output"""
    
    if not depression_result:
        return 0.0
    
    # Handle different result formats
    predictions = []
    if isinstance(depression_result, list):
        if len(depression_result) > 0 and isinstance(depression_result[0], list):
            predictions = depression_result[0]
        elif len(depression_result) > 0 and isinstance(depression_result[0], dict):
            predictions = depression_result
    elif isinstance(depression_result, dict):
        predictions = [depression_result]
    
    # Extract scores
    moderate_score = 0.0
    severe_score = 0.0
    
    for pred in predictions:
        if not isinstance(pred, dict):
            continue
            
        label = str(pred.get('label', '')).lower().strip()
        score = float(pred.get('score', 0.0))
        
        if label == 'moderate':
            moderate_score = score
        elif label == 'severe':
            severe_score = score
    
    # Return combined depression signal
    return moderate_score + severe_score

def apply_false_positive_reduction(message: str, base_score: float) -> float:
    """Apply additional false positive reduction for common mild expression patterns"""
    message_lower = message.lower().strip()
    
    # Common false positive patterns for mild emotional expressions
    mild_expressions = [
        r"just feel\s+(?:so|really|pretty|kinda|)\s*down",
        r"feeling\s+(?:a bit|kind of|sort of|pretty|)\s*down",
        r"having\s+(?:a|an)\s*(?:rough|tough|bad|off)\s+(?:day|time|moment)",
        r"not\s+(?:doing|feeling)\s+(?:so|very|)\s*(?:great|good|well)",
        r"(?:been|having)\s+(?:a|an)\s*(?:rough|tough|hard|difficult)\s+(?:day|week|time)",
        r"feeling\s+(?:pretty|really|quite|)\s*(?:low|blue|sad)",
        r"(?:i'm|im)\s+(?:just|really|)\s*(?:tired|exhausted|drained)"
    ]
    
    # Casual conversational indicators (reduce crisis scoring)
    casual_indicators = [
        r"(?:lol|haha|😄|😅|🙂)",  # Humor indicators
        r"(?:just|only|kinda|sorta)",  # Minimizing language
        r"(?:today|right now|at the moment)",  # Temporal/temporary
    ]
    
    for pattern in mild_expressions:
        if re.search(pattern, message_lower):
            # Check if there are casual indicators that suggest it's not severe
            has_casual = any(re.search(casual, message_lower) for casual in casual_indicators)
            
            if has_casual:
                # More aggressive reduction for casual expressions
                reduced_score = base_score * 0.6  # 40% reduction
                logger.info(f"MILD+CASUAL EXPRESSION REDUCTION: {pattern} -> {base_score:.3f} → {reduced_score:.3f}")
                return reduced_score
            else:
                # Standard reduction for mild expressions
                reduced_score = base_score * 0.75  # 25% reduction
                logger.info(f"MILD EXPRESSION REDUCTION: {pattern} -> {base_score:.3f} → {reduced_score:.3f}")
                return reduced_score
    
    return base_score

def enhanced_depression_analysis(depression_result, sentiment_scores: Dict, context: Dict, message: str = "") -> Tuple[float, List[str]]:
    """BALANCED SAFETY-FIRST depression model analysis - FIXED VERSION"""
    
    max_crisis_score = 0.0
    detected_categories = []
    
    if not depression_result:
        return max_crisis_score, detected_categories
    
    # Extract predictions
    predictions_to_process = []
    if isinstance(depression_result, list):
        if len(depression_result) > 0 and isinstance(depression_result[0], list):
            predictions_to_process = depression_result[0]
        elif len(depression_result) > 0 and isinstance(depression_result[0], dict):
            predictions_to_process = depression_result
    else:
        if isinstance(depression_result, dict):
            predictions_to_process = [depression_result]
        else:
            return max_crisis_score, detected_categories
    
    # Extract depression scores
    not_depression_score = 0.0
    moderate_score = 0.0
    severe_score = 0.0
    
    for prediction in predictions_to_process:
        if not isinstance(prediction, dict):
            continue
            
        label = str(prediction.get('label', '')).lower().strip()
        score = float(prediction.get('score', 0.0))
        
        if label == 'not depression':
            not_depression_score = score
        elif label == 'moderate':
            moderate_score = score
        elif label == 'severe':
            severe_score = score
        
        detected_categories.append({
            'category': label,
            'raw_score': score,
            'confidence': score,
            'original_label': prediction.get('label', 'unknown'),
            'is_crisis': label in ['moderate', 'severe']
        })
    
    # Calculate base depression score - BALANCED SAFETY-FIRST approach
    total_depression = moderate_score + severe_score
    
    # BALANCED SAFETY-FIRST SCORING: Still cautious but not over-reactive
    if severe_score > 0.15:  # 15% severe signal for HIGH (was 2% - much more reasonable)
        base_score = 0.65 + (severe_score * 2.0)  # More reasonable boost (was 6.0x)
        reason = f"severe_detected ({severe_score:.3f})"
        
    elif moderate_score > 0.70:  # 70% moderate for HIGH (was 60%)
        base_score = 0.60 + (moderate_score * 0.3)  # Less aggressive boost
        reason = f"strong_moderate ({moderate_score:.3f})"
        
    elif moderate_score > 0.50:  # 50% moderate for MEDIUM (was 35% for HIGH!)
        base_score = 0.35 + (moderate_score * 0.4)  # Target MEDIUM range
        reason = f"moderate_signal ({moderate_score:.3f})"
        
    elif moderate_score > 0.30:  # 30% moderate for LOW (was 20% for MEDIUM)
        base_score = 0.15 + (moderate_score * 0.5)  # Target LOW range
        reason = f"mild_moderate ({moderate_score:.3f})"
        
    elif total_depression > 0.20:  # Any depression signal above 20% - LOW range (was 15%)
        base_score = 0.10 + (total_depression * 0.6)  # Lower base score
        reason = f"minor_depression_signal ({total_depression:.3f})"
        
    else:
        # Very low or no depression signal
        base_score = total_depression * 0.5  # Minimal scoring
        reason = f"minimal_depression ({total_depression:.3f})"
    
    # Apply false positive reduction for mild expressions
    if message:
        base_score = apply_false_positive_reduction(message, base_score)
    
    # Context adjustments (existing logic - keep this)
    context_adjustment = 0.0
    adjustment_reasons = []
    
    # Negative sentiment boost (but less aggressive)
    if sentiment_scores and 'negative' in sentiment_scores:
        negative_score = sentiment_scores['negative']
        if negative_score > 0.8:  # Very negative sentiment
            context_adjustment += 0.10  # Reduced from potentially higher values
            adjustment_reasons.append(f"very_negative_sentiment (+0.10)")
        elif negative_score > 0.6:  # Moderately negative
            context_adjustment += 0.05  # Small boost
            adjustment_reasons.append(f"negative_sentiment (+0.05)")
    
    # Social context adjustments (keep these - they're reasonable)
    if context.get('social_isolation_indicators', 0) > 2:
        context_adjustment += 0.05
        adjustment_reasons.append("social_isolation (+0.05)")
    
    if context.get('hopelessness_indicators', 0) > 1:
        context_adjustment += 0.08
        adjustment_reasons.append("hopelessness_indicators (+0.08)")
    
    # Apply context adjustment
    max_crisis_score = base_score + context_adjustment
    max_crisis_score = max(0.0, min(1.0, max_crisis_score))  # Clamp to [0,1]
    
    if adjustment_reasons:
        logger.info(f"Context adjustments: {adjustment_reasons} -> {base_score:.3f} → {max_crisis_score:.3f}")
    
    logger.info(f"BALANCED SAFETY-FIRST analysis: {reason} -> final score: {max_crisis_score:.3f}")
    
    return max_crisis_score, detected_categories

def advanced_idiom_detection(message: str, context: Dict, base_score: float) -> float:
    """Advanced idiom detection with context verification"""
    message_lower = message.lower().strip()
    
    for idiom_rule in ENHANCED_IDIOM_PATTERNS:
        for pattern in idiom_rule['patterns']:
            if re.search(pattern, message_lower, re.IGNORECASE):
                if idiom_rule['required_context'](message):
                    reduced_score = base_score * idiom_rule['reduction_factor']
                    final_score = min(reduced_score, idiom_rule['max_score_after'])
                    
                    logger.info(f"ADVANCED IDIOM REDUCTION: {idiom_rule['name']} -> {base_score:.3f} → {final_score:.3f}")
                    return final_score
    
    return base_score

def enhanced_crisis_level_mapping(crisis_score: float) -> str:
    """BALANCED crisis level mapping with updated thresholds"""
    # Use the updated thresholds from environment
    if crisis_score >= CRISIS_THRESHOLDS.get("high", 0.65):  # Default 0.65 instead of 0.7
        return 'high'      
    elif crisis_score >= CRISIS_THRESHOLDS.get("medium", 0.35):  # Default 0.35 instead of 0.4
        return 'medium'    
    elif crisis_score >= CRISIS_THRESHOLDS.get("low", 0.18):  # Default 0.18 instead of 0.2
        return 'low'       
    else:
        return 'none'

def map_confidence_to_crisis_level(confidence: float) -> str:
    """Map confidence score to crisis level using balanced thresholds"""
    if confidence >= 0.65:  # Reduced from 0.7
        return 'high'
    elif confidence >= 0.35:  # Reduced from 0.5  
        return 'medium'
    elif confidence >= 0.18:  # Reduced from 0.3
        return 'low'
    else:
        return 'none'

# Keep all other existing functions unchanged...
# (determine_crisis_level_from_context, filter_and_rank_phrases, etc.)

def determine_crisis_level_from_context(phrase_data: Dict, confidence: float) -> str:
    """Determine crisis level based on context and confidence"""
    
    context_type = phrase_data.get('context_type', '')
    crisis_boost = phrase_data.get('crisis_boost', 'low')
    
    # Temporal urgency is always concerning
    if context_type == 'temporal_urgency':
        return 'high' if confidence > 0.5 else 'medium'
    
    # Social isolation is medium-high concern
    if context_type == 'social_isolation':
        return 'medium' if confidence > 0.4 else 'low'
    
    # Capability loss varies by confidence
    if context_type == 'capability_loss':
        return 'medium' if confidence > 0.6 else 'low'
    
    # Default mapping with balanced thresholds
    return map_confidence_to_crisis_level(confidence)

def filter_and_rank_phrases(phrases: List[Dict], params: Dict) -> List[Dict]:
    """Filter and rank phrases by relevance and confidence"""
    
    # Remove duplicates
    unique_phrases = {}
    for phrase in phrases:
        text = phrase['text']
        if text not in unique_phrases or phrase['confidence'] > unique_phrases[text]['confidence']:
            unique_phrases[text] = phrase
    
    # Convert back to list
    filtered_phrases = list(unique_phrases.values())
    
    # Sort by confidence descending
    filtered_phrases.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Apply additional filters with adjusted confidence threshold
    min_confidence = params.get('min_confidence', 0.25)  # Reduced from 0.3
    max_results = params.get('max_results', 20)
    
    final_phrases = [
        phrase for phrase in filtered_phrases
        if phrase['confidence'] >= min_confidence
    ][:max_results]
    
    return final_phrases