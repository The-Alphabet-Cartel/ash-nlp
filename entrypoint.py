#!/usr/bin/env python3
"""
============================================================================
Ash-NLP: Crisis Detection NLP Server
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Analyze  → Process messages through multi-model ensemble classification
    Detect   → Identify crisis signals with weighted consensus algorithms
    Explain  → Provide human-readable explanations for all decisions
    Protect  → Safeguard our LGBTQIA+ community through accurate detection

============================================================================
Docker Entrypoint for Ash-NLP Service
---
FILE VERSION: v5.0-8-1.1-1
LAST MODIFIED: 2026-01-05
PHASE: Phase 8 Step 1.1 - PUID/PGID Support in Entrypoint
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================
DESCRIPTION:
    Python-based Docker entrypoint that:
    1. Sets up user/group based on PUID/PGID environment variables
    2. Fixes ownership of application directories
    3. Initializes/downloads HuggingFace models at startup
    4. Drops privileges to the configured user
    5. Starts the FastAPI server via uvicorn

    This approach follows the project's "No Bash Scripting" philosophy
    while enabling LinuxServer.io-style user configuration.

USAGE:
    # Called automatically by Docker
    # Or manually:
    python entrypoint.py

    # With custom PUID/PGID:
    PUID=1000 PGID=1000 python entrypoint.py
"""

import logging
import os
import subprocess
import sys

# Module version
__version__ = "v5.0-8-1.1-1"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def run_user_setup() -> tuple:
    """
    Run the user/permissions setup phase.

    Returns:
        Tuple of (puid, pgid) that were configured
    """
    try:
        from src.startup.user_setup import setup_user_and_permissions

        return setup_user_and_permissions()
    except ImportError as e:
        logger.warning(f"⚠️  Could not import user_setup module: {e}")
        logger.warning("   Continuing with current user")
        return os.getuid(), os.getgid()
    except Exception as e:
        logger.warning(f"⚠️  User setup error: {e}")
        logger.warning("   Continuing with current user")
        return os.getuid(), os.getgid()


def run_model_initialization() -> bool:
    """
    Run the model initialization module.

    Returns:
        True if initialization succeeded
    """
    logger.info("=" * 60)
    logger.info("  Phase 2: Model Initialization")
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


def drop_to_user(puid: int, pgid: int) -> None:
    """
    Drop privileges to the specified user/group.

    Args:
        puid: User ID to switch to
        pgid: Group ID to switch to
    """
    try:
        from src.startup.user_setup import drop_privileges, is_root

        if is_root():
            logger.info("")
            logger.info("=" * 60)
            logger.info("  Phase 3: Dropping Privileges")
            logger.info("=" * 60)
            drop_privileges(puid, pgid)
            logger.info("")
    except ImportError:
        logger.debug("user_setup module not available, skipping privilege drop")
    except Exception as e:
        logger.warning(f"⚠️  Could not drop privileges: {e}")


def start_server() -> int:
    """
    Start the uvicorn server.

    Returns:
        Exit code from uvicorn
    """
    logger.info("")
    logger.info("=" * 60)
    logger.info("  Phase 4: Starting Server")
    logger.info("=" * 60)

    # Get configuration from environment
    host = os.environ.get("NLP_API_HOST", "0.0.0.0")
    port = os.environ.get("NLP_API_PORT", "30880")
    workers = os.environ.get("NLP_API_WORKERS", "1")
    log_level = os.environ.get("NLP_LOG_LEVEL", "INFO").lower()

    logger.info(f"📡 Starting server at http://{host}:{port}")
    logger.info(f"👷 Workers: {workers}")
    logger.info(f"📝 Log level: {log_level}")
    logger.info(f"🔑 Running as UID={os.getuid()}, GID={os.getgid()}")
    logger.info("")

    # Build uvicorn command
    cmd = [
        sys.executable,  # Use same Python interpreter
        "-m",
        "uvicorn",
        "src.api.app:app",
        "--host",
        host,
        "--port",
        port,
        "--workers",
        workers,
        "--log-level",
        log_level,
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

    Runs:
    1. User setup (PUID/PGID configuration)
    2. Model initialization
    3. Privilege drop
    4. Server startup

    Returns:
        Exit code
    """
    logger.info("")
    logger.info("🚀 Ash-NLP Container Entrypoint")
    logger.info(f"   Version: {__version__}")
    logger.info("")

    # Phase 1: Setup user and permissions (runs as root if available)
    puid, pgid = run_user_setup()

    # Phase 2: Initialize models (still as root to ensure cache writes work)
    run_model_initialization()

    # Phase 3: Drop privileges to configured user
    drop_to_user(puid, pgid)

    # Phase 4: Start server
    return start_server()


if __name__ == "__main__":
    sys.exit(main())
