# ash/ash-nlp/managers/analysis_parameters_manager.py
"""
Analysis Parameters Manager for Ash NLP Service v3.1 - Phase 3b
Handles analysis algorithm parameters with JSON configuration and environment overrides

Phase 3b: Migration of analysis parameters from hardcoded constants to JSON configuration
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# ANALYSIS PARAMETERS MANAGER CLASS - v3.1 Clean Architecture
# ============================================================================

class AnalysisParametersManager:
    """
    Manages analysis algorithm parameters with JSON configuration and environment overrides
    Phase 3b: Complete migration from hardcoded constants to configurable parameters
    """
    
    def __init__(self, config_manager):
        """
        Initialize AnalysisParametersManager with ConfigManager dependency injection
        
        Args:
            config_manager: ConfigManager instance for dependency injection
        """
        self.config_manager = config_manager
        self.analysis_config = {}
        self._load_analysis_parameters()
        
        logger.info("AnalysisParametersManager v3.1 initialized (Phase 3b - Analysis parameters externalized)")
    
    def _load_analysis_parameters(self):
        """Load analysis parameters from JSON configuration with environment overrides"""
        try:
            # Load analysis parameters configuration
            analysis_config_raw = self.config_manager.get_configuration('analysis_parameters')
            
            if not analysis_config_raw:
                logger.error("❌ Failed to load analysis_parameters.json configuration")
                raise ValueError("Analysis parameters configuration not available")
            
            # Extract analysis system configuration
            self.analysis_config = analysis_config_raw.get("analysis_system", {})
            
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
            # Load from configuration
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            thresholds_config = config_raw.get('crisis_thresholds', {})
            
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
    # PHRASE EXTRACTION PARAMETERS
    # ========================================================================
    
    def get_phrase_extraction_parameters(self) -> Dict[str, Any]:
        """
        Get phrase extraction parameters for crisis phrase analysis
        
        Returns:
            Dictionary with phrase extraction configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            phrase_config = config_raw.get('phrase_extraction', {})
            
            parameters = {
                'min_phrase_length': int(phrase_config.get('min_phrase_length', 
                                                         phrase_config.get('defaults', {}).get('min_phrase_length', 2))),
                'max_phrase_length': int(phrase_config.get('max_phrase_length', 
                                                         phrase_config.get('defaults', {}).get('max_phrase_length', 6))),
                'crisis_focus': self._parse_bool(phrase_config.get('crisis_focus', 
                                                                 phrase_config.get('defaults', {}).get('crisis_focus', True))),
                'community_specific': self._parse_bool(phrase_config.get('community_specific', 
                                                                       phrase_config.get('defaults', {}).get('community_specific', True))),
                'min_confidence': float(phrase_config.get('min_confidence', 
                                                        phrase_config.get('defaults', {}).get('min_confidence', 0.3))),
                'max_results': int(phrase_config.get('max_results', 
                                                   phrase_config.get('defaults', {}).get('max_results', 20)))
            }
            
            logger.debug(f"✅ Phrase extraction parameters: {parameters}")
            return parameters
            
        except Exception as e:
            logger.error(f"❌ Error loading phrase extraction parameters: {e}")
            # Return safe defaults
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
        Get pattern learning parameters for community message analysis
        
        Returns:
            Dictionary with pattern learning configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            pattern_config = config_raw.get('pattern_learning', {})
            defaults = pattern_config.get('defaults', {})
            
            parameters = {
                'min_crisis_messages': int(pattern_config.get('min_crisis_messages', 
                                                            defaults.get('min_crisis_messages', 10))),
                'max_phrases_to_analyze': int(pattern_config.get('max_phrases_to_analyze', 
                                                              defaults.get('max_phrases_to_analyze', 200))),
                'min_distinctiveness_ratio': float(pattern_config.get('min_distinctiveness_ratio', 
                                                                    defaults.get('min_distinctiveness_ratio', 2.0))),
                'min_frequency': int(pattern_config.get('min_frequency', 
                                                      defaults.get('min_frequency', 3))),
                'confidence_thresholds': self._get_pattern_confidence_thresholds(pattern_config)
            }
            
            logger.debug(f"✅ Pattern learning parameters: {parameters}")
            return parameters
            
        except Exception as e:
            logger.error(f"❌ Error loading pattern learning parameters: {e}")
            # Return safe defaults
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
    
    def _get_pattern_confidence_thresholds(self, pattern_config: Dict[str, Any]) -> Dict[str, float]:
        """Extract pattern confidence thresholds with fallback to defaults"""
        try:
            confidence_config = pattern_config.get('confidence_thresholds', {})
            defaults = confidence_config.get('defaults', {})
            
            thresholds = {
                'high_confidence': float(confidence_config.get('high_confidence', 
                                                             defaults.get('high_confidence', 0.7))),
                'medium_confidence': float(confidence_config.get('medium_confidence', 
                                                               defaults.get('medium_confidence', 0.4))),
                'low_confidence': float(confidence_config.get('low_confidence', 
                                                            defaults.get('low_confidence', 0.1)))
            }
            
            # Validate threshold ordering
            if not (thresholds['high_confidence'] > thresholds['medium_confidence'] > thresholds['low_confidence']):
                logger.warning("⚠️ Invalid pattern confidence threshold ordering, using defaults")
                return {'high_confidence': 0.7, 'medium_confidence': 0.4, 'low_confidence': 0.1}
            
            return thresholds
            
        except Exception as e:
            logger.error(f"❌ Error loading pattern confidence thresholds: {e}")
            return {'high_confidence': 0.7, 'medium_confidence': 0.4, 'low_confidence': 0.1}
    
    # ========================================================================
    # SEMANTIC ANALYSIS PARAMETERS
    # ========================================================================
    
    def get_semantic_analysis_parameters(self) -> Dict[str, Any]:
        """
        Get semantic analysis parameters for context understanding
        
        Returns:
            Dictionary with semantic analysis configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            semantic_config = config_raw.get('semantic_analysis', {})
            defaults = semantic_config.get('defaults', {})
            
            parameters = {
                'context_window': int(semantic_config.get('context_window', 
                                                        defaults.get('context_window', 3))),
                'boost_weights': self._get_semantic_boost_weights(semantic_config)
            }
            
            logger.debug(f"✅ Semantic analysis parameters: {parameters}")
            return parameters
            
        except Exception as e:
            logger.error(f"❌ Error loading semantic analysis parameters: {e}")
            # Return safe defaults
            return {
                'context_window': 3,
                'boost_weights': {
                    'high_relevance': 0.1,
                    'medium_relevance': 0.05,
                    'family_rejection': 0.15,
                    'discrimination_fear': 0.15,
                    'support_seeking': -0.05
                }
            }
    
    def _get_semantic_boost_weights(self, semantic_config: Dict[str, Any]) -> Dict[str, float]:
        """Extract semantic boost weights with fallback to defaults"""
        try:
            boost_config = semantic_config.get('boost_weights', {})
            defaults = boost_config.get('defaults', {})
            
            weights = {
                'high_relevance': float(boost_config.get('high_relevance', 
                                                       defaults.get('high_relevance', 0.1))),
                'medium_relevance': float(boost_config.get('medium_relevance', 
                                                         defaults.get('medium_relevance', 0.05))),
                'family_rejection': float(boost_config.get('family_rejection', 
                                                         defaults.get('family_rejection', 0.15))),
                'discrimination_fear': float(boost_config.get('discrimination_fear', 
                                                            defaults.get('discrimination_fear', 0.15))),
                'support_seeking': float(boost_config.get('support_seeking', 
                                                        defaults.get('support_seeking', -0.05)))
            }
            
            logger.debug(f"✅ Semantic boost weights: {weights}")
            return weights
            
        except Exception as e:
            logger.error(f"❌ Error loading semantic boost weights: {e}")
            return {
                'high_relevance': 0.1,
                'medium_relevance': 0.05,
                'family_rejection': 0.15,
                'discrimination_fear': 0.15,
                'support_seeking': -0.05
            }
    
    # ========================================================================
    # ADVANCED PARAMETERS
    # ========================================================================
    
    def get_advanced_parameters(self) -> Dict[str, Any]:
        """
        Get advanced analysis parameters for fine-tuning algorithm behavior
        
        Returns:
            Dictionary with advanced analysis configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            advanced_config = config_raw.get('advanced_parameters', {})
            defaults = advanced_config.get('defaults', {})
            
            parameters = {
                'pattern_confidence_boost': float(advanced_config.get('pattern_confidence_boost', 
                                                                    defaults.get('pattern_confidence_boost', 0.05))),
                'model_confidence_boost': float(advanced_config.get('model_confidence_boost', 
                                                                  defaults.get('model_confidence_boost', 0.0))),
                'context_signal_weight': float(advanced_config.get('context_signal_weight', 
                                                                 defaults.get('context_signal_weight', 1.0))),
                'temporal_urgency_multiplier': float(advanced_config.get('temporal_urgency_multiplier', 
                                                                       defaults.get('temporal_urgency_multiplier', 1.2))),
                'community_awareness_boost': float(advanced_config.get('community_awareness_boost', 
                                                                     defaults.get('community_awareness_boost', 0.1)))
            }
            
            logger.debug(f"✅ Advanced parameters: {parameters}")
            return parameters
            
        except Exception as e:
            logger.error(f"❌ Error loading advanced parameters: {e}")
            # Return safe defaults
            return {
                'pattern_confidence_boost': 0.05,
                'model_confidence_boost': 0.0,
                'context_signal_weight': 1.0,
                'temporal_urgency_multiplier': 1.2,
                'community_awareness_boost': 0.1
            }
    
    # ========================================================================
    # INTEGRATION SETTINGS
    # ========================================================================
    
    def get_integration_settings(self) -> Dict[str, Any]:
        """
        Get integration settings for analysis components
        
        Returns:
            Dictionary with integration configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            integration_config = config_raw.get('integration_settings', {})
            defaults = integration_config.get('defaults', {})
            
            settings = {
                'enable_pattern_analysis': self._parse_bool(integration_config.get('enable_pattern_analysis', 
                                                                                  defaults.get('enable_pattern_analysis', True))),
                'enable_semantic_analysis': self._parse_bool(integration_config.get('enable_semantic_analysis', 
                                                                                   defaults.get('enable_semantic_analysis', True))),
                'enable_phrase_extraction': self._parse_bool(integration_config.get('enable_phrase_extraction', 
                                                                                   defaults.get('enable_phrase_extraction', True))),
                'enable_pattern_learning': self._parse_bool(integration_config.get('enable_pattern_learning', 
                                                                                  defaults.get('enable_pattern_learning', True))),
                'integration_mode': str(integration_config.get('integration_mode', 
                                                             defaults.get('integration_mode', 'full')))
            }
            
            logger.debug(f"✅ Integration settings: {settings}")
            return settings
            
        except Exception as e:
            logger.error(f"❌ Error loading integration settings: {e}")
            # Return safe defaults
            return {
                'enable_pattern_analysis': True,
                'enable_semantic_analysis': True,
                'enable_phrase_extraction': True,
                'enable_pattern_learning': True,
                'integration_mode': 'full'
            }
    
    # ========================================================================
    # PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """
        Get performance settings for analysis algorithms
        
        Returns:
            Dictionary with performance configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            performance_config = config_raw.get('performance_settings', {})
            defaults = performance_config.get('defaults', {})
            
            settings = {
                'analysis_timeout_ms': int(performance_config.get('analysis_timeout_ms', 
                                                                defaults.get('analysis_timeout_ms', 5000))),
                'max_concurrent_analyses': int(performance_config.get('max_concurrent_analyses', 
                                                                    defaults.get('max_concurrent_analyses', 10))),
                'cache_analysis_results': self._parse_bool(performance_config.get('cache_analysis_results', 
                                                                                 defaults.get('cache_analysis_results', True))),
                'cache_ttl_seconds': int(performance_config.get('cache_ttl_seconds', 
                                                              defaults.get('cache_ttl_seconds', 300))),
                'enable_parallel_processing': self._parse_bool(performance_config.get('enable_parallel_processing', 
                                                                                     defaults.get('enable_parallel_processing', True)))
            }
            
            logger.debug(f"✅ Performance settings: {settings}")
            return settings
            
        except Exception as e:
            logger.error(f"❌ Error loading performance settings: {e}")
            # Return safe defaults
            return {
                'analysis_timeout_ms': 5000,
                'max_concurrent_analyses': 10,
                'cache_analysis_results': True,
                'cache_ttl_seconds': 300,
                'enable_parallel_processing': True
            }
    
    # ========================================================================
    # DEBUGGING SETTINGS
    # ========================================================================
    
    def get_debugging_settings(self) -> Dict[str, Any]:
        """
        Get debugging settings for development and troubleshooting
        
        Returns:
            Dictionary with debugging configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            debug_config = config_raw.get('debugging_settings', {})
            defaults = debug_config.get('defaults', {})
            
            settings = {
                'enable_detailed_logging': self._parse_bool(debug_config.get('enable_detailed_logging', 
                                                                           defaults.get('enable_detailed_logging', False))),
                'log_analysis_steps': self._parse_bool(debug_config.get('log_analysis_steps', 
                                                                       defaults.get('log_analysis_steps', False))),
                'include_reasoning_in_response': self._parse_bool(debug_config.get('include_reasoning_in_response', 
                                                                                 defaults.get('include_reasoning_in_response', True))),
                'enable_performance_metrics': self._parse_bool(debug_config.get('enable_performance_metrics', 
                                                                              defaults.get('enable_performance_metrics', True)))
            }
            
            logger.debug(f"✅ Debugging settings: {settings}")
            return settings
            
        except Exception as e:
            logger.error(f"❌ Error loading debugging settings: {e}")
            # Return safe defaults
            return {
                'enable_detailed_logging': False,
                'log_analysis_steps': False,
                'include_reasoning_in_response': True,
                'enable_performance_metrics': True
            }
    
    # ========================================================================
    # FEATURE FLAGS
    # ========================================================================
    
    def get_experimental_features(self) -> Dict[str, Any]:
        """
        Get experimental feature flags for analysis
        
        Returns:
            Dictionary with experimental feature configuration
        """
        try:
            config_raw = self.config_manager.get_configuration('analysis_parameters')
            feature_config = config_raw.get('feature_flags', {})
            experimental_config = feature_config.get('experimental_analysis_features', {})
            defaults = experimental_config.get('defaults', {})
            
            features = {
                'enable_advanced_context_analysis': self._parse_bool(experimental_config.get('enable_advanced_context_analysis', 
                                                                                            defaults.get('enable_advanced_context_analysis', False))),
                'enable_community_vocabulary_boost': self._parse_bool(experimental_config.get('enable_community_vocabulary_boost', 
                                                                                             defaults.get('enable_community_vocabulary_boost', False))),
                'enable_temporal_pattern_detection': self._parse_bool(experimental_config.get('enable_temporal_pattern_detection', 
                                                                                             defaults.get('enable_temporal_pattern_detection', False))),
                'enable_multi_language_support': self._parse_bool(experimental_config.get('enable_multi_language_support', 
                                                                                         defaults.get('enable_multi_language_support', False)))
            }
            
            logger.debug(f"✅ Experimental features: {features}")
            return features
            
        except Exception as e:
            logger.error(f"❌ Error loading experimental features: {e}")
            # Return safe defaults
            return {
                'enable_advanced_context_analysis': False,
                'enable_community_vocabulary_boost': False,
                'enable_temporal_pattern_detection': False,
                'enable_multi_language_support': False
            }
    
    # ========================================================================
    # VALIDATION METHODS
    # ========================================================================
    
    def validate_parameters(self) -> Dict[str, Any]:
        """
        Validate all analysis parameters for consistency and valid ranges
        
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Validate crisis thresholds
            thresholds = self.get_crisis_thresholds()
            if not (0.0 <= thresholds['low'] <= thresholds['medium'] <= thresholds['high'] <= 1.0):
                validation_result['errors'].append("Crisis thresholds must be in range [0.0-1.0] with high > medium > low")
                validation_result['valid'] = False
            
            # Validate phrase extraction parameters
            phrase_params = self.get_phrase_extraction_parameters()
            if phrase_params['min_phrase_length'] >= phrase_params['max_phrase_length']:
                validation_result['errors'].append("Phrase extraction: min_phrase_length must be < max_phrase_length")
                validation_result['valid'] = False
            
            # Validate pattern learning parameters
            pattern_params = self.get_pattern_learning_parameters()
            conf_thresholds = pattern_params['confidence_thresholds']
            if not (conf_thresholds['high_confidence'] > conf_thresholds['medium_confidence'] > conf_thresholds['low_confidence']):
                validation_result['errors'].append("Pattern learning confidence thresholds must be: high > medium > low")
                validation_result['valid'] = False
            
            # Validate performance settings
            perf_settings = self.get_performance_settings()
            if perf_settings['analysis_timeout_ms'] < 1000:
                validation_result['warnings'].append("Analysis timeout is very low, may cause timeouts")
            
            logger.info(f"✅ Parameter validation completed: {'PASSED' if validation_result['valid'] else 'FAILED'}")
            
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {e}")
            validation_result['valid'] = False
        
        return validation_result
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _parse_bool(self, value: Any) -> bool:
        """Parse boolean value from configuration"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all analysis parameters in a single dictionary
        
        Returns:
            Dictionary containing all analysis parameter categories
        """
        return {
            'crisis_thresholds': self.get_crisis_thresholds(),
            'phrase_extraction': self.get_phrase_extraction_parameters(),
            'pattern_learning': self.get_pattern_learning_parameters(),
            'semantic_analysis': self.get_semantic_analysis_parameters(),
            'advanced_parameters': self.get_advanced_parameters(),
            'integration_settings': self.get_integration_settings(),
            'performance_settings': self.get_performance_settings(),
            'debugging_settings': self.get_debugging_settings(),
            'experimental_features': self.get_experimental_features()
        }


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_analysis_parameters_manager(config_manager) -> AnalysisParametersManager:
    """
    Factory function to create AnalysisParametersManager instance
    
    Args:
        config_manager: ConfigManager instance for dependency injection
        
    Returns:
        AnalysisParametersManager instance
    """
    return AnalysisParametersManager(config_manager)


# ============================================================================
# CLEAN ARCHITECTURE EXPORTS (Phase 3b)
# ============================================================================

__all__ = [
    'AnalysisParametersManager',
    'create_analysis_parameters_manager'
]

# ============================================================================
# PHASE 3B IMPLEMENTATION COMPLETE
# ============================================================================

logger.info("✅ AnalysisParametersManager v3.1 - Phase 3b Implementation Complete")
logger.info("🔄 Analysis parameters migrated from hardcoded constants to JSON configuration")
logger.debug("📋 All analysis parameters now configurable via JSON + environment variables")
logger.debug("🎯 Ready for integration with SettingsManager and analysis components")