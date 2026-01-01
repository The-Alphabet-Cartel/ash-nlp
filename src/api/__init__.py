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
API Package for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.4-5
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.4 - API Package
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package provides the FastAPI application and all API components:

COMPONENTS:
- app: FastAPI application factory and default instance
- routes: API endpoint definitions
- schemas: Pydantic request/response models
- middleware: Request processing middleware

USAGE:
    # Run with uvicorn
    uvicorn src.api.app:app --host 0.0.0.0 --port 30880

    # Or create custom app
    from src.api import create_app
    app = create_app(config_manager=config)

ENDPOINTS:
    POST /analyze         - Analyze single message
    POST /analyze/batch   - Analyze multiple messages
    GET  /health          - Health check
    GET  /status          - Detailed status
    GET  /models          - Model information
"""

# Module version
__version__ = "v5.0-3-4.4-5"

# =============================================================================
# Application Factory and Instance
# =============================================================================

from .app import (
    app,
    create_app,
    create_testing_app,
    create_production_app,
    lifespan,
)

# =============================================================================
# Routers
# =============================================================================

from .routes import (
    analysis_router,
    health_router,
    models_router,
)

# =============================================================================
# Schemas (Request/Response Models)
# =============================================================================

from .schemas import (
    # Enums
    SeverityLevel,
    RecommendedAction,
    HealthStatus,
    # Request schemas
    AnalyzeRequest,
    BatchAnalyzeRequest,
    # Response schemas
    AnalyzeResponse,
    ModelSignalResponse,
    BatchAnalyzeResponse,
    BatchAnalyzeResponseItem,
    HealthResponse,
    StatusResponse,
    ModelStatusResponse,
    ErrorResponse,
    ErrorDetail,
    # Webhook schemas
    CrisisAlertPayload,
)

# =============================================================================
# Middleware
# =============================================================================

from .middleware import (
    RequestIDMiddleware,
    LoggingMiddleware,
    ErrorHandlingMiddleware,
    RateLimitMiddleware,
    RequestContext,
    setup_middleware,
    get_request_context,
    get_request_id,
    REQUEST_ID_HEADER,
)

# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Version
    "__version__",
    # Application
    "app",
    "create_app",
    "create_testing_app",
    "create_production_app",
    "lifespan",
    # Routers
    "analysis_router",
    "health_router",
    "models_router",
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
    "CrisisAlertPayload",
    # Middleware
    "RequestIDMiddleware",
    "LoggingMiddleware",
    "ErrorHandlingMiddleware",
    "RateLimitMiddleware",
    "RequestContext",
    "setup_middleware",
    "get_request_context",
    "get_request_id",
    "REQUEST_ID_HEADER",
]
