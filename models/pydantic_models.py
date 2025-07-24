"""
Pydantic models for the Enhanced Ash NLP Service
All request/response models in one place for easy management
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List

class FalsePositiveAnalysisRequest(BaseModel):
    """Request model for false positive analysis"""
    model_config = ConfigDict(protected_namespaces=())
    
    message: str
    detected_level: str  # The level that was incorrectly detected
    correct_level: str   # The correct level that should have been detected
    context: Optional[Dict] = {}
    severity_score: Optional[int] = 1

class FalseNegativeAnalysisRequest(BaseModel):
    """Request model for false negative analysis"""
    model_config = ConfigDict(protected_namespaces=())
    
    message: str
    should_detect_level: str  # The level that should have been detected
    actually_detected: str    # What was actually detected (usually 'none')
    context: Optional[Dict] = {}
    severity_score: Optional[int] = 1

class LearningUpdateRequest(BaseModel):
    """Request model for learning model updates"""
    model_config = ConfigDict(protected_namespaces=())
    
    learning_record_id: str
    record_type: str  # 'false_positive' or 'false_negative'
    message_data: Dict
    correction_data: Dict
    context_data: Optional[Dict] = {}
    timestamp: str

# RESPONSE MODELS for learning endpoints
class LearningAnalysisResponse(BaseModel):
    """Response model for learning analysis"""
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    patterns_discovered: int
    confidence_adjustments: int
    learning_applied: bool
    processing_time_ms: float
    analysis_details: Optional[Dict] = {}

class LearningUpdateResponse(BaseModel):
    """Response model for learning updates"""
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    model_updated: bool
    adjustments_applied: int
    processing_time_ms: float
    update_details: Optional[Dict] = {}

class LearningStatisticsResponse(BaseModel):
    """Response model for learning statistics"""
    model_config = ConfigDict(protected_namespaces=())
    
    total_false_positives: int
    total_false_negatives: int
    false_positives_by_level: Dict[str, int]
    false_negatives_by_level: Dict[str, int]
    detection_improvements: int
    last_analysis: Optional[str] = None
    learning_effectiveness: Optional[Dict] = {}

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