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
    
    def __init__(self, config_manager):
        """
        Initialize Crisis Pattern Manager with v3.1 compatibility
        
        Args:
            config_manager: UnifiedConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for CrisisPatternManager")
        
        self.config_manager = config_manager
        self._patterns_cache = {}
        self._compiled_regex_cache = {}
        
        logger.info("✅ CrisisPatternManager v3.1 initialized - Hybrid compatibility with enhanced safety features")
        
        # Load all pattern configurations
        self._load_pattern_configurations()
    
    def _load_pattern_configurations(self):
        """Load all crisis pattern configurations with v3.1 compatibility"""
        try:
            # Load all available pattern configurations
            pattern_types = [
                'enhanced_crisis_patterns',
                'crisis_context_patterns', 
                'positive_context_patterns',
                'temporal_indicators_patterns',
                'community_vocabulary_patterns',
                'context_weights_patterns',
                'crisis_idiom_patterns',
                'crisis_burden_patterns'
            ]
            
            patterns_loaded = 0
            for pattern_type in pattern_types:
                try:
                    pattern_data = self.config_manager.load_config_file(pattern_type)
                    if pattern_data:
                        self._patterns_cache[pattern_type] = pattern_data
                        patterns_loaded += 1
                        
                        # Log v3.1 metadata if available
                        metadata = pattern_data.get('_metadata', {})
                        if metadata:
                            config_version = metadata.get('configuration_version', 'unknown')
                            logger.debug(f"✅ Loaded {pattern_type} (v{config_version})")
                        else:
                            logger.debug(f"✅ Loaded {pattern_type} (legacy format)")
                    else:
                        logger.debug(f"⚠️ No configuration found for {pattern_type}")
                        self._patterns_cache[pattern_type] = {}
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load {pattern_type}: {e}")
                    self._patterns_cache[pattern_type] = {}
            
            logger.info(f"✅ Crisis patterns loaded: {patterns_loaded}/{len(pattern_types)} pattern types")
            
            # Validate critical patterns are available
            enhanced_patterns = self._patterns_cache.get('enhanced_crisis_patterns', {})
            if enhanced_patterns and 'patterns' in enhanced_patterns:
                critical_categories = ['hopelessness_patterns', 'planning_indicators', 'method_references']
                available_categories = list(enhanced_patterns['patterns'].keys())
                missing_critical = [cat for cat in critical_categories if cat not in available_categories]
                
                if missing_critical:
                    logger.warning(f"⚠️ Missing critical pattern categories: {missing_critical}")
                else:
                    logger.info("✅ All critical pattern categories available")
            
        except Exception as e:
            logger.error(f"❌ Failed to load pattern configurations: {e}")
            raise ValueError(f"Crisis pattern configuration error: {e}")
    
    # ========================================================================
    # ENHANCED PATTERNS ACCESS - v3.1 Compatible
    # ========================================================================
    
    def get_enhanced_patterns(self) -> Dict[str, Any]:
        """
        Get enhanced crisis patterns with v3.1 JSON compatibility
        
        Returns:
            Dictionary containing enhanced crisis patterns with metadata
        """
        try:
            enhanced_data = self._patterns_cache.get('enhanced_crisis_patterns', {})
            
            # Log v3.1 compliance status
            metadata = enhanced_data.get('_metadata', {})
            if metadata:
                compliance = metadata.get('compliance', 'unknown')
                version = metadata.get('configuration_version', 'unknown')
                logger.debug(f"✅ Enhanced patterns v{version} ({compliance})")
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"❌ Error accessing enhanced patterns: {e}")
            return {}
    
    def get_pattern_category(self, category: str) -> Dict[str, Any]:
        """
        Get specific pattern category from enhanced patterns
        
        Args:
            category: Pattern category name (e.g., 'hopelessness_patterns')
            
        Returns:
            Dictionary containing pattern category data
        """
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            patterns = enhanced_patterns.get('patterns', {})
            
            if category in patterns:
                logger.debug(f"✅ Retrieved pattern category: {category}")
                return patterns[category]
            else:
                logger.warning(f"⚠️ Pattern category not found: {category}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error retrieving pattern category {category}: {e}")
            return {}
    
    # ========================================================================
    # COMPREHENSIVE PATTERN ANALYSIS - Enhanced for Safety
    # ========================================================================
    
    def analyze_crisis_patterns(self, message: str, user_id: Optional[str] = None, 
                              channel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive crisis pattern analysis with immediate escalation for critical patterns
        
        Args:
            message: Message text to analyze
            user_id: Optional user identifier for tracking
            channel_id: Optional channel identifier for context
            
        Returns:
            Dictionary containing comprehensive crisis analysis results
        """
        try:
            analysis_result = {
                'patterns_triggered': [],
                'analysis_available': True,
                'details': {},
                'safety_flags': {
                    'immediate_intervention_required': False,
                    'auto_escalation_triggered': False,
                    'critical_patterns_detected': [],
                    'emergency_response_recommended': False
                }
            }
            
            logger.debug(f"🔍 Starting comprehensive crisis pattern analysis for message length: {len(message)}")
            
            # 1. Enhanced patterns analysis (CRITICAL - highest priority)
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
                            'details': pattern
                        }
                        
                        analysis_result['patterns_triggered'].append(pattern_data)
                        
                        # Check for critical safety flags
                        if pattern.get('crisis_level') == 'critical':
                            analysis_result['safety_flags']['critical_patterns_detected'].append(pattern_data['pattern_name'])
                        
                        if pattern.get('auto_escalate', False):
                            analysis_result['safety_flags']['auto_escalation_triggered'] = True
                        
                        if pattern.get('urgency') == 'critical':
                            analysis_result['safety_flags']['immediate_intervention_required'] = True
                
                analysis_result['details']['enhanced_patterns'] = enhanced_analysis
                
            except Exception as e:
                logger.error(f"❌ Enhanced patterns analysis failed: {e}")
                analysis_result['details']['enhanced_patterns'] = {'error': str(e)}
            
            # 2. Community vocabulary patterns
            try:
                community_analysis = self.analyze_community_patterns(message)
                if community_analysis and community_analysis.get('patterns_found'):
                    for pattern in community_analysis.get('patterns_found', []):
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"community_{pattern.get('pattern', 'unknown')}",
                            'pattern_type': 'community_vocabulary',
                            'crisis_level': pattern.get('crisis_level', 'low'),
                            'confidence': pattern.get('confidence', 0.5),
                            'details': pattern
                        })
                analysis_result['details']['community_patterns'] = community_analysis
            except Exception as e:
                logger.warning(f"⚠️ Community patterns analysis failed: {e}")
                analysis_result['details']['community_patterns'] = {'error': str(e)}
            
            # 3. Context phrase analysis
            try:
                context_analysis = self.analyze_context_phrases(message)
                if context_analysis and context_analysis.get('context_patterns'):
                    for pattern in context_analysis.get('context_patterns', []):
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"context_{pattern.get('pattern', 'unknown')}",
                            'pattern_type': 'context',
                            'crisis_level': pattern.get('level', 'low'),
                            'confidence': pattern.get('confidence', 0.4),
                            'details': pattern
                        })
                analysis_result['details']['context_patterns'] = context_analysis
            except Exception as e:
                logger.warning(f"⚠️ Context patterns analysis failed: {e}")
                analysis_result['details']['context_patterns'] = {'error': str(e)}
            
            # 4. Temporal indicators analysis
            try:
                temporal_analysis = self.analyze_temporal_indicators(message)
                if temporal_analysis and temporal_analysis.get('found_indicators'):
                    for indicator in temporal_analysis.get('found_indicators', []):
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"temporal_{indicator.get('pattern', 'unknown')}",
                            'pattern_type': 'temporal',
                            'crisis_level': indicator.get('crisis_level', 'medium'),
                            'confidence': indicator.get('confidence', 0.6),
                            'urgency_multiplier': indicator.get('urgency_multiplier', 1.0),
                            'details': indicator
                        })
                        
                        # Check temporal urgency
                        if indicator.get('time_sensitivity') == 'immediate':
                            analysis_result['safety_flags']['immediate_intervention_required'] = True
                
                analysis_result['details']['temporal_indicators'] = temporal_analysis
            except Exception as e:
                logger.warning(f"⚠️ Temporal indicators analysis failed: {e}")
                analysis_result['details']['temporal_indicators'] = {'error': str(e)}
            
            # 5. Calculate comprehensive safety assessment
            pattern_count = len(analysis_result['patterns_triggered'])
            crisis_levels = [p.get('crisis_level', 'low') for p in analysis_result['patterns_triggered']]
            
            # Determine highest crisis level
            level_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
            highest_level = 'none'
            if crisis_levels:
                highest_level = max(crisis_levels, key=lambda x: level_priority.get(x, 0))
            
            # Emergency response assessment
            emergency_threshold = 0.80  # Can be configured via enhanced patterns config
            enhanced_config = self.get_enhanced_patterns()
            if enhanced_config.get('escalation_rules', {}).get('emergency_response_threshold'):
                emergency_threshold = float(enhanced_config['escalation_rules']['emergency_response_threshold'])
            
            # Calculate emergency score based on pattern severity and count
            emergency_score = 0.0
            if pattern_count > 0:
                severity_weights = {'critical': 1.0, 'high': 0.8, 'medium': 0.5, 'low': 0.3}
                total_weight = sum(severity_weights.get(level, 0.3) for level in crisis_levels)
                emergency_score = min(total_weight / pattern_count, 1.0)
            
            if emergency_score >= emergency_threshold or highest_level == 'critical':
                analysis_result['safety_flags']['emergency_response_recommended'] = True
            
            # Build comprehensive summary
            analysis_result.update({
                'summary': {
                    'total_patterns': pattern_count,
                    'highest_crisis_level': highest_level,
                    'emergency_score': emergency_score,
                    'emergency_threshold': emergency_threshold,
                    'pattern_types': list(set([p.get('pattern_type', 'unknown') for p in analysis_result['patterns_triggered']])),
                    'requires_attention': highest_level in ['critical', 'high', 'medium'] or pattern_count >= 3,
                    'requires_immediate_response': analysis_result['safety_flags']['immediate_intervention_required'],
                    'auto_escalation_needed': analysis_result['safety_flags']['auto_escalation_triggered']
                },
                'metadata': {
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'analysis_timestamp': time.time(),
                    'analysis_date': datetime.now().isoformat(),
                    'methods_used': ['enhanced_patterns', 'community_patterns', 'context_phrases', 'temporal_indicators'],
                    'manager_version': 'v3.1-hybrid',
                    'safety_assessment_performed': True
                }
            })
            
            # Log safety-critical results
            if analysis_result['safety_flags']['immediate_intervention_required']:
                logger.critical(f"🚨 IMMEDIATE INTERVENTION REQUIRED - Critical patterns detected: {analysis_result['safety_flags']['critical_patterns_detected']}")
            elif analysis_result['safety_flags']['emergency_response_recommended']:
                logger.error(f"⚠️ EMERGENCY RESPONSE RECOMMENDED - High-risk patterns detected, emergency score: {emergency_score}")
            elif highest_level in ['high', 'medium']:
                logger.warning(f"⚠️ Crisis patterns detected - Highest level: {highest_level}, Pattern count: {pattern_count}")
            
            logger.debug(f"✅ Crisis pattern analysis complete: {pattern_count} patterns found, highest level: {highest_level}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Crisis pattern analysis failed: {e}")
            return {
                'patterns_triggered': [],
                'analysis_available': False,
                'error': str(e),
                'details': {},
                'safety_flags': {
                    'immediate_intervention_required': False,
                    'auto_escalation_triggered': False,
                    'critical_patterns_detected': [],
                    'emergency_response_recommended': False,
                    'analysis_error': True
                },
                'summary': {
                    'total_patterns': 0,
                    'highest_crisis_level': 'error',
                    'emergency_score': 0.0,
                    'pattern_types': [],
                    'requires_attention': True,  # Error condition requires attention
                    'requires_immediate_response': False,
                    'auto_escalation_needed': False
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
    # CORE PATTERN ACCESS METHODS - Backward Compatibility Maintained
    # ========================================================================
    
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
                            if isinstance(group_patterns, dict) and 'patterns' in group_patterns:
                                # v3.1 structure: group_patterns is a dict with 'patterns' list
                                for pattern in group_patterns['patterns']:
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
                            elif isinstance(group_patterns, list):
                                # Legacy structure: group_patterns is a direct list
                                for pattern in group_patterns:
                                    if isinstance(pattern, dict):
                                        pattern_with_meta = pattern.copy()
                                        pattern_with_meta['source_type'] = pattern_type
                                        pattern_with_meta['source_group'] = group_name
                                        all_patterns.append(pattern_with_meta)
                                    elif isinstance(pattern, str):
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
    # PATTERN EXTRACTION METHODS - Enhanced for v3.1
    # ========================================================================

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
    
    # ========================================================================
    # SEMANTIC PATTERN ANALYSIS - Preserved Original Functionality
    # ========================================================================

    def find_triggered_patterns(self, message: str, models_manager=None) -> List[Dict[str, Any]]:
        """
        Find triggered crisis patterns using semantic NLP classification
        
        This is the main entry point called by CrisisAnalyzer. It uses semantic
        classification when models are available, falls back to keyword matching otherwise.
        
        Args:
            message: Message text to analyze
            models_manager: ModelEnsembleManager instance for accessing NLP models
            
        Returns:
            List of dictionaries containing triggered pattern information
        """
        try:
            # Try semantic classification first
            if models_manager:
                semantic_patterns = self._find_patterns_semantic(message, models_manager)
                if semantic_patterns:
                    logger.info(f"✅ Semantic classification found {len(semantic_patterns)} patterns")
                    return semantic_patterns
            
            # Fallback to enhanced pattern matching
            logger.info("🔄 Using enhanced pattern matching fallback")
            return self._find_patterns_enhanced_fallback(message)
            
        except Exception as e:
            logger.error(f"❌ Error in find_triggered_patterns: {e}")
            return []

    def _find_patterns_semantic(self, message: str, models_manager) -> List[Dict[str, Any]]:
        """
        Use zero-shot classification models for semantic pattern detection
        
        Args:
            message: Message text to analyze
            models_manager: ModelEnsembleManager instance
            
        Returns:
            List of triggered patterns based on semantic classification
        """
        try:
            triggered_patterns = []
            
            logger.debug(f"🧠 Semantic analysis for: '{message[:50]}...'")
            
            # Define semantic crisis categories
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
            
            # Get model definitions to find zero-shot capable model
            try:
                model_definitions = models_manager.get_model_definitions()
                
                # Find a zero-shot classification model
                zero_shot_model = None
                for model_type, model_config in model_definitions.items():
                    if model_config.get('pipeline_task') == 'zero-shot-classification':
                        zero_shot_model = model_type
                        break
                
                if not zero_shot_model:
                    logger.warning("⚠️ No zero-shot classification model found, using fallback")
                    return []
                
                logger.debug(f"✅ Using {zero_shot_model} for semantic classification")
                
                # Classify message against each crisis category
                for category, category_info in crisis_categories.items():
                    try:
                        # Perform zero-shot classification
                        hypothesis = category_info['hypothesis_template']
                        
                        # Use the model for natural language inference
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
        """
        Perform zero-shot classification using the loaded model
        
        Args:
            message: Text to classify
            hypothesis: Hypothesis to test against
            model_type: Type of model to use  
            models_manager: Model manager instance
            
        Returns:
            Classification confidence score (0.0 to 1.0)
        """
        try:
            # This is where you'd integrate with your actual model pipeline
            # For now, we'll use a placeholder that demonstrates the concept
            
            # Example of what the real implementation would look like:
            # model_config = models_manager.get_model_config(model_type)
            # model_name = model_config.get('name')
            # pipeline = transformers.pipeline('zero-shot-classification', model=model_name)
            # result = pipeline(message, [hypothesis])
            # return result['scores'][0]
            
            # Placeholder implementation for demonstration
            return self._demo_classification(message, hypothesis)
            
        except Exception as e:
            logger.error(f"❌ Error in model classification: {e}")
            return 0.0

    def _demo_classification(self, message: str, hypothesis: str) -> float:
        """
        Demo classification logic - REPLACE with actual model calls
        
        This demonstrates the concept and provides reasonable results for testing.
        Replace this with actual zero-shot model integration.
        """
        message_lower = message.lower()
        
        # Simple semantic matching for demonstration
        if "suicide" in hypothesis.lower() or "not wanting to live" in hypothesis.lower():
            # Check for suicidal ideation patterns
            suicide_indicators = [
                "don't want to live", "do not want to live", "dont want to live",
                "want to die", "ready to die", "end my life", "kill myself",
                "suicide", "not worth living", "better off dead",
                "continue living", "keep living", "stay alive"
            ]
            
            # Check for negation patterns (don't want to...)
            negation_patterns = ["don't want", "do not want", "dont want"]
            life_patterns = ["live", "living", "continue", "stay alive", "be alive"]
            
            has_negation = any(neg in message_lower for neg in negation_patterns)
            has_life_ref = any(life in message_lower for life in life_patterns)
            
            if has_negation and has_life_ref:
                return 0.85  # High confidence for "don't want to live" type messages
                
            # Check for direct suicide indicators
            direct_matches = sum(1 for indicator in suicide_indicators if indicator in message_lower)
            if direct_matches > 0:
                return 0.75
        
        elif "hopeless" in hypothesis.lower():
            # Check for hopelessness patterns
            hopeless_indicators = [
                "hopeless", "no hope", "despair", "desperate", "pointless",
                "meaningless", "nothing matters", "give up", "giving up"
            ]
            
            matches = sum(1 for indicator in hopeless_indicators if indicator in message_lower)
            if matches > 0:
                return 0.80
        
        elif "distress" in hypothesis.lower():
            # Check for severe distress patterns
            distress_indicators = [
                "overwhelming", "can't cope", "breaking down", "falling apart",
                "drowning", "suffocating", "crushing", "unbearable"
            ]
            
            matches = sum(1 for indicator in distress_indicators if indicator in message_lower)
            if matches > 0:
                return 0.70
        
        return 0.0  # No semantic match

    def _find_patterns_enhanced_fallback(self, message: str) -> List[Dict[str, Any]]:
        """
        Enhanced fallback pattern matching when semantic classification isn't available
        
        This provides improved keyword-based detection with better coverage than
        the original exact phrase matching.
        """
        try:
            triggered_patterns = []
            message_lower = message.lower()
            
            logger.debug(f"🔍 Enhanced fallback pattern matching for: '{message[:50]}...'")
            
            # Enhanced keyword patterns with better coverage
            pattern_categories = {
                'suicidal_ideation': {
                    'patterns': [
                        # Direct expressions
                        "want to die", "ready to die", "going to die", "wish i was dead",
                        "better off dead", "end my life", "kill myself", "commit suicide",
                        
                        # Negation patterns (key improvement)
                        "don't want to live", "do not want to live", "dont want to live",
                        "don't want to be alive", "do not want to be alive", "dont want to be alive",
                        "don't want to continue", "do not want to continue", "dont want to continue",
                        "can't go on", "cannot go on", "cant go on",
                        
                        # Indirect expressions
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
            
            # Check each category
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
                        break  # Only trigger once per category
            
            return triggered_patterns
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced fallback matching: {e}")
            return []
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of crisis pattern manager with v3.1 information
        
        Returns:
            Dictionary containing manager status and loaded patterns info
        """
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
    
    # ========================================================================
    # v3.1 ENHANCED PATTERN ANALYSIS - Updated for v3.1 JSON Compatibility
    # ========================================================================
    
    def analyze_enhanced_patterns(self, message: str) -> Dict[str, Any]:
        """
        Analyze enhanced crisis patterns with v3.1 JSON compatibility and advanced matching logic
        
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
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary with v3.1 compliance status
        
        Returns:
            Dictionary with configuration details and v3.1 compliance info
        """
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            metadata = enhanced_patterns.get('_metadata', {})
            
            return {
                'manager_version': 'v3.1-hybrid',
                'json_configuration_version': metadata.get('configuration_version', 'unknown'),
                'json_compliance': metadata.get('compliance', 'unknown'),
                'last_updated': metadata.get('updated_date', 'unknown'),
                'safety_notice': metadata.get('safety_notice', 'Crisis detection system'),
                'patterns_loaded': len(self._patterns_cache),
                'pattern_types': list(self._patterns_cache.keys()),
                'enhanced_patterns_available': 'enhanced_crisis_patterns' in self._patterns_cache,
                'critical_categories_available': self._get_critical_categories_status(),
                'regex_cache_size': len(self._compiled_regex_cache),
                'processing_features': {
                    'semantic_classification': True,
                    'enhanced_fallback': True,
                    'temporal_analysis': True,
                    'community_patterns': True,
                    'context_analysis': True,
                    'safety_escalation': True
                },
                'manager_initialized': True,
                'v3.1_features': {
                    'metadata_tracking': bool(metadata),
                    'environment_variable_support': True,
                    'safety_flags': True,
                    'escalation_rules': True,
                    'processing_rules': True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting configuration summary: {e}")
            return {
                'manager_version': 'v3.1-hybrid',
                'error': str(e),
                'manager_initialized': False
            }
    
    def _get_critical_categories_status(self) -> Dict[str, bool]:
        """Check availability of critical pattern categories"""
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            patterns = enhanced_patterns.get('patterns', {})
            
            critical_categories = [
                'hopelessness_patterns',
                'planning_indicators', 
                'method_references',
                'isolation_patterns'
            ]
            
            return {category: category in patterns for category in critical_categories}
            
        except Exception as e:
            logger.error(f"❌ Error checking critical categories: {e}")
            return {}
    
    def validate_enhanced_patterns_config(self) -> Dict[str, Any]:
        """
        Validate enhanced patterns configuration for v3.1 compliance
        
        Returns:
            Dictionary with validation results
        """
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            errors = []
            warnings = []
            
            # Check v3.1 compliance
            metadata = enhanced_patterns.get('_metadata', {})
            if not metadata:
                errors.append("Missing _metadata section - not v3.1 compliant")
            else:
                config_version = metadata.get('configuration_version', '')
                if not config_version.startswith('3d.'):
                    warnings.append(f"Configuration version '{config_version}' may not be v3.1 compliant")
            
            # Check required sections
            required_sections = ['patterns', 'processing_rules', 'escalation_rules']
            for section in required_sections:
                if section not in enhanced_patterns:
                    errors.append(f"Missing required section: {section}")
            
            # Check critical pattern categories
            patterns = enhanced_patterns.get('patterns', {})
            critical_categories = ['hopelessness_patterns', 'planning_indicators', 'method_references']
            missing_critical = [cat for cat in critical_categories if cat not in patterns]
            
            if missing_critical:
                errors.append(f"Missing critical pattern categories: {missing_critical}")
            
            # Check processing rules
            processing_rules = enhanced_patterns.get('processing_rules', {})
            if 'defaults' not in processing_rules:
                warnings.append("Missing defaults in processing_rules")
            
            # Check escalation rules
            escalation_rules = enhanced_patterns.get('escalation_rules', {})
            if 'emergency_response_threshold' not in escalation_rules:
                warnings.append("Missing emergency_response_threshold in escalation_rules")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'v3_1_compliant': len(errors) == 0 and bool(metadata),
                'critical_categories_available': len(missing_critical) == 0,
                'validation_timestamp': time.time()
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
            
        except Exception as e:
            logger.error(f"❌ Error validating enhanced patterns config: {e}")
            return {
                'valid': False,
                'errors': [f"Validation failed: {str(e)}"],
                'warnings': [],
                'v3_1_compliant': False,
                'validation_timestamp': time.time()
            }