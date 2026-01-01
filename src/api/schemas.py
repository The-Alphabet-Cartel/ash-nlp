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
FILE VERSION: v5.0-3-4.4-1
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.4 - API Layer
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Define Pydantic models for request validation
- Define response schemas for consistent API output
- Provide OpenAPI documentation through model configs
- Handle field validation and serialization
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# Module version
__version__ = "v5.0-3-4.4-1"


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


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "SeverityLevel",
    "RecommendedAction",
    "HealthStatus",
    # Request schemas
    "AnalyzeRequest",
    "BatchAnalyzeRequest",
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
    # Webhook schemas
    "CrisisAlertPayload",
]
