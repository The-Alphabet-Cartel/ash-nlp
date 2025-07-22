"""
Scoring Helper Functions
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

def enhanced_depression_analysis(depression_result, sentiment_scores: Dict, context: Dict) -> Tuple[float, List[str]]:
    """Enhanced depression model analysis with SAFETY-FIRST recalibration"""
    
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
            return max_crisis_score, detected_categories
    elif isinstance(depression_result, dict):
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
    
    # Calculate base depression score - SAFETY FIRST approach
    total_depression = moderate_score + severe_score
    
    # SAFETY-FIRST SCORING: Err on side of caution for potential crises
    if severe_score > 0.02:  # Any severe signal is HIGH
        base_score = 0.70 + (severe_score * 6.0)  # Ensure HIGH threshold
        reason = f"severe_detected ({severe_score:.3f})"
        
    elif moderate_score > 0.60:  # Strong moderate is HIGH
        base_score = 0.65 + (moderate_score * 0.4)  # Ensure HIGH
        reason = f"strong_moderate ({moderate_score:.3f})"
        
    elif moderate_score > 0.35:  # Moderate signal - likely HIGH or high MEDIUM
        base_score = 0.50 + (moderate_score * 0.6)  # Borderline HIGH
        reason = f"moderate_signal ({moderate_score:.3f})"
        
    elif moderate_score > 0.20:  # Mild moderate - MEDIUM range
        base_score = 0.25 + (moderate_score * 0.8)  # MEDIUM range
        reason = f"mild_moderate ({moderate_score:.3f})"
        
    elif total_depression > 0.15:  # Any depression signal - LOW to MEDIUM
        base_score = 0.12 + (total_depression * 0.8)  # LOW range
        reason = f"mild_depression ({total_depression:.3f})"
        
    elif not_depression_score > 0.90:  # Very confident not depression
        base_score = 0.05  # Small residual
        reason = f"confident_not_depression ({not_depression_score:.3f})"
        
    else:  # Weak signals
        base_score = total_depression * 0.6
        reason = f"weak_signals ({total_depression:.3f})"
    
    # CRITICAL PATTERN DETECTION: Patterns that MUST be HIGH
    message_lower = context.get('message_lower', '')
    
    critical_pattern_found = False
    
    for pattern_list, pattern_name in [
        (BURDEN_PATTERNS, "burden_ideation"),
        (HOPELESSNESS_PATTERNS, "severe_hopelessness"),
        (STRUGGLE_PATTERNS, "severe_struggle")
    ]:
        for pattern in pattern_list:
            if pattern in message_lower:
                base_score = max(base_score, 0.70)  # Force HIGH threshold
                reason += f" + {pattern_name}_boost"
                critical_pattern_found = True
                break
        if critical_pattern_found:
            break
    
    # Context-based adjustments (more conservative for safety)
    context_adjustment = 0.0
    adjustment_reasons = []
    
    # Only reduce scores for clearly positive contexts
    if context['has_humor_context'] and base_score < 0.35:  # Don't reduce HIGH scores
        context_adjustment -= 0.15
        adjustment_reasons.append("humor_context")
    
    if context['has_work_context'] and base_score < 0.25:  # Don't reduce MEDIUM+ scores
        context_adjustment -= 0.10
        adjustment_reasons.append("work_success_context")
    
    # Sentiment integration (conservative)
    negative_sentiment = sentiment_scores.get('negative', 0.0)
    positive_sentiment = sentiment_scores.get('positive', 0.0)
    
    if negative_sentiment > 0.80 and base_score > 0.15:
        context_adjustment += 0.05  # Small boost for negative sentiment
        adjustment_reasons.append("high_negative_sentiment")
    
    if positive_sentiment > 0.80 and base_score < 0.20:  # Only reduce low scores
        context_adjustment -= 0.10
        adjustment_reasons.append("high_positive_sentiment")
    
    # Apply adjustments
    max_crisis_score = base_score + context_adjustment
    max_crisis_score = max(0.0, min(1.0, max_crisis_score))
    
    if adjustment_reasons:
        logger.info(f"Context adjustments: {adjustment_reasons} -> {base_score:.3f} → {max_crisis_score:.3f}")
    
    logger.info(f"SAFETY-FIRST analysis: {reason} -> final score: {max_crisis_score:.3f}")
    
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
    """SAFETY-FIRST crisis level mapping"""
    if crisis_score >= CRISIS_THRESHOLDS["high"]:
        return 'high'      
    elif crisis_score >= CRISIS_THRESHOLDS["medium"]:
        return 'medium'    
    elif crisis_score >= CRISIS_THRESHOLDS["low"]:
        return 'low'       
    else:
        return 'none'

async def score_phrases_with_models(model_manager, phrases: List[Dict], original_message: str) -> List[Dict]:
    """Score extracted phrases using depression + sentiment models"""
    
    scored_phrases = []
    
    for phrase_data in phrases:
        phrase_text = phrase_data['text']
        
        try:
            # Score with depression model
            depression_result = model_manager.analyze_with_depression_model(phrase_text)
            depression_score = extract_depression_score(depression_result)
            
            # Score with sentiment model
            sentiment_result = model_manager.analyze_with_sentiment_model(phrase_text)
            from utils.context_helpers import analyze_sentiment_context
            sentiment_scores = analyze_sentiment_context(sentiment_result)
            
            # Calculate combined confidence
            base_confidence = depression_score
            
            # Adjust based on phrase type
            if phrase_data.get('type') == 'community_pattern':
                # Community patterns get a boost since they're specifically relevant
                base_confidence = max(base_confidence, 0.6)
                crisis_level = phrase_data.get('crisis_level', 'medium')
            elif phrase_data.get('type') == 'crisis_context':
                # Crisis context phrases get boost based on urgency
                boost = {'high': 0.3, 'medium': 0.2, 'low': 0.1}.get(phrase_data.get('crisis_boost', 'low'), 0.1)
                base_confidence += boost
                crisis_level = determine_crisis_level_from_context(phrase_data, base_confidence)
            else:
                # Regular n-grams scored purely by model
                crisis_level = map_confidence_to_crisis_level(base_confidence)
            
            # Sentiment adjustment
            negative_sentiment = sentiment_scores.get('negative', 0.0)
            if negative_sentiment > 0.7:
                base_confidence += 0.1
            
            # Final confidence clamping
            final_confidence = max(0.0, min(1.0, base_confidence))
            
            # Only include phrases above threshold
            if final_confidence > 0.3:
                scored_phrases.append({
                    'text': phrase_text,
                    'crisis_level': crisis_level,
                    'confidence': final_confidence,
                    'reasoning': f"Depression: {depression_score:.2f}, Sentiment: {sentiment_scores.get('negative', 0):.2f}",
                    'metadata': {
                        'original_type': phrase_data.get('type', 'unknown'),
                        'depression_score': depression_score,
                        'sentiment_scores': sentiment_scores,
                        'source_context': phrase_data.get('category', 'general'),
                        'original_message_preview': original_message[:50]
                    }
                })
                
        except Exception as e:
            logger.error(f"Error scoring phrase '{phrase_text}': {e}")
            continue
    
    return scored_phrases

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
    
    # Default mapping
    return map_confidence_to_crisis_level(confidence)

def map_confidence_to_crisis_level(confidence: float) -> str:
    """Map confidence score to crisis level"""
    if confidence >= 0.7:
        return 'high'
    elif confidence >= 0.5:
        return 'medium'
    elif confidence >= 0.3:
        return 'low'
    else:
        return 'none'

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
    
    # Apply additional filters
    min_confidence = params.get('min_confidence', 0.3)
    max_results = params.get('max_results', 20)
    
    final_phrases = [
        phrase for phrase in filtered_phrases
        if phrase['confidence'] >= min_confidence
    ][:max_results]
    
    return final_phrases