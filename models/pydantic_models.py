"""
Pydantic models for the Enhanced Ash NLP Service
All request/response models in one place for easy management
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List

# EXISTING MODELS - Keep your original models

class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = "unknown"
    channel_id: Optional[str] = "unknown"

class CrisisResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    needs_response: bool
    crisis_level: str  # 'none', 'low', 'medium', 'high'
    confidence_score: float
    detected_categories: list
    method: str
    processing_time_ms: float
    model_info: str
    reasoning: Optional[str] = None

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    model_loaded: bool
    uptime_seconds: float
    hardware_info: dict

# NEW MODELS for keyword discovery

class PhraseExtractionRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    message: str
    user_id: Optional[str] = "unknown"
    channel_id: Optional[str] = "unknown"
    task: str = "phrase_extraction"
    parameters: Dict = {}

class PatternLearningRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    messages: List[Dict]
    analysis_type: str = "community_patterns"
    time_window_days: Optional[int] = 30

class SemanticAnalysisRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    message: str
    community_vocabulary: List[str] = []
    context_hints: List[str] = []

class PhraseCandidate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    text: str
    crisis_level: str
    confidence: float
    reasoning: str
    metadata: Dict = {}

# Response models for new endpoints

class PhraseExtractionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    phrases: List[PhraseCandidate]
    total_extracted: int
    total_scored: int
    processing_time_ms: float
    model_info: str
    extraction_methods: List[str]

class PatternLearningResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    patterns_learned: int
    crisis_messages_analyzed: int
    normal_messages_analyzed: int
    keyword_recommendations: int
    processing_time_ms: float
    patterns: Dict

class SemanticAnalysisResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    depression_score: float
    sentiment_scores: Dict
    community_matches: List[Dict]
    context_analysis: Dict
    final_assessment: Dict
    processing_time_ms: float
    model_info: str