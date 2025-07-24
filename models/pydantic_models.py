"""
Pydantic models for the Enhanced Ash NLP Service
All request/response models in one place for easy management
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List, Union

# LEARNING REQUEST MODELS
class FalsePositiveAnalysisRequest(BaseModel):
    """Request model for false positive analysis (over-detection)"""
    model_config = ConfigDict(protected_namespaces=())
    
    message: str
    detected_level: str         # The level that was incorrectly detected
    correct_level: str          # The correct level that should have been detected
    context: Optional[Dict[str, Any]] = {}
    severity_score: Optional[Union[int, float]] = 1  # How bad this over-detection was (1-10)

class FalseNegativeAnalysisRequest(BaseModel):
    """Request model for false negative analysis (under-detection/missed crises)"""
    model_config = ConfigDict(protected_namespaces=())
    
    message: str
    should_detect_level: str    # The crisis level that should have been detected
    actually_detected: str      # What was actually detected (usually 'none' or lower level)
    context: Optional[Dict[str, Any]] = {}
    severity_score: Optional[Union[int, float]] = 1  # How critical this miss was (1-10)

class LearningUpdateRequest(BaseModel):
    """Request model for learning model updates"""
    model_config = ConfigDict(protected_namespaces=())
    
    learning_record_id: str
    record_type: str  # 'false_positive' or 'false_negative'
    message_data: Dict
    correction_data: Dict
    context_data: Optional[Dict[str, Any]] = {}
    timestamp: str

# LEARNING RESPONSE MODELS
class FalsePositiveAnalysisResponse(BaseModel):
    """Response model for false positive analysis"""
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    patterns_discovered: int
    confidence_adjustments: int
    learning_applied: bool
    sensitivity_reduced: bool    # Did we reduce sensitivity for similar patterns?
    processing_time_ms: float
    analysis_details: Optional[Dict] = {}

class FalseNegativeAnalysisResponse(BaseModel):
    """Response model for false negative analysis"""
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    patterns_discovered: int
    confidence_adjustments: int
    learning_applied: bool
    sensitivity_increased: bool  # Did we increase sensitivity for similar patterns?
    processing_time_ms: float
    analysis_details: Optional[Dict] = {}

class LearningUpdateResponse(BaseModel):
    """Response model for learning model updates"""
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    model_updated: bool
    adjustments_applied: int
    processing_time_ms: float
    update_details: Optional[Dict] = {}

class LearningStatisticsResponse(BaseModel):
    """Response model for learning statistics"""
    model_config = ConfigDict(protected_namespaces=())
    
    learning_system_status: str
    total_false_positives_processed: int
    total_false_negatives_processed: int
    total_adjustments_made: int
    false_positives_by_level: Dict[str, int]
    false_negatives_by_level: Dict[str, int]
    last_learning_update: Optional[str] = None
    learning_effectiveness: Optional[Dict] = {}
    model_performance_trends: Optional[Dict] = {}

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