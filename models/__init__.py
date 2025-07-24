"""
Models Package for Ash NLP Service
Contains ML model management and Pydantic data models
"""

# ML Models
from .ml_models import ModelManager

# Pydantic Models - Request/Response structures
from .pydantic_models import (
    # Core analysis models
    MessageRequest,
    CrisisResponse,
    HealthResponse,
    
    # Data structures
    PhraseCandidate
)

# Model configuration and metadata
MODEL_INFO = {
    "primary_models": {
        "depression": {
            "name": "rafalposwiata/deproberta-large-depression",
            "type": "DeBERTa-based classification",
            "labels": ["not depression", "moderate", "severe"],
            "purpose": "Primary crisis classification"
        },
        "sentiment": {
            "name": "cardiffnlp/twitter-roberta-base-sentiment-latest", 
            "type": "RoBERTa-based sentiment analysis",
            "labels": ["negative", "neutral", "positive"],
            "purpose": "Contextual validation and enhancement"
        }
    },
    "pipeline": [
        "Context extraction (humor, idioms, situational context)",
        "Depression analysis (primary crisis classification)", 
        "Sentiment integration (contextual validation)",
        "Pattern boosting (handle commonly missed patterns)",
        "Idiom filtering (reduce false positives)",
        "Safety mapping (conservative threshold application)"
    ],
    "safety_features": [
        "Pattern boosting for burden ideation",
        "Enhanced context-aware idiom filtering",
        "Conservative threshold mapping",
        "Forced HIGH classification for critical patterns"
    ]
}

def get_model_info():
    """Get information about loaded models and pipeline"""
    return MODEL_INFO

def get_supported_endpoints():
    """Get list of supported API endpoints"""
    return {
        "analysis": [
            "/analyze - Enhanced message analysis with multi-model approach",
            "/extract_phrases - Extract potential crisis keywords using model scoring",
            "/learn_patterns - Learn crisis communication patterns from history",
            "/semantic_analysis - Enhanced crisis detection with community context"
        ],
        "system": [
            "/health - Service health and model status",
            "/stats - Performance metrics and configuration", 
            "/enhanced_stats - Comprehensive bot integration statistics"
        ]
    }

__all__ = [
    # ML Model Management
    "ModelManager",
    
    # Request Models
    "MessageRequest",
    "PhraseExtractionRequest", 
    "PatternLearningRequest",
    "SemanticAnalysisRequest",
    
    # Response Models
    "CrisisResponse",
    "HealthResponse",
    "PhraseExtractionResponse",
    "PatternLearningResponse", 
    "SemanticAnalysisResponse",
    
    # Data Structures
    "PhraseCandidate",
    
    # Metadata
    "MODEL_INFO",
    "get_model_info",
    "get_supported_endpoints"
]