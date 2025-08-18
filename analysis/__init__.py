# ash-nlp/analysis/__init__.py
"""
Analysis module initialization for Ash-NLP Service v3.1
FILE VERSION: v3.1-3e-4.2-1
LAST MODIFIED: 2025-08-17
PHASE: 3e, Step 4.2 - Enhanced CrisisAnalyzer Factory with Consolidated Methods
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Phase 3e Step 4.2 COMPLETE - Enhanced factory function with SharedUtilities and LearningSystem
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, Optional

# Import core analyzer (updated for Phase 3e)
from .crisis_analyzer import CrisisAnalyzer
from .phrase_extractor import PhraseExtractor

logger = logging.getLogger(__name__)

# ============================================================================
# ANALYSIS CAPABILITIES - Updated for Phase 3e Step 4.2
# ============================================================================

ANALYSIS_CAPABILITIES = {
    "crisis_detection": {
        "status": "enhanced_phase_3e",
        "description": "Advanced crisis detection with consolidated analysis methods",
        "managers": [
            "ModelEnsembleManager", "CrisisPatternManager", "AnalysisParametersManager",
            "ThresholdMappingManager", "FeatureConfigManager", "PerformanceConfigManager",
            "ContextPatternManager", "SharedUtilitiesManager", "LearningSystemManager"
        ],
        "capabilities": [
            "three_model_ensemble_analysis",
            "json_based_pattern_matching",
            "mode_aware_thresholds",
            "context_pattern_integration",
            "consolidated_analysis_methods",        # NEW Phase 3e
            "learning_enhanced_thresholds",         # NEW Phase 3e
            "shared_utilities_integration",         # NEW Phase 3e
            "adaptive_confidence_boosts"            # NEW Phase 3e
        ]
    },
    "pattern_analysis": {
        "status": "implemented_with_consolidation",
        "description": "Comprehensive pattern analysis with consolidated scoring methods",
        "capabilities": [
            "crisis_keyword_detection",
            "context_pattern_analysis", 
            "temporal_indicator_processing",
            "community_vocabulary_recognition",
            "consolidated_scoring_functions",       # Phase 3d Step 10.6
            "learning_adapted_weights"              # NEW Phase 3e
        ]
    },
    "ensemble_analysis": {
        "status": "enhanced_phase_3e",
        "description": "Multi-model ensemble analysis with learning integration",
        "capabilities": [
            "consolidated_ensemble_methods",        # NEW Phase 3e
            "learning_enhanced_combinations",       # NEW Phase 3e
            "adaptive_model_weighting",            # NEW Phase 3e
            "performance_optimized_analysis"
        ]
    }
}

ANALYSIS_WORKFLOWS = {
    "enhanced_crisis_detection": {
        "steps": [
            "consolidated_ensemble_analysis",      # NEW Phase 3e method
            "learning_enhanced_threshold_application",  # NEW Phase 3e
            "adaptive_confidence_calculation",     # NEW Phase 3e
            "mode_specific_crisis_assessment",     # NEW Phase 3e
            "shared_utilities_validation"          # NEW Phase 3e
        ],
        "primary_component": "CrisisAnalyzer (Phase 3e Enhanced)",
        "learning_integration": True,               # NEW
        "shared_utilities_integration": True       # NEW
    },
    
    "adaptive_threshold_management": {              # NEW Phase 3e workflow
        "steps": [
            "get_mode_specific_crisis_thresholds",
            "apply_learning_system_adaptations",
            "calculate_crisis_level_from_confidence",
            "validate_crisis_analysis_thresholds"
        ],
        "primary_component": "CrisisAnalyzer + LearningSystemManager",
        "consolidation_source": ["AnalysisParametersManager", "ThresholdMappingManager"]
    },
    
    "consolidated_analysis_parameters": {          # NEW Phase 3e workflow
        "steps": [
            "get_analysis_crisis_thresholds",
            "get_analysis_confidence_boosts", 
            "get_analysis_pattern_weights",
            "get_analysis_algorithm_parameters"
        ],
        "primary_component": "CrisisAnalyzer + SharedUtilitiesManager",
        "consolidation_source": "AnalysisParametersManager"
    }
}

# ============================================================================
# ENHANCED FACTORY FUNCTION - Phase 3e Step 4.2
# ============================================================================

def create_crisis_analyzer(model_ensemble_manager, 
                          crisis_pattern_manager=None, 
                          learning_manager=None, 
                          analysis_parameters_manager=None, 
                          threshold_mapping_manager=None,
                          feature_config_manager=None, 
                          performance_config_manager=None,
                          context_pattern_manager=None,
                          # NEW Phase 3e dependencies
                          shared_utilities_manager=None,      # Step 2: SharedUtilitiesManager
                          learning_system_manager=None) -> CrisisAnalyzer:       # Step 3: LearningSystemManager
    """
    PHASE 3E STEP 4.2 ENHANCED: Create CrisisAnalyzer with consolidated analysis methods
    
    Enhanced factory function with SharedUtilities and LearningSystem integration
    Supports all consolidated analysis methods from AnalysisParameters, ThresholdMapping, and ModelEnsemble managers
    
    Args:
        model_ensemble_manager: Model ensemble manager for ensemble analysis
        crisis_pattern_manager: CrisisPatternManager for pattern-based analysis (Phase 3a)
        learning_manager: Optional learning manager for feedback (legacy)
        analysis_parameters_manager: AnalysisParametersManager for configurable parameters (Phase 3b)
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds (Phase 3c)
        feature_config_manager: FeatureConfigManager for feature flags (Phase 3d Step 7)
        performance_config_manager: PerformanceConfigManager for performance settings (Phase 3d Step 7)
        context_pattern_manager: ContextPatternManager for context analysis (Phase 3d Step 10.8)
        shared_utilities_manager: SharedUtilitiesManager for common operations (Phase 3e Step 2) - NEW
        learning_system_manager: LearningSystemManager for adaptive thresholds (Phase 3e Step 3) - NEW
        
    Returns:
        CrisisAnalyzer instance with Phase 3e consolidated analysis methods and enhanced dependencies
        
    Example:
        ```python
        # Phase 3e enhanced creation with all dependencies
        crisis_analyzer = create_crisis_analyzer(
            model_ensemble_manager=model_ensemble,
            crisis_pattern_manager=crisis_patterns,
            analysis_parameters_manager=analysis_params,
            threshold_mapping_manager=threshold_mapping,
            feature_config_manager=feature_config,
            performance_config_manager=performance_config,
            context_pattern_manager=context_patterns,
            shared_utilities_manager=shared_utilities,     # NEW
            learning_system_manager=learning_system        # NEW
        )
        
        # Use consolidated analysis methods
        thresholds = crisis_analyzer.get_analysis_crisis_thresholds()
        crisis_level = crisis_analyzer.apply_crisis_thresholds(0.85, mode='emergency')
        results = await crisis_analyzer.perform_ensemble_crisis_analysis(message, user_id, channel_id)
        ```
    """
    try:
        # Log dependency status for Phase 3e
        deps_status = {
            'model_ensemble': bool(model_ensemble_manager),
            'crisis_pattern': bool(crisis_pattern_manager),
            'analysis_parameters': bool(analysis_parameters_manager),
            'threshold_mapping': bool(threshold_mapping_manager),
            'feature_config': bool(feature_config_manager),
            'performance_config': bool(performance_config_manager),
            'context_pattern': bool(context_pattern_manager),
            'shared_utilities': bool(shared_utilities_manager),        # NEW
            'learning_system': bool(learning_system_manager)           # NEW
        }
        
        logger.info(f"🏗️ Creating enhanced CrisisAnalyzer with Phase 3e dependencies: {deps_status}")
        
        # Create enhanced CrisisAnalyzer with all dependencies
        analyzer = CrisisAnalyzer(
            model_ensemble_manager=model_ensemble_manager,
            crisis_pattern_manager=crisis_pattern_manager,
            learning_manager=learning_manager,
            analysis_parameters_manager=analysis_parameters_manager,
            threshold_mapping_manager=threshold_mapping_manager,
            feature_config_manager=feature_config_manager,
            performance_config_manager=performance_config_manager,
            context_pattern_manager=context_pattern_manager,
            # NEW Phase 3e dependencies
            shared_utilities_manager=shared_utilities_manager,         # Step 2
            learning_system_manager=learning_system_manager            # Step 3
        )
        
        # Validate enhanced functionality
        if shared_utilities_manager:
            logger.info("✅ SharedUtilitiesManager integration enabled - Enhanced configuration access")
        
        if learning_system_manager:
            logger.info("✅ LearningSystemManager integration enabled - Adaptive threshold management")
        
        # Test consolidated method availability
        try:
            test_thresholds = analyzer.get_analysis_crisis_thresholds()
            logger.info(f"✅ Consolidated analysis methods working - Sample thresholds: {list(test_thresholds.keys())}")
        except Exception as e:
            logger.warning(f"⚠️ Consolidated methods test warning: {e}")
        
        logger.info("🎉 Enhanced CrisisAnalyzer created successfully with Phase 3e consolidation")
        return analyzer
        
    except Exception as e:
        logger.error(f"❌ Error creating enhanced CrisisAnalyzer: {e}")
        
        # Attempt fallback creation without new dependencies
        logger.warning("🔄 Attempting fallback creation without Phase 3e dependencies")
        try:
            fallback_analyzer = CrisisAnalyzer(
                model_ensemble_manager=model_ensemble_manager,
                crisis_pattern_manager=crisis_pattern_manager,
                learning_manager=learning_manager,
                analysis_parameters_manager=analysis_parameters_manager,
                threshold_mapping_manager=threshold_mapping_manager,
                feature_config_manager=feature_config_manager,
                performance_config_manager=performance_config_manager,
                context_pattern_manager=context_pattern_manager
                # No Phase 3e dependencies in fallback
            )
            logger.warning("⚠️ Fallback CrisisAnalyzer created - Phase 3e features may be limited")
            return fallback_analyzer
            
        except Exception as fallback_error:
            logger.error(f"❌ Fallback creation also failed: {fallback_error}")
            raise Exception(f"Failed to create CrisisAnalyzer: {e}, Fallback: {fallback_error}")

# ============================================================================
# INFORMATION FUNCTIONS - Updated for Phase 3e
# ============================================================================

def get_analysis_capabilities():
    """Get detailed capabilities of all analysis components including Phase 3e enhancements"""
    return ANALYSIS_CAPABILITIES

def get_analysis_workflows():
    """Get information about available analysis workflows including Phase 3e consolidated workflows"""
    return ANALYSIS_WORKFLOWS

def get_available_analyzers():
    """Get list of available analyzer classes with Phase 3e status"""
    return {
        "CrisisAnalyzer": "Phase 3e enhanced crisis detection with consolidated analysis methods",
        "PhraseExtractor": "Phrase extraction and analysis",
        "consolidation_status": "Phase 3e Step 4.2 - Analysis method consolidation complete"
    }

def get_implemented_features():
    """Get comprehensive feature implementation status for Phase 3e"""
    return {
        "crisis_detection": {
            "status": "enhanced_phase_3e", 
            "description": "Multi-model ensemble crisis analysis with consolidated methods",
            "managers": ["CrisisAnalyzer", "SharedUtilitiesManager", "LearningSystemManager"],
            "capabilities": [
                "consolidated_analysis_parameters",
                "adaptive_threshold_management", 
                "learning_enhanced_ensemble_analysis",
                "shared_utilities_integration"
            ]
        },
        "configuration_management": {
            "status": "phase_3e_enhanced",
            "description": "Unified configuration access via SharedUtilities",
            "capabilities": [
                "safe_configuration_access",
                "unified_config_manager_integration",
                "resilient_fallback_behavior",
                "environment_variable_consolidation"
            ]
        },
        "learning_system": {
            "status": "phase_3e_integrated",
            "description": "Adaptive learning system for threshold and analysis enhancement", 
            "capabilities": [
                "adaptive_threshold_adjustment",
                "learning_enhanced_confidence_boosts",
                "context_aware_adaptations",
                "feedback_driven_improvements"
            ]
        }
    }

def get_migration_status():
    """Get Phase 3e migration and consolidation status"""
    return {
        "current_phase": "3e",
        "current_step": "4.2_complete", 
        "consolidation_status": "analysis_methods_consolidated",
        "completed_consolidations": [
            "utils/scoring_helpers.py",
            "utils/community_patterns.py", 
            "utils/context_helpers.py",
            "AnalysisParametersManager analysis methods",
            "ThresholdMappingManager threshold methods",
            "ModelEnsembleManager ensemble methods"
        ],
        "new_integrations": [
            "SharedUtilitiesManager integration",
            "LearningSystemManager integration"
        ],
        "architecture_compliance": "clean_v3_1_achieved",
        "environment_variables": "rule_7_compliant",
        "version": "v3.1.3e.4.2.1"
    }

# ============================================================================
# EXPORTS - Updated for Phase 3e
# ============================================================================

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
    "get_migration_status",
    
    # Enhanced factory function
    "create_crisis_analyzer",
]

# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

logger.info("✅ Analysis module v3.1 Phase 3e Step 4.2 loaded")
logger.info("🔗 Enhanced CrisisAnalyzer factory with SharedUtilities and LearningSystem support")
logger.info("📊 Consolidated analysis methods from AnalysisParameters, ThresholdMapping, and ModelEnsemble")
logger.info("🧠 Learning-enhanced adaptive threshold management enabled")
logger.info("🛠️ SharedUtilities integration for resilient configuration access")