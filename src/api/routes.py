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
FILE VERSION: v5.0-5-5.2-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Define API endpoints for crisis detection
- Handle request validation and response formatting
- Integrate with Decision Engine for analysis
- Provide health and status endpoints

PHASE 4 ENHANCEMENTS:
- Consensus configuration endpoint
- Enhanced analysis with explanations
- Conflict analysis in responses

PHASE 5 ENHANCEMENTS:
- Message history input for context analysis
- Context analysis in responses
- Context configuration endpoints

ENDPOINTS:
- POST /analyze - Analyze single message for crisis signals
- POST /analyze/batch - Analyze multiple messages
- GET /health - Health check for load balancers
- GET /status - Detailed service status
- GET /models - Model information
- GET /config/consensus - Get consensus configuration (Phase 4)
- PUT /config/consensus - Update consensus configuration (Phase 4)
- GET /config/context - Get context configuration (Phase 5)
- PUT /config/context - Update context configuration (Phase 5)
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .schemas import (
    # Request schemas
    AnalyzeRequest,
    AnalyzeResponse,
    BatchAnalyzeRequest,
    BatchAnalyzeResponse,
    BatchAnalyzeResponseItem,
    ConsensusConfigUpdateRequest,
    ContextConfigUpdateRequest,
    # Response schemas
    HealthResponse,
    StatusResponse,
    ModelStatusResponse,
    ModelSignalResponse,
    ErrorResponse,
    # Phase 3 Vigil Response schemas
    VigilStatusResponse,
    # Phase 4 Response schemas
    ExplanationResponse,
    ConflictAnalysisResponse,
    DetectedConflictResponse,
    ConsensusResponse,
    ConsensusConfigResponse,
    Phase4StatusResponse,
    # Phase 5 Response schemas
    ContextAnalysisResponse,
    TrendResponse,
    TemporalFactorsResponse,
    TrajectoryResponse,
    InterventionResponse,
    HistoryMetadataResponse,
    ContextConfigResponse,
    EscalationConfigResponse,
    TemporalConfigResponse,
    TrendConfigResponse,
    # Enums
    SeverityLevel,
    RecommendedAction,
    HealthStatus,
    ConsensusAlgorithm,
    ResolutionStrategy,
    VerbosityLevel,
    ConflictType,
    ConflictSeverity,
    AgreementLevel,
    # Phase 5 Enums
    InterventionUrgency,
    TrendDirection,
    TrendVelocity,
    EscalationRate,
)
from .middleware import get_request_id

# Module version
__version__ = "v5.0-5-5.2-1"

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

# Phase 4: Configuration router
config_router = APIRouter(
    prefix="/config",
    tags=["Configuration"],
)


# =============================================================================
# Dependency Injection
# =============================================================================


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
    - BART Zero-Shot Classification (primary, weight 0.65)
    - DeBERTa Sentiment Zero-Shot Analyzer (secondary, weight 0.25)
    - Cardiff Irony Detection (gatekeeper — post-scoring, not additive)
    - DeBERTa Emotions Zero-Shot Analyzer (supplementary, weight 0.10)

    **Phase 4 Features:**
    - Multiple consensus algorithms (weighted_voting, majority_voting, unanimous, conflict_aware)
    - Conflict detection and resolution
    - Human-readable explanations with configurable verbosity

    **Phase 5 Features:**
    - Context history analysis with message_history input
    - Escalation pattern detection (rapid, gradual, sudden)
    - Temporal pattern detection (late night, rapid posting)
    - Trend analysis (worsening, stable, improving)
    - Intervention urgency recommendations

    Returns a comprehensive crisis assessment including severity level,
    confidence score, recommended action, optional explanation, and context analysis.
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
    Supports Phase 4 and Phase 5 enhanced options.
    """
    request_id = get_request_id(request)
    history_count = len(body.message_history) if body.message_history else 0

    logger.info(
        f"Analyzing message (length={len(body.message)}, history={history_count})",
        extra={
            "request_id": request_id,
            "user_id": body.user_id,
            "channel_id": body.channel_id,
            "include_explanation": body.include_explanation,
            "include_context_analysis": body.include_context_analysis,
            "history_count": history_count,
            "verbosity": body.verbosity.value if body.verbosity else None,
            "consensus_algorithm": body.consensus_algorithm.value if body.consensus_algorithm else None,
        },
    )

    try:
        # Convert message history to format expected by engine
        message_history = None
        if body.message_history and body.include_context_analysis:
            message_history = [
                {
                    "message": item.message,
                    "timestamp": item.timestamp.isoformat(),
                    "crisis_score": item.crisis_score,
                }
                for item in body.message_history
            ]

        # Run analysis with Phase 4 and Phase 5 options
        assessment = engine.analyze(
            message=body.message,
            include_explanation=body.include_explanation,
            verbosity=body.verbosity.value if body.verbosity else None,
            consensus_algorithm=body.consensus_algorithm.value if body.consensus_algorithm else None,
            message_history=message_history,
            include_context_analysis=body.include_context_analysis,
        )

        # Convert signals to response format
        signals = {}
        for name, signal_data in assessment.signals.items():
            if isinstance(signal_data, dict):
                signals[name] = ModelSignalResponse(
                    label=signal_data.get("label", "unknown"),
                    score=signal_data.get("score", 0.0),
                    crisis_signal=signal_data.get("crisis_signal", 0.0),
                )

        # Build base response
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

        # Add Phase 4 enhanced fields
        if assessment.explanation:
            response.explanation = _build_explanation_response(assessment.explanation)

        if assessment.conflict_report:
            response.conflict_analysis = _build_conflict_response(
                assessment.conflict_report,
                assessment.aggregated_result.resolution if assessment.aggregated_result else None,
            )

        if assessment.consensus_result:
            response.consensus = _build_consensus_response(assessment.consensus_result)

        # Add Phase 5 context analysis
        if hasattr(assessment, 'context_analysis') and assessment.context_analysis:
            response.context_analysis = _build_context_analysis_response(
                assessment.context_analysis
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

    **Note:** For performance, explanations are optional in batch mode
    and only a summary is returned when enabled.
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
        extra={"request_id": request_id, "include_explanation": body.include_explanation},
    )

    start_time = time.perf_counter()
    results: List[BatchAnalyzeResponseItem] = []
    crisis_count = 0
    critical_count = 0
    high_count = 0

    try:
        for idx, message in enumerate(body.messages):
            assessment = engine.analyze(
                message=message,
                include_explanation=body.include_explanation,
                verbosity="minimal" if body.include_explanation else None,
            )

            # Create preview
            preview = message[:50] + "..." if len(message) > 50 else message

            # Get explanation summary if requested
            explanation_summary = None
            if body.include_explanation and assessment.explanation:
                explanation_summary = assessment.explanation.get("decision_summary", "")

            results.append(
                BatchAnalyzeResponseItem(
                    index=idx,
                    message_preview=preview,
                    crisis_detected=assessment.crisis_detected,
                    severity=SeverityLevel(assessment.severity.value),
                    crisis_score=assessment.crisis_score,
                    requires_intervention=assessment.requires_intervention,
                    explanation_summary=explanation_summary,
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
# Phase 4: Configuration Endpoints
# =============================================================================


@config_router.get(
    "/consensus",
    response_model=ConsensusConfigResponse,
    summary="Get consensus configuration",
    description="""
    Get the current consensus algorithm configuration.

    **Phase 4 Feature**

    Returns:
    - Default algorithm being used
    - Available algorithms
    - Model weights
    - Thresholds
    - Conflict resolution settings
    - Explainability settings
    """,
)
async def get_consensus_config(
    engine=Depends(get_engine),
) -> ConsensusConfigResponse:
    """
    Get current consensus configuration.
    """
    status_data = engine.get_status()

    # Get Phase 4 config
    phase4_config = status_data.get("phase4", {})
    consensus_config = phase4_config.get("consensus", {}) or {}
    conflict_config = phase4_config.get("conflict_detection", {}) or {}
    resolution_config = phase4_config.get("conflict_resolution", {}) or {}
    explainability_config = phase4_config.get("explainability", {}) or {}

    return ConsensusConfigResponse(
        default_algorithm=ConsensusAlgorithm(
            consensus_config.get("algorithm", "weighted_voting")
        ),
        available_algorithms=list(ConsensusAlgorithm),
        weights=status_data.get("weights", {}),
        thresholds=consensus_config.get("thresholds", {}),
        conflict_detection_enabled=conflict_config.get("enabled", True),
        resolution_strategy=ResolutionStrategy(
            resolution_config.get("default_strategy", "conservative")
        ),
        explainability_verbosity=VerbosityLevel(
            explainability_config.get("default_verbosity", "standard")
        ),
    )


@config_router.put(
    "/consensus",
    response_model=ConsensusConfigResponse,
    summary="Update consensus configuration",
    description="""
    Update the consensus algorithm configuration.

    **Phase 4 Feature**

    Allows updating:
    - Default consensus algorithm
    - Conflict resolution strategy
    - Explainability verbosity
    - Threshold values

    Changes take effect immediately for new requests.
    """,
)
async def update_consensus_config(
    body: ConsensusConfigUpdateRequest,
    engine=Depends(get_engine),
) -> ConsensusConfigResponse:
    """
    Update consensus configuration.
    """
    logger.info(f"Updating consensus config: {body.model_dump(exclude_none=True)}")

    try:
        # Apply updates
        if body.default_algorithm:
            engine.set_consensus_algorithm(body.default_algorithm.value)

        if body.resolution_strategy:
            engine.set_resolution_strategy(body.resolution_strategy.value)

        if body.explainability_verbosity:
            engine.set_explainability_verbosity(body.explainability_verbosity.value)

        # Return updated config
        return await get_consensus_config(engine)

    except Exception as e:
        logger.error(f"Failed to update consensus config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration update failed: {str(e)}",
        )


# =============================================================================
# Phase 5: Context Configuration Endpoints
# =============================================================================


@config_router.get(
    "/context",
    response_model=ContextConfigResponse,
    summary="Get context configuration",
    description="""
    Get the current context analysis configuration.

    **Phase 5 Feature**

    Returns:
    - Whether context analysis is enabled
    - Maximum message history size
    - Escalation detection settings
    - Temporal pattern detection settings
    - Trend analysis settings
    """,
)
async def get_context_config(
    engine=Depends(get_engine),
) -> ContextConfigResponse:
    """
    Get current context analysis configuration.
    """
    # Get context config from engine
    context_config = engine.get_context_config() if hasattr(engine, 'get_context_config') else {}
    
    # Build escalation config
    escalation = context_config.get("escalation", {})
    escalation_response = EscalationConfigResponse(
        enabled=escalation.get("enabled", True),
        rapid_threshold_hours=escalation.get("rapid_threshold_hours", 4),
        gradual_threshold_hours=escalation.get("gradual_threshold_hours", 24),
        score_increase_threshold=escalation.get("score_increase_threshold", 0.3),
        minimum_messages=escalation.get("minimum_messages", 3),
        alert_on_detection=escalation.get("alert_on_detection", True),
        alert_cooldown_seconds=escalation.get("alert_cooldown_seconds", 300),
    )
    
    # Build temporal config
    temporal = context_config.get("temporal", {})
    temporal_response = TemporalConfigResponse(
        enabled=temporal.get("enabled", True),
        late_night_start_hour=temporal.get("late_night_start_hour", 22),
        late_night_end_hour=temporal.get("late_night_end_hour", 4),
        late_night_risk_modifier=temporal.get("late_night_risk_modifier", 1.2),
        rapid_posting_threshold_minutes=temporal.get("rapid_posting_threshold_minutes", 30),
        rapid_posting_message_count=temporal.get("rapid_posting_message_count", 5),
    )
    
    # Build trend config
    trend = context_config.get("trend", {})
    trend_response = TrendConfigResponse(
        enabled=trend.get("enabled", True),
        worsening_threshold=trend.get("worsening_threshold", 0.15),
        improving_threshold=trend.get("improving_threshold", -0.15),
        velocity_rapid_threshold=trend.get("velocity_rapid_threshold", 0.1),
    )
    
    return ContextConfigResponse(
        enabled=context_config.get("enabled", True),
        max_history_size=context_config.get("max_history_size", 20),
        escalation=escalation_response,
        temporal=temporal_response,
        trend=trend_response,
    )


@config_router.put(
    "/context",
    response_model=ContextConfigResponse,
    summary="Update context configuration",
    description="""
    Update the context analysis configuration.

    **Phase 5 Feature**

    Allows updating:
    - Enable/disable context analysis
    - Maximum message history size
    - Escalation alert settings
    - Individual feature toggles

    Changes take effect immediately for new requests.
    """,
)
async def update_context_config(
    body: ContextConfigUpdateRequest,
    engine=Depends(get_engine),
) -> ContextConfigResponse:
    """
    Update context analysis configuration.
    """
    logger.info(f"Updating context config: {body.model_dump(exclude_none=True)}")

    try:
        # Apply updates through engine
        if hasattr(engine, 'update_context_config'):
            updates = body.model_dump(exclude_none=True)
            engine.update_context_config(updates)

        # Return updated config
        return await get_context_config(engine)

    except Exception as e:
        logger.error(f"Failed to update context config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration update failed: {str(e)}",
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
                phase4_enabled=False,
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
        phase4_enabled=health.get("phase4_enabled", True),
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

    Includes model status, statistics, configuration, and Phase 4 status.
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

    # Build Phase 4 status
    phase4_status = None
    if status_data.get("phase4_enabled", True):
        phase4_config = status_data.get("phase4", {})
        consensus_config = phase4_config.get("consensus", {}) or {}
        resolution_config = phase4_config.get("conflict_resolution", {}) or {}
        explainability_config = phase4_config.get("explainability", {}) or {}

        phase4_status = Phase4StatusResponse(
            enabled=True,
            consensus_algorithm=ConsensusAlgorithm(
                consensus_config.get("algorithm", "weighted_voting")
            ) if consensus_config.get("algorithm") else None,
            resolution_strategy=ResolutionStrategy(
                resolution_config.get("default_strategy", "conservative")
            ) if resolution_config.get("default_strategy") else None,
            explainability_verbosity=VerbosityLevel(
                explainability_config.get("default_verbosity", "standard")
            ) if explainability_config.get("default_verbosity") else None,
            conflicts_detected=status_data.get("stats", {}).get("conflicts_detected", 0),
        )

    # Build Phase 3 Vigil status
    vigil_status = None
    vigil_data = status_data.get("vigil")
    if vigil_data and vigil_data.get("enabled", False):
        # Extract circuit breaker state from client_health
        client_health = vigil_data.get("client_health", {})
        circuit_breaker = client_health.get("circuit_breaker", {})
        circuit_state = circuit_breaker.get("state", "unknown")
        
        # Determine if Vigil is healthy (circuit closed and client enabled)
        is_healthy = (
            vigil_data.get("client_enabled", False) and
            circuit_state == "closed"
        )
        
        vigil_status = VigilStatusResponse(
            enabled=vigil_data.get("enabled", False),
            healthy=is_healthy,
            circuit_state=circuit_state,
            calls=status_data.get("stats", {}).get("vigil_calls", 0),
            amplifications=status_data.get("stats", {}).get("vigil_amplifications", 0),
        )

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
        vigil=vigil_status,
        phase4=phase4_status,
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
        "phase4": "enabled",
    }


# =============================================================================
# Helper Functions for Phase 4 Response Building
# =============================================================================


def _build_explanation_response(explanation_data: Dict[str, Any]) -> ExplanationResponse:
    """Build ExplanationResponse from explanation dict."""
    return ExplanationResponse(
        verbosity=VerbosityLevel(explanation_data.get("verbosity", "standard")),
        decision_summary=explanation_data.get("decision_summary", ""),
        key_factors=explanation_data.get("key_factors", []),
        recommended_action=explanation_data.get("recommended_action"),
        plain_text=explanation_data.get("plain_text", ""),
        confidence_summary=explanation_data.get("confidence_summary"),
        model_contributions=explanation_data.get("model_contributions"),
        conflict_summary=explanation_data.get("conflict_summary"),
    )


def _build_conflict_response(
    conflict_data: Dict[str, Any],
    resolution_data: Optional[Any] = None,
) -> ConflictAnalysisResponse:
    """Build ConflictAnalysisResponse from conflict report dict."""
    conflicts = []
    for conflict in conflict_data.get("conflicts", []):
        conflicts.append(
            DetectedConflictResponse(
                conflict_type=ConflictType(conflict.get("conflict_type", "score_disagreement")),
                severity=ConflictSeverity(conflict.get("severity", "medium")),
                description=conflict.get("description", ""),
                involved_models=conflict.get("involved_models", []),
                details=conflict.get("details", {}),
            )
        )

    response = ConflictAnalysisResponse(
        has_conflicts=conflict_data.get("has_conflicts", False),
        conflict_count=conflict_data.get("conflict_count", 0),
        conflicts=conflicts,
        highest_severity=ConflictSeverity(conflict_data["highest_severity"]) if conflict_data.get("highest_severity") else None,
        requires_review=conflict_data.get("requires_review", False),
        summary=conflict_data.get("summary", ""),
    )

    # Add resolution info if available
    if resolution_data:
        if hasattr(resolution_data, "to_dict"):
            res_dict = resolution_data.to_dict()
        else:
            res_dict = resolution_data

        response.resolution_strategy = ResolutionStrategy(
            res_dict.get("strategy_used", "conservative")
        )
        response.original_score = res_dict.get("original_score")
        response.resolved_score = res_dict.get("resolved_score")

    return response


def _build_consensus_response(consensus_data: Dict[str, Any]) -> ConsensusResponse:
    """Build ConsensusResponse from consensus result dict."""
    return ConsensusResponse(
        algorithm=ConsensusAlgorithm(consensus_data.get("algorithm", "weighted_voting")),
        crisis_score=consensus_data.get("crisis_score", 0.0),
        confidence=consensus_data.get("confidence", 0.0),
        agreement_level=AgreementLevel(consensus_data.get("agreement_level", "moderate_agreement")),
        is_crisis=consensus_data.get("is_crisis", False),
        requires_review=consensus_data.get("requires_review", False),
        has_conflict=consensus_data.get("has_conflict", False),
        individual_scores=consensus_data.get("individual_scores", {}),
        vote_breakdown=consensus_data.get("vote_breakdown"),
    )


# =============================================================================
# Helper Functions for Phase 5 Response Building
# =============================================================================


def _build_context_analysis_response(context_data: Any) -> ContextAnalysisResponse:
    """
    Build ContextAnalysisResponse from context analysis result.
    
    Handles both dict format and ContextAnalysisResult dataclass.
    """
    # Handle dataclass with to_dict method
    if hasattr(context_data, 'to_dict'):
        data = context_data.to_dict()
    elif hasattr(context_data, '__dict__'):
        # Handle dataclass directly
        data = _context_dataclass_to_dict(context_data)
    else:
        data = context_data
    
    # Build trend response
    trend_data = data.get("trend", {})
    trend = TrendResponse(
        direction=TrendDirection(trend_data.get("direction", "stable")),
        velocity=TrendVelocity(trend_data.get("velocity", "none")),
        score_delta=trend_data.get("score_delta", 0.0),
        time_span_hours=trend_data.get("time_span_hours", 0.0),
    )
    
    # Build temporal factors response
    temporal_data = data.get("temporal_factors", {})
    temporal = TemporalFactorsResponse(
        late_night_risk=temporal_data.get("late_night_risk", False),
        rapid_posting=temporal_data.get("rapid_posting", False),
        time_risk_modifier=temporal_data.get("time_risk_modifier", 1.0),
        hour_of_day=temporal_data.get("hour_of_day", 12),
        is_weekend=temporal_data.get("is_weekend", False),
    )
    
    # Build trajectory response
    trajectory_data = data.get("trajectory", {})
    trajectory = TrajectoryResponse(
        start_score=trajectory_data.get("start_score", 0.0),
        end_score=trajectory_data.get("end_score", 0.0),
        peak_score=trajectory_data.get("peak_score", trajectory_data.get("end_score", 0.0)),
        scores=trajectory_data.get("scores", []),
    )
    
    # Build intervention response
    intervention_data = data.get("intervention", {})
    intervention = InterventionResponse(
        urgency=InterventionUrgency(intervention_data.get("urgency", "none")),
        recommended_point=intervention_data.get("recommended_point"),
        intervention_delayed=intervention_data.get("intervention_delayed", False),
        reason=intervention_data.get("reason", ""),
    )
    
    # Build history metadata response
    history_data = data.get("history_analyzed", data.get("metadata", {}))
    history = HistoryMetadataResponse(
        message_count=history_data.get("message_count", 0),
        time_span_hours=history_data.get("time_span_hours", 0.0),
        oldest_timestamp=history_data.get("oldest_timestamp"),
        newest_timestamp=history_data.get("newest_timestamp"),
    )
    
    return ContextAnalysisResponse(
        escalation_detected=data.get("escalation_detected", False),
        escalation_rate=EscalationRate(data.get("escalation_rate", "none")),
        escalation_pattern=data.get("escalation_pattern"),
        pattern_confidence=data.get("pattern_confidence", 0.0),
        trend=trend,
        temporal_factors=temporal,
        trajectory=trajectory,
        intervention=intervention,
        history_analyzed=history,
    )


def _context_dataclass_to_dict(context_data: Any) -> Dict[str, Any]:
    """
    Convert ContextAnalysisResult dataclass to dict format.
    
    Handles nested dataclasses from the context module.
    """
    result = {}
    
    # Escalation fields
    if hasattr(context_data, 'escalation'):
        esc = context_data.escalation
        result["escalation_detected"] = esc.detected if hasattr(esc, 'detected') else False
        result["escalation_rate"] = esc.rate if hasattr(esc, 'rate') else "none"
        result["escalation_pattern"] = esc.pattern if hasattr(esc, 'pattern') else None
        result["pattern_confidence"] = esc.confidence if hasattr(esc, 'confidence') else 0.0
    
    # Trend fields
    if hasattr(context_data, 'trend'):
        trend = context_data.trend
        result["trend"] = {
            "direction": trend.direction if hasattr(trend, 'direction') else "stable",
            "velocity": trend.velocity if hasattr(trend, 'velocity') else "none",
            "score_delta": trend.score_delta if hasattr(trend, 'score_delta') else 0.0,
            "time_span_hours": trend.time_span_hours if hasattr(trend, 'time_span_hours') else 0.0,
        }
    
    # Temporal fields
    if hasattr(context_data, 'temporal'):
        temp = context_data.temporal
        result["temporal_factors"] = {
            "late_night_risk": temp.late_night_risk if hasattr(temp, 'late_night_risk') else False,
            "rapid_posting": temp.rapid_posting if hasattr(temp, 'rapid_posting') else False,
            "time_risk_modifier": temp.time_risk_modifier if hasattr(temp, 'time_risk_modifier') else 1.0,
            "hour_of_day": temp.hour_of_day if hasattr(temp, 'hour_of_day') else 12,
            "is_weekend": temp.is_weekend if hasattr(temp, 'is_weekend') else False,
        }
    
    # Trajectory fields
    if hasattr(context_data, 'trajectory'):
        traj = context_data.trajectory
        result["trajectory"] = {
            "start_score": traj.start_score if hasattr(traj, 'start_score') else 0.0,
            "end_score": traj.end_score if hasattr(traj, 'end_score') else 0.0,
            "peak_score": traj.max_score if hasattr(traj, 'max_score') else 0.0,
            "scores": traj.scores if hasattr(traj, 'scores') else [],
        }
    
    # Intervention fields
    if hasattr(context_data, 'intervention'):
        intv = context_data.intervention
        result["intervention"] = {
            "urgency": intv.urgency if hasattr(intv, 'urgency') else "none",
            "recommended_point": intv.recommended_point if hasattr(intv, 'recommended_point') else None,
            "intervention_delayed": intv.intervention_delayed if hasattr(intv, 'intervention_delayed') else False,
            "reason": intv.reason if hasattr(intv, 'reason') else "",
        }
    
    # Metadata fields
    if hasattr(context_data, 'metadata'):
        meta = context_data.metadata
        result["history_analyzed"] = {
            "message_count": meta.message_count if hasattr(meta, 'message_count') else 0,
            "time_span_hours": meta.time_span_hours if hasattr(meta, 'time_span_hours') else 0.0,
            "oldest_timestamp": None,
            "newest_timestamp": None,
        }
    
    return result


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "analysis_router",
    "health_router",
    "models_router",
    "config_router",
]
