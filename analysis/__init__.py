# ash-nlp/analysis/__init__.py
"""
Analysis Package for Ash-NLP Service v3.1
FILE VERSION: v3.1-4b-1
LAST MODIFIED: 2025-08-30
PHASE: 3e Step 4.2 - Enhanced analysis with consolidated methods and learning integration
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""
import logging

logger = logging.getLogger(__name__)

# Core analysis components
from .crisis_analyzer import CrisisAnalyzer

# ============================================================================
# ANALYSIS METADATA
# ============================================================================

ANALYSIS_CAPABILITIES = {
    "crisis_analyzer": {
        "description": "Enhanced crisis analysis with consolidated analysis methods from multiple managers",
        "input": "text_message",
        "output": "crisis_level_with_learning_enhancement_and_shared_utilities",
        "features": [
            "consolidated_analysis_methods",
            "learning_system_integration",
            "shared_utilities_integration",
            "three_model_coordination_analysis",
            "context_signal_extraction", 
            "consolidated_scoring_functions",
            "safety_first_scoring",
            "community_pattern_integration",
            "configurable_analysis_config",
            "mode_aware_crisis_threshold",
            "dynamic_feature_flags",
            "adaptive_performance_settings"
        ],
        "processing_time": "<80ms (configurable via performance settings)",
        "accuracy_target": "80%+ (enhanced with learning and consolidated methods)",
        "consolidation_status": "12_methods_consolidated_from_3_managers"
    },
    
    "consolidated_analysis_methods": {
        "description": "Analysis methods consolidated from AnalysisParameters, ThresholdMapping, and ModelEnsemble managers",
        "location": "CrisisAnalyzer instance methods",
        "source_managers": ["AnalysisConfigManager", "CrisisThresholdManager", "ModelCoordinationManager"],
        "methods": {
            "from_analysis_config": [
                "get_analysis_crisis_thresholds",
                "get_analysis_timeouts", 
                "get_analysis_confidence_boosts",
                "get_analysis_pattern_weights",
                "get_analysis_algorithm_parameters"
            ],
            "from_crisis_threshold": [
                "apply_crisis_thresholds",
                "calculate_crisis_level_from_confidence",
                "validate_crisis_analysis_thresholds", 
                "get_crisis_threshold_for_mode"
            ],
            "from_model_coordination": [
                "perform_ensemble_crisis_analysis",
                "combine_ensemble_model_results",
                "apply_analysis_ensemble_weights"
            ]
        },
        "benefits": [
            "centralized_analysis_logic",
            "shared_utilities_integration",
            "learning_system_enhancement",
            "configuration_standardization"
        ]
    },

    "learning_system_integration": {
        "description": "Adaptive learning system for crisis detection improvement",
        "capabilities": [
            "threshold_adjustment_based_on_feedback",
            "false_positive_reduction",
            "false_negative_mitigation", 
            "adaptive_confidence_scoring"
        ],
        "methods": [
            "analyze_message_with_learning",
            "process_analysis_feedback"
        ],
        "feedback_types": ["false_positive", "false_negative", "correct"]
    },

    "shared_utilities_integration": {
        "description": "Common utilities for error handling and configuration access",
        "capabilities": [
            "safe_analysis_execution",
            "standardized_input_validation",
            "unified_configuration_access",
            "resilient_error_handling"
        ],
        "utilities_used": [
            "execute_safely",
            "validate_type", 
            "get_config_section_safely"
        ]
    },

    "scoring_functions": {
        "description": "Consolidated scoring functions integrated into CrisisAnalyzer",
        "location": "CrisisAnalyzer instance methods",
        "functions": [
            "extract_depression_score",
            "enhanced_depression_analysis"
        ],
        "manager_integration": [
            "CrisisThresholdManager",
            "AnalysisConfigManager", 
            "PatternDetectionManager",
            "ModelCoordinationManager"
        ]
    },

    "feature_management": {
        "description": "Dynamic feature flag management for crisis analysis components",
        "capabilities": [
            "ensemble_analysis_toggle",
            "pattern_integration_control",
            "learning_system_toggle",
            "experimental_feature_flags",
            "development_debug_options"
        ]
    },

    "performance_optimization": {
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
    "enhanced_crisis_detection": {
        "description": "Full crisis detection with consolidated methods and learning",
        "steps": [
            "validate_input_with_shared_utilities",
            "check_feature_flags",
            "apply_performance_settings", 
            "get_consolidated_analysis_config",
            "extract_context_signals",
            "run_enhanced_ensemble_analysis",
            "apply_pattern_detection_analysis",
            "use_consolidated_scoring_functions",
            "apply_consolidated_thresholds",
            "integrate_learning_adjustments",
            "combine_ensemble_results",
            "apply_pattern_adjustments",
            "map_to_crisis_level",
            "determine_staff_review_requirement"
        ],
        "primary_component": "Enhanced CrisisAnalyzer with consolidated methods",
        "phase": "3e.4.2"
    },

    "learning_enhanced_analysis": {
        "description": "Crisis analysis with learning system integration",
        "steps": [
            "perform_base_ensemble_analysis",
            "apply_learning_threshold_adjustments",
            "integrate_false_positive_feedback",
            "integrate_false_negative_feedback", 
            "calculate_learning_adjusted_score",
            "process_feedback_for_future_learning"
        ],
        "primary_component": "CrisisAnalyzer + LearningSystemManager",
        "triggers": ["analyze_message_with_learning", "process_analysis_feedback"]
    },
    
    "consolidated_scoring": {
        "description": "Scoring functions now integrated as CrisisAnalyzer methods",
        "steps": [
            "access_via_crisis_analyzer_instance",
            "use_manager_dependency_injection",
            "apply_configurable_parameters",
            "utilize_smart_fallbacks"
        ],
        "benefits": [
            "centralized_scoring_logic",
            "manager_integration",
            "dependency_injection",
            "resilient_error_handling"
        ]
    },

    "safe_analysis_execution": {
        "description": "Error-resilient analysis using SharedUtilities patterns",
        "steps": [
            "validate_analysis_input",
            "execute_analysis_safely",
            "handle_errors_gracefully",
            "provide_safe_defaults",
            "log_issues_for_debugging"
        ],
        "primary_component": "CrisisAnalyzer + SharedUtilitiesManager"
    },
    
    "feature_controlled_analysis": {
        "steps": [
            "validate_feature_flags",
            "select_analysis_components",
            "apply_performance_constraints",
            "execute_enabled_features",
            "provide_feature_status_feedback"
        ],
        "primary_component": "CrisisAnalyzer + FeatureConfigManager"
    },
    
    "performance_optimized_detection": {
        "steps": [
            "check_performance_profile",
            "apply_timeout_settings",
            "manage_concurrent_requests",
            "optimize_cache_usage",
            "monitor_processing_time"
        ],
        "primary_component": "CrisisAnalyzer + PerformanceConfigManager"
    }
}

# ============================================================================
# INFORMATION FUNCTIONS
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
        "CrisisAnalyzer": "Enhanced crisis detection with consolidated analysis methods, learning system integration, shared utilities, and comprehensive manager integration",
    }

def get_implemented_features():
    """Get detailed feature implementation status"""
    return {
        "core_analysis": {
            "status": "implemented",
            "description": "Enhanced three-model ensemble crisis detection with consolidated methods",
            "managers": ["ModelCoordinationManager", "PatternDetectionManager", "AnalysisConfigManager", "CrisisThresholdManager"]
        },
        
        "consolidated_analysis_methods": {
            "status": "implemented",
            "description": "Analysis methods consolidated from multiple managers into CrisisAnalyzer",
            "source_managers": ["AnalysisConfigManager", "CrisisThresholdManager", "ModelCoordinationManager"],
            "methods_count": 12,
            "configuration_access": "UnifiedConfigManager via SharedUtilities",
            "benefits": [
                "centralized_analysis_logic",
                "reduced_inter_manager_dependencies",
                "improved_error_handling",
                "learning_system_integration"
            ]
        },

        "learning_system_integration": {
            "status": "implemented", 
            "description": "Adaptive learning system for crisis detection improvement",
            "managers": ["LearningSystemManager"],
            "capabilities": [
                "threshold_adjustment_based_on_feedback",
                "false_positive_reduction",
                "false_negative_mitigation",
                "adaptive_confidence_scoring"
            ],
            "feedback_processing": "real_time_learning_adjustments"
        },

        "shared_utilities_integration": {
            "status": "implemented",
            "description": "Common utilities for error handling and configuration access",
            "managers": ["SharedUtilitiesManager"],
            "utilities": [
                "safe_analysis_execution",
                "input_validation",
                "configuration_access",
                "error_handling_with_fallbacks"
            ],
            "benefits": [
                "consistent_error_handling",
                "reduced_duplicate_code",
                "standardized_configuration_access"
            ]
        },

        "pattern_integration": {
            "status": "implemented", 
            "description": "JSON-based crisis pattern recognition",
            "managers": ["PatternDetectionManager"]
        },

        "configurable_parameters": {
            "status": "enhanced",
            "description": "Externalized analysis parameters with consolidated access",
            "managers": ["AnalysisConfigManager", "SharedUtilitiesManager"],
            "enhancement": "consolidated_methods_in_crisis_analyzer"
        },

        "threshold_management": {
            "status": "enhanced",
            "description": "Mode-aware threshold mappings with learning integration",
            "managers": ["CrisisThresholdManager", "LearningSystemManager"],
            "enhancement": "learning_adjusted_thresholds"
        },

        "scoring_consolidation": {
            "status": "implemented",
            "description": "Consolidated scoring functions integrated into CrisisAnalyzer",
            "managers": ["CrisisAnalyzer with dependency injection"],
            "functions": [
                "extract_depression_score",
                "enhanced_depression_analysis"
            ],
            "benefits": [
                "centralized_scoring_logic",
                "manager_integration",
                "dependency_injection",
                "improved_testability"
            ]
        },

        "feature_flags": {
            "status": "enhanced",
            "description": "Dynamic feature toggle system with learning system control",
            "managers": ["FeatureConfigManager"],
            "capabilities": [
                "ensemble_analysis_control",
                "pattern_integration_toggle",
                "learning_system_control",
                "experimental_feature_management",
                "development_debug_controls"
            ]
        },

        "performance_optimization": {
            "status": "implemented", 
            "description": "Adaptive performance settings management",
            "managers": ["PerformanceConfigManager"],
            "capabilities": [
                "configurable_timeouts",
                "concurrent_request_management", 
                "cache_optimization",
                "gpu_optimization_controls"
            ]
        }
    }

# ============================================================================
# ENHANCED FACTORY FUNCTIONS
# ============================================================================

def create_crisis_analyzer(unified_config, model_coordination_manager, pattern_detection_manager=None, 
                          analysis_config_manager=None, crisis_threshold_manager=None,
                          feature_config_manager=None, performance_config_manager=None,
                          context_analysis_manager=None, shared_utilities_manager=None,
                          learning_system_manager=None, zero_shot_manager=None):
    """
    Create and return an enhanced CrisisAnalyzer instance
    
    Args:
        # Existing parameters (maintained for backward compatibility)
        model_coordination_manager: Model ensemble manager for ensemble analysis
        pattern_detection_manager: PatternDetectionManager for pattern-based analysis (Phase 3a)
        analysis_config_manager: AnalysisConfigManager for configurable parameters (Phase 3b)
        crisis_threshold_manager: CrisisThresholdManager for mode-aware thresholds (Phase 3c)
        feature_config_manager: FeatureConfigManager for feature flags (Phase 3d Step 7)
        performance_config_manager: PerformanceConfigManager for performance settings (Phase 3d Step 7)
        context_analysis_manager: ContextAnalysisManager for context analysis (Phase 3d Step 10.8)
        shared_utilities_manager: SharedUtilitiesManager for common utilities and error handling
        learning_system_manager: LearningSystemManager for adaptive learning and feedback processing
        
    Returns:
        Enhanced CrisisAnalyzer instance
    """
    return CrisisAnalyzer(
        unified_config,
        # Existing dependencies (maintained)
        model_coordination_manager=model_coordination_manager,
        pattern_detection_manager=pattern_detection_manager,
        analysis_config_manager=analysis_config_manager,
        crisis_threshold_manager=crisis_threshold_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager,
        context_analysis_manager=context_analysis_manager,
        shared_utilities_manager=shared_utilities_manager,
        learning_system_manager=learning_system_manager,
        zero_shot_manager=zero_shot_manager
    )

def create_enhanced_crisis_analyzer(unified_config, model_coordination_manager, shared_utilities_manager, 
                                        learning_system_manager, **kwargs):
    """
    Convenience factory function for CrisisAnalyzer
    
    Args:
        model_coordination_manager: Required - Model ensemble manager
        shared_utilities_manager: Required - SharedUtilitiesManager
        learning_system_manager: Required - LearningSystemManager
        **kwargs: Optional legacy managers for backward compatibility
        
    Returns:
        CrisisAnalyzer
    """
    return create_crisis_analyzer(
        unified_config,
        model_coordination_manager=model_coordination_manager,
        shared_utilities_manager=shared_utilities_manager,
        learning_system_manager=learning_system_manager,
        **kwargs
    )

def validate_crisis_analyzer_dependencies(unified_config=None, model_coordination_manager=None, shared_utilities_manager=None,
                                         learning_system_manager=None, **kwargs):
    """
    Validate dependencies for CrisisAnalyzer creation
    
    Args:
        model_coordination_manager: Model ensemble manager
        shared_utilities_manager: SharedUtilitiesManager
        learning_system_manager: LearningSystemManager
        **kwargs: Other optional managers
        
    Returns:
        Dictionary with validation results and recommendations
    """
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "recommendations": [],
        "phase": "unknown"
    }
    
    # Required dependencies
    if not unified_config:
        validation_result["valid"] = False
        validation_result["errors"].append("unified_config_manager is required")

    if not model_coordination_manager:
        validation_result["valid"] = False
        validation_result["errors"].append("model_coordination_manager is required")
    
    if not shared_utilities_manager:
        validation_result["warnings"].append("shared_utilities_manager not provided - reduced error handling capabilities")
        validation_result["recommendations"].append("Include SharedUtilitiesManager")
    
    if not learning_system_manager:
        validation_result["warnings"].append("learning_system_manager not provided - no adaptive learning")
        validation_result["recommendations"].append("Include LearningSystemManager")
    
    # Determine configuration phase
    if shared_utilities_manager and learning_system_manager:
        validation_result["phase"] = "3e_enhanced"
    elif kwargs.get("context_analysis_manager"):
        validation_result["phase"] = "3d_step_10.8"
    elif kwargs.get("feature_config_manager") or kwargs.get("performance_config_manager"):
        validation_result["phase"] = "3d_step_7+"
    elif kwargs.get("crisis_threshold_manager"):
        validation_result["phase"] = "3c+"
    elif kwargs.get("analysis_config_manager"):
        validation_result["phase"] = "3b+"
    elif kwargs.get("pattern_detection_manager"):
        validation_result["phase"] = "3a+"
    else:
        validation_result["phase"] = "basic"
    
    return validation_result

__all__ = [
    # Core analyzer classes
    "CrisisAnalyzer",
    
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
    "create_enhanced_crisis_analyzer",
    "validate_crisis_analyzer_dependencies",
]

logger.info("✅ Analysis Package Loaded:")