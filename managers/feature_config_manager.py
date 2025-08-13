# ash-nlp/managers/feature_config_manager.py
"""
Feature Configuration Manager for Ash NLP Service v3.1
Clean v3.1 Architecture - Updated for v3.1 Configuration Format
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
    Feature Configuration Manager for Ash NLP Service v3.1d - Updated for v3.1 Configuration Format
    
    Manages feature flags for crisis analysis system components with comprehensive validation and dependency management.
    Implements Clean v3.1 architecture patterns with dependency injection and fail-fast validation.
    
    Features:
    - Core system feature toggles
    - Analysis component feature flags  
    - Learning system feature management
    - Experimental feature management
    - Development and debug toggles
    - Feature dependency validation
    - Profile-based feature sets
    
    Updated for v3.1 configuration format with environment variable placeholders and comprehensive defaults.
    """
    
    def __init__(self, config_manager):
        """
        Initialize FeatureConfigManager with dependency injection
        
        Args:
            config_manager: UnifiedConfigManager instance for accessing configuration
        """
        self.config_manager = config_manager
        self.config_cache = {}
        self.validation_errors = []
        
        logger.info("🚩 Initializing FeatureConfigManager v3.1 (Updated for v3.1 Config Format)")
        
        try:
            self._load_feature_configuration()
            self._validate_feature_dependencies()
            logger.info("✅ FeatureConfigManager v3.1 initialization complete")
        except Exception as e:
            logger.error(f"❌ FeatureConfigManager initialization failed: {e}")
            logger.info("🛡️ Falling back to safe defaults per Clean Architecture Charter Rule #5")
            self._initialize_safe_defaults()
    
    def _load_feature_configuration(self):
        """Load feature flag configuration from v3.1 JSON with environment overrides"""
        try:
            # Load feature flags configuration through UnifiedConfigManager
            feature_config_raw = self.config_manager.load_config_file('feature_flags')
            
            if not feature_config_raw:
                logger.error("❌ Could not load feature_flags.json configuration")
                raise ValueError("Feature flags configuration not available")
            
            # Extract feature flags configuration - Updated for v3.1 format
            if 'feature_flags' in feature_config_raw:
                self.config_cache = feature_config_raw['feature_flags']
            else:
                # Handle direct configuration format or legacy format
                self.config_cache = feature_config_raw
                
            logger.debug("✅ Feature flags v3.1 configuration loaded successfully")
            logger.debug(f"🔍 Configuration keys loaded: {list(self.config_cache.keys())}")
            
            # Validate v3.1 structure
            if not self._validate_v31_structure():
                logger.warning("⚠️ Configuration doesn't match v3.1 format, using resilient fallbacks")
                
        except Exception as e:
            logger.error(f"❌ Failed to load feature flags configuration: {e}")
            raise
    
    def _validate_v31_structure(self) -> bool:
        """Validate that configuration matches v3.1 format"""
        required_sections = [
            'core_system_features',
            'analysis_component_features', 
            'learning_features',
            'experimental_features',
            'development_debug_features'
        ]
        
        for section in required_sections:
            if section not in self.config_cache:
                logger.warning(f"⚠️ Missing v3.1 section: {section}")
                return False
                
        return True
    
    def _initialize_safe_defaults(self):
        """Initialize safe default configuration per Clean Architecture Charter Rule #5"""
        self.config_cache = {
            'core_system_features': {
                'defaults': {
                    'ensemble_analysis': True,
                    'pattern_integration': True,
                    'staff_review_logic': True,
                    'safety_controls': True
                }
            },
            'analysis_component_features': {
                'defaults': {
                    'pattern_analysis': True,
                    'semantic_analysis': True,
                    'context_analysis': True,
                    'phrase_extraction': True,
                    'analysis_caching': True,
                    'parallel_processing': True
                }
            },
            'learning_features': {
                'defaults': {
                    'threshold_learning': False,
                    'pattern_learning': False
                }
            },
            'experimental_features': {
                'defaults': {
                    'advanced_context': False,
                    'community_vocab': True,
                    'temporal_patterns': True,
                    'multi_language': False
                }
            },
            'development_debug_features': {
                'defaults': {
                    'detailed_logging': True,
                    'performance_metrics': True,
                    'reload_on_changes': False,
                    'flip_sentiment_logic': False
                }
            }
        }
        logger.info("✅ Safe defaults initialized for resilient operation")
    
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
    # CORE SYSTEM FEATURES - Updated for v3.1
    # ========================================================================
    
    def is_ensemble_analysis_enabled(self) -> bool:
        """Check if three-model ensemble analysis is enabled"""
        return self._get_feature_flag('core_system_features', 'ensemble_analysis', True)
    
    def is_pattern_integration_enabled(self) -> bool:
        """Check if crisis pattern integration is enabled"""
        return self._get_feature_flag('core_system_features', 'pattern_integration', True)
    
    def is_staff_review_logic_enabled(self) -> bool:
        """Check if staff review logic is enabled"""
        return self._get_feature_flag('core_system_features', 'staff_review_logic', True)
    
    def is_safety_controls_enabled(self) -> bool:
        """Check if safety controls and validation are enabled"""
        return self._get_feature_flag('core_system_features', 'safety_controls', True)
    
    def get_core_system_features(self) -> Dict[str, bool]:
        """Get all core system feature flags"""
        return {
            'ensemble_analysis': self.is_ensemble_analysis_enabled(),
            'pattern_integration': self.is_pattern_integration_enabled(),
            'staff_review_logic': self.is_staff_review_logic_enabled(),
            'safety_controls': self.is_safety_controls_enabled()
        }
    
    # ========================================================================
    # ANALYSIS COMPONENT FEATURES - Updated for v3.1
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
            'analysis_caching': self.is_analysis_caching_enabled(),
            'parallel_processing': self.is_parallel_processing_enabled()
        }
    
    # ========================================================================
    # LEARNING FEATURES - New for v3.1
    # ========================================================================
    
    def is_threshold_learning_enabled(self) -> bool:
        """Check if threshold learning is enabled"""
        return self._get_feature_flag('learning_features', 'threshold_learning', False)
    
    def is_pattern_learning_enabled(self) -> bool:
        """Check if pattern learning is enabled"""
        return self._get_feature_flag('learning_features', 'pattern_learning', False)
    
    def get_learning_features(self) -> Dict[str, bool]:
        """Get all learning feature flags"""
        return {
            'threshold_learning': self.is_threshold_learning_enabled(),
            'pattern_learning': self.is_pattern_learning_enabled()
        }
    
    # ========================================================================
    # EXPERIMENTAL FEATURES - Updated for v3.1
    # ========================================================================
    
    def is_advanced_context_enabled(self) -> bool:
        """Check if advanced context analysis is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'advanced_context', False)
    
    def is_community_vocab_enabled(self) -> bool:
        """Check if community vocabulary analysis is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'community_vocab', True)
    
    def is_temporal_patterns_enabled(self) -> bool:
        """Check if temporal patterns analysis is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'temporal_patterns', True)
    
    def is_multi_language_enabled(self) -> bool:
        """Check if multi-language support is enabled (experimental)"""
        return self._get_feature_flag('experimental_features', 'multi_language', False)
    
    def get_experimental_features(self) -> Dict[str, bool]:
        """Get all experimental feature flags"""
        return {
            'advanced_context': self.is_advanced_context_enabled(),
            'community_vocab': self.is_community_vocab_enabled(),
            'temporal_patterns': self.is_temporal_patterns_enabled(),
            'multi_language': self.is_multi_language_enabled()
        }
    
    # ========================================================================
    # DEVELOPMENT & DEBUG FEATURES - Updated for v3.1
    # ========================================================================
    
    def is_detailed_logging_enabled(self) -> bool:
        """Check if detailed debug logging is enabled"""
        return self._get_feature_flag('development_debug_features', 'detailed_logging', True)
    
    def is_performance_metrics_enabled(self) -> bool:
        """Check if performance metrics collection is enabled"""
        return self._get_feature_flag('development_debug_features', 'performance_metrics', True)
    
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
            'reload_on_changes': self.is_reload_on_changes_enabled(),
            'flip_sentiment_logic': self.is_flip_sentiment_logic_enabled()
        }
    
    # ========================================================================
    # UTILITY METHODS - Updated for v3.1
    # ========================================================================
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a specific feature is enabled by name
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            Boolean indicating if feature is enabled
        """
        # Updated feature methods mapping for v3.1
        feature_methods = {
            # Core system features
            'ensemble_analysis': self.is_ensemble_analysis_enabled,
            'pattern_integration': self.is_pattern_integration_enabled,
            'staff_review_logic': self.is_staff_review_logic_enabled,
            'safety_controls': self.is_safety_controls_enabled,
            
            # Analysis component features
            'pattern_analysis': self.is_pattern_analysis_enabled,
            'semantic_analysis': self.is_semantic_analysis_enabled,
            'context_analysis': self.is_context_analysis_enabled,
            'phrase_extraction': self.is_phrase_extraction_enabled,
            'analysis_caching': self.is_analysis_caching_enabled,
            'parallel_processing': self.is_parallel_processing_enabled,
            
            # Learning features
            'threshold_learning': self.is_threshold_learning_enabled,
            'pattern_learning': self.is_pattern_learning_enabled,
            
            # Experimental features
            'advanced_context': self.is_advanced_context_enabled,
            'community_vocab': self.is_community_vocab_enabled,
            'temporal_patterns': self.is_temporal_patterns_enabled,
            'multi_language': self.is_multi_language_enabled,
            
            # Development debug features
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
            'learning_features': self.get_learning_features(),
            'experimental_features': self.get_experimental_features(),
            'development_debug_features': self.get_development_debug_features()
        }
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get feature categorization for management purposes"""
        return self.config_cache.get('feature_categories', {})
    
    def get_validation_errors(self) -> List[str]:
        """Get any feature dependency validation errors"""
        return self.validation_errors.copy()
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a feature profile from configuration
        
        Args:
            profile_name: Name of the profile to activate
            
        Returns:
            Boolean indicating if profile was activated successfully
        """
        try:
            profiles = self.config_cache.get('feature_profiles', {})
            if profile_name not in profiles:
                logger.warning(f"⚠️ Profile '{profile_name}' not found")
                return False
            
            profile = profiles[profile_name]
            logger.info(f"🔄 Activating feature profile: {profile_name}")
            
            # Profile activation would typically override current settings
            # For now, just log the profile settings
            logger.debug(f"📋 Profile '{profile_name}' settings: {profile}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error activating profile '{profile_name}': {e}")
            return False
    
    def _get_feature_flag(self, category: str, feature: str, default: bool) -> bool:
        """
        Internal method to get feature flag value with proper type conversion
        Handles v3.1 configuration format with environment variables and defaults
        
        Args:
            category: Feature category
            feature: Feature name
            default: Default value if not found
            
        Returns:
            Boolean feature flag value
        """
        try:
            category_config = self.config_cache.get(category, {})
            
            # First try to get the value directly (after environment substitution)
            value = category_config.get(feature)
            
            # If value is None or still has placeholder, fall back to defaults
            if value is None or (isinstance(value, str) and value.startswith('${') and value.endswith('}')):
                defaults = category_config.get('defaults', {})
                value = defaults.get(feature, default)
            
            # Convert to boolean if needed
            if isinstance(value, str):
                # Handle string boolean values
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
        config_manager: UnifiedConfigManager instance
        
    Returns:
        Initialized FeatureConfigManager instance
    """
    return FeatureConfigManager(config_manager)

# Export public interface
__all__ = ['FeatureConfigManager', 'create_feature_config_manager']