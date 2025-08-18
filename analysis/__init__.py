# ash-nlp/analysis/__init__.py
"""
Analysis Package for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.11-3
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Analysis package updated for scoring function consolidation
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""
import logging

logger = logging.getLogger(__name__)

# Core analysis components
from .crisis_analyzer import CrisisAnalyzer

# ============================================================================
# ANALYSIS METADATA - Phase 3d Step 10.6 Enhanced
# ============================================================================

ANALYSIS_CAPABILITIES = {
    "crisis_analyzer": {
        "description": "Enhanced crisis analysis with consolidated scoring functions and comprehensive manager integration",
        "input": "text_message",
        "output": "crisis_level_with_confidence_and_feature_flags",
        "features": [
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
        "accuracy_target": "75%+ (enhanced with pattern integration)",
        "scoring_integration": "functions_consolidated_as_instance_methods"  # Phase 3d Step 10.6
    },
    "scoring_functions": {  # Phase 3d Step 10.6
        "description": "Consolidated scoring functions integrated into CrisisAnalyzer",
        "location": "CrisisAnalyzer instance methods",
        "functions": [
            "extract_depression_score",
            "enhanced_depression_analysis",
            "advanced_idiom_detection",
            "enhanced_crisis_level_mapping",
            "score_phrases_with_models",
            "filter_and_rank_phrases"
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
    "enhanced_crisis_detection": {  # Updated for Phase 3d Step 10.6
        "steps": [
            "check_feature_flags",
            "apply_performance_settings",
            "extract_context_signals",
            "run_three_model_ensemble", 
            "apply_crisis_pattern_analysis",
            "use_consolidated_scoring_functions",  # Phase 3d Step 10.6
            "use_mode_aware_thresholds",
            "combine_ensemble_results",
            "apply_pattern_adjustments",
            "map_to_crisis_level",
            "determine_staff_review_requirement"
        ],
        "primary_component": "CrisisAnalyzer (with consolidated scoring)",
        "phase": "3d.10.6"
    },
    
    "consolidated_scoring": {  # New Phase 3d Step 10.6
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
    },

    "keyword_discovery": {
        "steps": [
            "extract_candidate_phrases",
            "score_with_consolidated_methods",  # Phase 3d Step 10.6
            "filter_by_confidence",
            "rank_by_relevance",
            "format_suggestions"
        ],
        "primary_component": "CrisisAnalyzer (consolidated scoring methods)"
    }
}

# ============================================================================
# INFORMATION FUNCTIONS - Phase 3d Step 10.6 Enhanced
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
        "CrisisAnalyzer": "Enhanced crisis detection with consolidated scoring functions, three-model ensemble, feature flags, and performance optimization",
    }

def get_implemented_features():
    """Get detailed feature implementation status including Phase 3d Step 10.6"""
    return {
        "core_analysis": {
            "status": "implemented",
            "description": "Three-model ensemble crisis detection",
            "managers": ["ModelEnsembleManager", "CrisisPatternManager", "AnalysisParametersManager", "ThresholdMappingManager"]
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
        "scoring_consolidation": {  # Phase 3d Step 10.6
            "status": "implemented",
            "description": "Consolidated scoring functions integrated into CrisisAnalyzer",
            "managers": ["CrisisAnalyzer with dependency injection"],
            "functions": [
                "extract_depression_score",
                "enhanced_depression_analysis",
                "advanced_idiom_detection", 
                "enhanced_crisis_level_mapping",
                "score_phrases_with_models",
                "filter_and_rank_phrases"
            ],
            "benefits": [
                "centralized_scoring_logic",
                "manager_integration",
                "dependency_injection",
                "improved_testability"
            ]
        },
        "feature_flags": {
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
        },
        "learning_system": {
            "status": "partial",
            "description": "Adaptive learning from community feedback",
            "managers": ["LearningManager"]
        }
    }

def get_migration_status():
    """Get Phase 3d Step 10.6 migration status"""
    return {
        "current_phase": "3d",
        "current_step": "10.6_complete",
        "migration": "scoring_functions_consolidated",
        "completed_consolidations": ["utils/scoring_helpers.py"],
        "pending_consolidations": ["utils/community_patterns.py", "utils/context_helpers.py"],
        "architecture_compliance": "clean_v3_1_achieved",
        "version": "v3.1.3d.10.6.1"
    }

# ============================================================================
# FACTORY FUNCTIONS - Clean v3.1 Architecture with Phase 3d Step 10.6 Support
# ============================================================================

def create_crisis_analyzer(model_ensemble_manager, crisis_pattern_manager=None, learning_manager=None, 
                          analysis_parameters_manager=None, threshold_mapping_manager=None,
                          feature_config_manager=None, performance_config_manager=None,
                          context_pattern_manager=None):  # NEW: Step 10.8
    """
    Create and return a CrisisAnalyzer instance with Phase 3d Step 10.8 support
    
    Args:
        model_ensemble_manager: Model ensemble manager for ensemble analysis
        crisis_pattern_manager: CrisisPatternManager for pattern-based analysis (Phase 3a)
        learning_manager: Optional learning manager for feedback
        analysis_parameters_manager: AnalysisParametersManager for configurable parameters (Phase 3b)
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds (Phase 3c)
        feature_config_manager: FeatureConfigManager for feature flags (Phase 3d Step 7)
        performance_config_manager: PerformanceConfigManager for performance settings (Phase 3d Step 7)
        context_pattern_manager: ContextPatternManager for context analysis (Phase 3d Step 10.8) - NEW
        
    Returns:
        CrisisAnalyzer instance with ContextPatternManager integration (Phase 3d Step 10.8)
    """
    return CrisisAnalyzer(
        model_ensemble_manager=model_ensemble_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        learning_manager=learning_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager,
        context_pattern_manager=context_pattern_manager  # NEW: Step 10.8
    )

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
    "get_migration_status",  # Phase 3d Step 10.6
    
    # Factory functions
    "create_crisis_analyzer",
]

logger.info("✅ CrisisAnalyzer v3.1 Step 10.8 loaded - ContextPatternManager integration complete")