"""
Context Helpers for Ash NLP Service v3.1 - Phase 3a Updated
Enhanced context analysis with crisis pattern integration

Phase 3a: Updated to work without hardcoded pattern imports
All pattern analysis now handled by CrisisPatternManager
"""

import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# Basic negation patterns - these are simple enough to keep here
BASIC_NEGATION_PATTERNS = [
    r'\bnot\s+(?:really\s+)?(?:feeling|thinking|wanting)',
    r'\b(?:don\'t|won\'t|can\'t)\s+(?:want|feel|think)',
    r'\bnever\s+(?:thought|felt|wanted)',
    r'\bno\s+(?:thoughts|feelings|desire)',
    r'\bnot\s+(?:suicidal|depressed|hopeless)'
]

def extract_context_signals(message: str) -> Dict[str, Any]:
    """
    Extract contextual signals from message - Updated for Phase 3a
    
    Args:
        message: Message text to analyze
        
    Returns:
        Dictionary with basic context signals
        
    Note:
        Advanced pattern analysis now handled by CrisisPatternManager.
        This function provides basic context signals only.
    """
    message_lower = message.lower().strip()
    
    # Basic context signals
    context = {
        'message_length': len(message),
        'word_count': len(message.split()),
        'has_question_mark': '?' in message,
        'has_exclamation': '!' in message,
        'has_capitalization': any(c.isupper() for c in message),
        'negation_context': detect_negation_context(message),
        'temporal_indicators': extract_basic_temporal_indicators(message_lower),
        'message_lower': message_lower,
        'social_isolation_indicators': count_social_isolation_indicators(message_lower),
        'hopelessness_indicators': count_hopelessness_indicators(message_lower),
        # Placeholder flags - actual pattern analysis done by CrisisPatternManager
        'requires_pattern_analysis': True,
        'pattern_manager_needed': True
    }
    
    return context

def detect_negation_context(message: str) -> bool:
    """Detect if the message contains negation that might affect crisis interpretation"""
    message_lower = message.lower().strip()
    
    for pattern in BASIC_NEGATION_PATTERNS:
        if re.search(pattern, message_lower):
            return True
    
    return False

def extract_basic_temporal_indicators(message_lower: str) -> List[str]:
    """Extract basic temporal indicators from message"""
    basic_temporal_words = [
        'today', 'yesterday', 'tomorrow', 'lately', 'recently', 'always', 
        'never', 'sometimes', 'right now', 'immediately', 'urgent', 'tonight'
    ]
    
    return [word for word in basic_temporal_words if word in message_lower]

def count_social_isolation_indicators(message_lower: str) -> int:
    """Count basic social isolation indicators"""
    isolation_words = [
        'alone', 'lonely', 'isolated', 'nobody', 'no one', 'abandoned', 
        'by myself', 'on my own', 'no friends', 'no family'
    ]
    
    return sum(1 for word in isolation_words if word in message_lower)

def count_hopelessness_indicators(message_lower: str) -> int:
    """Count basic hopelessness indicators"""
    hopelessness_words = [
        'hopeless', 'pointless', 'meaningless', 'worthless', 'useless',
        'no point', 'no hope', 'give up', 'giving up', 'lost cause'
    ]
    
    return sum(1 for word in hopelessness_words if word in message_lower)

def analyze_sentiment_context(sentiment_result) -> Dict[str, float]:
    """
    UPDATED: Analyze sentiment with Siebert RoBERTa support
    
    Handles multiple sentiment model formats:
    - Siebert RoBERTa: [{'label': 'POSITIVE', 'score': 0.95}] (binary)
    - Cardiff NLP: [{'label': 'LABEL_0', 'score': 0.85}] (ternary) 
    - Human-readable: [{'label': 'negative', 'score': 0.80}] (legacy)
    """
    
    if not sentiment_result or not isinstance(sentiment_result, list):
        logger.warning("Invalid or empty sentiment result")
        return {}
    
    sentiment_scores = {}
    
    try:
        for result in sentiment_result:
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
            else:
                # Handle lowercase or other formats
                label_lower = label.lower()
                if label_lower in ['positive', 'negative', 'neutral']:
                    sentiment_scores[label_lower] = score
        
        logger.debug(f"Processed sentiment scores: {sentiment_scores}")
        return sentiment_scores
        
    except Exception as e:
        logger.error(f"Error processing sentiment result: {e}")
        return {}

def process_sentiment_with_flip(sentiment_scores: Dict[str, float], flip_threshold: float = 0.60) -> Dict[str, float]:
    """
    Process sentiment scores with context-aware flipping for crisis detection
    
    Args:
        sentiment_scores: Dictionary of sentiment scores
        flip_threshold: Threshold for flipping positive to negative in crisis context
        
    Returns:
        Processed sentiment scores
    """
    
    if not sentiment_scores:
        return sentiment_scores
    
    processed_scores = sentiment_scores.copy()
    
    # Context-aware sentiment flipping for crisis detection
    # In mental health contexts, "positive" sentiment might actually indicate crisis
    # Example: "I'm so excited to finally end this pain"
    
    positive_score = sentiment_scores.get('positive', 0.0)
    negative_score = sentiment_scores.get('negative', 0.0)
    
    # If positive sentiment is very high but in a potentially crisis context,
    # this might indicate euphoria before a crisis decision
    if positive_score > flip_threshold and negative_score < 0.3:
        logger.debug(f"High positive sentiment detected ({positive_score:.3f}) - potential crisis euphoria")
        processed_scores['crisis_euphoria_detected'] = positive_score
    
    return processed_scores

def perform_enhanced_context_analysis(message: str, crisis_pattern_manager=None) -> Dict[str, Any]:
    """
    Perform enhanced context analysis using CrisisPatternManager if available
    
    Args:
        message: Message text to analyze
        crisis_pattern_manager: Optional CrisisPatternManager for advanced analysis
        
    Returns:
        Enhanced context analysis results
    """
    
    # Start with basic context signals
    context = extract_context_signals(message)
    
    if crisis_pattern_manager:
        try:
            # Get enhanced pattern analysis from CrisisPatternManager
            context_patterns = crisis_pattern_manager.get_crisis_context_patterns()
            positive_patterns = crisis_pattern_manager.get_positive_context_patterns()
            temporal_analysis = crisis_pattern_manager.analyze_temporal_indicators(message)
            
            # Merge advanced analysis into context
            context.update({
                'crisis_context_available': True,
                'temporal_analysis': temporal_analysis,
                'pattern_manager_status': 'available'
            })
            
            logger.debug("Enhanced context analysis completed with CrisisPatternManager")
            
        except Exception as e:
            logger.error(f"Error in enhanced context analysis: {e}")
            context.update({
                'crisis_context_available': False,
                'pattern_manager_status': 'error',
                'pattern_manager_error': str(e)
            })
    else:
        context.update({
            'crisis_context_available': False,
            'pattern_manager_status': 'not_available'
        })
        logger.debug("Basic context analysis only - CrisisPatternManager not available")
    
    return context

def score_term_in_context(term: str, message: str, context_window: int = 3) -> Dict[str, Any]:
    """
    Score a term's relevance in message context
    
    Args:
        term: Term to score
        message: Full message text
        context_window: Number of words around term to consider
        
    Returns:
        Dictionary with term scoring results
    """
    
    message_lower = message.lower()
    term_lower = term.lower()
    
    if term_lower not in message_lower:
        return {
            'term': term,
            'found': False,
            'relevance_score': 0.0,
            'context_words': []
        }
    
    words = message_lower.split()
    term_positions = []
    
    # Find all positions of the term
    for i, word in enumerate(words):
        if term_lower in word:
            term_positions.append(i)
    
    context_words = []
    for pos in term_positions:
        start = max(0, pos - context_window)
        end = min(len(words), pos + context_window + 1)
        context_words.extend(words[start:end])
    
    # Remove duplicates while preserving order
    context_words = list(dict.fromkeys(context_words))
    
    # Basic relevance scoring based on context
    crisis_indicators = ['crisis', 'help', 'struggling', 'difficult', 'hard', 'scared', 'worried']
    positive_indicators = ['good', 'great', 'happy', 'love', 'amazing', 'wonderful']
    
    crisis_score = sum(1 for word in context_words if word in crisis_indicators)
    positive_score = sum(1 for word in context_words if word in positive_indicators)
    
    relevance_score = (crisis_score * 0.7 + len(context_words) * 0.1) / (positive_score * 0.5 + 1)
    relevance_score = min(1.0, max(0.0, relevance_score))
    
    return {
        'term': term,
        'found': True,
        'positions': term_positions,
        'relevance_score': relevance_score,
        'context_words': context_words,
        'crisis_indicators': crisis_score,
        'positive_indicators': positive_score
    }

# Export for clean architecture
__all__ = [
    'extract_context_signals',
    'detect_negation_context', 
    'analyze_sentiment_context',
    'process_sentiment_with_flip',
    'perform_enhanced_context_analysis',
    'score_term_in_context'
]