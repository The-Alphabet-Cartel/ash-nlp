# ash-nlp/managers/pattern_detection_manager.py
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
Crisis Pattern Manager for Ash NLP Service - OPTIMIZED
---
FILE VERSION: v3.1-3e-6-3
LAST MODIFIED: 2025-08-22
PHASE: 3e Sub-step 5.3 - PatternDetectionManager cleanup + optimization
CLEAN ARCHITECTURE: v3.1 Compliant
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
from managers.unified_config import UnifiedConfigManager, create_unified_config_manager
from managers.helpers.pattern_detection_helper import CrisisPatternHelper, create_pattern_detection_helper

logger = logging.getLogger(__name__)

class PatternDetectionManager:
    """
    Crisis Pattern Manager with consolidated context pattern support and v3.1 JSON compatibility
    
    Features:
    - Enhanced crisis pattern detection with immediate escalation
    - Consolidated context pattern management (crisis_context + positive_context + context_weights)
    - Advanced pattern matching with context validation
    - Temporal indicators for time-sensitive crisis detection
    - Community-specific vocabulary and context patterns
    - Production-ready error handling and resilience
    - v3.1 JSON configuration compatibility
    - Phase 3e: Clean architecture with optimized organization
    
    CRITICAL: This manager detects life-threatening situations requiring immediate response.
    """
    
    def __init__(self, config_manager: UnifiedConfigManager):
        """
        Initialize Crisis Pattern Manager with v3.1 compatibility and context consolidation
        
        Args:
            config_manager: UnifiedConfigManager instance for configuration access
        """
        self.config_manager = config_manager
        self._patterns_cache = {}
        self._compiled_regex_cache = {}
        
        # Initialize helper methods
        self._helpers = create_pattern_detection_helper(config_manager)
        
        logger.info("PatternDetectionManager v3.1-3e-5.3-optimized initializing...")
        self._load_all_patterns()
        logger.info(f"PatternDetectionManager initialized with {len(self._patterns_cache)} pattern sets")

    def _load_all_patterns(self) -> None:
        """Load all crisis pattern configurations with v3.1 consolidation support"""
        pattern_files = [
            'patterns_context',
            'patterns_temporal',
            'patterns_community',
            'patterns_crisis',
            'patterns_idiom',
            'patterns_burden',
        ]
        
        for pattern_type in pattern_files:
            try:
                patterns = self.config_manager.get_patterns_crisis(pattern_type)
                if patterns:
                    self._patterns_cache[pattern_type] = patterns
                    logger.debug(f"Loaded {pattern_type}: {len(patterns.get('patterns', {}) if isinstance(patterns.get('patterns'), dict) else patterns)} pattern groups")
                else:
                    logger.warning(f"No patterns found for {pattern_type}")
            except Exception as e:
                logger.error(f"Failed to load {pattern_type}: {e}")
                self._patterns_cache[pattern_type] = {}

    # ========================================================================
    # ENHANCED PATTERNS ACCESS - v3.1 Compatible
    # ========================================================================
    
    def get_enhanced_patterns(self) -> Dict[str, Any]:
        """Get enhanced crisis patterns with v3.1 JSON compatibility"""
        return self._patterns_cache.get('patterns_crisis', {})

    def analyze_enhanced_patterns(self, message: str) -> Dict[str, Any]:
        """Analyze enhanced crisis patterns with v3.1 JSON compatibility"""
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
            
            # Get processing configuration with v3.1 fallbacks and safe type conversion
            case_sensitive = self._helpers.safe_get_bool(processing_rules, 'case_sensitive', defaults.get('case_sensitive', False))
            context_window = self._helpers.safe_get_int(processing_rules, 'context_window', defaults.get('context_window', 10))
            max_pattern_boost = self._helpers.safe_get_float(processing_rules, 'max_pattern_boost', defaults.get('max_pattern_boost', 0.50))
            
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
            
            # Check emergency response threshold with more aggressive defaults
            emergency_threshold = self._helpers.safe_get_float(escalation_rules, 'emergency_response_threshold', 
                                                     escalation_rules.get('defaults', {}).get('emergency_response_threshold', 0.60))
            
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
    # CONTEXT PATTERN METHODS - UPDATED FOR PHASE 3e
    # ========================================================================

    def apply_context_weights(self, message: str, base_crisis_score: float) -> Tuple[float, Dict[str, Any]]:
        """Apply context weights to modify crisis score - Updated for Phase 3e with existing environment variables"""
        try:
            # Get context weights from consolidated patterns
            context_weights = self.get_context_weights()
            if not context_weights:
                logger.debug("No context weights available - returning base score")
                return base_crisis_score, {'weights_applied': [], 'total_adjustment': 0.0}
            
            message_lower = message.lower()
            weights_applied = []
            total_adjustment = 0.0
            
            # Use existing environment variables instead of undefined ones
            try:
                context_boost_weight = float(self.config_manager.get_env('NLP_ANALYSIS_CONTEXT_BOOST_WEIGHT', 1.5))
                crisis_base_weight = context_boost_weight * 0.1
                crisis_multiplier = float(self.config_manager.get_env('NLP_CONFIG_CRISIS_CONTEXT_BOOST_MULTIPLIER', 1.0))
                max_boost = crisis_base_weight * crisis_multiplier * 2.0
                
            except Exception as e:
                logger.warning(f"Error reading existing environment variables: {e}, using safe defaults")
                crisis_base_weight = 0.15
                max_boost = 0.35
            
            # Apply crisis amplifier weights
            crisis_words = context_weights.get('crisis_context_words', {})
            if crisis_words and 'words' in crisis_words:
                amplifier_words = crisis_words.get('words', [])
                
                for word in amplifier_words:
                    if isinstance(word, str) and word.lower() in message_lower:
                        adjustment = min(crisis_base_weight, max_boost - total_adjustment)
                        if adjustment > 0:
                            total_adjustment += adjustment
                            weights_applied.append({
                                'word': word,
                                'type': 'crisis_amplifier',
                                'adjustment': adjustment,
                                'weight': crisis_base_weight,
                                'source': 'existing_env_vars'
                            })
            
            # Apply positive reducer weights
            positive_words = context_weights.get('positive_context_words', {})
            if positive_words and 'words' in positive_words:
                reducer_words = positive_words.get('words', [])
                positive_base_weight = -0.10
                max_reduction = -0.30
                
                for word in reducer_words:
                    if isinstance(word, str) and word.lower() in message_lower:
                        adjustment = max(positive_base_weight, max_reduction - total_adjustment)
                        if adjustment < 0:
                            total_adjustment += adjustment
                            weights_applied.append({
                                'word': word,
                                'type': 'positive_reducer',
                                'adjustment': adjustment,
                                'weight': positive_base_weight,
                                'source': 'safe_defaults'
                            })
            
            # Additional context boost from hopelessness detection
            if any(word in message_lower for word in ['hopeless', 'hope', 'despair', 'desperate']):
                try:
                    enhanced_weight = float(self.config_manager.get_env('NLP_CONFIG_ENHANCED_CRISIS_WEIGHT', 1.2))
                    hopelessness_boost = (enhanced_weight - 1.0) * 0.2
                    if hopelessness_boost > 0:
                        total_adjustment += hopelessness_boost
                        weights_applied.append({
                            'word': 'hopelessness_context',
                            'type': 'enhanced_crisis_boost',
                            'adjustment': hopelessness_boost,
                            'weight': enhanced_weight,
                            'source': 'NLP_CONFIG_ENHANCED_CRISIS_WEIGHT'
                        })
                except Exception as e:
                    logger.warning(f"Error applying enhanced crisis weight: {e}")
            
            # Calculate final score with bounds checking
            modified_score = max(0.0, min(1.0, base_crisis_score + total_adjustment))
            
            analysis_details = {
                'weights_applied': weights_applied,
                'total_adjustment': total_adjustment,
                'base_score': base_crisis_score,
                'modified_score': modified_score,
                'crisis_words_found': len([w for w in weights_applied if w['type'] == 'crisis_amplifier']),
                'positive_words_found': len([w for w in weights_applied if w['type'] == 'positive_reducer']),
                'enhanced_boosts': len([w for w in weights_applied if w['type'] == 'enhanced_crisis_boost']),
                'source': 'existing_environment_variables',
                'uses_new_env_vars': False,
                'reuses_existing_infrastructure': True,
                'phase_3e_compliant': True
            }
            
            if total_adjustment != 0:
                logger.info(f"Context weights (using existing env vars): {base_crisis_score:.3f} → {modified_score:.3f} (Δ{total_adjustment:+.3f})")
            
            return modified_score, analysis_details
            
        except Exception as e:
            logger.error(f"Error applying context weights: {e}")
            return base_crisis_score, {'error': str(e), 'weights_applied': [], 'total_adjustment': 0.0}

    def check_patterns_crisis(self, message: str) -> Dict[str, Any]:
        """Check for enhanced crisis patterns - Updated for Phase 3e consolidation"""
        try:
            enhanced_analysis = self.analyze_enhanced_patterns(message)
            
            if not enhanced_analysis or 'patterns_found' not in enhanced_analysis:
                return {
                    'matches': [],
                    'highest_urgency': 'none',
                    'auto_escalate': False,
                    'total_weight': 0.0,
                    'requires_immediate_attention': False,
                    'confidence_score': 0.0
                }
            
            patterns_found = enhanced_analysis.get('patterns_found', [])
            safety_flags = enhanced_analysis.get('safety_flags', {})
            
            # Convert to community pattern format
            matches = []
            for pattern in patterns_found:
                matches.append({
                    'pattern_name': pattern.get('pattern_name', ''),
                    'pattern_group': pattern.get('pattern_group', ''),
                    'crisis_level': pattern.get('crisis_level', 'medium'),
                    'urgency': pattern.get('urgency', 'medium'),
                    'weight': pattern.get('weight', 0.7),
                    'confidence': pattern.get('confidence', 0.7),
                    'auto_escalate': pattern.get('auto_escalate', False),
                    'matched_text': pattern.get('matched_text', ''),
                    'pattern_type': pattern.get('pattern_type', 'enhanced'),
                    'phase_3e_updated': True
                })
            
            # Determine highest urgency
            urgency_levels = [m.get('urgency', 'none') for m in matches]
            urgency_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'none': 0}
            highest_urgency = 'none'
            if urgency_levels:
                highest_urgency = max(urgency_levels, key=lambda x: urgency_priority.get(x, 0))
            
            # Check auto-escalation and immediate attention requirements
            auto_escalate = any(m.get('auto_escalate', False) for m in matches)
            total_weight = sum(m.get('weight', 0.0) for m in matches)
            requires_immediate_attention = (
                safety_flags.get('emergency_response_triggered', False) or
                safety_flags.get('immediate_intervention_patterns', []) or
                highest_urgency == 'critical' or
                any(m.get('crisis_level') == 'critical' for m in matches)
            )
            
            result = {
                'matches': matches,
                'highest_urgency': highest_urgency,
                'auto_escalate': auto_escalate,
                'total_weight': total_weight,
                'requires_immediate_attention': requires_immediate_attention,
                'confidence_score': enhanced_analysis.get('confidence_score', 0.0),
                'safety_flags': safety_flags,
                'critical_patterns_count': len(safety_flags.get('critical_patterns_detected', [])),
                'source': 'analyze_enhanced_patterns_v3.1_phase_3e',
                'phase_3e_migration_complete': True
            }
            
            if matches:
                logger.info(f"Enhanced crisis patterns check: {len(matches)} matches, urgency: {highest_urgency}")
            
            return result
            
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

    # ========================================================================
    # CONSOLIDATED CONTEXT PATTERN ACCESS METHODS
    # ========================================================================
    
    def get_consolidated_patterns_context(self) -> Dict[str, Any]:
        """Get consolidated context patterns"""
        return self._patterns_cache.get('patterns_context', {})
    
    def get_patterns_context(self) -> Dict[str, Any]:
        """Get crisis context patterns that amplify crisis detection"""
        consolidated = self.get_consolidated_patterns_context()
        if consolidated and 'crisis_amplification_patterns' in consolidated:
            return {
                'patterns': consolidated['crisis_amplification_patterns'],
                'configuration': consolidated.get('configuration', {}),
                'processing_rules': consolidated.get('processing_rules', {}),
                '_metadata': consolidated.get('_metadata', {}),
                'source': 'consolidated_patterns_context'
            }

        logger.warning("⚠️ Context patterns not found ...")
        return {
            'patterns': 'Not Found!',
            'configuration': 'Not Found!'
        }
    
    def get_positive_patterns(self) -> Dict[str, Any]:
        """Get positive context patterns that reduce false positives"""
        consolidated = self.get_consolidated_patterns_context()
        if consolidated and 'positive_reduction_patterns' in consolidated:
            return {
                'patterns': consolidated['positive_reduction_patterns'],
                'configuration': consolidated.get('configuration', {}),
                'processing_rules': consolidated.get('processing_rules', {}),
                '_metadata': consolidated.get('_metadata', {}),
                'source': 'consolidated_patterns_context'
            }

        logger.warning("⚠️ Positive patterns not found ...")
        return {
            'patterns': 'Not Found!',
            'configuration': 'Not Found!'
        }
    
    def get_context_weights(self) -> Dict[str, Any]:
        """Get context weight multipliers for pattern matching"""
        consolidated = self.get_consolidated_patterns_context()
        if consolidated:
            weights = {
                'crisis_context_words': {},
                'positive_context_words': {},
                'configuration': consolidated.get('configuration', {}),
                'processing_rules': consolidated.get('processing_rules', {}),
                '_metadata': consolidated.get('_metadata', {}),
                'source': 'consolidated_patterns_context'
            }
            
            # Extract crisis amplifier words
            crisis_amp = consolidated.get('crisis_amplification_patterns', {})
            if 'crisis_amplifier_words' in crisis_amp:
                amplifier_data = crisis_amp['crisis_amplifier_words']
                weights['crisis_context_words'] = {
                    'weight_type': 'crisis_amplifier',
                    'base_weight': amplifier_data.get('base_weight', 0.10),
                    'max_cumulative_boost': amplifier_data.get('max_cumulative_boost', 0.30),
                    'words': amplifier_data.get('words', [])
                }
            
            # Extract positive reducer words
            positive_red = consolidated.get('positive_reduction_patterns', {})
            if 'positive_reducer_words' in positive_red:
                reducer_data = positive_red['positive_reducer_words']
                weights['positive_context_words'] = {
                    'weight_type': 'crisis_reducer',
                    'base_weight': reducer_data.get('base_weight', -0.08),
                    'max_cumulative_reduction': reducer_data.get('max_cumulative_reduction', -0.25),
                    'words': reducer_data.get('words', [])
                }
            
            return weights

        logger.warning("⚠️ Context weights not found ...")
        return {
            'patterns': 'Not Found!',
            'configuration': 'Not Found!'
        }
    
    # ========================================================================
    # CORE PATTERN ACCESS METHODS - Backward Compatibility
    # ========================================================================
    
    def get_patterns_crisis(self) -> List[Dict[str, Any]]:
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

    def get_temporal_indicators(self) -> Dict[str, Any]:
        """Get temporal indicator patterns for time-based crisis modification"""
        return self._patterns_cache.get('patterns_temporal', {})
    
    def get_community_vocabulary(self) -> Dict[str, Any]:
        """Get community-specific vocabulary patterns"""
        return self._patterns_cache.get('patterns_community', {})
    
    def get_idiom_patterns(self) -> Dict[str, Any]:
        """Get idiom-based crisis patterns"""
        return self._patterns_cache.get('patterns_idiom', {})
    
    def get_burden_patterns(self) -> Dict[str, Any]:
        """Get burden and stress-related patterns"""
        return self._patterns_cache.get('patterns_burden', {})
    
    # ========================================================================
    # PATTERN EXTRACTION METHODS - Using Helpers
    # ========================================================================

    def extract_community_patterns(self, message: str) -> List[Dict[str, Any]]:
        """Extract community-specific patterns from message using helper methods"""
        return self._helpers.extract_community_patterns(message, self._patterns_cache)

    def extract_crisis_context_phrases(self, message: str) -> List[Dict[str, Any]]:
        """Extract crisis context phrases using helper methods"""
        return self._helpers.extract_crisis_context_phrases(message, self._patterns_cache)

    def analyze_temporal_indicators(self, message: str) -> Dict[str, Any]:
        """Analyze temporal indicators using helper methods"""
        return self._helpers.analyze_temporal_indicators(message, self._patterns_cache)

    # ========================================================================
    # COMPREHENSIVE MESSAGE ANALYSIS - Updated for Phase 3e
    # ========================================================================

    def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict[str, Any]:
        """Comprehensive message analysis with Phase 3e enhanced safety features"""
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
            
            logger.debug(f"🔍 Starting comprehensive Phase 3e analysis for message (length: {len(message)})")
            
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
                            'details': pattern,
                            'phase_3e_analysis': True
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
                            'details': pattern,
                            'phase_3e_analysis': True
                        })
                analysis_result['details']['community_patterns'] = community_patterns
            except Exception as e:
                logger.warning(f"⚠️ Community patterns analysis failed: {e}")
                analysis_result['details']['community_patterns'] = {'error': str(e)}
            
            # Context phrases analysis (now uses consolidated patterns)
            try:
                context_phrases = self.extract_crisis_context_phrases(message)
                if context_phrases:
                    for phrase in context_phrases:
                        analysis_result['patterns_triggered'].append({
                            'pattern_name': f"context_{phrase.get('phrase_type', 'unknown')}",
                            'pattern_type': 'context_phrase',
                            'crisis_level': phrase.get('crisis_level', 'low'),
                            'confidence': phrase.get('confidence', 0.5),
                            'details': phrase,
                            'phase_3e_analysis': True
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
                            'details': indicator,
                            'phase_3e_analysis': True
                        }
                        analysis_result['patterns_triggered'].append(pattern_data)
                        
                        # Check for immediate intervention based on temporal urgency
                        if indicator.get('time_sensitivity') in ['immediate', 'critical']:
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
                    'manager_version': 'v3.1-3e-5.3-optimized-1',
                    'safety_analysis_version': 'v3.1_phase_3e',
                    'v3_1_features_used': True,
                    'context_consolidation': True,
                    'community_pattern_consolidation': True,
                    'phase_3e_migration_complete': True,
                    'optimized_architecture': True
                }
            })
            
            # Log safety-critical results with appropriate severity
            if analysis_result['safety_assessment']['immediate_intervention_required']:
                logger.critical(f"🚨 IMMEDIATE INTERVENTION REQUIRED - User: {user_id}, Channel: {channel_id}")
            elif analysis_result['safety_assessment']['emergency_response_recommended']:
                logger.error(f"⚠️ EMERGENCY RESPONSE RECOMMENDED - Highest level: {highest_level}, User: {user_id}")
            elif highest_level in ['high', 'medium']:
                logger.warning(f"⚠️ Crisis patterns detected - Level: {highest_level}, Count: {pattern_count}, User: {user_id}")
            
            logger.debug(f"✅ Phase 3e crisis analysis complete: {pattern_count} patterns, level: {highest_level}")
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
                    'manager_version': 'v3.1-3e-5.3-optimized-1',
                    'phase_3e_migration_complete': True,
                    'optimized_architecture': True
                }
            }

    # ========================================================================
    # SEMANTIC PATTERN ANALYSIS - Using Helpers
    # ========================================================================

    def find_triggered_patterns(self, message: str, model_coordination_manager=None) -> List[Dict[str, Any]]:
        """Find triggered crisis patterns using semantic NLP classification"""
        try:
            if model_coordination_manager:
                semantic_patterns = self._helpers.find_patterns_semantic(message, model_coordination_manager)
                if semantic_patterns:
                    logger.info(f"✅ Semantic classification found {len(semantic_patterns)} patterns")
                    return semantic_patterns
            
            logger.info("🔥 Using enhanced pattern matching fallback")
            return self._helpers.find_patterns_enhanced_fallback(message)
            
        except Exception as e:
            logger.error(f"❌ Error in find_triggered_patterns: {e}")
            return []
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status of crisis pattern manager with Phase 3e optimization info"""
        try:
            enhanced_patterns = self.get_enhanced_patterns()
            metadata = enhanced_patterns.get('_metadata', {})
            
            # Check consolidation status
            has_consolidated_context = 'patterns_context' in self._patterns_cache
            has_legacy_context_files = any(f in self._patterns_cache for f in 
                ['patterns_context', 'positive_patterns', 'context_weights_patterns'])
            has_legacy_community_files = any(f in self._patterns_cache for f in
                ['crisis_lgbtqia_patterns', 'patterns_community'])
            
            return {
                'status': 'operational',
                'patterns_loaded': len(self._patterns_cache),
                'pattern_types': list(self._patterns_cache.keys()),
                'cache_size': len(self._compiled_regex_cache),
                'version': 'v3.1-3e-5.3-optimized-1',
                'config_manager': 'UnifiedConfigManager',
                'optimization_status': {
                    'helper_extraction_complete': True,
                    'migration_references_consolidated': True,
                    'estimated_line_reduction': '~610 lines',
                    'target_line_count': '~790 lines',
                    'helper_file': 'pattern_detection_helpers.py'
                },
                'phase_3e_status': {
                    'sub_step': '5.3',
                    'migration_complete': True,
                    'methods_migrated': 5,
                    'migration_handler': 'consolidated',
                    'shared_utilities_integration': True,
                    'learning_system_integration': True,
                    'helper_methods_extracted': True
                },
                'v3_1_compliance': {
                    'json_version': metadata.get('configuration_version', 'unknown'),
                    'compliance_status': metadata.get('compliance', 'unknown'),
                    'metadata_available': bool(metadata),
                    'safety_features_enabled': True
                },
                'consolidation_status': {
                    'context_consolidation_active': has_consolidated_context,
                    'legacy_context_files_present': has_legacy_context_files,
                    'context_consolidation_complete': has_consolidated_context and not has_legacy_context_files,
                    'community_consolidation_complete': not has_legacy_community_files,
                    'community_pattern_methods_consolidated': True,
                    'files_eliminated_context': 3 if has_consolidated_context else 0,
                    'files_eliminated_community': 2,
                    'total_files_eliminated': (3 if has_consolidated_context else 0) + 2,
                    'pattern_ecosystem_files': len([f for f in self._patterns_cache.keys() 
                                                  if not f.startswith('crisis_context') and 
                                                     not f.startswith('positive_context') and 
                                                     not f.startswith('context_weights') and
                                                     not f == 'crisis_lgbtqia_patterns' and
                                                     not f == 'patterns_community'])
                },
                'pattern_files_status': {
                    'v3_1_compliant': [
                        'patterns_community',
                        'patterns_temporal',
                        'patterns_crisis',
                        'patterns_idiom',
                        'patterns_burden'
                    ],
                    'consolidated': [
                        'patterns_context'
                    ],
                },
                'phase_3e_consolidated_migration_handler': {
                    'validate_pattern_structure': 'SharedUtilitiesManager.validate_data_structure()',
                    'format_pattern_output': 'SharedUtilitiesManager.format_response_data()',
                    'log_pattern_performance': 'SharedUtilitiesManager.log_performance_metric()',
                    'update_pattern_from_feedback': 'LearningSystemManager.update_patterns_from_feedback()',
                    'evaluate_pattern_effectiveness': 'LearningSystemManager.evaluate_pattern_performance()'
                },
                'safety_features': {
                    'immediate_intervention_detection': True,
                    'auto_escalation_support': True,
                    'emergency_response_triggers': True,
                    'critical_pattern_monitoring': True,
                    'community_pattern_integration': True,
                    'phase_3e_enhanced_safety': True,
                    'optimized_performance': True
                }
            }
        except Exception as e:
            logger.error(f"❌ Error getting status: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'version': 'v3.1-3e-5.3-optimized-1'
            }


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_pattern_detection_manager(config_manager: UnifiedConfigManager) -> PatternDetectionManager:
    """
    Factory function to create PatternDetectionManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        PatternDetectionManager instance with Phase 3e optimization and migration references
    """
    return PatternDetectionManager(config_manager)

__all__ = ['PatternDetectionManager', 'create_pattern_detection_manager']

logger.info("✅ PatternDetectionManager v3.1-3e-5.3-optimized loaded - Hybrid optimization complete!")