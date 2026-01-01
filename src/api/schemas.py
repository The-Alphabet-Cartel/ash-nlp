"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
API Schemas for Ash-NLP Service
---
FILE VERSION: v5.0-4-5.1-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 - API Enhancements
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Define Pydantic models for request validation
- Define response schemas for consistent API output
- Provide OpenAPI documentation through model configs
- Handle field validation and serialization

PHASE 4 ENHANCEMENTS:
- Consensus algorithm selection in requests
- Explainability verbosity levels
- Conflict analysis in responses
- Consensus configuration endpoints
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# Module version
__version__ = "v5.0-4-5.1-1"


# =============================================================================
# Enums
# =============================================================================


class SeverityLevel(str, Enum):
    """Crisis severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SAFE = "safe"


class RecommendedAction(str, Enum):
    """Recommended response actions."""

    IMMEDIATE_OUTREACH = "immediate_outreach"
    PRIORITY_RESPONSE = "priority_response"
    STANDARD_MONITORING = "standard_monitoring"
    PASSIVE_MONITORING = "passive_monitoring"
    NONE = "none"
    ERROR = "error"


class HealthStatus(str, Enum):
    """Service health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


# =============================================================================
# Phase 4 Enums
# =============================================================================


class ConsensusAlgorithm(str, Enum):
    """Available consensus algorithms (Phase 4)."""

    WEIGHTED_VOTING = "weighted_voting"
    MAJORITY_VOTING = "majority_voting"
    UNANIMOUS = "unanimous"
    CONFLICT_AWARE = "conflict_aware"


class ResolutionStrategy(str, Enum):
    """Conflict resolution strategies (Phase 4)."""

    CONSERVATIVE = "conservative"
    OPTIMISTIC = "optimistic"
    MEAN = "mean"
    REVIEW_FLAG = "review_flag"


class VerbosityLevel(str, Enum):
    """Explanation verbosity levels (Phase 4)."""

    MINIMAL = "minimal"
    STANDARD = "standard"
    DETAILED = "detailed"


class ConflictType(str, Enum):
    """Types of model conflicts (Phase 4)."""

    SCORE_DISAGREEMENT = "score_disagreement"
    IRONY_SENTIMENT_CONFLICT = "irony_sentiment_conflict"
    EMOTION_CRISIS_MISMATCH = "emotion_crisis_mismatch"
    LABEL_DISAGREEMENT = "label_disagreement"


class ConflictSeverity(str, Enum):
    """Conflict severity levels (Phase 4)."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AgreementLevel(str, Enum):
    """Model agreement levels (Phase 4)."""

    STRONG_AGREEMENT = "strong_agreement"
    MODERATE_AGREEMENT = "moderate_agreement"
    WEAK_AGREEMENT = "weak_agreement"
    SIGNIFICANT_DISAGREEMENT = "significant_disagreement"


# =============================================================================
# Request Schemas
# =============================================================================


class AnalyzeRequest(BaseModel):
    """
    Request schema for message analysis endpoint.

    Attributes:
        message: The text message to analyze for crisis signals
        user_id: Optional user identifier for tracking
        channel_id: Optional channel identifier
        metadata: Optional additional context
        
        # Phase 4 options
        include_explanation: Include human-readable explanation
        verbosity: Explanation verbosity level
        consensus_algorithm: Override default consensus algorithm
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text message to analyze for crisis signals",
        examples=["I'm feeling really overwhelmed today"],
    )
    user_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional user identifier for tracking",
    )
    channel_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional channel identifier",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional additional context",
    )
    
    # Phase 4 options
    include_explanation: bool = Field(
        default=True,
        description="Include human-readable explanation in response",
    )
    verbosity: Optional[VerbosityLevel] = Field(
        default=None,
        description="Explanation verbosity: minimal, standard, detailed",
    )
    consensus_algorithm: Optional[ConsensusAlgorithm] = Field(
        default=None,
        description="Override consensus algorithm for this request",
    )

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        """Validate message is not just whitespace."""
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "I don't know if I can keep going anymore",
                    "user_id": "user_12345",
                    "channel_id": "general",
                    "include_explanation": True,
                    "verbosity": "standard",
                }
            ]
        }
    }


class BatchAnalyzeRequest(BaseModel):
    """
    Request schema for batch message analysis.

    Attributes:
        messages: List of messages to analyze
        include_details: Whether to include detailed signals
        include_explanation: Include explanations for each message
    """

    messages: List[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of messages to analyze (max 100)",
    )
    include_details: bool = Field(
        default=False,
        description="Include detailed model signals in response",
    )
    include_explanation: bool = Field(
        default=False,
        description="Include explanations (increases processing time)",
    )

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v: List[str]) -> List[str]:
        """Validate each message."""
        validated = []
        for msg in v:
            stripped = msg.strip()
            if stripped:
                validated.append(stripped)
        if not validated:
            raise ValueError("At least one non-empty message required")
        return validated


# =============================================================================
# Phase 4 Response Components
# =============================================================================


class ExplanationResponse(BaseModel):
    """Human-readable explanation (Phase 4)."""

    verbosity: VerbosityLevel = Field(description="Verbosity level used")
    decision_summary: str = Field(description="Plain-English summary")
    key_factors: List[str] = Field(
        default_factory=list,
        description="Primary factors driving the classification",
    )
    recommended_action: Optional[Dict[str, str]] = Field(
        default=None,
        description="Action recommendation details",
    )
    plain_text: str = Field(description="Full plain-text explanation")
    
    # Detailed fields (only in detailed verbosity)
    confidence_summary: Optional[str] = Field(
        default=None,
        description="Explanation of confidence level",
    )
    model_contributions: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Per-model contribution breakdown",
    )
    conflict_summary: Optional[str] = Field(
        default=None,
        description="Summary of model conflicts",
    )


class DetectedConflictResponse(BaseModel):
    """Single detected conflict (Phase 4)."""

    conflict_type: ConflictType
    severity: ConflictSeverity
    description: str
    involved_models: List[str]
    details: Dict[str, Any] = Field(default_factory=dict)


class ConflictAnalysisResponse(BaseModel):
    """Conflict analysis results (Phase 4)."""

    has_conflicts: bool = Field(description="Whether any conflicts detected")
    conflict_count: int = Field(description="Number of conflicts")
    conflicts: List[DetectedConflictResponse] = Field(
        default_factory=list,
        description="List of detected conflicts",
    )
    highest_severity: Optional[ConflictSeverity] = Field(
        default=None,
        description="Most severe conflict level",
    )
    requires_review: bool = Field(description="Whether human review recommended")
    summary: str = Field(description="Brief conflict summary")
    
    # Resolution info
    resolution_strategy: Optional[ResolutionStrategy] = Field(
        default=None,
        description="Strategy used to resolve conflicts",
    )
    original_score: Optional[float] = Field(
        default=None,
        description="Score before resolution",
    )
    resolved_score: Optional[float] = Field(
        default=None,
        description="Score after resolution",
    )


class ConsensusResponse(BaseModel):
    """Consensus algorithm results (Phase 4)."""

    algorithm: ConsensusAlgorithm = Field(description="Algorithm used")
    crisis_score: float = Field(description="Consensus crisis score")
    confidence: float = Field(description="Confidence in consensus")
    agreement_level: AgreementLevel = Field(description="Model agreement level")
    is_crisis: bool = Field(description="Binary crisis determination")
    requires_review: bool = Field(description="Whether review recommended")
    has_conflict: bool = Field(description="Whether conflict detected")
    individual_scores: Dict[str, float] = Field(description="Per-model scores")
    vote_breakdown: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Voting details for voting algorithms",
    )


# =============================================================================
# Response Schemas
# =============================================================================


class ModelSignalResponse(BaseModel):
    """Individual model signal in analysis response."""

    label: str = Field(description="Primary predicted label")
    score: float = Field(description="Raw confidence score (0-1)")
    crisis_signal: float = Field(description="Extracted crisis signal (0-1)")


class AnalyzeResponse(BaseModel):
    """
    Response schema for message analysis.

    This is the primary output format for crisis detection results.
    Includes Phase 4 enhanced fields.
    """

    crisis_detected: bool = Field(description="Whether a crisis was detected")
    severity: SeverityLevel = Field(description="Crisis severity level")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the assessment (0-1)",
    )
    crisis_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Final weighted crisis score (0-1)",
    )
    requires_intervention: bool = Field(
        description="Whether immediate action is recommended"
    )
    recommended_action: RecommendedAction = Field(
        description="Suggested response action"
    )
    signals: Dict[str, ModelSignalResponse] = Field(
        description="Individual model signals"
    )
    processing_time_ms: float = Field(
        ge=0.0, description="Total processing time in milliseconds"
    )
    models_used: List[str] = Field(description="Models that contributed to analysis")
    is_degraded: bool = Field(
        default=False, description="Whether service is in degraded mode"
    )
    request_id: Optional[str] = Field(
        default=None, description="Unique request identifier for tracking"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Response timestamp (UTC)"
    )
    
    # Phase 4 Enhanced Fields
    explanation: Optional[ExplanationResponse] = Field(
        default=None,
        description="Human-readable explanation (Phase 4)",
    )
    conflict_analysis: Optional[ConflictAnalysisResponse] = Field(
        default=None,
        description="Conflict detection and resolution (Phase 4)",
    )
    consensus: Optional[ConsensusResponse] = Field(
        default=None,
        description="Consensus algorithm results (Phase 4)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "crisis_detected": True,
                    "severity": "high",
                    "confidence": 0.87,
                    "crisis_score": 0.78,
                    "requires_intervention": True,
                    "recommended_action": "priority_response",
                    "signals": {
                        "bart": {
                            "label": "emotional distress",
                            "score": 0.89,
                            "crisis_signal": 0.89,
                        },
                        "sentiment": {
                            "label": "negative",
                            "score": 0.92,
                            "crisis_signal": 0.75,
                        },
                    },
                    "processing_time_ms": 145.32,
                    "models_used": ["bart", "sentiment", "irony", "emotions"],
                    "is_degraded": False,
                    "request_id": "req_abc123",
                    "timestamp": "2025-12-31T12:00:00Z",
                    "explanation": {
                        "verbosity": "standard",
                        "decision_summary": "HIGH CONCERN: Crisis indicators detected with 87% confidence.",
                        "key_factors": ["emotional distress", "negative sentiment"],
                        "plain_text": "DECISION SUMMARY:\nHIGH CONCERN...",
                    },
                    "consensus": {
                        "algorithm": "weighted_voting",
                        "crisis_score": 0.78,
                        "confidence": 0.87,
                        "agreement_level": "strong_agreement",
                        "is_crisis": True,
                    },
                }
            ]
        }
    }


class BatchAnalyzeResponseItem(BaseModel):
    """Single item in batch analysis response."""

    index: int = Field(description="Index of message in request")
    message_preview: str = Field(description="First 50 chars of message")
    crisis_detected: bool
    severity: SeverityLevel
    crisis_score: float
    requires_intervention: bool
    explanation_summary: Optional[str] = Field(
        default=None,
        description="Brief explanation (if requested)",
    )


class BatchAnalyzeResponse(BaseModel):
    """Response schema for batch analysis."""

    total_messages: int = Field(description="Total messages analyzed")
    crisis_count: int = Field(description="Number with crisis detected")
    critical_count: int = Field(description="Number at critical severity")
    high_count: int = Field(description="Number at high severity")
    results: List[BatchAnalyzeResponseItem] = Field(description="Individual results")
    processing_time_ms: float = Field(description="Total processing time")
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Consensus Configuration Schemas (Phase 4)
# =============================================================================


class ConsensusConfigResponse(BaseModel):
    """Current consensus configuration (Phase 4)."""

    default_algorithm: ConsensusAlgorithm = Field(
        description="Default consensus algorithm"
    )
    available_algorithms: List[ConsensusAlgorithm] = Field(
        description="All available algorithms"
    )
    weights: Dict[str, float] = Field(description="Model weights")
    thresholds: Dict[str, float] = Field(description="Algorithm thresholds")
    conflict_detection_enabled: bool = Field(
        description="Whether conflict detection is enabled"
    )
    resolution_strategy: ResolutionStrategy = Field(
        description="Default conflict resolution strategy"
    )
    explainability_verbosity: VerbosityLevel = Field(
        description="Default explanation verbosity"
    )


class ConsensusConfigUpdateRequest(BaseModel):
    """Request to update consensus configuration (Phase 4)."""

    default_algorithm: Optional[ConsensusAlgorithm] = Field(
        default=None,
        description="Set default consensus algorithm",
    )
    resolution_strategy: Optional[ResolutionStrategy] = Field(
        default=None,
        description="Set conflict resolution strategy",
    )
    explainability_verbosity: Optional[VerbosityLevel] = Field(
        default=None,
        description="Set default explanation verbosity",
    )
    thresholds: Optional[Dict[str, float]] = Field(
        default=None,
        description="Update threshold values",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "default_algorithm": "conflict_aware",
                    "resolution_strategy": "conservative",
                    "explainability_verbosity": "detailed",
                }
            ]
        }
    }


# =============================================================================
# Health and Status Schemas
# =============================================================================


class ModelStatusResponse(BaseModel):
    """Status of a single model."""

    name: str
    loaded: bool
    enabled: bool
    device: Optional[str] = None
    weight: float
    average_latency_ms: Optional[float] = None


class Phase4StatusResponse(BaseModel):
    """Phase 4 component status (Phase 4)."""

    enabled: bool = Field(description="Whether Phase 4 features are enabled")
    consensus_algorithm: Optional[ConsensusAlgorithm] = None
    resolution_strategy: Optional[ResolutionStrategy] = None
    explainability_verbosity: Optional[VerbosityLevel] = None
    conflicts_detected: int = Field(
        default=0,
        description="Total conflicts detected since startup",
    )


class HealthResponse(BaseModel):
    """
    Health check response schema.

    Used by load balancers and monitoring systems.
    """

    status: HealthStatus = Field(description="Overall service health")
    ready: bool = Field(description="Whether service can accept requests")
    degraded: bool = Field(description="Whether running in degraded mode")
    models_loaded: int = Field(description="Number of models loaded")
    total_models: int = Field(description="Total expected models")
    uptime_seconds: Optional[float] = Field(
        default=None, description="Service uptime in seconds"
    )
    version: str = Field(description="Service version")
    phase4_enabled: bool = Field(
        default=True,
        description="Whether Phase 4 features are enabled",
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "ready": True,
                    "degraded": False,
                    "models_loaded": 4,
                    "total_models": 4,
                    "uptime_seconds": 3600.5,
                    "version": "v5.0.0",
                    "phase4_enabled": True,
                    "timestamp": "2025-12-31T12:00:00Z",
                }
            ]
        }
    }


class StatusResponse(BaseModel):
    """
    Detailed status response schema.

    Provides comprehensive service status information.
    """

    service: str = Field(default="ash-nlp", description="Service name")
    version: str = Field(description="Service version")
    environment: str = Field(description="Running environment")
    status: HealthStatus
    ready: bool
    degraded: bool
    degradation_reason: Optional[str] = None
    models: List[ModelStatusResponse] = Field(description="Model statuses")
    stats: Dict[str, Any] = Field(description="Service statistics")
    config: Dict[str, Any] = Field(description="Active configuration")
    phase4: Optional[Phase4StatusResponse] = Field(
        default=None,
        description="Phase 4 component status",
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Error Schemas
# =============================================================================


class ErrorDetail(BaseModel):
    """Detailed error information."""

    code: str = Field(description="Error code")
    message: str = Field(description="Human-readable error message")
    field: Optional[str] = Field(
        default=None, description="Field that caused the error (for validation errors)"
    )


class ErrorResponse(BaseModel):
    """
    Standard error response schema.

    Used for all API error responses.
    """

    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Optional[List[ErrorDetail]] = Field(
        default=None, description="Additional error details"
    )
    request_id: Optional[str] = Field(
        default=None, description="Request ID for tracking"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "validation_error",
                    "message": "Request validation failed",
                    "details": [
                        {
                            "code": "value_error",
                            "message": "Message cannot be empty",
                            "field": "message",
                        }
                    ],
                    "request_id": "req_abc123",
                    "timestamp": "2025-12-31T12:00:00Z",
                }
            ]
        }
    }


# =============================================================================
# Webhook/Callback Schemas (for Discord integration)
# =============================================================================


class CrisisAlertPayload(BaseModel):
    """
    Payload for crisis alert webhooks.

    Sent to Discord or other notification systems when crisis detected.
    """

    alert_type: str = Field(default="crisis_detected")
    severity: SeverityLevel
    crisis_score: float
    confidence: float
    recommended_action: RecommendedAction
    message_preview: str = Field(description="First 100 chars of message (for context)")
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("message_preview")
    @classmethod
    def truncate_preview(cls, v: str) -> str:
        """Truncate message preview to 100 chars."""
        if len(v) > 100:
            return v[:97] + "..."
        return v


class ConflictAlertPayload(BaseModel):
    """
    Payload for model conflict alert webhooks (Phase 4).

    Sent to Discord when significant model conflicts detected.
    """

    alert_type: str = Field(default="model_conflict")
    conflict_severity: ConflictSeverity
    conflict_count: int
    conflict_types: List[ConflictType]
    crisis_score: float
    requires_review: bool
    resolution_strategy: ResolutionStrategy
    message_preview: str = Field(description="First 100 chars of message")
    summary: str = Field(description="Conflict summary")
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "SeverityLevel",
    "RecommendedAction",
    "HealthStatus",
    # Phase 4 Enums
    "ConsensusAlgorithm",
    "ResolutionStrategy",
    "VerbosityLevel",
    "ConflictType",
    "ConflictSeverity",
    "AgreementLevel",
    # Request schemas
    "AnalyzeRequest",
    "BatchAnalyzeRequest",
    "ConsensusConfigUpdateRequest",
    # Response schemas
    "AnalyzeResponse",
    "ModelSignalResponse",
    "BatchAnalyzeResponse",
    "BatchAnalyzeResponseItem",
    "HealthResponse",
    "StatusResponse",
    "ModelStatusResponse",
    "ErrorResponse",
    "ErrorDetail",
    # Phase 4 Response components
    "ExplanationResponse",
    "ConflictAnalysisResponse",
    "DetectedConflictResponse",
    "ConsensusResponse",
    "ConsensusConfigResponse",
    "Phase4StatusResponse",
    # Webhook schemas
    "CrisisAlertPayload",
    "ConflictAlertPayload",
]
