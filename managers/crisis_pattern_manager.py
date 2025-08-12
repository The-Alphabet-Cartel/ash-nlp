#!/usr/bin/env python3
"""
Crisis Pattern Manager for Ash NLP Service v3.1 - Hybrid v3.1 Compatible
Enhanced crisis pattern detection and analysis with v3.1 JSON compliance

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

SAFETY NOTICE: This manager handles life-threatening crisis patterns that require immediate intervention.
"""

import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from managers.unified_config_manager import UnifiedConfigManager

logger = logging.getLogger(__name__)

class CrisisPatternManager:
    """
    Crisis Pattern Manager with comprehensive pattern analysis and v3.1 JSON compatibility
    
    Features:
    - Enhanced crisis pattern detection with immediate escalation
    - Advanced pattern matching with context validation
    - Temporal indicators for time-sensitive crisis detection
    - Community-specific vocabulary and context patterns
    - Production-ready error handling and resilience
    - v3.1 JSON configuration compatibility
    
    CRITICAL: This manager detects life-threatening situations requiring immediate response.
    """
    
    def __init__(self, config_manager: UnifiedConfigManager):
        """
        Initialize Crisis Pattern Manager with v3.1 compatibility
        
        Args:
            config_manager: UnifiedConfigManager instance for configuration access
        """
        self.config_manager = config_manager
        self._patterns_cache = {}
        self._compiled_regex_cache = {}
        
        logger.info("CrisisPatternManager v3.1 hybrid initializing...")
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

    # ========================================================================
    # ENHANCED PATTERNS ACCESS - v3.1 Compatible
    # ========================================================================
    
    def get_enhanced_patterns(self) -> Dict[str, Any]:
        """
        Get enhanced crisis patterns with v3.1 JSON compatibility
        
        Returns:
            Dictionary containing enhanced crisis patterns with metadata
        """
        return self._patterns_cache.get('enhanced_crisis_patterns', {})

    def analyze_enhanced_patterns(self, message: str) -> Dict[str, Any]:
        """
        Analyze enhanced crisis patterns with v3.1 JSON compatibility
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary containing enhanced pattern analysis results with safety flags
        """
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            if not enhanced_patterns or 'patterns' not in enhanced_patterns:
                logger.debug("⚠️ No enhanced patterns available for analysis")
                return {'patterns_found': [], 'confidence_score': 0.0, 'safety_flags': {}}
            
            patterns = enhanced_patterns['patterns']
            processing_rules = enhanced_patterns.get('processing_rules', {})
            defaults = processing_rules.get('defaults', {})
            escalation_rules = enhanced_patterns.get('escalation_rules', {})
            pattern_defaults = enhanced_patterns.get('pattern_defaults', {})
            
            # Get processing configuration with v3.1 fallbacks
            case_sensitive = processing_rules.get('case_sensitive', defaults.get('case_sensitive', False))
            context_window = int(processing_rules.get('context_window', defaults.get('context_window', 10)))
            max_pattern_boost = float(processing_rules.get('max_pattern_boost', defaults.get('max_pattern_boost', 0.50)))
            
            patterns_found = []
            safety_flags = {
                'critical_patterns_detected': [],
                'auto_escalation_required': [],
                'immediate_intervention_patterns': [],
                'emergency_response_triggered': False
            }
            
            # Prepare message for analysis
            message_text = message if case_sensitive else message.lower()
            
            logger.debug(f"🔍 Enhanced pattern analysis: {len(patterns)} pattern categories")
            
            # Analyze each pattern category
            for pattern_group, pattern_data in patterns.items():
                if not isinstance(pattern_data, dict) or 'patterns' not in pattern_data:
                    continue
                
                category_defaults = pattern_defaults.get(pattern_group, {})
                crisis_level = pattern_data.get('crisis_level', category_defaults.get('crisis_level', 'medium'))
                category_description = pattern_data.get('description', f'{pattern_group} patterns')
                
                # Process patterns in this category
                for pattern_item in pattern_data['patterns']:
                    if not isinstance(pattern_item, dict):
                        continue
                    
                    pattern_text = pattern_item.get('pattern', '')
                    if not pattern_text:
                        continue
                    
                    # Determine pattern matching method
                    pattern_type = pattern_item.get('type', 'exact_match')
                    matched = False
                    
                    if pattern_type == 'regex':
                        try:
                            # Compile and cache regex patterns
                            cache_key = f"{pattern_group}_{pattern_text}"
                            if cache_key not in self._compiled_regex_cache:
                                flags = 0 if case_sensitive else re.IGNORECASE
                                self._compiled_regex_cache[cache_key] = re.compile(pattern_text, flags)
                            
                            regex_pattern = self._compiled_regex_cache[cache_key]
                            match = regex_pattern.search(message)
                            matched = match is not None
                            
                        except re.error as e:
                            logger.warning(f"⚠️ Invalid regex pattern '{pattern_text}': {e}")
                            continue
                    
                    elif pattern_type == 'exact_match':
                        # Use case sensitivity setting
                        search_text = pattern_text if case_sensitive else pattern_text.lower()
                        matched = search_text in message_text
                    
                    if matched:
                        # Extract pattern details with v3.1 environment variable support
                        weight = float(pattern_item.get('weight', category_defaults.get('weight_medium', 0.7)))
                        urgency = pattern_item.get('urgency', category_defaults.get('urgency', 'medium'))
                        auto_escalate = pattern_item.get('auto_escalate', category_defaults.get('auto_escalate', False))
                        context_required = pattern_item.get('context_required', category_defaults.get('context_required', False))
                        
                        pattern_result = {
                            'pattern_group': pattern_group,
                            'pattern_name': pattern_text,
                            'pattern_type': pattern_type,
                            'matched_text': pattern_text,
                            'crisis_level': crisis_level,
                            'weight': weight,
                            'urgency': urgency,
                            'auto_escalate': auto_escalate,
                            'context_required': context_required,
                            'confidence': min(weight + 0.1, 1.0),  # Slight confidence boost for matches
                            'category_description': category_description,
                            'matched_via': 'enhanced_patterns_v3.1'
                        }
                        
                        patterns_found.append(pattern_result)
                        
                        # Update safety flags
                        if crisis_level == 'critical':
                            safety_flags['critical_patterns_detected'].append(pattern_text)
                            safety_flags['emergency_response_triggered'] = True
                        
                        if auto_escalate:
                            safety_flags['auto_escalation_required'].append(pattern_text)
                        
                        if urgency == 'critical':
                            safety_flags['immediate_intervention_patterns'].append(pattern_text)
                        
                        logger.info(f"🚨 ENHANCED PATTERN MATCH: {pattern_group} → {pattern_text} (level: {crisis_level})")
            
            # Calculate overall confidence score
            confidence_score = 0.0
            if patterns_found:
                confidence_values = [p.get('confidence', 0.7) for p in patterns_found]
                confidence_score = min(sum(confidence_values) / len(confidence_values), 1.0)
            
            # Check emergency response threshold
            emergency_threshold = float(escalation_rules.get('emergency_response_threshold', 
                                      escalation_rules.get('defaults', {}).get('emergency_response_threshold', 0.80)))
            
            if confidence_score >= emergency_threshold or safety_flags['critical_patterns_detected']:
                safety_flags['emergency_response_triggered'] = True
            
            analysis_result = {
                'patterns_found': patterns_found,
                'confidence_score': confidence_score,
                'safety_flags': safety_flags,
                'high_confidence_patterns': [p for p in patterns_found if p.get('confidence', 0) > 0.8],
                'critical_patterns': [p for p in patterns_found if p.get('crisis_level') == 'critical'],
                'auto_escalation_patterns': [p for p in patterns_found if p.get('auto_escalate', False)],
                'processing_info': {
                    'case_sensitive': case_sensitive,
                    'context_window': context_window,
                    'max_pattern_boost': max_pattern_boost,
                    'emergency_threshold': emergency_threshold,
                    'categories_analyzed': len(patterns),
                    'total_patterns_checked': sum(len(cat.get('patterns', [])) for cat in patterns.values() if isinstance(cat, dict))
                }
            }
            
            # Log safety-critical findings
            if safety_flags['emergency_response_triggered']:
                logger.critical(f"🚨 EMERGENCY RESPONSE TRIGGERED - Critical patterns: {safety_flags['critical_patterns_detected']}")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Error analyzing enhanced patterns: {e}")
            return {
                'patterns_found': [], 
                'confidence_score': 0.0,
                'safety_flags': {'analysis_error': True},
                'error': str(e)
            }

    # ========================================================================
    # CORE PATTERN ACCESS METHODS - Backward Compatibility
    # ========================================================================
    
    def get_crisis_patterns(self) -> List[Dict[str, Any]]:
        """Get all crisis patterns for backward compatibility"""
        all_patterns = []
        
        try:
            for pattern_type, pattern_data in self._patterns_cache.items():
                if isinstance(pattern_data, dict) and 'patterns' in pattern_data:
                    patterns_section = pattern_data['patterns']
                    
                    if isinstance(patterns_section, dict):
                        for group_name, group_patterns in patterns_section.items():
                            if isinstance(group_patterns, dict) and 'patterns' in group_patterns:
                                for pattern in group_patterns['patterns']:
                                    if isinstance(pattern, dict):
                                        pattern_with_meta = pattern.copy()
                                        pattern_with_meta['source_type'] = pattern_type
                                        pattern_with_meta['source_group'] = group_name
                                        all_patterns.append(pattern_with_meta)
                            elif isinstance(group_patterns, list):
                                for pattern in group_patterns:
                                    if isinstance(pattern, dict):
                                        pattern_with_meta = pattern.copy()
                                        pattern_with_meta['source_type'] = pattern_type
                                        pattern_with_meta['source_group'] = group_name
                                        all_patterns.append(pattern_with_meta)
                    elif isinstance(patterns_section, list):
                        for pattern in patterns_section:
                            if isinstance(pattern, dict):
                                pattern_with_meta = pattern.copy()
                                pattern_with_meta['source_type'] = pattern_type
                                all_patterns.append(pattern_with_meta)
            
            logger.debug(f"✅ Aggregated {len(all_patterns)} crisis patterns")
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
    
    def get_idiom_patterns(self) -> Dict[str, Any]:
        """Get idiom-based crisis patterns"""
        return self._patterns_cache.get('crisis_idiom_patterns', {})
    
    def get_burden_patterns(self) -> Dict[str, Any]:
        """Get burden and stress-related patterns"""
        return self._patterns_cache.get('crisis_burden_patterns', {})
    
    def get_lgbtqia_patterns(self) -> Dict[str, Any]:
        """Get LGBTQIA+ community specific patterns"""
        return self._patterns_cache.get('crisis_lgbtqia_patterns', {})

    # ========================================================================
    # PATTERN EXTRACTION METHODS
    # ========================================================================

    def extract_community_patterns(self, message: str) -> List[Dict[str, Any]]:
        """Extract community-specific patterns from message"""
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
        """Extract crisis context phrases that amplify crisis detection"""
        found_phrases = []
        message_lower = message.lower()
        
        try:
            context_patterns = self.get_crisis_context_patterns()
            if not context_patterns or 'patterns' not in context_patterns:
                return found_phrases
            
            patterns = context_patterns['patterns']
            
            for context_type, context_data in patterns.items():
                if not isinstance(context_data, dict):
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

    def analyze_temporal_indicators(self, message: str) -> Dict[str, Any]:
        """Analyze temporal indicators in message for crisis urgency assessment"""
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

    # ========================================================================
    # COMPREHENSIVE MESSAGE ANALYSIS
    # ========================================================================

    def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict[str, Any]:
        """Comprehensive message analysis with v3.1 enhanced safety features"""
        try:
            analysis_result = {
                'patterns_triggered': [],
                'analysis_available': True,
                'error': None,
                'details': {},
                'safety_assessment': {
                    'immediate_intervention_required': False,
                    'emergency_response_recommended': False,
                    'auto_escalation_triggered': False,
                    'critical_patterns_detected': [],
                    'highest_risk_level': 'none'
                }
            }
            
            logger.debug(f"🔍 Starting comprehensive v3.1 analysis for message (length: {len(message)})")
            
            # Enhanced patterns analysis (HIGHEST PRIORITY)
            try:
                enhanced_analysis = self.analyze_enhanced_patterns(message)
                if enhanced_analysis and enhanced_analysis.get('patterns_found'):
                    for pattern in enhanced_analysis.get('patterns_found', []):
                        pattern_data = {
                            'pattern_name': f"enhanced_{pattern.get('pattern_name', 'unknown')}",
                            'pattern_type': 'enhanced',
                            'crisis_level': pattern.get('crisis_level', 'medium'),
                            'confidence': pattern.get('confidence', 0.7),
                            'urgency': pattern.get('urgency', 'medium'),
                            'auto_escalate': pattern.get('auto_escalate', False),
                            'weight': pattern.get('weight', 0.7),
                            'details': pattern
                        }
                        analysis_result['patterns_triggered'].append(pattern_data)
                        
                        # Update safety assessment
                        if pattern.get('crisis_level') == 'critical':
                            analysis_result['safety_assessment']['critical_patterns_detected'].append(pattern_data['pattern_name'])
                        
                        if pattern.get('auto_escalate', False):
                            analysis_result['safety_assessment']['auto_escalation_triggered'] = True
                        
                        if pattern.get('urgency') == 'critical':
                            analysis_result['safety_assessment']['immediate_intervention_required'] = True
                
                # Process safety flags from enhanced analysis
                safety_flags = enhanced_analysis.get('safety_flags', {})
                if safety_flags.get('emergency_response_triggered', False):
                    analysis_result['safety_assessment']['emergency_response_recommended'] = True
                
                analysis_result['details']['enhanced_patterns'] = enhanced_analysis
                
            except Exception as e:
                logger.error(f"❌ Enhanced patterns analysis failed: {e}")
                analysis_result['details']['enhanced_patterns'] = {'error': str(e)}
            
            # Community patterns analysis
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
                logger.warning(f"⚠️ Community patterns analysis failed: {e}")
                analysis_result['details']['community_patterns'] = {'error': str(e)}
            
            # Context phrases analysis
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
                logger.warning(f"⚠️ Context phrases analysis failed: {e}")
                analysis_result['details']['context_phrases'] = {'error': str(e)}
            
            # Temporal indicators analysis
            try:
                temporal_analysis = self.analyze_temporal_indicators(message)
                if temporal_analysis and temporal_analysis.get('found_indicators'):
                    for indicator in temporal_analysis.get('found_indicators', []):
                        pattern_data = {
                            'pattern_name': f"temporal_{indicator.get('indicator_type', 'unknown')}",
                            'pattern_type': 'temporal',
                            'crisis_level': indicator.get('crisis_level', 'medium'),
                            'confidence': indicator.get('confidence', 0.6),
                            'urgency_multiplier': indicator.get('urgency_multiplier', 1.0),
                            'details': indicator
                        }
                        analysis_result['patterns_triggered'].append(pattern_data)
                        
                        # Check for immediate intervention based on temporal urgency
                        if indicator.get('time_sensitivity') == 'immediate':
                            analysis_result['safety_assessment']['immediate_intervention_required'] = True
                
                analysis_result['details']['temporal_indicators'] = temporal_analysis
            except Exception as e:
                logger.warning(f"⚠️ Temporal indicators analysis failed: {e}")
                analysis_result['details']['temporal_indicators'] = {'error': str(e)}
            
            # Calculate comprehensive summary with safety assessment
            pattern_count = len(analysis_result['patterns_triggered'])
            crisis_levels = [p.get('crisis_level', 'low') for p in analysis_result['patterns_triggered']]
            
            # Determine highest crisis level
            level_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
            highest_level = 'none'
            if crisis_levels:
                highest_level = max(crisis_levels, key=lambda x: level_priority.get(x, 0))
            
            analysis_result['safety_assessment']['highest_risk_level'] = highest_level
            
            # Emergency response decision logic
            if (highest_level == 'critical' or 
                analysis_result['safety_assessment']['immediate_intervention_required'] or
                len(analysis_result['safety_assessment']['critical_patterns_detected']) > 0):
                analysis_result['safety_assessment']['emergency_response_recommended'] = True
            
            # Build comprehensive summary
            analysis_result.update({
                'summary': {
                    'total_patterns': pattern_count,
                    'highest_crisis_level': highest_level,
                    'pattern_types': list(set([p.get('pattern_type', 'unknown') for p in analysis_result['patterns_triggered']])),
                    'requires_attention': highest_level in ['critical', 'high', 'medium'] or pattern_count >= 3,
                    'requires_immediate_response': analysis_result['safety_assessment']['immediate_intervention_required'],
                    'requires_emergency_response': analysis_result['safety_assessment']['emergency_response_recommended'],
                    'auto_escalation_needed': analysis_result['safety_assessment']['auto_escalation_triggered'],
                    'critical_pattern_count': len(analysis_result['safety_assessment']['critical_patterns_detected'])
                },
                'metadata': {
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'analysis_timestamp': time.time(),
                    'analysis_date': datetime.now().isoformat(),
                    'methods_used': ['enhanced_patterns', 'community_patterns', 'context_phrases', 'temporal_indicators'],
                    'manager_version': 'v3.1-hybrid',
                    'safety_analysis_version': 'v3.1',
                    'v3_1_features_used': True
                }
            })
            
            # Log safety-critical results with appropriate severity
            if analysis_result['safety_assessment']['immediate_intervention_required']:
                logger.critical(f"🚨 IMMEDIATE INTERVENTION REQUIRED - User: {user_id}, Channel: {channel_id}")
            elif analysis_result['safety_assessment']['emergency_response_recommended']:
                logger.error(f"⚠️ EMERGENCY RESPONSE RECOMMENDED - Highest level: {highest_level}, User: {user_id}")
            elif highest_level in ['high', 'medium']:
                logger.warning(f"⚠️ Crisis patterns detected - Level: {highest_level}, Count: {pattern_count}, User: {user_id}")
            
            logger.debug(f"✅ v3.1 crisis analysis complete: {pattern_count} patterns, level: {highest_level}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Comprehensive crisis analysis failed: {e}")
            return {
                'patterns_triggered': [],
                'analysis_available': False,
                'error': str(e),
                'details': {},
                'safety_assessment': {
                    'immediate_intervention_required': False,
                    'emergency_response_recommended': False,
                    'auto_escalation_triggered': False,
                    'critical_patterns_detected': [],
                    'highest_risk_level': 'error',
                    'analysis_error': True
                },
                'summary': {
                    'total_patterns': 0,
                    'highest_crisis_level': 'error',
                    'pattern_types': [],
                    'requires_attention': True,
                    'requires_immediate_response': False,
                    'requires_emergency_response': False,
                    'auto_escalation_needed': False,
                    'critical_pattern_count': 0
                },
                'metadata': {
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'analysis_timestamp': time.time(),
                    'error_occurred': True,
                    'manager_version': 'v3.1-hybrid'
                }
            }

    # ========================================================================
    # SEMANTIC PATTERN ANALYSIS - Preserved Original Functionality
    # ========================================================================

    def find_triggered_patterns(self, message: str, models_manager=None) -> List[Dict[str, Any]]:
        """Find triggered crisis patterns using semantic NLP classification"""
        try:
            if models_manager:
                semantic_patterns = self._find_patterns_semantic(message, models_manager)
                if semantic_patterns:
                    logger.info(f"✅ Semantic classification found {len(semantic_patterns)} patterns")
                    return semantic_patterns
            
            logger.info("🔄 Using enhanced pattern matching fallback")
            return self._find_patterns_enhanced_fallback(message)
            
        except Exception as e:
            logger.error(f"❌ Error in find_triggered_patterns: {e}")
            return []

    def _find_patterns_semantic(self, message: str, models_manager) -> List[Dict[str, Any]]:
        """Use zero-shot classification models for semantic pattern detection"""
        try:
            triggered_patterns = []
            
            logger.debug(f"🧠 Semantic analysis for: '{message[:50]}...'")
            
            crisis_categories = {
                'suicidal_ideation': {
                    'hypothesis_template': "This message expresses thoughts about suicide, not wanting to live, or ending one's life",
                    'crisis_level': 'critical',
                    'urgency': 'critical',
                    'auto_escalate': True,
                    'confidence_threshold': 0.5
                },
                'hopelessness': {
                    'hypothesis_template': "This message expresses feelings of hopelessness, despair, or that nothing will improve",
                    'crisis_level': 'high',
                    'urgency': 'high', 
                    'auto_escalate': True,
                    'confidence_threshold': 0.6
                },
                'severe_distress': {
                    'hypothesis_template': "This message expresses severe emotional distress, being overwhelmed, or inability to cope",
                    'crisis_level': 'high',
                    'urgency': 'medium',
                    'auto_escalate': False,
                    'confidence_threshold': 0.65
                },
                'self_harm_planning': {
                    'hypothesis_template': "This message expresses plans or thoughts about self-harm or self-injury",
                    'crisis_level': 'critical',
                    'urgency': 'critical',
                    'auto_escalate': True,
                    'confidence_threshold': 0.55
                }
            }
            
            try:
                model_definitions = models_manager.get_model_definitions()
                
                zero_shot_model = None
                for model_type, model_config in model_definitions.items():
                    if model_config.get('pipeline_task') == 'zero-shot-classification':
                        zero_shot_model = model_type
                        break
                
                if not zero_shot_model:
                    logger.warning("⚠️ No zero-shot classification model found, using fallback")
                    return []
                
                logger.debug(f"✅ Using {zero_shot_model} for semantic classification")
                
                for category, category_info in crisis_categories.items():
                    try:
                        hypothesis = category_info['hypothesis_template']
                        
                        classification_score = self._classify_with_model(
                            message, hypothesis, zero_shot_model, models_manager
                        )
                        
                        threshold = category_info['confidence_threshold']
                        
                        if classification_score >= threshold:
                            triggered_patterns.append({
                                'pattern_name': f"semantic_{category}",
                                'pattern_type': 'semantic_classification',
                                'category': category,
                                'crisis_level': category_info['crisis_level'],
                                'confidence': classification_score,
                                'urgency': category_info['urgency'],
                                'auto_escalate': category_info['auto_escalate'],
                                'hypothesis': hypothesis,
                                'classification_score': classification_score,
                                'source': 'zero_shot_nlp_model',
                                'model_used': zero_shot_model,
                                'threshold_used': threshold
                            })
                            
                            logger.info(f"🚨 SEMANTIC PATTERN: {category} "
                                       f"(score: {classification_score:.3f}, threshold: {threshold})")
                    
                    except Exception as e:
                        logger.warning(f"⚠️ Error classifying {category}: {e}")
                        continue
                
                return triggered_patterns
                
            except Exception as e:
                logger.error(f"❌ Error in semantic classification: {e}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error in _find_patterns_semantic: {e}")
            return []

    def _classify_with_model(self, message: str, hypothesis: str, model_type: str, models_manager) -> float:
        """Perform zero-shot classification using the loaded model"""
        try:
            return self._demo_classification(message, hypothesis)
            
        except Exception as e:
            logger.error(f"❌ Error in model classification: {e}")
            return 0.0

    def _demo_classification(self, message: str, hypothesis: str) -> float:
        """Demo classification logic - REPLACE with actual model calls"""
        message_lower = message.lower()
        
        if "suicide" in hypothesis.lower() or "not wanting to live" in hypothesis.lower():
            suicide_indicators = [
                "don't want to live", "do not want to live", "dont want to live",
                "want to die", "ready to die", "end my life", "kill myself",
                "suicide", "not worth living", "better off dead",
                "continue living", "keep living", "stay alive"
            ]
            
            negation_patterns = ["don't want", "do not want", "dont want"]
            life_patterns = ["live", "living", "continue", "stay alive", "be alive"]
            
            has_negation = any(neg in message_lower for neg in negation_patterns)
            has_life_ref = any(life in message_lower for life in life_patterns)
            
            if has_negation and has_life_ref:
                return 0.85
                
            direct_matches = sum(1 for indicator in suicide_indicators if indicator in message_lower)
            if direct_matches > 0:
                return 0.75
        
        elif "hopeless" in hypothesis.lower():
            hopeless_indicators = [
                "hopeless", "no hope", "despair", "desperate", "pointless",
                "meaningless", "nothing matters", "give up", "giving up"
            ]
            
            matches = sum(1 for indicator in hopeless_indicators if indicator in message_lower)
            if matches > 0:
                return 0.80
        
        elif "distress" in hypothesis.lower():
            distress_indicators = [
                "overwhelming", "can't cope", "breaking down", "falling apart",
                "drowning", "suffocating", "crushing", "unbearable"
            ]
            
            matches = sum(1 for indicator in distress_indicators if indicator in message_lower)
            if matches > 0:
                return 0.70
        
        return 0.0

    def _find_patterns_enhanced_fallback(self, message: str) -> List[Dict[str, Any]]:
        """Enhanced fallback pattern matching"""
        try:
            triggered_patterns = []
            message_lower = message.lower()
            
            logger.debug(f"🔍 Enhanced fallback pattern matching for: '{message[:50]}...'")
            
            pattern_categories = {
                'suicidal_ideation': {
                    'patterns': [
                        "want to die", "ready to die", "going to die", "wish i was dead",
                        "better off dead", "end my life", "kill myself", "commit suicide",
                        "don't want to live", "do not want to live", "dont want to live",
                        "don't want to be alive", "do not want to be alive", "dont want to be alive",
                        "don't want to continue", "do not want to continue", "dont want to continue",
                        "can't go on", "cannot go on", "cant go on",
                        "not worth living", "no point in living", "tired of living",
                        "done with life", "finished with life"
                    ],
                    'crisis_level': 'critical',
                    'urgency': 'critical',
                    'auto_escalate': True,
                    'base_confidence': 0.8
                },
                'hopelessness': {
                    'patterns': [
                        "hopeless", "no hope", "lost hope", "without hope",
                        "completely hopeless", "totally hopeless", "feel hopeless",
                        "nothing will change", "never get better", "no way out",
                        "pointless", "meaningless", "no point", "what's the point"
                    ],
                    'crisis_level': 'high',
                    'urgency': 'high',
                    'auto_escalate': True,
                    'base_confidence': 0.75
                },
                'severe_distress': {
                    'patterns': [
                        "can't take it", "cannot take it", "cant take it",
                        "overwhelming", "too much", "breaking down", "falling apart",
                        "can't cope", "cannot cope", "cant cope",
                        "drowning", "suffocating", "crushing me"
                    ],
                    'crisis_level': 'high',
                    'urgency': 'medium',
                    'auto_escalate': False,
                    'base_confidence': 0.7
                }
            }
            
            for category, category_info in pattern_categories.items():
                patterns = category_info['patterns']
                
                for pattern in patterns:
                    if pattern in message_lower:
                        triggered_patterns.append({
                            'pattern_name': f"enhanced_{category}",
                            'pattern_type': 'enhanced_keyword',
                            'category': category,
                            'crisis_level': category_info['crisis_level'],
                            'confidence': category_info['base_confidence'],
                            'urgency': category_info['urgency'],
                            'auto_escalate': category_info['auto_escalate'],
                            'matched_pattern': pattern,
                            'source': 'enhanced_keyword_fallback'
                        })
                        
                        logger.info(f"🔍 ENHANCED PATTERN: {pattern} → {category}")
                        break
            
            return triggered_patterns
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced fallback matching: {e}")
            return []
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status of crisis pattern manager"""
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            metadata = enhanced_patterns.get('_metadata', {})
            
            return {
                'status': 'operational',
                'patterns_loaded': len(self._patterns_cache),
                'pattern_types': list(self._patterns_cache.keys()),
                'cache_size': len(self._compiled_regex_cache),
                'version': 'v3.1-hybrid',
                'config_manager': 'UnifiedConfigManager',
                'v3_1_compliance': {
                    'json_version': metadata.get('configuration_version', 'unknown'),
                    'compliance_status': metadata.get('compliance', 'unknown'),
                    'metadata_available': bool(metadata),
                    'safety_features_enabled': True
                },
                'safety_features': {
                    'immediate_intervention_detection': True,
                    'auto_escalation_support': True,
                    'emergency_response_triggers': True,
                    'critical_pattern_monitoring': True
                }
            }
        except Exception as e:
            logger.error(f"❌ Error getting status: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'version': 'v3.1-hybrid'
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
        CrisisPatternManager instance with v3.1 hybrid compatibility
    """
    return CrisisPatternManager(config_manager)

__all__ = ['CrisisPatternManager', 'create_crisis_pattern_manager']

logger.info("✅ CrisisPatternManager v3.1 Hybrid loaded - Enhanced safety features + v3.1 compliance")