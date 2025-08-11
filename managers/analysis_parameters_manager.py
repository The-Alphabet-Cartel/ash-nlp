# ash/ash-nlp/managers/analysis_parameters_manager.py - Phase 3d Cleaned
"""
Analysis Parameters Manager for Ash NLP Service v3.1d - Duplicate Variables Removed
Phase 3d: Removed duplicate ensemble weight variables (use ModelEnsembleManager instead)

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalysisParametersManager:
    """
    Analysis Parameters Manager with Phase 3d duplicate variable cleanup
    REMOVED: Duplicate ensemble weight variables (now handled by ModelEnsembleManager)
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
        
        logger.info("✅ AnalysisParametersManager v3.1d initialized - Phase 3d cleaned")
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self):
        """Load analysis parameters configuration"""
        try:
            # Load analysis parameters via UnifiedConfigManager
            analysis_config_raw = self.config_manager.load_config_file('analysis_parameters')
            
            if not analysis_config_raw:
                logger.error("❌ Could not load analysis_parameters.json configuration")
                raise ValueError("Analysis parameters configuration not available")
            
            # Extract analysis system configuration
            self.analysis_config = analysis_config_raw.get("analysis_system", {})
            
            # Store the full configuration for access by parameter methods
            self._full_config = analysis_config_raw
            
            logger.info("✅ Analysis parameters loaded from JSON configuration with environment overrides")
            logger.debug(f"📋 Configuration version: {self.analysis_config.get('version', 'unknown')}")
            logger.debug(f"🏗️ Architecture: {self.analysis_config.get('architecture', 'unknown')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load analysis parameters: {e}")
            raise ValueError(f"Analysis parameters configuration error: {e}")
    
    # ========================================================================
    # CRISIS THRESHOLDS - Core Algorithm Configuration
    # ========================================================================
    
    def get_crisis_thresholds(self) -> Dict[str, float]:
        """
        Get crisis threshold settings for analysis algorithms
        
        Returns:
            Dictionary with high, medium, low thresholds
        """
        try:
            thresholds_config = self._full_config.get('crisis_thresholds', {})
            
            # Extract thresholds with environment variable support
            thresholds = {
                'high': float(thresholds_config.get('high', thresholds_config.get('defaults', {}).get('high', 0.55))),
                'medium': float(thresholds_config.get('medium', thresholds_config.get('defaults', {}).get('medium', 0.28))),
                'low': float(thresholds_config.get('low', thresholds_config.get('defaults', {}).get('low', 0.16)))
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
    # PHRASE EXTRACTION PARAMETERS
    # ========================================================================
    
    def get_phrase_extraction_parameters(self) -> Dict[str, Any]:
        """
        Get phrase extraction parameters
        
        Returns:
            Dictionary with phrase extraction settings
        """
        try:
            phrase_config = self._full_config.get('phrase_extraction', {})
            defaults = phrase_config.get('defaults', {})
            
            return {
                'min_phrase_length': int(phrase_config.get('min_phrase_length', defaults.get('min_phrase_length', 2))),
                'max_phrase_length': int(phrase_config.get('max_phrase_length', defaults.get('max_phrase_length', 6))),
                'crisis_focus': phrase_config.get('crisis_focus', defaults.get('crisis_focus', True)),
                'community_specific': phrase_config.get('community_specific', defaults.get('community_specific', True)),
                'min_confidence': float(phrase_config.get('min_confidence', defaults.get('min_confidence', 0.3))),
                'max_results': int(phrase_config.get('max_results', defaults.get('max_results', 20)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading phrase extraction parameters: {e}")
            return {
                'min_phrase_length': 2,
                'max_phrase_length': 6,
                'crisis_focus': True,
                'community_specific': True,
                'min_confidence': 0.3,
                'max_results': 20
            }
    
    # ========================================================================
    # PATTERN LEARNING PARAMETERS
    # ========================================================================
    
    def get_pattern_learning_parameters(self) -> Dict[str, Any]:
        """
        Get pattern learning parameters
        
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
    # SEMANTIC ANALYSIS PARAMETERS
    # ========================================================================
    
    def get_semantic_analysis_parameters(self) -> Dict[str, Any]:
        """
        Get semantic analysis parameters
        
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
    # PERFORMANCE AND INTEGRATION PARAMETERS
    # ========================================================================
    
    def get_performance_parameters(self) -> Dict[str, Any]:
        """
        Get performance and timeout parameters
        
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
        Get integration settings for pattern analysis
        
        Returns:
            Dictionary with integration settings
        """
        try:
            integration_config = self._full_config.get('integration_settings', {})
            defaults = integration_config.get('defaults', {})
            
            return {
                'enable_pattern_analysis': integration_config.get('enable_pattern_analysis', defaults.get('enable_pattern_analysis', True)),
                'enable_semantic_analysis': integration_config.get('enable_semantic_analysis', defaults.get('enable_semantic_analysis', True)),
                'enable_phrase_extraction': integration_config.get('enable_phrase_extraction', defaults.get('enable_phrase_extraction', True)),
                'enable_pattern_learning': integration_config.get('enable_pattern_learning', defaults.get('enable_pattern_learning', True)),
                'integration_mode': integration_config.get('integration_mode', defaults.get('integration_mode', 'full'))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading integration settings: {e}")
            return {
                'enable_pattern_analysis': True,
                'enable_semantic_analysis': True,
                'enable_phrase_extraction': True,
                'enable_pattern_learning': True,
                'integration_mode': 'full'
            }
    
    # ========================================================================
    # DEBUGGING AND EXPERIMENTAL PARAMETERS
    # ========================================================================
    
    def get_debugging_settings(self) -> Dict[str, Any]:
        """
        Get debugging and logging settings
        
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
                'enable_performance_metrics': debug_config.get('enable_performance_metrics', defaults.get('enable_performance_metrics', True))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading debugging settings: {e}")
            return {
                'enable_detailed_logging': True,
                'log_analysis_steps': False,
                'include_reasoning': True,
                'enable_performance_metrics': True
            }
    
    def get_experimental_features(self) -> Dict[str, Any]:
        """
        Get experimental feature flags
        
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
    # AGGREGATE ACCESS METHODS
    # ========================================================================
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all analysis parameters in organized structure
        PHASE 3D STEP 4: Enhanced to include learning system parameters
        """
        return {
            'version': '3.1d-step4',
            'architecture': 'clean-v3.1-unified',
            'phase_3d_changes': {
                'step_4': 'Added learning system parameters support',
                'consolidated': 'Learning parameters from multiple locations',
                'standardized': 'All learning variables use NLP_ANALYSIS_LEARNING_* naming'
            },
            'crisis_thresholds': self.get_crisis_thresholds(),
            'confidence_boost': self.get_confidence_boost_parameters(),
            'phrase_extraction': self.get_phrase_extraction_parameters(),
            'pattern_learning': self.get_pattern_learning_parameters(),
            'semantic_analysis': self.get_semantic_analysis_parameters(),
            'advanced_parameters': self.get_advanced_parameters(),
            'integration_settings': self.get_integration_settings(),
            'performance_settings': self.get_performance_parameters(),
            'debugging_settings': self.get_debugging_settings(),
            'experimental_features': self.get_experimental_features(),
            'learning_system': self.get_learning_system_parameters() if hasattr(self, 'get_learning_system_parameters') else {},
            'ensemble_weights_info': self.get_ensemble_weights()
        }
        
    def validate_parameters(self) -> Dict[str, Any]:
        """
        Validate all analysis parameters
        
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        try:
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
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'parameters_validated': 'all'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': warnings,
                'parameters_validated': 'partial'
            }

    # ========================================================================
    # LEARNING SYSTEM PARAMETERS - PHASE 3D STEP 4 NEW FUNCTIONALITY
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

    def get_advanced_parameters(self) -> Dict[str, Any]:
        """
        Get advanced analysis parameters
        
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

# ============================================================================
# Factory Function - Clean v3.1 Architecture Compliance
# ============================================================================

def create_analysis_parameters_manager(config_manager) -> AnalysisParametersManager:
    """
    Factory function to create AnalysisParametersManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        AnalysisParametersManager instance
    """
    return AnalysisParametersManager(config_manager)

__all__ = ['AnalysisParametersManager', 'create_analysis_parameters_manager']

logger.info("✅ Cleaned AnalysisParametersManager v3.1d loaded - Phase 3d duplicate variables removed")