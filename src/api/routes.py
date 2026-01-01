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
API Routes for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.4-3
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.4 - API Layer
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Define API endpoints for crisis detection
- Handle request validation and response formatting
- Integrate with Decision Engine for analysis
- Provide health and status endpoints

ENDPOINTS:
- POST /analyze - Analyze single message for crisis signals
- POST /analyze/batch - Analyze multiple messages
- GET /health - Health check for load balancers
- GET /status - Detailed service status
- GET /models - Model information
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BatchAnalyzeRequest,
    BatchAnalyzeResponse,
    BatchAnalyzeResponseItem,
    HealthResponse,
    StatusResponse,
    ModelStatusResponse,
    ModelSignalResponse,
    ErrorResponse,
    SeverityLevel,
    RecommendedAction,
    HealthStatus,
)
from .middleware import get_request_id

# Module version
__version__ = "v5.0-3-4.4-3"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Router Setup
# =============================================================================

# Main analysis router
analysis_router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)

# Health and status router
health_router = APIRouter(
    tags=["Health"],
)

# Models router
models_router = APIRouter(
    prefix="/models",
    tags=["Models"],
)


# =============================================================================
# Dependency Injection
# =============================================================================


# Engine will be injected via app.state
def get_engine(request: Request):
    """Get decision engine from app state."""
    engine = getattr(request.app.state, "engine", None)
    if engine is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized",
        )
    return engine


def get_config(request: Request):
    """Get config manager from app state."""
    return getattr(request.app.state, "config", None)


def get_start_time(request: Request) -> float:
    """Get service start time from app state."""
    return getattr(request.app.state, "start_time", time.time())


# =============================================================================
# Analysis Endpoints
# =============================================================================


@analysis_router.post(
    "",
    response_model=AnalyzeResponse,
    responses={
        200: {"description": "Successful analysis"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
    summary="Analyze message for crisis signals",
    description="""
    Analyze a text message for crisis signals using the multi-model ensemble.

    The ensemble combines:
    - BART Zero-Shot Classification (primary, weight 0.50)
    - Cardiff Sentiment Analysis (secondary, weight 0.25)
    - Cardiff Irony Detection (tertiary, weight 0.15)
    - RoBERTa Emotions Classification (supplementary, weight 0.10)

    Returns a comprehensive crisis assessment including severity level,
    confidence score, and recommended action.
    """,
)
async def analyze_message(
    request: Request,
    body: AnalyzeRequest,
    engine=Depends(get_engine),
) -> AnalyzeResponse:
    """
    Analyze a single message for crisis signals.

    This is the primary endpoint for crisis detection.
    """
    request_id = get_request_id(request)

    logger.info(
        f"Analyzing message (length={len(body.message)})",
        extra={
            "request_id": request_id,
            "user_id": body.user_id,
            "channel_id": body.channel_id,
        },
    )

    try:
        # Run analysis
        assessment = engine.analyze(body.message)

        # Convert signals to response format
        signals = {}
        for name, signal_data in assessment.signals.items():
            if isinstance(signal_data, dict):
                signals[name] = ModelSignalResponse(
                    label=signal_data.get("label", "unknown"),
                    score=signal_data.get("score", 0.0),
                    crisis_signal=signal_data.get("crisis_signal", 0.0),
                )

        # Build response
        response = AnalyzeResponse(
            crisis_detected=assessment.crisis_detected,
            severity=SeverityLevel(assessment.severity.value),
            confidence=assessment.confidence,
            crisis_score=assessment.crisis_score,
            requires_intervention=assessment.requires_intervention,
            recommended_action=RecommendedAction(assessment.recommended_action),
            signals=signals,
            processing_time_ms=assessment.processing_time_ms,
            models_used=assessment.models_used,
            is_degraded=assessment.is_degraded,
            request_id=request_id,
            timestamp=datetime.utcnow(),
        )

        # Log crisis detections
        if assessment.crisis_detected:
            logger.warning(
                f"Crisis detected: severity={assessment.severity.value}, "
                f"score={assessment.crisis_score:.2f}",
                extra={
                    "request_id": request_id,
                    "severity": assessment.severity.value,
                    "crisis_score": assessment.crisis_score,
                    "user_id": body.user_id,
                },
            )

        return response

    except Exception as e:
        logger.error(
            f"Analysis failed: {e}",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@analysis_router.post(
    "/batch",
    response_model=BatchAnalyzeResponse,
    responses={
        200: {"description": "Successful batch analysis"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
    summary="Analyze multiple messages",
    description="""
    Analyze multiple messages in a single request.

    Useful for processing historical messages or bulk analysis.
    Maximum 100 messages per request.
    """,
)
async def analyze_batch(
    request: Request,
    body: BatchAnalyzeRequest,
    engine=Depends(get_engine),
) -> BatchAnalyzeResponse:
    """
    Analyze multiple messages in batch.
    """
    request_id = get_request_id(request)

    logger.info(
        f"Batch analysis: {len(body.messages)} messages",
        extra={"request_id": request_id},
    )

    start_time = time.perf_counter()
    results: List[BatchAnalyzeResponseItem] = []
    crisis_count = 0
    critical_count = 0
    high_count = 0

    try:
        for idx, message in enumerate(body.messages):
            assessment = engine.analyze(message)

            # Create preview
            preview = message[:50] + "..." if len(message) > 50 else message

            results.append(
                BatchAnalyzeResponseItem(
                    index=idx,
                    message_preview=preview,
                    crisis_detected=assessment.crisis_detected,
                    severity=SeverityLevel(assessment.severity.value),
                    crisis_score=assessment.crisis_score,
                    requires_intervention=assessment.requires_intervention,
                )
            )

            if assessment.crisis_detected:
                crisis_count += 1
            if assessment.severity.value == "critical":
                critical_count += 1
            elif assessment.severity.value == "high":
                high_count += 1

        processing_time_ms = (time.perf_counter() - start_time) * 1000

        return BatchAnalyzeResponse(
            total_messages=len(body.messages),
            crisis_count=crisis_count,
            critical_count=critical_count,
            high_count=high_count,
            results=results,
            processing_time_ms=processing_time_ms,
            request_id=request_id,
            timestamp=datetime.utcnow(),
        )

    except Exception as e:
        logger.error(
            f"Batch analysis failed: {e}",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch analysis failed: {str(e)}",
        )


# =============================================================================
# Health Endpoints
# =============================================================================


@health_router.get(
    "/health",
    response_model=HealthResponse,
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"},
    },
    summary="Health check",
    description="Simple health check for load balancers and orchestration.",
)
async def health_check(
    request: Request,
    start_time: float = Depends(get_start_time),
) -> HealthResponse:
    """
    Health check endpoint.

    Returns 200 if service is healthy, 503 if not.
    """
    engine = getattr(request.app.state, "engine", None)

    if engine is None:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=HealthResponse(
                status=HealthStatus.UNHEALTHY,
                ready=False,
                degraded=False,
                models_loaded=0,
                total_models=4,
                version=__version__,
            ).model_dump(mode="json"),
        )

    health = engine.get_health()
    uptime = time.time() - start_time

    health_status = HealthStatus.HEALTHY
    if not health.get("ready", False):
        health_status = HealthStatus.UNHEALTHY
    elif health.get("degraded", False):
        health_status = HealthStatus.DEGRADED

    response = HealthResponse(
        status=health_status,
        ready=health.get("ready", False),
        degraded=health.get("degraded", False),
        models_loaded=health.get("models_loaded", 0),
        total_models=health.get("total_models", 4),
        uptime_seconds=uptime,
        version=__version__,
        timestamp=datetime.utcnow(),
    )

    if health_status == HealthStatus.UNHEALTHY:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response.model_dump(mode="json"),
        )

    return response


@health_router.get(
    "/healthz",
    response_model=HealthResponse,
    include_in_schema=False,  # Kubernetes style, not in docs
)
async def healthz(
    request: Request,
    start_time: float = Depends(get_start_time),
) -> HealthResponse:
    """Kubernetes-style health check (alias for /health)."""
    return await health_check(request, start_time)


@health_router.get(
    "/ready",
    responses={
        200: {"description": "Service is ready"},
        503: {"description": "Service is not ready"},
    },
    summary="Readiness check",
    description="Check if service is ready to accept traffic.",
)
async def readiness_check(request: Request) -> Dict[str, Any]:
    """
    Readiness check for Kubernetes.

    Returns 200 only when models are loaded and service is ready.
    """
    engine = getattr(request.app.state, "engine", None)

    if engine is None or not engine.is_ready():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"ready": False, "message": "Service not ready"},
        )

    return {"ready": True, "message": "Service is ready"}


@health_router.get(
    "/status",
    response_model=StatusResponse,
    summary="Detailed service status",
    description="Get comprehensive status information about the service.",
)
async def get_status(
    request: Request,
    engine=Depends(get_engine),
    config=Depends(get_config),
) -> StatusResponse:
    """
    Get detailed service status.

    Includes model status, statistics, and configuration.
    """
    status_data = engine.get_status()

    # Build model status list
    models = []
    for name, info in status_data.get("models", {}).get("models", {}).items():
        models.append(
            ModelStatusResponse(
                name=name,
                loaded=info.get("loaded", False),
                enabled=info.get("enabled", True),
                device=info.get("device"),
                weight=status_data.get("weights", {}).get(name, 0.0),
                average_latency_ms=info.get("stats", {}).get("average_latency_ms"),
            )
        )

    # Determine health status
    health_status = HealthStatus.HEALTHY
    if not status_data.get("is_ready", False):
        health_status = HealthStatus.UNHEALTHY
    elif status_data.get("is_degraded", False):
        health_status = HealthStatus.DEGRADED

    # Get environment from config
    environment = "production"
    if config:
        environment = getattr(config, "environment", "production")

    return StatusResponse(
        service="ash-nlp",
        version=__version__,
        environment=environment,
        status=health_status,
        ready=status_data.get("is_ready", False),
        degraded=status_data.get("is_degraded", False),
        degradation_reason=status_data.get("degradation_reason"),
        models=models,
        stats=status_data.get("stats", {}),
        config={
            "weights": status_data.get("weights", {}),
            "thresholds": status_data.get("thresholds", {}),
            "async_inference": status_data.get("async_inference", True),
        },
        timestamp=datetime.utcnow(),
    )


# =============================================================================
# Models Endpoints
# =============================================================================


@models_router.get(
    "",
    response_model=List[ModelStatusResponse],
    summary="List models",
    description="Get information about all ensemble models.",
)
async def list_models(
    engine=Depends(get_engine),
) -> List[ModelStatusResponse]:
    """
    List all models in the ensemble.
    """
    status_data = engine.get_status()
    weights = status_data.get("weights", {})

    models = []
    for name, info in status_data.get("models", {}).get("models", {}).items():
        models.append(
            ModelStatusResponse(
                name=name,
                loaded=info.get("loaded", False),
                enabled=info.get("enabled", True),
                device=info.get("device"),
                weight=weights.get(name, 0.0),
                average_latency_ms=info.get("stats", {}).get("average_latency_ms"),
            )
        )

    return models


@models_router.get(
    "/{model_name}",
    response_model=ModelStatusResponse,
    responses={
        200: {"description": "Model found"},
        404: {"description": "Model not found"},
    },
    summary="Get model details",
    description="Get detailed information about a specific model.",
)
async def get_model(
    model_name: str,
    engine=Depends(get_engine),
) -> ModelStatusResponse:
    """
    Get details for a specific model.
    """
    status_data = engine.get_status()
    models_data = status_data.get("models", {}).get("models", {})
    weights = status_data.get("weights", {})

    if model_name not in models_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_name}' not found",
        )

    info = models_data[model_name]

    return ModelStatusResponse(
        name=model_name,
        loaded=info.get("loaded", False),
        enabled=info.get("enabled", True),
        device=info.get("device"),
        weight=weights.get(model_name, 0.0),
        average_latency_ms=info.get("stats", {}).get("average_latency_ms"),
    )


# =============================================================================
# Root Endpoint
# =============================================================================


@health_router.get(
    "/",
    summary="Service info",
    description="Basic service information.",
)
async def root() -> Dict[str, str]:
    """
    Root endpoint with basic service info.
    """
    return {
        "service": "ash-nlp",
        "version": __version__,
        "description": "Crisis Detection Backend for The Alphabet Cartel Discord Community",
        "docs": "/docs",
        "health": "/health",
    }


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "analysis_router",
    "health_router",
    "models_router",
]
