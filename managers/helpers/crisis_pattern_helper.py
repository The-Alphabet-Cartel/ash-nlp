# ash-nlp/managers/crisis_pattern_helpers.py
"""
Crisis Pattern Helpers for Ash NLP Service
FILE VERSION: v3.1-3e-5.3-helpers-2
LAST MODIFIED: 2025-08-19
PHASE: 3e Sub-step 5.3 - CrisisPatternManager optimization (helper extraction)
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Helper methods extracted from CrisisPatternManager to reduce line count and improve organization.
Contains semantic analysis, pattern extraction, and utility methods.

EXTRACTED METHODS:
- Semantic analysis and classification methods
- Community and context pattern extraction methods  
- Temporal indicator analysis methods
- Safe type conversion utility methods
"""

import logging
import re
import time
from typing import Dict, List, Any, Optional, Tuple
from managers.unified_config_manager import UnifiedConfigManager

logger = logging.getLogger(__name__)

class CrisisPatternHelper:
    """
    Helper class for CrisisPatternManager containing extracted methods for:
    - Semantic pattern analysis and classification
    - Community and context pattern extraction
    - Temporal indicator analysis
    - Safe type conversion utilities
    """
    
    def __init__(self, config_manager: UnifiedConfigManager):
        """
        Initialize helper with configuration manager
        
        Args:
            config_manager: UnifiedConfigManager instance for configuration access
        """
        self.config_manager = config_manager
        logger.debug("CrisisPatternHelper initialized")

    # ========================================================================
    # SAFE TYPE CONVERSION UTILITIES
    # ========================================================================

    def safe_get_int(self, data: dict, key: str, default: int) -> int:
        """Safely get integer value, handling environment variable placeholders"""
        try:
            value = data.get(key, default)
            if isinstance(value, str) and value.startswith('${'):
                logger.warning(f"Environment variable '{value}' not resolved, using default {default}")
                return default
            return int(value)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert '{key}' to int, using default {default}")
            return default

    def safe_get_float(self, data: dict, key: str, default: float) -> float:
        """Safely get float value, handling environment variable placeholders"""
        try:
            value = data.get(key, default)
            if isinstance(value, str) and value.startswith('${'):
                logger.warning(f"Environment variable '{value}' not resolved, using default {default}")
                return default
            return float(value)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert '{key}' to float, using default {default}")
            return default

    def safe_get_bool(self, data: dict, key: str, default: bool) -> bool:
        """Safely get boolean value, handling environment variable placeholders"""
        try:
            value = data.get(key, default)
            if isinstance(value, str) and value.startswith('${'):
                logger.warning(f"Environment variable '{value}' not resolved, using default {default}")
                return default
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert '{key}' to bool, using default {default}")
            return default

    # ========================================================================
    # PATTERN EXTRACTION METHODS
    # ========================================================================

    def extract_community_patterns(self, message: str, patterns_cache: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract community-specific patterns from message - Updated for v3.1 consolidated format"""
        found_patterns = []
        message_lower = message.lower()
        
        try:
            community_vocab = patterns_cache.get('community_vocabulary_patterns', {})
            if not community_vocab:
                return found_patterns
            
            # Handle v3.1 consolidated structure from Phase 3e work
            vocabulary_sections = [
                'identity_vocabulary', 'experience_vocabulary', 'community_support_vocabulary',
                'struggle_vocabulary', 'medical_transition_vocabulary'
            ]
            
            for section_name in vocabulary_sections:
                section_data = community_vocab.get(section_name, {})
                if isinstance(section_data, dict):
                    terms = section_data.get('terms', [])
                    defaults = section_data.get('defaults', {})
                    
                    for term in terms:
                        if isinstance(term, str) and term.lower() in message_lower:
                            found_patterns.append({
                                'pattern_type': section_name,
                                'matched_pattern': term,
                                'crisis_level': defaults.get('crisis_relevance', 'low'),
                                'confidence': defaults.get('weight', 0.5),
                                'weight': defaults.get('boost_factor', 1.0),
                                'phase_3e_extraction': True
                            })
            
            # Check for crisis patterns section (regex patterns)
            crisis_patterns = community_vocab.get('crisis_patterns', {})
            if isinstance(crisis_patterns, dict):
                for pattern_category, pattern_data in crisis_patterns.items():
                    if isinstance(pattern_data, dict) and 'patterns' in pattern_data:
                        defaults = pattern_data.get('defaults', {})
                        for pattern_item in pattern_data['patterns']:
                            if isinstance(pattern_item, dict):
                                pattern_text = pattern_item.get('pattern', '')
                                pattern_type = pattern_item.get('type', 'exact_match')
                                
                                matched = False
                                if pattern_type == 'regex':
                                    try:
                                        if re.search(pattern_text, message, re.IGNORECASE):
                                            matched = True
                                    except re.error:
                                        continue
                                elif pattern_type == 'exact_match':
                                    if pattern_text.lower() in message_lower:
                                        matched = True
                                
                                if matched:
                                    found_patterns.append({
                                        'pattern_type': pattern_category,
                                        'matched_pattern': pattern_text,
                                        'crisis_level': defaults.get('crisis_level', 'medium'),
                                        'confidence': defaults.get('weight', 0.8),
                                        'weight': defaults.get('urgency', 1.0),
                                        'phase_3e_extraction': True
                                    })
            
            # Fallback: Handle legacy structure if still present
            patterns_data = community_vocab.get('patterns', community_vocab.get('vocabulary', {}))
            for pattern_type, pattern_info in patterns_data.items():
                if isinstance(pattern_info, dict):
                    # Handle consolidated structure with terms/keywords
                    terms = pattern_info.get('terms', pattern_info.get('keywords', pattern_info.get('indicators', [])))
                    
                    for term in terms:
                        if isinstance(term, str) and term.lower() in message_lower:
                            found_patterns.append({
                                'pattern_type': pattern_type,
                                'matched_pattern': term,
                                'crisis_level': pattern_info.get('crisis_level', 'low'),
                                'confidence': pattern_info.get('confidence', 0.5),
                                'weight': pattern_info.get('weight', 1.0),
                                'phase_3e_extraction': True
                            })
                        elif isinstance(term, dict):
                            term_text = term.get('term', term.get('word', ''))
                            if term_text and term_text.lower() in message_lower:
                                found_patterns.append({
                                    'pattern_type': pattern_type,
                                    'matched_pattern': term_text,
                                    'crisis_level': term.get('crisis_level', pattern_info.get('crisis_level', 'low')),
                                    'confidence': term.get('confidence', pattern_info.get('confidence', 0.5)),
                                    'weight': term.get('weight', pattern_info.get('weight', 1.0)),
                                    'phase_3e_extraction': True
                                })
            
            return found_patterns
            
        except Exception as e:
            logger.error(f"Error extracting community patterns: {e}")
            return []

    def extract_crisis_context_phrases(self, message: str, patterns_cache: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract crisis context phrases that amplify crisis detection - Updated for Phase 3e consolidation"""
        found_phrases = []
        message_lower = message.lower()
        
        try:
            # Get crisis context patterns from consolidated context patterns
            consolidated = patterns_cache.get('context_patterns', {})
            context_patterns = {}
            
            if consolidated and 'crisis_amplification_patterns' in consolidated:
                context_patterns = {
                    'patterns': consolidated['crisis_amplification_patterns'],
                    'configuration': consolidated.get('configuration', {}),
                    'processing_rules': consolidated.get('processing_rules', {}),
                    '_metadata': consolidated.get('_metadata', {}),
                    'source': 'consolidated_context_patterns'
                }
            else:
                # Fallback to legacy file
                context_patterns = patterns_cache.get('crisis_context_patterns', {})
            
            if not context_patterns or 'patterns' not in context_patterns:
                return found_phrases
            
            patterns = context_patterns['patterns']
            
            for context_type, context_data in patterns.items():
                if not isinstance(context_data, dict):
                    continue
                
                # Handle both consolidated and legacy structures
                indicators = context_data.get('indicators', context_data.get('keywords', context_data.get('terms', [])))
                
                for indicator in indicators:
                    if isinstance(indicator, str) and indicator.lower() in message_lower:
                        found_phrases.append({
                            'phrase_type': context_type,
                            'matched_phrase': indicator,
                            'crisis_level': context_data.get('crisis_level', context_data.get('crisis_boost', 'low')),
                            'confidence': context_data.get('confidence', 0.6),
                            'boost_multiplier': context_data.get('boost_multiplier', context_data.get('boost_factor', 1.0)),
                            'phase_3e_extraction': True
                        })
                    elif isinstance(indicator, dict):
                        phrase = indicator.get('phrase', indicator.get('indicator', ''))
                        if phrase and phrase.lower() in message_lower:
                            found_phrases.append({
                                'phrase_type': context_type,
                                'matched_phrase': phrase,
                                'crisis_level': indicator.get('crisis_level', context_data.get('crisis_level', 'low')),
                                'confidence': indicator.get('confidence', context_data.get('confidence', 0.6)),
                                'boost_multiplier': indicator.get('boost_multiplier', context_data.get('boost_factor', 1.0)),
                                'phase_3e_extraction': True
                            })
            
            return found_phrases
            
        except Exception as e:
            logger.error(f"Error extracting crisis context phrases: {e}")
            return []

    def analyze_temporal_indicators(self, message: str, patterns_cache: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal indicators in message for crisis urgency assessment - Updated for Phase 3e"""
        try:
            temporal_patterns = patterns_cache.get('temporal_indicators_patterns', {})
            if not temporal_patterns or 'patterns' not in temporal_patterns:
                return {'found_indicators': [], 'urgency_score': 0.0}
            
            patterns = temporal_patterns['patterns']
            found_indicators = []
            message_lower = message.lower()
            
            # Handle v3.1 format from Phase 3e work
            for indicator_type, indicator_data in patterns.items():
                if isinstance(indicator_data, dict):
                    defaults = indicator_data.get('defaults', {})
                    # Handle v3.1 structure with indicators array
                    indicators = indicator_data.get('indicators', [])
                    
                    for indicator in indicators:
                        if isinstance(indicator, str) and indicator.lower() in message_lower:
                            found_indicators.append({
                                'indicator_type': indicator_type,
                                'matched_phrase': indicator,
                                'crisis_level': defaults.get('crisis_boost', 'medium'),
                                'confidence': defaults.get('weight', 0.6),
                                'urgency_multiplier': defaults.get('boost_factor', 1.0),
                                'time_sensitivity': defaults.get('urgency', 'normal'),
                                'auto_escalate': defaults.get('auto_escalate', False),
                                'phase_3e_analysis': True
                            })
            
            urgency_score = 0.0
            if found_indicators:
                urgency_values = [ind.get('urgency_multiplier', 1.0) for ind in found_indicators]
                urgency_score = sum(urgency_values) / len(urgency_values)
            
            return {
                'found_indicators': found_indicators,
                'urgency_score': urgency_score,
                'requires_immediate_attention': urgency_score > 1.5 or any(
                    ind.get('time_sensitivity') in ['immediate', 'critical'] or ind.get('auto_escalate', False)
                    for ind in found_indicators
                ),
                'phase_3e_analysis_complete': True
            }
            
        except Exception as e:
            logger.error(f"Error analyzing temporal indicators: {e}")
            return {'found_indicators': [], 'urgency_score': 0.0}


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_crisis_pattern_helper(config_manager: UnifiedConfigManager) -> CrisisPatternHelper:
    """
    Factory function to create CrisisPatternHelper instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        CrisisPatternHelper instance
    """
    return CrisisPatternHelper(config_manager)

__all__ = ['CrisisPatternHelper', 'create_crisis_pattern_helper']

logger.debug("✅ CrisisPatternHelper v3.1-3e-5.3 loaded - Helper methods for CrisisPatternManager")