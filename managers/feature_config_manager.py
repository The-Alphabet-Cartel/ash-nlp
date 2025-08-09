# managers/feature_config_manager.py - PHASE 3D STEP 7
"""
Phase 3d Step 7: Feature Configuration Manager
Clean v3.1 Architecture with comprehensive feature flag management

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

class FeatureConfigManager:
    """
    Feature Configuration Manager for Ash-NLP v3.1d Step 7
    
    Manages all feature flags and toggles with JSON configuration + environment overrides.
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
            # Load feature flags configuration through ConfigManager
            feature_config = self.config_manager.get_config('feature_flags')
            
            if not feature_config or 'feature_flags' not in feature_config:
                raise ValueError("Invalid feature_flags configuration - missing 'feature_flags' section")
            
            self.config_cache = feature_config['feature_flags']
            logger.debug("✅ Feature flags configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load feature flags configuration: {e}")
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
                            logger.warning(f"⚠️ Dependency validation warning: {error_msg}")
            
            # Validate conflicts
            for feature, conflict_info in conflicts.items():
                if self.is_feature_enabled(feature):
                    conflicting_features = conflict_info.get('conflicts_with', [])
                    for conflict in conflicting_features:
                        if self.is_feature_enabled(conflict):
                            error_msg = f"Feature '{feature}' conflicts with '{conflict}'"
                            self.validation_errors.append(error_msg)
                            logger.warning(f"⚠️ Conflict validation warning: {error_msg}")
            
            if self.validation_errors:
                logger.warning(f"⚠️ Feature dependency validation found {len(self.validation_errors)} issues")
            else:
                logger.debug("✅ Feature dependency validation passed")
                
        except Exception as e:
            logger.error(f"❌ Feature dependency validation failed: {e}")
            raise
    
    # ========================================================================
    # CORE SYSTEM FEATURES
    # ========================================================================
    
    def is_ensemble_analysis_enabled(self) -> bool:
        """Check if ensemble analysis is enabled"""
        return self._get_feature_flag('core_system_features', 'ensemble_analysis', True)
    
    def is_pattern_integration_enabled(self) -> bool:
        """Check if pattern integration is enabled"""
        return self._get_feature_flag('core_system_features', 'pattern_integration', True)
    
    def is_threshold_learning_enabled(self) -> bool:
        """Check if threshold learning is enabled"""
        return self._get_feature_flag('core_system_features', 'threshold_learning', True)
    
    def is_staff_review_logic_enabled(self) -> bool:
        """Check if staff review logic is enabled"""
        return self._get_feature_flag('core_system_features', 'staff_review_logic', True)
    
    def is_safety_controls_enabled(self) -> bool:
        """Check if safety controls are enabled"""
        return self._get_feature_flag('core_system_features', 'safety_controls', True)
    
    def get_core_system_features(self) -> Dict[str, bool]:
        """Get all core system feature flags"""
        return {
            'ensemble_analysis': self.is_ensemble_analysis_enabled(),
            'pattern_integration': self.is_pattern_integration_enabled(),
            'threshold_learning': self.is_threshold_learning_enabled(),
            'staff_review_logic': self.is_staff_review_logic_enabled(),
            'safety_controls': self.is_safety_controls_enabled()
        }
    
    # ========================================================================
    # ANALYSIS COMPONENT FEATURES
    # ========================================================================
    
    def is_pattern_analysis_enabled(self) -> bool:
        """Check if pattern analysis is enabled"""
        return self._get_feature_flag('analysis_component_features', 'pattern_analysis', True)
    
    def is_semantic_analysis_enabled(self) -> bool:
        """Check if semantic analysis is enabled"""
        return self._get_feature_flag('analysis_component_features', 'semantic_analysis', True)
    
    def is_phrase_extraction_enabled(self) -> bool:
        """Check if phrase extraction is enabled"""
        return self._get_feature_flag('analysis_component_features', 'phrase_extraction', True)
    
    def is_pattern_learning_enabled(self) -> bool:
        """Check if pattern learning is enabled"""
        return self._get_feature_flag('analysis_component_features', 'pattern_learning', True)
    
    def is_analysis_caching_enabled(self) -> bool:
        """Check if analysis caching is enabled"""
        return self._get_feature_flag('analysis_component_features', 'analysis_caching', True)
    
    def is_parallel_processing_enabled(self) -> bool:
        """Check if parallel processing is enabled"""
        return self._get_feature_flag('analysis_component_features', 'parallel_processing', True)
    
    def get_analysis_component_features(self) -> Dict[str, bool]:
        """Get all analysis component feature flags"""
        return {
            'pattern_analysis': self.is_pattern_analysis_enabled(),
            'semantic_analysis': self.is_semantic_analysis_enabled(),
            'phrase_extraction': self.is_phrase_extraction_enabled(),
            'pattern_learning': self.is_pattern_learning_enabled(),
            'analysis_caching': self.is_analysis_caching_enabled(),
            'parallel_processing': self.is_parallel_processing_enabled()
        }
    
    # ========================================================================
    # EXPERIMENTAL FEATURES
    # ========================================================================
    
    def is_experimental_advanced_context_enabled(self) -> bool:
        """Check if experimental advanced context is enabled"""
        return self._get_feature_flag('experimental_features', 'advanced_context', False)
    
    def is_experimental_community_vocab_enabled(self) -> bool:
        """Check if experimental community vocabulary is enabled"""
        return self._get_feature_flag('experimental_features', 'community_vocab', True)
    
    def is_experimental_temporal_patterns_enabled(self) -> bool:
        """Check if experimental temporal patterns are enabled"""
        return self._get_feature_flag('experimental_features', 'temporal_patterns', True)
    
    def is_experimental_multi_language_enabled(self) -> bool:
        """Check if experimental multi-language support is enabled"""
        return self._get_feature_flag('experimental_features', 'multi_language', False)
    
    def get_experimental_features(self) -> Dict[str, bool]:
        """Get all experimental feature flags"""
        return {
            'advanced_context': self.is_experimental_advanced_context_enabled(),
            'community_vocab': self.is_experimental_community_vocab_enabled(),
            'temporal_patterns': self.is_experimental_temporal_patterns_enabled(),
            'multi_language': self.is_experimental_multi_language_enabled()
        }
    
    # ========================================================================
    # DEVELOPMENT & DEBUG FEATURES
    # ========================================================================
    
    def is_detailed_logging_enabled(self) -> bool:
        """Check if detailed logging is enabled"""
        return self._get_feature_flag('development_debug_features', 'detailed_logging', True)
    
    def is_performance_metrics_enabled(self) -> bool:
        """Check if performance metrics are enabled"""
        return self._get_feature_flag('development_debug_features', 'performance_metrics', True)
    
    def is_reload_on_changes_enabled(self) -> bool:
        """Check if reload on changes is enabled"""
        return self._get_feature_flag('development_debug_features', 'reload_on_changes', False)
    
    def is_flip_sentiment_logic_enabled(self) -> bool:
        """Check if sentiment logic flipping is enabled"""
        return self._get_feature_flag('development_debug_features', 'flip_sentiment_logic', False)
    
    def get_development_debug_features(self) -> Dict[str, bool]:
        """Get all development and debug feature flags"""
        return {
            'detailed_logging': self.is_detailed_logging_enabled(),
            'performance_metrics': self.is_performance_metrics_enabled(),
            'reload_on_changes': self.is_reload_on_changes_enabled(),
            'flip_sentiment_logic': self.is_flip_sentiment_logic_enabled()
        }
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if any feature is enabled by name
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            Boolean indicating if feature is enabled
        """
        # Map feature names to their getter methods
        feature_methods = {
            'ensemble_analysis': self.is_ensemble_analysis_enabled,
            'pattern_integration': self.is_pattern_integration_enabled,
            'threshold_learning': self.is_threshold_learning_enabled,
            'staff_review_logic': self.is_staff_review_logic_enabled,
            'safety_controls': self.is_safety_controls_enabled,
            'pattern_analysis': self.is_pattern_analysis_enabled,
            'semantic_analysis': self.is_semantic_analysis_enabled,
            'phrase_extraction': self.is_phrase_extraction_enabled,
            'pattern_learning': self.is_pattern_learning_enabled,
            'analysis_caching': self.is_analysis_caching_enabled,
            'parallel_processing': self.is_parallel_processing_enabled,
            'advanced_context': self.is_experimental_advanced_context_enabled,
            'community_vocab': self.is_experimental_community_vocab_enabled,
            'temporal_patterns': self.is_experimental_temporal_patterns_enabled,
            'multi_language': self.is_experimental_multi_language_enabled,
            'detailed_logging': self.is_detailed_logging_enabled,
            'performance_metrics': self.is_performance_metrics_enabled,
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