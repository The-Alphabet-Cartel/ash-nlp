"""
Context Helper Functions - UPDATED for Siebert RoBERTa Integration
Handles context extraction and sentiment analysis with Siebert support
"""

import re
from typing import Dict, List
from config.nlp_settings import POSITIVE_CONTEXT_PATTERNS, IDIOM_PATTERNS, NEGATION_PATTERNS
import os

def process_sentiment_with_flip(sentiment_scores):
    """Process sentiment with optional logic flip for testing - UPDATED for 5-class models"""
    
    # Check if we should flip sentiment logic
    flip_sentiment = os.getenv('NLP_FLIP_SENTIMENT_LOGIC', 'false').lower() == 'true'
    
    if not sentiment_scores:
        return {'negative': 0.5, 'neutral': 0.5, 'positive': 0.0}
    
    if flip_sentiment:
        # Check if this is a 5-class model (tabularisai) or 3-class model
        has_5_classes = any(key in sentiment_scores for key in ['very_negative', 'very_positive'])
        
        if has_5_classes:
            # FLIP for 5-class models: Very Negative <-> Very Positive, Negative <-> Positive
            flipped_scores = {
                'very_negative': sentiment_scores.get('very_positive', 0.0),
                'negative': sentiment_scores.get('positive', 0.0),
                'neutral': sentiment_scores.get('neutral', 0.0),  # Neutral stays neutral
                'positive': sentiment_scores.get('negative', 0.0),
                'very_positive': sentiment_scores.get('very_negative', 0.0)
            }
            print(f"5-CLASS SENTIMENT FLIP ACTIVE: Original {sentiment_scores} -> Flipped {flipped_scores}")
            return flipped_scores
        else:
            # FLIP for 3-class models (original logic)
            flipped_scores = {
                'negative': sentiment_scores.get('positive', 0.0),
                'neutral': sentiment_scores.get('neutral', 0.0),
                'positive': sentiment_scores.get('negative', 0.0)
            }
            print(f"3-CLASS SENTIMENT FLIP ACTIVE: Original {sentiment_scores} -> Flipped {flipped_scores}")
            return flipped_scores
    else:
        # Normal logic
        return sentiment_scores

def extract_context_signals(message: str) -> Dict[str, any]:
    """Extract contextual signals from the message"""
    message_lower = message.lower().strip()
    
    context = {
        'has_positive_words': False,
        'has_humor_context': False,
        'has_work_context': False,
        'has_idiom': False,
        'idiom_type': None,
        'question_mark': '?' in message,
        'exclamation': '!' in message,
        'negation_context': False,
        'temporal_indicators': [],
        'message_lower': message_lower
    }
    
    # Check for positive context
    for category, words in POSITIVE_CONTEXT_PATTERNS.items():
        if any(word in message_lower for word in words):
            context['has_positive_words'] = True
            if category == 'humor':
                context['has_humor_context'] = True
            elif category in ['work_success', 'entertainment']:
                context['has_work_context'] = True
    
    # Check for idioms
    for pattern, idiom_type in IDIOM_PATTERNS:
        if re.search(pattern, message_lower, re.IGNORECASE):
            context['has_idiom'] = True
            context['idiom_type'] = idiom_type
            break
    
    # Check for negation context
    context['negation_context'] = detect_negation_context(message)
    
    # Temporal indicators
    temporal_words = ['today', 'yesterday', 'lately', 'recently', 'always', 'never', 'sometimes']
    context['temporal_indicators'] = [word for word in temporal_words if word in message_lower]
    
    return context

def detect_negation_context(message: str) -> bool:
    """Detect if the message contains negation that might affect crisis interpretation"""
    message_lower = message.lower().strip()
    
    for pattern in NEGATION_PATTERNS:
        if re.search(pattern, message_lower):
            return True
    
    return False

def analyze_sentiment_context(sentiment_result) -> Dict[str, float]:
    """
    UPDATED: Analyze sentiment with Siebert RoBERTa support
    
    Handles multiple sentiment model formats:
    - Siebert RoBERTa: [{'label': 'POSITIVE', 'score': 0.95}] (binary)
    - Cardiff NLP: [{'label': 'LABEL_0', 'score': 0.85}] (ternary) 
    - Human-readable: [{'label': 'negative', 'score': 0.80}] (legacy)
    """
    sentiment_scores = {'negative': 0.0, 'neutral': 0.0, 'positive': 0.0}
    
    if not sentiment_result:
        return sentiment_scores
    
    # Handle different result formats from different sentiment models
    predictions_to_process = []
    
    if isinstance(sentiment_result, list):
        if len(sentiment_result) > 0:
            if isinstance(sentiment_result[0], list):
                # Nested list format: [[{...}, {...}]]
                predictions_to_process = sentiment_result[0]
            elif isinstance(sentiment_result[0], dict):
                # Flat list format: [{...}, {...}]
                predictions_to_process = sentiment_result
    elif isinstance(sentiment_result, dict):
        # Single prediction format: {...}
        predictions_to_process = [sentiment_result]
    
    # Process all predictions and take the max score for each sentiment type
    for item in predictions_to_process:
        if isinstance(item, dict):
            label = item.get('label', '').upper()
            score = float(item.get('score', 0.0))
            
            # ====== NEW: Handle Siebert RoBERTa labels (BINARY) ======
            if label == 'POSITIVE':
                sentiment_scores['positive'] = max(sentiment_scores['positive'], score)
                # Infer neutral for low-confidence positive
                if score < 0.75:
                    inferred_neutral = 1.0 - score
                    sentiment_scores['neutral'] = max(sentiment_scores['neutral'], inferred_neutral)
                    
            elif label == 'NEGATIVE':
                sentiment_scores['negative'] = max(sentiment_scores['negative'], score)
                # Infer neutral for low-confidence negative
                if score < 0.75:
                    inferred_neutral = 1.0 - score
                    sentiment_scores['neutral'] = max(sentiment_scores['neutral'], inferred_neutral)
            
            # ====== EXISTING: Handle Cardiff NLP model labels ======
            elif label == 'LABEL_0':  # Cardiff NLP: negative
                sentiment_scores['negative'] = max(sentiment_scores['negative'], score)
            elif label == 'LABEL_1':  # Cardiff NLP: neutral
                sentiment_scores['neutral'] = max(sentiment_scores['neutral'], score)
            elif label == 'LABEL_2':  # Cardiff NLP: positive
                sentiment_scores['positive'] = max(sentiment_scores['positive'], score)
            
            # ====== EXISTING: Handle human-readable labels (LEGACY) ======
            elif 'negative' in label.lower() or 'sadness' in label.lower() or 'anger' in label.lower():
                sentiment_scores['negative'] = max(sentiment_scores['negative'], score)
            elif 'positive' in label.lower() or 'joy' in label.lower() or 'optimism' in label.lower():
                sentiment_scores['positive'] = max(sentiment_scores['positive'], score)
            elif 'neutral' in label.lower():
                sentiment_scores['neutral'] = max(sentiment_scores['neutral'], score)
    
    return sentiment_scores

def extract_sentiment_scores_from_result(sentiment_result) -> Dict[str, float]:
    """UPDATED: Extract sentiment scores with Siebert RoBERTa support"""
    # Use the same logic as analyze_sentiment_context for consistency
    return analyze_sentiment_context(sentiment_result)

def perform_enhanced_context_analysis(message: str, context_hints: List[str]) -> Dict:
    """Perform enhanced context analysis with community awareness"""
    
    message_lower = message.lower()
    
    context_signals = {
        'temporal_urgency': 0.0,
        'social_isolation': 0.0,
        'identity_crisis': 0.0,
        'family_rejection': 0.0,
        'discrimination_fear': 0.0,
        'support_seeking': 0.0
    }
    
    # Temporal urgency indicators
    urgency_patterns = ['right now', 'tonight', 'today', 'immediately', 'urgent', 'asap', 'can\'t wait']
    context_signals['temporal_urgency'] = min(1.0, sum(0.2 for pattern in urgency_patterns if pattern in message_lower))
    
    # Social isolation indicators
    isolation_patterns = ['alone', 'nobody', 'no one', 'isolated', 'abandoned', 'everyone left']
    context_signals['social_isolation'] = min(1.0, sum(0.15 for pattern in isolation_patterns if pattern in message_lower))
    
    # Identity crisis indicators
    identity_patterns = ['questioning', 'confused about', 'don\'t know who', 'identity crisis', 'am i really']
    context_signals['identity_crisis'] = min(1.0, sum(0.2 for pattern in identity_patterns if pattern in message_lower))
    
    # Family rejection indicators
    family_patterns = ['family rejected', 'parents don\'t accept', 'kicked out', 'disowned', 'family doesn\'t']
    context_signals['family_rejection'] = min(1.0, sum(0.25 for pattern in family_patterns if pattern in message_lower))
    
    # Discrimination fear indicators
    discrimination_patterns = ['scared to come out', 'unsafe', 'discrimination', 'harassment', 'hate crime']
    context_signals['discrimination_fear'] = min(1.0, sum(0.2 for pattern in discrimination_patterns if pattern in message_lower))
    
    # Support seeking indicators (positive signal)
    support_patterns = ['need help', 'looking for support', 'anyone else', 'advice', 'what should i do']
    context_signals['support_seeking'] = min(1.0, sum(0.1 for pattern in support_patterns if pattern in message_lower))
    
    # Apply context hints if provided
    for hint in context_hints:
        hint_lower = hint.lower()
        for signal_name in context_signals.keys():
            if signal_name.replace('_', ' ') in hint_lower:
                context_signals[signal_name] = min(1.0, context_signals[signal_name] + 0.1)
    
    return context_signals

def score_term_in_context(term: str, message: str) -> float:
    """Score how relevant a community term is in the given message context"""
    
    message_lower = message.lower()
    term_lower = term.lower()
    
    if term_lower not in message_lower:
        return 0.0
    
    # Base score for presence
    base_score = 0.5
    
    # Context enhancement patterns
    from config.nlp_settings import CONTEXT_WEIGHTS
    
    crisis_context_words = CONTEXT_WEIGHTS['crisis_context_words']
    positive_context_words = CONTEXT_WEIGHTS['positive_context_words']
    
    # Check for crisis context around the term
    words = message_lower.split()
    term_index = -1
    
    for i, word in enumerate(words):
        if term_lower.startswith(word) or word in term_lower:
            term_index = i
            break
    
    if term_index >= 0:
        # Check surrounding words (±3 positions)
        start = max(0, term_index - 3)
        end = min(len(words), term_index + 4)
        context_words = words[start:end]
        
        # Count crisis vs positive context
        crisis_count = sum(1 for word in context_words if any(crisis_word in word for crisis_word in crisis_context_words))
        positive_count = sum(1 for word in context_words if any(pos_word in word for pos_word in positive_context_words))
        
        # Adjust score based on context
        if crisis_count > positive_count:
            base_score += 0.3  # Crisis context boosts relevance
        elif positive_count > crisis_count:
            base_score -= 0.2  # Positive context reduces crisis relevance
    
    return min(1.0, max(0.0, base_score))