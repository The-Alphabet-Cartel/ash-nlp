# ash-nlp/analysis/__init__.py
"""
Analysis Package for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

# Core analysis components
from .crisis_analyzer import CrisisAnalyzer

# ============================================================================
# ANALYSIS METADATA - Phase 3d Step 7 Enhanced
# ============================================================================

ANALYSIS_CAPABILITIES = {
    "crisis_analyzer": {
        "description": "Enhanced crisis analysis using three zero-shot model ensemble with comprehensive manager integration",
        "input": "text_message",
        "output": "crisis_level_with_confidence_and_feature_flags",
        "features": [
            "three_model_ensemble_analysis",
            "context_signal_extraction", 
            "advanced_idiom_detection",
            "safety_first_scoring",
            "community_pattern_integration",
            "configurable_analysis_parameters",
            "mode_aware_threshold_mapping",
            "dynamic_feature_flags",  # Phase 3d Step 7
            "adaptive_performance_settings"  # Phase 3d Step 7
        ],
        "processing_time": "<80ms (configurable via performance settings)",
        "accuracy_target": "75%+ (enhanced with pattern integration)"
    },
    "feature_management": {  # Phase 3d Step 7
        "description": "Dynamic feature flag management for crisis analysis components",
        "capabilities": [
            "ensemble_analysis_toggle",
            "pattern_integration_control",
            "experimental_feature_flags",
            "development_debug_options"
        ]
    },
    "performance_optimization": {  # Phase 3d Step 7
        "description": "Adaptive performance settings for optimal crisis detection",
        "capabilities": [
            "configurable_analysis_timeouts",
            "concurrent_request_management",
            "cache_optimization",
            "gpu_optimization_controls"
        ]
    }
}

ANALYSIS_WORKFLOWS = {
    "enhanced_crisis_detection": {  # Updated for Phase 3d Step 7
        "steps": [
            "check_feature_flags",
            "apply_performance_settings",
            "extract_context_signals",
            "run_three_model_ensemble", 
            "apply_crisis_pattern_analysis",
            "use_mode_aware_thresholds",
            "combine_ensemble_results",
            "apply_pattern_adjustments",
            "map_to_crisis_level",
            "determine_staff_review_requirement"
        ],
        "primary_component": "CrisisAnalyzer",
        "phase": "3d.7"
    },
    
    "feature_controlled_analysis": {  # New Phase 3d Step 7
        "steps": [
            "validate_feature_flags",
            "select_analysis_components",
            "apply_performance_constraints",
            "execute_enabled_features",
            "provide_feature_status_feedback"
        ],
        "primary_component": "CrisisAnalyzer + FeatureConfigManager"
    },
    
    "performance_optimized_detection": {  # New Phase 3d Step 7
        "steps": [
            "check_performance_profile",
            "apply_timeout_settings",
            "manage_concurrent_requests",
            "optimize_cache_usage",
            "monitor_processing_time"
        ],
        "primary_component": "CrisisAnalyzer + PerformanceConfigManager"
    },

    "keyword_discovery": {
        "steps": [
            "extract_candidate_phrases",
            "score_with_models",
            "filter_by_confidence",
            "rank_by_relevance",
            "format_suggestions"
        ],
        "primary_component": "PhraseExtractor"
    }
}

# ============================================================================
# INFORMATION FUNCTIONS - Phase 3d Step 7 Enhanced
# ============================================================================

def get_analysis_capabilities():
    """Get detailed capabilities of all analysis components"""
    return ANALYSIS_CAPABILITIES

def get_analysis_workflows():
    """Get information about available analysis workflows"""
    return ANALYSIS_WORKFLOWS

def get_available_analyzers():
    """Get list of available analyzer classes"""
    return {
        "CrisisAnalyzer": "Enhanced crisis detection with three-model ensemble, feature flags, and performance optimization",
    }

def get_implemented_features():
    """Get detailed feature implementation status including Phase 3d Step 7"""
    return {
        "core_analysis": {
            "status": "implemented",
            "description": "Three-model ensemble crisis detection",
            "managers": ["ModelsManager", "CrisisPatternManager", "AnalysisParametersManager", "ThresholdMappingManager"]
        },
        "pattern_integration": {
            "status": "implemented", 
            "description": "JSON-based crisis pattern recognition",
            "managers": ["CrisisPatternManager"]
        },
        "configurable_parameters": {
            "status": "implemented",
            "description": "Externalized analysis parameters",
            "managers": ["AnalysisParametersManager"]
        },
        "threshold_management": {
            "status": "implemented",
            "description": "Mode-aware threshold mappings",
            "managers": ["ThresholdMappingManager"]
        },
        "feature_flags": {  # Phase 3d Step 7
            "status": "implemented",
            "description": "Dynamic feature toggle system for crisis analysis",
            "managers": ["FeatureConfigManager"],
            "capabilities": [
                "ensemble_analysis_control",
                "pattern_integration_toggle",
                "experimental_feature_management",
                "development_debug_controls"
            ]
        },
        "performance_optimization": {  # Phase 3d Step 7
            "status": "implemented", 
            "description": "Adaptive performance settings management",
            "managers": ["PerformanceConfigManager"],
            "capabilities": [
                "configurable_timeouts",
                "concurrent_request_management", 
                "cache_optimization",
                "gpu_optimization_controls"
            ]
        },
        "learning_system": {
            "status": "partial",
            "description": "Adaptive learning from community feedback",
            "managers": ["LearningManager"]
        }
    }

# ============================================================================
# FACTORY FUNCTIONS - Clean v3.1 Architecture with Phase 3d Step 7 Support
# ============================================================================

def create_crisis_analyzer(models_manager, crisis_pattern_manager=None, learning_manager=None, 
                          analysis_parameters_manager=None, threshold_mapping_manager=None,
                          feature_config_manager=None, performance_config_manager=None):
    """
    Create and return a CrisisAnalyzer instance with Phase 3d Step 7 support
    
    Args:
        models_manager: ML model manager for ensemble analysis
        crisis_pattern_manager: CrisisPatternManager for pattern-based analysis (Phase 3a)
        learning_manager: Optional learning manager for feedback
        analysis_parameters_manager: AnalysisParametersManager for configurable parameters (Phase 3b)
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds (Phase 3c)
        feature_config_manager: FeatureConfigManager for feature flags (Phase 3d Step 7)
        performance_config_manager: PerformanceConfigManager for performance settings (Phase 3d Step 7)
    """
    return CrisisAnalyzer(
        models_manager=models_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        learning_manager=learning_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager
    )

__all__ = [
    # Core analyzer classes
    "CrisisAnalyzer",
    "PhraseExtractor", 
    
    # Metadata
    "ANALYSIS_CAPABILITIES",
    "ANALYSIS_WORKFLOWS",
    
    # Information functions
    "get_analysis_capabilities",
    "get_analysis_workflows",
    "get_available_analyzers",
    "get_implemented_features",
    
    # Factory functions
    "create_crisis_analyzer",
]