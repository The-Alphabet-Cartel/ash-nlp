"""
Analysis Package for Ash NLP Service
Contains all analysis components for crisis detection and keyword discovery
"""

# Core analysis components
from .crisis_analyzer import CrisisAnalyzer
from .phrase_extractor import PhraseExtractor

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
    },
    
    "phrase_extractor": {
        "description": "Extract potential crisis keywords using model scoring",
        "input": "text_message_with_parameters",
        "output": "scored_phrase_candidates", 
        "methods": [
            "ngram_extraction_with_scoring",
            "community_pattern_matching",
            "crisis_context_extraction",
            "model_based_scoring"
        ],
        "processing_time": "<200ms",
        "max_phrases": 20
    },
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
    },
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
        "PatternLearner": "Community pattern learning (planned)",
    }

def get_implemented_features():
    """Get list of currently implemented vs planned features"""
    return {
        "implemented": [
            "crisis_analysis",
            "phrase_extraction", 
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

def create_phrase_extractor(model_manager):
    """Create and return a PhraseExtractor instance"""
    return PhraseExtractor(model_manager)

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
    "create_phrase_extractor",
]