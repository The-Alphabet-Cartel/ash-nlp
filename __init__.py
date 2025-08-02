"""
Ash NLP Service - Enhanced Mental Health Crisis Detection
Version 4.1 - Modular Architecture

A specialized microservice for analyzing Discord messages to detect mental health crises
with a safety-first approach designed for LGBTQIA+ communities.
"""

__version__ = "4.1.0"
__author__ = "The Alphabet Cartel"
__description__ = "Enhanced Mental Health Crisis Detection with Keyword Discovery"

# Core API imports for external usage
from .models.pydantic_models import (
    MessageRequest,
    CrisisResponse, 
    HealthResponse,
    PhraseExtractionRequest,
    PatternLearningRequest,
    SemanticAnalysisRequest
)

from .models.ml_models import ModelManager
from .analysis.crisis_analyzer import CrisisAnalyzer
from .managers.settings_manager import SERVER_CONFIG, CRISIS_THRESHOLDS

# Service metadata
SERVICE_INFO = {
    "name": "Ash NLP Service",
    "version": __version__,
    "architecture": "modular",
    "description": __description__,
    "capabilities": [
        "Crisis analysis with depression + sentiment models",
        "Phrase extraction for keyword discovery", 
        "Pattern learning from community messages",
        "Semantic analysis with community context",
        "LGBTQIA+ specific pattern recognition"
    ],
    "performance_targets": {
        "overall_accuracy": "75%+ (vs 61.7% baseline)",
        "high_crisis_detection": "95%+ (with bot's keyword detection)",
        "false_positive_rate": "<8% (vs current 15%)",
        "processing_time": "<80ms for analysis, <200ms for phrase extraction"
    },
    "hardware_requirements": {
        "min_ram": "4GB",
        "recommended_ram": "8GB+",
        "cpu_cores": "2+",
        "gpu": "Optional (CPU optimized)"
    }
}

def get_service_info():
    """Get comprehensive service information"""
    return SERVICE_INFO

def get_version_info():
    """Get version and build information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "api_endpoints": [
            "/analyze - Original crisis detection",
            "/extract_phrases - Extract keyword candidates", 
            "/learn_patterns - Learn from message history",
            "/semantic_analysis - Enhanced semantic detection",
            "/health - System health check",
            "/stats - Service statistics"
        ]
    }

__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__description__",
    
    # Core models
    "MessageRequest",
    "CrisisResponse",
    "HealthResponse", 
    "PhraseExtractionRequest",
    "PatternLearningRequest",
    "SemanticAnalysisRequest",
    
    # Core components
    "ModelManager",
    "CrisisAnalyzer",
    
    # Configuration
    "SERVER_CONFIG",
    "CRISIS_THRESHOLDS",
    
    # Service info
    "SERVICE_INFO",
    "get_service_info",
    "get_version_info"
]