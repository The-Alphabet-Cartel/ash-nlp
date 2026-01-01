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
FastAPI Application Factory for Ash-NLP Service
---
FILE VERSION: v5.0-3-7.4-3
LAST MODIFIED: 2026-01-01
PHASE: Phase 3 Step 7 - Performance Optimization
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Create and configure FastAPI application
- Register routers and middleware
- Manage application lifespan (startup/shutdown)
- Initialize decision engine and configuration
- Provide CORS configuration
- Configure alerting and logging

PHASE 3.7 FEATURES:
- 3.7.1: Model warmup on startup with Discord alerting
- 3.7.2: Async parallel inference enabled by default
- 3.7.4: Response caching enabled by default
"""

import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.managers.config_manager import ConfigManager, create_config_manager
from src.ensemble import EnsembleDecisionEngine, create_decision_engine

from .routes import analysis_router, health_router, models_router
from .middleware import setup_middleware

# Module version
__version__ = "v5.0-3-7.4-3"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Application Lifespan
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events:
    - Startup: Configure logging, secrets, alerter, load models, warmup, send alerts
    - Shutdown: Gracefully shutdown engine, close alerter, release resources
    """
    # =========================================================================
    # STARTUP
    # =========================================================================

    logger.info("🚀 Starting Ash-NLP Service...")
    start_time = time.time()

    alerter = None

    try:
        # Configure logging from environment
        log_format = os.environ.get("NLP_LOG_FORMAT", "human")
        log_level = os.environ.get("NLP_LOG_LEVEL", "INFO")
        
        if log_format.lower() == "json":
            from src.utils.logging import setup_logging
            setup_logging(level=log_level, json_format=True)
            logger.info("JSON logging configured")

        # Configure secrets (HuggingFace token, etc.)
        logger.info("🔐 Configuring secrets...")
        from src.managers import create_secrets_manager

        secrets = create_secrets_manager()
        if secrets.configure_huggingface():
            logger.info("✅ HuggingFace token configured")
        else:
            logger.info("ℹ️  No HuggingFace token (using public models)")

        # Initialize Discord alerter (Phase 3.7.1)
        alerting_enabled = os.environ.get("NLP_ALERTING_ENABLED", "true").lower() == "true"
        if alerting_enabled:
            from src.utils.alerting import create_discord_alerter, set_alerter
            
            alerter = create_discord_alerter(secrets_manager=secrets)
            set_alerter(alerter)  # Set global alerter
            
            if alerter.enabled:
                logger.info("🔔 Discord alerting configured")
            else:
                logger.info("ℹ️  Discord alerting disabled (no webhook configured)")
        else:
            logger.info("ℹ️  Discord alerting disabled by configuration")

        # Get config manager from app state (set by factory)
        config = getattr(app.state, "config", None)

        if config is None:
            logger.info("Creating default configuration...")
            config = create_config_manager()
            app.state.config = config

        # Create decision engine with alerter
        logger.info("Initializing Decision Engine...")
        engine = create_decision_engine(
            config_manager=config,
            auto_initialize=False,
            alerter=alerter,
        )

        # Load models
        logger.info("Loading ensemble models...")
        init_success = engine.initialize()
        
        if not init_success:
            logger.error("❌ Engine initialization failed - service may be degraded")
            # Alert on failed startup
            if alerter and alerter.enabled:
                await alerter.send_critical(
                    title="Ash-NLP Startup Failed",
                    description="Engine initialization failed. Crisis detection unavailable.",
                    fields={"Status": "FAILED"},
                    source="startup",
                )

        # Warmup engine (Phase 3.7.1)
        logger.info("🔥 Warming up engine...")
        warmup_success = engine.warmup()
        
        if not warmup_success:
            logger.warning("⚠️ Engine warmup failed")

        # Store in app state
        app.state.engine = engine
        app.state.start_time = start_time
        app.state.secrets = secrets
        app.state.alerter = alerter

        startup_time = time.time() - start_time
        models_loaded = engine.model_loader._models_loaded
        total_models = len(engine.model_loader._models) if engine.model_loader._models else 4

        logger.info(f"✅ Ash-NLP Service started in {startup_time:.2f}s")

        # Send startup alert (Phase 3.7.1)
        if alerter and alerter.enabled:
            await alerter.alert_system_startup(
                models_loaded=models_loaded,
                total_models=total_models,
            )

    except Exception as e:
        logger.critical(f"❌ Failed to start service: {e}", exc_info=True)
        
        # Alert on critical startup failure
        if alerter and alerter.enabled:
            await alerter.send_critical(
                title="Ash-NLP Critical Startup Failure",
                description=f"Service failed to start: {str(e)[:200]}",
                source="startup",
            )
        
        raise

    # =========================================================================
    # YIELD (application runs here)
    # =========================================================================

    yield

    # =========================================================================
    # SHUTDOWN
    # =========================================================================

    logger.info("🛑 Shutting down Ash-NLP Service...")

    try:
        engine = getattr(app.state, "engine", None)
        if engine:
            engine.shutdown()

        # Close alerter session
        alerter = getattr(app.state, "alerter", None)
        if alerter:
            await alerter.close()

        logger.info("✅ Ash-NLP Service shutdown complete")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)


# =============================================================================
# Application Factory
# =============================================================================


def create_app(
    config_manager: Optional[ConfigManager] = None,
    enable_cors: bool = True,
    cors_origins: Optional[list] = None,
    enable_rate_limiting: bool = True,
    requests_per_minute: int = 60,
) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Factory function following Clean Architecture v5.1 (Rule #1).

    Args:
        config_manager: Pre-configured ConfigManager (optional)
        enable_cors: Enable CORS middleware
        cors_origins: Allowed CORS origins (default: all)
        enable_rate_limiting: Enable rate limiting middleware
        requests_per_minute: Rate limit threshold

    Returns:
        Configured FastAPI application

    Example:
        >>> app = create_app()
        >>> # Run with: uvicorn src.api.app:app

        >>> config = create_config_manager(environment="testing")
        >>> app = create_app(config_manager=config)
    """

    # =========================================================================
    # Create Application
    # =========================================================================

    app = FastAPI(
        title="Ash-NLP",
        description="""
# Ash-NLP Crisis Detection API

Crisis Detection Backend for [The Alphabet Cartel](https://discord.gg/alphabetcartel) Discord Community.

## Overview

Ash-NLP uses a multi-model ensemble for crisis detection:

| Model | Role | Weight | Purpose |
|-------|------|--------|---------|
| BART | Primary | 0.50 | Zero-shot crisis classification |
| Sentiment | Secondary | 0.25 | Emotional context analysis |
| Irony | Tertiary | 0.15 | Sarcasm detection (reduces false positives) |
| Emotions | Supplementary | 0.10 | Fine-grained emotion signals |

## Crisis Severity Levels

- **Critical** (≥0.85): Immediate intervention required
- **High** (≥0.70): Priority response needed
- **Medium** (≥0.50): Standard monitoring
- **Low** (≥0.30): Passive monitoring
- **Safe** (<0.30): No crisis detected

## Performance Features (v5.0)

- **Response Caching**: Repeated messages served from cache
- **Async Parallel Inference**: All models run concurrently
- **Model Warmup**: Consistent latency from first request

## Community

- Website: [alphabetcartel.org](https://alphabetcartel.org)
- Discord: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- GitHub: [github.com/the-alphabet-cartel](https://github.com/the-alphabet-cartel)
        """,
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        contact={
            "name": "The Alphabet Cartel",
            "url": "https://alphabetcartel.org",
        },
    )

    # =========================================================================
    # Store Config in State (for lifespan to access)
    # =========================================================================

    if config_manager:
        app.state.config = config_manager

    # =========================================================================
    # Configure CORS
    # =========================================================================

    if enable_cors:
        origins = cors_origins or ["*"]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        logger.debug(f"CORS enabled for origins: {origins}")

    # =========================================================================
    # Setup Custom Middleware
    # =========================================================================

    setup_middleware(
        app=app,
        enable_rate_limiting=enable_rate_limiting,
        requests_per_minute=requests_per_minute,
    )

    # =========================================================================
    # Register Routers
    # =========================================================================

    # Analysis endpoints (main functionality)
    app.include_router(analysis_router)

    # Health and status endpoints
    app.include_router(health_router)

    # Models information endpoints
    app.include_router(models_router)

    logger.info(
        f"🔧 Application created "
        f"(cors={enable_cors}, rate_limit={enable_rate_limiting})"
    )

    return app


# =============================================================================
# Default Application Instance
# =============================================================================

# Create default app for uvicorn
# Usage: uvicorn src.api.app:app --host 0.0.0.0 --port 30880
app = create_app()


# =============================================================================
# Convenience Functions
# =============================================================================


def create_testing_app() -> FastAPI:
    """
    Create application configured for testing.

    - Uses testing configuration
    - Disables rate limiting
    - Enables all CORS

    Returns:
        FastAPI application for testing
    """
    config = create_config_manager(environment="testing")

    return create_app(
        config_manager=config,
        enable_cors=True,
        cors_origins=["*"],
        enable_rate_limiting=False,
    )


def create_production_app() -> FastAPI:
    """
    Create application configured for production.

    - Uses production configuration
    - Enables rate limiting
    - Restricts CORS

    Returns:
        FastAPI application for production
    """
    config = create_config_manager(environment="production")

    # Get rate limiting config
    api_config = config.get_api_config() if config else {}
    rate_limit_enabled = api_config.get("rate_limit_enabled", True)
    rate_limit_rpm = api_config.get("rate_limit_rpm", 60)

    return create_app(
        config_manager=config,
        enable_cors=True,
        cors_origins=["https://alphabetcartel.org", "https://discord.gg"],
        enable_rate_limiting=rate_limit_enabled,
        requests_per_minute=rate_limit_rpm,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "app",
    "create_app",
    "create_testing_app",
    "create_production_app",
    "lifespan",
]
