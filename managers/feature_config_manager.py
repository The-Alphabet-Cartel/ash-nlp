# ash-nlp/managers/feature_config_manager.py
"""
Feature Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3e-5.5-5
LAST MODIFIED: 2025-08-20
PHASE: 3e, Sub-step 5.5, Task 5 - FeatureConfigManager Standard Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Phase 3e cleanup complete - get_config_section patterns applied
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class FeatureConfigManager:
    """
    Feature Configuration Manager for Ash NLP Service
    
    Phase 3e Sub-step 5.5: Enhanced with get_config_section() patterns and improved feature management
    
    Manages feature flags for crisis analysis system components with comprehensive validation and dependency management.
    Implements Clean v3.1 architecture patterns with dependency injection and fail-fast validation.
    
    Features managed:
    - Core system feature toggles (ensemble analysis, pattern integration, staff review logic)
    - Analysis component feature flags (pattern analysis, semantic analysis, context analysis)
    - Learning system feature management (threshold learning, pattern learning)
    - Experimental feature management (advanced context, community vocab, temporal patterns)
    - Development and debug toggles (detailed logging, performance metrics, reload behavior)
    - Feature dependency validation and conflict detection
    - Profile-based feature sets for different deployment scenarios
    
    Phase 3e Improvements:
    - Replaced load_config_file() with get_config_section() patterns
    - Enhanced error handling and resilience for feature flag access
    - Improved fallback mechanisms for safe operation
    - Better integration with UnifiedConfigManager
    - Added comprehensive feature validation and monitoring
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
        
        logger.info("Initializing FeatureConfigManager v3.1e-5.5 with Phase 3e patterns")
        
        try:
            self._load_feature_configuration()
            self._validate_feature_dependencies()
            logger.info("FeatureConfigManager v3.1e-5.5 initialization complete")
        except Exception as e:
            logger.error(f"FeatureConfigManager initialization failed: {e}")
            logger.info("Falling back to safe defaults per Clean Architecture Charter Rule #5")
            self._initialize_safe_defaults()
    
    def _load_feature_configuration(self):
        """Load feature flag configuration using Phase 3e get_config_section patterns"""
        try:
            # PHASE 3E: Use get_config_section instead of load_config_file
            feature_config_raw = self.config_manager.get_config_section('feature_flags')
            
            if not feature_config_raw:
                logger.error("Could not load feature flags configuration")
                raise ValueError("Feature flags configuration not available")
            
            # Extract feature flags configuration - Enhanced for Phase 3e
            if 'features' in feature_config_raw:
                self.config_cache = self.config_manager.get_config_section('feature_flags', 'features', {}')
            else:
                # Handle direct configuration format
                self.config_cache = feature_config_raw
                
            logger.debug("Feature flags configuration loaded successfully using Phase 3e patterns")
            logger.debug(f"Configuration sections loaded: {list(self.config_cache.keys())}")
            
            # Validate configuration structure
            if not self._validate_configuration_structure():
                logger.warning("Configuration doesn't match expected format, using resilient fallbacks")
                
        except Exception as e:
            logger.error(f"Failed to load feature flags configuration: {e}")
            raise
    
    def _validate_configuration_structure(self) -> bool:
        """Validate that configuration matches expected structure for Phase 3e"""
        required_sections = [
            'core_system_features',
            'analysis_component_features', 
            'learning_features',
            'experimental_features',
            'development_debug_features'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in self.config_cache:
                missing_sections.append(section)
                
        if missing_sections:
            logger.warning(f"Missing configuration sections: {missing_sections}")
            return False
                
        return True
    
    def _initialize_safe_defaults(self):
        """Initialize safe default configuration per Clean Architecture Charter Rule #5"""
        self.config_cache = {
            'core_system_features': {
                'ensemble_analysis': True,
                'pattern_integration': True,
                'staff_review_logic': True,
                'safety_controls': True,
                'defaults': {
                    'ensemble_analysis': True,
                    'pattern_integration': True,
                    'staff_review_logic': True,
                    'safety_controls': True
                }
            },
            'analysis_component_features': {
                'pattern_analysis': True,
                'semantic_analysis': True,
                'context_analysis': True,
                'phrase_extraction': True,
                'analysis_caching': True,
                'parallel_processing': True,
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
                'threshold_learning': False,
                'pattern_learning': False,
                'defaults': {
                    'threshold_learning': False,
                    'pattern_learning': False
                }
            },
            'experimental_features': {
                'advanced_context': False,
                'community_vocab': True,
                'temporal_patterns': True,
                'multi_language': False,
                'defaults': {
                    'advanced_context': False,
                    'community_vocab': True,
                    'temporal_patterns': True,
                    'multi_language': False
                }
            },
            'development_debug_features': {
                'detailed_logging': True,
                'performance_metrics': True,
                'reload_on_changes': False,
                'flip_sentiment_logic': False,
                'defaults': {
                    'detailed_logging': True,
                    'performance_metrics': True,
                    'reload_on_changes': False,
                    'flip_sentiment_logic': False
                }
            }
        }
        logger.info("Safe defaults initialized for resilient operation")
    
    def _validate_feature_dependencies(self):
        """Validate feature dependencies and conflicts with enhanced error handling"""
        try:
            # PHASE 3E: Enhanced dependency validation using get_config_section patterns
            dependencies_config = self.config_manager.get_config_section('feature_flags', 'feature_dependencies', {})
            dependencies = dependencies_config.get('dependencies', {})
            conflicts = dependencies_config.get('conflicts', {})
            
            # Validate dependencies
            for feature, deps in dependencies.items():
                if self.is_feature_enabled(feature):
                    required_features = deps.get('requires', [])
                    for required in required_features:
                        if not self.is_feature_enabled(required):
                            error_msg = f"Feature '{feature}' requires '{required}' to be enabled"
                            self.validation_errors.append(error_msg)
                            logger.warning(f"Feature dependency error: {error_msg}")
            
            # Validate conflicts
            for feature, conflict_list in conflicts.items():
                if self.is_feature_enabled(feature):
                    for conflicting in conflict_list:
                        if self.is_feature_enabled(conflicting):
                            error_msg = f"Feature '{feature}' conflicts with '{conflicting}'"
                            self.validation_errors.append(error_msg)
                            logger.warning(f"Feature conflict error: {error_msg}")
            
            if self.validation_errors:
                logger.warning(f"Feature validation found {len(self.validation_errors)} issues")
            else:
                logger.debug("Feature dependency validation passed")
                
        except Exception as e:
            logger.warning(f"Error during feature dependency validation: {e}")
    
    # ========================================================================
    # CORE SYSTEM FEATURES (Phase 3e Enhanced)
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
        """Get all core system feature flags with enhanced error handling"""
        try:
            return {
                'ensemble_analysis': self.is_ensemble_analysis_enabled(),
                'pattern_integration': self.is_pattern_integration_enabled(),
                'staff_review_logic': self.is_staff_review_logic_enabled(),
                'safety_controls': self.is_safety_controls_enabled()
            }
        except Exception as e:
            logger.error(f"Error getting core system features: {e}")
            return {
                'ensemble_analysis': True,
                'pattern_integration': True,
                'staff_review_logic': True,
                'safety_controls': True
            }
    
    # ========================================================================
    # ANALYSIS COMPONENT FEATURES (Phase 3e Enhanced)
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
        """Get all analysis component feature flags with enhanced error handling"""
        try:
            return {
                'pattern_analysis': self.is_pattern_analysis_enabled(),
                'semantic_analysis': self.is_semantic_analysis_enabled(),
                'context_analysis': self.is_context_analysis_enabled(),
                'phrase_extraction': self.is_phrase_extraction_enabled(),
                'analysis_caching': self.is_analysis_caching_enabled(),
                'parallel_processing': self.is_parallel_processing_enabled()
            }
        except Exception as e:
            logger.error(f"Error getting analysis component features: {e}")
            return {
                'pattern_analysis': True,
                'semantic_analysis': True,
                'context_analysis': True,
                'phrase_extraction': True,
                'analysis_caching': True,
                'parallel_processing': True
            }
    
    # ========================================================================
    # LEARNING FEATURES (Phase 3e Enhanced)
    # ========================================================================
    
    def is_threshold_learning_enabled(self) -> bool:
        """Check if threshold learning is enabled"""
        return self._get_feature_flag('learning_features', 'threshold_learning', False)
    
    def is_pattern_learning_enabled(self) -> bool:
        """Check if pattern learning is enabled"""
        return self._get_feature_flag('learning_features', 'pattern_learning', False)
    
    def get_learning_features(self) -> Dict[str, bool]:
        """Get all learning feature flags with enhanced error handling"""
        try:
            return {
                'threshold_learning': self.is_threshold_learning_enabled(),
                'pattern_learning': self.is_pattern_learning_enabled()
            }
        except Exception as e:
            logger.error(f"Error getting learning features: {e}")
            return {
                'threshold_learning': False,
                'pattern_learning': False
            }
    
    # ========================================================================
    # EXPERIMENTAL FEATURES (Phase 3e Enhanced)
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
        """Get all experimental feature flags with enhanced error handling"""
        try:
            return {
                'advanced_context': self.is_advanced_context_enabled(),
                'community_vocab': self.is_community_vocab_enabled(),
                'temporal_patterns': self.is_temporal_patterns_enabled(),
                'multi_language': self.is_multi_language_enabled()
            }
        except Exception as e:
            logger.error(f"Error getting experimental features: {e}")
            return {
                'advanced_context': False,
                'community_vocab': True,
                'temporal_patterns': True,
                'multi_language': False
            }
    
    # ========================================================================
    # DEVELOPMENT & DEBUG FEATURES (Phase 3e Enhanced)
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
        """Get all development and debug feature flags with enhanced error handling"""
        try:
            return {
                'detailed_logging': self.is_detailed_logging_enabled(),
                'performance_metrics': self.is_performance_metrics_enabled(),
                'reload_on_changes': self.is_reload_on_changes_enabled(),
                'flip_sentiment_logic': self.is_flip_sentiment_logic_enabled()
            }
        except Exception as e:
            logger.error(f"Error getting development debug features: {e}")
            return {
                'detailed_logging': True,
                'performance_metrics': True,
                'reload_on_changes': False,
                'flip_sentiment_logic': False
            }
    
    # ========================================================================
    # UTILITY METHODS (Phase 3e Enhanced)
    # ========================================================================
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a specific feature is enabled by name with enhanced error handling
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            Boolean indicating if feature is enabled
        """
        try:
            # Enhanced feature methods mapping for Phase 3e
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
                logger.warning(f"Unknown feature name: {feature_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking feature {feature_name}: {e}")
            return False
    
    def get_all_features(self) -> Dict[str, Dict[str, bool]]:
        """Get all feature flags organized by category with enhanced error handling"""
        try:
            return {
                'core_system_features': self.get_core_system_features(),
                'analysis_component_features': self.get_analysis_component_features(),
                'learning_features': self.get_learning_features(),
                'experimental_features': self.get_experimental_features(),
                'development_debug_features': self.get_development_debug_features()
            }
        except Exception as e:
            logger.error(f"Error getting all features: {e}")
            return {
                'core_system_features': {},
                'analysis_component_features': {},
                'learning_features': {},
                'experimental_features': {},
                'development_debug_features': {}
            }
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get feature categorization for management purposes with enhanced access patterns"""
        try:
            # PHASE 3E: Use get_config_section pattern for feature categories
            categories = self.config_manager.get_config_section('feature_flags', 'feature_categories', {})
            if not categories:
                # Fallback to direct config cache access
                categories = self.config_cache.get('feature_categories', {})
            
            return categories
            
        except Exception as e:
            logger.error(f"Error getting feature categories: {e}")
            return {}
    
    def get_validation_errors(self) -> List[str]:
        """Get any feature dependency validation errors"""
        return self.validation_errors.copy()
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a feature profile from configuration with enhanced validation
        
        Args:
            profile_name: Name of the profile to activate
            
        Returns:
            Boolean indicating if profile was activated successfully
        
        NOT CURRENTLY USED!
        """
#        try:
#            # PHASE 3E: Enhanced profile access using get_config_section patterns
#            profiles = self.config_manager.get_config_section('feature_flags', 'feature_profiles', {})
#            if not profiles:
#                # Fallback to direct config cache access
#                profiles = self.config_cache.get('feature_profiles', {})
#                
#            if profile_name not in profiles:
#                logger.warning(f"Profile '{profile_name}' not found")
#                return False
#            
#            profile = profiles[profile_name]
#            logger.info(f"Activating feature profile: {profile_name}")
#            
#            # Profile activation would typically override current settings
#            # For now, just log the profile settings
#            logger.debug(f"Profile '{profile_name}' settings: {profile}")
#            return True
#            
#        except Exception as e:
#            logger.error(f"Error activating profile '{profile_name}': {e}")
        return False
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary for monitoring and debugging
        Phase 3e: New method for enhanced system visibility
        """
        try:
            all_features = self.get_all_features()
            
            return {
                'manager_version': 'v3.1e-5.5-3',
                'phase': '3e Sub-step 5.5 Task 5',
                'total_features': sum(len(category) for category in all_features.values()),
                'enabled_features': sum(
                    sum(1 for enabled in category.values() if enabled) 
                    for category in all_features.values()
                ),
                'validation_errors_count': len(self.validation_errors),
                'configuration_source': 'json_with_env_overrides',
                'feature_categories': list(all_features.keys()),
                'core_features_enabled': all(self.get_core_system_features().values()),
                'experimental_features_count': len(self.get_experimental_features()),
                'learning_features_enabled': any(self.get_learning_features().values()),
                'initialization_status': 'complete',
                'cleanup_status': 'phase_3e_complete'
            }
            
        except Exception as e:
            logger.error(f"Error generating configuration summary: {e}")
            return {
                'manager_version': 'v3.1e-5.5-3',
                'phase': '3e Sub-step 5.5 Task 5',
                'error': str(e),
                'initialization_status': 'error',
                'cleanup_status': 'phase_3e_complete'
            }
    
    def _get_feature_flag(self, category: str, feature: str, default: bool) -> bool:
        """
        Internal method to get feature flag value with enhanced Phase 3e type conversion
        Handles configuration format with environment variables and enhanced defaults
        
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
            
            # Enhanced type conversion for Phase 3e
            if isinstance(value, str):
                # Handle string boolean values
                return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
            elif isinstance(value, (int, float)):
                return bool(value)
            else:
                return bool(value)
                
        except Exception as e:
            logger.warning(f"Error getting feature flag {category}.{feature}: {e}, using default: {default}")
            return default

# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance (Phase 3e Enhanced)
# ============================================================================

def create_feature_config_manager(config_manager) -> FeatureConfigManager:
    """
    Factory function for FeatureConfigManager (Clean v3.1 Pattern) - Phase 3e Enhanced
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        Initialized FeatureConfigManager instance with Phase 3e enhancements
    """
    return FeatureConfigManager(config_manager)

# Export public interface
__all__ = ['FeatureConfigManager', 'create_feature_config_manager']

logger.info("FeatureConfigManager v3.1e-5.5-3 loaded - Phase 3e Sub-step 5.5 cleanup complete with enhanced patterns")