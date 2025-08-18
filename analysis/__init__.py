# ash-nlp/analysis/__init__.py
"""
Analysis Package for Ash-NLP Service v3.1
FILE VERSION: v3.1-3e-4.2-5
LAST MODIFIED: 2025-08-18
PHASE: 3e Step 4.2 - Enhanced analysis with consolidated methods and learning integration
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Phase 3e Step 4.2 - Analysis method consolidation with SharedUtilities and LearningSystem
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""
import logging

logger = logging.getLogger(__name__)

# Core analysis components
from .crisis_analyzer import CrisisAnalyzer

# ============================================================================
# ANALYSIS METADATA - Phase 3e Step 4.2 Enhanced
# ============================================================================

ANALYSIS_CAPABILITIES = {
    "crisis_analyzer": {
        "description": "Enhanced crisis analysis with consolidated analysis methods from multiple managers",
        "input": "text_message",
        "output": "crisis_level_with_learning_enhancement_and_shared_utilities",
        "features": [
            "consolidated_analysis_methods",  # Phase 3e Step 4.2 NEW
            "learning_system_integration",   # Phase 3e Step 4.2 NEW  
            "shared_utilities_integration",  # Phase 3e Step 4.2 NEW
            "three_model_ensemble_analysis",
            "context_signal_extraction", 
            "consolidated_scoring_functions",  # Phase 3d Step 10.6
            "safety_first_scoring",
            "community_pattern_integration",
            "configurable_analysis_parameters",
            "mode_aware_threshold_mapping",
            "dynamic_feature_flags",
            "adaptive_performance_settings"
        ],
        "processing_time": "<80ms (configurable via performance settings)",
        "accuracy_target": "80%+ (enhanced with learning and consolidated methods)",
        "consolidation_status": "12_methods_consolidated_from_3_managers"  # Phase 3e Step 4.2
    },
    
    "consolidated_analysis_methods": {  # Phase 3e Step 4.2 NEW
        "description": "Analysis methods consolidated from AnalysisParameters, ThresholdMapping, and ModelEnsemble managers",
        "location": "CrisisAnalyzer instance methods",
        "source_managers": ["AnalysisParametersManager", "ThresholdMappingManager", "ModelEnsembleManager"],
        "methods": {
            "from_analysis_parameters": [
                "get_analysis_crisis_thresholds",
                "get_analysis_timeouts", 
                "get_analysis_confidence_boosts",
                "get_analysis_pattern_weights",
                "get_analysis_algorithm_parameters"
            ],
            "from_threshold_mapping": [
                "apply_crisis_thresholds",
                "calculate_crisis_level_from_confidence",
                "validate_crisis_analysis_thresholds", 
                "get_crisis_threshold_for_mode"
            ],
            "from_model_ensemble": [
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

    "learning_system_integration": {  # Phase 3e Step 4.2 NEW
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

    "shared_utilities_integration": {  # Phase 3e Step 4.2 NEW
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

    "scoring_functions": {  # Phase 3d Step 10.6 (maintained)
        "description": "Consolidated scoring functions integrated into CrisisAnalyzer",
        "location": "CrisisAnalyzer instance methods",
        "functions": [
            "extract_depression_score",
            "enhanced_depression_analysis"
        ],
        "manager_integration": [
            "ThresholdMappingManager",
            "AnalysisParametersManager", 
            "CrisisPatternManager",
            "ModelEnsembleManager"
        ]
    },

    "feature_management": {
        "description": "Dynamic feature flag management for crisis analysis components",
        "capabilities": [
            "ensemble_analysis_toggle",
            "pattern_integration_control",
            "learning_system_toggle",  # Phase 3e Step 4.2 NEW
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
    "enhanced_crisis_detection": {  # Phase 3e Step 4.2 Enhanced
        "description": "Full crisis detection with consolidated methods and learning",
        "steps": [
            "validate_input_with_shared_utilities",     # Phase 3e Step 4.2 NEW
            "check_feature_flags",
            "apply_performance_settings", 
            "get_consolidated_analysis_parameters",     # Phase 3e Step 4.2 NEW
            "extract_context_signals",
            "run_enhanced_ensemble_analysis",           # Phase 3e Step 4.2 NEW
            "apply_crisis_pattern_analysis",
            "use_consolidated_scoring_functions",
            "apply_consolidated_thresholds",            # Phase 3e Step 4.2 NEW
            "integrate_learning_adjustments",           # Phase 3e Step 4.2 NEW
            "combine_ensemble_results",
            "apply_pattern_adjustments",
            "map_to_crisis_level",
            "determine_staff_review_requirement"
        ],
        "primary_component": "Enhanced CrisisAnalyzer with consolidated methods",
        "phase": "3e.4.2"
    },

    "learning_enhanced_analysis": {  # Phase 3e Step 4.2 NEW
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
    
    "consolidated_scoring": {  # Phase 3d Step 10.6 (maintained)
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

    "safe_analysis_execution": {  # Phase 3e Step 4.2 NEW
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
# INFORMATION FUNCTIONS - Phase 3e Step 4.2 Enhanced
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
    """Get detailed feature implementation status including Phase 3e Step 4.2"""
    return {
        "core_analysis": {
            "status": "implemented",
            "description": "Enhanced three-model ensemble crisis detection with consolidated methods",
            "managers": ["ModelEnsembleManager", "CrisisPatternManager", "AnalysisParametersManager", "ThresholdMappingManager"]
        },
        
        "consolidated_analysis_methods": {  # Phase 3e Step 4.2 NEW
            "status": "implemented",
            "description": "Analysis methods consolidated from multiple managers into CrisisAnalyzer",
            "source_managers": ["AnalysisParametersManager", "ThresholdMappingManager", "ModelEnsembleManager"],
            "methods_count": 12,
            "configuration_access": "UnifiedConfigManager via SharedUtilities",
            "benefits": [
                "centralized_analysis_logic",
                "reduced_inter_manager_dependencies",
                "improved_error_handling",
                "learning_system_integration"
            ]
        },

        "learning_system_integration": {  # Phase 3e Step 4.2 NEW
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

        "shared_utilities_integration": {  # Phase 3e Step 4.2 NEW
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
            "managers": ["CrisisPatternManager"]
        },

        "configurable_parameters": {
            "status": "enhanced",
            "description": "Externalized analysis parameters with consolidated access",
            "managers": ["AnalysisParametersManager", "SharedUtilitiesManager"],
            "enhancement": "consolidated_methods_in_crisis_analyzer"
        },

        "threshold_management": {
            "status": "enhanced",
            "description": "Mode-aware threshold mappings with learning integration",
            "managers": ["ThresholdMappingManager", "LearningSystemManager"],
            "enhancement": "learning_adjusted_thresholds"
        },

        "scoring_consolidation": {  # Phase 3d Step 10.6 (maintained)
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
                "learning_system_control",  # Phase 3e Step 4.2 NEW
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

def get_migration_status():
    """Get Phase 3e Step 4.2 migration status"""
    return {
        "current_phase": "3e",
        "current_step": "4.2_complete",
        "migration": "analysis_methods_consolidated_with_learning_integration",
        "completed_consolidations": [
            "utils/scoring_helpers.py",       # Phase 3d Step 10.6
            "utils/community_patterns.py",   # Phase 3d Step 10.7  
            "utils/context_helpers.py",      # Phase 3d Step 10.8
            "analysis_methods_consolidation" # Phase 3e Step 4.2 NEW
        ],
        "consolidated_methods": {
            "analysis_parameters_methods": 5,
            "threshold_mapping_methods": 4,
            "model_ensemble_methods": 3,
            "total_methods": 12
        },
        "new_integrations": [
            "SharedUtilitiesManager",
            "LearningSystemManager"
        ],
        "architecture_compliance": "clean_v3_1_enhanced",
        "version": "v3.1.3e.4.2.1"
    }

def get_consolidation_summary():
    """Get Phase 3e Step 4.2 consolidation summary"""
    return {
        "phase": "3e_step_4.2",
        "objective": "consolidate_analysis_methods_into_crisis_analyzer",
        "methods_consolidated": {
            "from_analysis_parameters_manager": [
                "get_analysis_crisis_thresholds",
                "get_analysis_timeouts",
                "get_analysis_confidence_boosts", 
                "get_analysis_pattern_weights",
                "get_analysis_algorithm_parameters"
            ],
            "from_threshold_mapping_manager": [
                "apply_crisis_thresholds",
                "calculate_crisis_level_from_confidence",
                "validate_crisis_analysis_thresholds",
                "get_crisis_threshold_for_mode"
            ],
            "from_model_ensemble_manager": [
                "perform_ensemble_crisis_analysis",
                "combine_ensemble_model_results", 
                "apply_analysis_ensemble_weights"
            ]
        },
        "new_capabilities": [
            "learning_system_integration",
            "shared_utilities_integration", 
            "enhanced_error_handling",
            "adaptive_threshold_adjustment"
        ],
        "configuration_access": "unified_via_shared_utilities_manager",
        "backward_compatibility": "maintained",
        "total_methods_added": 12,
        "dependencies_added": ["SharedUtilitiesManager", "LearningSystemManager"]
    }

# ============================================================================
# ENHANCED FACTORY FUNCTIONS - Phase 3e Step 4.2
# ============================================================================

def create_crisis_analyzer(unified_config, model_ensemble_manager, crisis_pattern_manager=None, 
                          analysis_parameters_manager=None, threshold_mapping_manager=None,
                          feature_config_manager=None, performance_config_manager=None,
                          context_pattern_manager=None,
                          # NEW Phase 3e Step 4.2 parameters
                          shared_utilities_manager=None, learning_system_manager=None):
    """
    Create and return an enhanced CrisisAnalyzer instance with Phase 3e Step 4.2 integration
    
    Phase 3e Enhancements:
    - Consolidated analysis methods from AnalysisParameters, ThresholdMapping, ModelEnsemble managers
    - SharedUtilitiesManager integration for error handling and configuration access
    - LearningSystemManager integration for adaptive learning and threshold adjustment
    - Enhanced crisis detection with learning feedback processing
    
    Args:
        # Existing parameters (maintained for backward compatibility)
        model_ensemble_manager: Model ensemble manager for ensemble analysis
        crisis_pattern_manager: CrisisPatternManager for pattern-based analysis (Phase 3a)
        analysis_parameters_manager: AnalysisParametersManager for configurable parameters (Phase 3b)
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds (Phase 3c)
        feature_config_manager: FeatureConfigManager for feature flags (Phase 3d Step 7)
        performance_config_manager: PerformanceConfigManager for performance settings (Phase 3d Step 7)
        context_pattern_manager: ContextPatternManager for context analysis (Phase 3d Step 10.8)
        
        # NEW Phase 3e Step 4.2 parameters
        shared_utilities_manager: SharedUtilitiesManager for common utilities and error handling
        learning_system_manager: LearningSystemManager for adaptive learning and feedback processing
        
    Returns:
        Enhanced CrisisAnalyzer instance with Phase 3e capabilities:
        - 12+ consolidated analysis methods
        - Learning system integration for adaptive analysis
        - Shared utilities for resilient error handling
        - Backward compatibility with existing functionality
    """
    return CrisisAnalyzer(
        unified_config,
        # Existing dependencies (maintained)
        model_ensemble_manager=model_ensemble_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager,
        context_pattern_manager=context_pattern_manager,
        
        # NEW Phase 3e Step 4.2 dependencies
        shared_utilities_manager=shared_utilities_manager,
        learning_system_manager=learning_system_manager
    )

def create_enhanced_crisis_analyzer(unified_config, model_ensemble_manager, shared_utilities_manager, 
                                        learning_system_manager, **kwargs):
    """
    Convenience factory function for Phase 3e enhanced CrisisAnalyzer
    
    This function emphasizes the new Phase 3e dependencies while maintaining
    backward compatibility with optional legacy dependencies.
    
    Args:
        model_ensemble_manager: Required - Model ensemble manager
        shared_utilities_manager: Required - SharedUtilitiesManager for Phase 3e
        learning_system_manager: Required - LearningSystemManager for Phase 3e
        **kwargs: Optional legacy managers for backward compatibility
        
    Returns:
        Enhanced CrisisAnalyzer with Phase 3e capabilities
    """
    return create_crisis_analyzer(
        unified_config,
        model_ensemble_manager=model_ensemble_manager,
        shared_utilities_manager=shared_utilities_manager,
        learning_system_manager=learning_system_manager,
        **kwargs
    )

def validate_crisis_analyzer_dependencies(unified_config=None, model_ensemble_manager=None, shared_utilities_manager=None,
                                         learning_system_manager=None, **kwargs):
    """
    Validate dependencies for CrisisAnalyzer creation
    
    Args:
        model_ensemble_manager: Model ensemble manager (required)
        shared_utilities_manager: SharedUtilitiesManager (recommended for Phase 3e)
        learning_system_manager: LearningSystemManager (recommended for Phase 3e)
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

    if not model_ensemble_manager:
        validation_result["valid"] = False
        validation_result["errors"].append("model_ensemble_manager is required")
    
    # Phase 3e recommendations
    if not shared_utilities_manager:
        validation_result["warnings"].append("shared_utilities_manager not provided - reduced error handling capabilities")
        validation_result["recommendations"].append("Include SharedUtilitiesManager for Phase 3e enhanced error handling")
    
    if not learning_system_manager:
        validation_result["warnings"].append("learning_system_manager not provided - no adaptive learning")
        validation_result["recommendations"].append("Include LearningSystemManager for Phase 3e adaptive learning capabilities")
    
    # Determine configuration phase
    if shared_utilities_manager and learning_system_manager:
        validation_result["phase"] = "3e_enhanced"
    elif kwargs.get("context_pattern_manager"):
        validation_result["phase"] = "3d_step_10.8"
    elif kwargs.get("feature_config_manager") or kwargs.get("performance_config_manager"):
        validation_result["phase"] = "3d_step_7+"
    elif kwargs.get("threshold_mapping_manager"):
        validation_result["phase"] = "3c+"
    elif kwargs.get("analysis_parameters_manager"):
        validation_result["phase"] = "3b+"
    elif kwargs.get("crisis_pattern_manager"):
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
    "get_migration_status",          # Phase 3d Step 10.6 + Phase 3e Step 4.2
    "get_consolidation_summary",     # Phase 3e Step 4.2 NEW
    
    # Factory functions
    "create_crisis_analyzer",                    # Enhanced for Phase 3e
    "create_enhanced_crisis_analyzer",       # Phase 3e Step 4.2 NEW
    "validate_crisis_analyzer_dependencies",     # Phase 3e Step 4.2 NEW
]

logger.info("✅ Enhanced Analysis Package v3.1-3e-4.2-1 loaded:")
logger.info("   🎯 12+ analysis methods consolidated into CrisisAnalyzer")
logger.info("   🧠 LearningSystemManager integration for adaptive analysis")
logger.info("   🛠️ SharedUtilitiesManager integration for resilient error handling")
logger.info("   🔄 Backward compatibility maintained with existing functionality")
logger.info("   📈 Phase 3e Step 4.2 analysis method consolidation complete!")