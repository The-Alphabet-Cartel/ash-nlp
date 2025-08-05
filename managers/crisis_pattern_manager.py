"""
Crisis Pattern Manager - v3.1 Clean Architecture
Manages all crisis pattern configurations from JSON files with ENV overrides
"""

import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from managers.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class CrisisPatternManager:
    """
    Manages crisis pattern configurations with JSON defaults and ENV overrides
    Following v3.1 clean architecture patterns
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize CrisisPatternManager with ConfigManager dependency injection
        
        Args:
            config_manager: ConfigManager instance for loading JSON configurations
        """
        self.config_manager = config_manager
        self._patterns_cache = {}
        self._compiled_regex_cache = {}
        
        logger.info("CrisisPatternManager v3.1 initializing...")
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
        """Get LGBTQIA+ community vocabulary for enhanced context awareness"""
        return self._patterns_cache.get('community_vocabulary_patterns', {})
    
    def get_context_weights(self) -> Dict[str, Any]:
        """Get context weighting patterns for crisis and positive words"""
        return self._patterns_cache.get('context_weights_patterns', {})
    
    def get_enhanced_crisis_patterns(self) -> Dict[str, Any]:
        """Get enhanced crisis patterns including hopelessness, struggle, and negation"""
        return self._patterns_cache.get('enhanced_crisis_patterns', {})
    
    def get_idiom_patterns(self) -> Dict[str, Any]:
        """Get idiom patterns for false positive reduction"""
        return self._patterns_cache.get('crisis_idiom_patterns', {})
    
    def get_burden_patterns(self) -> Dict[str, Any]:
        """Get burden feeling patterns for self-worth crisis detection"""
        return self._patterns_cache.get('crisis_burden_patterns', {})
    
    def get_lgbtqia_patterns(self) -> Dict[str, Any]:
        """Get LGBTQIA+ specific crisis patterns"""
        return self._patterns_cache.get('crisis_lgbtqia_patterns', {})
    
    def extract_community_patterns(self, message: str) -> List[Dict[str, Any]]:
        """
        Extract LGBTQIA+ community-specific patterns from message
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of matched community patterns with metadata
        """
        phrases = []
        message_lower = message.lower()
        
        lgbtqia_patterns = self.get_lgbtqia_patterns()
        if not lgbtqia_patterns.get('patterns'):
            logger.warning("No LGBTQIA patterns available")
            return phrases
        
        for pattern_name, pattern_group in lgbtqia_patterns['patterns'].items():
            if not pattern_group.get('patterns'):
                continue
                
            for pattern_config in pattern_group['patterns']:
                pattern = pattern_config.get('pattern', '')
                pattern_type = pattern_config.get('type', 'exact_match')
                
                matches = self._find_pattern_matches(message_lower, pattern, pattern_type)
                
                for match_text in matches:
                    phrases.append({
                        'text': match_text,
                        'type': 'community_pattern',
                        'crisis_level': pattern_group.get('crisis_level', 'medium'),
                        'category': pattern_group.get('category', pattern_name),
                        'matched_pattern': pattern,
                        'weight': pattern_config.get('weight', 1.0),
                        'urgency': pattern_config.get('urgency', 'medium')
                    })
        
        return phrases
    
    def extract_crisis_context_phrases(self, message: str) -> List[Dict[str, Any]]:
        """
        Extract phrases with crisis context indicators
        
        Args:
            message: Message text to analyze
            
        Returns:
            List of matched context phrases with metadata
        """
        phrases = []
        message_lower = message.lower()
        words = message_lower.split()
        
        context_patterns = self.get_crisis_context_patterns()
        if not context_patterns.get('patterns'):
            logger.warning("No crisis context patterns available")
            return phrases
        
        for context_name, context_data in context_patterns['patterns'].items():
            indicators = context_data.get('indicators', [])
            
            for indicator in indicators:
                if indicator in message_lower:
                    # Find phrases around the indicator
                    indicator_words = indicator.split()
                    
                    for i, word in enumerate(words):
                        if word == indicator_words[0]:
                            # Check if full indicator matches
                            if ' '.join(words[i:i+len(indicator_words)]) == indicator:
                                # Extract context phrases around the indicator
                                window = context_patterns.get('configuration', {}).get('context_window', 5)
                                start = max(0, i - window//2)
                                end = min(len(words), i + len(indicator_words) + window//2)
                                
                                context_phrase = ' '.join(words[start:end])
                                
                                phrases.append({
                                    'text': context_phrase,
                                    'type': 'crisis_context',
                                    'context_type': context_data.get('context_type', context_name),
                                    'crisis_boost': context_data.get('crisis_boost', 'medium'),
                                    'boost_factor': context_data.get('boost_factor', 0.1),
                                    'indicator': indicator,
                                    'weight': context_data.get('weight', 1.0),
                                    'priority': context_data.get('priority', 'medium')
                                })
        
        return phrases
    
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
            
            # 4. Check enhanced crisis patterns
            try:
                enhanced_patterns = self.check_enhanced_crisis_patterns(message)
                if enhanced_patterns and enhanced_patterns.get('matches'):
                    for match in enhanced_patterns.get('matches', []):
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"enhanced_{match.get('pattern_name', 'unknown')}",
                            'pattern_type': 'enhanced',
                            'crisis_level': match.get('crisis_level', 'high'),
                            'confidence': match.get('confidence', 0.7),
                            'details': match
                        })
                analysis_result['details']['enhanced_patterns'] = enhanced_patterns
            except Exception as e:
                logger.warning(f"Enhanced patterns analysis failed: {e}")
                analysis_result['details']['enhanced_patterns'] = {}
            
            # 5. Apply context weights if patterns were found
            if analysis_result['patterns_triggered']:
                try:
                    # Use a base score for weight calculation
                    base_score = 0.5
                    weighted_score, weight_details = self.apply_context_weights(message, base_score)
                    analysis_result['details']['context_weights'] = {
                        'original_score': base_score,
                        'weighted_score': weighted_score,
                        'weight_details': weight_details
                    }
                except Exception as e:
                    logger.warning(f"Context weights application failed: {e}")
                    analysis_result['details']['context_weights'] = {}
            
            # 6. Calculate summary statistics
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
            Dictionary with temporal analysis results
        """
        message_lower = message.lower()
        temporal_patterns = self.get_temporal_indicators()
        
        if not temporal_patterns.get('patterns'):
            return {
                'found_indicators': [],
                'highest_urgency': 'none',
                'total_boost': 0.0,
                'auto_escalate': False,
                'staff_alert': False
            }
        
        found_indicators = []
        highest_urgency = 'none'
        total_boost = 0.0
        auto_escalate = False
        staff_alert = False
        
        urgency_levels = {'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4, 'immediate': 5}
        max_urgency_score = 0
        
        for pattern_name, pattern_data in temporal_patterns['patterns'].items():
            indicators = pattern_data.get('indicators', [])
            
            for indicator in indicators:
                if indicator in message_lower:
                    boost_factor = pattern_data.get('boost_factor', 0.0)
                    urgency = pattern_data.get('escalation_level', 'medium')
                    
                    found_indicators.append({
                        'indicator': indicator,
                        'pattern_type': pattern_name,
                        'boost_factor': boost_factor,
                        'urgency': urgency,
                        'auto_escalate': pattern_data.get('auto_escalate', False),
                        'staff_alert': pattern_data.get('staff_alert', False)
                    })
                    
                    total_boost += boost_factor
                    
                    if pattern_data.get('auto_escalate', False):
                        auto_escalate = True
                    if pattern_data.get('staff_alert', False):
                        staff_alert = True
                    
                    urgency_score = urgency_levels.get(urgency, 0)
                    if urgency_score > max_urgency_score:
                        max_urgency_score = urgency_score
                        highest_urgency = urgency
        
        # Apply maximum boost limit
        max_boost = temporal_patterns.get('escalation_rules', {}).get('max_temporal_boost', 0.50)
        total_boost = min(total_boost, max_boost)
        
        return {
            'found_indicators': found_indicators,
            'highest_urgency': highest_urgency,
            'total_boost': total_boost,
            'auto_escalate': auto_escalate,
            'staff_alert': staff_alert
        }
    
    def apply_context_weights(self, message: str, base_crisis_score: float) -> Tuple[float, Dict[str, Any]]:
        """
        Apply context weights to modify crisis score based on context words
        
        Args:
            message: Message text to analyze
            base_crisis_score: Base crisis score to modify
            
        Returns:
            Tuple of (modified_score, analysis_details)
        """
        message_lower = message.lower()
        context_weights = self.get_context_weights()
        
        if not context_weights.get('weights'):
            return base_crisis_score, {'analysis': 'no_context_weights_available'}
        
        crisis_boost = 0.0
        positive_reduction = 0.0
        found_crisis_words = []
        found_positive_words = []
        
        # Process crisis context words
        crisis_words = context_weights['weights'].get('crisis_context_words', {})
        if crisis_words.get('words'):
            for word_config in crisis_words['words']:
                word = word_config.get('word', '')
                weight = word_config.get('weight', 0.0)
                
                if self._word_in_message(word, message_lower):
                    crisis_boost += weight
                    found_crisis_words.append({
                        'word': word,
                        'weight': weight,
                        'priority': word_config.get('priority', 'medium')
                    })
        
        # Process positive context words  
        positive_words = context_weights['weights'].get('positive_context_words', {})
        if positive_words.get('words'):
            for word_config in positive_words['words']:
                word = word_config.get('word', '')
                weight = word_config.get('weight', 0.0)
                validation_required = word_config.get('validation_required', True)
                
                if self._word_in_message(word, message_lower):
                    # Simple validation - ensure word is not negated
                    if not validation_required or not self._is_word_negated(word, message_lower):
                        positive_reduction += weight  # weight is negative for positive words
                        found_positive_words.append({
                            'word': word,
                            'weight': weight,
                            'priority': word_config.get('priority', 'medium')
                        })
        
        # Apply limits
        max_crisis_boost = context_weights.get('processing_rules', {}).get('max_total_crisis_boost', 0.30)
        max_positive_reduction = context_weights.get('processing_rules', {}).get('max_total_positive_reduction', -0.25)
        
        crisis_boost = min(crisis_boost, max_crisis_boost)
        positive_reduction = max(positive_reduction, max_positive_reduction)
        
        # Calculate final score
        total_adjustment = crisis_boost + positive_reduction
        modified_score = max(0.0, min(1.0, base_crisis_score + total_adjustment))
        
        analysis_details = {
            'crisis_boost': crisis_boost,
            'positive_reduction': positive_reduction,
            'total_adjustment': total_adjustment,
            'found_crisis_words': found_crisis_words,
            'found_positive_words': found_positive_words,
            'original_score': base_crisis_score,
            'modified_score': modified_score
        }
        
        return modified_score, analysis_details
    
    def check_enhanced_crisis_patterns(self, message: str) -> Dict[str, Any]:
        """
        Check for enhanced crisis patterns (hopelessness, planning, methods, etc.)
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary with enhanced pattern analysis results
        """
        message_lower = message.lower()
        enhanced_patterns = self.get_enhanced_crisis_patterns()
        
        if not enhanced_patterns.get('patterns'):
            return {
                'matches': [],
                'highest_urgency': 'none',
                'auto_escalate': False,
                'total_weight': 0.0,
                'requires_immediate_attention': False
            }
        
        matches = []
        highest_urgency = 'none'
        auto_escalate = False
        total_weight = 0.0
        requires_immediate_attention = False
        
        urgency_levels = {'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        max_urgency_score = 0
        
        for pattern_category, pattern_data in enhanced_patterns['patterns'].items():
            category_patterns = pattern_data.get('patterns', [])
            
            for pattern_config in category_patterns:
                pattern = pattern_config.get('pattern', '')
                pattern_type = pattern_config.get('type', 'exact_match')
                weight = pattern_config.get('weight', 0.0)
                urgency = pattern_config.get('urgency', 'medium')
                
                if pattern_config.get('context_required', False):
                    # For context-required patterns, do additional validation
                    pattern_matches = self._find_pattern_matches_with_context(message_lower, pattern, pattern_type)
                else:
                    pattern_matches = self._find_pattern_matches(message_lower, pattern, pattern_type)
                
                if pattern_matches:
                    match_info = {
                        'category': pattern_category,
                        'pattern': pattern,
                        'weight': weight,
                        'urgency': urgency,
                        'auto_escalate': pattern_config.get('auto_escalate', False),
                        'matches': pattern_matches
                    }
                    
                    matches.append(match_info)
                    total_weight += abs(weight)  # Use absolute value for total weight calculation
                    
                    if pattern_config.get('auto_escalate', False):
                        auto_escalate = True
                    
                    if urgency in ['critical']:
                        requires_immediate_attention = True
                    
                    urgency_score = urgency_levels.get(urgency, 0)
                    if urgency_score > max_urgency_score:
                        max_urgency_score = urgency_score
                        highest_urgency = urgency
        
        return {
            'matches': matches,
            'highest_urgency': highest_urgency,
            'auto_escalate': auto_escalate,
            'total_weight': total_weight,
            'requires_immediate_attention': requires_immediate_attention
        }
    
    def _find_pattern_matches(self, text: str, pattern: str, pattern_type: str) -> List[str]:
        """Find pattern matches in text based on pattern type"""
        matches = []
        
        try:
            if pattern_type == 'exact_match':
                if pattern in text:
                    matches.append(pattern)
            elif pattern_type == 'regex':
                compiled_pattern = self._get_compiled_regex(pattern)
                if compiled_pattern:
                    regex_matches = compiled_pattern.finditer(text)
                    matches.extend([match.group().strip() for match in regex_matches])
        except Exception as e:
            logger.error(f"Error matching pattern '{pattern}': {e}")
        
        return matches
    
    def _find_pattern_matches_with_context(self, text: str, pattern: str, pattern_type: str) -> List[str]:
        """Find pattern matches with additional context validation"""
        # For now, use basic pattern matching
        # This can be enhanced with more sophisticated context analysis
        return self._find_pattern_matches(text, pattern, pattern_type)
    
    def _get_compiled_regex(self, pattern: str) -> Optional[re.Pattern]:
        """Get compiled regex pattern with caching"""
        if pattern not in self._compiled_regex_cache:
            try:
                self._compiled_regex_cache[pattern] = re.compile(pattern, re.IGNORECASE)
            except re.error as e:
                logger.error(f"Invalid regex pattern '{pattern}': {e}")
                return None
        
        return self._compiled_regex_cache.get(pattern)
    
    def _word_in_message(self, word: str, message: str) -> bool:
        """Check if word exists in message with word boundary awareness"""
        pattern = f"\\b{re.escape(word)}\\b"
        return bool(re.search(pattern, message, re.IGNORECASE))
    
    def _is_word_negated(self, word: str, message: str) -> bool:
        """Simple negation detection for context words"""
        negation_words = ['not', 'never', 'no', "don't", "won't", "can't", "isn't", "aren't"]
        
        words = message.split()
        for i, msg_word in enumerate(words):
            if word in msg_word.lower():
                # Check if any negation word appears within 3 words before
                for j in range(max(0, i-3), i):
                    if words[j].lower() in negation_words:
                        return True
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get CrisisPatternManager status information"""
        return {
            'manager': 'CrisisPatternManager',
            'version': '3.1.0',
            'architecture': 'v3.1_clean',
            'loaded_pattern_sets': len(self._patterns_cache),
            'available_pattern_types': list(self._patterns_cache.keys()),
            'compiled_regex_cache_size': len(self._compiled_regex_cache),
            'configuration_enabled': all(
                patterns.get('configuration', {}).get('enabled', False) 
                for patterns in self._patterns_cache.values()
            )
        }
    
    def validate_patterns(self) -> Dict[str, Any]:
        """Validate all loaded patterns for integrity"""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'pattern_counts': {}
        }
        
        # Known configuration keys that might accidentally appear in patterns section
        config_keys_to_skip = {
            'weight_multiplier', 'boost_multiplier', 'enabled', 'threshold',
            'confidence_threshold', 'priority_level', 'escalation_enabled',
            'auto_escalate', 'staff_alert', 'requires_attention'
        }
        
        for pattern_type, patterns in self._patterns_cache.items():
            try:
                if not patterns:
                    validation_result['warnings'].append(f"Empty pattern set: {pattern_type}")
                    continue
                
                pattern_groups = patterns.get('patterns', {})
                total_patterns = 0
                
                if not pattern_groups:
                    validation_result['warnings'].append(f"No patterns found in {pattern_type}")
                    validation_result['pattern_counts'][pattern_type] = 0
                    continue
                
                # FIXED: Skip configuration values that leaked into patterns section
                for group_name, group_data in pattern_groups.items():
                    # Skip known configuration keys
                    if group_name in config_keys_to_skip:
                        logger.debug(f"⚠️ Skipping config value in patterns: {group_name} = {group_data}")
                        continue
                    
                    # Only process actual pattern groups (dictionaries)
                    if not isinstance(group_data, dict):
                        logger.warning(f"⚠️ Skipping non-dict pattern group: {group_name} ({type(group_data).__name__})")
                        continue
                    
                    # Count patterns in this group
                    group_patterns = group_data.get('patterns', [])
                    if isinstance(group_patterns, list):
                        total_patterns += len(group_patterns)
                    elif isinstance(group_patterns, dict):
                        total_patterns += len(group_patterns)
                    elif group_patterns:  # Non-empty value
                        total_patterns += 1
                
                validation_result['pattern_counts'][pattern_type] = total_patterns
                
                if total_patterns == 0:
                    validation_result['warnings'].append(f"No patterns found in {pattern_type}")
                else:
                    logger.debug(f"✅ {pattern_type}: {total_patterns} patterns validated")
                
            except Exception as e:
                error_msg = f"Validation error in {pattern_type}: {e}"
                validation_result['errors'].append(error_msg)
                validation_result['valid'] = False
                logger.error(f"❌ {error_msg}")
        
        # Log summary
        total_errors = len(validation_result['errors'])
        total_warnings = len(validation_result['warnings'])
        total_patterns = sum(validation_result['pattern_counts'].values())
        
        if total_errors == 0:
            logger.info(f"✅ Pattern validation successful: {total_patterns} patterns across {len(validation_result['pattern_counts'])} sets")
            if total_warnings > 0:
                logger.info(f"⚠️ {total_warnings} warnings (non-critical)")
        else:
            logger.error(f"❌ Pattern validation failed: {total_errors} errors, {total_warnings} warnings")
        
        return validation_result

def create_crisis_pattern_manager(config_manager: ConfigManager) -> CrisisPatternManager:
    """
    Factory function to create CrisisPatternManager instance
    
    Args:
        config_manager: ConfigManager instance for dependency injection
        
    Returns:
        CrisisPatternManager instance
    """
    return CrisisPatternManager(config_manager)


# Export for clean architecture
__all__ = [
    'CrisisPatternManager',
    'create_crisis_pattern_manager'
]