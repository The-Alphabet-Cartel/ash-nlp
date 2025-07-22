"""
LGBTQIA+ Community Pattern Extraction
Handles community-specific crisis pattern recognition
"""

import re
from typing import List, Dict
from config.nlp_settings import LGBTQIA_PATTERNS, CRISIS_CONTEXTS

def extract_community_patterns(message: str) -> List[Dict]:
    """Extract LGBTQIA+ community-specific patterns"""
    phrases = []
    message_lower = message.lower()
    
    for pattern_name, pattern_group in LGBTQIA_PATTERNS.items():
        for pattern in pattern_group['patterns']:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                phrase = match.group().strip()
                phrases.append({
                    'text': phrase,
                    'type': 'community_pattern',
                    'crisis_level': pattern_group['crisis_level'],
                    'category': pattern_group['category'],
                    'matched_pattern': pattern
                })
    
    return phrases

def extract_crisis_context_phrases(message: str) -> List[Dict]:
    """Extract phrases with crisis context indicators"""
    phrases = []
    message_lower = message.lower()
    words = message_lower.split()
    
    for context_name, context_data in CRISIS_CONTEXTS.items():
        for indicator in context_data['indicators']:
            if indicator in message_lower:
                # Find phrases around the indicator
                indicator_words = indicator.split()
                
                for i, word in enumerate(words):
                    if word == indicator_words[0]:
                        # Check if full indicator matches
                        if ' '.join(words[i:i+len(indicator_words)]) == indicator:
                            # Extract context phrases around the indicator
                            start = max(0, i - 2)
                            end = min(len(words), i + len(indicator_words) + 3)
                            
                            context_phrase = ' '.join(words[start:end])
                            
                            phrases.append({
                                'text': context_phrase,
                                'type': 'crisis_context',
                                'context_type': context_data['context_type'],
                                'crisis_boost': context_data['crisis_boost'],
                                'indicator': indicator
                            })
    
    return phrases