# ash-nlp/managers/crisis_pattern_manager.py
"""
Crisis Pattern Manager for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from managers.unified_config_manager import UnifiedConfigManager

logger = logging.getLogger(__name__)

class CrisisPatternManager:
    """
    Manages crisis pattern configurations with JSON defaults and ENV overrides
    Following v3.1 clean architecture patterns
    
    STEP 9.8: Updated to use UnifiedConfigManager instead of legacy ConfigManager
    """
    
    def __init__(self, config_manager: UnifiedConfigManager):
        """
        Initialize CrisisPatternManager with UnifiedConfigManager dependency injection
        
        Args:
            config_manager: UnifiedConfigManager instance for loading JSON configurations
        """
        self.config_manager = config_manager
        self._patterns_cache = {}
        self._compiled_regex_cache = {}
        
        logger.info("CrisisPatternManager v3.1 Step 9.8 initializing...")
        self._load_all_patterns()
        logger.info(f"CrisisPatternManager initialized with {len(self._patterns_cache)} pattern sets")
    
    def _load_all_patterns(self) -> None:
        """Load all crisis pattern configurations"""
        pattern_files = [
            'crisis_context_patterns',
            'positive_context_patterns', 
            'temporal_indicators_patterns',
            'community_vocabulary_patterns',
            'context_weights_patterns',
            'enhanced_crisis_patterns',
            'crisis_idiom_patterns',
            'crisis_burden_patterns',
            'crisis_lgbtqia_patterns'
        ]
        
        for pattern_type in pattern_files:
            try:
                patterns = self.config_manager.get_crisis_patterns(pattern_type)
                if patterns:
                    self._patterns_cache[pattern_type] = patterns
                    logger.debug(f"Loaded {pattern_type}: {len(patterns.get('patterns', {}))} pattern groups")
                else:
                    logger.warning(f"No patterns found for {pattern_type}")
            except Exception as e:
                logger.error(f"Failed to load {pattern_type}: {e}")
                self._patterns_cache[pattern_type] = {}
    
    def get_crisis_patterns(self) -> List[Dict[str, Any]]:
        """
        Get all crisis patterns for backward compatibility with tests
        
        Returns:
            List of all crisis patterns from all loaded pattern sets
        """
        all_patterns = []
        
        try:
            # Aggregate patterns from all loaded pattern sets
            for pattern_type, pattern_data in self._patterns_cache.items():
                if isinstance(pattern_data, dict) and 'patterns' in pattern_data:
                    patterns_section = pattern_data['patterns']
                    
                    # Handle different pattern structures
                    if isinstance(patterns_section, dict):
                        # Flatten nested pattern groups
                        for group_name, group_patterns in patterns_section.items():
                            if isinstance(group_patterns, list):
                                for pattern in group_patterns:
                                    if isinstance(pattern, dict):
                                        # Add metadata about source
                                        pattern_with_meta = pattern.copy()
                                        pattern_with_meta['source_type'] = pattern_type
                                        pattern_with_meta['source_group'] = group_name
                                        all_patterns.append(pattern_with_meta)
                                    elif isinstance(pattern, str):
                                        # Convert string patterns to dict format
                                        all_patterns.append({
                                            'pattern': pattern,
                                            'type': 'regex',
                                            'source_type': pattern_type,
                                            'source_group': group_name,
                                            'weight': 1.0
                                        })
                    elif isinstance(patterns_section, list):
                        # Direct list of patterns
                        for pattern in patterns_section:
                            if isinstance(pattern, dict):
                                pattern_with_meta = pattern.copy()
                                pattern_with_meta['source_type'] = pattern_type
                                all_patterns.append(pattern_with_meta)
                            elif isinstance(pattern, str):
                                all_patterns.append({
                                    'pattern': pattern,
                                    'type': 'regex',
                                    'source_type': pattern_type,
                                    'weight': 1.0
                                })
            
            logger.debug(f"✅ Aggregated {len(all_patterns)} crisis patterns from {len(self._patterns_cache)} pattern sets")
            return all_patterns
            
        except Exception as e:
            logger.error(f"❌ Error aggregating crisis patterns: {e}")
            return []

    def get_crisis_context_patterns(self) -> Dict[str, Any]:
        """Get crisis context patterns that amplify crisis detection"""
        return self._patterns_cache.get('crisis_context_patterns', {})
    
    def get_positive_context_patterns(self) -> Dict[str, Any]:
        """Get positive context patterns that reduce false positives"""
        return self._patterns_cache.get('positive_context_patterns', {})
    
    def get_temporal_indicators(self) -> Dict[str, Any]:
        """Get temporal indicator patterns for time-based crisis modification"""
        return self._patterns_cache.get('temporal_indicators_patterns', {})
    
    def get_community_vocabulary(self) -> Dict[str, Any]:
        """Get community-specific vocabulary patterns"""
        return self._patterns_cache.get('community_vocabulary_patterns', {})
    
    def get_context_weights(self) -> Dict[str, Any]:
        """Get context weight multipliers for pattern matching"""
        return self._patterns_cache.get('context_weights_patterns', {})
    
    def get_enhanced_patterns(self) -> Dict[str, Any]:
        """Get enhanced crisis patterns with advanced matching"""
        return self._patterns_cache.get('enhanced_crisis_patterns', {})
    
    def get_idiom_patterns(self) -> Dict[str, Any]:
        """Get idiom-based crisis patterns"""
        return self._patterns_cache.get('crisis_idiom_patterns', {})
    
    def get_burden_patterns(self) -> Dict[str, Any]:
        """Get burden and stress-related patterns"""
        return self._patterns_cache.get('crisis_burden_patterns', {})
    
    def get_lgbtqia_patterns(self) -> Dict[str, Any]:
        """Get LGBTQIA+ community specific patterns"""
        return self._patterns_cache.get('crisis_lgbtqia_patterns', {})

    def extract_community_patterns(self, message: str) -> List[Dict[str, Any]]:
        """
        Extract community-specific patterns from message
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of matched community patterns with metadata
        """
        found_patterns = []
        message_lower = message.lower()
        
        try:
            community_vocab = self.get_community_vocabulary()
            if not community_vocab or 'patterns' not in community_vocab:
                return found_patterns
            
            patterns = community_vocab['patterns']
            
            for pattern_type, pattern_list in patterns.items():
                if isinstance(pattern_list, list):
                    for pattern_item in pattern_list:
                        if isinstance(pattern_item, dict):
                            pattern = pattern_item.get('pattern', '')
                            if pattern and pattern.lower() in message_lower:
                                found_patterns.append({
                                    'pattern_type': pattern_type,
                                    'matched_pattern': pattern,
                                    'crisis_level': pattern_item.get('crisis_level', 'low'),
                                    'confidence': pattern_item.get('confidence', 0.5),
                                    'weight': pattern_item.get('weight', 1.0)
                                })
            
            return found_patterns
            
        except Exception as e:
            logger.error(f"Error extracting community patterns: {e}")
            return []

    def extract_crisis_context_phrases(self, message: str) -> List[Dict[str, Any]]:
        """
        Extract crisis context phrases that amplify crisis detection
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of matched context phrases with crisis amplification data
        """
        found_phrases = []
        message_lower = message.lower()
        
        try:
            context_patterns = self.get_crisis_context_patterns()
            if not context_patterns or 'patterns' not in context_patterns:
                return found_phrases
            
            patterns = context_patterns['patterns']
            
            for context_type, context_data in patterns.items():
                # FIXED: Skip non-dictionary values (like configuration floats)
                if not isinstance(context_data, dict):
                    logger.debug(f"⚠️ Skipping non-dict context data: {context_type} ({type(context_data).__name__})")
                    continue
                
                indicators = context_data.get('indicators', [])
                for indicator in indicators:
                    if isinstance(indicator, dict):
                        phrase = indicator.get('phrase', '')
                        if phrase and phrase.lower() in message_lower:
                            found_phrases.append({
                                'phrase_type': context_type,
                                'matched_phrase': phrase,
                                'crisis_level': indicator.get('crisis_level', 'low'),
                                'confidence': indicator.get('confidence', 0.6),
                                'boost_multiplier': indicator.get('boost_multiplier', 1.0)
                            })
            
            return found_phrases
            
        except Exception as e:
            logger.error(f"Error extracting crisis context phrases: {e}")
            return []

    def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict[str, Any]:
        """
        Comprehensive message analysis using all available crisis pattern methods
        
        Args:
            message: Message text to analyze
            user_id: User ID (for context)
            channel_id: Channel ID (for context)
            
        Returns:
            Dictionary containing comprehensive pattern analysis results
        """
        try:
            analysis_result = {
                'patterns_triggered': [],
                'analysis_available': True,
                'error': None,
                'details': {}
            }
            
            # 1. Extract community patterns
            try:
                community_patterns = self.extract_community_patterns(message)
                if community_patterns:
                    for pattern in community_patterns:
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"community_{pattern.get('pattern_type', 'unknown')}",
                            'pattern_type': 'community',
                            'crisis_level': pattern.get('crisis_level', 'low'),
                            'confidence': pattern.get('confidence', 0.5),
                            'details': pattern
                        })
                analysis_result['details']['community_patterns'] = community_patterns
            except Exception as e:
                logger.warning(f"Community patterns analysis failed: {e}")
                analysis_result['details']['community_patterns'] = []
            
            # 2. Extract crisis context phrases
            try:
                context_phrases = self.extract_crisis_context_phrases(message)
                if context_phrases:
                    for phrase in context_phrases:
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"context_{phrase.get('phrase_type', 'unknown')}",
                            'pattern_type': 'context_phrase',
                            'crisis_level': phrase.get('crisis_level', 'low'),
                            'confidence': phrase.get('confidence', 0.5),
                            'details': phrase
                        })
                analysis_result['details']['context_phrases'] = context_phrases
            except Exception as e:
                logger.warning(f"Context phrases analysis failed: {e}")
                analysis_result['details']['context_phrases'] = []
            
            # 3. Analyze temporal indicators
            try:
                temporal_analysis = self.analyze_temporal_indicators(message)
                if temporal_analysis and temporal_analysis.get('found_indicators'):
                    for indicator in temporal_analysis.get('found_indicators', []):
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"temporal_{indicator.get('indicator_type', 'unknown')}",
                            'pattern_type': 'temporal',
                            'crisis_level': indicator.get('crisis_level', 'medium'),
                            'confidence': indicator.get('confidence', 0.6),
                            'details': indicator
                        })
                analysis_result['details']['temporal_indicators'] = temporal_analysis
            except Exception as e:
                logger.warning(f"Temporal indicators analysis failed: {e}")
                analysis_result['details']['temporal_indicators'] = {}
            
            # 4. Analyze enhanced patterns
            try:
                enhanced_analysis = self.analyze_enhanced_patterns(message)
                if enhanced_analysis and enhanced_analysis.get('patterns_found'):
                    for pattern in enhanced_analysis.get('patterns_found', []):
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"enhanced_{pattern.get('pattern_name', 'unknown')}",
                            'pattern_type': 'enhanced',
                            'crisis_level': pattern.get('crisis_level', 'medium'),
                            'confidence': pattern.get('confidence', 0.7),
                            'details': pattern
                        })
                analysis_result['details']['enhanced_patterns'] = enhanced_analysis
            except Exception as e:
                logger.warning(f"Enhanced patterns analysis failed: {e}")
                analysis_result['details']['enhanced_patterns'] = {}
            
            # 5. Calculate summary statistics
            pattern_count = len(analysis_result['patterns_triggered'])
            crisis_levels = [p.get('crisis_level', 'low') for p in analysis_result['patterns_triggered']]
            
            # Determine highest crisis level
            level_priority = {'high': 3, 'medium': 2, 'low': 1}
            highest_level = 'none'
            if crisis_levels:
                highest_level = max(crisis_levels, key=lambda x: level_priority.get(x, 0))
            
            analysis_result.update({
                'summary': {
                    'total_patterns': pattern_count,
                    'highest_crisis_level': highest_level,
                    'pattern_types': list(set([p.get('pattern_type', 'unknown') for p in analysis_result['patterns_triggered']])),
                    'requires_attention': highest_level in ['high', 'medium'] or pattern_count >= 3
                },
                'metadata': {
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'analysis_timestamp': time.time(),
                    'methods_used': ['community_patterns', 'context_phrases', 'temporal_indicators', 'enhanced_patterns']
                }
            })
            
            logger.debug(f"✅ Crisis pattern analysis complete: {pattern_count} patterns found, highest level: {highest_level}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Crisis pattern analysis failed: {e}")
            return {
                'patterns_triggered': [],
                'analysis_available': False,
                'error': str(e),
                'details': {},
                'summary': {
                    'total_patterns': 0,
                    'highest_crisis_level': 'none',
                    'pattern_types': [],
                    'requires_attention': False
                },
                'metadata': {
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'analysis_timestamp': time.time(),
                    'error': str(e)
                }
            }

    def analyze_temporal_indicators(self, message: str) -> Dict[str, Any]:
        """
        Analyze temporal indicators in message for crisis urgency assessment
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary containing temporal indicator analysis results
        """
        try:
            temporal_patterns = self.get_temporal_indicators()
            if not temporal_patterns or 'patterns' not in temporal_patterns:
                return {'found_indicators': [], 'urgency_score': 0.0}
            
            patterns = temporal_patterns['patterns']
            found_indicators = []
            message_lower = message.lower()
            
            for indicator_type, indicator_data in patterns.items():
                if isinstance(indicator_data, dict) and 'indicators' in indicator_data:
                    for indicator in indicator_data['indicators']:
                        if isinstance(indicator, dict):
                            phrase = indicator.get('phrase', '')
                            if phrase and phrase.lower() in message_lower:
                                found_indicators.append({
                                    'indicator_type': indicator_type,
                                    'matched_phrase': phrase,
                                    'crisis_level': indicator.get('crisis_level', 'medium'),
                                    'confidence': indicator.get('confidence', 0.6),
                                    'urgency_multiplier': indicator.get('urgency_multiplier', 1.0),
                                    'time_sensitivity': indicator.get('time_sensitivity', 'normal')
                                })
            
            # Calculate overall urgency score
            urgency_score = 0.0
            if found_indicators:
                urgency_values = [ind.get('urgency_multiplier', 1.0) for ind in found_indicators]
                urgency_score = sum(urgency_values) / len(urgency_values)
            
            return {
                'found_indicators': found_indicators,
                'urgency_score': urgency_score,
                'requires_immediate_attention': urgency_score > 1.5 or any(
                    ind.get('time_sensitivity') == 'immediate' for ind in found_indicators
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing temporal indicators: {e}")
            return {'found_indicators': [], 'urgency_score': 0.0}

    def analyze_enhanced_patterns(self, message: str) -> Dict[str, Any]:
        """
        Analyze enhanced crisis patterns with advanced matching logic
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary containing enhanced pattern analysis results
        """
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            if not enhanced_patterns or 'patterns' not in enhanced_patterns:
                return {'patterns_found': [], 'confidence_score': 0.0}
            
            patterns = enhanced_patterns['patterns']
            patterns_found = []
            message_lower = message.lower()
            
            for pattern_group, pattern_data in patterns.items():
                if isinstance(pattern_data, dict) and 'patterns' in pattern_data:
                    for pattern in pattern_data['patterns']:
                        if isinstance(pattern, dict):
                            pattern_text = pattern.get('pattern', '')
                            if pattern_text and pattern_text.lower() in message_lower:
                                patterns_found.append({
                                    'pattern_group': pattern_group,
                                    'pattern_name': pattern.get('name', 'unnamed'),
                                    'matched_text': pattern_text,
                                    'crisis_level': pattern.get('crisis_level', 'medium'),
                                    'confidence': pattern.get('confidence', 0.7),
                                    'context_required': pattern.get('context_required', False),
                                    'severity_modifier': pattern.get('severity_modifier', 1.0)
                                })
            
            # Calculate overall confidence score
            confidence_score = 0.0
            if patterns_found:
                confidence_values = [p.get('confidence', 0.7) for p in patterns_found]
                confidence_score = sum(confidence_values) / len(confidence_values)
            
            return {
                'patterns_found': patterns_found,
                'confidence_score': confidence_score,
                'high_confidence_patterns': [p for p in patterns_found if p.get('confidence', 0) > 0.8]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing enhanced patterns: {e}")
            return {'patterns_found': [], 'confidence_score': 0.0}

    def find_triggered_patterns(self, message: str) -> List[Dict[str, Any]]:
        """
        Find triggered crisis patterns in a message - CRITICAL MISSING METHOD
        
        This method is called by CrisisAnalyzer but was missing from CrisisPatternManager.
        It should search through all pattern types and return triggered patterns.
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of dictionaries containing triggered pattern information
        """
        try:
            triggered_patterns = []
            message_lower = message.lower()
            
            logger.debug(f"🔍 Finding triggered patterns in message: '{message[:50]}...'")
            
            # 1. Check enhanced crisis patterns (these contain the suicidal/hopeless patterns)
            try:
                enhanced_patterns = self.get_enhanced_patterns()
                if enhanced_patterns and 'patterns' in enhanced_patterns:
                    patterns = enhanced_patterns['patterns']
                    
                    for pattern_group, pattern_data in patterns.items():
                        if isinstance(pattern_data, dict) and 'patterns' in pattern_data:
                            for pattern in pattern_data['patterns']:
                                if isinstance(pattern, dict):
                                    pattern_text = pattern.get('pattern', '')
                                    if pattern_text and pattern_text.lower() in message_lower:
                                        triggered_patterns.append({
                                            'pattern_name': pattern_text,
                                            'pattern_type': 'enhanced',
                                            'pattern_group': pattern_group,
                                            'crisis_level': pattern_data.get('crisis_level', 'medium'),
                                            'confidence': pattern.get('weight', 0.7),
                                            'urgency': pattern.get('urgency', 'medium'),
                                            'auto_escalate': pattern.get('auto_escalate', False),
                                            'category': pattern_data.get('category', 'unknown'),
                                            'matched_text': pattern_text,
                                            'source': 'enhanced_crisis_patterns'
                                        })
                                        logger.info(f"🚨 PATTERN TRIGGERED: {pattern_text} (group: {pattern_group}, urgency: {pattern.get('urgency', 'medium')})")
            except Exception as e:
                logger.warning(f"⚠️ Error checking enhanced patterns: {e}")
            
            # 2. Check community patterns
            try:
                community_patterns = self.extract_community_patterns(message)
                for pattern in community_patterns:
                    triggered_patterns.append({
                        'pattern_name': f"community_{pattern.get('pattern_type', 'unknown')}",
                        'pattern_type': 'community',
                        'crisis_level': pattern.get('crisis_level', 'low'),
                        'confidence': pattern.get('confidence', 0.5),
                        'category': 'community',
                        'matched_text': pattern.get('matched_phrase', ''),
                        'source': 'community_patterns'
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error checking community patterns: {e}")
            
            # 3. Check crisis context phrases  
            try:
                context_phrases = self.extract_crisis_context_phrases(message)
                for phrase in context_phrases:
                    triggered_patterns.append({
                        'pattern_name': f"context_{phrase.get('phrase_type', 'unknown')}",
                        'pattern_type': 'context_phrase',
                        'crisis_level': phrase.get('crisis_level', 'low'),
                        'confidence': phrase.get('confidence', 0.5),
                        'category': phrase.get('phrase_type', 'context'),
                        'matched_text': phrase.get('matched_phrase', ''),
                        'source': 'crisis_context_patterns'
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error checking context phrases: {e}")
            
            # 4. Check temporal indicators
            try:
                temporal_analysis = self.analyze_temporal_indicators(message)
                if temporal_analysis and temporal_analysis.get('found_indicators'):
                    for indicator in temporal_analysis.get('found_indicators', []):
                        triggered_patterns.append({
                            'pattern_name': f"temporal_{indicator.get('indicator_type', 'unknown')}",
                            'pattern_type': 'temporal',
                            'crisis_level': indicator.get('crisis_level', 'medium'),
                            'confidence': indicator.get('confidence', 0.6),
                            'category': 'temporal',
                            'matched_text': indicator.get('matched_text', ''),
                            'source': 'temporal_indicators'
                        })
            except Exception as e:
                logger.warning(f"⚠️ Error checking temporal indicators: {e}")
            
            # Log results
            if triggered_patterns:
                logger.info(f"✅ Found {len(triggered_patterns)} triggered patterns")
                for pattern in triggered_patterns:
                    logger.debug(f"   - {pattern['pattern_name']} ({pattern['crisis_level']}) from {pattern['source']}")
            else:
                logger.warning(f"⚠️ No patterns triggered for message: '{message[:50]}...'")
                logger.debug(f"📋 Available pattern sources checked: enhanced_crisis_patterns, community_patterns, crisis_context_patterns, temporal_indicators")
            
            return triggered_patterns
            
        except Exception as e:
            logger.error(f"❌ Error in find_triggered_patterns: {e}")
            logger.exception("Full error details:")
            return []

    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of crisis pattern manager
        
        Returns:
            Dictionary containing manager status and loaded patterns info
        """
        return {
            'status': 'operational',
            'patterns_loaded': len(self._patterns_cache),
            'pattern_types': list(self._patterns_cache.keys()),
            'cache_size': len(self._compiled_regex_cache),
            'version': 'v3.1_step_9.8',
            'config_manager': 'UnifiedConfigManager'
        }


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_crisis_pattern_manager(config_manager: UnifiedConfigManager) -> CrisisPatternManager:
    """
    Factory function to create CrisisPatternManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        CrisisPatternManager instance
    """
    return CrisisPatternManager(config_manager)

__all__ = ['CrisisPatternManager', 'create_crisis_pattern_manager']

logger.info("✅ CrisisPatternManager v3.1 Step 9.8 loaded - ConfigManager eliminated, UnifiedConfigManager integration complete")