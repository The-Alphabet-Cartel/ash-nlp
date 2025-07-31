"""
Models Package for Ash NLP Service - Three Model Ensemble Architecture
Contains ML model management and Pydantic data models
"""

# ML Models - Updated for three-model ensemble
from .ml_models import ModelManager

# Pydantic Models - Request/Response structures
from .pydantic_models import (
    # Core analysis models
    MessageRequest,
    CrisisResponse,
    HealthResponse,
)

# Model configuration and metadata - UPDATED FOR THREE MODELS
MODEL_INFO = {
    "ensemble_architecture": "three_model_consensus",
    "primary_models": {
        "depression": {
            "name": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
            "type": "DeBERTa-based classification",
            "labels": ['Dynamic Zero-Shot Labels'],
            "purpose": "Primary crisis classification",
            "weight": 0.5,
            "specialization": "Depression and suicidal ideation detection"
        },
        "sentiment": {
            "name": "Lowerated/lm6-deberta-v3-topic-sentiment", 
            "type": "DeBERTa-based sentiment analysis",
            "labels": ['Dynamic Zero-Shot Labels'],
            "purpose": "Contextual validation and enhancement",
            "weight": 0.2,
            "specialization": "Emotional tone and context analysis"
        },
        "emotional_distress": {  # NEW MODEL
            "name": "facebook/bart-large-mnli",
            "type": "BART-based emotional classification",
            "labels": ['Dynamic Zero-Shot Labels'], 
            "purpose": "Emotional distress and stress detection",
            "weight": 0.3,
            "specialization": "General emotional distress and mental strain"
        }
    },
    "ensemble_features": {
        "gap_detection": "Identifies disagreements between models for manual review",
        "consensus_building": "Combines predictions using configurable ensemble modes",
        "confidence_spreading": "Analyzes confidence distribution across models",
        "disagreement_flagging": "Auto-flags high-disagreement cases for staff review"
    },
    "ensemble_modes": {
        "consensus": "Unanimous agreement required for high confidence",
        "majority": "Simple majority vote with confidence weighting", 
        "weighted": "Weighted combination based on model specialization"
    },
    "pipeline": [
        "Message preprocessing and context extraction",
        "Parallel analysis with all three models",
        "Individual prediction confidence scoring",
        "Gap detection and disagreement analysis",
        "Ensemble consensus building",
        "Pattern boosting for commonly missed patterns",
        "Idiom filtering to reduce false positives",
        "Safety-first threshold mapping"
    ],
    "gap_detection_features": [
        "High confidence disagreement detection",
        "Low confidence consensus identification", 
        "Split decision flagging",
        "Confidence spread analysis",
        "Automatic staff notification for review"
    ],
    "safety_features": [
        "Three-model redundancy for missed crisis detection",
        "Enhanced pattern boosting for burden ideation",
        "Multi-perspective context-aware idiom filtering",
        "Conservative ensemble threshold mapping",
        "Automatic flagging of model disagreements"
    ],
    "performance_characteristics": {
        "target_accuracy": "80%+ (vs 75% two-model, 61.7% baseline)",
        "high_crisis_detection": "98%+ (vs 95% two-model)",
        "false_positive_rate": "<5% (vs <8% two-model, 15% baseline)",
        "processing_time": "<120ms for ensemble analysis (vs <80ms single model)",
        "gap_detection_rate": "15-25% of messages flagged for potential gaps"
    }
}

def get_model_info():
    """Get information about the three-model ensemble and pipeline"""
    return MODEL_INFO

def get_supported_endpoints():
    """Get list of supported API endpoints for three-model ensemble"""
    return {
        "analysis": [
            "/analyze - Full ensemble analysis with gap detection",
            "/extract_phrases - Extract potential crisis keywords using ensemble scoring",
            "/learn_patterns - Learn crisis communication patterns from history",
            "/semantic_analysis - Enhanced crisis detection with community context"
        ],
        "ensemble": [
            "/ensemble_health - Health status of all three models",
            "/ensemble_stats - Performance metrics for ensemble system",
            "/gap_analysis - Analyze recent model disagreements",
            "/confidence_distribution - Analyze confidence patterns across models"
        ],
        "system": [
            "/health - Service health and model status",
            "/stats - Performance metrics and configuration", 
            "/enhanced_stats - Comprehensive bot integration statistics"
        ]
    }

def get_ensemble_capabilities():
    """Get detailed ensemble system capabilities"""
    return {
        "model_count": 3,
        "ensemble_modes": ["consensus", "majority", "weighted"],
        "gap_detection": True,
        "automatic_learning": True,
        "disagreement_flagging": True,
        "confidence_analysis": True,
        "redundancy_factor": "3x crisis detection coverage",
        "specializations": [
            "Depression/suicide detection (DeBERTa) - 50%", 
            "General distress detection (DistilBERT) - 30%",
            "Emotional context analysis (RoBERTa) - 20%"
        ]
    }

def get_performance_targets():
    """Get performance targets for the three-model ensemble"""
    return MODEL_INFO["performance_characteristics"]

__all__ = [
    # ML Model Management
    "ModelManager",
    
    # Request Models
    "MessageRequest",
    
    # Response Models
    "CrisisResponse",
    "HealthResponse",
    
    # Metadata Functions
    "MODEL_INFO",
    "get_model_info",
    "get_supported_endpoints",
    "get_ensemble_capabilities", 
    "get_performance_targets"
]