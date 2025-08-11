# ash-nlp/utils/community_patterns.py
"""
LGBTQIA+ Community Pattern Extraction for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import List, Dict, Optional
from managers.crisis_pattern_manager import CrisisPatternManager

logger = logging.getLogger(__name__)

class CommunityPatternExtractor:
    """
    Community pattern extraction using CrisisPatternManager
    Following v3.1 clean architecture patterns
    """
    
    def __init__(self, crisis_pattern_manager: CrisisPatternManager):
        """
        Initialize CommunityPatternExtractor with CrisisPatternManager dependency injection
        
        Args:
            crisis_pattern_manager: CrisisPatternManager instance for pattern access
        """
        self.crisis_pattern_manager = crisis_pattern_manager
        logger.debug("CommunityPatternExtractor v3.1 initialized with CrisisPatternManager")
    
    def extract_community_patterns(self, message: str) -> List[Dict]:
        """
        Extract LGBTQIA+ community-specific patterns using CrisisPatternManager
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of matched community patterns with metadata
        """
        try:
            return self.crisis_pattern_manager.extract_community_patterns(message)
        except Exception as e:
            logger.error(f"Error extracting community patterns: {e}")
            return []
    
    def extract_crisis_context_phrases(self, message: str) -> List[Dict]:
        """
        Extract phrases with crisis context indicators using CrisisPatternManager
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of matched context phrases with metadata
        """
        try:
            return self.crisis_pattern_manager.extract_crisis_context_phrases(message)
        except Exception as e:
            logger.error(f"Error extracting crisis context phrases: {e}")
            return []
    
    def analyze_temporal_indicators(self, message: str) -> Dict:
        """
        Analyze temporal indicators for crisis urgency assessment
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary with temporal analysis results
        """
        try:
            return self.crisis_pattern_manager.analyze_temporal_indicators(message)
        except Exception as e:
            logger.error(f"Error analyzing temporal indicators: {e}")
            return {
                'found_indicators': [],
                'highest_urgency': 'none',
                'total_boost': 0.0,
                'auto_escalate': False,
                'staff_alert': False,
                'error': str(e)
            }
    
    def apply_context_weights(self, message: str, base_crisis_score: float) -> tuple:
        """
        Apply context weights to modify crisis score
        
        Args:
            message: Message text to analyze
            base_crisis_score: Base crisis score to modify
            
        Returns:
            Tuple of (modified_score, analysis_details)
        """
        try:
            return self.crisis_pattern_manager.apply_context_weights(message, base_crisis_score)
        except Exception as e:
            logger.error(f"Error applying context weights: {e}")
            return base_crisis_score, {'error': str(e)}
    
    def check_enhanced_crisis_patterns(self, message: str) -> Dict:
        """
        Check for enhanced crisis patterns (hopelessness, planning, methods, etc.)
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary with enhanced pattern analysis results
        """
        try:
            return self.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
        except Exception as e:
            logger.error(f"Error checking enhanced crisis patterns: {e}")
            return {
                'matches': [],
                'highest_urgency': 'none',
                'auto_escalate': False,
                'total_weight': 0.0,
                'requires_immediate_attention': False,
                'error': str(e)
            }


# ============================================================================
# LEGACY COMPATIBILITY FUNCTIONS (Phase 3a Migration Support)
# ============================================================================

def extract_community_patterns(message: str, crisis_pattern_manager: Optional[CrisisPatternManager] = None) -> List[Dict]:
    """
    Legacy compatibility function for community pattern extraction
    
    Args:
        message: Message text to analyze
        crisis_pattern_manager: Optional CrisisPatternManager instance
        
    Returns:
        List of matched community patterns
        
    Note:
        This function maintains backward compatibility during Phase 3a migration.
        New code should use CommunityPatternExtractor class directly.
    """
    if crisis_pattern_manager is None:
        logger.warning("extract_community_patterns called without CrisisPatternManager - patterns may be limited")
        return []
    
    extractor = CommunityPatternExtractor(crisis_pattern_manager)
    return extractor.extract_community_patterns(message)

def extract_crisis_context_phrases(message: str, crisis_pattern_manager: Optional[CrisisPatternManager] = None) -> List[Dict]:
    """
    Legacy compatibility function for crisis context phrase extraction
    
    Args:
        message: Message text to analyze
        crisis_pattern_manager: Optional CrisisPatternManager instance
        
    Returns:
        List of matched context phrases
        
    Note:
        This function maintains backward compatibility during Phase 3a migration.
        New code should use CommunityPatternExtractor class directly.
    """
    if crisis_pattern_manager is None:
        logger.warning("extract_crisis_context_phrases called without CrisisPatternManager - patterns may be limited")
        return []
    
    extractor = CommunityPatternExtractor(crisis_pattern_manager)
    return extractor.extract_crisis_context_phrases(message)


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_community_pattern_extractor(crisis_pattern_manager: CrisisPatternManager) -> CommunityPatternExtractor:
    """
    Factory function to create CommunityPatternExtractor instance
    
    Args:
        crisis_pattern_manager: CrisisPatternManager instance for dependency injection
        
    Returns:
        CommunityPatternExtractor instance
    """
    return CommunityPatternExtractor(crisis_pattern_manager)


# Export for clean architecture
__all__ = [
    'CommunityPatternExtractor',
    'create_community_pattern_extractor',
    # Legacy compatibility functions
    'extract_community_patterns',
    'extract_crisis_context_phrases'
]