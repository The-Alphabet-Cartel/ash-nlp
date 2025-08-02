"""
Phrase Extractor - Extract crisis keywords using model scoring
Uses your depression + sentiment models to score potential crisis phrases
"""

import logging
import time
from typing import Dict, List
from utils.community_patterns import extract_community_patterns, extract_crisis_context_phrases
from utils.scoring_helpers import extract_depression_score, score_phrases_with_models, filter_and_rank_phrases
from managers.settings_manager import DEFAULT_PARAMS

logger = logging.getLogger(__name__)

class PhraseExtractor:
    """Extract potential crisis keywords/phrases using your existing models"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    async def extract_phrases(self, message: str, user_id: str = "unknown", 
                            channel_id: str = "unknown", parameters: Dict = None) -> Dict:
        """
        Extract potential crisis keywords/phrases using your existing models
        """
        
        if not parameters:
            parameters = DEFAULT_PARAMS['phrase_extraction']
        
        start_time = time.time()
        
        try:
            min_length = parameters.get('min_phrase_length', 2)
            max_length = parameters.get('max_phrase_length', 6)
            crisis_focus = parameters.get('crisis_focus', True)
            community_specific = parameters.get('community_specific', True)
            
            phrases = []
            
            # Method 1: N-gram extraction with model scoring
            ngram_phrases = self._extract_scored_ngrams(message, min_length, max_length)
            phrases.extend(ngram_phrases)
            
            # Method 2: LGBTQIA+ community-specific pattern extraction
            if community_specific:
                community_phrases = extract_community_patterns(message)
                phrases.extend(community_phrases)
            
            # Method 3: Crisis-context phrase extraction
            if crisis_focus:
                crisis_phrases = extract_crisis_context_phrases(message)
                phrases.extend(crisis_phrases)
            
            # Method 4: Score phrases with your models
            model_scored_phrases = await score_phrases_with_models(
                self.model_manager, phrases, message
            )
            
            # Filter and rank phrases
            final_phrases = filter_and_rank_phrases(model_scored_phrases, parameters)
            
            processing_time = (time.time() - start_time) * 1000
            
            logger.info(f"Phrase extraction: {len(final_phrases)} phrases from '{message[:30]}...' ({processing_time:.1f}ms)")
            
            return {
                'phrases': final_phrases[:20],  # Top 20 candidates
                'total_extracted': len(phrases),
                'total_scored': len(model_scored_phrases),
                'processing_time_ms': processing_time,
                'model_info': 'depression+sentiment+community_patterns',
                'extraction_methods': ['ngrams', 'community_patterns', 'crisis_context', 'model_scoring']
            }
            
        except Exception as e:
            logger.error(f"Error in phrase extraction: {e}")
            raise
    
    def _extract_scored_ngrams(self, message: str, min_length: int, max_length: int) -> List[Dict]:
        """Extract n-grams and score them for crisis relevance"""
        
        phrases = []
        words = message.lower().split()
        
        # Extract n-grams of various lengths
        for i in range(len(words)):
            for phrase_len in range(min_length, min(max_length + 1, len(words) - i + 1)):
                phrase = ' '.join(words[i:i + phrase_len])
                
                # Skip very common phrases
                if phrase in ['the', 'and', 'but', 'for', 'you are', 'i am', 'it is', 'to be']:
                    continue
                
                # Skip if too short or all stop words
                if len(phrase) < 4:
                    continue
                
                phrases.append({
                    'text': phrase,
                    'type': 'ngram',
                    'source_position': i,
                    'length': phrase_len
                })
        
        return phrases