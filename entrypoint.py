#!/usr/bin/env python3
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
Docker Entrypoint for Ash-NLP Service
---
FILE VERSION: v5.0-7-1.2-1
LAST MODIFIED: 2025-01-02
PHASE: Phase 7 Step 1.2 - Runtime Model Initialization
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

DESCRIPTION:
    Python-based Docker entrypoint that:
    1. Initializes/downloads HuggingFace models at startup
    2. Starts the FastAPI server via uvicorn

    This approach follows the project's "No Bash Scripting" philosophy
    while enabling runtime model caching.

USAGE:
    # Called automatically by Docker
    # Or manually:
    python entrypoint.py
"""

import logging
import os
import subprocess
import sys

# Module version
__version__ = "v5.0-7-1.2-1"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def run_model_initialization() -> bool:
    """
    Run the model initialization module.

    Returns:
        True if initialization succeeded
    """
    logger.info("=" * 60)
    logger.info("  Phase 1: Model Initialization")
    logger.info("=" * 60)

    try:
        # Import and run initialization
        from src.startup.model_initializer import initialize_models_sync

        success = initialize_models_sync()

        if success:
            logger.info("✅ Model initialization complete")
        else:
            logger.warning("⚠️  Model initialization incomplete - will use lazy loading")

        return success

    except ImportError as e:
        logger.error(f"❌ Failed to import model initializer: {e}")
        logger.warning("⚠️  Skipping model initialization - will use lazy loading")
        return False

    except Exception as e:
        logger.error(f"❌ Model initialization error: {e}")
        logger.warning("⚠️  Continuing with lazy loading fallback")
        return False


def start_server() -> int:
    """
    Start the uvicorn server.

    Returns:
        Exit code from uvicorn
    """
    logger.info("")
    logger.info("=" * 60)
    logger.info("  Phase 2: Starting Server")
    logger.info("=" * 60)

    # Get configuration from environment
    host = os.environ.get("NLP_API_HOST", "0.0.0.0")
    port = os.environ.get("NLP_API_PORT", "30880")
    workers = os.environ.get("NLP_API_WORKERS", "1")
    log_level = os.environ.get("NLP_LOG_LEVEL", "INFO").lower()

    logger.info(f"📡 Starting server at http://{host}:{port}")
    logger.info(f"👷 Workers: {workers}")
    logger.info(f"📝 Log level: {log_level}")
    logger.info("")

    # Build uvicorn command
    cmd = [
        sys.executable,  # Use same Python interpreter
        "-m", "uvicorn",
        "src.api.app:app",
        "--host", host,
        "--port", port,
        "--workers", workers,
        "--log-level", log_level,
    ]

    # Execute uvicorn (replaces this process)
    try:
        os.execvp(sys.executable, cmd)
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return 1

    # This line should never be reached (execvp replaces process)
    return 0


def main() -> int:
    """
    Main entrypoint function.

    Runs model initialization then starts the server.

    Returns:
        Exit code
    """
    logger.info("")
    logger.info("🚀 Ash-NLP Container Entrypoint")
    logger.info(f"   Version: {__version__}")
    logger.info("")

    # Phase 1: Initialize models (non-blocking on failure)
    run_model_initialization()

    # Phase 2: Start server
    return start_server()


if __name__ == "__main__":
    sys.exit(main())
