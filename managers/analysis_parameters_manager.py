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
            config_manager: ConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("ConfigManager is required for AnalysisParametersManager")
        
        self.config_manager = config_manager
        self.analysis_config = {}
        self._full_config = {}
        
        logger.info("✅ AnalysisParametersManager v3.1d initialized - Phase 3d cleaned")
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self):
        """Load analysis parameters configuration"""
        try:
            # Load analysis parameters via ConfigManager
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
        
        Returns:
            Dictionary containing all parameter categories
        """
        return {
            'version': '3.1d-cleaned',
            'architecture': 'clean-v3.1-unified',
            'phase_3d_changes': 'Removed duplicate ensemble weight variables',
            'crisis_thresholds': self.get_crisis_thresholds(),
            'confidence_boost': self.get_confidence_boost_parameters(),
            'phrase_extraction': self.get_phrase_extraction_parameters(),
            'pattern_learning': self.get_pattern_learning_parameters(),
            'semantic_analysis': self.get_semantic_analysis_parameters(),
            'performance': self.get_performance_parameters(),
            'integration': self.get_integration_settings(),
            'debugging': self.get_debugging_settings(),
            'experimental': self.get_experimental_features(),
            'ensemble_weights': self.get_ensemble_weights()  # Shows where to get them now
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

# ============================================================================
# Factory Function - Clean v3.1 Architecture Compliance
# ============================================================================

def create_analysis_parameters_manager(config_manager) -> AnalysisParametersManager:
    """
    Factory function to create AnalysisParametersManager instance
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        AnalysisParametersManager instance
    """
    return AnalysisParametersManager(config_manager)

__all__ = ['AnalysisParametersManager', 'create_analysis_parameters_manager']

logger.info("✅ Cleaned AnalysisParametersManager v3.1d loaded - Phase 3d duplicate variables removed")