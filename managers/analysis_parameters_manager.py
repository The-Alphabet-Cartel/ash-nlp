#!/usr/bin/env python3
"""
Analysis Parameters Manager for Ash NLP Service
FILE VERSION: v3.1-3d-10-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalysisParametersManager:
    """
    Analysis Parameters Manager with Phase 3d functionality and v3.1 JSON compatibility
    
    Hybrid approach: Preserves all current enhanced functionality while ensuring
    compatibility with Clean v3.1 JSON configuration standards.
    
    REMOVED: Duplicate ensemble weight variables (now handled by ModelEnsembleManager)
    ADDED: v3.1 JSON compatibility and contextual weighting support
    """
    
    def __init__(self, config_manager):
        """
        Initialize Analysis Parameters Manager
        
        Args:
            config_manager: UnifiedConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for AnalysisParametersManager")
        
        self.config_manager = config_manager
        self.analysis_config = {}
        self._full_config = {}
        
        logger.info("✅ AnalysisParametersManager v3.1d initialized - Phase 3d + v3.1 compatibility")
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self):
        """Load analysis parameters configuration with v3.1 compatibility"""
        try:
            # Load analysis parameters via UnifiedConfigManager
            analysis_config_raw = self.config_manager.load_config_file('analysis_parameters')
            
            if not analysis_config_raw:
                logger.error("❌ Could not load analysis_parameters.json configuration")
                raise ValueError("Analysis parameters configuration not available")
            
            # Extract analysis system configuration (backward compatibility)
            self.analysis_config = analysis_config_raw.get("analysis_system", {})
            
            # Store the full configuration for access by parameter methods
            self._full_config = analysis_config_raw
            
            # Log v3.1 metadata if available
            metadata = self._full_config.get('_metadata', {})
            config_version = metadata.get('configuration_version', 'unknown')
            compliance = metadata.get('compliance', 'unknown')
            
            logger.info("✅ Analysis parameters loaded from JSON configuration with environment overrides")
            logger.debug(f"📋 Configuration version: {config_version}")
            logger.debug(f"🏗️ Compliance: {compliance}")
            logger.debug(f"🔧 Architecture: {self.analysis_config.get('architecture', 'v3.1-hybrid')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load analysis parameters: {e}")
            raise ValueError(f"Analysis parameters configuration error: {e}")
    
    # ========================================================================
    # CRISIS THRESHOLDS - Core Algorithm Configuration
    # ========================================================================
    
    def get_crisis_thresholds(self) -> Dict[str, float]:
        """
        Get crisis threshold settings for analysis algorithms
        
        NOTE: Primary thresholds managed by ThresholdMappingManager in Phase 3c.
        These are fallback/secondary thresholds for specific analysis components.
        
        Returns:
            Dictionary with high, medium, low thresholds
        """
        try:
            thresholds_config = self._full_config.get('crisis_thresholds', {})
            defaults = thresholds_config.get('defaults', {})
            
            # Extract thresholds with environment variable support and v3.1 compatibility
            thresholds = {
                'high': float(thresholds_config.get('high', defaults.get('high', 0.55))),
                'medium': float(thresholds_config.get('medium', defaults.get('medium', 0.28))),
                'low': float(thresholds_config.get('low', defaults.get('low', 0.16)))
            }
            
            # Validate threshold ordering
            if not (thresholds['high'] > thresholds['medium'] > thresholds['low']):
                logger.warning(f"⚠️ Invalid threshold ordering: {thresholds}")
                logger.warning("🔧 Using default thresholds")
                return {'high': 0.55, 'medium': 0.28, 'low': 0.16}
            
            logger.debug(f"✅ Crisis thresholds: {thresholds}")
            return thresholds
            
        except Exception as e:
            logger.error(f"❌ Error loading crisis thresholds: {e}")
            # Return safe defaults
            return {'high': 0.55, 'medium': 0.28, 'low': 0.16}
    
    # ========================================================================
    # CONFIDENCE BOOST PARAMETERS - Core Algorithm Configuration
    # ========================================================================
    
    def get_confidence_boost_parameters(self) -> Dict[str, float]:
        """
        Get confidence boost parameters for analysis algorithms
        
        Returns:
            Dictionary with confidence boost settings
        """
        try:
            boost_config = self._full_config.get('confidence_boost', {})
            defaults = boost_config.get('defaults', {})
            
            return {
                'high_confidence_boost': float(boost_config.get('high_confidence_boost', defaults.get('high_confidence_boost', 0.15))),
                'medium_confidence_boost': float(boost_config.get('medium_confidence_boost', defaults.get('medium_confidence_boost', 0.10))),
                'low_confidence_boost': float(boost_config.get('low_confidence_boost', defaults.get('low_confidence_boost', 0.05))),
                'pattern_confidence_boost': float(boost_config.get('pattern_confidence_boost', defaults.get('pattern_confidence_boost', 0.05))),
                'model_confidence_boost': float(boost_config.get('model_confidence_boost', defaults.get('model_confidence_boost', 0.0)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading confidence boost parameters: {e}")
            return {
                'high_confidence_boost': 0.15,
                'medium_confidence_boost': 0.10,
                'low_confidence_boost': 0.05,
                'pattern_confidence_boost': 0.05,
                'model_confidence_boost': 0.0
            }
    
    # ========================================================================
    # PHRASE EXTRACTION PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_phrase_extraction_parameters(self) -> Dict[str, Any]:
        """
        Get phrase extraction parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with phrase extraction settings
        """
        try:
            phrase_config = self._full_config.get('phrase_extraction', {})
            defaults = phrase_config.get('defaults', {})
            
            return {
                'min_phrase_length': int(phrase_config.get('min_phrase_length', defaults.get('min_phrase_length', 3))),
                'max_phrase_length': int(phrase_config.get('max_phrase_length', defaults.get('max_phrase_length', 6))),
                'crisis_focus': phrase_config.get('crisis_focus', defaults.get('crisis_focus', True)),
                'community_specific': phrase_config.get('community_specific', defaults.get('community_specific', True)),
                'min_confidence': float(phrase_config.get('min_confidence', defaults.get('min_confidence', 0.3))),
                'max_results': int(phrase_config.get('max_results', defaults.get('max_results', 20)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading phrase extraction parameters: {e}")
            return {
                'min_phrase_length': 3,
                'max_phrase_length': 6,
                'crisis_focus': True,
                'community_specific': True,
                'min_confidence': 0.3,
                'max_results': 20
            }
    
    # ========================================================================
    # PATTERN LEARNING PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_pattern_learning_parameters(self) -> Dict[str, Any]:
        """
        Get pattern learning parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with pattern learning settings
        """
        try:
            learning_config = self._full_config.get('pattern_learning', {})
            defaults = learning_config.get('defaults', {})
            
            return {
                'min_crisis_messages': int(learning_config.get('min_crisis_messages', defaults.get('min_crisis_messages', 10))),
                'max_phrases_to_analyze': int(learning_config.get('max_phrases_to_analyze', defaults.get('max_phrases_to_analyze', 200))),
                'min_distinctiveness_ratio': float(learning_config.get('min_distinctiveness_ratio', defaults.get('min_distinctiveness_ratio', 2.0))),
                'min_frequency': int(learning_config.get('min_frequency', defaults.get('min_frequency', 3))),
                'confidence_thresholds': learning_config.get('confidence_thresholds', defaults.get('confidence_thresholds', {
                    'high_confidence': 0.7,
                    'medium_confidence': 0.4,
                    'low_confidence': 0.1
                }))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading pattern learning parameters: {e}")
            return {
                'min_crisis_messages': 10,
                'max_phrases_to_analyze': 200,
                'min_distinctiveness_ratio': 2.0,
                'min_frequency': 3,
                'confidence_thresholds': {
                    'high_confidence': 0.7,
                    'medium_confidence': 0.4,
                    'low_confidence': 0.1
                }
            }
    
    # ========================================================================
    # SEMANTIC ANALYSIS PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_semantic_analysis_parameters(self) -> Dict[str, Any]:
        """
        Get semantic analysis parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with semantic analysis settings
        """
        try:
            semantic_config = self._full_config.get('semantic_analysis', {})
            defaults = semantic_config.get('defaults', {})
            
            return {
                'context_window': int(semantic_config.get('context_window', defaults.get('context_window', 3))),
                'similarity_threshold': float(semantic_config.get('similarity_threshold', defaults.get('similarity_threshold', 0.75))),
                'context_boost_weight': float(semantic_config.get('context_boost_weight', defaults.get('context_boost_weight', 1.5))),
                'negative_threshold': float(semantic_config.get('negative_threshold', defaults.get('negative_threshold', 0.6))),
                'boost_weights': semantic_config.get('boost_weights', defaults.get('boost_weights', {
                    'high_relevance_boost': 0.1,
                    'medium_relevance_boost': 0.05,
                    'family_rejection_boost': 0.15,
                    'discrimination_fear_boost': 0.15,
                    'support_seeking_boost': -0.05
                }))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading semantic analysis parameters: {e}")
            return {
                'context_window': 3,
                'similarity_threshold': 0.75,
                'context_boost_weight': 1.5,
                'negative_threshold': 0.6,
                'boost_weights': {
                    'high_relevance_boost': 0.1,
                    'medium_relevance_boost': 0.05,
                    'family_rejection_boost': 0.15,
                    'discrimination_fear_boost': 0.15,
                    'support_seeking_boost': -0.05
                }
            }
    
    # ========================================================================
    # CONTEXTUAL WEIGHTING PARAMETERS - NEW v3.1 Support
    # ========================================================================
    
    def get_contextual_weighting_parameters(self) -> Dict[str, Any]:
        """
        Get contextual weighting parameters from v3.1 JSON configuration
        
        NEW METHOD: Added to support v3.1 JSON contextual_weighting section
        
        Returns:
            Dictionary with contextual weighting settings
        """
        try:
            context_config = self._full_config.get('contextual_weighting', {})
            defaults = context_config.get('defaults', {})
            
            return {
                'temporal_context_weight': float(context_config.get('temporal_context_weight', defaults.get('temporal_context_weight', 1.0))),
                'social_context_weight': float(context_config.get('social_context_weight', defaults.get('social_context_weight', 1.2))),
                'context_signal_weight': float(context_config.get('context_signal_weight', defaults.get('context_signal_weight', 0.8))),
                'temporal_urgency_multiplier': float(context_config.get('temporal_urgency_multiplier', defaults.get('temporal_urgency_multiplier', 1.5))),
                'community_awareness_boost': float(context_config.get('community_awareness_boost', defaults.get('community_awareness_boost', 0.3)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading contextual weighting parameters: {e}")
            return {
                'temporal_context_weight': 1.0,
                'social_context_weight': 1.2,
                'context_signal_weight': 0.8,
                'temporal_urgency_multiplier': 1.5,
                'community_awareness_boost': 0.3
            }
    
    # ========================================================================
    # PERFORMANCE AND INTEGRATION PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_performance_parameters(self) -> Dict[str, Any]:
        """
        Get performance and timeout parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with performance settings
        """
        try:
            perf_config = self._full_config.get('performance_settings', {})
            defaults = perf_config.get('defaults', {})
            
            return {
                'timeout_ms': int(perf_config.get('timeout_ms', defaults.get('timeout_ms', 5000))),
                'max_concurrent': int(perf_config.get('max_concurrent', defaults.get('max_concurrent', 10))),
                'enable_caching': perf_config.get('enable_caching', defaults.get('enable_caching', True)),
                'cache_ttl_seconds': int(perf_config.get('cache_ttl_seconds', defaults.get('cache_ttl_seconds', 300))),
                'enable_parallel_processing': perf_config.get('enable_parallel_processing', defaults.get('enable_parallel_processing', True))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading performance parameters: {e}")
            return {
                'timeout_ms': 5000,
                'max_concurrent': 10,
                'enable_caching': True,
                'cache_ttl_seconds': 300,
                'enable_parallel_processing': True
            }
    
    def get_integration_settings(self) -> Dict[str, Any]:
        """
        Get integration settings for pattern analysis from v3.1 JSON configuration
        
        Returns:
            Dictionary with integration settings
        """
        try:
            integration_config = self._full_config.get('integration_settings', {})
            defaults = integration_config.get('defaults', {})
            
            return {
                'enable_pattern_analysis': integration_config.get('enable_pattern_analysis', defaults.get('enable_pattern_analysis', False)),
                'enable_semantic_analysis': integration_config.get('enable_semantic_analysis', defaults.get('enable_semantic_analysis', False)),
                'enable_phrase_extraction': integration_config.get('enable_phrase_extraction', defaults.get('enable_phrase_extraction', False)),
                'enable_pattern_learning': integration_config.get('enable_pattern_learning', defaults.get('enable_pattern_learning', False)),
                'integration_mode': integration_config.get('integration_mode', defaults.get('integration_mode', 'full'))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading integration settings: {e}")
            return {
                'enable_pattern_analysis': False,
                'enable_semantic_analysis': False,
                'enable_phrase_extraction': False,
                'enable_pattern_learning': False,
                'integration_mode': 'full'
            }
    
    # ========================================================================
    # DEBUGGING AND EXPERIMENTAL PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_debugging_settings(self) -> Dict[str, Any]:
        """
        Get debugging and logging settings from v3.1 JSON configuration
        
        Returns:
            Dictionary with debugging settings
        """
        try:
            debug_config = self._full_config.get('debugging_settings', {})
            defaults = debug_config.get('defaults', {})
            
            return {
                'enable_detailed_logging': debug_config.get('enable_detailed_logging', defaults.get('enable_detailed_logging', True)),
                'log_analysis_steps': debug_config.get('log_analysis_steps', defaults.get('log_analysis_steps', False)),
                'include_reasoning': debug_config.get('include_reasoning', defaults.get('include_reasoning', True)),
                'enable_performance_metrics': debug_config.get('enable_performance_metrics', defaults.get('enable_performance_metrics', True)),
                'save_intermediate_results': debug_config.get('save_intermediate_results', defaults.get('save_intermediate_results', False)),
                'enable_timing_metrics': debug_config.get('enable_timing_metrics', defaults.get('enable_timing_metrics', True))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading debugging settings: {e}")
            return {
                'enable_detailed_logging': True,
                'log_analysis_steps': False,
                'include_reasoning': True,
                'enable_performance_metrics': True,
                'save_intermediate_results': False,
                'enable_timing_metrics': True
            }
    
    def get_experimental_features(self) -> Dict[str, Any]:
        """
        Get experimental feature flags from v3.1 JSON configuration
        
        Returns:
            Dictionary with experimental feature settings
        """
        try:
            experimental_config = self._full_config.get('experimental_features', {})
            defaults = experimental_config.get('defaults', {})
            
            return {
                'advanced_context': experimental_config.get('advanced_context', defaults.get('advanced_context', False)),
                'community_vocab': experimental_config.get('community_vocab', defaults.get('community_vocab', True)),
                'temporal_patterns': experimental_config.get('temporal_patterns', defaults.get('temporal_patterns', True)),
                'multi_language': experimental_config.get('multi_language', defaults.get('multi_language', False))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading experimental features: {e}")
            return {
                'advanced_context': False,
                'community_vocab': True,
                'temporal_patterns': True,
                'multi_language': False
            }
    
    # ========================================================================
    # ADVANCED PARAMETERS - Enhanced Functionality
    # ========================================================================

    def get_advanced_parameters(self) -> Dict[str, Any]:
        """
        Get advanced analysis parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with advanced analysis parameters
        """
        try:
            advanced_config = self._full_config.get('advanced_parameters', {})
            defaults = advanced_config.get('defaults', {})
            
            return {
                'pattern_confidence_boost': float(advanced_config.get('pattern_confidence_boost', defaults.get('pattern_confidence_boost', 0.05))),
                'model_confidence_boost': float(advanced_config.get('model_confidence_boost', defaults.get('model_confidence_boost', 0.0))),
                'context_signal_weight': float(advanced_config.get('context_signal_weight', defaults.get('context_signal_weight', 1.0))),
                'temporal_urgency_multiplier': float(advanced_config.get('temporal_urgency_multiplier', defaults.get('temporal_urgency_multiplier', 1.2))),
                'community_awareness_boost': float(advanced_config.get('community_awareness_boost', defaults.get('community_awareness_boost', 0.1)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading advanced parameters: {e}")
            return {
                'pattern_confidence_boost': 0.05,
                'model_confidence_boost': 0.0,
                'context_signal_weight': 1.0,
                'temporal_urgency_multiplier': 1.2,
                'community_awareness_boost': 0.1
            }
    
    # ========================================================================
    # ENSEMBLE WEIGHT ACCESS - PHASE 3D CLEANED: REMOVED DUPLICATE VARIABLES
    # ========================================================================
    
    def get_ensemble_weights(self) -> Dict[str, float]:
        """
        PHASE 3D CLEANED: Get ensemble weights from ModelEnsembleManager instead
        
        Note: This method now refers users to ModelEnsembleManager for ensemble weights.
        The duplicate NLP_ANALYSIS_ENSEMBLE_WEIGHT_* variables have been removed.
        
        Returns:
            Dictionary indicating where to get ensemble weights
        """
        logger.info("ℹ️ Phase 3d: Ensemble weights now managed by ModelEnsembleManager")
        logger.info("💡 Use ModelEnsembleManager.get_model_weights() for ensemble weights")
        
        return {
            'note': 'Ensemble weights managed by ModelEnsembleManager',
            'use_instead': 'ModelEnsembleManager.get_model_weights()',
            'reason': 'Phase 3d duplicate variable cleanup - removed NLP_ANALYSIS_ENSEMBLE_WEIGHT_* variables'
        }
    
    # ========================================================================
    # LEARNING SYSTEM PARAMETERS - PHASE 3D STEP 4 FUNCTIONALITY
    # ========================================================================

    def get_learning_system_parameters(self) -> Dict[str, Any]:
        """
        PHASE 3D STEP 4: Get learning system parameters for adaptive threshold adjustment
        
        Returns:
            Dictionary with learning system configuration
        """
        try:
            learning_config = self._full_config.get('learning_system', {})
            defaults = learning_config.get('defaults', {})
            
            # Core learning parameters
            core_params = {
                'enabled': learning_config.get('enabled', defaults.get('enabled', True)),
                'learning_rate': float(learning_config.get('learning_rate', defaults.get('learning_rate', 0.01))),
                'min_confidence_adjustment': float(learning_config.get('min_confidence_adjustment', defaults.get('min_confidence_adjustment', 0.05))),
                'max_confidence_adjustment': float(learning_config.get('max_confidence_adjustment', defaults.get('max_confidence_adjustment', 0.30))),
                'max_adjustments_per_day': int(learning_config.get('max_adjustments_per_day', defaults.get('max_adjustments_per_day', 50))),
                'persistence_file': learning_config.get('persistence_file', defaults.get('persistence_file', './learning_data/adjustments.json')),
                'feedback_weight': float(learning_config.get('feedback_weight', defaults.get('feedback_weight', 0.1))),
                'min_samples': int(learning_config.get('min_samples', defaults.get('min_samples', 5))),
                'adjustment_limit': float(learning_config.get('adjustment_limit', defaults.get('adjustment_limit', 0.05))),
                'max_drift': float(learning_config.get('max_drift', defaults.get('max_drift', 0.1)))
            }
            
            # Sensitivity bounds
            sensitivity_bounds = learning_config.get('sensitivity_bounds', {})
            sensitivity_defaults = defaults.get('sensitivity_bounds', {})
            core_params['sensitivity_bounds'] = {
                'min_global_sensitivity': float(sensitivity_bounds.get('min_global_sensitivity', sensitivity_defaults.get('min_global_sensitivity', 0.5))),
                'max_global_sensitivity': float(sensitivity_bounds.get('max_global_sensitivity', sensitivity_defaults.get('max_global_sensitivity', 1.5)))
            }
            
            # Adjustment factors
            adjustment_factors = learning_config.get('adjustment_factors', {})
            adjustment_defaults = defaults.get('adjustment_factors', {})
            core_params['adjustment_factors'] = {
                'false_positive_factor': float(adjustment_factors.get('false_positive_factor', adjustment_defaults.get('false_positive_factor', -0.1))),
                'false_negative_factor': float(adjustment_factors.get('false_negative_factor', adjustment_defaults.get('false_negative_factor', 0.1)))
            }
            
            # Severity multipliers
            severity_multipliers = learning_config.get('severity_multipliers', {})
            severity_defaults = defaults.get('severity_multipliers', {})
            core_params['severity_multipliers'] = {
                'high_severity': float(severity_multipliers.get('high_severity', severity_defaults.get('high_severity', 3.0))),
                'medium_severity': float(severity_multipliers.get('medium_severity', severity_defaults.get('medium_severity', 2.0))),
                'low_severity': float(severity_multipliers.get('low_severity', severity_defaults.get('low_severity', 1.0)))
            }
            
            return core_params
            
        except Exception as e:
            logger.error(f"❌ Error loading learning system parameters: {e}")
            return {
                'enabled': True,
                'learning_rate': 0.01,
                'min_confidence_adjustment': 0.05,
                'max_confidence_adjustment': 0.30,
                'max_adjustments_per_day': 50,
                'persistence_file': './learning_data/adjustments.json',
                'feedback_weight': 0.1,
                'min_samples': 5,
                'adjustment_limit': 0.05,
                'max_drift': 0.1,
                'sensitivity_bounds': {
                    'min_global_sensitivity': 0.5,
                    'max_global_sensitivity': 1.5
                },
                'adjustment_factors': {
                    'false_positive_factor': -0.1,
                    'false_negative_factor': 0.1
                },
                'severity_multipliers': {
                    'high_severity': 3.0,
                    'medium_severity': 2.0,
                    'low_severity': 1.0
                }
            }

    def validate_learning_system_parameters(self) -> Dict[str, Any]:
        """
        PHASE 3D STEP 4: Validate learning system parameter ranges and types
        
        Returns:
            Dictionary with validation results
        """
        try:
            params = self.get_learning_system_parameters()
            errors = []
            warnings = []
            
            # Validate learning rate
            if not 0.001 <= params['learning_rate'] <= 1.0:
                errors.append(f"Learning rate {params['learning_rate']} outside valid range [0.001, 1.0]")
            
            # Validate confidence adjustments
            if not 0.01 <= params['min_confidence_adjustment'] <= 1.0:
                errors.append(f"Min confidence adjustment {params['min_confidence_adjustment']} outside valid range [0.01, 1.0]")
            
            if not 0.05 <= params['max_confidence_adjustment'] <= 1.0:
                errors.append(f"Max confidence adjustment {params['max_confidence_adjustment']} outside valid range [0.05, 1.0]")
            
            if params['min_confidence_adjustment'] >= params['max_confidence_adjustment']:
                errors.append(f"Min confidence adjustment {params['min_confidence_adjustment']} must be less than max {params['max_confidence_adjustment']}")
            
            # Validate adjustments per day
            if not 1 <= params['max_adjustments_per_day'] <= 1000:
                errors.append(f"Max adjustments per day {params['max_adjustments_per_day']} outside valid range [1, 1000]")
            
            # Validate sensitivity bounds
            sensitivity = params['sensitivity_bounds']
            if not 0.1 <= sensitivity['min_global_sensitivity'] <= 5.0:
                errors.append(f"Min global sensitivity {sensitivity['min_global_sensitivity']} outside valid range [0.1, 5.0]")
            
            if not 0.1 <= sensitivity['max_global_sensitivity'] <= 5.0:
                errors.append(f"Max global sensitivity {sensitivity['max_global_sensitivity']} outside valid range [0.1, 5.0]")
            
            if sensitivity['min_global_sensitivity'] >= sensitivity['max_global_sensitivity']:
                errors.append(f"Min global sensitivity {sensitivity['min_global_sensitivity']} must be less than max {sensitivity['max_global_sensitivity']}")
            
            # Validate adjustment factors
            factors = params['adjustment_factors']
            if not -1.0 <= factors['false_positive_factor'] <= 1.0:
                errors.append(f"False positive factor {factors['false_positive_factor']} outside valid range [-1.0, 1.0]")
            
            if not -1.0 <= factors['false_negative_factor'] <= 1.0:
                errors.append(f"False negative factor {factors['false_negative_factor']} outside valid range [-1.0, 1.0]")
            
            # Validate severity multipliers
            multipliers = params['severity_multipliers']
            for severity, multiplier in multipliers.items():
                if not 0.1 <= multiplier <= 10.0:
                    errors.append(f"Severity multiplier {severity} value {multiplier} outside valid range [0.1, 10.0]")
            
            # Check logical ordering of severity multipliers
            if not (multipliers['high_severity'] >= multipliers['medium_severity'] >= multipliers['low_severity']):
                warnings.append("Severity multipliers should follow pattern: high >= medium >= low")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'parameters_validated': len(params),
                'validation_timestamp': str(datetime.now())
            }
            
        except Exception as e:
            logger.error(f"❌ Error validating learning system parameters: {e}")
            return {
                'valid': False,
                'errors': [f"Validation failed: {str(e)}"],
                'warnings': [],
                'parameters_validated': 0,
                'validation_timestamp': str(datetime.now())
            }
    
    # ========================================================================
    # AGGREGATE ACCESS METHODS - Enhanced for v3.1
    # ========================================================================
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all analysis parameters in organized structure
        Enhanced for v3.1 compatibility with hybrid functionality
        """
        metadata = self._full_config.get('_metadata', {})
        
        return {
            'version': '3.1d-hybrid',
            'architecture': 'clean-v3.1-unified-hybrid',
            'json_version': metadata.get('configuration_version', 'unknown'),
            'compliance': metadata.get('compliance', 'unknown'),
            'phase_3d_changes': {
                'hybrid_approach': 'Preserves enhanced functionality with v3.1 compliance',
                'learning_system': 'Phase 3d Step 4 learning system parameters',
                'contextual_weighting': 'NEW v3.1 contextual weighting support',
                'consolidated': 'Learning parameters from multiple locations',
                'standardized': 'All learning variables use NLP_ANALYSIS_LEARNING_* naming'
            },
            'crisis_thresholds': self.get_crisis_thresholds(),
            'confidence_boost': self.get_confidence_boost_parameters(),
            'phrase_extraction': self.get_phrase_extraction_parameters(),
            'pattern_learning': self.get_pattern_learning_parameters(),
            'semantic_analysis': self.get_semantic_analysis_parameters(),
            'contextual_weighting': self.get_contextual_weighting_parameters(),
            'advanced_parameters': self.get_advanced_parameters(),
            'integration_settings': self.get_integration_settings(),
            'performance_settings': self.get_performance_parameters(),
            'debugging_settings': self.get_debugging_settings(),
            'experimental_features': self.get_experimental_features(),
            'learning_system': self.get_learning_system_parameters(),
            'ensemble_weights_info': self.get_ensemble_weights()
        }
        
    def validate_parameters(self) -> Dict[str, Any]:
        """
        Validate all analysis parameters with v3.1 compliance checks
        
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        try:
            # Check v3.1 compliance
            metadata = self._full_config.get('_metadata', {})
            if not metadata:
                warnings.append("Missing _metadata section - not fully v3.1 compliant")
            elif metadata.get('configuration_version', '').startswith('3d.'):
                logger.info("✅ Configuration is v3.1 compliant")
            
            # Validate crisis thresholds
            thresholds = self.get_crisis_thresholds()
            if not (thresholds['high'] > thresholds['medium'] > thresholds['low']):
                errors.append("Crisis thresholds not in correct order (high > medium > low)")
            
            # Validate confidence boost parameters
            boost_params = self.get_confidence_boost_parameters()
            for param, value in boost_params.items():
                if not isinstance(value, (int, float)):
                    errors.append(f"Confidence boost parameter '{param}' is not numeric: {value}")
                elif value < 0:
                    warnings.append(f"Confidence boost parameter '{param}' is negative: {value}")
            
            # Validate phrase extraction parameters
            phrase_params = self.get_phrase_extraction_parameters()
            if phrase_params['min_phrase_length'] >= phrase_params['max_phrase_length']:
                errors.append("Phrase min_length must be less than max_length")
            
            # Validate contextual weighting parameters
            context_params = self.get_contextual_weighting_parameters()
            for param, value in context_params.items():
                if not isinstance(value, (int, float)):
                    errors.append(f"Contextual weighting parameter '{param}' is not numeric: {value}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'parameters_validated': 'all-hybrid-v3.1',
                'json_compliance': 'v3.1' if metadata else 'partial',
                'validation_timestamp': str(datetime.now())
            }
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': warnings,
                'parameters_validated': 'partial',
                'validation_timestamp': str(datetime.now())
            }

    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get summary of current configuration for monitoring and debugging
        Enhanced for v3.1 hybrid compatibility
        
        Returns:
            Dictionary with configuration summary
        """
        try:
            metadata = self._full_config.get('_metadata', {})
            
            return {
                'manager_version': 'v3.1d-hybrid',
                'json_configuration_version': metadata.get('configuration_version', 'unknown'),
                'json_compliance': metadata.get('compliance', 'unknown'),
                'last_updated': metadata.get('updated_date', 'unknown'),
                'total_parameter_categories': 11,  # All parameter categories including new ones
                'integration_mode': self.get_integration_settings().get('integration_mode', 'unknown'),
                'performance_timeout_ms': self.get_performance_parameters().get('timeout_ms', 'unknown'),
                'debug_logging_enabled': self.get_debugging_settings().get('enable_detailed_logging', False),
                'learning_system_enabled': self.get_learning_system_parameters().get('enabled', False),
                'contextual_weighting_enabled': True,  # New v3.1 feature
                'manager_initialized': True,
                'configuration_loaded': self._full_config is not None,
                'hybrid_features': {
                    'phase_3d_learning_system': True,
                    'v3_1_contextual_weighting': True,
                    'enhanced_validation': True,
                    'metadata_tracking': bool(metadata)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting configuration summary: {e}")
            return {
                'manager_version': 'v3.1d-hybrid',
                'json_configuration_version': 'error',
                'error': str(e),
                'manager_initialized': False
            }

# ============================================================================
# Factory Function - Clean v3.1 Architecture Compliance
# ============================================================================

def create_analysis_parameters_manager(config_manager) -> AnalysisParametersManager:
    """
    Factory function to create AnalysisParametersManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        AnalysisParametersManager instance with hybrid v3.1 compatibility
    """
    return AnalysisParametersManager(config_manager)

__all__ = ['AnalysisParametersManager', 'create_analysis_parameters_manager']

logger.info("✅ Hybrid AnalysisParametersManager v3.1d loaded - Phase 3d functionality + v3.1 compliance")