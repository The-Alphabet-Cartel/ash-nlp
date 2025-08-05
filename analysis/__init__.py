"""
Analysis Package for Ash NLP Service
Contains all analysis components for crisis detection
"""

# Core analysis components
from .crisis_analyzer import CrisisAnalyzer

# Analysis capabilities metadata
ANALYSIS_CAPABILITIES = {
    "crisis_analyzer": {
        "description": "Enhanced crisis analysis using depression + sentiment models",
        "input": "text_message",
        "output": "crisis_level_with_confidence",
        "features": [
            "multi_model_analysis",
            "context_signal_extraction", 
            "advanced_idiom_detection",
            "safety_first_scoring"
        ],
        "processing_time": "<80ms",
        "accuracy_target": "75%+"
    }
}

# Analysis workflow metadata
ANALYSIS_WORKFLOWS = {
    "standard_crisis_detection": {
        "steps": [
            "extract_context_signals",
            "run_depression_model", 
            "run_sentiment_model",
            "combine_model_results",
            "apply_idiom_filtering",
            "map_to_crisis_level"
        ],
        "primary_component": "CrisisAnalyzer"
    }
}

def get_analysis_capabilities():
    """Get detailed capabilities of all analysis components"""
    return ANALYSIS_CAPABILITIES

def get_analysis_workflows():
    """Get information about available analysis workflows"""
    return ANALYSIS_WORKFLOWS

def get_available_analyzers():
    """Get list of available analyzer classes"""
    return {
        "CrisisAnalyzer": "Enhanced crisis detection with multi-model approach",
        "PatternLearner": "Community pattern learning (planned)"
    }

def get_implemented_features():
    """Get list of currently implemented vs planned features"""
    return {
        "implemented": [
            "crisis_analysis",
            "multi_model_detection",
            "context_analysis",
            "idiom_filtering",
            "safety_first_scoring"
        ],
        "planned": [
            "community_vocabulary_integration",
            "automated_keyword_suggestions"
        ]
    }

# Component factory functions
def create_crisis_analyzer(model_manager):
    """Create and return a CrisisAnalyzer instance"""
    return CrisisAnalyzer(model_manager)

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
]