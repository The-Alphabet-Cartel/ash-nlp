# ash-nlp/managers/feature_config_manager.py - PHASE 3D STEP 7 COMPLETE
"""
Feature Configuration Manager for Ash NLP Service v3.1d - Phase 3d Step 7 Complete
Comprehensive feature flag management system with Clean v3.1 architecture

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class FeatureConfigManager:
    """
    Feature Configuration Manager for Ash NLP Service v3.1d - Phase 3d Step 7 Complete
    
    Manages feature flags for crisis analysis system components with comprehensive validation and dependency management.
    Implements Clean v3.1 architecture patterns with dependency injection and fail-fast validation.
    
    Features:
    - Core system feature toggles
    - Analysis component feature flags  
    - Experimental feature management
    - Development and debug toggles
    - Feature dependency validation
    - Profile-based feature sets
    """
    
    def __init__(self, config_manager):
        """
        Initialize FeatureConfigManager with dependency injection
        
        Args:
            config_manager: ConfigManager instance for accessing configuration
        """
        self.config_manager = config_manager
        self.config_cache = {}
        self.validation_errors = []
        
        logger.info("🚩 Initializing FeatureConfigManager (Phase 3d Step 7)")
        
        try:
            self._load_feature_configuration()
            self._validate_feature_dependencies()
            logger.info("✅ FeatureConfigManager initialization complete")
        except Exception as e:
            logger.error(f"❌ FeatureConfigManager initialization failed: {e}")
            raise
    
    def _load_feature_configuration(self):
        """Load feature flag configuration from JSON with environment overrides"""
        try:
            # Load feature flags configuration through ConfigManager using correct method
            feature_config_raw = self.config_manager.load_config_file('feature_flags')
            
            if not feature_config_raw:
                logger.error("❌ Could not load feature_flags.json configuration")
                raise ValueError("Feature flags configuration not available")
            
            # Extract feature flags configuration
            if 'feature_flags' in feature_config_raw:
                self.config_cache = feature_config_raw['feature_flags']
            else:
                # Direct configuration format
                self.config_cache = feature_config_raw
                
            logger.debug("✅ Feature flags configuration loaded successfully")
            logger.debug(f"🔍 Configuration keys loaded: {list(self.config_cache.keys())}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load feature flags configuration: {e}")
            # Initialize with safe defaults to prevent system failure
            self.config_cache = {
                'core_system_features': {
                    'defaults': {
                        'ensemble_analysis': True,
                        'pattern_integration': True,
                        'safety_controls': True
                    }
                },
                'analysis_component_features': {
                    'defaults': {
                        'pattern_analysis': True,
                        'semantic_analysis': True,
                        'phrase_extraction': True
                    }
                },
                'experimental_features': {
                    'defaults': {}
                },
                'development_debug_features': {
                    'defaults': {
                        'detailed_logging': False,
                        'performance_metrics': False,
                        'debug_output': False
                    }
                }
            }
            logger.warning("⚠️ Using fallback feature flag configuration")
            raise
    
    def _validate_feature_dependencies(self):
        """Validate feature dependencies and conflicts"""
        try:
            dependencies = self.config_cache.get('feature_dependencies', {}).get('dependencies', {})
            conflicts = self.config_cache.get('feature_dependencies', {}).get('conflicts', {})
            
            # Validate dependencies
            for feature, deps in dependencies.items():
                if self.is_feature_enabled(feature):
                    required_features = deps.get('requires', [])
                    for required in required_features:
                        if not self.is_feature_enabled(required):
                            error_msg = f"Feature '{feature}' requires '{required}' to be enabled"
                            self.validation_errors.append(error_msg)
                            logger.warning(f"⚠️ {error_msg}")
            
            # Validate conflicts
            for feature, conflict_list in conflicts.items():
                if self.is_feature_enabled(feature):
                    for conflicting in conflict_list:
                        if self.is_feature_enabled(conflicting):
                            error_msg = f"Feature '{feature}' conflicts with '{conflicting}'"
                            self.validation_errors.append(error_msg)
                            logger.warning(f"⚠️ {error_msg}")
            
            if self.validation_errors:
                logger.warning(f"⚠️ Feature validation found {len(self.validation_errors)} issues")
            else:
                logger.debug("✅ Feature dependency validation passed")
                
        except Exception as e:
            logger.warning(f"⚠️ Error during feature dependency validation: {e}")
    
    # ========================================================================
    # CORE SYSTEM FEATURES
    # ========================================================================
    
    def is_ensemble_analysis_enabled(self) -> bool:
        """Check if three-model ensemble analysis is enabled"""
        return self._get_feature_flag('core_system_features', 'ensemble_analysis', True)
    
    def is_pattern_integration_enabled(self) -> bool:
        """Check if crisis pattern integration is enabled"""
        return self._get_feature_flag('core_system_features', 'pattern_integration', True)
    
    def is_safety_controls_enabled(self) -> bool:
        """Check if safety controls and validation are enabled"""
        return self._get_feature_flag('core_system_features', 'safety_controls', True)
    
    def get_core_system_features(self) -> Dict[str, bool]:
        """Get all core system feature flags"""
        return {
            'ensemble_analysis': self.is_ensemble_analysis_enabled(),
            'pattern_integration': self.is_pattern_integration_enabled(),
            'safety_controls': self.is_safety_controls_enabled()
        }
    
    # ========================================================================
    # ANALYSIS COMPONENT FEATURES
    # ========================================================================
    
    def is_pattern_analysis_enabled(self) -> bool:
        """Check if pattern-based analysis is enabled"""
        return self._get_feature_flag('analysis_component_features', 'pattern_analysis', True)
    
    def is_semantic_analysis_enabled(self) -> bool:
        """Check if semantic analysis is enabled"""
        return self._get_feature_flag('analysis_component_features', 'semantic_analysis', True)
    
    def is_context_analysis_enabled(self) -> bool:
        """Check if context analysis is enabled"""
        return self._get_feature_flag('analysis_component_features', 'context_analysis', True)
    
    def is_phrase_extraction_enabled(self) -> bool:
        """Check if phrase extraction is enabled"""
        return self._get_feature_flag('analysis_component_features', 'phrase_extraction', True)
    
    def is_pattern_learning_enabled(self) -> bool:
        """Check if pattern learning is enabled"""
        return self._get_feature_flag('analysis_component_features', 'pattern_learning', True)
    
    def is_community_patterns_enabled(self) -> bool:
        """Check if community-specific patterns are enabled"""
        return self._get_feature_flag('analysis_component_features', 'community_patterns', True)
    
    def is_analysis_caching_enabled(self) -> bool:
        """Check if analysis result caching is enabled"""
        return self._get_feature_flag('analysis_component_features', 'analysis_caching', True)
    
    def is_parallel_processing_enabled(self) -> bool:
        """Check if parallel processing is enabled"""
        return self._get_feature_flag('analysis_component_features', 'parallel_processing', True)
    
    def get_analysis_component_features(self) -> Dict[str, bool]:
        """Get all analysis component feature flags"""
        return {
            'pattern_analysis': self.is_pattern_analysis_enabled(),
            'semantic_analysis': self.is_semantic_analysis_enabled(),
            'context_analysis': self.is_context_analysis_enabled(),
            'phrase_extraction': self.is_phrase_extraction_enabled(),
            'pattern_learning': self.is_pattern_learning_enabled(),
            'community_patterns': self.is_community_patterns_enabled(),
            'analysis_caching': self.is_analysis_caching_enabled(),
            'parallel_processing': self.is_parallel_processing_enabled()
        }
    
    # ========================================================================
    # EXPERIMENTAL FEATURES
    # ========================================================================
    
    def is_advanced_context_enabled(self) -> bool:
        """Check if advanced context analysis is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'advanced_context', False)
    
    def is_neural_patterns_enabled(self) -> bool:
        """Check if neural pattern detection is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'neural_patterns', False)
    
    def is_multi_language_enabled(self) -> bool:
        """Check if multi-language support is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'multi_language', False)
    
    def is_advanced_learning_enabled(self) -> bool:
        """Check if advanced learning algorithms are enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'advanced_learning', False)
    
    def is_real_time_adaptation_enabled(self) -> bool:
        """Check if real-time model adaptation is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'real_time_adaptation', False)
    
    def get_experimental_features(self) -> Dict[str, bool]:
        """Get all experimental feature flags"""
        return {
            'advanced_context': self.is_advanced_context_enabled(),
            'neural_patterns': self.is_neural_patterns_enabled(),
            'multi_language': self.is_multi_language_enabled(),
            'advanced_learning': self.is_advanced_learning_enabled(),
            'real_time_adaptation': self.is_real_time_adaptation_enabled()
        }
    
    # ========================================================================
    # DEVELOPMENT & DEBUG FEATURES
    # ========================================================================
    
    def is_detailed_logging_enabled(self) -> bool:
        """Check if detailed debug logging is enabled"""
        return self._get_feature_flag('development_debug_features', 'detailed_logging', False)
    
    def is_performance_metrics_enabled(self) -> bool:
        """Check if performance metrics collection is enabled"""
        return self._get_feature_flag('development_debug_features', 'performance_metrics', False)
    
    def is_debug_output_enabled(self) -> bool:
        """Check if debug output is enabled"""
        return self._get_feature_flag('development_debug_features', 'debug_output', False)
    
    def is_reload_on_changes_enabled(self) -> bool:
        """Check if configuration reload on changes is enabled"""
        return self._get_feature_flag('development_debug_features', 'reload_on_changes', False)
    
    def is_flip_sentiment_logic_enabled(self) -> bool:
        """Check if sentiment logic flipping is enabled (for testing)"""
        return self._get_feature_flag('development_debug_features', 'flip_sentiment_logic', False)
    
    def get_development_debug_features(self) -> Dict[str, bool]:
        """Get all development and debug feature flags"""
        return {
            'detailed_logging': self.is_detailed_logging_enabled(),
            'performance_metrics': self.is_performance_metrics_enabled(),
            'debug_output': self.is_debug_output_enabled(),
            'reload_on_changes': self.is_reload_on_changes_enabled(),
            'flip_sentiment_logic': self.is_flip_sentiment_logic_enabled()
        }
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a specific feature is enabled by name
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            Boolean indicating if feature is enabled
        """
        # Map feature names to their respective methods
        feature_methods = {
            'ensemble_analysis': self.is_ensemble_analysis_enabled,
            'pattern_integration': self.is_pattern_integration_enabled,
            'safety_controls': self.is_safety_controls_enabled,
            'pattern_analysis': self.is_pattern_analysis_enabled,
            'semantic_analysis': self.is_semantic_analysis_enabled,
            'context_analysis': self.is_context_analysis_enabled,
            'phrase_extraction': self.is_phrase_extraction_enabled,
            'pattern_learning': self.is_pattern_learning_enabled,
            'community_patterns': self.is_community_patterns_enabled,
            'analysis_caching': self.is_analysis_caching_enabled,
            'parallel_processing': self.is_parallel_processing_enabled,
            'advanced_context': self.is_advanced_context_enabled,
            'neural_patterns': self.is_neural_patterns_enabled,
            'multi_language': self.is_multi_language_enabled,
            'advanced_learning': self.is_advanced_learning_enabled,
            'real_time_adaptation': self.is_real_time_adaptation_enabled,
            'detailed_logging': self.is_detailed_logging_enabled,
            'performance_metrics': self.is_performance_metrics_enabled,
            'debug_output': self.is_debug_output_enabled,
            'reload_on_changes': self.is_reload_on_changes_enabled,
            'flip_sentiment_logic': self.is_flip_sentiment_logic_enabled
        }
        
        method = feature_methods.get(feature_name)
        if method:
            return method()
        else:
            logger.warning(f"⚠️ Unknown feature name: {feature_name}")
            return False
    
    def get_all_features(self) -> Dict[str, Dict[str, bool]]:
        """Get all feature flags organized by category"""
        return {
            'core_system_features': self.get_core_system_features(),
            'analysis_component_features': self.get_analysis_component_features(),
            'experimental_features': self.get_experimental_features(),
            'development_debug_features': self.get_development_debug_features()
        }
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get feature categorization for management purposes"""
        return self.config_cache.get('feature_categories', {})
    
    def get_validation_errors(self) -> List[str]:
        """Get any feature dependency validation errors"""
        return self.validation_errors.copy()
    
    def _get_feature_flag(self, category: str, feature: str, default: bool) -> bool:
        """
        Internal method to get feature flag value with proper type conversion
        
        Args:
            category: Feature category
            feature: Feature name
            default: Default value if not found
            
        Returns:
            Boolean feature flag value
        """
        try:
            category_config = self.config_cache.get(category, {})
            value = category_config.get(feature)
            
            if value is None:
                # Fall back to defaults
                defaults = category_config.get('defaults', {})
                value = defaults.get(feature, default)
            
            # Convert to boolean if needed
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
            elif isinstance(value, (int, float)):
                return bool(value)
            else:
                return bool(value)
                
        except Exception as e:
            logger.warning(f"⚠️ Error getting feature flag {category}.{feature}: {e}, using default: {default}")
            return default

def create_feature_config_manager(config_manager) -> FeatureConfigManager:
    """
    Factory function for FeatureConfigManager (Clean v3.1 Pattern)
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        Initialized FeatureConfigManager instance
    """
    return FeatureConfigManager(config_manager)

# Export public interface
__all__ = ['FeatureConfigManager', 'create_feature_config_manager']