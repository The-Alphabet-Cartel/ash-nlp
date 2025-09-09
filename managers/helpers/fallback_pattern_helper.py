# ash-nlp/managers/helpers/fallback_pattern_helper.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Pattern-Based Fallback Classification Helper for Ash-NLP Service
---
FILE VERSION: v3.1-3e-7-1
LAST MODIFIED: 2025-09-09
PHASE: 3e Step 7 - Model Coordination Refactoring
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Handle pattern-based classification when AI models are unavailable
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FallbackPatternHelper:
    """
    Pattern-Based Fallback Classification Helper
    
    Handles:
    - Pattern-based crisis detection when AI models unavailable
    - Keyword matching and scoring
    - Model-specific pattern definitions
    - Fallback label generation
    """
    
    def __init__(self, config_manager, model_coordination_manager):
        """
        Initialize Fallback Pattern Helper
        
        Args:
            config_manager: UnifiedConfigManager instance
            model_coordination_manager: Parent ModelCoordinationManager instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for FallbackPatternHelper")
        if model_coordination_manager is None:
            raise ValueError("ModelCoordinationManager is required for FallbackPatternHelper")
        
        self.config_manager = config_manager
        self.model_manager = model_coordination_manager
        
        # Load pattern configurations
        self._crisis_keywords = self._load_crisis_keywords()
        self._model_specific_patterns = self._load_model_specific_patterns()
        
        logger.info("FallbackPatternHelper initialized for pattern-based classification")

    def _load_crisis_keywords(self) -> List[str]:
        """Load general crisis detection keywords from configuration"""
        try:
            # Try to get crisis keywords from pattern detection configuration
            pattern_config = self.config_manager.get_config_section('pattern_detection')
            if pattern_config and 'crisis_keywords' in pattern_config:
                keywords = pattern_config['crisis_keywords']
                if isinstance(keywords, list):
                    logger.debug(f"Loaded {len(keywords)} crisis keywords from configuration")
                    return keywords
            
            # Fallback to default crisis keywords
            default_keywords = [
                'suicide', 'suicidal', 'kill myself', 'end it all', 'hopeless', 
                'helpless', 'worthless', 'crisis', 'breakdown', 'panic attack',
                'overwhelmed', 'can\'t cope', 'giving up', 'want to die',
                'self harm', 'cutting', 'hurt myself', 'emergency'
            ]
            
            logger.debug(f"Using default crisis keywords: {len(default_keywords)} keywords")
            return default_keywords
            
        except Exception as e:
            logger.warning(f"Error loading crisis keywords: {e}")
            return ['crisis', 'help', 'emergency', 'suicide', 'hopeless']

    def _load_model_specific_patterns(self) -> Dict[str, List[str]]:
        """Load model-specific pattern keywords"""
        try:
            # Try to get model-specific patterns from configuration
            model_patterns = {}
            
            models = self.model_manager.get_model_definitions()
            for model_type in models.keys():
                try:
                    # Check if there are specific patterns for this model type
                    pattern_key = f'{model_type}_patterns'
                    pattern_config = self.config_manager.get_config_section('pattern_detection', pattern_key)
                    
                    if pattern_config and isinstance(pattern_config, list):
                        model_patterns[model_type] = pattern_config
                        logger.debug(f"Loaded {len(pattern_config)} patterns for {model_type}")
                        continue
                        
                except Exception as e:
                    logger.debug(f"No specific patterns found for {model_type}: {e}")
                
                # Use default patterns based on model type
                model_patterns[model_type] = self._get_default_model_patterns(model_type)
            
            return model_patterns
            
        except Exception as e:
            logger.warning(f"Error loading model-specific patterns: {e}")
            return {}

    def _get_default_model_patterns(self, model_type: str) -> List[str]:
        """Get default patterns for a specific model type"""
        default_patterns = {
            'depression': [
                'suicide', 'suicidal', 'hopeless', 'worthless', 'depression',
                'kill myself', 'end my life', 'want to die', 'can\'t go on',
                'nothing matters', 'empty inside', 'numb', 'broken'
            ],
            'sentiment': [
                'hate', 'angry', 'furious', 'terrible', 'awful', 'worst',
                'disgusting', 'horrible', 'devastating', 'tragic', 'miserable',
                'depressed', 'sad', 'heartbroken', 'disappointed'
            ],
            'emotional_distress': [
                'crisis', 'breakdown', 'panic', 'overwhelmed', 'distress',
                'emergency', 'can\'t cope', 'falling apart', 'losing it',
                'stressed out', 'anxiety', 'anxious', 'scared', 'terrified'
            ]
        }
        
        return default_patterns.get(model_type, [
            'crisis', 'help', 'emergency', 'urgent', 'desperate'
        ])

    async def pattern_fallback_classification(self, text: str, labels: List[str], model_type: str) -> Dict[str, Any]:
        """
        Pattern-based fallback when transformers unavailable
        
        Args:
            text: Text to classify
            labels: Classification labels
            model_type: Model type for context
            
        Returns:
            Pattern-based classification result
        """
        try:
            # Use model-specific patterns if available, otherwise use general crisis keywords
            if model_type in self._model_specific_patterns:
                keywords = self._model_specific_patterns[model_type]
                logger.debug(f"Using {len(keywords)} model-specific patterns for {model_type}")
            else:
                keywords = self._crisis_keywords
                logger.debug(f"Using {len(keywords)} general crisis keywords for {model_type}")
            
            # Perform pattern matching
            score = self._calculate_pattern_score(text, keywords)
            confidence = self._calculate_pattern_confidence(score, len(keywords))
            
            return {
                'score': score,
                'confidence': confidence,
                'model': f'pattern_fallback_{model_type}',
                'model_type': model_type,
                'method': 'pattern_fallback',
                'labels_used': len(labels),
                'keywords_used': len(keywords),
                'transformers_used': False,
                'ensemble_manager': True,
                'pattern_details': {
                    'keywords_matched': self._get_matched_keywords(text, keywords),
                    'total_keywords': len(keywords),
                    'match_ratio': score / max(0.1, len(keywords) * 0.1)
                }
            }
            
        except Exception as e:
            logger.error(f"Pattern fallback failed: {e}")
            return {
                'score': 0.0,
                'confidence': 0.0,
                'error': str(e),
                'model_type': model_type,
                'method': 'pattern_fallback_error'
            }

    def _calculate_pattern_score(self, text: str, keywords: List[str]) -> float:
        """
        Calculate crisis score based on keyword pattern matching
        
        Args:
            text: Text to analyze
            keywords: List of crisis keywords to match
            
        Returns:
            Crisis score between 0.0 and 1.0
        """
        try:
            text_lower = text.lower()
            
            # Count direct keyword matches
            direct_matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            # Calculate base score from direct matches
            base_score = min(0.7, direct_matches * 0.1)
            
            # Boost score for multiple matches (compound crisis indicators)
            if direct_matches >= 3:
                base_score = min(0.85, base_score + 0.15)
            elif direct_matches >= 2:
                base_score = min(0.75, base_score + 0.1)
            
            # Additional scoring for high-severity keywords
            high_severity_keywords = ['suicide', 'suicidal', 'kill myself', 'want to die', 'end my life']
            severe_matches = sum(1 for keyword in high_severity_keywords if keyword in text_lower)
            
            if severe_matches > 0:
                # Significant boost for high-severity matches
                base_score = min(0.95, base_score + (severe_matches * 0.2))
            
            # Cap the final score
            final_score = min(0.95, base_score)
            
            logger.debug(f"Pattern scoring: {direct_matches} matches, {severe_matches} severe matches, score: {final_score:.3f}")
            return final_score
            
        except Exception as e:
            logger.error(f"Pattern score calculation failed: {e}")
            return 0.0

    def _calculate_pattern_confidence(self, score: float, keyword_count: int) -> float:
        """
        Calculate confidence based on pattern matching results
        
        Args:
            score: Calculated crisis score
            keyword_count: Total number of keywords used
            
        Returns:
            Confidence value between 0.0 and 1.0
        """
        try:
            # Base confidence is lower than AI models since patterns are less sophisticated
            base_confidence = min(0.6, score + 0.1)
            
            # Adjust confidence based on keyword coverage
            if keyword_count > 10:
                # More keywords available = higher confidence in results
                base_confidence = min(0.7, base_confidence + 0.1)
            
            # Boost confidence for very high scores (clear crisis indicators)
            if score >= 0.8:
                base_confidence = min(0.75, base_confidence + 0.1)
            
            return base_confidence
            
        except Exception as e:
            logger.error(f"Pattern confidence calculation failed: {e}")
            return 0.3  # Low but non-zero confidence as fallback

    def _get_matched_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """
        Get list of keywords that matched in the text
        
        Args:
            text: Text to analyze
            keywords: List of keywords to check
            
        Returns:
            List of keywords that were found in the text
        """
        try:
            text_lower = text.lower()
            matched = [keyword for keyword in keywords if keyword in text_lower]
            return matched
            
        except Exception as e:
            logger.error(f"Keyword matching failed: {e}")
            return []

    def get_fallback_labels(self, model_type: str) -> List[str]:
        """Get fallback labels for a model type"""
        fallback_labels = {
            'depression': [
                "person expressing suicidal thoughts or plans",
                "person showing severe depression symptoms",
                "person experiencing moderate depression",
                "person feeling emotionally stable"
            ],
            'sentiment': [
                "extreme negative sentiment with crisis indicators",
                "moderate negative sentiment", 
                "neutral emotional expression",
                "positive emotional expression"
            ],
            'emotional_distress': [
                "person in acute psychological crisis",
                "person experiencing severe emotional distress",
                "person showing moderate distress signs",
                "person demonstrating emotional resilience"
            ]
        }
        
        return fallback_labels.get(model_type, [
            "high crisis level detected",
            "moderate crisis level detected",
            "low crisis level detected",
            "no crisis indicators detected"
        ])

    def get_pattern_info(self) -> Dict[str, Any]:
        """Get information about loaded patterns for diagnostics"""
        try:
            return {
                'general_crisis_keywords': len(self._crisis_keywords),
                'model_specific_patterns': {
                    model_type: len(patterns) 
                    for model_type, patterns in self._model_specific_patterns.items()
                },
                'total_patterns_loaded': len(self._crisis_keywords) + sum(
                    len(patterns) for patterns in self._model_specific_patterns.values()
                ),
                'available_model_types': list(self._model_specific_patterns.keys()),
                'pattern_source': 'configuration' if self._model_specific_patterns else 'defaults'
            }
        except Exception as e:
            return {
                'error': str(e),
                'pattern_source': 'unknown'
            }

# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_fallback_pattern_helper(config_manager, model_coordination_manager) -> FallbackPatternHelper:
    """
    Factory function to create FallbackPatternHelper instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        model_coordination_manager: ModelCoordinationManager instance
        
    Returns:
        FallbackPatternHelper instance
    """
    return FallbackPatternHelper(config_manager, model_coordination_manager)
# ============================================================================

__all__ = [
    'FallbackPatternHelper',
    'create_fallback_pattern_helper'
]

logger.info("FallbackPatternHelper v3.1-3e-7-1 loaded - Pattern-based fallback classification functionality")