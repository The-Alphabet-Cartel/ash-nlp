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
Main Entry Point for Ash-NLP Service
---
FILE VERSION: v5.0-6-1.0-2
LAST MODIFIED: 2026-01-17
PHASE: Phase 6 - Logging Colorization Enforcement
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

USAGE:
    # Run with default settings
    python main.py

    # Run with custom settings
    python main.py --host 0.0.0.0 --port 30880 --workers 1

    # Run in development mode
    python main.py --reload --env development

    # Or use uvicorn directly
    uvicorn src.api.app:app --host 0.0.0.0 --port 30880

ENVIRONMENT VARIABLES:
    NLP_API_HOST - Server host (default: 0.0.0.0)
    NLP_API_PORT - Server port (default: 30880)
    NLP_API_WORKERS - Number of workers (default: 4)
    NLP_ENVIRONMENT - Environment name (default: production)
    NLP_LOG_LEVEL - Logging level (default: INFO)
"""

import argparse
import logging
import os
import sys

import uvicorn

# Module version
__version__ = "v5.0-6-1.0-2"

# Default configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 30880
DEFAULT_WORKERS = 1
DEFAULT_ENVIRONMENT = "production"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "human"

# Global logging manager instance (initialized in main)
_logging_manager = None


def get_logging_manager():
    """Get the global logging manager instance."""
    return _logging_manager


def setup_logging(log_level: str = "INFO", log_format: str = "human") -> None:
    """
    Configure logging using Charter v5.2 compliant LoggingConfigManager.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_format: Log format ('human' for colorized, 'json' for structured)
    """
    global _logging_manager

    # Import and create the logging manager
    from src.managers.logging_config_manager import create_logging_config_manager

    _logging_manager = create_logging_config_manager(
        log_level=log_level,
        log_format=log_format,
        app_name="ash-nlp",
    )

    logger = _logging_manager.get_logger("main")
    logger.info(f"Logging configured at {log_level} level ({log_format} format)")
    logger.success("Charter v5.2 colorized logging active")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Ash-NLP Crisis Detection Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run with defaults
  python main.py --port 8080              # Custom port
  python main.py --reload --env testing   # Development mode
  python main.py --workers 8              # Production with 8 workers

Environment Variables:
  NLP_API_HOST, NLP_API_PORT, NLP_API_WORKERS, NLP_ENVIRONMENT, NLP_LOG_LEVEL
        """,
    )

    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("NLP_API_HOST", DEFAULT_HOST),
        help=f"Server host (default: {DEFAULT_HOST})",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("NLP_API_PORT", DEFAULT_PORT)),
        help=f"Server port (default: {DEFAULT_PORT})",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.getenv("NLP_API_WORKERS", DEFAULT_WORKERS)),
        help=f"Number of worker processes (default: {DEFAULT_WORKERS})",
    )

    parser.add_argument(
        "--env",
        "--environment",
        type=str,
        dest="environment",
        default=os.getenv("NLP_ENVIRONMENT", DEFAULT_ENVIRONMENT),
        choices=["production", "testing", "development"],
        help=f"Environment name (default: {DEFAULT_ENVIRONMENT})",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default=os.getenv("NLP_LOG_LEVEL", DEFAULT_LOG_LEVEL),
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help=f"Logging level (default: {DEFAULT_LOG_LEVEL})",
    )

    parser.add_argument(
        "--log-format",
        type=str,
        default=os.getenv("NLP_LOG_FORMAT", DEFAULT_LOG_FORMAT),
        choices=["human", "json"],
        help=f"Log format (default: {DEFAULT_LOG_FORMAT})",
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (development only)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Ash-NLP {__version__}",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for running the service.
    """
    # Parse arguments
    args = parse_args()

    # Setup logging with Charter v5.2 colorization
    setup_logging(args.log_level, args.log_format)

    logger = _logging_manager.get_logger("main")

    # Print startup banner
    logger.info("=" * 60)
    logger.info("  Ash-NLP Crisis Detection Service")
    logger.info(f"  Version: {__version__}")
    logger.info(f"  Environment: {args.environment}")
    logger.info("=" * 60)

    # Set environment variable for the app to pick up
    os.environ["NLP_ENVIRONMENT"] = args.environment

    # Configure uvicorn
    uvicorn_config = {
        "app": "src.api.app:app",
        "host": args.host,
        "port": args.port,
        "log_level": args.log_level.lower(),
        "access_log": True,
    }

    # Development vs Production settings
    if args.reload or args.environment == "development":
        logger.info("🔧 Running in DEVELOPMENT mode (auto-reload enabled)")
        uvicorn_config["reload"] = True
        uvicorn_config["workers"] = 1  # Reload doesn't work with multiple workers
    else:
        logger.info(f"🚀 Running in PRODUCTION mode ({args.workers} workers)")
        uvicorn_config["workers"] = args.workers

    logger.info(f"📡 Starting server at http://{args.host}:{args.port}")
    logger.info(f"📚 API docs available at http://{args.host}:{args.port}/docs")

    # Run the server
    try:
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
