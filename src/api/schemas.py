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
FILE VERSION: v5.0-3-5.0-1
LAST MODIFIED: 2026-01-27
PHASE: Phase 3 - Ash-Vigil Integration
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Define Pydantic models for request validation
- Define response schemas for consistent API output
- Provide OpenAPI documentation through model configs
- Handle field validation and serialization

PHASE 3 VIGIL ENHANCEMENTS:
- Vigil status enum for tracking integration status
- Vigil response schema with risk detection details
- requires_review flag in analysis response
- Vigil configuration response schemas
- Health endpoint includes Vigil status

PHASE 4 ENHANCEMENTS:
- Consensus algorithm selection in requests
- Explainability verbosity levels
- Conflict analysis in responses
- Consensus configuration endpoints

PHASE 5 ENHANCEMENTS:
- Message history input for context analysis
- Context analysis response schemas
- Escalation, temporal, and trend detection outputs
- Context configuration endpoints

PHASE 6 ENHANCEMENTS:
- FE-001: User timezone support for late night detection
- Timezone parameter in analyze requests
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# Module version
__version__ = "v5.0-3-5.0-1"


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
# Phase 3 Vigil Enums
# =============================================================================


class VigilStatus(str, Enum):
    """
    Status of Vigil integration for a request (Phase 3 Vigil).
    
    Indicates what happened with the Ash-Vigil integration
    for each analysis request.
    """

    USED = "used"
    """Vigil was called successfully and result was incorporated."""
    
    SKIPPED = "skipped"
    """Base score already high enough, Vigil call not needed."""
    
    UNAVAILABLE = "unavailable"
    """Network error or Vigil returned an error."""
    
    TIMEOUT = "timeout"
    """Vigil call exceeded the configured timeout."""
    
    CIRCUIT_OPEN = "circuit_open"
    """Circuit breaker tripped due to repeated failures."""
    
    DISABLED = "disabled"
    """Vigil integration is disabled in configuration."""


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
# Phase 5 Enums
# =============================================================================


class InterventionUrgency(str, Enum):
    """Intervention urgency levels (Phase 5)."""

    NONE = "none"
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    IMMEDIATE = "immediate"


class TrendDirection(str, Enum):
    """Trend direction indicators (Phase 5)."""

    IMPROVING = "improving"
    STABLE = "stable"
    WORSENING = "worsening"
    VOLATILE = "volatile"


class TrendVelocity(str, Enum):
    """Trend velocity indicators (Phase 5)."""

    NONE = "none"
    GRADUAL = "gradual"
    MODERATE = "moderate"
    RAPID = "rapid"


class EscalationRate(str, Enum):
    """Escalation rate classification (Phase 5)."""

    NONE = "none"
    GRADUAL = "gradual"
    RAPID = "rapid"
    SUDDEN = "sudden"


# =============================================================================
# Request Schemas
# =============================================================================


class MessageHistoryItemRequest(BaseModel):
    """
    Single message in history for context analysis (Phase 5).
    
    Attributes:
        message: The message text content
        timestamp: When the message was sent (ISO format)
        crisis_score: Pre-calculated crisis score (optional)
        message_id: Optional message identifier
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Message text content",
    )
    timestamp: datetime = Field(
        ...,
        description="When message was sent (ISO 8601 format)",
    )
    crisis_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Pre-calculated crisis score (will calculate if not provided)",
    )
    message_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional message identifier",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Not having the best day",
                    "timestamp": "2025-01-01T16:00:00Z",
                    "crisis_score": 0.25,
                    "message_id": "msg_001",
                }
            ]
        }
    }


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
        
        # Phase 5 options
        message_history: Previous messages for context analysis
        include_context_analysis: Enable context history analysis
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
    
    # Phase 5 options
    message_history: Optional[List[MessageHistoryItemRequest]] = Field(
        default=None,
        max_length=20,
        description="Previous messages for context analysis (max 20)",
    )
    include_context_analysis: bool = Field(
        default=True,
        description="Enable context history analysis (Phase 5)",
    )
    
    # Phase 6 options (FE-001)
    user_timezone: Optional[str] = Field(
        default=None,
        max_length=50,
        description="User's timezone for late night detection (e.g., 'America/New_York', 'Europe/London')",
        examples=["America/New_York", "Europe/London", "Asia/Tokyo", "UTC"],
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
                    "message_history": [
                        {
                            "message": "Not having the best day",
                            "timestamp": "2025-01-01T16:00:00Z",
                            "crisis_score": 0.25,
                        },
                        {
                            "message": "Things are getting harder",
                            "timestamp": "2025-01-01T18:00:00Z",
                            "crisis_score": 0.45,
                        },
                    ],
                    "include_context_analysis": True,
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
# Phase 3 Vigil Response Components
# =============================================================================


class VigilResponse(BaseModel):
    """
    Vigil integration details in analysis response (Phase 3 Vigil).
    
    Provides complete visibility into what happened with the 
    Ash-Vigil integration for each analysis request.
    
    Attributes:
        status: What happened with Vigil (used, skipped, unavailable, etc.)
        risk_score: Risk score from Vigil if available (0.0-1.0)
        risk_label: Risk classification label from Vigil
        amplification_applied: Whether Vigil boosted the base score
        base_score: Pre-amplification ensemble score (for transparency)
        amplified_score: Post-amplification score (before irony dampening)
    """

    status: VigilStatus = Field(
        description="What happened with Vigil integration",
    )
    risk_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Risk score from Vigil (0-1) if called successfully",
    )
    risk_label: Optional[str] = Field(
        default=None,
        description="Risk classification label from Vigil",
    )
    amplification_applied: bool = Field(
        default=False,
        description="Whether Vigil amplification was applied to base score",
    )
    base_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Pre-amplification ensemble score (for debugging/transparency)",
    )
    amplified_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Post-amplification score before irony dampening",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "used",
                    "risk_score": 0.72,
                    "risk_label": "moderate_risk",
                    "amplification_applied": True,
                    "base_score": 0.35,
                    "amplified_score": 0.57,
                },
                {
                    "status": "skipped",
                    "amplification_applied": False,
                    "base_score": 0.78,
                },
                {
                    "status": "circuit_open",
                    "amplification_applied": False,
                    "base_score": 0.42,
                },
            ]
        }
    }


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
# Phase 5 Response Components
# =============================================================================


class EscalationResponse(BaseModel):
    """Escalation detection results (Phase 5)."""

    detected: bool = Field(description="Whether escalation was detected")
    rate: EscalationRate = Field(
        default=EscalationRate.NONE,
        description="Escalation rate: none, gradual, rapid, sudden",
    )
    pattern: Optional[str] = Field(
        default=None,
        description="Matched escalation pattern name",
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence in escalation detection (0-1)",
    )


class TemporalFactorsResponse(BaseModel):
    """Temporal pattern detection results (Phase 5)."""

    late_night_risk: bool = Field(
        default=False,
        description="Whether message was sent during late night hours (in user's local time)",
    )
    rapid_posting: bool = Field(
        default=False,
        description="Whether user is posting rapidly",
    )
    time_risk_modifier: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Risk modifier based on temporal factors",
    )
    hour_of_day: int = Field(
        default=12,
        ge=0,
        le=23,
        description="Hour of day (0-23) in user's local time if timezone provided, otherwise UTC",
    )
    is_weekend: bool = Field(
        default=False,
        description="Whether message was sent on weekend (in user's local time)",
    )
    # FE-001: Timezone support fields
    user_timezone: Optional[str] = Field(
        default=None,
        description="User's timezone if provided (FE-001)",
    )
    local_hour: Optional[int] = Field(
        default=None,
        ge=0,
        le=23,
        description="Hour in user's local timezone (FE-001)",
    )


class TrendResponse(BaseModel):
    """Trend analysis results (Phase 5)."""

    direction: TrendDirection = Field(
        default=TrendDirection.STABLE,
        description="Trend direction: improving, stable, worsening, volatile",
    )
    velocity: TrendVelocity = Field(
        default=TrendVelocity.NONE,
        description="Trend velocity: none, gradual, moderate, rapid",
    )
    score_delta: float = Field(
        default=0.0,
        description="Change in score from start to end",
    )
    time_span_hours: float = Field(
        default=0.0,
        ge=0.0,
        description="Time span analyzed in hours",
    )


class TrajectoryResponse(BaseModel):
    """Score trajectory information (Phase 5)."""

    start_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Score of first message in sequence",
    )
    end_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Score of last message (current)",
    )
    peak_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Highest score in sequence",
    )
    scores: List[float] = Field(
        default_factory=list,
        description="All scores in sequence order",
    )


class InterventionResponse(BaseModel):
    """Intervention recommendations (Phase 5)."""

    urgency: InterventionUrgency = Field(
        default=InterventionUrgency.NONE,
        description="Intervention urgency: none, low, standard, high, immediate",
    )
    recommended_point: Optional[int] = Field(
        default=None,
        description="Message index where intervention should have occurred",
    )
    intervention_delayed: bool = Field(
        default=False,
        description="Whether intervention point has passed",
    )
    reason: str = Field(
        default="",
        description="Explanation for urgency level",
    )


class HistoryMetadataResponse(BaseModel):
    """Metadata about analyzed history (Phase 5)."""

    message_count: int = Field(
        default=0,
        ge=0,
        description="Number of messages analyzed",
    )
    time_span_hours: float = Field(
        default=0.0,
        ge=0.0,
        description="Time span of history in hours",
    )
    oldest_timestamp: Optional[datetime] = Field(
        default=None,
        description="Timestamp of oldest message",
    )
    newest_timestamp: Optional[datetime] = Field(
        default=None,
        description="Timestamp of newest message",
    )


class ContextAnalysisResponse(BaseModel):
    """
    Complete context analysis results (Phase 5).
    
    Contains escalation detection, temporal patterns, trend analysis,
    trajectory information, and intervention recommendations.
    """

    # Escalation detection
    escalation_detected: bool = Field(
        default=False,
        description="Whether escalation pattern detected",
    )
    escalation_rate: EscalationRate = Field(
        default=EscalationRate.NONE,
        description="Escalation rate classification",
    )
    escalation_pattern: Optional[str] = Field(
        default=None,
        description="Matched escalation pattern name",
    )
    pattern_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence in pattern match",
    )
    
    # Sub-components
    trend: TrendResponse = Field(
        default_factory=TrendResponse,
        description="Trend analysis results",
    )
    temporal_factors: TemporalFactorsResponse = Field(
        default_factory=TemporalFactorsResponse,
        description="Temporal pattern results",
    )
    trajectory: TrajectoryResponse = Field(
        default_factory=TrajectoryResponse,
        description="Score trajectory information",
    )
    intervention: InterventionResponse = Field(
        default_factory=InterventionResponse,
        description="Intervention recommendations",
    )
    history_analyzed: HistoryMetadataResponse = Field(
        default_factory=HistoryMetadataResponse,
        description="Metadata about analyzed history",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "escalation_detected": True,
                    "escalation_rate": "rapid",
                    "escalation_pattern": "evening_deterioration",
                    "pattern_confidence": 0.87,
                    "trend": {
                        "direction": "worsening",
                        "velocity": "rapid",
                        "score_delta": 0.66,
                        "time_span_hours": 6.0,
                    },
                    "temporal_factors": {
                        "late_night_risk": False,
                        "rapid_posting": False,
                        "time_risk_modifier": 1.0,
                    },
                    "trajectory": {
                        "start_score": 0.25,
                        "end_score": 0.91,
                        "peak_score": 0.91,
                        "scores": [0.25, 0.45, 0.70, 0.91],
                    },
                    "intervention": {
                        "urgency": "immediate",
                        "recommended_point": 2,
                        "intervention_delayed": True,
                    },
                    "history_analyzed": {
                        "message_count": 4,
                        "time_span_hours": 6.0,
                    },
                }
            ]
        }
    }


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
    Includes Phase 3 Vigil, Phase 4, and Phase 5 enhanced fields.
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
    
    # Phase 3 Vigil Enhanced Fields
    vigil: Optional[VigilResponse] = Field(
        default=None,
        description="Ash-Vigil integration details (Phase 3 Vigil)",
    )
    requires_review: bool = Field(
        default=False,
        description="Whether CRT human review is recommended (Phase 3 Vigil)",
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
    
    # Phase 5 Enhanced Fields
    context_analysis: Optional[ContextAnalysisResponse] = Field(
        default=None,
        description="Context history analysis results (Phase 5)",
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
                    "requires_review": True,
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
                    "vigil": {
                        "status": "used",
                        "risk_score": 0.72,
                        "risk_label": "moderate_risk",
                        "amplification_applied": True,
                        "base_score": 0.45,
                        "amplified_score": 0.67,
                    },
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
    requires_review: bool = Field(
        default=False,
        description="Whether CRT review recommended (Phase 3 Vigil)",
    )
    vigil_status: Optional[VigilStatus] = Field(
        default=None,
        description="Vigil integration status (Phase 3 Vigil)",
    )
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
    review_count: int = Field(
        default=0,
        description="Number requiring CRT review (Phase 3 Vigil)",
    )
    results: List[BatchAnalyzeResponseItem] = Field(description="Individual results")
    processing_time_ms: float = Field(description="Total processing time")
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Phase 3 Vigil Configuration Schemas
# =============================================================================


class VigilAmplificationConfigResponse(BaseModel):
    """
    Vigil amplification configuration (Phase 3 Vigil).
    
    Shows the current amplification settings that control
    when and how much Vigil boosts ensemble scores.
    """

    enabled: bool = Field(description="Whether amplification is enabled")
    score_cap: float = Field(description="Hard cap for amplified scores (default: 1.0)")
    skip_threshold: float = Field(
        description="Base score at which Vigil is skipped (default: 0.70)"
    )
    amplify_medium: bool = Field(
        description="Whether to amplify MEDIUM severity scores"
    )
    vigil_thresholds: Dict[str, float] = Field(
        description="Vigil risk score thresholds (critical, high, moderate)"
    )
    boosts: Dict[str, float] = Field(
        description="Boost values (critical_boost, critical_minimum, high_multiplier, moderate_multiplier)"
    )


class VigilClientConfigResponse(BaseModel):
    """
    Vigil client configuration (Phase 3 Vigil).
    
    Shows the client connection settings for Ash-Vigil.
    """

    enabled: bool = Field(description="Whether Vigil client is enabled")
    host: str = Field(description="Vigil server host")
    port: int = Field(description="Vigil server port")
    timeout_ms: int = Field(description="Request timeout in milliseconds")
    retry_attempts: int = Field(description="Number of retry attempts")


class VigilCircuitBreakerResponse(BaseModel):
    """
    Vigil circuit breaker status (Phase 3 Vigil).
    
    Shows the current state of the circuit breaker for
    fault tolerance monitoring.
    """

    state: str = Field(description="Circuit state: closed, open, half_open")
    consecutive_failures: int = Field(description="Current failure count")
    failure_threshold: int = Field(description="Failures before circuit opens")
    recovery_timeout_seconds: int = Field(description="Seconds before recovery attempt")
    total_failures: int = Field(description="Total failures since startup")
    total_successes: int = Field(description="Total successes since startup")


class VigilStatsResponse(BaseModel):
    """
    Vigil usage statistics (Phase 3 Vigil).
    
    Shows Vigil integration performance metrics.
    """

    calls: int = Field(description="Total Vigil API calls")
    amplifications: int = Field(description="Times amplification was applied")
    amplification_rate: float = Field(
        description="Percentage of calls that resulted in amplification"
    )
    average_latency_ms: Optional[float] = Field(
        default=None,
        description="Average call latency in milliseconds",
    )
    success_rate: Optional[float] = Field(
        default=None,
        description="Percentage of successful calls",
    )


class VigilConfigResponse(BaseModel):
    """
    Complete Vigil configuration response (Phase 3 Vigil).
    
    Returns all Vigil-related configuration and status.
    """

    enabled: bool = Field(description="Whether Vigil integration is enabled")
    client: Optional[VigilClientConfigResponse] = Field(
        default=None,
        description="Client connection configuration",
    )
    amplification: VigilAmplificationConfigResponse = Field(
        description="Amplification configuration",
    )
    circuit_breaker: Optional[VigilCircuitBreakerResponse] = Field(
        default=None,
        description="Circuit breaker status",
    )
    stats: VigilStatsResponse = Field(
        description="Usage statistics",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "enabled": True,
                    "client": {
                        "enabled": True,
                        "host": "10.20.30.14",
                        "port": 30882,
                        "timeout_ms": 500,
                        "retry_attempts": 1,
                    },
                    "amplification": {
                        "enabled": True,
                        "score_cap": 1.0,
                        "skip_threshold": 0.70,
                        "amplify_medium": True,
                        "vigil_thresholds": {
                            "critical": 0.8,
                            "high": 0.6,
                            "moderate": 0.4,
                        },
                        "boosts": {
                            "critical_boost": 0.35,
                            "critical_minimum": 0.55,
                            "high_multiplier": 0.3,
                            "moderate_multiplier": 0.1,
                        },
                    },
                    "circuit_breaker": {
                        "state": "closed",
                        "consecutive_failures": 0,
                        "failure_threshold": 3,
                        "recovery_timeout_seconds": 30,
                        "total_failures": 2,
                        "total_successes": 1523,
                    },
                    "stats": {
                        "calls": 1525,
                        "amplifications": 312,
                        "amplification_rate": 0.2046,
                        "average_latency_ms": 28.5,
                        "success_rate": 0.9987,
                    },
                }
            ]
        }
    }


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
# Context Configuration Schemas (Phase 5)
# =============================================================================


class EscalationConfigResponse(BaseModel):
    """Escalation detection configuration (Phase 5)."""

    enabled: bool = Field(description="Whether escalation detection is enabled")
    rapid_threshold_hours: int = Field(description="Hours threshold for rapid escalation")
    gradual_threshold_hours: int = Field(description="Hours threshold for gradual escalation")
    score_increase_threshold: float = Field(description="Score increase to trigger detection")
    minimum_messages: int = Field(description="Minimum messages needed for detection")
    alert_on_detection: bool = Field(description="Whether to alert on detection")
    alert_cooldown_seconds: int = Field(description="Cooldown between alerts")


class TemporalConfigResponse(BaseModel):
    """Temporal detection configuration (Phase 5)."""

    enabled: bool = Field(description="Whether temporal detection is enabled")
    late_night_start_hour: int = Field(description="Hour when late night starts (0-23)")
    late_night_end_hour: int = Field(description="Hour when late night ends (0-23)")
    late_night_risk_modifier: float = Field(description="Risk modifier for late night")
    rapid_posting_threshold_minutes: int = Field(description="Minutes for rapid posting")
    rapid_posting_message_count: int = Field(description="Messages for rapid posting")


class TrendConfigResponse(BaseModel):
    """Trend analysis configuration (Phase 5)."""

    enabled: bool = Field(description="Whether trend analysis is enabled")
    worsening_threshold: float = Field(description="Score change for worsening")
    improving_threshold: float = Field(description="Score change for improving")
    velocity_rapid_threshold: float = Field(description="Threshold for rapid velocity")


class ContextConfigResponse(BaseModel):
    """
    Current context analysis configuration (Phase 5).
    
    Returns all configuration for escalation detection,
    temporal patterns, and trend analysis.
    """

    enabled: bool = Field(description="Whether context analysis is enabled")
    max_history_size: int = Field(description="Maximum messages in history")
    escalation: EscalationConfigResponse = Field(description="Escalation config")
    temporal: TemporalConfigResponse = Field(description="Temporal config")
    trend: TrendConfigResponse = Field(description="Trend config")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "enabled": True,
                    "max_history_size": 20,
                    "escalation": {
                        "enabled": True,
                        "rapid_threshold_hours": 4,
                        "gradual_threshold_hours": 24,
                        "score_increase_threshold": 0.3,
                        "minimum_messages": 3,
                        "alert_on_detection": True,
                        "alert_cooldown_seconds": 300,
                    },
                    "temporal": {
                        "enabled": True,
                        "late_night_start_hour": 22,
                        "late_night_end_hour": 4,
                        "late_night_risk_modifier": 1.2,
                        "rapid_posting_threshold_minutes": 30,
                        "rapid_posting_message_count": 5,
                    },
                    "trend": {
                        "enabled": True,
                        "worsening_threshold": 0.15,
                        "improving_threshold": -0.15,
                        "velocity_rapid_threshold": 0.1,
                    },
                }
            ]
        }
    }


class ContextConfigUpdateRequest(BaseModel):
    """
    Request to update context analysis configuration (Phase 5).
    
    Only provided fields will be updated.
    """

    enabled: Optional[bool] = Field(
        default=None,
        description="Enable/disable context analysis",
    )
    max_history_size: Optional[int] = Field(
        default=None,
        ge=3,
        le=50,
        description="Maximum messages in history (3-50)",
    )
    escalation_enabled: Optional[bool] = Field(
        default=None,
        description="Enable/disable escalation detection",
    )
    temporal_enabled: Optional[bool] = Field(
        default=None,
        description="Enable/disable temporal detection",
    )
    trend_enabled: Optional[bool] = Field(
        default=None,
        description="Enable/disable trend analysis",
    )
    alert_on_escalation: Optional[bool] = Field(
        default=None,
        description="Enable/disable escalation alerts",
    )
    alert_cooldown_seconds: Optional[int] = Field(
        default=None,
        ge=60,
        le=3600,
        description="Cooldown between alerts (60-3600 seconds)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "enabled": True,
                    "max_history_size": 20,
                    "alert_on_escalation": True,
                    "alert_cooldown_seconds": 300,
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


class VigilStatusResponse(BaseModel):
    """
    Vigil component status (Phase 3 Vigil).
    
    Used in health and status endpoints.
    """

    enabled: bool = Field(description="Whether Vigil integration is enabled")
    healthy: bool = Field(description="Whether Vigil is currently healthy")
    circuit_state: str = Field(
        default="unknown",
        description="Circuit breaker state: closed, open, half_open",
    )
    calls: int = Field(default=0, description="Total Vigil calls")
    amplifications: int = Field(default=0, description="Total amplifications applied")


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
    # Phase 3 Vigil fields
    vigil_enabled: bool = Field(
        default=False,
        description="Whether Vigil integration is enabled (Phase 3 Vigil)",
    )
    vigil_healthy: bool = Field(
        default=False,
        description="Whether Vigil is currently healthy (Phase 3 Vigil)",
    )
    phase4_enabled: bool = Field(
        default=True,
        description="Whether Phase 4 features are enabled",
    )
    phase5_enabled: bool = Field(
        default=True,
        description="Whether Phase 5 features are enabled",
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
                    "vigil_enabled": True,
                    "vigil_healthy": True,
                    "phase4_enabled": True,
                    "phase5_enabled": True,
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
    # Phase 3 Vigil status
    vigil: Optional[VigilStatusResponse] = Field(
        default=None,
        description="Vigil component status (Phase 3 Vigil)",
    )
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
    requires_review: bool = Field(
        default=False,
        description="Whether CRT review is recommended (Phase 3 Vigil)",
    )
    vigil_status: Optional[VigilStatus] = Field(
        default=None,
        description="Vigil integration status (Phase 3 Vigil)",
    )
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


class EscalationAlertPayload(BaseModel):
    """
    Payload for escalation detection alert webhooks (Phase 5).

    Sent to Discord when an escalation pattern is detected.
    """

    alert_type: str = Field(default="escalation_detected")
    escalation_rate: EscalationRate = Field(description="Rate of escalation")
    escalation_pattern: Optional[str] = Field(
        default=None,
        description="Matched escalation pattern name",
    )
    pattern_confidence: float = Field(description="Confidence in pattern match")
    crisis_score: float = Field(description="Current crisis score")
    score_delta: float = Field(description="Score change during escalation")
    time_span_hours: float = Field(description="Time span of escalation")
    intervention_urgency: InterventionUrgency = Field(
        description="Recommended intervention urgency",
    )
    message_preview: str = Field(description="First 100 chars of message")
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


class VigilUnavailableAlertPayload(BaseModel):
    """
    Payload for Vigil unavailability alert webhooks (Phase 3 Vigil).

    Sent to Discord when Vigil becomes unavailable or circuit opens.
    """

    alert_type: str = Field(default="vigil_unavailable")
    vigil_status: VigilStatus = Field(description="Current Vigil status")
    circuit_state: str = Field(description="Circuit breaker state")
    consecutive_failures: int = Field(description="Number of consecutive failures")
    last_error: Optional[str] = Field(
        default=None,
        description="Last error message",
    )
    recovery_in_seconds: Optional[int] = Field(
        default=None,
        description="Seconds until recovery attempt",
    )
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "SeverityLevel",
    "RecommendedAction",
    "HealthStatus",
    # Phase 3 Vigil Enums
    "VigilStatus",
    # Phase 4 Enums
    "ConsensusAlgorithm",
    "ResolutionStrategy",
    "VerbosityLevel",
    "ConflictType",
    "ConflictSeverity",
    "AgreementLevel",
    # Phase 5 Enums
    "InterventionUrgency",
    "TrendDirection",
    "TrendVelocity",
    "EscalationRate",
    # Request schemas
    "AnalyzeRequest",
    "BatchAnalyzeRequest",
    "MessageHistoryItemRequest",
    "ConsensusConfigUpdateRequest",
    "ContextConfigUpdateRequest",
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
    # Phase 3 Vigil Response components
    "VigilResponse",
    "VigilConfigResponse",
    "VigilAmplificationConfigResponse",
    "VigilClientConfigResponse",
    "VigilCircuitBreakerResponse",
    "VigilStatsResponse",
    "VigilStatusResponse",
    # Phase 4 Response components
    "ExplanationResponse",
    "ConflictAnalysisResponse",
    "DetectedConflictResponse",
    "ConsensusResponse",
    "ConsensusConfigResponse",
    "Phase4StatusResponse",
    # Phase 5 Response components
    "ContextAnalysisResponse",
    "EscalationResponse",
    "TemporalFactorsResponse",
    "TrendResponse",
    "TrajectoryResponse",
    "InterventionResponse",
    "HistoryMetadataResponse",
    "ContextConfigResponse",
    "EscalationConfigResponse",
    "TemporalConfigResponse",
    "TrendConfigResponse",
    # Webhook schemas
    "CrisisAlertPayload",
    "ConflictAlertPayload",
    "EscalationAlertPayload",
    "VigilUnavailableAlertPayload",
]
